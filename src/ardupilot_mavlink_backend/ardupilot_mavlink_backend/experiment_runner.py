from __future__ import annotations

import argparse
import csv
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fep_core.config import RunConfig, clamp, euler_to_quaternion, load_run_config
from fep_core.io import capture_host_snapshot, ensure_run_directories, write_single_row_csv, write_yaml
from fep_core.paths import ARDUPILOT_ROOT, ARDUPILOT_RUNS_ROOT
from fep_core.profiles import ProfileGenerator
from pymavlink import mavutil


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
    time.sleep(3.0)
    return anomalies


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


def _send_manual_control(master: mavutil.mavfile, roll: float, pitch: float, yaw: float, throttle: float) -> None:
    master.mav.manual_control_send(
        master.target_system,
        int(clamp(pitch, -1.0, 1.0) * 1000),
        int(clamp(roll, -1.0, 1.0) * 1000),
        int(clamp((throttle + 1.0) * 500.0, 0.0, 1000.0)),
        int(clamp(yaw, -1.0, 1.0) * 1000),
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


def run_experiment(
    config: RunConfig,
    vehicle: str = "ArduCopter",
    frame: str = "quad",
    master_uri: str = DEFAULT_MASTER,
    start_sitl: bool = True,
    connect_timeout_s: float = 60.0,
    arm_and_takeoff: bool = False,
) -> tuple[int, Path]:
    run_id = config.build_run_id()
    paths = ensure_run_directories(ARDUPILOT_RUNS_ROOT, run_id)
    sitl_log_path = paths["base_dir"] / "ardupilot_sitl.log"
    tlog_path = paths["telemetry_dir"] / "ardupilot.tlog"

    bin_before = _snapshot_logs(ARDUPILOT_ROOT, (".bin",))
    host_start = capture_host_snapshot()
    start_time = datetime.now(timezone.utc).astimezone()

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

    try:
        if start_sitl:
            process = _start_sitl(run_id, vehicle, frame, sitl_log_path)
            time.sleep(5.0)
        master = _connect(master_uri, tlog_path, connect_timeout_s)
        if arm_and_takeoff or bool(config.extras.get("ardupilot_arm_takeoff", False)):
            anomalies.extend(_arm_and_takeoff(master, config.takeoff_altitude_m))
            if any(item in {"guided_mode_unavailable", "arm_failed"} for item in anomalies):
                run_status = "invalid_runtime"

        started = time.monotonic()
        end_deadline = started + profile.total_duration_s + 2.0
        while time.monotonic() < end_deadline:
            elapsed_s = time.monotonic() - started
            if config.input_chain == "attitude":
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
                profile_value, roll, pitch, yaw, throttle, phase = profile.manual_targets_at(elapsed_s)
                _send_manual_control(master, roll, pitch, yaw, throttle)
                input_profile_rows.append(
                    {
                        "publish_time_ns": time.time_ns(),
                        "elapsed_s": round(elapsed_s, 6),
                        "profile_value": profile_value,
                        "roll_body": roll,
                        "pitch_body": pitch,
                        "yaw_body": yaw,
                        "thrust_z": throttle,
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
                _append_message_rows(master, attitude_rows, position_rows, heartbeat_rows, status_rows)
                master.close()
            except Exception:
                pass
        _stop_process(process)

    end_time = datetime.now(timezone.utc).astimezone()
    host_end = capture_host_snapshot()
    bin_after = _snapshot_logs(ARDUPILOT_ROOT, (".bin",))
    bin_log_path = _resolve_latest_file(bin_before, bin_after)

    _write_telemetry_csv(paths["telemetry_dir"] / "attitude.csv", attitude_rows, ATTITUDE_FIELDNAMES)
    _write_telemetry_csv(paths["telemetry_dir"] / "local_position.csv", position_rows, LOCAL_POSITION_FIELDNAMES)
    _write_telemetry_csv(paths["telemetry_dir"] / "heartbeat.csv", heartbeat_rows, HEARTBEAT_FIELDNAMES)
    _write_telemetry_csv(paths["telemetry_dir"] / "sys_status.csv", status_rows, STATUS_FIELDNAMES)
    _write_telemetry_csv(paths["input_trace_path"], input_profile_rows, INPUT_TRACE_FIELDNAMES)

    metrics = {
        "run_id": run_id,
        "backend": BACKEND_NAME,
        "input_chain": config.input_chain,
        "profile_type": config.profile_type,
        "axis": config.axis,
        "input_peak": abs(config.amplitude),
        "heartbeat_count": len(heartbeat_rows),
        "attitude_samples": len(attitude_rows),
        "local_position_samples": len(position_rows),
        "status_samples": len(status_rows),
        "failsafe_event": int(any(row["system_status"] >= mavutil.mavlink.MAV_STATE_CRITICAL for row in heartbeat_rows)),
    }
    write_single_row_csv(
        paths["metrics_path"],
        metrics,
        [
            "run_id",
            "backend",
            "input_chain",
            "profile_type",
            "axis",
            "input_peak",
            "heartbeat_count",
            "attitude_samples",
            "local_position_samples",
            "status_samples",
            "failsafe_event",
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
        "ardupilot_bin_log_path": bin_log_path,
        "ardupilot_tlog_path": str(tlog_path),
        "host_snapshot_start": host_start,
        "host_snapshot_end": host_end,
        "anomaly_summary": anomalies,
    }
    write_yaml(paths["manifest_path"], manifest)

    notes = "\n".join(
        [
            f"# {run_id}",
            f"- backend: {BACKEND_NAME}",
            f"- status: {run_status}",
            f"- vehicle: {vehicle}",
            f"- frame: {frame}",
            f"- master_uri: {master_uri}",
            f"- ardupilot_bin_log_path: {bin_log_path or 'missing'}",
            f"- ardupilot_tlog_path: {tlog_path}",
            f"- anomalies: {', '.join(anomalies) if anomalies else 'none'}",
        ]
    )
    paths["notes_path"].write_text(notes, encoding="utf-8")
    return (0 if run_status == "completed" else 1), paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run a minimal ArduPilot MAVLink experiment and write artifacts.")
    parser.add_argument("--config", type=Path, required=True, help="YAML config path.")
    parser.add_argument("--vehicle", default="ArduCopter", help="ArduPilot vehicle, default ArduCopter.")
    parser.add_argument("--frame", default="quad", help="SITL frame, default quad.")
    parser.add_argument("--master", default=DEFAULT_MASTER, help="MAVLink master URI, default tcp:127.0.0.1:5760.")
    parser.add_argument("--skip-sitl", action="store_true", help="Connect to an existing ArduPilot instance instead of starting SITL.")
    parser.add_argument("--arm-and-takeoff", action="store_true", help="Attempt GUIDED arm/takeoff before sending commands.")
    args = parser.parse_args(argv)

    config = load_run_config(args.config)
    exit_code, artifact_dir = run_experiment(
        config,
        vehicle=args.vehicle,
        frame=args.frame,
        master_uri=args.master,
        start_sitl=not args.skip_sitl,
        arm_and_takeoff=args.arm_and_takeoff,
    )
    print(f"artifact_dir={artifact_dir}")
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
