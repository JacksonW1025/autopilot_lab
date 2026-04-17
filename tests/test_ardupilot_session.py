from __future__ import annotations

import os
from pathlib import Path

from ardupilot_mavlink_backend import session


def test_visualization_defaults_to_gui_when_display_is_available(monkeypatch) -> None:
    monkeypatch.delenv("AUTOPILOT_LAB_HEADLESS", raising=False)
    monkeypatch.setenv("DISPLAY", ":1")
    monkeypatch.delenv("WAYLAND_DISPLAY", raising=False)

    assert session._headless_enabled() is False
    assert session._visualization_enabled() is True


def test_visualization_respects_headless_override(monkeypatch) -> None:
    monkeypatch.setenv("AUTOPILOT_LAB_HEADLESS", "1")
    monkeypatch.setenv("DISPLAY", ":1")

    assert session._headless_enabled() is True
    assert session._visualization_enabled() is False


def test_visualization_explicit_false_overrides_display(monkeypatch) -> None:
    monkeypatch.delenv("AUTOPILOT_LAB_HEADLESS", raising=False)
    monkeypatch.setenv("DISPLAY", ":1")
    monkeypatch.delenv("WAYLAND_DISPLAY", raising=False)

    assert session._headless_enabled() is False
    assert session._visualization_enabled(False) is False


def test_visualizer_command_includes_map_when_supported(monkeypatch) -> None:
    monkeypatch.setattr(session, "_mavproxy_executable", lambda: "/usr/bin/mavproxy.py")

    command = session._visualizer_command("tcp:127.0.0.1:5760")

    assert command is not None
    assert "--console --map" in command[-1]


def test_finalize_visualization_report_detects_loaded_map(tmp_path: Path) -> None:
    log_path = tmp_path / "ardupilot_mavproxy.log"
    log_path.write_text("Loaded module console\nLoaded module map\n", encoding="utf-8")

    managed = session.ManagedSession(
        sitl_process=None,
        sitl_log_path=tmp_path / "ardupilot_sitl.log",
        visualizer_process=None,
        visualizer_log_path=log_path,
        visualization=session.VisualizationReport(
            requested=True,
            headless=False,
            mavproxy_started=True,
            map_requested=True,
        ),
    )

    report = session.finalize_visualization_report(managed)

    assert report["requested"] is True
    assert report["mavproxy_started"] is True
    assert report["map_requested"] is True
    assert report["map_loaded"] is True
    assert report["failure_reason"] == ""


def test_finalize_visualization_report_records_map_failure(tmp_path: Path, monkeypatch) -> None:
    log_path = tmp_path / "ardupilot_mavproxy.log"
    log_path.write_text("ModuleNotFoundError: No module named 'cv2'\n", encoding="utf-8")
    monkeypatch.setattr(session, "_mavproxy_map_supported", lambda: False)

    managed = session.ManagedSession(
        sitl_process=None,
        sitl_log_path=tmp_path / "ardupilot_sitl.log",
        visualizer_process=None,
        visualizer_log_path=log_path,
        visualization=session.VisualizationReport(
            requested=True,
            headless=False,
            mavproxy_started=False,
            map_requested=True,
        ),
    )

    report = session.finalize_visualization_report(managed)

    assert report["requested"] is True
    assert report["map_requested"] is True
    assert report["map_loaded"] is False
    assert report["failure_reason"] == "map_module_unavailable"


def test_matching_external_pids_ignores_ancestor_with_vehicle_name(monkeypatch) -> None:
    monkeypatch.setattr(session, "_ancestor_pids", lambda: {os.getpid(), 222})

    class _Completed:
        stdout = "\n".join(
            [
                "222 /usr/bin/python3 ... ardupilot_linearity_matrix --vehicle ArduCopter --frame quad",
                "333 python3 Tools/autotest/sim_vehicle.py -v ArduCopter -f quad --no-mavproxy",
                "444 /home/car/.local/bin/mavproxy.py --master=tcp:127.0.0.1:5760 --console --map",
            ]
        )

    monkeypatch.setattr(session.subprocess, "run", lambda *args, **kwargs: _Completed())

    assert session._matching_external_pids() == [333, 444]


def test_cleanup_residual_processes_escalates_until_processes_exit(monkeypatch) -> None:
    sent: list[tuple[int, int]] = []
    states = {333: 2}

    monkeypatch.setattr(session, "_matching_external_pids", lambda: [333])

    def _fake_exists(pid: int) -> bool:
        return states.get(pid, 0) > 0

    def _fake_kill(pid: int, sig: int) -> None:
        sent.append((pid, sig))
        states[pid] = max(0, states.get(pid, 0) - 1)

    monkeypatch.setattr(session, "_pid_exists", _fake_exists)
    monkeypatch.setattr(session.os, "kill", _fake_kill)
    monkeypatch.setattr(session.time, "sleep", lambda _seconds: None)

    session.cleanup_residual_processes()

    assert sent == [
        (333, session.signal.SIGINT),
        (333, session.signal.SIGTERM),
    ]


def test_cleanup_residual_processes_rescans_for_new_descendants(monkeypatch) -> None:
    sent: list[tuple[int, int]] = []
    scan_states = [[333], [333], [444], [444], []]

    def _fake_matching_external_pids():
        if scan_states:
            return scan_states.pop(0)
        return []

    monkeypatch.setattr(session, "_matching_external_pids", _fake_matching_external_pids)
    monkeypatch.setattr(session, "_pid_exists", lambda _pid: True)
    monkeypatch.setattr(session.os, "kill", lambda pid, sig: sent.append((pid, sig)))
    monkeypatch.setattr(session.time, "sleep", lambda _seconds: None)

    session.cleanup_residual_processes()

    assert sent == [
        (333, session.signal.SIGINT),
        (444, session.signal.SIGTERM),
    ]


def test_start_visualizer_launches_after_connection(tmp_path: Path, monkeypatch) -> None:
    log_path = tmp_path / "ardupilot_sitl.log"
    log_path.write_text("", encoding="utf-8")
    managed = session.ManagedSession(
        sitl_process=None,
        sitl_log_path=log_path,
        visualizer_process=None,
        visualizer_log_path=None,
        visualization=session.VisualizationReport(
            requested=True,
            headless=False,
        ),
    )

    class _FakeProcess:
        def poll(self):
            return None

    monkeypatch.setattr(session, "_mavproxy_executable", lambda: "/usr/bin/mavproxy.py")
    monkeypatch.setattr(session, "_visualizer_command", lambda *args, **kwargs: ["bash", "-lc", "echo ok"])
    monkeypatch.setattr(session.subprocess, "Popen", lambda *args, **kwargs: _FakeProcess())
    monkeypatch.setattr(session.time, "sleep", lambda _seconds: None)

    updated = session.start_visualizer(managed, "tcp:127.0.0.1:5760")

    assert updated.visualizer_process is not None
    assert updated.visualizer_log_path == tmp_path / "ardupilot_mavproxy.log"
    assert updated.visualization is not None
    assert updated.visualization.mavproxy_started is True
    assert updated.visualization.map_requested is True


def test_connect_allows_autoreconnect_override(monkeypatch, tmp_path: Path) -> None:
    captured: dict[str, object] = {}

    class _FakeMaster:
        def setup_logfile_raw(self, path: str) -> None:
            captured["logfile"] = path

        def wait_heartbeat(self, timeout: float) -> None:
            captured["timeout"] = timeout

        class mav:
            @staticmethod
            def request_data_stream_send(*args, **kwargs):  # noqa: ANN002,ARG003
                return None

        target_system = 1
        target_component = 1

    def _fake_connection(uri: str, source_system: int, autoreconnect: bool):
        captured["uri"] = uri
        captured["source_system"] = source_system
        captured["autoreconnect"] = autoreconnect
        return _FakeMaster()

    monkeypatch.setattr(session.mavutil, "mavlink_connection", _fake_connection)

    master = session.connect("tcp:127.0.0.1:5760", tmp_path / "mav.tlog", timeout_s=3.0, autoreconnect=False)

    assert isinstance(master, _FakeMaster)
    assert captured["autoreconnect"] is False
