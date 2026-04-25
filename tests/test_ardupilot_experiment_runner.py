from __future__ import annotations

import csv
from pathlib import Path
from types import SimpleNamespace

from pymavlink import mavutil

from ardupilot_mavlink_backend import experiment_runner
from ardupilot_mavlink_backend.session import wait_for_mode
from linearity_core.attack_runtime import AttackDelta
from linearity_core.config import RunConfig
from linearity_core.io import read_yaml, write_rows_csv


class _FakeMav:
    def __init__(self) -> None:
        self.calls: list[tuple[int, int, int]] = []

    def set_mode_send(self, target_system: int, base_mode: int, custom_mode: int) -> None:
        self.calls.append((target_system, base_mode, custom_mode))


class _FakeMaster:
    def __init__(self, mapping: dict[str, int] | None = None) -> None:
        self._mapping = mapping or {}
        self.target_system = 1
        self.mav = _FakeMav()
        self.set_mode_apm_calls: list[str] = []
        self.flightmode = ""
        self._messages: list[object] = []

    def mode_mapping(self) -> dict[str, int]:
        return dict(self._mapping)

    def set_mode_apm(self, mode_name: str) -> None:
        self.set_mode_apm_calls.append(mode_name)
        raise RuntimeError("set_mode_apm should not be needed when mapping exists")

    def recv_match(self, type=None, blocking=False, timeout=None):  # noqa: ANN001,ARG002
        if self._messages:
            return self._messages.pop(0)
        return None


def test_set_mode_prefers_mapping_without_set_mode_apm() -> None:
    master = _FakeMaster({"LAND": 9})

    ok = experiment_runner._set_mode(master, "LAND")

    assert ok is True
    assert master.set_mode_apm_calls == []
    assert master.mav.calls == [
        (
            1,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            9,
        )
    ]


def test_prepare_runtime_arming_retries_until_parameter_write_succeeds(monkeypatch) -> None:
    attempts = {"count": 0}

    def _fake_set_parameter(master, name, value, timeout_s=0.0):  # noqa: ANN001
        attempts["count"] += 1
        return attempts["count"] >= 3

    monkeypatch.setattr(experiment_runner, "fetch_parameter", lambda *args, **kwargs: 1.0)
    monkeypatch.setattr(experiment_runner, "set_parameter", _fake_set_parameter)
    monkeypatch.setattr(experiment_runner.time, "sleep", lambda _seconds: None)

    snapshot_after = {}
    anomalies = experiment_runner._prepare_runtime_arming(SimpleNamespace(), snapshot_after)

    assert anomalies == []
    assert attempts["count"] == 3
    assert snapshot_after["ARMING_CHECK"] == 0.0


def test_wait_for_mode_accepts_matching_custom_mode() -> None:
    master = _FakeMaster({"STABILIZE": 0})
    master._messages = [SimpleNamespace(custom_mode=0)]

    assert wait_for_mode(master, "STABILIZE", timeout_s=0.1) is True


def test_apply_bin_canonical_fallback_synthesizes_missing_csvs(tmp_path: Path) -> None:
    telemetry_dir = tmp_path / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    input_trace_path = telemetry_dir / "input_trace.csv"
    write_rows_csv(
        input_trace_path,
        [
            {
                "publish_time_ns": 1_000_000_000,
                "elapsed_s": 0.0,
                "profile_value": 0.1,
                "roll_body": 0.0,
                "pitch_body": 0.0,
                "yaw_body": 0.0,
                "thrust_z": -0.69,
                "command_roll": 0.0,
                "command_pitch": 0.0,
                "command_yaw": 0.0,
                "command_throttle": 0.1,
                "phase": "hold_active",
            }
        ],
    )
    for filename, fieldnames in (
        ("attitude.csv", experiment_runner.ATTITUDE_FIELDNAMES),
        ("local_position.csv", experiment_runner.LOCAL_POSITION_FIELDNAMES),
        ("heartbeat.csv", experiment_runner.HEARTBEAT_FIELDNAMES),
        ("sys_status.csv", experiment_runner.STATUS_FIELDNAMES),
    ):
        with (telemetry_dir / filename).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()

    write_rows_csv(
        telemetry_dir / "bin_att.csv",
        [
            {
                "received_time_ns": 1_000_000,
                "des_roll": 0.0,
                "roll": 10.0,
                "des_pitch": 0.0,
                "pitch": -5.0,
                "des_yaw": 350.0,
                "yaw": 355.0,
                "err_rp": 0.0,
                "err_yaw": 0.0,
            }
        ],
    )
    write_rows_csv(
        telemetry_dir / "bin_rate.csv",
        [
            {
                "received_time_ns": 1_000_000,
                "des_roll_rate": 0.0,
                "roll_rate": 0.11,
                "roll_out": 0.0,
                "des_pitch_rate": 0.0,
                "pitch_rate": -0.22,
                "pitch_out": 0.0,
                "des_yaw_rate": 0.0,
                "yaw_rate": 0.33,
                "yaw_out": 0.0,
            }
        ],
    )
    write_rows_csv(
        telemetry_dir / "bin_pos.csv",
        [
            {
                "received_time_ns": 1_000_000,
                "lat_deg": -35.0,
                "lon_deg": 149.0,
                "alt_m": 580.0,
                "rel_home_alt_m": 1.5,
                "rel_origin_alt_m": 1.5,
            },
            {
                "received_time_ns": 2_000_000,
                "lat_deg": -34.999999,
                "lon_deg": 149.000001,
                "alt_m": 580.1,
                "rel_home_alt_m": 1.6,
                "rel_origin_alt_m": 1.6,
            },
        ],
    )
    write_rows_csv(
        telemetry_dir / "bin_orgn.csv",
        [
            {
                "received_time_ns": 500_000,
                "type": 0,
                "lat_deg": -35.0,
                "lon_deg": 149.0,
                "alt_m": 578.5,
            }
        ],
    )
    write_rows_csv(
        telemetry_dir / "bin_mode.csv",
        [
            {
                "received_time_ns": 800_000,
                "mode": 0,
                "mode_num": 0,
                "reason": 0,
            }
        ],
    )
    write_rows_csv(
        telemetry_dir / "bin_bat.csv",
        [
            {
                "received_time_ns": 900_000,
                "instance": 0,
                "voltage_v": 12.588,
                "current_a": 1.23,
                "battery_remaining_pct": 87,
            }
        ],
    )

    sources = experiment_runner._apply_bin_canonical_fallback(
        {
            "telemetry_dir": telemetry_dir,
            "input_trace_path": input_trace_path,
        },
        {"experiment_start_time_ns": 1_000_000_000},
        experiment_runner._sorted_csv_rows(input_trace_path, "publish_time_ns"),
        900_000_000,
    )

    assert sources == {
        "attitude.csv": "bin_fallback",
        "local_position.csv": "bin_fallback",
        "heartbeat.csv": "bin_fallback",
        "sys_status.csv": "bin_fallback",
    }
    attitude_rows = experiment_runner._sorted_csv_rows(telemetry_dir / "attitude.csv", "received_time_ns")
    assert len(attitude_rows) == 1
    assert abs(float(attitude_rows[0]["roll"]) - 0.1745329) < 1e-5
    assert abs(float(attitude_rows[0]["pitch"]) + 0.0872664) < 1e-5
    assert abs(float(attitude_rows[0]["yawspeed"]) - 0.33) < 1e-9

    position_rows = experiment_runner._sorted_csv_rows(telemetry_dir / "local_position.csv", "received_time_ns")
    assert len(position_rows) == 2
    assert abs(float(position_rows[0]["z"]) + 1.5) < 1e-9
    heartbeat_rows = experiment_runner._sorted_csv_rows(telemetry_dir / "heartbeat.csv", "received_time_ns")
    assert heartbeat_rows[0]["custom_mode"] == "0"
    status_rows = experiment_runner._sorted_csv_rows(telemetry_dir / "sys_status.csv", "received_time_ns")
    assert status_rows[0]["voltage_battery"] == "12588"
    assert status_rows[0]["battery_remaining"] == "87"


def test_apply_bin_canonical_fallback_preserves_nonempty_live_csv(tmp_path: Path) -> None:
    telemetry_dir = tmp_path / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    input_trace_path = telemetry_dir / "input_trace.csv"
    write_rows_csv(input_trace_path, [])
    write_rows_csv(
        telemetry_dir / "attitude.csv",
        [
            {
                "received_time_ns": 123,
                "roll": 0.01,
                "pitch": 0.02,
                "yaw": 0.03,
                "rollspeed": 0.1,
                "pitchspeed": 0.2,
                "yawspeed": 0.3,
            }
        ],
    )
    for filename, fieldnames in (
        ("local_position.csv", experiment_runner.LOCAL_POSITION_FIELDNAMES),
        ("heartbeat.csv", experiment_runner.HEARTBEAT_FIELDNAMES),
        ("sys_status.csv", experiment_runner.STATUS_FIELDNAMES),
    ):
        with (telemetry_dir / filename).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
    write_rows_csv(
        telemetry_dir / "bin_att.csv",
        [
            {
                "received_time_ns": 1,
                "des_roll": 0.0,
                "roll": 10.0,
                "des_pitch": 0.0,
                "pitch": 0.0,
                "des_yaw": 0.0,
                "yaw": 0.0,
                "err_rp": 0.0,
                "err_yaw": 0.0,
            }
        ],
    )

    sources = experiment_runner._apply_bin_canonical_fallback(
        {
            "telemetry_dir": telemetry_dir,
            "input_trace_path": input_trace_path,
        },
        {"experiment_start_time_ns": 0},
        [],
        500,
    )

    assert sources["attitude.csv"] == "live_mavlink"
    attitude_rows = experiment_runner._sorted_csv_rows(telemetry_dir / "attitude.csv", "received_time_ns")
    assert attitude_rows[0]["received_time_ns"] == "123"


def test_arm_vehicle_bootstraps_guided_nogps_via_stabilize(monkeypatch) -> None:
    calls: list[tuple[str, str]] = []

    def _fake_set_mode(master, mode_name):  # noqa: ANN001
        calls.append(("set", mode_name))
        return True

    def _fake_wait_for_mode(master, mode_name, timeout_s=0.0):  # noqa: ANN001,ARG001
        calls.append(("wait", mode_name))
        return True

    monkeypatch.setattr(experiment_runner, "_set_mode", _fake_set_mode)
    monkeypatch.setattr(experiment_runner, "wait_for_mode", _fake_wait_for_mode)
    monkeypatch.setattr(experiment_runner, "_wait_for_armed", lambda *args, **kwargs: True)
    monkeypatch.setattr(experiment_runner.time, "sleep", lambda _seconds: None)

    master = SimpleNamespace(arducopter_arm=lambda: calls.append(("arm", "arducopter_arm")))
    anomalies = experiment_runner._arm_vehicle(master, "GUIDED_NOGPS", timeout_s=3.0)

    assert anomalies == []
    assert calls == [
        ("set", "STABILIZE"),
        ("wait", "STABILIZE"),
        ("arm", "arducopter_arm"),
        ("set", "GUIDED_NOGPS"),
        ("wait", "GUIDED_NOGPS"),
    ]


def test_arm_vehicle_guided_nogps_tolerates_prearm_stabilize_confirmation_flake(monkeypatch) -> None:
    calls: list[tuple[str, str]] = []
    wait_results = {
        "STABILIZE": [False, True],
        "GUIDED_NOGPS": [True],
    }

    def _fake_set_mode(master, mode_name):  # noqa: ANN001
        calls.append(("set", mode_name))
        return True

    def _fake_wait_for_mode(master, mode_name, timeout_s=0.0):  # noqa: ANN001,ARG001
        calls.append(("wait", mode_name))
        values = wait_results[mode_name]
        return values.pop(0) if values else False

    monkeypatch.setattr(experiment_runner, "_set_mode", _fake_set_mode)
    monkeypatch.setattr(experiment_runner, "wait_for_mode", _fake_wait_for_mode)
    monkeypatch.setattr(experiment_runner, "_wait_for_armed", lambda *args, **kwargs: True)
    monkeypatch.setattr(experiment_runner.time, "sleep", lambda _seconds: None)

    master = SimpleNamespace(arducopter_arm=lambda: calls.append(("arm", "arducopter_arm")))
    anomalies = experiment_runner._arm_vehicle(master, "GUIDED_NOGPS", timeout_s=3.0)

    assert anomalies == []
    assert calls == [
        ("set", "STABILIZE"),
        ("wait", "STABILIZE"),
        ("set", "STABILIZE"),
        ("wait", "STABILIZE"),
        ("arm", "arducopter_arm"),
        ("set", "GUIDED_NOGPS"),
        ("wait", "GUIDED_NOGPS"),
    ]


def test_run_capture_disables_autoreconnect(monkeypatch, tmp_path: Path) -> None:
    captured: dict[str, object] = {}

    class _FakeProfile:
        total_duration_s = 0.0

    class _FakeConnectedMaster:
        def __init__(self) -> None:
            self.autoreconnect = False

        def close(self) -> None:
            captured["closed"] = True

    def _fake_connect(uri: str, tlog_path: Path, timeout_s: float, *, autoreconnect: bool):
        captured["uri"] = uri
        captured["tlog_path"] = tlog_path
        captured["timeout_s"] = timeout_s
        captured["autoreconnect"] = autoreconnect
        tlog_path.parent.mkdir(parents=True, exist_ok=True)
        tlog_path.write_bytes(b"")
        return _FakeConnectedMaster()

    monkeypatch.setattr(experiment_runner, "ARDUPILOT_RAW_ROOT", tmp_path / "raw")
    monkeypatch.setattr(experiment_runner, "ARDUPILOT_ROOT", tmp_path / "ardupilot")
    monkeypatch.setattr(experiment_runner, "ExcitationGenerator", lambda config: _FakeProfile())
    monkeypatch.setattr(experiment_runner, "connect", _fake_connect)
    monkeypatch.setattr(experiment_runner, "cleanup_residual_processes", lambda: None)
    monkeypatch.setattr(experiment_runner, "_wait_for_vehicle_ready", lambda *args, **kwargs: [])
    monkeypatch.setattr(experiment_runner, "_prepare_parameters", lambda *args, **kwargs: ({}, {}, []))
    monkeypatch.setattr(experiment_runner, "_prepare_runtime_arming", lambda *args, **kwargs: [])
    monkeypatch.setattr(experiment_runner, "_arm_vehicle", lambda *args, **kwargs: [])
    monkeypatch.setattr(experiment_runner, "_append_message_rows", lambda *args, **kwargs: None)
    monkeypatch.setattr(experiment_runner, "_land_vehicle", lambda *args, **kwargs: None)
    monkeypatch.setattr(experiment_runner, "stop_process", lambda process: None)
    monkeypatch.setattr(experiment_runner, "finalize_visualization_report", lambda process: {})
    monkeypatch.setattr(experiment_runner, "capture_host_snapshot", lambda: {})
    monkeypatch.setattr(experiment_runner, "_snapshot_logs", lambda *args, **kwargs: {})
    monkeypatch.setattr(experiment_runner, "_apply_bin_canonical_fallback", lambda *args, **kwargs: {})
    monkeypatch.setattr(
        experiment_runner,
        "_ardupilot_data_quality",
        lambda *args, **kwargs: {
            "topic_presence": {"missing_topics": []},
            "quality_flags": {
                "non_monotonic_streams": [],
                "alignment_p95_exceeded_streams": [],
            },
            "acceptance": experiment_runner.build_acceptance_block(
                experiment_started=True,
                active_phase_present=True,
                expected_active_samples=0,
                active_sample_count=0,
                active_nonzero_command_samples=0,
                failsafe_during_experiment=False,
                missing_topics_blocking=[],
                accepted=True,
            ),
        },
    )

    config = RunConfig.from_dict(
        {
            "study_name": "unit_test",
            "backend": "ardupilot",
            "flight_mode": "GUIDED_NOGPS",
            "scenario": "connect_override",
            "config_profile": "test",
            "seed": 1,
            "repeat_count": 1,
            "sampling_rate_hz": 10.0,
            "x_schema": "state_minimal_v1",
            "input_type": "manual",
            "axis": "throttle",
            "profile_type": "pulse_train",
            "duration_s": 0.0,
            "extras": {
                "ardupilot_tail_s": -1.0,
            },
        }
    )

    exit_code, artifact_dir = experiment_runner.run_capture(
        config,
        start_sitl=False,
        master_uri="tcp:127.0.0.1:5760",
        connect_timeout_s=3.5,
    )

    assert exit_code == 0
    assert artifact_dir.exists()
    assert captured == {
        "uri": "tcp:127.0.0.1:5760",
        "tlog_path": artifact_dir / "telemetry" / "ardupilot.tlog",
        "timeout_s": 3.5,
        "autoreconnect": False,
        "closed": True,
    }


def test_run_capture_uses_visualizer_bridge_uri_when_visualization_enabled(monkeypatch, tmp_path: Path) -> None:
    captured: dict[str, object] = {}

    class _FakeProfile:
        total_duration_s = 0.0

    class _FakeConnectedMaster:
        def __init__(self) -> None:
            self.autoreconnect = False

        def close(self) -> None:
            captured["closed"] = True

    def _fake_connect(uri: str, tlog_path: Path, timeout_s: float, *, autoreconnect: bool):
        captured["uri"] = uri
        captured["tlog_path"] = tlog_path
        captured["timeout_s"] = timeout_s
        captured["autoreconnect"] = autoreconnect
        tlog_path.parent.mkdir(parents=True, exist_ok=True)
        tlog_path.write_bytes(b"")
        return _FakeConnectedMaster()

    def _fake_start_sitl(*args, **kwargs):  # noqa: ANN002,ANN003
        del args, kwargs
        return SimpleNamespace(
            sitl_process=None,
            sitl_log_path=tmp_path / "ardupilot_sitl.log",
            visualizer_process=None,
            visualizer_log_path=None,
            visualization=SimpleNamespace(requested=True),
            control_master_uri="tcp:127.0.0.1:5760",
        )

    def _fake_start_visualizer(process, master_uri):  # noqa: ANN001
        captured["visualizer_master_uri"] = master_uri
        process.control_master_uri = "tcp:127.0.0.1:5770"
        return process

    monkeypatch.setattr(experiment_runner, "ARDUPILOT_RAW_ROOT", tmp_path / "raw")
    monkeypatch.setattr(experiment_runner, "ARDUPILOT_ROOT", tmp_path / "ardupilot")
    monkeypatch.setattr(experiment_runner, "ExcitationGenerator", lambda config: _FakeProfile())
    monkeypatch.setattr(experiment_runner, "start_sitl_process", _fake_start_sitl)
    monkeypatch.setattr(experiment_runner, "start_visualizer", _fake_start_visualizer)
    monkeypatch.setattr(experiment_runner, "connect", _fake_connect)
    monkeypatch.setattr(experiment_runner, "cleanup_residual_processes", lambda: None)
    monkeypatch.setattr(experiment_runner, "_wait_for_vehicle_ready", lambda *args, **kwargs: [])
    monkeypatch.setattr(experiment_runner, "_prepare_parameters", lambda *args, **kwargs: ({}, {}, []))
    monkeypatch.setattr(experiment_runner, "_prepare_runtime_arming", lambda *args, **kwargs: [])
    monkeypatch.setattr(experiment_runner, "_arm_vehicle", lambda *args, **kwargs: [])
    monkeypatch.setattr(experiment_runner, "_append_message_rows", lambda *args, **kwargs: None)
    monkeypatch.setattr(experiment_runner, "_land_vehicle", lambda *args, **kwargs: None)
    monkeypatch.setattr(experiment_runner, "stop_process", lambda process: None)
    monkeypatch.setattr(experiment_runner, "finalize_visualization_report", lambda process: {})
    monkeypatch.setattr(experiment_runner, "capture_host_snapshot", lambda: {})
    monkeypatch.setattr(experiment_runner, "_snapshot_logs", lambda *args, **kwargs: {})
    monkeypatch.setattr(experiment_runner, "_apply_bin_canonical_fallback", lambda *args, **kwargs: {})
    monkeypatch.setattr(
        experiment_runner,
        "_ardupilot_data_quality",
        lambda *args, **kwargs: {
            "topic_presence": {"missing_topics": []},
            "quality_flags": {
                "non_monotonic_streams": [],
                "alignment_p95_exceeded_streams": [],
            },
            "acceptance": experiment_runner.build_acceptance_block(
                experiment_started=True,
                active_phase_present=True,
                expected_active_samples=0,
                active_sample_count=0,
                active_nonzero_command_samples=0,
                failsafe_during_experiment=False,
                missing_topics_blocking=[],
                accepted=True,
            ),
        },
    )

    config = RunConfig.from_dict(
        {
            "study_name": "visualizer_bridge_unit",
            "backend": "ardupilot",
            "flight_mode": "GUIDED_NOGPS",
            "scenario": "bridge",
            "config_profile": "bridge",
            "seed": 2,
            "repeat_count": 1,
            "sampling_rate_hz": 10.0,
            "x_schema": "state_minimal_v1",
            "input_type": "manual",
            "axis": "throttle",
            "profile_type": "pulse_train",
            "duration_s": 0.0,
            "extras": {"ardupilot_tail_s": -1.0},
        }
    )

    exit_code, artifact_dir = experiment_runner.run_capture(
        config,
        start_sitl=True,
        master_uri="tcp:127.0.0.1:5760",
        connect_timeout_s=3.5,
    )

    assert exit_code == 0
    assert artifact_dir.exists()
    assert captured["visualizer_master_uri"] == "tcp:127.0.0.1:5760"
    assert captured["uri"] == "tcp:127.0.0.1:5770"


def test_run_capture_writes_attack_trace_when_attack_injection_is_enabled(tmp_path: Path, monkeypatch) -> None:
    class _ManualMav:
        def __init__(self) -> None:
            self.manual_control_calls: list[tuple[int, int, int, int, int, int]] = []

        def manual_control_send(self, *args):  # noqa: ANN001
            self.manual_control_calls.append(args)

    class _ManualMaster:
        def __init__(self) -> None:
            self.target_system = 1
            self.target_component = 1
            self.mav = _ManualMav()
            self.autoreconnect = False
            self.closed = False

        def close(self) -> None:
            self.closed = True

    class _FakeAttackController:
        def __init__(self) -> None:
            self.method_spec = SimpleNamespace(
                method_name="family_aware_usdta_v1",
                line_code="AP-DAB",
                candidate_id="winner_01",
                search_iteration=1,
            )

        def reset(self) -> None:
            return None

        def generate(self, context):  # noqa: ANN001
            del context
            return AttackDelta(
                line_code="AP-DAB",
                family_name="family_aware_usdta_v1",
                active=True,
                delta_command=(0.05, 0.0, 0.0, 0.02),
                pre_projection_command=(0.06, 0.0, 0.0, 0.03),
                objective_terms={
                    "bundle_gain": 0.18,
                    "tracking_deviation": 0.08,
                    "attitude_deviation": 0.05,
                    "boundary_stress": 0.12,
                    "recovery_cost": 0.03,
                    "off_target_leakage": 0.10,
                    "conditioning": 0.12,
                    "budget": 0.22,
                },
                objective_score=0.16,
                budget_terms={
                    "cumulative_energy": 0.04,
                    "energy_limit": 0.35,
                    "budget_usage": 0.22,
                },
                context_features={
                    "context_drive": 0.26,
                    "bundle_drive": 0.30,
                    "temporal_mean": 0.18,
                    "temporal_slope": 0.10,
                    "temporal_curvature": 0.07,
                    "temporal_energy": 0.20,
                    "schedule": 0.90,
                    "conditioning_factor": 0.80,
                    "leakage_factor": 0.82,
                    "recovery_factor": 0.88,
                },
                notes=(),
            )

    fake_master = _ManualMaster()
    monotonic_values = iter([0.0, 0.01, 0.02, 0.20])

    monkeypatch.setattr(experiment_runner, "ARDUPILOT_RAW_ROOT", tmp_path / "raw")
    monkeypatch.setattr(experiment_runner, "cleanup_residual_processes", lambda: None)
    monkeypatch.setattr(experiment_runner, "connect", lambda *args, **kwargs: fake_master)
    monkeypatch.setattr(experiment_runner, "_wait_for_vehicle_ready", lambda *args, **kwargs: [])
    monkeypatch.setattr(experiment_runner, "_prepare_parameters", lambda *args, **kwargs: ({}, {}, []))
    monkeypatch.setattr(experiment_runner, "_prepare_runtime_arming", lambda *args, **kwargs: [])
    monkeypatch.setattr(experiment_runner, "_arm_vehicle", lambda *args, **kwargs: [])
    monkeypatch.setattr(experiment_runner, "_land_vehicle", lambda *args, **kwargs: None)
    monkeypatch.setattr(experiment_runner, "_restore_parameters", lambda *args, **kwargs: [])
    monkeypatch.setattr(experiment_runner, "stop_process", lambda *args, **kwargs: None)
    monkeypatch.setattr(experiment_runner, "finalize_visualization_report", lambda *args, **kwargs: {})
    monkeypatch.setattr(experiment_runner, "_snapshot_logs", lambda *args, **kwargs: {})
    monkeypatch.setattr(experiment_runner, "_resolve_latest_file", lambda *args, **kwargs: None)
    monkeypatch.setattr(experiment_runner, "capture_host_snapshot", lambda: {"uptime": "test", "loadavg": "0 0 0"})
    monkeypatch.setattr(experiment_runner, "_apply_bin_canonical_fallback", lambda *args, **kwargs: {})
    monkeypatch.setattr(
        experiment_runner,
        "_ardupilot_data_quality",
        lambda *args, **kwargs: {
            "topic_presence": {"missing_topics": []},
            "quality_flags": {
                "non_monotonic_streams": [],
                "alignment_p95_exceeded_streams": [],
            },
            "acceptance": experiment_runner.build_acceptance_block(
                experiment_started=True,
                active_phase_present=True,
                expected_active_samples=1,
                active_sample_count=1,
                active_nonzero_command_samples=1,
                failsafe_during_experiment=False,
                missing_topics_blocking=[],
                accepted=True,
            ),
        },
    )
    monkeypatch.setattr(experiment_runner, "build_attack_controller_from_config", lambda *args, **kwargs: _FakeAttackController())
    monkeypatch.setattr(experiment_runner.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(experiment_runner.time, "monotonic", lambda: next(monotonic_values))

    def _append_message_rows(master, attitude_rows, position_rows, heartbeat_rows, status_rows, position_origin):  # noqa: ANN001
        del master
        timestamp = 1_000_000_000 + len(attitude_rows)
        attitude_rows.append(
            {
                "received_time_ns": timestamp,
                "roll": 0.10,
                "pitch": -0.02,
                "yaw": 0.03,
                "rollspeed": 0.05,
                "pitchspeed": -0.01,
                "yawspeed": 0.02,
            }
        )
        position_rows.append(
            {
                "received_time_ns": timestamp,
                "x": 0.0,
                "y": 0.0,
                "z": -1.2,
                "vx": 0.0,
                "vy": 0.0,
                "vz": -0.05,
            }
        )
        heartbeat_rows.append(
            {
                "received_time_ns": timestamp,
                "base_mode": 0,
                "custom_mode": 0,
                "system_status": 0,
            }
        )
        status_rows.append(
            {
                "received_time_ns": timestamp,
                "voltage_battery": 12000,
                "current_battery": 100,
                "battery_remaining": 95,
                "drop_rate_comm": 0,
            }
        )
        return position_origin

    monkeypatch.setattr(experiment_runner, "_append_message_rows", _append_message_rows)

    config = RunConfig.from_dict(
        {
            "study_name": "attack_trace_unit",
            "backend": "ardupilot",
            "flight_mode": "STABILIZE",
            "scenario": "nominal",
            "config_profile": "attack_trace_unit",
            "seed": 7,
            "repeat_count": 1,
            "sampling_rate_hz": 10.0,
            "x_schema": "commands_plus_state",
            "input_type": "manual",
            "axis": "composite",
            "profile_type": "pulse",
            "start_after_s": 0.0,
            "duration_s": 0.1,
            "hold_s": 0.0,
            "extras": {
                "ardupilot_tail_s": 0.0,
            },
        }
    )

    exit_code, artifact_dir = experiment_runner.run_capture(
        config,
        start_sitl=False,
        master_uri="tcp:127.0.0.1:5760",
    )

    assert exit_code == 0
    attack_trace_path = artifact_dir / "telemetry" / "attack_trace.csv"
    manifest_path = artifact_dir / "manifest.yaml"
    input_trace_path = artifact_dir / "telemetry" / "input_trace.csv"
    assert attack_trace_path.exists()
    assert manifest_path.exists()
    assert input_trace_path.exists()

    with attack_trace_path.open("r", encoding="utf-8", newline="") as handle:
        attack_rows = list(csv.DictReader(handle))
    assert len(attack_rows) == 1
    assert attack_rows[0]["method_name"] == "family_aware_usdta_v1"
    assert float(attack_rows[0]["delta_roll"]) > 0.0
    assert float(attack_rows[0]["delta_throttle"]) > 0.0

    with input_trace_path.open("r", encoding="utf-8", newline="") as handle:
        input_rows = list(csv.DictReader(handle))
    assert len(input_rows) == 1
    assert float(input_rows[0]["command_roll"]) > 0.20
    assert float(input_rows[0]["command_throttle"]) > 0.20

    manifest = read_yaml(manifest_path)
    assert manifest["runtime_report"]["attack_summary"]["method_name"] == "family_aware_usdta_v1"
    assert manifest["runtime_report"]["attack_summary"]["line_code"] == "AP-DAB"
    assert manifest["runtime_report"]["attack_summary"]["row_count"] == 1
