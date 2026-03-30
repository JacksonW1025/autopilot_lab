from __future__ import annotations

import csv
import math
from pathlib import Path

from fep_core.config import RunConfig, load_run_config
from ardupilot_mavlink_backend import experiment_runner as ardupilot_experiment_runner
from ardupilot_mavlink_backend import matrix_runner as ardupilot_matrix_runner
from ardupilot_mavlink_backend.experiment_runner import METRICS_FIELDNAMES, _append_message_rows
from px4_ros2_backend.metrics import compute_metrics
from px4_ros2_backend import matrix_runner as px4_matrix_runner
from px4_ros2_backend.experiment_runner import _manual_xy_motion_anomaly, _post_run_manual_anomalies


def test_layered_rate_config_resolves_backend_contracts() -> None:
    config = load_run_config(Path("/home/car/autopilot_lab/src/fep_research/config/layered_rate_roll_010.yaml"))
    assert config.input_chain == "rate"
    assert config.resolved_study_layer == "rate_single_loop"
    assert config.mode_under_test_for_backend("px4") == "OFFBOARD_RATE"
    assert config.mode_under_test_for_backend("ardupilot") == "GUIDED_RATE"
    assert "vehicle_angular_velocity" in config.output_contract_for_backend("px4")["signals"]
    assert "vehicle_rates_setpoint" in config.output_contract_for_backend("px4")["signals"]


def test_ardupilot_matrix_runner_writes_repeat_and_session_dir(tmp_path: Path, monkeypatch) -> None:
    config_path = tmp_path / "demo.yaml"
    config_path.write_text(
        "\n".join(
            [
                "phase: 1",
                "input_chain: rate",
                "axis: roll",
                "profile_type: step",
                "amplitude: 0.1",
                "bias: 0.0",
                "start_after_s: 1.0",
                "duration_s: 1.0",
                "sample_rate_hz: 20.0",
                "hover_thrust: -0.69",
                "hold_s: 1.0",
                "timing_required: false",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(ardupilot_matrix_runner, "ARDUPILOT_MATRIX_ROOT", tmp_path / "matrix")
    monkeypatch.setattr(ardupilot_matrix_runner, "ARDUPILOT_RUNS_ROOT", tmp_path / "ardupilot_runs")
    monkeypatch.setattr(ardupilot_matrix_runner, "PX4_RUNS_ROOT", tmp_path / "px4_runs")

    def fake_run_experiment(*args, **kwargs):
        artifact_dir = tmp_path / "artifacts" / f"run_{len(list((tmp_path / 'artifacts').glob('*'))) if (tmp_path / 'artifacts').exists() else 0}"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        return 0, artifact_dir

    def fake_analysis(*args, **kwargs):
        return tmp_path / "studies" / "dummy"

    monkeypatch.setattr(ardupilot_matrix_runner, "run_experiment", fake_run_experiment)
    monkeypatch.setattr(ardupilot_matrix_runner, "run_study_analysis", fake_analysis)

    matrix_dir, rows = ardupilot_matrix_runner.run_matrix(
        [config_path],
        vehicle="ArduCopter",
        frame="quad",
        skip_sitl=True,
        repeat=2,
    )
    assert matrix_dir.exists()
    assert len(rows) == 2
    assert rows[0]["repeat_index"] == "1"
    assert rows[1]["repeat_index"] == "2"
    assert rows[0]["session_dir"]
    written_rows = list(csv.DictReader((matrix_dir / "runs.csv").open("r", encoding="utf-8")))
    assert len(written_rows) == 2
    assert all(row["session_dir"] for row in written_rows)


def test_px4_matrix_runner_resets_persistent_rootfs_state(tmp_path: Path, monkeypatch) -> None:
    rootfs_dir = tmp_path / "build" / "px4_sitl_default" / "rootfs"
    rootfs_dir.mkdir(parents=True)
    preserved = rootfs_dir / "gz_env.sh"
    preserved.write_text("keep", encoding="utf-8")
    for name in px4_matrix_runner.ROOTFS_STATE_FILES:
        (rootfs_dir / name).write_text("stale", encoding="utf-8")

    monkeypatch.setattr(px4_matrix_runner, "PX4_ROOT", tmp_path)

    px4_matrix_runner._reset_px4_rootfs_state()

    assert preserved.exists()
    for name in px4_matrix_runner.ROOTFS_STATE_FILES:
        assert not (rootfs_dir / name).exists()


def test_ardupilot_run_experiment_uses_start_sitl_function(tmp_path: Path, monkeypatch) -> None:
    config = RunConfig.from_dict(
        {
            "phase": 1,
            "study_layer": "manual_whole_loop",
            "study_role": "primary",
            "oracle_profile": "manual_whole_loop_v1",
            "input_chain": "manual",
            "axis": "roll",
            "profile_type": "step",
            "amplitude": 0.2,
            "bias": 0.0,
            "start_after_s": 1.0,
            "duration_s": 1.0,
            "sample_rate_hz": 10.0,
            "hover_thrust": -0.69,
            "hold_s": 1.0,
            "timing_required": False,
            "ardupilot_arm_takeoff": False,
        }
    )
    telemetry_dir = tmp_path / "telemetry"
    telemetry_dir.mkdir(parents=True)
    fake_paths = {
        "base_dir": tmp_path,
        "telemetry_dir": telemetry_dir,
        "input_trace_path": telemetry_dir / "input_profile.csv",
        "metrics_path": tmp_path / "metrics.csv",
        "manifest_path": tmp_path / "manifest.yaml",
        "notes_path": tmp_path / "notes.md",
    }
    started: list[tuple[str, str, str]] = []

    class _FakeMaster:
        def close(self) -> None:
            return None

    monkeypatch.setattr(ardupilot_experiment_runner, "ensure_run_directories", lambda *args, **kwargs: fake_paths)
    monkeypatch.setattr(ardupilot_experiment_runner, "_snapshot_logs", lambda *args, **kwargs: {})
    monkeypatch.setattr(
        ardupilot_experiment_runner,
        "capture_host_snapshot",
        lambda: {"uptime": "0", "loadavg": "0"},
    )
    monkeypatch.setattr(ardupilot_experiment_runner, "cleanup_residual_processes", lambda: None)
    monkeypatch.setattr(
        ardupilot_experiment_runner,
        "start_sitl_process",
        lambda run_id, vehicle, frame, log_path: started.append((run_id, vehicle, frame)) or object(),
    )
    monkeypatch.setattr(ardupilot_experiment_runner, "connect", lambda *args, **kwargs: _FakeMaster())
    monkeypatch.setattr(ardupilot_experiment_runner, "_wait_for_vehicle_ready", lambda *args, **kwargs: [])
    monkeypatch.setattr(ardupilot_experiment_runner, "_prepare_parameters", lambda *args, **kwargs: ({}, {}, []))
    monkeypatch.setattr(ardupilot_experiment_runner, "_prepare_runtime_arming", lambda *args, **kwargs: [])
    monkeypatch.setattr(ardupilot_experiment_runner, "_arm_vehicle", lambda *args, **kwargs: ["arm_failed"])
    monkeypatch.setattr(ardupilot_experiment_runner, "_land_vehicle", lambda master: None)
    monkeypatch.setattr(ardupilot_experiment_runner, "stop_process", lambda process: None)

    exit_code, _ = ardupilot_experiment_runner.run_experiment(
        config,
        start_sitl=True,
        arm_and_takeoff=False,
        connect_timeout_s=0.1,
    )

    assert exit_code == 1
    assert started
    manifest_text = fake_paths["manifest_path"].read_text(encoding="utf-8")
    assert "arm_failed" in manifest_text
    assert "runtime_error:TypeError" not in manifest_text


def test_scripts_help_text() -> None:
    root = Path("/home/car/autopilot_lab")
    for script_name in ("bootstrap_lab.sh", "ci_minimal.sh", "doctor_lab.sh", "smoke_lab.sh"):
        script_path = root / "scripts" / script_name
        text = script_path.read_text(encoding="utf-8")
        assert "Usage:" in text


def test_px4_manual_motion_accepts_recover_window() -> None:
    config = RunConfig.from_dict(
        {
            "phase": 1,
            "input_chain": "manual",
            "axis": "roll",
            "profile_type": "step",
            "amplitude": 0.2,
            "bias": 0.0,
            "start_after_s": 2.0,
            "duration_s": 2.0,
            "sample_rate_hz": 20.0,
            "hover_thrust": -0.69,
            "hold_s": 4.0,
            "timing_required": False,
            "manual_mode": "flight",
            "manual_motion_min_displacement_m": 0.2,
        }
    )
    recorder_rows = {
        "manual_control_setpoint": [
            {"received_time_ns": 10, "valid": True, "data_source": 2},
            {"received_time_ns": 30, "valid": True, "data_source": 2},
        ],
        "vehicle_control_mode": [
            {"received_time_ns": 10, "flag_control_manual_enabled": True},
        ],
        "vehicle_status": [
            {"received_time_ns": 10, "nav_state": 2},
        ],
        "vehicle_local_position": [
            {"received_time_ns": 13, "xy_valid": True, "x": 0.0, "y": 0.0},
            {"received_time_ns": 18, "xy_valid": True, "x": 0.1, "y": 0.0},
            {"received_time_ns": 28, "xy_valid": True, "x": 0.25, "y": 0.0},
        ],
        "vehicle_attitude": [],
    }
    injector_report = {
        "experiment_start_time_ns": 0,
        "completion_time_ns": 40,
        "command_trace": [
            {"publish_time_ns": 12, "phase": "step_active"},
            {"publish_time_ns": 29, "phase": "recover"},
        ],
    }

    assert _post_run_manual_anomalies(config, recorder_rows, injector_report) == []


def test_px4_manual_motion_accepts_threshold_edge() -> None:
    recorder_rows = {
        "vehicle_local_position": [
            {"received_time_ns": 10, "xy_valid": True, "x": 0.0, "y": 0.0},
            {"received_time_ns": 20, "xy_valid": True, "x": 0.199565, "y": 0.0},
        ]
    }
    assert _manual_xy_motion_anomaly(recorder_rows, 0, 30, 0.20) is None


def test_ardupilot_metrics_fieldnames_include_bin_message_counts() -> None:
    assert "bin_message_counts" in METRICS_FIELDNAMES


def test_ardupilot_append_message_rows_tolerates_empty_fields() -> None:
    class _Message:
        def __init__(self, message_type: str, **kwargs) -> None:
            self._message_type = message_type
            for key, value in kwargs.items():
                setattr(self, key, value)

        def get_type(self) -> str:
            return self._message_type

    class _Master:
        def __init__(self, messages) -> None:
            self._messages = list(messages)

        def recv_match(self, blocking=False):
            if not self._messages:
                return None
            return self._messages.pop(0)

    master = _Master(
        [
            _Message("ATTITUDE", roll=None, pitch=0.1, yaw=0.2, rollspeed=None, pitchspeed=0.3, yawspeed=0.4),
            _Message("LOCAL_POSITION_NED", x=None, y=1.0, z=2.0, vx=None, vy=3.0, vz=4.0),
            _Message("HEARTBEAT", base_mode=None, custom_mode=5, system_status=None),
            _Message(
                "SYS_STATUS",
                voltage_battery=None,
                current_battery=120,
                battery_remaining=None,
                drop_rate_comm=7,
            ),
        ]
    )
    attitude_rows: list[dict[str, object]] = []
    position_rows: list[dict[str, object]] = []
    heartbeat_rows: list[dict[str, object]] = []
    status_rows: list[dict[str, object]] = []

    position_origin = _append_message_rows(master, attitude_rows, position_rows, heartbeat_rows, status_rows)

    assert position_origin is None
    assert len(attitude_rows) == 1
    assert math.isnan(float(attitude_rows[0]["roll"]))
    assert math.isnan(float(attitude_rows[0]["rollspeed"]))
    assert len(position_rows) == 1
    assert math.isnan(float(position_rows[0]["x"]))
    assert math.isnan(float(position_rows[0]["vx"]))
    assert len(heartbeat_rows) == 1
    assert heartbeat_rows[0]["base_mode"] == 0
    assert heartbeat_rows[0]["system_status"] == 0
    assert len(status_rows) == 1
    assert status_rows[0]["voltage_battery"] == 0
    assert status_rows[0]["battery_remaining"] == 0


def test_ardupilot_append_message_rows_projects_global_position() -> None:
    class _Message:
        def __init__(self, message_type: str, **kwargs) -> None:
            self._message_type = message_type
            for key, value in kwargs.items():
                setattr(self, key, value)

        def get_type(self) -> str:
            return self._message_type

    class _Master:
        def __init__(self, messages) -> None:
            self._messages = list(messages)

        def recv_match(self, blocking=False):
            if not self._messages:
                return None
            return self._messages.pop(0)

    master = _Master(
        [
            _Message(
                "GLOBAL_POSITION_INT",
                lat=374221234,
                lon=-1220845678,
                relative_alt=1500,
                vx=25,
                vy=-10,
                vz=5,
            )
        ]
    )
    position_rows: list[dict[str, object]] = []

    position_origin = _append_message_rows(master, [], position_rows, [], [], None)

    assert position_origin == {"lat_deg": 37.4221234, "lon_deg": -122.0845678}
    assert len(position_rows) == 1
    assert abs(float(position_rows[0]["x"])) < 1e-6
    assert abs(float(position_rows[0]["y"])) < 1e-6
    assert float(position_rows[0]["z"]) == -1.5
    assert float(position_rows[0]["vx"]) == 0.25
    assert float(position_rows[0]["vy"]) == -0.1
    assert float(position_rows[0]["vz"]) == 0.05


def test_px4_metrics_ignore_post_window_failsafe() -> None:
    config = RunConfig.from_dict(
        {
            "phase": 1,
            "input_chain": "rate",
            "axis": "roll",
            "profile_type": "step",
            "amplitude": 0.1,
            "bias": 0.0,
            "start_after_s": 1.0,
            "duration_s": 1.0,
            "sample_rate_hz": 20.0,
            "hover_thrust": -0.69,
            "hold_s": 1.0,
            "timing_required": False,
        }
    )
    metrics = compute_metrics(
        config,
        command_trace=[
            {"publish_time_ns": 110, "elapsed_s": 0.0, "profile_value": 0.0},
            {"publish_time_ns": 150, "elapsed_s": 0.2, "profile_value": 0.1},
        ],
        attitude_rows=[],
        angular_velocity_rows=[],
        rate_setpoint_rows=[],
        manual_rows=[],
        local_position_rows=[],
        status_rows=[
            {"received_time_ns": 120, "nav_state": "14", "failsafe": "False", "failure_detector_status": "0"},
            {"received_time_ns": 250, "nav_state": "18", "failsafe": "False", "failure_detector_status": "1"},
        ],
        start_time_ns=100,
        end_time_ns=200,
    )
    assert metrics["failsafe_event"] == 0
