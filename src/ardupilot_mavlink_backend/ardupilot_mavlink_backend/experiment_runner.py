from __future__ import annotations

import argparse
import csv
import math
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from linearity_core.config import RunConfig, clamp, euler_to_quaternion, load_run_config
from linearity_core.excitation import ExcitationGenerator
from linearity_core.io import capture_host_snapshot, ensure_raw_run_directories, write_rows_csv, write_yaml
from linearity_core.mav_params import fetch_parameter, set_parameter, set_parameters, snapshot_parameters
from linearity_core.paths import ARDUPILOT_ROOT, ARDUPILOT_RAW_ROOT
from linearity_core.research_contract import apply_manifest_research_contract, build_acceptance_block
from pymavlink import mavutil

from .bin_log_extract import extract_bin_log
from .session import (
    cleanup_residual_processes,
    connect,
    finalize_visualization_report,
    start_visualizer,
    start_sitl as start_sitl_process,
    stop_process,
    wait_for_mode,
)


BACKEND_NAME = "ardupilot"
DEFAULT_MASTER = "tcp:127.0.0.1:5760"
EARTH_RADIUS_M = 6378137.0
ATTITUDE_FIELDNAMES = ["received_time_ns", "roll", "pitch", "yaw", "rollspeed", "pitchspeed", "yawspeed"]
LOCAL_POSITION_FIELDNAMES = ["received_time_ns", "x", "y", "z", "vx", "vy", "vz"]
HEARTBEAT_FIELDNAMES = ["received_time_ns", "base_mode", "custom_mode", "system_status"]
STATUS_FIELDNAMES = ["received_time_ns", "voltage_battery", "current_battery", "battery_remaining", "drop_rate_comm"]
INPUT_TRACE_FIELDNAMES = [
    "publish_time_ns",
    "elapsed_s",
    "profile_value",
    "roll_body",
    "pitch_body",
    "yaw_body",
    "thrust_z",
    "command_roll",
    "command_pitch",
    "command_yaw",
    "command_throttle",
    "phase",
]
ACTIVE_PHASE_COMPATIBILITY = {"experiment"}
BLOCKING_TOPICS = ("attitude", "local_position", "heartbeat", "sys_status")
QUALITY_TOPICS = BLOCKING_TOPICS + ("bin_att", "bin_rate", "bin_motb", "bin_rcou")
ALIGNMENT_FLAG_TOPICS = ("attitude", "local_position", "sys_status", "bin_att", "bin_rate", "bin_motb", "bin_rcou")
BIN_ALIGNMENT_TOPICS = ("bin_att", "bin_rate", "bin_motb", "bin_rcou")
CANONICAL_TELEMETRY_FILES = {
    "attitude.csv": ("attitude", ATTITUDE_FIELDNAMES),
    "local_position.csv": ("local_position", LOCAL_POSITION_FIELDNAMES),
    "heartbeat.csv": ("heartbeat", HEARTBEAT_FIELDNAMES),
    "sys_status.csv": ("sys_status", STATUS_FIELDNAMES),
}


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


def _safe_timestamp_ns(value: Any, default: int = 0) -> int:
    if value in ("", None):
        return default
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _safe_time_ns_for_row(row: dict[str, Any], key: str = "received_time_ns") -> int:
    return _safe_timestamp_ns(row.get(key), 0)


def _has_nonempty_rows(rows: list[dict[str, Any]]) -> bool:
    return bool(rows)


def _wrap_radians_from_degrees(angle_deg: float) -> float:
    angle_rad = math.radians(angle_deg)
    return math.atan2(math.sin(angle_rad), math.cos(angle_rad))


def _wrapped_angle_delta(current: float, previous: float) -> float:
    return math.atan2(math.sin(current - previous), math.cos(current - previous))


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


def _input_anchor_time_ns(input_rows: list[dict[str, Any]]) -> int | None:
    positive = [_safe_timestamp_ns(row.get("publish_time_ns"), 0) for row in input_rows]
    positive = [value for value in positive if value > 0]
    if not positive:
        return None
    return min(positive)


def _bin_global_start_ns_from_telemetry_dir(
    telemetry_dir: Path,
    filenames: tuple[str, ...] = ("bin_att.csv", "bin_rate.csv", "bin_motb.csv", "bin_rcou.csv"),
) -> int | None:
    candidates: list[int] = []
    for filename in filenames:
        rows = _sorted_csv_rows(telemetry_dir / filename, "received_time_ns")
        if not rows:
            continue
        positive = [_safe_timestamp_ns(row.get("received_time_ns"), 0) for row in rows]
        positive = [value for value in positive if value > 0]
        if positive:
            candidates.append(min(positive))
    if not candidates:
        return None
    return min(candidates)


def _aligned_bin_rows(input_rows: list[dict[str, Any]], bin_rows: list[dict[str, Any]], *, telemetry_dir: Path) -> list[dict[str, Any]]:
    anchor_time_ns = _input_anchor_time_ns(input_rows)
    bin_start_ns = _bin_global_start_ns_from_telemetry_dir(telemetry_dir)
    if anchor_time_ns is None or bin_start_ns is None:
        return []
    aligned_rows: list[dict[str, Any]] = []
    for row in bin_rows:
        received_time_ns = _safe_timestamp_ns(row.get("received_time_ns"), 0)
        aligned_rows.append(
            {
                **row,
                "aligned_time_ns": anchor_time_ns + max(0, received_time_ns - bin_start_ns),
            }
        )
    return aligned_rows


def _set_mode(master: mavutil.mavfile, mode_name: str) -> bool:
    normalized_mode = str(mode_name).strip().upper()
    mapping = master.mode_mapping() or {}
    normalized_mapping = {str(name).strip().upper(): value for name, value in mapping.items()}
    if normalized_mode in normalized_mapping:
        master.mav.set_mode_send(
            master.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            normalized_mapping[normalized_mode],
        )
        return True
    try:
        master.set_mode_apm(mode_name)
        return True
    except Exception:
        return False


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


def _wait_for_vehicle_ready(master: mavutil.mavfile, timeout_s: float = 20.0) -> list[str]:
    deadline = time.monotonic() + timeout_s
    autopilot_ready = False

    while time.monotonic() < deadline and not autopilot_ready:
        message = master.recv_match(blocking=True, timeout=0.5)
        if message is None:
            continue
        message_type = message.get_type()
        if message_type != "STATUSTEXT":
            continue
        text = str(getattr(message, "text", "")).strip()
        if text == "ArduPilot Ready":
            autopilot_ready = True

    anomalies: list[str] = []
    if not autopilot_ready:
        anomalies.append("autopilot_ready_text_missing")
    return anomalies


def _arm_vehicle(master: mavutil.mavfile, mode_name: str, timeout_s: float = 15.0) -> list[str]:
    def _set_and_confirm_mode(target_mode: str, confirm_timeout_s: float) -> list[str]:
        mode_set_attempted = False
        deadline = time.monotonic() + max(2.0, confirm_timeout_s)
        while time.monotonic() < deadline:
            mode_set_attempted = _set_mode(master, target_mode) or mode_set_attempted
            if wait_for_mode(master, target_mode, timeout_s=1.0):
                return []
            time.sleep(0.5)
        if not mode_set_attempted:
            return [f"mode_unavailable:{target_mode}"]
        return [f"mode_not_confirmed:{target_mode}"]

    normalized_mode = str(mode_name).strip().upper()
    bootstrap_mode = "STABILIZE" if normalized_mode == "GUIDED_NOGPS" else normalized_mode
    bootstrap_anomalies = _set_and_confirm_mode(bootstrap_mode, timeout_s * 0.4)
    if bootstrap_anomalies and not (
        bootstrap_mode == "STABILIZE" and all(item == "mode_not_confirmed:STABILIZE" for item in bootstrap_anomalies)
    ):
        return bootstrap_anomalies

    anomalies: list[str] = []

    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        try:
            master.arducopter_arm()
        except Exception:
            pass
        remaining_s = max(0.5, min(2.0, deadline - time.monotonic()))
        if _wait_for_armed(master, timeout_s=remaining_s):
            if normalized_mode != bootstrap_mode:
                anomalies.extend(_set_and_confirm_mode(normalized_mode, timeout_s * 0.4))
            elif bootstrap_anomalies:
                anomalies.extend(bootstrap_anomalies)
            return anomalies
        time.sleep(0.5)
    anomalies.extend(bootstrap_anomalies)
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


def _send_rate_target(master: mavutil.mavfile, roll_rate: float, pitch_rate: float, yaw_rate: float, thrust_z: float) -> None:
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


def _canonical_csv_rows(path: Path) -> list[dict[str, Any]]:
    return _sorted_csv_rows(path, "received_time_ns")


def _bin_global_start_ns(rows_by_name: dict[str, list[dict[str, Any]]]) -> int | None:
    candidates = [
        _safe_time_ns_for_row(rows[0])
        for rows in rows_by_name.values()
        if rows
    ]
    return min(candidates) if candidates else None


def _telemetry_anchor_time_ns(
    input_profile_rows: list[dict[str, Any]],
    runtime_report: dict[str, Any],
    capture_start_time_ns: int,
) -> int:
    if input_profile_rows:
        return _safe_timestamp_ns(input_profile_rows[0].get("publish_time_ns"), capture_start_time_ns)
    experiment_start_time_ns = _safe_timestamp_ns(runtime_report.get("experiment_start_time_ns"), 0)
    if experiment_start_time_ns > 0:
        return experiment_start_time_ns
    return capture_start_time_ns


def _aligned_received_time_ns(
    row: dict[str, Any],
    *,
    bin_start_ns: int,
    anchor_time_ns: int,
) -> int:
    return anchor_time_ns + max(0, _safe_time_ns_for_row(row) - bin_start_ns)


def _nearest_by_time(rows: list[dict[str, Any]], target_ns: int) -> dict[str, Any] | None:
    if not rows:
        return None
    return min(rows, key=lambda item: abs(_safe_time_ns_for_row(item) - target_ns))


def _derive_axis_rates(rows: list[dict[str, Any]]) -> None:
    if len(rows) < 2:
        for row in rows:
            row["rollspeed"] = 0.0
            row["pitchspeed"] = 0.0
            row["yawspeed"] = 0.0
        return

    for index, row in enumerate(rows):
        if index == 0:
            previous = row
            current = rows[index + 1]
        elif index == len(rows) - 1:
            previous = rows[index - 1]
            current = row
        else:
            previous = rows[index - 1]
            current = rows[index + 1]
        dt_ns = max(1, _safe_time_ns_for_row(current) - _safe_time_ns_for_row(previous))
        dt_s = dt_ns / 1_000_000_000.0
        row["rollspeed"] = _wrapped_angle_delta(float(current["roll"]), float(previous["roll"])) / dt_s
        row["pitchspeed"] = _wrapped_angle_delta(float(current["pitch"]), float(previous["pitch"])) / dt_s
        row["yawspeed"] = _wrapped_angle_delta(float(current["yaw"]), float(previous["yaw"])) / dt_s


def _derive_velocity_rows(rows: list[dict[str, Any]]) -> None:
    if len(rows) < 2:
        for row in rows:
            row["vx"] = 0.0
            row["vy"] = 0.0
            row["vz"] = 0.0
        return

    for index, row in enumerate(rows):
        if index == 0:
            previous = row
            current = rows[index + 1]
        elif index == len(rows) - 1:
            previous = rows[index - 1]
            current = row
        else:
            previous = rows[index - 1]
            current = rows[index + 1]
        dt_ns = max(1, _safe_time_ns_for_row(current) - _safe_time_ns_for_row(previous))
        dt_s = dt_ns / 1_000_000_000.0
        row["vx"] = (float(current["x"]) - float(previous["x"])) / dt_s
        row["vy"] = (float(current["y"]) - float(previous["y"])) / dt_s
        row["vz"] = (float(current["z"]) - float(previous["z"])) / dt_s


def _synthesize_attitude_rows(
    *,
    bin_att_rows: list[dict[str, Any]],
    bin_rate_rows: list[dict[str, Any]],
    bin_ahr2_rows: list[dict[str, Any]],
    bin_start_ns: int,
    anchor_time_ns: int,
) -> list[dict[str, Any]]:
    source_rows = bin_att_rows or bin_ahr2_rows
    if not source_rows:
        return []

    rows: list[dict[str, Any]] = []
    for source_row in source_rows:
        received_time_ns = _aligned_received_time_ns(source_row, bin_start_ns=bin_start_ns, anchor_time_ns=anchor_time_ns)
        if bin_att_rows:
            roll = _wrap_radians_from_degrees(_safe_float(source_row.get("roll")))
            pitch = _wrap_radians_from_degrees(_safe_float(source_row.get("pitch")))
            yaw = _wrap_radians_from_degrees(_safe_float(source_row.get("yaw")))
        else:
            roll = _wrap_radians_from_degrees(_safe_float(source_row.get("roll_deg")))
            pitch = _wrap_radians_from_degrees(_safe_float(source_row.get("pitch_deg")))
            yaw = _wrap_radians_from_degrees(_safe_float(source_row.get("yaw_deg")))
        rate_row = _nearest_by_time(bin_rate_rows, _safe_time_ns_for_row(source_row))
        rows.append(
            {
                "received_time_ns": received_time_ns,
                "roll": roll,
                "pitch": pitch,
                "yaw": yaw,
                "rollspeed": _safe_float(rate_row.get("roll_rate") if rate_row else None),
                "pitchspeed": _safe_float(rate_row.get("pitch_rate") if rate_row else None),
                "yawspeed": _safe_float(rate_row.get("yaw_rate") if rate_row else None),
            }
        )
    if not bin_rate_rows:
        _derive_axis_rates(rows)
    return rows


def _synthesize_local_position_rows(
    *,
    bin_pos_rows: list[dict[str, Any]],
    bin_orgn_rows: list[dict[str, Any]],
    bin_start_ns: int,
    anchor_time_ns: int,
) -> list[dict[str, Any]]:
    if not bin_pos_rows:
        return []

    origin_row = bin_orgn_rows[0] if bin_orgn_rows else bin_pos_rows[0]
    origin_lat_deg = _safe_float(origin_row.get("lat_deg"))
    origin_lon_deg = _safe_float(origin_row.get("lon_deg"))
    origin_alt_m = _safe_float(origin_row.get("alt_m"))
    if any(math.isnan(value) for value in (origin_lat_deg, origin_lon_deg)):
        return []
    origin_lat_rad = math.radians(origin_lat_deg)
    origin_lon_rad = math.radians(origin_lon_deg)

    rows: list[dict[str, Any]] = []
    for source_row in bin_pos_rows:
        lat_deg = _safe_float(source_row.get("lat_deg"))
        lon_deg = _safe_float(source_row.get("lon_deg"))
        alt_m = _safe_float(source_row.get("alt_m"))
        rel_origin_alt_m = _safe_float(source_row.get("rel_origin_alt_m"))
        if any(math.isnan(value) for value in (lat_deg, lon_deg)):
            continue
        lat_rad = math.radians(lat_deg)
        lon_rad = math.radians(lon_deg)
        z = -rel_origin_alt_m if not math.isnan(rel_origin_alt_m) else -(alt_m - origin_alt_m)
        rows.append(
            {
                "received_time_ns": _aligned_received_time_ns(source_row, bin_start_ns=bin_start_ns, anchor_time_ns=anchor_time_ns),
                "x": EARTH_RADIUS_M * (lat_rad - origin_lat_rad),
                "y": EARTH_RADIUS_M * math.cos(origin_lat_rad) * (lon_rad - origin_lon_rad),
                "z": z,
                "vx": math.nan,
                "vy": math.nan,
                "vz": math.nan,
            }
        )
    _derive_velocity_rows(rows)
    return rows


def _synthesize_heartbeat_rows(
    *,
    bin_mode_rows: list[dict[str, Any]],
    bin_start_ns: int,
    anchor_time_ns: int,
) -> list[dict[str, Any]]:
    if not bin_mode_rows:
        return []
    rows: list[dict[str, Any]] = []
    for source_row in bin_mode_rows:
        custom_mode = _safe_int(source_row.get("mode_num"), _safe_int(source_row.get("mode"), 0))
        rows.append(
            {
                "received_time_ns": _aligned_received_time_ns(source_row, bin_start_ns=bin_start_ns, anchor_time_ns=anchor_time_ns),
                "base_mode": 0,
                "custom_mode": custom_mode,
                "system_status": 0,
            }
        )
    return rows


def _synthesize_sys_status_rows(
    *,
    bin_bat_rows: list[dict[str, Any]],
    bin_start_ns: int,
    anchor_time_ns: int,
) -> list[dict[str, Any]]:
    if not bin_bat_rows:
        return []
    rows: list[dict[str, Any]] = []
    for source_row in bin_bat_rows:
        rows.append(
            {
                "received_time_ns": _aligned_received_time_ns(source_row, bin_start_ns=bin_start_ns, anchor_time_ns=anchor_time_ns),
                "voltage_battery": int(round(_safe_float(source_row.get("voltage_v"), 0.0) * 1000.0)),
                "current_battery": int(round(_safe_float(source_row.get("current_a"), 0.0) * 100.0)),
                "battery_remaining": _safe_int(source_row.get("battery_remaining_pct"), 0),
                "drop_rate_comm": 0,
            }
        )
    return rows


def _apply_bin_canonical_fallback(
    paths: dict[str, Path],
    runtime_report: dict[str, Any],
    input_profile_rows: list[dict[str, Any]],
    capture_start_time_ns: int,
) -> dict[str, str]:
    telemetry_dir = paths["telemetry_dir"]
    canonical_rows = {
        name: _canonical_csv_rows(telemetry_dir / name)
        for name in CANONICAL_TELEMETRY_FILES
    }
    sources = {
        name: ("live_mavlink" if _has_nonempty_rows(rows) else "missing")
        for name, rows in canonical_rows.items()
    }
    if all(source == "live_mavlink" for source in sources.values()):
        return sources

    bin_rows = {
        "bin_att": _sorted_csv_rows(telemetry_dir / "bin_att.csv", "received_time_ns"),
        "bin_rate": _sorted_csv_rows(telemetry_dir / "bin_rate.csv", "received_time_ns"),
        "bin_pos": _sorted_csv_rows(telemetry_dir / "bin_pos.csv", "received_time_ns"),
        "bin_ahr2": _sorted_csv_rows(telemetry_dir / "bin_ahr2.csv", "received_time_ns"),
        "bin_bat": _sorted_csv_rows(telemetry_dir / "bin_bat.csv", "received_time_ns"),
        "bin_mode": _sorted_csv_rows(telemetry_dir / "bin_mode.csv", "received_time_ns"),
        "bin_orgn": _sorted_csv_rows(telemetry_dir / "bin_orgn.csv", "received_time_ns"),
    }
    bin_start_ns = _bin_global_start_ns(bin_rows)
    if bin_start_ns is None:
        return sources
    anchor_time_ns = _telemetry_anchor_time_ns(input_profile_rows, runtime_report, capture_start_time_ns)

    fallback_rows = {
        "attitude.csv": _synthesize_attitude_rows(
            bin_att_rows=bin_rows["bin_att"],
            bin_rate_rows=bin_rows["bin_rate"],
            bin_ahr2_rows=bin_rows["bin_ahr2"],
            bin_start_ns=bin_start_ns,
            anchor_time_ns=anchor_time_ns,
        ),
        "local_position.csv": _synthesize_local_position_rows(
            bin_pos_rows=bin_rows["bin_pos"],
            bin_orgn_rows=bin_rows["bin_orgn"],
            bin_start_ns=bin_start_ns,
            anchor_time_ns=anchor_time_ns,
        ),
        "heartbeat.csv": _synthesize_heartbeat_rows(
            bin_mode_rows=bin_rows["bin_mode"],
            bin_start_ns=bin_start_ns,
            anchor_time_ns=anchor_time_ns,
        ),
        "sys_status.csv": _synthesize_sys_status_rows(
            bin_bat_rows=bin_rows["bin_bat"],
            bin_start_ns=bin_start_ns,
            anchor_time_ns=anchor_time_ns,
        ),
    }

    for filename, (_, fieldnames) in CANONICAL_TELEMETRY_FILES.items():
        if sources[filename] == "live_mavlink":
            continue
        rows = fallback_rows.get(filename, [])
        if rows:
            _write_telemetry_csv(telemetry_dir / filename, rows, fieldnames)
            sources[filename] = "bin_fallback"
        else:
            sources[filename] = "missing"
    return sources


def _int_value(value: Any, default: int = 0) -> int:
    if value in ("", None):
        return default
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _sorted_csv_rows(path: Path, time_key: str) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows.sort(key=lambda row: _int_value(row.get(time_key), 0))
    return rows


def _timestamp_monotonic(rows: list[dict[str, Any]], time_key: str) -> bool:
    previous = None
    for row in rows:
        current = _int_value(row.get(time_key), 0)
        if previous is not None and current < previous:
            return False
        previous = current
    return True


def _nearest_gap_metrics(reference_rows: list[dict[str, Any]], target_rows: list[dict[str, Any]], reference_key: str, target_key: str) -> dict[str, float]:
    if not reference_rows or not target_rows:
        return {"count": 0.0, "median_ns": math.nan, "p95_ns": math.nan, "max_ns": math.nan}
    target_times = [_int_value(row.get(target_key), 0) for row in target_rows]
    gaps: list[int] = []
    for row in reference_rows:
        target_ns = _int_value(row.get(reference_key), 0)
        nearest = min(target_times, key=lambda value: abs(value - target_ns))
        gaps.append(abs(nearest - target_ns))
    if not gaps:
        return {"count": 0.0, "median_ns": math.nan, "p95_ns": math.nan, "max_ns": math.nan}
    return {
        "count": float(len(gaps)),
        "median_ns": float(sorted(gaps)[len(gaps) // 2]),
        "p95_ns": float(sorted(gaps)[min(len(gaps) - 1, int(0.95 * (len(gaps) - 1)))]),
        "max_ns": float(max(gaps)),
    }


def _phase_is_active(phase: Any) -> bool:
    normalized = str(phase or "").strip().lower()
    return (
        normalized.endswith("_active")
        or "_active_" in normalized
        or normalized in ACTIVE_PHASE_COMPATIBILITY
    )


def _command_row_has_nonzero_command(row: dict[str, Any], *, epsilon: float = 1e-9) -> bool:
    return any(abs(float(row.get(name, 0.0) or 0.0)) > epsilon for name in ("command_roll", "command_pitch", "command_yaw", "command_throttle"))


def _expected_active_sample_count(config: RunConfig) -> int:
    duration_s = max(0.0, float(config.duration_s))
    sampling_rate_hz = max(0.0, float(config.sampling_rate_hz))
    return int(math.ceil(duration_s * sampling_rate_hz))


def _minimum_active_nonzero_samples(config: RunConfig) -> int:
    duration_s = max(0.0, float(config.duration_s))
    sampling_rate_hz = max(0.0, float(config.sampling_rate_hz))
    return max(10, int(math.ceil(0.25 * duration_s * sampling_rate_hz)))


def _failsafe_after_experiment_start(heartbeat_rows: list[dict[str, Any]], runtime_report: dict[str, Any]) -> bool:
    experiment_start_time_ns = _int_value(runtime_report.get("experiment_start_time_ns"), 0)
    if experiment_start_time_ns <= 0:
        return False
    critical_states = {
        mavutil.mavlink.MAV_STATE_CRITICAL,
        mavutil.mavlink.MAV_STATE_EMERGENCY,
        mavutil.mavlink.MAV_STATE_FLIGHT_TERMINATION,
    }
    for row in heartbeat_rows:
        if _int_value(row.get("received_time_ns"), 0) < experiment_start_time_ns:
            continue
        if _int_value(row.get("system_status"), 0) in critical_states:
            return True
    return False


def _completion_reason_indicates_truncation(completion_reason: str) -> bool:
    normalized = str(completion_reason or "").strip().lower()
    return normalized not in {"profile_completed", "completed"}


def _prediction_constructibility_metrics(command_trace: list[dict[str, Any]], topic_counts: dict[str, int], config: RunConfig) -> dict[str, float]:
    total_samples = float(len(command_trace))
    future_samples = max(0.0, total_samples - float(config.prediction_horizon))
    actuator_samples = float(topic_counts.get("bin_rcou", 0))
    return {
        "total_input_samples": total_samples,
        "prediction_horizon": float(config.prediction_horizon),
        "future_state_ratio_estimate": (future_samples / total_samples) if total_samples > 0 else 0.0,
        "delta_state_ratio_estimate": (future_samples / total_samples) if total_samples > 0 else 0.0,
        "window_summary_ratio_estimate": (future_samples / total_samples) if total_samples > 0 else 0.0,
        "actuator_response_ratio_estimate": min(1.0, actuator_samples / total_samples) if total_samples > 0 else 0.0,
    }


def _ardupilot_acceptance(
    paths: dict[str, Path],
    command_trace: list[dict[str, Any]],
    config: RunConfig,
    runtime_report: dict[str, Any],
    status: str,
    missing_topics: list[str],
) -> dict[str, Any]:
    input_rows = command_trace or _sorted_csv_rows(paths["input_trace_path"], "publish_time_ns")
    heartbeat_rows = _sorted_csv_rows(paths["telemetry_dir"] / "heartbeat.csv", "received_time_ns")
    active_rows = [row for row in input_rows if _phase_is_active(row.get("phase"))]
    active_nonzero_command_samples = int(sum(1 for row in active_rows if _command_row_has_nonzero_command(row)))
    experiment_started = _int_value(runtime_report.get("experiment_start_time_ns"), 0) > 0
    expected_active_samples = _expected_active_sample_count(config)
    failsafe_during_experiment = _failsafe_after_experiment_start(heartbeat_rows, runtime_report)
    completion_reason = str(runtime_report.get("completion_reason", "") or "").strip()
    rejection_reasons: list[str] = []
    if status != "completed":
        rejection_reasons.append(f"capture_status_{status}")
    if missing_topics:
        rejection_reasons.append("missing_topics_blocking")
    if not experiment_started:
        rejection_reasons.append("experiment_not_started")
    if not active_rows:
        rejection_reasons.append("active_phase_missing")
    if active_nonzero_command_samples < _minimum_active_nonzero_samples(config):
        rejection_reasons.append("insufficient_active_nonzero_command_samples")
    if failsafe_during_experiment:
        rejection_reasons.append("failsafe_during_experiment")
    if (
        experiment_started
        and len(active_rows) < expected_active_samples
        and (_completion_reason_indicates_truncation(completion_reason) or failsafe_during_experiment)
    ):
        rejection_reasons.append("experiment_truncated_before_expected_active_samples")
    accepted = not rejection_reasons
    return build_acceptance_block(
        experiment_started=experiment_started,
        active_phase_present=bool(active_rows),
        expected_active_samples=expected_active_samples,
        active_sample_count=len(active_rows),
        active_nonzero_command_samples=active_nonzero_command_samples,
        failsafe_during_experiment=failsafe_during_experiment,
        missing_topics_blocking=missing_topics,
        accepted=accepted,
        rejection_reasons=rejection_reasons,
    )


def _ardupilot_data_quality(
    paths: dict[str, Path],
    command_trace: list[dict[str, Any]],
    config: RunConfig,
    runtime_report: dict[str, Any],
    status: str,
) -> dict[str, Any]:
    input_rows = _sorted_csv_rows(paths["input_trace_path"], "publish_time_ns")
    telemetry_rows = {
        "attitude": _sorted_csv_rows(paths["telemetry_dir"] / "attitude.csv", "received_time_ns"),
        "local_position": _sorted_csv_rows(paths["telemetry_dir"] / "local_position.csv", "received_time_ns"),
        "heartbeat": _sorted_csv_rows(paths["telemetry_dir"] / "heartbeat.csv", "received_time_ns"),
        "sys_status": _sorted_csv_rows(paths["telemetry_dir"] / "sys_status.csv", "received_time_ns"),
        "bin_att": _sorted_csv_rows(paths["telemetry_dir"] / "bin_att.csv", "received_time_ns"),
        "bin_rate": _sorted_csv_rows(paths["telemetry_dir"] / "bin_rate.csv", "received_time_ns"),
        "bin_motb": _sorted_csv_rows(paths["telemetry_dir"] / "bin_motb.csv", "received_time_ns"),
        "bin_rcou": _sorted_csv_rows(paths["telemetry_dir"] / "bin_rcou.csv", "received_time_ns"),
    }
    topic_counts = {topic: len(rows) for topic, rows in telemetry_rows.items()}
    missing_topics = sorted(topic for topic in BLOCKING_TOPICS if topic_counts.get(topic, 0) <= 0)
    timestamp_monotonicity = {
        "input_trace": _timestamp_monotonic(input_rows, "publish_time_ns"),
        **{name: _timestamp_monotonic(rows, "received_time_ns") for name, rows in telemetry_rows.items()},
    }
    input_alignment_ns: dict[str, dict[str, float]] = {}
    for name, rows in telemetry_rows.items():
        if name in BIN_ALIGNMENT_TOPICS:
            aligned_rows = _aligned_bin_rows(input_rows, rows, telemetry_dir=paths["telemetry_dir"])
            input_alignment_ns[name] = _nearest_gap_metrics(input_rows, aligned_rows, "publish_time_ns", "aligned_time_ns")
        else:
            input_alignment_ns[name] = _nearest_gap_metrics(input_rows, rows, "publish_time_ns", "received_time_ns")
    max_alignment_error_ms = float(config.reporting.get("max_alignment_error_ms", 150.0))
    p95_alignment_failures = sorted(
        name
        for name, metrics in input_alignment_ns.items()
        if name in ALIGNMENT_FLAG_TOPICS
        and not math.isnan(metrics["p95_ns"])
        and metrics["p95_ns"] > max_alignment_error_ms * 1_000_000.0
    )
    acceptance = _ardupilot_acceptance(paths, command_trace, config, runtime_report, status, missing_topics)
    return {
        "topic_presence": {
            "required_topic_counts": topic_counts,
            "missing_topics": missing_topics,
            "ros_message_counts": {topic: count for topic, count in topic_counts.items()},
        },
        "timestamp_monotonicity": timestamp_monotonicity,
        "input_alignment_ns": input_alignment_ns,
        "prediction_constructibility": _prediction_constructibility_metrics(command_trace, topic_counts, config),
        "thresholds": {
            "max_alignment_error_ms": max_alignment_error_ms,
        },
        "quality_flags": {
            "non_monotonic_streams": sorted(name for name, ok in timestamp_monotonicity.items() if not ok),
            "alignment_p95_exceeded_streams": p95_alignment_failures,
        },
        "acceptance": acceptance,
    }


def _prepare_parameters(master: mavutil.mavfile, config: RunConfig) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    parameter_names = list(dict.fromkeys(config.controlled_parameters_for_backend("ardupilot")))
    parameter_names.extend(name for name in config.parameter_overrides_for_backend("ardupilot") if name not in parameter_names)
    if "ARMING_CHECK" not in parameter_names:
        parameter_names.append("ARMING_CHECK")
    before = snapshot_parameters(master, parameter_names, timeout_s=2.0)
    anomalies: list[str] = []
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
    for _ in range(3):
        if set_parameter(master, "ARMING_CHECK", 0.0, timeout_s=5.0):
            parameter_snapshot_after["ARMING_CHECK"] = 0.0
            return []
        time.sleep(1.0)
    return ["arming_check_disable_failed"]


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


def _notes_text(run_id: str, config: RunConfig, status: str, anomalies: list[str], bin_log_path: str | None, tlog_path: Path) -> str:
    return "\n".join(
        [
            f"# {run_id}",
            "- ardupilot raw linearity capture",
            f"- status: {status}",
            f"- backend: {BACKEND_NAME}",
            f"- input_type: {config.input_type}",
            f"- flight_mode: {config.mode_under_test_for_backend('ardupilot')}",
            f"- x_schema: {config.x_schema}",
            f"- y_schema: {config.y_schema}",
            f"- ardupilot_bin_log_path: {bin_log_path or 'missing'}",
            f"- ardupilot_tlog_path: {tlog_path}",
            f"- anomalies: {', '.join(anomalies) if anomalies else 'none'}",
        ]
    )


def run_capture(
    config: RunConfig,
    vehicle: str = "ArduCopter",
    frame: str = "quad",
    master_uri: str = DEFAULT_MASTER,
    start_sitl: bool = True,
    connect_timeout_s: float = 60.0,
    sitl_log_path: Path | None = None,
    enable_visualization: bool | None = None,
) -> tuple[int, Path]:
    start_time = datetime.now(timezone.utc).astimezone()
    capture_start_time_ns = time.time_ns()
    run_id = config.build_run_id(start_time, repeat_index=config.repeat_index)
    paths = ensure_raw_run_directories("ardupilot", run_id, root=ARDUPILOT_RAW_ROOT)
    resolved_sitl_log_path = sitl_log_path or (paths["logs_dir"] / "ardupilot_sitl.log")
    tlog_path = paths["telemetry_dir"] / "ardupilot.tlog"

    bin_before = _snapshot_logs(ARDUPILOT_ROOT, (".bin",))
    host_start = capture_host_snapshot()
    anomalies: list[str] = []
    input_profile_rows: list[dict[str, Any]] = []
    attitude_rows: list[dict[str, Any]] = []
    position_rows: list[dict[str, Any]] = []
    heartbeat_rows: list[dict[str, Any]] = []
    status_rows: list[dict[str, Any]] = []
    profile = ExcitationGenerator(config)
    position_origin: dict[str, float] | None = None

    process = None
    master: mavutil.mavfile | None = None
    status = "completed"
    failure_reason = ""
    parameter_snapshot_before: dict[str, Any] = {}
    parameter_snapshot_after: dict[str, Any] = {}
    extracted_bin_summary: dict[str, Any] = {}
    runtime_report: dict[str, Any] = {
        "experiment_start_time_ns": None,
        "completion_time_ns": None,
        "completion_reason": "not_started",
        "anomalies": [],
        "visualization": {
            "requested": False,
            "headless": True,
            "mavproxy_started": False,
            "map_requested": False,
            "map_loaded": False,
            "failure_reason": "",
        },
    }

    try:
        if start_sitl:
            cleanup_residual_processes()
            process = start_sitl_process(
                run_id,
                vehicle,
                frame,
                resolved_sitl_log_path,
                enable_visualization=enable_visualization,
            )

        master = connect(master_uri, tlog_path, connect_timeout_s)
        if process is not None:
            process = start_visualizer(process, master_uri)
        readiness_anomalies = _wait_for_vehicle_ready(master, timeout_s=float(config.extras.get("ardupilot_ready_timeout_s", 20.0)))
        anomalies.extend(readiness_anomalies)

        parameter_snapshot_before, parameter_snapshot_after, parameter_anomalies = _prepare_parameters(master, config)
        anomalies.extend(parameter_anomalies)
        anomalies.extend(_prepare_runtime_arming(master, parameter_snapshot_after))

        if status == "completed":
            desired_mode = config.mode_under_test_for_backend("ardupilot")
            arming_anomalies = _arm_vehicle(master, desired_mode)
            anomalies.extend(arming_anomalies)
            if arming_anomalies:
                status = "failed"
                if any(item.startswith("mode_not_confirmed:") for item in arming_anomalies):
                    failure_reason = "mode_not_confirmed"
                elif any(item.startswith("mode_unavailable:") for item in arming_anomalies):
                    failure_reason = "mode_unavailable"
                else:
                    failure_reason = "arm_failed"
                runtime_report["completion_reason"] = failure_reason

        started = time.monotonic()
        end_deadline = started + profile.total_duration_s + float(config.extras.get("ardupilot_tail_s", 2.0))
        manual_bias = float(config.extras.get("ardupilot_manual_throttle_bias", 0.65))
        manual_scale = float(config.extras.get("ardupilot_manual_throttle_scale", 0.30))
        if status == "completed":
            runtime_report["experiment_start_time_ns"] = time.time_ns()
            runtime_report["completion_reason"] = "running"

        while status == "completed" and time.monotonic() < end_deadline:
            elapsed_s = time.monotonic() - started
            if config.input_type == "manual":
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
                        "command_roll": roll,
                        "command_pitch": pitch,
                        "command_yaw": yaw,
                        "command_throttle": throttle_norm,
                        "phase": phase,
                    }
                )
            elif config.input_type == "attitude":
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
                        "command_roll": roll_body,
                        "command_pitch": pitch_body,
                        "command_yaw": yaw_body,
                        "command_throttle": thrust_z,
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
                        "command_roll": roll_rate,
                        "command_pitch": pitch_rate,
                        "command_yaw": yaw_rate,
                        "command_throttle": thrust_z,
                        "phase": phase,
                    }
                )
            position_origin = _append_message_rows(master, attitude_rows, position_rows, heartbeat_rows, status_rows, position_origin)
            time.sleep(config.period_s)
        if status == "completed":
            runtime_report["completion_reason"] = "profile_completed"
            runtime_report["completion_time_ns"] = time.time_ns()
    except Exception as exc:
        anomalies.append(f"runtime_error:{type(exc).__name__}")
        status = "failed"
        failure_reason = failure_reason or f"runtime_error:{type(exc).__name__}"
        runtime_report["completion_reason"] = failure_reason
        runtime_report["completion_time_ns"] = time.time_ns()
    finally:
        if master is not None:
            try:
                _land_vehicle(master)
                time.sleep(float(config.extras.get("ardupilot_land_settle_s", 2.0)))
                position_origin = _append_message_rows(master, attitude_rows, position_rows, heartbeat_rows, status_rows, position_origin)
                if parameter_snapshot_after != parameter_snapshot_before:
                    anomalies.extend(_restore_parameters(master, parameter_snapshot_before))
                if hasattr(master, "autoreconnect"):
                    master.autoreconnect = False
                master.close()
            except Exception:
                pass
        stop_process(process)
        runtime_report["visualization"] = finalize_visualization_report(process)
        if process is not None and getattr(process, "visualizer_log_path", None):
            source_log_path = Path(process.visualizer_log_path)
            if source_log_path.exists():
                destination_log_path = paths["logs_dir"] / "ardupilot_mavproxy.log"
                if source_log_path.resolve() != destination_log_path.resolve():
                    shutil.copy2(source_log_path, destination_log_path)
        cleanup_residual_processes()
    if runtime_report.get("completion_time_ns") in ("", None):
        runtime_report["completion_time_ns"] = time.time_ns()

    end_time = datetime.now(timezone.utc).astimezone()
    host_end = capture_host_snapshot()
    bin_after = _snapshot_logs(ARDUPILOT_ROOT, (".bin",))
    bin_log_path = _resolve_latest_file(bin_before, bin_after)
    copied_bin_path: str | None = None
    if bin_log_path is not None:
        destination = paths["telemetry_dir"] / "ardupilot.BIN"
        shutil.copy2(bin_log_path, destination)
        copied_bin_path = str(destination)
        try:
            extracted_bin_summary = extract_bin_log(destination, paths["telemetry_dir"])
        except Exception as exc:
            anomalies.append(f"bin_parse_failed:{type(exc).__name__}")
    else:
        anomalies.append("bin_log_missing")

    _write_telemetry_csv(paths["telemetry_dir"] / "attitude.csv", attitude_rows, ATTITUDE_FIELDNAMES)
    _write_telemetry_csv(paths["telemetry_dir"] / "local_position.csv", position_rows, LOCAL_POSITION_FIELDNAMES)
    _write_telemetry_csv(paths["telemetry_dir"] / "heartbeat.csv", heartbeat_rows, HEARTBEAT_FIELDNAMES)
    _write_telemetry_csv(paths["telemetry_dir"] / "sys_status.csv", status_rows, STATUS_FIELDNAMES)
    write_rows_csv(paths["input_trace_path"], input_profile_rows, INPUT_TRACE_FIELDNAMES)
    runtime_report["telemetry_sources"] = _apply_bin_canonical_fallback(
        paths,
        runtime_report,
        input_profile_rows,
        capture_start_time_ns,
    )
    runtime_report["anomalies"] = sorted(dict.fromkeys(anomalies))
    data_quality = _ardupilot_data_quality(paths, input_profile_rows, config, runtime_report, status)
    if data_quality["topic_presence"]["missing_topics"]:
        anomalies.append("quality_missing_topics")
    if data_quality["quality_flags"]["non_monotonic_streams"]:
        anomalies.append("quality_non_monotonic_streams")
    if data_quality["quality_flags"]["alignment_p95_exceeded_streams"]:
        anomalies.append("quality_alignment_p95_exceeded")
    runtime_report["anomalies"] = sorted(dict.fromkeys(anomalies))

    manifest = apply_manifest_research_contract(
        {
        "kind": "linearity_raw_run",
        "run_id": run_id,
        "backend": BACKEND_NAME,
        "status": status,
        "failure_reason": failure_reason,
        "study_name": config.study_name,
        "study_config": config.to_dict(),
        "flight_mode": config.mode_under_test_for_backend("ardupilot"),
        "scenario": config.scenario,
        "config_profile": config.config_profile,
        "seed": config.seed,
        "repeat_index": config.repeat_index,
        "input_type": config.input_type,
        "profile_type": config.profile_type,
        "axis": config.axis,
        "vehicle": vehicle,
        "frame": frame,
        "master_uri": master_uri,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "ardupilot_bin_log_path": copied_bin_path or bin_log_path,
        "ardupilot_tlog_path": str(tlog_path),
        "host_snapshot_start": host_start,
        "host_snapshot_end": host_end,
        "parameter_snapshot_before": parameter_snapshot_before,
        "parameter_snapshot_after": parameter_snapshot_after,
        "bin_extract_summary": extracted_bin_summary,
        "runtime_report": runtime_report,
        "data_quality": data_quality,
        "anomaly_summary": sorted(dict.fromkeys(anomalies)),
        "telemetry_files": sorted(path.name for path in paths["telemetry_dir"].glob("*.csv")),
        },
        research_tier=config.research_tier,
        acceptance=data_quality["acceptance"],
    )
    write_yaml(paths["manifest_path"], manifest)
    paths["notes_path"].write_text(
        _notes_text(run_id, config, status, sorted(dict.fromkeys(anomalies)), copied_bin_path or bin_log_path, tlog_path),
        encoding="utf-8",
    )
    return (0 if status == "completed" else 1), paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="运行 ArduPilot raw linearity capture，并写出新的 raw artifact。")
    parser.add_argument("--config", type=Path, required=True, help="study config YAML 路径。")
    parser.add_argument("--vehicle", default="ArduCopter", help="ArduPilot vehicle，默认 ArduCopter。")
    parser.add_argument("--frame", default="quad", help="SITL frame，默认 quad。")
    parser.add_argument("--master", default=DEFAULT_MASTER, help="MAVLink master URI，默认 tcp:127.0.0.1:5760。")
    parser.add_argument("--skip-sitl", action="store_true", help="连接已有实例，不启动 sim_vehicle.py。")
    parser.add_argument("--enable-visualization", action="store_true", help="显式启用 MAVProxy/map 可视化。默认关闭。")
    args = parser.parse_args(argv)

    config = load_run_config(args.config)
    exit_code, artifact_dir = run_capture(
        config,
        vehicle=args.vehicle,
        frame=args.frame,
        master_uri=args.master,
        start_sitl=not args.skip_sitl,
        enable_visualization=args.enable_visualization,
    )
    print(f"artifact_dir={artifact_dir}")
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
