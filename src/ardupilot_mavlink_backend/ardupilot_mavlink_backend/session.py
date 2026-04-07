from __future__ import annotations

import subprocess
import time
from pathlib import Path

from linearity_core.paths import ARDUPILOT_ROOT
from pymavlink import mavutil


def cleanup_residual_processes() -> None:
    subprocess.run(
        [
            "bash",
            "-lc",
            "pkill -INT -f 'sim_vehicle.py|arducopter|arducopter.elf|ArduCopter' || true",
        ],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2.0)


def start_sitl(run_id: str, vehicle: str, frame: str, log_path: Path) -> subprocess.Popen[str]:
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


def stop_process(process: subprocess.Popen[str] | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=10.0)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5.0)


def connect(
    master_uri: str,
    tlog_path: Path,
    timeout_s: float,
    stream_rate_hz: int = 20,
) -> mavutil.mavfile:
    tlog_path.parent.mkdir(parents=True, exist_ok=True)
    tlog_path.touch(exist_ok=True)
    master = mavutil.mavlink_connection(master_uri, source_system=250, autoreconnect=True)
    master.setup_logfile_raw(str(tlog_path))
    master.wait_heartbeat(timeout=timeout_s)
    master.mav.request_data_stream_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_ALL,
        stream_rate_hz,
        1,
    )
    return master


def wait_for_mode(master: mavutil.mavfile, expected_mode: str, timeout_s: float = 10.0) -> bool:
    deadline = time.monotonic() + timeout_s
    expected = expected_mode.strip().upper()
    while time.monotonic() < deadline:
        master.recv_match(type="HEARTBEAT", blocking=True, timeout=0.5)
        if str(getattr(master, "flightmode", "")).strip().upper() == expected:
            return True
    return str(getattr(master, "flightmode", "")).strip().upper() == expected


def wait_for_message(master: mavutil.mavfile, message_type: str, timeout_s: float = 5.0):
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        message = master.recv_match(type=message_type, blocking=True, timeout=0.5)
        if message is not None:
            return message
    return None


def wait_for_takeoff_altitude(master: mavutil.mavfile, target_altitude_m: float, timeout_s: float = 15.0) -> bool:
    threshold_altitude_m = max(target_altitude_m * 0.70, min(target_altitude_m, 0.8))
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        message = master.recv_match(type="LOCAL_POSITION_NED", blocking=True, timeout=0.5)
        if message is None:
            continue
        if abs(float(message.z)) >= threshold_altitude_m:
            return True
    return False
