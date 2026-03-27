from __future__ import annotations

import argparse
import csv
import math
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fep_core.config import RunConfig, clamp, euler_to_quaternion, load_run_config
from fep_core.io import capture_host_snapshot, ensure_run_directories, write_single_row_csv, write_yaml
from fep_core.mav_params import set_parameters, snapshot_parameters
from fep_core.paths import ARDUPILOT_ROOT, ARDUPILOT_RUNS_ROOT
from fep_core.profiles import ProfileGenerator
from pymavlink import mavutil

from .bin_log_metrics import summarize_bin_log


BACKEND_NAME = "ardupilot_mavlink"
DEFAULT_MASTER = "tcp:127.0.0.1:5760"
ATTITUDE_FIELDNAMES = ["received_time_ns", "roll", "pitch", "yaw", "rollspeed", "pitchspeed", "yawspeed"]
LOCAL_POSITION_FIELDNAMES = ["received_time_ns", "x", "y", "z", "vx", "vy", "vz"]
HEARTBEAT_FIELDNAMES = ["received_time_ns", "base_mode", "custom_mode", "system_status"]
STATUS_FIELDNAMES = ["received_time_ns", "voltage_battery", "current_battery", "battery_remaining", "drop_rate_comm"]
INPUT_TRACE_FIELDNAMES = ["publish_time_ns", "elapsed_s", "profile_value", "roll_body", "pitch_body", "yaw_body", "thrust_z", "phase"]


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


def _start_sitl(run_id: str, vehicle: str, frame: str, log_path: Path) -> subprocess.Popen[str]:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "bash",
        "-lc",
        (
            f"cd {ARDUPILOT_ROOT} && "
            "stdbuf -oL -eL python3 Tools/autotest/sim_vehicle.py "
            f"-v {vehicle} -f {frame} --no-mavproxy -N -w --aircraft {run_id}"
        ),
    ]
    handle = log_path.open("w", encoding="utf-8")
    return subprocess.Popen(command, stdout=handle, stderr=subprocess.STDOUT, text=True)


def _stop_process(process: subprocess.Popen[str] | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=10.0)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5.0)


def _connect(master_uri: str, tlog_path: Path, timeout_s: float) -> mavutil.mavfile:
    master = mavutil.mavlink_connection(master_uri, source_system=250, autoreconnect=True)
    master.setup_logfile_raw(str(tlog_path))
    master.wait_heartbeat(timeout=timeout_s)
    master.mav.request_data_stream_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_ALL,
        20,
        1,
    )
    return master


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
        master.recv_match(blocking=False)
        time.sleep(0.2)
    return master.motors_armed()


def _arm_and_takeoff(master: mavutil.mavfile, target_altitude_m: float) -> list[str]:
    anomalies: list[str] = []
    if not _set_mode(master, "GUIDED"):
        anomalies.append("guided_mode_unavailable")
        return anomalies
    time.sleep(1.0)
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
    time.sleep(6.0)
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
) -> None:
    while True:
        message = master.recv_match(blocking=False)
        if message is None:
            return
        message_type = message.get_type()
        now_ns = time.time_ns()
        if message_type == "ATTITUDE":
            attitude_rows.append(
                {
                    "received_time_ns": now_ns,
                    "roll": float(message.roll),
                    "pitch": float(message.pitch),
                    "yaw": float(message.yaw),
                    "rollspeed": float(message.rollspeed),
                    "pitchspeed": float(message.pitchspeed),
                    "yawspeed": float(message.yawspeed),
                }
            )
        elif message_type == "LOCAL_POSITION_NED":
            position_rows.append(
                {
                    "received_time_ns": now_ns,
                    "x": float(message.x),
                    "y": float(message.y),
                    "z": float(message.z),
                    "vx": float(message.vx),
                    "vy": float(message.vy),
                    "vz": float(message.vz),
                }
            )
        elif message_type == "HEARTBEAT":
            heartbeat_rows.append(
                {
                    "received_time_ns": now_ns,
                    "base_mode": int(message.base_mode),
                    "custom_mode": int(message.custom_mode),
                    "system_status": int(message.system_status),
                }
            )
        elif message_type == "SYS_STATUS":
            status_rows.append(
                {
                    "received_time_ns": now_ns,
                    "voltage_battery": int(message.voltage_battery),
                    "current_battery": int(message.current_battery),
                    "battery_remaining": int(message.battery_remaining),
                    "drop_rate_comm": int(message.drop_rate_comm),
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
) -> str:
    return "\n".join(
        [
            f"# {run_id}",
            f"- backend: {BACKEND_NAME}",
            f"- study_layer: {study['study_layer']}",
            f"- study_role: {study['study_role']}",
            f"- mode_under_test: {study['mode_under_test']}",
            f"- parameter_group: {study['parameter_group']}",
            f"- parameter_set_name: {study['parameter_set_name']}",
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
) -> tuple[int, Path]:
    start_time = datetime.now(timezone.utc).astimezone()
    run_id = config.build_run_id(start_time)
    study = config.study_metadata("ardupilot")
    paths = ensure_run_directories(ARDUPILOT_RUNS_ROOT, run_id)
    sitl_log_path = paths["base_dir"] / "ardupilot_sitl.log"
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

    process: subprocess.Popen[str] | None = None
    master: mavutil.mavfile | None = None
    run_status = "completed"
    parameter_snapshot_before: dict[str, Any] = {}
    parameter_snapshot_after: dict[str, Any] = {}

    try:
        if start_sitl:
            process = _start_sitl(run_id, vehicle, frame, sitl_log_path)
            time.sleep(5.0)

        master = _connect(master_uri, tlog_path, connect_timeout_s)
        parameter_snapshot_before, parameter_snapshot_after, parameter_anomalies = _prepare_parameters(master, config)
        anomalies.extend(parameter_anomalies)

        if arm_and_takeoff or bool(config.extras.get("ardupilot_arm_takeoff", True)):
            anomalies.extend(_arm_and_takeoff(master, config.takeoff_altitude_m))
            if any(item in {"guided_mode_unavailable", "arm_failed", "takeoff_command_failed"} for item in anomalies):
                run_status = "invalid_runtime"

        desired_mode = study["mode_under_test"]
        if run_status == "completed" and config.resolved_study_layer == "manual_whole_loop":
            if not _set_mode(master, desired_mode):
                anomalies.append(f"mode_under_test_unavailable:{desired_mode}")
                run_status = "invalid_runtime"
            time.sleep(float(config.extras.get("ardupilot_mode_settle_s", 1.5)))

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
            _append_message_rows(master, attitude_rows, position_rows, heartbeat_rows, status_rows)
            time.sleep(config.period_s)
    except Exception as exc:
        anomalies.append(f"runtime_error:{type(exc).__name__}")
        run_status = "invalid_runtime"
    finally:
        if master is not None:
            try:
                _land_vehicle(master)
                time.sleep(float(config.extras.get("ardupilot_land_settle_s", 2.0)))
                _append_message_rows(master, attitude_rows, position_rows, heartbeat_rows, status_rows)
                anomalies.extend(_restore_parameters(master, parameter_snapshot_before))
                master.close()
            except Exception:
                pass
        _stop_process(process)

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
        [
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
        ],
    )

    manifest = {
        "run_id": run_id,
        "backend": BACKEND_NAME,
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
        _notes_text(run_id, config, study, run_status, anomalies, metrics, copied_bin_path or bin_log_path, tlog_path),
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
