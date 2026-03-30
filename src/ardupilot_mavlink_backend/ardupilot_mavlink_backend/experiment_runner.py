from __future__ import annotations

import argparse
import csv
import math
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fep_core.config import RunConfig, clamp, euler_to_quaternion, load_run_config
from fep_core.io import capture_host_snapshot, ensure_run_directories, write_single_row_csv, write_yaml
from fep_core.milestone import capability_level, milestone_id, schema_version
from fep_core.mav_params import fetch_parameter, set_parameter, set_parameters, snapshot_parameters
from fep_core.paths import ARDUPILOT_ROOT, ARDUPILOT_RUNS_ROOT
from fep_core.profiles import ProfileGenerator
from pymavlink import mavutil

from .bin_log_metrics import summarize_bin_log
from .session import (
    cleanup_residual_processes,
    connect,
    start_sitl as start_sitl_process,
    stop_process,
    wait_for_message,
    wait_for_mode,
    wait_for_takeoff_altitude,
)


BACKEND_NAME = "ardupilot_mavlink"
DEFAULT_MASTER = "tcp:127.0.0.1:5760"
EARTH_RADIUS_M = 6378137.0
ATTITUDE_FIELDNAMES = ["received_time_ns", "roll", "pitch", "yaw", "rollspeed", "pitchspeed", "yawspeed"]
LOCAL_POSITION_FIELDNAMES = ["received_time_ns", "x", "y", "z", "vx", "vy", "vz"]
HEARTBEAT_FIELDNAMES = ["received_time_ns", "base_mode", "custom_mode", "system_status"]
STATUS_FIELDNAMES = ["received_time_ns", "voltage_battery", "current_battery", "battery_remaining", "drop_rate_comm"]
INPUT_TRACE_FIELDNAMES = ["publish_time_ns", "elapsed_s", "profile_value", "roll_body", "pitch_body", "yaw_body", "thrust_z", "phase"]
METRICS_FIELDNAMES = [
    "run_id",
    "backend",
    "study_layer",
    "study_role",
    "mode_under_test",
    "parameter_group",
    "parameter_set_name",
    "input_chain",
    "profile_type",
    "axis",
    "input_peak",
    "heartbeat_count",
    "attitude_samples",
    "local_position_samples",
    "status_samples",
    "failsafe_event",
    "tracking_error_peak",
    "tracking_error_rms",
    "rate_tracking_error_peak",
    "rate_tracking_error_rms",
    "response_delay_ms",
    "start_xy_radius_m",
    "end_xy_radius_m",
    "xy_radius_peak_m",
    "xy_displacement_peak_m",
    "clip_frac",
    "thlimit_peak",
    "max_motor_output",
    "oracle_valid",
    "oracle_failure_reason",
    "stress_class",
    "mechanism_flags",
    "rate_layer_recommended",
    "rate_layer_reasons",
    "attribution_boundary",
    "bin_parse_status",
    "bin_message_counts",
]


def _safe_float(value: Any, default: float = math.nan) -> float:
    if value in ("", None):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    if value in ("", None):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _snapshot_logs(root: Path, suffixes: tuple[str, ...]) -> dict[str, float]:
    if not root.exists():
        return {}
    files: dict[str, float] = {}
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in suffixes and path.name.lower() != "eeprom.bin":
            files[str(path)] = path.stat().st_mtime
    return files


def _resolve_latest_file(before: dict[str, float], after: dict[str, float]) -> str | None:
    candidates = [path for path in after if path not in before]
    if not candidates:
        candidates = list(after.keys())
    if not candidates:
        return None
    candidates.sort(key=lambda item: after[item], reverse=True)
    return candidates[0]


def _set_mode(master: mavutil.mavfile, mode_name: str) -> bool:
    try:
        master.set_mode_apm(mode_name)
        return True
    except Exception:
        mapping = master.mode_mapping() or {}
        if mode_name not in mapping:
            return False
        master.mav.set_mode_send(
            master.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mapping[mode_name],
        )
        return True


def _wait_for_armed(master: mavutil.mavfile, timeout_s: float = 15.0) -> bool:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if master.motors_armed():
            return True
        message = master.recv_match(type="HEARTBEAT", blocking=True, timeout=0.5)
        if message is not None and int(getattr(message, "base_mode", 0) or 0) & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED:
            return True
        time.sleep(0.2)
    return master.motors_armed()


def _arm_and_takeoff(master: mavutil.mavfile, target_altitude_m: float) -> list[str]:
    anomalies: list[str] = []
    if not _set_mode(master, "GUIDED"):
        anomalies.append("guided_mode_unavailable")
        return anomalies
    if not wait_for_mode(master, "GUIDED", timeout_s=10.0):
        anomalies.append("guided_mode_not_confirmed")
        return anomalies
    try:
        master.arducopter_arm()
        if not _wait_for_armed(master, timeout_s=15.0):
            anomalies.append("arm_failed")
            return anomalies
    except Exception:
        anomalies.append("arm_failed")
        return anomalies
    try:
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            target_altitude_m,
        )
    except Exception:
        anomalies.append("takeoff_command_failed")
        return anomalies
    if not wait_for_takeoff_altitude(master, target_altitude_m, timeout_s=20.0):
        anomalies.append("takeoff_altitude_not_reached")
    return anomalies


def _wait_for_position_message(master: mavutil.mavfile, timeout_s: float = 10.0):
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        message = master.recv_match(blocking=True, timeout=0.5)
        if message is None:
            continue
        if message.get_type() in {"LOCAL_POSITION_NED", "GLOBAL_POSITION_INT"}:
            return message
    return None


def _wait_for_vehicle_ready(master: mavutil.mavfile, timeout_s: float = 20.0) -> list[str]:
    deadline = time.monotonic() + timeout_s
    position_ready = False
    autopilot_ready = False
    origin_ready = False

    while time.monotonic() < deadline and not (position_ready and autopilot_ready and origin_ready):
        message = master.recv_match(blocking=True, timeout=0.5)
        if message is None:
            continue
        message_type = message.get_type()
        if message_type in {"LOCAL_POSITION_NED", "GLOBAL_POSITION_INT"}:
            position_ready = True
            continue
        if message_type != "STATUSTEXT":
            continue
        text = str(getattr(message, "text", "")).strip()
        if text == "ArduPilot Ready":
            autopilot_ready = True
        if "origin set" in text:
            origin_ready = True

    anomalies: list[str] = []
    if not position_ready:
        anomalies.append("position_unavailable")
    if not autopilot_ready:
        anomalies.append("autopilot_ready_text_missing")
    if not origin_ready:
        anomalies.append("ekf_origin_not_ready")
    return anomalies


def _arm_vehicle(master: mavutil.mavfile, mode_name: str, timeout_s: float = 15.0) -> list[str]:
    anomalies: list[str] = []
    if not _set_mode(master, mode_name):
        anomalies.append(f"mode_under_test_unavailable:{mode_name}")
        return anomalies
    if not wait_for_mode(master, mode_name, timeout_s=10.0):
        anomalies.append(f"mode_under_test_not_confirmed:{mode_name}")
        return anomalies
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        try:
            master.arducopter_arm()
        except Exception:
            pass
        remaining_s = max(0.5, min(2.0, deadline - time.monotonic()))
        if _wait_for_armed(master, timeout_s=remaining_s):
            return anomalies
        time.sleep(0.5)
    anomalies.append("arm_failed")
    return anomalies


def _land_vehicle(master: mavutil.mavfile) -> None:
    if not _set_mode(master, "LAND"):
        try:
            master.mav.command_long_send(
                master.target_system,
                master.target_component,
                mavutil.mavlink.MAV_CMD_NAV_LAND,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            )
        except Exception:
            return


def _send_attitude_target(master: mavutil.mavfile, roll: float, pitch: float, yaw: float, thrust_z: float) -> None:
    quaternion = euler_to_quaternion(roll, pitch, yaw)
    thrust = clamp(-thrust_z, 0.0, 1.0)
    type_mask = (
        mavutil.mavlink.ATTITUDE_TARGET_TYPEMASK_BODY_ROLL_RATE_IGNORE
        | mavutil.mavlink.ATTITUDE_TARGET_TYPEMASK_BODY_PITCH_RATE_IGNORE
        | mavutil.mavlink.ATTITUDE_TARGET_TYPEMASK_BODY_YAW_RATE_IGNORE
    )
    master.mav.set_attitude_target_send(
        int(time.time() * 1000) & 0xFFFFFFFF,
        master.target_system,
        master.target_component,
        type_mask,
        quaternion,
        0.0,
        0.0,
        0.0,
        thrust,
    )


def _send_rate_target(
    master: mavutil.mavfile,
    roll_rate: float,
    pitch_rate: float,
    yaw_rate: float,
    thrust_z: float,
) -> None:
    type_mask = mavutil.mavlink.ATTITUDE_TARGET_TYPEMASK_ATTITUDE_IGNORE
    master.mav.set_attitude_target_send(
        int(time.time() * 1000) & 0xFFFFFFFF,
        master.target_system,
        master.target_component,
        type_mask,
        [1.0, 0.0, 0.0, 0.0],
        float(roll_rate),
        float(pitch_rate),
        float(yaw_rate),
        clamp(-thrust_z, 0.0, 1.0),
    )


def _send_manual_control(master: mavutil.mavfile, roll: float, pitch: float, yaw: float, throttle_norm: float) -> None:
    master.mav.manual_control_send(
        master.target_system,
        int(clamp(pitch, -1.0, 1.0) * 1000.0),
        int(clamp(roll, -1.0, 1.0) * 1000.0),
        int(clamp(throttle_norm, 0.0, 1.0) * 1000.0),
        int(clamp(yaw, -1.0, 1.0) * 1000.0),
        0,
    )


def _append_message_rows(
    master: mavutil.mavfile,
    attitude_rows: list[dict[str, Any]],
    position_rows: list[dict[str, Any]],
    heartbeat_rows: list[dict[str, Any]],
    status_rows: list[dict[str, Any]],
    position_origin: dict[str, float] | None = None,
) -> dict[str, float] | None:
    while True:
        message = master.recv_match(blocking=False)
        if message is None:
            return position_origin
        message_type = message.get_type()
        now_ns = time.time_ns()
        if message_type == "ATTITUDE":
            attitude_rows.append(
                {
                    "received_time_ns": now_ns,
                    "roll": _safe_float(getattr(message, "roll", None)),
                    "pitch": _safe_float(getattr(message, "pitch", None)),
                    "yaw": _safe_float(getattr(message, "yaw", None)),
                    "rollspeed": _safe_float(getattr(message, "rollspeed", None)),
                    "pitchspeed": _safe_float(getattr(message, "pitchspeed", None)),
                    "yawspeed": _safe_float(getattr(message, "yawspeed", None)),
                }
            )
        elif message_type == "LOCAL_POSITION_NED":
            position_rows.append(
                {
                    "received_time_ns": now_ns,
                    "x": _safe_float(getattr(message, "x", None)),
                    "y": _safe_float(getattr(message, "y", None)),
                    "z": _safe_float(getattr(message, "z", None)),
                    "vx": _safe_float(getattr(message, "vx", None)),
                    "vy": _safe_float(getattr(message, "vy", None)),
                    "vz": _safe_float(getattr(message, "vz", None)),
                }
            )
        elif message_type == "GLOBAL_POSITION_INT":
            lat = _safe_float(getattr(message, "lat", None))
            lon = _safe_float(getattr(message, "lon", None))
            relative_alt = _safe_float(getattr(message, "relative_alt", None))
            if any(math.isnan(value) for value in (lat, lon, relative_alt)):
                continue
            lat_deg = lat / 1.0e7
            lon_deg = lon / 1.0e7
            if position_origin is None:
                position_origin = {
                    "lat_deg": lat_deg,
                    "lon_deg": lon_deg,
                }
            origin_lat_rad = math.radians(position_origin["lat_deg"])
            origin_lon_rad = math.radians(position_origin["lon_deg"])
            lat_rad = math.radians(lat_deg)
            lon_rad = math.radians(lon_deg)
            position_rows.append(
                {
                    "received_time_ns": now_ns,
                    "x": EARTH_RADIUS_M * (lat_rad - origin_lat_rad),
                    "y": EARTH_RADIUS_M * math.cos(origin_lat_rad) * (lon_rad - origin_lon_rad),
                    "z": -(relative_alt / 1000.0),
                    "vx": _safe_float(getattr(message, "vx", None)) / 100.0,
                    "vy": _safe_float(getattr(message, "vy", None)) / 100.0,
                    "vz": _safe_float(getattr(message, "vz", None)) / 100.0,
                }
            )
        elif message_type == "HEARTBEAT":
            heartbeat_rows.append(
                {
                    "received_time_ns": now_ns,
                    "base_mode": _safe_int(getattr(message, "base_mode", None)),
                    "custom_mode": _safe_int(getattr(message, "custom_mode", None)),
                    "system_status": _safe_int(getattr(message, "system_status", None)),
                }
            )
        elif message_type == "SYS_STATUS":
            status_rows.append(
                {
                    "received_time_ns": now_ns,
                    "voltage_battery": _safe_int(getattr(message, "voltage_battery", None)),
                    "current_battery": _safe_int(getattr(message, "current_battery", None)),
                    "battery_remaining": _safe_int(getattr(message, "battery_remaining", None)),
                    "drop_rate_comm": _safe_int(getattr(message, "drop_rate_comm", None)),
                }
            )


def _write_telemetry_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _prepare_parameters(master: mavutil.mavfile, config: RunConfig) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    parameter_names = list(dict.fromkeys(config.controlled_parameters_for_backend("ardupilot")))
    parameter_names.extend(
        name for name in config.parameter_overrides_for_backend("ardupilot") if name not in parameter_names
    )
    if "ARMING_CHECK" not in parameter_names:
        parameter_names.append("ARMING_CHECK")
    if not parameter_names:
        return {}, {}, []

    anomalies: list[str] = []
    before = snapshot_parameters(master, parameter_names, timeout_s=2.0)
    overrides = config.parameter_overrides_for_backend("ardupilot")
    if overrides:
        apply_results = set_parameters(master, overrides, timeout_s=2.0)
        failed = [name for name, ok in apply_results.items() if not ok]
        if failed:
            anomalies.append(f"parameter_apply_failed:{','.join(failed)}")
    after_apply = snapshot_parameters(master, parameter_names, timeout_s=2.0)
    return before, after_apply, anomalies


def _prepare_runtime_arming(master: mavutil.mavfile, parameter_snapshot_after: dict[str, Any]) -> list[str]:
    if "ARMING_CHECK" not in parameter_snapshot_after:
        current = fetch_parameter(master, "ARMING_CHECK", timeout_s=2.0)
        if current is not None:
            parameter_snapshot_after["ARMING_CHECK"] = current
    if not set_parameter(master, "ARMING_CHECK", 0.0, timeout_s=5.0):
        return ["arming_check_disable_failed"]
    parameter_snapshot_after["ARMING_CHECK"] = 0.0
    return []


def _restore_parameters(master: mavutil.mavfile, snapshot_before: dict[str, Any]) -> list[str]:
    if not snapshot_before:
        return []
    restore_values = {name: value for name, value in snapshot_before.items() if value not in ("", None)}
    if not restore_values:
        return []
    try:
        results = set_parameters(master, restore_values, timeout_s=2.0)
    except Exception as exc:
        return [f"parameter_restore_failed:{type(exc).__name__}"]

    failed = [name for name, ok in results.items() if not ok]
    if failed:
        return [f"parameter_restore_failed:{','.join(failed)}"]
    return []


def _xy_motion_metrics(position_rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not position_rows:
        return {
            "start_xy_radius_m": math.nan,
            "end_xy_radius_m": math.nan,
            "xy_radius_peak_m": math.nan,
            "xy_displacement_peak_m": math.nan,
        }
    x0 = float(position_rows[0]["x"])
    y0 = float(position_rows[0]["y"])
    start_xy_radius_m = math.hypot(x0, y0)
    end_xy_radius_m = math.hypot(float(position_rows[-1]["x"]), float(position_rows[-1]["y"]))
    xy_radius_peak_m = max(math.hypot(float(row["x"]), float(row["y"])) for row in position_rows)
    xy_displacement_peak_m = max(
        math.hypot(float(row["x"]) - x0, float(row["y"]) - y0) for row in position_rows
    )
    return {
        "start_xy_radius_m": round(start_xy_radius_m, 3),
        "end_xy_radius_m": round(end_xy_radius_m, 3),
        "xy_radius_peak_m": round(xy_radius_peak_m, 3),
        "xy_displacement_peak_m": round(xy_displacement_peak_m, 3),
    }


def _mechanism_flags(metrics: dict[str, Any], anomalies: list[str]) -> list[str]:
    flags: list[str] = []
    if metrics.get("failsafe_event") == 1:
        flags.append("failsafe")
    if any(item.startswith("parameter_") for item in anomalies):
        flags.append("parameter_session_issue")
    if float(metrics.get("clip_frac", 0.0) or 0.0) >= 0.02:
        flags.append("motor_clipping")
    if float(metrics.get("thlimit_peak", 0.0) or 0.0) >= 1.0:
        flags.append("thrust_limited")
    if float(metrics.get("tracking_error_peak", 0.0) or 0.0) >= 0.25:
        flags.append("tracking_error_high")
    if float(metrics.get("response_delay_ms", 0.0) or 0.0) >= 250.0:
        flags.append("response_delay_high")
    if float(metrics.get("xy_displacement_peak_m", 0.0) or 0.0) >= 15.0:
        flags.append("xy_drift_high")
    return flags


def _stress_class(metrics: dict[str, Any], run_status: str, mechanism_flags: list[str]) -> str:
    if run_status != "completed" or metrics.get("failsafe_event") == 1:
        return "saturated"
    if any(flag in mechanism_flags for flag in {"motor_clipping", "thrust_limited", "xy_drift_high"}):
        return "saturated"
    if any(flag in mechanism_flags for flag in {"tracking_error_high", "response_delay_high"}):
        return "stressed"
    return "nominal"


def _oracle_decision(config: RunConfig, metrics: dict[str, Any], run_status: str, anomalies: list[str]) -> tuple[int, str]:
    if run_status != "completed":
        return 0, f"run_status:{run_status}"
    if metrics.get("failsafe_event") == 1:
        return 0, "failsafe_event"
    if "bin_log_missing" in anomalies:
        return 0, "missing_bin_log"
    if config.resolved_study_layer == "manual_whole_loop":
        if float(metrics.get("xy_displacement_peak_m", 0.0) or 0.0) >= float(
            config.extras.get("oracle_manual_xy_displacement_limit_m", 25.0)
        ):
            return 0, "manual_xy_drift_high"
    elif config.resolved_study_layer == "attitude_explicit":
        if float(metrics.get("tracking_error_peak", 0.0) or 0.0) >= float(
            config.extras.get("oracle_attitude_tracking_error_peak_limit", 0.35)
        ):
            return 0, "attitude_tracking_error_peak_high"
        if float(metrics.get("tracking_error_rms", 0.0) or 0.0) >= float(
            config.extras.get("oracle_attitude_tracking_error_rms_limit", 0.20)
        ):
            return 0, "attitude_tracking_error_rms_high"
        if float(metrics.get("response_delay_ms", 0.0) or 0.0) >= float(
            config.extras.get("oracle_attitude_response_delay_ms_limit", 400.0)
        ):
            return 0, "attitude_response_delay_high"
    else:
        if float(metrics.get("rate_tracking_error_peak", 0.0) or 0.0) >= float(
            config.extras.get("oracle_rate_tracking_error_peak_limit", 0.60)
        ):
            return 0, "rate_tracking_error_peak_high"
    return 1, "valid"


def _rate_layer_recommendation(
    config: RunConfig,
    oracle_valid: int,
    mechanism_flags: list[str],
) -> tuple[int, list[str]]:
    reasons = list(config.rate_layer_recommended_reasons())
    if config.resolved_study_layer == "attitude_explicit" and oracle_valid == 0 and not mechanism_flags:
        reasons.append("attitude_difference_unexplained_by_current_mechanisms")
    if config.resolved_study_layer == "attitude_explicit" and "tracking_error_high" in mechanism_flags:
        reasons.append("attitude_tracking_difference_needs_rate_attribution")
    deduped = list(dict.fromkeys(reasons))
    return (1 if deduped else 0), deduped


def _notes_text(
    run_id: str,
    config: RunConfig,
    study: dict[str, Any],
    run_status: str,
    anomalies: list[str],
    metrics: dict[str, Any],
    bin_log_path: str | None,
    tlog_path: Path,
    vehicle: str,
    frame: str,
) -> str:
    return "\n".join(
        [
            f"# {run_id}",
            f"- backend: {BACKEND_NAME}",
            f"- vehicle/frame: {vehicle}/{frame}",
            f"- study_layer: {study['study_layer']}",
            f"- study_role: {study['study_role']}",
            f"- mode_under_test: {study['mode_under_test']}",
            f"- parameter_group: {study['parameter_group']}",
            f"- parameter_set_name: {study['parameter_set_name']}",
            f"- takeoff_altitude_m: {config.takeoff_altitude_m}",
            f"- manual_throttle_bias: {float(config.extras.get('ardupilot_manual_throttle_bias', 0.65))}",
            f"- manual_throttle_scale: {float(config.extras.get('ardupilot_manual_throttle_scale', 0.30))}",
            f"- controlled_parameters: {', '.join(study['controlled_parameters'])}",
            f"- status: {run_status}",
            f"- oracle_valid: {metrics.get('oracle_valid', '')}",
            f"- oracle_failure_reason: {metrics.get('oracle_failure_reason', '')}",
            f"- stress_class: {metrics.get('stress_class', '')}",
            f"- ardupilot_bin_log_path: {bin_log_path or 'missing'}",
            f"- ardupilot_tlog_path: {tlog_path}",
            f"- anomalies: {', '.join(anomalies) if anomalies else 'none'}",
            f"- attribution_boundary: {config.resolved_attribution_boundary}",
        ]
    )


def run_experiment(
    config: RunConfig,
    vehicle: str = "ArduCopter",
    frame: str = "quad",
    master_uri: str = DEFAULT_MASTER,
    start_sitl: bool = True,
    connect_timeout_s: float = 60.0,
    arm_and_takeoff: bool = True,
    sitl_log_path: Path | None = None,
) -> tuple[int, Path]:
    start_time = datetime.now(timezone.utc).astimezone()
    run_id = config.build_run_id(start_time)
    study = config.study_metadata("ardupilot")
    paths = ensure_run_directories(ARDUPILOT_RUNS_ROOT, run_id)
    resolved_sitl_log_path = sitl_log_path or (paths["base_dir"] / "ardupilot_sitl.log")
    tlog_path = paths["telemetry_dir"] / "ardupilot.tlog"

    bin_before = _snapshot_logs(ARDUPILOT_ROOT, (".bin",))
    host_start = capture_host_snapshot()
    anomalies: list[str] = []
    input_profile_rows: list[dict[str, Any]] = []
    attitude_rows: list[dict[str, Any]] = []
    position_rows: list[dict[str, Any]] = []
    heartbeat_rows: list[dict[str, Any]] = []
    status_rows: list[dict[str, Any]] = []
    profile = ProfileGenerator(config)
    position_origin: dict[str, float] | None = None

    process = None
    master: mavutil.mavfile | None = None
    run_status = "completed"
    parameter_snapshot_before: dict[str, Any] = {}
    parameter_snapshot_after: dict[str, Any] = {}

    try:
        if start_sitl:
            cleanup_residual_processes()
            process = start_sitl_process(run_id, vehicle, frame, resolved_sitl_log_path)

        master = connect(master_uri, tlog_path, connect_timeout_s)
        readiness_anomalies = _wait_for_vehicle_ready(
            master,
            timeout_s=float(config.extras.get("ardupilot_ready_timeout_s", 20.0)),
        )
        anomalies.extend(readiness_anomalies)
        if readiness_anomalies:
            run_status = "invalid_runtime"
        parameter_snapshot_before, parameter_snapshot_after, parameter_anomalies = _prepare_parameters(master, config)
        anomalies.extend(parameter_anomalies)
        anomalies.extend(_prepare_runtime_arming(master, parameter_snapshot_after))
        if "arming_check_disable_failed" in anomalies:
            run_status = "invalid_runtime"

        desired_mode = study["mode_under_test"]
        arming_mode = desired_mode if config.resolved_study_layer == "manual_whole_loop" else "GUIDED_NOGPS"
        if run_status == "completed":
            anomalies.extend(_arm_vehicle(master, arming_mode))
            if any(
                item in {
                    "arm_failed",
                    f"mode_under_test_unavailable:{arming_mode}",
                    f"mode_under_test_not_confirmed:{arming_mode}",
                }
                for item in anomalies
            ):
                run_status = "invalid_runtime"

        started = time.monotonic()
        end_deadline = started + profile.total_duration_s + float(config.extras.get("ardupilot_tail_s", 2.0))
        manual_bias = float(config.extras.get("ardupilot_manual_throttle_bias", 0.65))
        manual_scale = float(config.extras.get("ardupilot_manual_throttle_scale", 0.30))

        while run_status == "completed" and time.monotonic() < end_deadline:
            elapsed_s = time.monotonic() - started
            if config.resolved_study_layer == "manual_whole_loop":
                profile_value, roll, pitch, yaw, throttle, phase = profile.manual_targets_at(elapsed_s)
                throttle_norm = manual_bias
                if config.axis in {"throttle", "composite"}:
                    throttle_norm = clamp(manual_bias + (throttle * manual_scale), 0.0, 1.0)
                _send_manual_control(master, roll, pitch, yaw, throttle_norm)
                input_profile_rows.append(
                    {
                        "publish_time_ns": time.time_ns(),
                        "elapsed_s": round(elapsed_s, 6),
                        "profile_value": profile_value,
                        "roll_body": roll,
                        "pitch_body": pitch,
                        "yaw_body": yaw,
                        "thrust_z": throttle_norm,
                        "phase": phase,
                    }
                )
            elif config.resolved_study_layer == "attitude_explicit":
                profile_value, roll_body, pitch_body, yaw_body, thrust_z, phase = profile.attitude_targets_at(elapsed_s)
                _send_attitude_target(master, roll_body, pitch_body, yaw_body, thrust_z)
                input_profile_rows.append(
                    {
                        "publish_time_ns": time.time_ns(),
                        "elapsed_s": round(elapsed_s, 6),
                        "profile_value": profile_value,
                        "roll_body": roll_body,
                        "pitch_body": pitch_body,
                        "yaw_body": yaw_body,
                        "thrust_z": thrust_z,
                        "phase": phase,
                    }
                )
            else:
                profile_value, roll_rate, pitch_rate, yaw_rate, thrust_z, phase = profile.rate_targets_at(elapsed_s)
                _send_rate_target(master, roll_rate, pitch_rate, yaw_rate, thrust_z)
                input_profile_rows.append(
                    {
                        "publish_time_ns": time.time_ns(),
                        "elapsed_s": round(elapsed_s, 6),
                        "profile_value": profile_value,
                        "roll_body": roll_rate,
                        "pitch_body": pitch_rate,
                        "yaw_body": yaw_rate,
                        "thrust_z": thrust_z,
                        "phase": phase,
                    }
                )
            position_origin = _append_message_rows(
                master,
                attitude_rows,
                position_rows,
                heartbeat_rows,
                status_rows,
                position_origin,
            )
            time.sleep(config.period_s)
    except Exception as exc:
        anomalies.append(f"runtime_error:{type(exc).__name__}")
        run_status = "invalid_runtime"
    finally:
        if master is not None:
            try:
                _land_vehicle(master)
                time.sleep(float(config.extras.get("ardupilot_land_settle_s", 2.0)))
                position_origin = _append_message_rows(
                    master,
                    attitude_rows,
                    position_rows,
                    heartbeat_rows,
                    status_rows,
                    position_origin,
                )
                if parameter_snapshot_after != parameter_snapshot_before:
                    anomalies.extend(_restore_parameters(master, parameter_snapshot_before))
                master.close()
            except Exception:
                pass
        stop_process(process)
        cleanup_residual_processes()

    end_time = datetime.now(timezone.utc).astimezone()
    host_end = capture_host_snapshot()
    bin_after = _snapshot_logs(ARDUPILOT_ROOT, (".bin",))
    bin_log_path = _resolve_latest_file(bin_before, bin_after)
    copied_bin_path: str | None = None
    if bin_log_path is not None:
        destination = paths["telemetry_dir"] / "ardupilot.BIN"
        shutil.copy2(bin_log_path, destination)
        copied_bin_path = str(destination)
    else:
        anomalies.append("bin_log_missing")

    _write_telemetry_csv(paths["telemetry_dir"] / "attitude.csv", attitude_rows, ATTITUDE_FIELDNAMES)
    _write_telemetry_csv(paths["telemetry_dir"] / "local_position.csv", position_rows, LOCAL_POSITION_FIELDNAMES)
    _write_telemetry_csv(paths["telemetry_dir"] / "heartbeat.csv", heartbeat_rows, HEARTBEAT_FIELDNAMES)
    _write_telemetry_csv(paths["telemetry_dir"] / "sys_status.csv", status_rows, STATUS_FIELDNAMES)
    _write_telemetry_csv(paths["input_trace_path"], input_profile_rows, INPUT_TRACE_FIELDNAMES)

    metrics: dict[str, Any] = {
        "run_id": run_id,
        "backend": BACKEND_NAME,
        "study_layer": study["study_layer"],
        "study_role": study["study_role"],
        "mode_under_test": study["mode_under_test"],
        "parameter_group": study["parameter_group"],
        "parameter_set_name": study["parameter_set_name"],
        "input_chain": config.input_chain,
        "profile_type": config.profile_type,
        "axis": config.axis,
        "input_peak": abs(config.amplitude),
        "heartbeat_count": len(heartbeat_rows),
        "attitude_samples": len(attitude_rows),
        "local_position_samples": len(position_rows),
        "status_samples": len(status_rows),
        "failsafe_event": int(any(row["system_status"] >= mavutil.mavlink.MAV_STATE_CRITICAL for row in heartbeat_rows)),
        "tracking_error_peak": math.nan,
        "tracking_error_rms": math.nan,
        "rate_tracking_error_peak": math.nan,
        "rate_tracking_error_rms": math.nan,
        "response_delay_ms": math.nan,
        "clip_frac": 0.0,
        "thlimit_peak": math.nan,
        "max_motor_output": math.nan,
    }
    metrics.update(_xy_motion_metrics(position_rows))

    if copied_bin_path is not None:
        try:
            metrics.update(summarize_bin_log(config, copied_bin_path, telemetry_dir=paths["telemetry_dir"]))
        except Exception as exc:
            anomalies.append(f"bin_parse_failed:{type(exc).__name__}")
            metrics["bin_parse_status"] = "parse_failed"
    else:
        metrics["bin_parse_status"] = "missing"

    if metrics["failsafe_event"] == 1:
        run_status = "invalid_runtime"

    mechanism_flags = _mechanism_flags(metrics, anomalies)
    metrics["stress_class"] = _stress_class(metrics, run_status, mechanism_flags)
    oracle_valid, oracle_failure_reason = _oracle_decision(config, metrics, run_status, anomalies)
    metrics["oracle_valid"] = oracle_valid
    metrics["oracle_failure_reason"] = oracle_failure_reason
    metrics["mechanism_flags"] = ",".join(mechanism_flags)
    rate_layer_recommended, rate_layer_reasons = _rate_layer_recommendation(config, oracle_valid, mechanism_flags)
    metrics["rate_layer_recommended"] = rate_layer_recommended
    metrics["rate_layer_reasons"] = ",".join(rate_layer_reasons)
    metrics["attribution_boundary"] = config.resolved_attribution_boundary

    write_single_row_csv(
        paths["metrics_path"],
        metrics,
        METRICS_FIELDNAMES,
    )

    manifest = {
        "run_id": run_id,
        "backend": BACKEND_NAME,
        "schema_version": schema_version(),
        "milestone_id": milestone_id(),
        "capability_level": capability_level(),
        "phase": config.phase,
        "input_chain": config.input_chain,
        "profile_type": config.profile_type,
        "profile_params": config.profile_params(),
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "status": run_status,
        "vehicle": vehicle,
        "frame": frame,
        "master_uri": master_uri,
        "mode_under_test": study["mode_under_test"],
        "takeoff_altitude_m": config.takeoff_altitude_m,
        "manual_throttle_bias": float(config.extras.get("ardupilot_manual_throttle_bias", 0.65)),
        "manual_throttle_scale": float(config.extras.get("ardupilot_manual_throttle_scale", 0.30)),
        "study": study,
        "ardupilot_bin_log_path": copied_bin_path or bin_log_path,
        "ardupilot_tlog_path": str(tlog_path),
        "host_snapshot_start": host_start,
        "host_snapshot_end": host_end,
        "parameter_snapshot_before": parameter_snapshot_before,
        "parameter_snapshot_after": parameter_snapshot_after,
        "anomaly_summary": anomalies,
    }
    write_yaml(paths["manifest_path"], manifest)
    paths["notes_path"].write_text(
        _notes_text(
            run_id,
            config,
            study,
            run_status,
            anomalies,
            metrics,
            copied_bin_path or bin_log_path,
            tlog_path,
            vehicle,
            frame,
        ),
        encoding="utf-8",
    )
    return (0 if run_status == "completed" else 1), paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="运行 ArduPilot 分层敏感性实验并写入研究产物。")
    parser.add_argument("--config", type=Path, required=True, help="YAML 配置路径。")
    parser.add_argument("--vehicle", default="ArduCopter", help="ArduPilot vehicle，默认 ArduCopter。")
    parser.add_argument("--frame", default="quad", help="SITL frame，默认 quad。")
    parser.add_argument("--master", default=DEFAULT_MASTER, help="MAVLink master URI，默认 tcp:127.0.0.1:5760。")
    parser.add_argument("--skip-sitl", action="store_true", help="连接已有实例，不启动 sim_vehicle.py。")
    parser.add_argument("--no-arm-and-takeoff", action="store_true", help="跳过 GUIDED 起飞流程。")
    args = parser.parse_args(argv)

    config = load_run_config(args.config)
    exit_code, artifact_dir = run_experiment(
        config,
        vehicle=args.vehicle,
        frame=args.frame,
        master_uri=args.master,
        start_sitl=not args.skip_sitl,
        arm_and_takeoff=not args.no_arm_and_takeoff,
    )
    print(f"artifact_dir={artifact_dir}")
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
