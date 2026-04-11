from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from linearity_core.config import load_study_config
from linearity_core.dataset import build_prepared_sample_table
from linearity_core.io import write_rows_csv, write_yaml
from linearity_core.schemas import SchemaMatrices, build_schema_matrices
from linearity_core.fit import fit_schema_combo
from px4_ros2_backend.experiment_runner import _px4_data_quality
from px4_ros2_backend import ulog_backfill
from tests.support import load_synthetic_config


ROOT = Path(__file__).resolve().parents[1]


class _FakeDataset:
    def __init__(self, name: str, data: dict[str, list[float | int | bool]], multi_id: int = 0) -> None:
        self.name = name
        self.data = data
        self.multi_id = multi_id


class _FakeULog:
    def __init__(self, _path: str, _unused: object) -> None:
        timestamps = [1_000_000 + index * 50_000 for index in range(12)]
        timestamp_samples = [value - 2_000 for value in timestamps]
        self.data_list = [
            _FakeDataset(
                "vehicle_angular_velocity",
                {
                    "timestamp": timestamps,
                    "timestamp_sample": timestamp_samples,
                    "xyz[0]": [0.01 * index for index in range(12)],
                    "xyz[1]": [0.02 * index for index in range(12)],
                    "xyz[2]": [0.03 * index for index in range(12)],
                    "xyz_derivative[0]": [0.001] * 12,
                    "xyz_derivative[1]": [0.002] * 12,
                    "xyz_derivative[2]": [0.003] * 12,
                },
            ),
            _FakeDataset(
                "vehicle_rates_setpoint",
                {
                    "timestamp": timestamps,
                    "roll": [0.05] * 12,
                    "pitch": [0.04] * 12,
                    "yaw": [0.03] * 12,
                    "thrust_body[0]": [0.0] * 12,
                    "thrust_body[1]": [0.0] * 12,
                    "thrust_body[2]": [-0.7] * 12,
                    "reset_integral": [False] * 12,
                },
            ),
            _FakeDataset(
                "rate_ctrl_status",
                {
                    "timestamp": timestamps,
                    "rollspeed_integ": [0.1] * 12,
                    "pitchspeed_integ": [0.2] * 12,
                    "yawspeed_integ": [0.3] * 12,
                    "wheel_rate_integ": [0.0] * 12,
                },
            ),
            _FakeDataset(
                "control_allocator_status",
                {
                    "timestamp": timestamps,
                    "torque_setpoint_achieved": [True] * 12,
                    "thrust_setpoint_achieved": [True] * 12,
                    "unallocated_torque[0]": [0.0] * 12,
                    "unallocated_torque[1]": [0.0] * 12,
                    "unallocated_torque[2]": [0.0] * 12,
                    "unallocated_thrust[0]": [0.0] * 12,
                    "unallocated_thrust[1]": [0.0] * 12,
                    "unallocated_thrust[2]": [0.0] * 12,
                    "handled_motor_failure_mask": [0] * 12,
                    **{f"actuator_saturation[{index}]": [0] * 12 for index in range(16)},
                },
            ),
            _FakeDataset(
                "actuator_motors",
                {
                    "timestamp": timestamps,
                    "timestamp_sample": timestamp_samples,
                    "reversible_flags": [0] * 12,
                    **{f"control[{index}]": [0.1 * (index + 1)] * 12 for index in range(12)},
                },
            ),
            _FakeDataset(
                "vehicle_attitude_setpoint",
                {
                    "timestamp": timestamps,
                    "roll_body": [0.05] * 12,
                    "pitch_body": [0.04] * 12,
                    "yaw_body": [0.03] * 12,
                    "yaw_sp_move_rate": [0.02] * 12,
                    "thrust_body[0]": [0.0] * 12,
                    "thrust_body[1]": [0.0] * 12,
                    "thrust_body[2]": [-0.7] * 12,
                    "reset_integral": [False] * 12,
                },
            ),
        ]


class _FakeULogWithReference(_FakeULog):
    def __init__(self, _path: str, _unused: object) -> None:
        super().__init__(_path, _unused)
        reference_timestamps = [1_000_000 + index * 50_000 for index in range(12)]
        self.data_list.insert(
            0,
            _FakeDataset(
                "vehicle_attitude",
                {
                    "timestamp": reference_timestamps,
                },
            ),
        )


def _write_px4_reference_csvs(telemetry_dir: Path, input_trace_path: Path) -> None:
    base_received_offset = 7_000_000
    timestamps = [1_000_000 + index * 50_000 for index in range(12)]
    timestamp_samples = [value - 2_000 for value in timestamps]
    write_rows_csv(
        input_trace_path,
        [
            {
                "publish_time_ns": timestamp * 1000 + base_received_offset,
                "elapsed_s": 0.05 * index,
                "profile_value": 0.1,
                "roll_body": 0.01 * index,
                "pitch_body": 0.02 * index,
                "yaw_body": 0.03 * index,
                "thrust_z": -0.7,
                "command_roll": 0.01 * index,
                "command_pitch": 0.02 * index,
                "command_yaw": 0.03 * index,
                "command_throttle": -0.7,
                "phase": "experiment",
            }
            for index, timestamp in enumerate(timestamps)
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_attitude.csv",
        [
            {
                "received_time_ns": timestamp * 1000 + base_received_offset,
                "timestamp": timestamp,
                "timestamp_sample": timestamp_sample,
                "q_w": 1.0,
                "q_x": 0.0,
                "q_y": 0.0,
                "q_z": 0.0,
                "roll": 0.01 * index,
                "pitch": 0.02 * index,
                "yaw": 0.03 * index,
            }
            for index, (timestamp, timestamp_sample) in enumerate(zip(timestamps, timestamp_samples, strict=False))
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_local_position.csv",
        [
            {
                "received_time_ns": timestamp * 1000 + base_received_offset,
                "timestamp": timestamp,
                "timestamp_sample": timestamp_sample,
                "x": 0.1 * index,
                "y": -0.1 * index,
                "z": -1.0 - 0.01 * index,
                "vx": 0.01 * index,
                "vy": -0.02 * index,
                "vz": -0.03 * index,
                "heading": 0.03 * index,
                "dist_bottom": 1.2,
                "dist_bottom_valid": True,
                "xy_valid": True,
                "z_valid": True,
                "v_xy_valid": True,
                "v_z_valid": True,
            }
            for index, (timestamp, timestamp_sample) in enumerate(zip(timestamps, timestamp_samples, strict=False))
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_status.csv",
        [
            {
                "received_time_ns": timestamp * 1000 + base_received_offset,
                "timestamp": timestamp,
                "arming_state": 2,
                "nav_state": 14,
                "nav_state_user_intention": 14,
                "failsafe": 0,
                "failsafe_defer_state": 0,
                "failure_detector_status": 0,
                "pre_flight_checks_pass": 1,
                "gcs_connection_lost": 0,
                "latest_arming_reason": 0,
                "latest_disarming_reason": 0,
                "vehicle_type": 2,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_control_mode.csv",
        [
            {
                "received_time_ns": timestamp * 1000 + base_received_offset,
                "timestamp": timestamp,
                "flag_armed": True,
                "flag_control_manual_enabled": True,
                "flag_control_auto_enabled": False,
                "flag_control_offboard_enabled": False,
                "flag_control_position_enabled": True,
                "flag_control_velocity_enabled": False,
                "flag_control_altitude_enabled": True,
                "flag_control_acceleration_enabled": False,
                "flag_control_attitude_enabled": True,
                "flag_control_rates_enabled": True,
                "source_id": 0,
            }
            for timestamp in timestamps
        ],
    )


def _write_px4_reference_epoch_csvs(telemetry_dir: Path, input_trace_path: Path) -> None:
    received_base_ns = 1_775_555_670_000_000_000
    ros_timestamps_us = [1_775_555_669_000_000 + index * 50_000 for index in range(12)]
    input_timestamps_ns = [received_base_ns + index * 50_000_000 for index in range(12)]
    write_rows_csv(
        input_trace_path,
        [
            {
                "publish_time_ns": timestamp_ns,
                "elapsed_s": 0.05 * index,
                "profile_value": 0.1,
                "roll_body": 0.01 * index,
                "pitch_body": 0.02 * index,
                "yaw_body": 0.03 * index,
                "thrust_z": -0.7,
                "command_roll": 0.01 * index,
                "command_pitch": 0.02 * index,
                "command_yaw": 0.03 * index,
                "command_throttle": -0.7,
                "phase": "experiment",
            }
            for index, timestamp_ns in enumerate(input_timestamps_ns)
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_attitude.csv",
        [
            {
                "received_time_ns": input_timestamps_ns[index],
                "timestamp": ros_timestamp_us,
                "timestamp_sample": ros_timestamp_us - 2_000,
                "q_w": 1.0,
                "q_x": 0.0,
                "q_y": 0.0,
                "q_z": 0.0,
                "roll": 0.01 * index,
                "pitch": 0.02 * index,
                "yaw": 0.03 * index,
            }
            for index, ros_timestamp_us in enumerate(ros_timestamps_us)
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_local_position.csv",
        [
            {
                "received_time_ns": input_timestamps_ns[index],
                "timestamp": ros_timestamp_us - 10_000,
                "timestamp_sample": ros_timestamp_us - 12_000,
                "x": 0.1 * index,
                "y": -0.1 * index,
                "z": -1.0 - 0.01 * index,
                "vx": 0.01 * index,
                "vy": -0.02 * index,
                "vz": -0.03 * index,
                "heading": 0.03 * index,
                "dist_bottom": 1.2,
                "dist_bottom_valid": True,
                "xy_valid": True,
                "z_valid": True,
                "v_xy_valid": True,
                "v_z_valid": True,
            }
            for index, ros_timestamp_us in enumerate(ros_timestamps_us)
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_status.csv",
        [
            {
                "received_time_ns": input_timestamps_ns[index],
                "timestamp": ros_timestamp_us - 20_000,
                "arming_state": 2,
                "nav_state": 14,
                "nav_state_user_intention": 14,
                "failsafe": 0,
                "failsafe_defer_state": 0,
                "failure_detector_status": 0,
                "pre_flight_checks_pass": 1,
                "gcs_connection_lost": 0,
                "latest_arming_reason": 0,
                "latest_disarming_reason": 0,
                "vehicle_type": 2,
            }
            for index, ros_timestamp_us in enumerate(ros_timestamps_us)
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_control_mode.csv",
        [
            {
                "received_time_ns": input_timestamps_ns[index],
                "timestamp": ros_timestamps_us[index],
                "flag_armed": True,
                "flag_control_manual_enabled": True,
                "flag_control_auto_enabled": False,
                "flag_control_offboard_enabled": False,
                "flag_control_position_enabled": True,
                "flag_control_velocity_enabled": False,
                "flag_control_altitude_enabled": True,
                "flag_control_acceleration_enabled": False,
                "flag_control_attitude_enabled": True,
                "flag_control_rates_enabled": True,
                "source_id": 0,
            }
            for index in range(12)
        ],
    )


def _write_px4_acceptance_fixture(
    telemetry_dir: Path,
    input_trace_path: Path,
    *,
    phases: list[str],
    experiment_started: bool,
    completion_reason: str,
    nonzero_active_count: int | None = None,
    failsafe_from_index: int | None = None,
) -> dict[str, object]:
    base_received_offset = 7_000_000
    timestamps = [1_000_000 + index * 50_000 for index in range(len(phases))]
    timestamp_samples = [value - 2_000 for value in timestamps]
    active_indices = [
        index
        for index, phase in enumerate(phases)
        if phase.endswith("_active") or "_active_" in phase or phase == "experiment"
    ]
    if nonzero_active_count is None:
        nonzero_active_count = len(active_indices)
    active_nonzero_indices = set(active_indices[: max(0, nonzero_active_count)])

    write_rows_csv(
        input_trace_path,
        [
            {
                "publish_time_ns": timestamp * 1000 + base_received_offset,
                "elapsed_s": 0.05 * index,
                "profile_value": 0.2 if index in active_nonzero_indices else 0.0,
                "roll_body": 0.2 if index in active_nonzero_indices else 0.0,
                "pitch_body": 0.0,
                "yaw_body": 0.0,
                "thrust_z": -0.7 if index in active_nonzero_indices else 0.0,
                "command_roll": 0.2 if index in active_nonzero_indices else 0.0,
                "command_pitch": 0.0,
                "command_yaw": 0.0,
                "command_throttle": -0.7 if index in active_nonzero_indices else 0.0,
                "phase": phase,
            }
            for index, (timestamp, phase) in enumerate(zip(timestamps, phases, strict=False))
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_attitude.csv",
        [
            {
                "received_time_ns": timestamp * 1000 + base_received_offset,
                "timestamp": timestamp,
                "timestamp_sample": timestamp_sample,
                "q_w": 1.0,
                "q_x": 0.0,
                "q_y": 0.0,
                "q_z": 0.0,
                "roll": 0.01 * index,
                "pitch": 0.0,
                "yaw": 0.0,
            }
            for index, (timestamp, timestamp_sample) in enumerate(zip(timestamps, timestamp_samples, strict=False))
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_angular_velocity.csv",
        [
            {
                "received_time_ns": timestamp * 1000 + base_received_offset,
                "timestamp": timestamp,
                "timestamp_sample": timestamp_sample,
                "xyz_x": 0.01 * index,
                "xyz_y": 0.0,
                "xyz_z": 0.0,
                "xyz_derivative_x": 0.001,
                "xyz_derivative_y": 0.0,
                "xyz_derivative_z": 0.0,
            }
            for index, (timestamp, timestamp_sample) in enumerate(zip(timestamps, timestamp_samples, strict=False))
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_local_position.csv",
        [
            {
                "received_time_ns": timestamp * 1000 + base_received_offset,
                "timestamp": timestamp,
                "timestamp_sample": timestamp_sample,
                "x": 0.1 * index,
                "y": 0.0,
                "z": -1.0,
                "vx": 0.0,
                "vy": 0.0,
                "vz": 0.0,
                "heading": 0.0,
                "dist_bottom": 1.2,
                "dist_bottom_valid": True,
                "xy_valid": True,
                "z_valid": True,
                "v_xy_valid": True,
                "v_z_valid": True,
            }
            for index, (timestamp, timestamp_sample) in enumerate(zip(timestamps, timestamp_samples, strict=False))
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_status.csv",
        [
            {
                "received_time_ns": timestamp * 1000 + base_received_offset,
                "timestamp": timestamp,
                "arming_state": 2,
                "nav_state": 14,
                "nav_state_user_intention": 14,
                "failsafe": 1 if failsafe_from_index is not None and index >= failsafe_from_index else 0,
                "failsafe_defer_state": 0,
                "failure_detector_status": 0,
                "pre_flight_checks_pass": 1,
                "gcs_connection_lost": 0,
                "latest_arming_reason": 0,
                "latest_disarming_reason": 0,
                "vehicle_type": 2,
            }
            for index, timestamp in enumerate(timestamps)
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_control_mode.csv",
        [
            {
                "received_time_ns": timestamp * 1000 + base_received_offset,
                "timestamp": timestamp,
                "flag_armed": True,
                "flag_control_manual_enabled": True,
                "flag_control_auto_enabled": False,
                "flag_control_offboard_enabled": False,
                "flag_control_position_enabled": True,
                "flag_control_velocity_enabled": False,
                "flag_control_altitude_enabled": True,
                "flag_control_acceleration_enabled": False,
                "flag_control_attitude_enabled": True,
                "flag_control_rates_enabled": True,
                "source_id": 0,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "actuator_motors.csv",
        [
            {
                "received_time_ns": timestamp * 1000 + base_received_offset,
                "timestamp": timestamp,
                "timestamp_sample": timestamp_sample,
                "motor_1": 0.2,
                "motor_2": 0.2,
                "motor_3": 0.2,
                "motor_4": 0.2,
            }
            for timestamp, timestamp_sample in zip(timestamps, timestamp_samples, strict=False)
        ],
    )
    return {
        "experiment_start_time_ns": timestamps[0] * 1000 + base_received_offset if experiment_started else None,
        "completion_reason": completion_reason,
        "anomalies": ["vehicle_status_failsafe"] if failsafe_from_index is not None else [],
    }


def _acceptance_test_config():
    config = load_study_config(ROOT / "configs/studies/px4_real_nominal_broad_ablation_analysis.yaml")
    config.sampling_rate_hz = 8.0
    config.duration_s = 1.0
    return config


def test_px4_ulog_backfill_recovers_missing_topics(tmp_path: Path, monkeypatch) -> None:
    telemetry_dir = tmp_path / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    input_trace_path = telemetry_dir / "input_trace.csv"
    _write_px4_reference_csvs(telemetry_dir, input_trace_path)
    ulog_path = tmp_path / "capture.ulg"
    ulog_path.touch()
    monkeypatch.setattr(ulog_backfill, "ULog", _FakeULog)

    summary = ulog_backfill.backfill_px4_ulog_topics(telemetry_dir, ulog_path=ulog_path)

    assert summary["timebase_reference_topic"] == "vehicle_attitude"
    assert summary["offset_ns"] == 7_000_000
    assert summary["topics"]["vehicle_angular_velocity"]["source"] == "ulog_backfill"
    assert summary["topics"]["actuator_motors"]["row_count"] == 12
    actuator_rows = ulog_backfill.read_rows_csv(telemetry_dir / "actuator_motors.csv")
    assert len(actuator_rows) == 12
    assert actuator_rows[0]["motor_1"] == "0.1"
    angular_velocity_rows = ulog_backfill.read_rows_csv(telemetry_dir / "vehicle_angular_velocity.csv")
    assert angular_velocity_rows[0]["received_time_ns"] == str(1_000_000 * 1000 + 7_000_000)


def test_px4_ulog_backfill_uses_reference_topic_alignment_for_epoch_ros_timestamps(tmp_path: Path, monkeypatch) -> None:
    telemetry_dir = tmp_path / "telemetry_epoch"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    input_trace_path = telemetry_dir / "input_trace.csv"
    _write_px4_reference_epoch_csvs(telemetry_dir, input_trace_path)
    ulog_path = tmp_path / "capture_epoch.ulg"
    ulog_path.touch()
    monkeypatch.setattr(ulog_backfill, "ULog", _FakeULogWithReference)

    summary = ulog_backfill.backfill_px4_ulog_topics(telemetry_dir, ulog_path=ulog_path)

    assert summary["timebase_reference_topic"] == "vehicle_attitude"
    assert int(summary["offset_ns"]) > 1_000_000_000_000_000_000
    angular_velocity_rows = ulog_backfill.read_rows_csv(telemetry_dir / "vehicle_angular_velocity.csv")
    assert len(angular_velocity_rows) == 12
    received_time_ns = int(angular_velocity_rows[0]["received_time_ns"])
    assert received_time_ns > 1_000_000_000_000_000_000
    assert abs(received_time_ns - 1_775_555_670_000_000_000) < 20_000_000


def test_px4_dataset_actuator_response_available_after_backfill(tmp_path: Path, monkeypatch) -> None:
    run_dir = tmp_path / "raw" / "px4" / "test_run"
    telemetry_dir = run_dir / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    input_trace_path = telemetry_dir / "input_trace.csv"
    _write_px4_reference_csvs(telemetry_dir, input_trace_path)
    ulog_path = tmp_path / "capture.ulg"
    ulog_path.touch()
    monkeypatch.setattr(ulog_backfill, "ULog", _FakeULog)
    backfill_summary = ulog_backfill.backfill_px4_ulog_topics(telemetry_dir, ulog_path=ulog_path)
    write_yaml(
        run_dir / "manifest.yaml",
        {
            "run_id": "test_run",
            "backend": "px4",
            "status": "completed",
            "flight_mode": "POSCTL",
            "scenario": "nominal",
            "config_profile": "px4_test",
            "seed": 1,
            "parameter_snapshot_after": {},
            "study_config": {"reporting": {"max_alignment_error_ms": 150}},
            "data_quality": {},
            "telemetry_backfill": backfill_summary,
            "px4_log_path": str(ulog_path),
        },
    )
    config = load_study_config(ROOT / "configs/studies/px4_real_nominal_broad_ablation_analysis.yaml")
    table, inventory = build_prepared_sample_table([run_dir], config)
    matrices = build_schema_matrices(table, config, "commands_plus_state", "actuator_response")
    full_augmented_matrices = build_schema_matrices(table, config, "full_augmented", "actuator_response")
    assert inventory["data_quality"]["actuator_response_available_ratio"] == 1.0
    assert inventory["data_quality"]["tracking_error_available_ratio"] == 1.0
    assert matrices.response_names == ["actuator_1", "actuator_2", "actuator_3", "actuator_4"]
    assert int(np.sum(matrices.valid_mask)) >= 10
    assert full_augmented_matrices.response_names == ["actuator_1", "actuator_2", "actuator_3", "actuator_4"]
    assert all(name not in {"actuator_1", "actuator_2", "actuator_3", "actuator_4"} for name in full_augmented_matrices.feature_names)
    assert full_augmented_matrices.schema_metadata["dropped_response_leakage_features"] == [
        "actuator_1",
        "actuator_2",
        "actuator_3",
        "actuator_4",
    ]


def test_px4_data_quality_uses_backfilled_topic_counts(tmp_path: Path, monkeypatch) -> None:
    run_dir = tmp_path / "raw" / "px4" / "test_run_quality"
    telemetry_dir = run_dir / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    input_trace_path = telemetry_dir / "input_trace.csv"
    _write_px4_reference_csvs(telemetry_dir, input_trace_path)
    ulog_path = tmp_path / "capture_quality.ulg"
    ulog_path.touch()
    monkeypatch.setattr(ulog_backfill, "ULog", _FakeULog)
    ulog_backfill.backfill_px4_ulog_topics(telemetry_dir, ulog_path=ulog_path)

    config = load_study_config(ROOT / "configs/studies/px4_real_nominal_broad_ablation_analysis.yaml")
    data_quality = _px4_data_quality(
        {
            "telemetry_dir": telemetry_dir,
            "input_trace_path": input_trace_path,
        },
        {
            "message_counts": {
                "vehicle_attitude": 12,
                "vehicle_angular_velocity": 0,
                "vehicle_local_position": 12,
                "vehicle_status": 12,
                "vehicle_control_mode": 12,
                "actuator_motors": 0,
            }
        },
        ulog_backfill.read_rows_csv(input_trace_path),
        config,
    )

    assert data_quality["topic_presence"]["missing_topics"] == []
    assert data_quality["topic_presence"]["required_topic_counts"]["actuator_motors"] == 12
    assert data_quality["topic_presence"]["ros_message_counts"]["actuator_motors"] == 0
    assert data_quality["prediction_constructibility"]["actuator_response_ratio_estimate"] == 1.0
    assert "accepted" in data_quality["acceptance"]


def test_px4_acceptance_marks_authoritative_fixture_as_accepted(tmp_path: Path) -> None:
    telemetry_dir = tmp_path / "accepted" / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    input_trace_path = telemetry_dir / "input_trace.csv"
    injector_report = _write_px4_acceptance_fixture(
        telemetry_dir,
        input_trace_path,
        phases=["broad_active"] * 12,
        experiment_started=True,
        completion_reason="disarmed_after_land",
    )
    config = _acceptance_test_config()
    data_quality = _px4_data_quality(
        {
            "telemetry_dir": telemetry_dir,
            "input_trace_path": input_trace_path,
        },
        {"message_counts": {"vehicle_attitude": 12, "vehicle_angular_velocity": 12, "vehicle_local_position": 12, "vehicle_status": 12, "vehicle_control_mode": 12, "actuator_motors": 12}},
        ulog_backfill.read_rows_csv(input_trace_path),
        config,
        injector_report,
        "completed",
    )

    acceptance = data_quality["acceptance"]
    assert acceptance["accepted"] is True
    assert acceptance["active_phase_present"] is True
    assert acceptance["active_nonzero_command_samples"] == 12
    assert acceptance["rejection_reasons"] == []


def test_px4_acceptance_rejects_when_experiment_never_reaches_active_phase(tmp_path: Path) -> None:
    telemetry_dir = tmp_path / "rejected_no_active" / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    input_trace_path = telemetry_dir / "input_trace.csv"
    injector_report = _write_px4_acceptance_fixture(
        telemetry_dir,
        input_trace_path,
        phases=["takeoff_position_hold"] * 12,
        experiment_started=False,
        completion_reason="disarmed_before_experiment",
        nonzero_active_count=0,
    )
    config = _acceptance_test_config()
    data_quality = _px4_data_quality(
        {
            "telemetry_dir": telemetry_dir,
            "input_trace_path": input_trace_path,
        },
        {"message_counts": {"vehicle_attitude": 12, "vehicle_angular_velocity": 12, "vehicle_local_position": 12, "vehicle_status": 12, "vehicle_control_mode": 12, "actuator_motors": 12}},
        ulog_backfill.read_rows_csv(input_trace_path),
        config,
        injector_report,
        "completed",
    )

    acceptance = data_quality["acceptance"]
    assert acceptance["accepted"] is False
    assert "experiment_not_started" in acceptance["rejection_reasons"]
    assert "active_phase_missing" in acceptance["rejection_reasons"]
    assert "insufficient_active_nonzero_command_samples" in acceptance["rejection_reasons"]


def test_px4_acceptance_rejects_when_no_active_nonzero_commands_exist(tmp_path: Path) -> None:
    telemetry_dir = tmp_path / "rejected_zero_active" / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    input_trace_path = telemetry_dir / "input_trace.csv"
    injector_report = _write_px4_acceptance_fixture(
        telemetry_dir,
        input_trace_path,
        phases=["takeoff_position_hold"] * 12,
        experiment_started=False,
        completion_reason="disarmed_before_or_during_mode_switch",
        nonzero_active_count=0,
    )
    config = _acceptance_test_config()
    data_quality = _px4_data_quality(
        {
            "telemetry_dir": telemetry_dir,
            "input_trace_path": input_trace_path,
        },
        {"message_counts": {"vehicle_attitude": 12, "vehicle_angular_velocity": 12, "vehicle_local_position": 12, "vehicle_status": 12, "vehicle_control_mode": 12, "actuator_motors": 12}},
        ulog_backfill.read_rows_csv(input_trace_path),
        config,
        injector_report,
        "completed",
    )

    acceptance = data_quality["acceptance"]
    assert acceptance["accepted"] is False
    assert acceptance["active_nonzero_command_samples"] == 0
    assert "active_phase_missing" in acceptance["rejection_reasons"]
    assert "insufficient_active_nonzero_command_samples" in acceptance["rejection_reasons"]


def test_px4_acceptance_rejects_failsafe_truncated_run(tmp_path: Path) -> None:
    telemetry_dir = tmp_path / "rejected_failsafe" / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    input_trace_path = telemetry_dir / "input_trace.csv"
    injector_report = _write_px4_acceptance_fixture(
        telemetry_dir,
        input_trace_path,
        phases=["sweep_active"] * 6 + ["recover"] * 6,
        experiment_started=True,
        completion_reason="land_timeout",
        nonzero_active_count=6,
        failsafe_from_index=6,
    )
    config = _acceptance_test_config()
    data_quality = _px4_data_quality(
        {
            "telemetry_dir": telemetry_dir,
            "input_trace_path": input_trace_path,
        },
        {"message_counts": {"vehicle_attitude": 12, "vehicle_angular_velocity": 12, "vehicle_local_position": 12, "vehicle_status": 12, "vehicle_control_mode": 12, "actuator_motors": 12}},
        ulog_backfill.read_rows_csv(input_trace_path),
        config,
        injector_report,
        "completed",
    )

    acceptance = data_quality["acceptance"]
    assert acceptance["accepted"] is False
    assert acceptance["failsafe_during_experiment"] is True
    assert "failsafe_during_experiment" in acceptance["rejection_reasons"]
    assert "experiment_truncated_before_expected_active_samples" in acceptance["rejection_reasons"]


def test_px4_acceptance_rejects_single_pulse_throttle_shape(tmp_path: Path) -> None:
    telemetry_dir = tmp_path / "single_pulse" / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    input_trace_path = telemetry_dir / "input_trace.csv"
    phases = ["pulse_active"] * 6 + ["recover"] * 114
    injector_report = _write_px4_acceptance_fixture(
        telemetry_dir,
        input_trace_path,
        phases=phases,
        experiment_started=True,
        completion_reason="disarmed_after_land",
        nonzero_active_count=6,
    )
    config = _acceptance_test_config()
    config.sampling_rate_hz = 20.0
    config.duration_s = 6.0
    data_quality = _px4_data_quality(
        {
            "telemetry_dir": telemetry_dir,
            "input_trace_path": input_trace_path,
        },
        {"message_counts": {"vehicle_attitude": 120, "vehicle_angular_velocity": 120, "vehicle_local_position": 120, "vehicle_status": 120, "vehicle_control_mode": 120, "actuator_motors": 120}},
        ulog_backfill.read_rows_csv(input_trace_path),
        config,
        injector_report,
        "completed",
    )

    acceptance = data_quality["acceptance"]
    assert acceptance["accepted"] is False
    assert acceptance["active_nonzero_command_samples"] == 6
    assert "insufficient_active_nonzero_command_samples" in acceptance["rejection_reasons"]


def test_px4_acceptance_accepts_pulse_train_throttle_shape(tmp_path: Path) -> None:
    telemetry_dir = tmp_path / "pulse_train" / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    input_trace_path = telemetry_dir / "input_trace.csv"
    phases = ["pulse_active"] * 35 + ["pulse_gap"] * 85
    injector_report = _write_px4_acceptance_fixture(
        telemetry_dir,
        input_trace_path,
        phases=phases,
        experiment_started=True,
        completion_reason="disarmed_after_land",
        nonzero_active_count=35,
    )
    config = _acceptance_test_config()
    config.sampling_rate_hz = 20.0
    config.duration_s = 6.0
    data_quality = _px4_data_quality(
        {
            "telemetry_dir": telemetry_dir,
            "input_trace_path": input_trace_path,
        },
        {"message_counts": {"vehicle_attitude": 120, "vehicle_angular_velocity": 120, "vehicle_local_position": 120, "vehicle_status": 120, "vehicle_control_mode": 120, "actuator_motors": 120}},
        ulog_backfill.read_rows_csv(input_trace_path),
        config,
        injector_report,
        "completed",
    )

    acceptance = data_quality["acceptance"]
    assert acceptance["accepted"] is True
    assert acceptance["active_nonzero_command_samples"] == 35
    assert acceptance["rejection_reasons"] == []


def test_px4_acceptance_accepts_alternating_pulse_train_active_phases(tmp_path: Path) -> None:
    telemetry_dir = tmp_path / "alternating_pulse_train" / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    input_trace_path = telemetry_dir / "input_trace.csv"
    alternating = []
    for index in range(35):
        alternating.append("alternating_pulse_active_pos" if index % 2 == 0 else "alternating_pulse_active_neg")
    phases = alternating + ["pulse_gap"] * 85
    injector_report = _write_px4_acceptance_fixture(
        telemetry_dir,
        input_trace_path,
        phases=phases,
        experiment_started=True,
        completion_reason="disarmed_after_land",
        nonzero_active_count=35,
    )
    config = _acceptance_test_config()
    config.sampling_rate_hz = 20.0
    config.duration_s = 6.0
    data_quality = _px4_data_quality(
        {
            "telemetry_dir": telemetry_dir,
            "input_trace_path": input_trace_path,
        },
        {"message_counts": {"vehicle_attitude": 120, "vehicle_angular_velocity": 120, "vehicle_local_position": 120, "vehicle_status": 120, "vehicle_control_mode": 120, "actuator_motors": 120}},
        ulog_backfill.read_rows_csv(input_trace_path),
        config,
        injector_report,
        "completed",
    )

    acceptance = data_quality["acceptance"]
    assert acceptance["accepted"] is True
    assert acceptance["active_phase_present"] is True
    assert acceptance["active_nonzero_command_samples"] == 35
    assert acceptance["rejection_reasons"] == []


def test_fit_summary_reports_raw_and_effective_conditioning(tmp_path: Path) -> None:
    rng = np.random.default_rng(7)
    sample_count = 32
    position_z = rng.normal(size=sample_count)
    velocity_z = rng.normal(size=sample_count)
    mode_posctl = np.asarray([1.0 if index % 2 == 0 else 0.0 for index in range(sample_count)], dtype=float)
    mode_offboard = 1.0 - mode_posctl
    command_roll = rng.normal(size=sample_count)
    X = np.column_stack(
        [
            command_roll,
            position_z,
            -position_z,
            velocity_z,
            -velocity_z,
            mode_posctl,
            mode_offboard,
        ]
    )
    Y = (0.7 * command_roll + 0.3 * position_z - 0.2 * velocity_z).reshape(-1, 1)
    matrices = SchemaMatrices(
        X=X,
        Y=Y,
        feature_names=[
            "command_roll",
            "position_z",
            "altitude",
            "velocity_z",
            "vertical_speed",
            "mode_posctl",
            "mode_offboard_attitude",
        ],
        response_names=["response"],
        valid_mask=np.ones(sample_count, dtype=bool),
        schema_metadata={},
    )
    config = load_synthetic_config(tmp_path, filename="conditioning_config.json")
    result = fit_schema_combo(
        [f"run_{index // 16}" for index in range(sample_count)],
        ["px4"] * sample_count,
        ["POSCTL" if index % 2 == 0 else "OFFBOARD_ATTITUDE" for index in range(sample_count)],
        ["nominal"] * sample_count,
        matrices,
        config,
        "ols_affine",
    )
    summary = result.summary
    assert math.isinf(summary["raw_condition_number"])
    assert math.isfinite(summary["effective_condition_number"])
    assert "altitude" in summary["conditioning_pruned_features"]
    assert "vertical_speed" in summary["conditioning_pruned_features"]
    assert "mode_offboard_attitude" in summary["conditioning_baseline_drops"]
