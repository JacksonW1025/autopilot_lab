from __future__ import annotations

import os
import shlex
import shutil
import signal
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from linearity_core.paths import ARDUPILOT_ROOT
from pymavlink import mavutil

TARGET_PROCESS_TOKENS = (
    "Tools/autotest/sim_vehicle.py",
    "build/sitl/bin/arducopter",
    "build/sitl/bin/arducopter.elf",
    "mavproxy.py",
    "MAVProxy.py",
)


@dataclass(slots=True)
class ManagedSession:
    sitl_process: subprocess.Popen[str]
    sitl_log_path: Path
    visualizer_process: subprocess.Popen[str] | None = None
    visualizer_log_path: Path | None = None
    visualization: "VisualizationReport" | None = None


@dataclass(slots=True)
class VisualizationReport:
    requested: bool
    headless: bool
    mavproxy_started: bool = False
    map_requested: bool = False
    map_loaded: bool = False
    failure_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "requested": self.requested,
            "headless": self.headless,
            "mavproxy_started": self.mavproxy_started,
            "map_requested": self.map_requested,
            "map_loaded": self.map_loaded,
            "failure_reason": self.failure_reason,
        }


def _headless_enabled() -> bool:
    if os.environ.get("AUTOPILOT_LAB_HEADLESS", "").strip() == "1":
        return True
    if os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"):
        return False
    return True


def _mavproxy_executable() -> str | None:
    return shutil.which("mavproxy.py") or shutil.which("MAVProxy.py")


def _mavproxy_map_supported() -> bool:
    try:
        import cv2  # noqa: F401
    except Exception:
        return False
    return True


def _visualization_enabled(enable_visualization: bool | None = None) -> bool:
    if enable_visualization is not None:
        return bool(enable_visualization)
    return not _headless_enabled()


def _sitl_command(run_id: str, vehicle: str, frame: str) -> list[str]:
    return [
        "bash",
        "-lc",
        (
            f"cd {ARDUPILOT_ROOT} && "
            "stdbuf -oL -eL python3 Tools/autotest/sim_vehicle.py "
            f"-v {vehicle} -f {frame} --no-mavproxy -N -w --aircraft {run_id}"
        ),
    ]


def _visualizer_command(master_uri: str, *, executable: str | None = None, request_map: bool = True) -> list[str] | None:
    executable = executable or _mavproxy_executable()
    if executable is None:
        return None
    modules = ["--console"]
    if request_map:
        modules.append("--map")
    joined = " ".join(modules)
    return [
        "bash",
        "-lc",
        f"exec {shlex.quote(executable)} --master={shlex.quote(master_uri)} {joined}",
    ]


def _read_visualizer_log(path: Path | None) -> str:
    if path is None or not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _visualizer_log_failure_reason(log_text: str) -> str:
    lowered = log_text.lower()
    if "no module named 'cv2'" in lowered or "no module named cv2" in lowered:
        return "map_module_unavailable"
    if "failed to load module map" in lowered or ("module map" in lowered and "failed" in lowered):
        return "map_load_failed"
    if "connection refused" in lowered or "link 1 down" in lowered:
        return "mavproxy_connection_failed"
    if "traceback" in lowered:
        return "mavproxy_runtime_error"
    return "mavproxy_exited_early"


def _ancestor_pids() -> set[int]:
    ancestors: set[int] = set()
    pid = os.getpid()
    while pid > 1 and pid not in ancestors:
        ancestors.add(pid)
        try:
            stat_fields = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8").split()
        except OSError:
            break
        if len(stat_fields) < 4:
            break
        try:
            pid = int(stat_fields[3])
        except ValueError:
            break
    return ancestors


def _matching_external_pids() -> list[int]:
    protected = _ancestor_pids()
    result = subprocess.run(
        ["ps", "-eo", "pid=,args="],
        check=True,
        capture_output=True,
        text=True,
    )
    matches: list[int] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        pid_text, command = parts
        try:
            pid = int(pid_text)
        except ValueError:
            continue
        if pid in protected:
            continue
        if any(token in command for token in TARGET_PROCESS_TOKENS):
            matches.append(pid)
    return matches


def _pid_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def cleanup_residual_processes() -> None:
    # Rescan after each escalation stage so newly orphaned descendants do not survive.
    for _ in range(4):
        matched = _matching_external_pids()
        if not matched:
            return
        for sig, wait_s in ((signal.SIGINT, 2.0), (signal.SIGTERM, 2.0), (signal.SIGKILL, 1.0)):
            current = _matching_external_pids()
            if not current:
                return
            for pid in current:
                if not _pid_exists(pid):
                    continue
                try:
                    os.kill(pid, sig)
                except ProcessLookupError:
                    continue
                except PermissionError:
                    continue
            time.sleep(wait_s)
            if not _matching_external_pids():
                return


def start_sitl(
    run_id: str,
    vehicle: str,
    frame: str,
    log_path: Path,
    *,
    enable_visualization: bool | None = None,
    master_uri: str = "tcp:127.0.0.1:5760",
) -> ManagedSession:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    sitl_handle = log_path.open("w", encoding="utf-8")
    sitl_process = subprocess.Popen(_sitl_command(run_id, vehicle, frame), stdout=sitl_handle, stderr=subprocess.STDOUT, text=True)

    visualization = VisualizationReport(
        requested=_visualization_enabled(enable_visualization),
        headless=_headless_enabled(),
    )

    return ManagedSession(
        sitl_process=sitl_process,
        sitl_log_path=log_path,
        visualizer_process=None,
        visualizer_log_path=None,
        visualization=visualization,
    )


def start_visualizer(session: ManagedSession, master_uri: str) -> ManagedSession:
    if session.visualization is None:
        session.visualization = VisualizationReport(requested=False, headless=_headless_enabled())
    if not session.visualization.requested:
        return session
    if session.visualizer_process is not None and session.visualizer_process.poll() is None:
        return session

    session.visualization.map_requested = True
    executable = _mavproxy_executable()
    if executable is None:
        session.visualization.failure_reason = "mavproxy_missing"
        return session

    visualizer_command = _visualizer_command(master_uri, executable=executable, request_map=True)
    if visualizer_command is None:
        session.visualization.failure_reason = "mavproxy_missing"
        return session

    session.visualizer_log_path = session.sitl_log_path.parent / "ardupilot_mavproxy.log"
    visualizer_handle = session.visualizer_log_path.open("w", encoding="utf-8")
    time.sleep(1.0)
    session.visualizer_process = subprocess.Popen(
        visualizer_command,
        stdout=visualizer_handle,
        stderr=subprocess.STDOUT,
        text=True,
    )
    time.sleep(1.0)
    if session.visualizer_process.poll() is None:
        session.visualization.mavproxy_started = True
        session.visualization.failure_reason = ""
    else:
        session.visualization.failure_reason = _visualizer_log_failure_reason(_read_visualizer_log(session.visualizer_log_path))
    return session


def _stop_one(process: subprocess.Popen[str] | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=10.0)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5.0)


def stop_process(process: ManagedSession | subprocess.Popen[str] | None) -> None:
    if process is None:
        return
    if isinstance(process, ManagedSession):
        _stop_one(process.visualizer_process)
        _stop_one(process.sitl_process)
        return
    if process.poll() is not None:
        return
    _stop_one(process)


def finalize_visualization_report(process: ManagedSession | None) -> dict[str, Any]:
    if process is None or process.visualization is None:
        return VisualizationReport(requested=False, headless=_headless_enabled()).to_dict()

    report = VisualizationReport(**process.visualization.to_dict())
    log_text = _read_visualizer_log(process.visualizer_log_path)
    if report.map_requested and "loaded module map" in log_text.lower():
        report.map_loaded = True
    if report.requested and not report.mavproxy_started and not report.failure_reason:
        report.failure_reason = _visualizer_log_failure_reason(log_text)
    if report.requested and report.map_requested and not report.map_loaded and not report.failure_reason:
        if not _mavproxy_map_supported():
            report.failure_reason = "map_module_unavailable"
        else:
            report.failure_reason = "map_not_confirmed"
    return report.to_dict()


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
    mapping = master.mode_mapping() or {}
    expected_custom_mode = None
    for name, value in mapping.items():
        if str(name).strip().upper() == expected:
            expected_custom_mode = int(value)
            break
    while time.monotonic() < deadline:
        heartbeat = master.recv_match(type="HEARTBEAT", blocking=True, timeout=0.5)
        if str(getattr(master, "flightmode", "")).strip().upper() == expected:
            return True
        if heartbeat is not None and expected_custom_mode is not None:
            custom_mode = getattr(heartbeat, "custom_mode", None)
            if custom_mode is not None and int(custom_mode) == expected_custom_mode:
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
