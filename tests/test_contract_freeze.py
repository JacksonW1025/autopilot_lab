from __future__ import annotations

from pathlib import Path

import pytest
from pymavlink import mavutil

from ardupilot_mavlink_backend.experiment_runner import _ardupilot_data_quality
from linearity_analysis.contract_audit import run_contract_audit
from linearity_core.config import load_study_config
from linearity_core.dataset import (
    PREPARED_SAMPLE_IDENTITY_COLUMNS,
    build_prepared_sample_table,
    prepared_sample_table_fieldnames,
)
from linearity_core.io import read_yaml, write_rows_csv, write_yaml
from linearity_core.research_contract import apply_manifest_research_contract
from linearity_core.schemas import available_x_schemas, available_y_schemas
from linearity_core.study_artifacts import build_contract_audit_payload, render_contract_audit_markdown
from px4_ros2_backend.experiment_runner import _px4_data_quality
from tests.support import fixture_path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ACCEPTANCE_KEYS = {
    "experiment_started",
    "active_phase_present",
    "expected_active_samples",
    "active_sample_count",
    "active_nonzero_command_samples",
    "failsafe_during_experiment",
    "missing_topics_blocking",
    "accepted",
    "rejection_reasons",
}


def _accepted_throttle_trace(sample_count: int, start_ns: int, period_ns: int) -> list[dict[str, float | int | str]]:
    return [
        {
            "publish_time_ns": start_ns + index * period_ns,
            "elapsed_s": index * (period_ns / 1_000_000_000.0),
            "profile_value": 0.18,
            "roll_body": 0.0,
            "pitch_body": 0.0,
            "yaw_body": 0.0,
            "thrust_z": -0.72,
            "command_roll": 0.0,
            "command_pitch": 0.0,
            "command_yaw": 0.0,
            "command_throttle": 0.18,
            "phase": "pulse_active",
        }
        for index in range(sample_count)
    ]


def _write_px4_contract_run(tmp_path: Path) -> tuple[Path, object]:
    config = load_study_config(ROOT / "configs/studies/px4_diagnostic_posctl_throttle_capture.yaml")
    telemetry_dir = tmp_path / "telemetry"
    paths = {
        "telemetry_dir": telemetry_dir,
        "input_trace_path": telemetry_dir / "input_trace.csv",
    }
    start_ns = 2_000_000_000
    period_ns = int(1_000_000_000 / config.sampling_rate_hz)
    command_trace = _accepted_throttle_trace(35, start_ns, period_ns)
    write_rows_csv(paths["input_trace_path"], command_trace)

    timestamps = [start_ns + index * period_ns for index in range(len(command_trace))]
    write_rows_csv(
        telemetry_dir / "vehicle_attitude.csv",
        [
            {
                "received_time_ns": timestamp,
                "roll": 0.01,
                "pitch": -0.02,
                "yaw": 0.03,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_angular_velocity.csv",
        [
            {
                "received_time_ns": timestamp,
                "xyz_x": 0.10,
                "xyz_y": -0.20,
                "xyz_z": 0.30,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_local_position.csv",
        [
            {
                "received_time_ns": timestamp,
                "x": 0.0,
                "y": 0.0,
                "z": -1.5,
                "vx": 0.0,
                "vy": 0.0,
                "vz": 0.0,
                "heading": 0.03,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_status.csv",
        [
            {
                "received_time_ns": timestamp,
                "failsafe": 0,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "vehicle_control_mode.csv",
        [
            {
                "received_time_ns": timestamp,
                "flag_control_manual_enabled": True,
                "flag_control_attitude_enabled": True,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "actuator_motors.csv",
        [
            {
                "received_time_ns": timestamp,
                "motor_1": 0.20,
                "motor_2": 0.21,
                "motor_3": 0.22,
                "motor_4": 0.23,
            }
            for timestamp in timestamps
        ],
    )

    data_quality = _px4_data_quality(
        paths,
        {"message_counts": {name: len(timestamps) for name in (
            "vehicle_attitude",
            "vehicle_angular_velocity",
            "vehicle_local_position",
            "vehicle_status",
            "vehicle_control_mode",
            "actuator_motors",
        )}},
        command_trace,
        config,
        {
            "experiment_start_time_ns": start_ns,
            "completion_reason": "completed",
            "anomalies": [],
        },
        "completed",
    )
    manifest = apply_manifest_research_contract(
        {
            "kind": "linearity_raw_run",
            "run_id": "px4_contract_run",
            "backend": "px4",
            "status": "completed",
            "study_name": config.study_name,
            "study_config": config.to_dict(),
            "flight_mode": config.mode_under_test_for_backend("px4"),
            "scenario": config.scenario,
            "config_profile": config.config_profile,
            "seed": config.seed,
            "input_type": config.input_type,
            "profile_type": config.profile_type,
            "axis": config.axis,
            "parameter_snapshot_after": {"LINEARITY_GAIN": 1.25},
            "data_quality": data_quality,
        },
        research_tier=config.research_tier,
        acceptance=data_quality["acceptance"],
    )
    write_yaml(tmp_path / "manifest.yaml", manifest)
    return tmp_path, config


def _write_ardupilot_contract_run(tmp_path: Path) -> tuple[Path, object]:
    config = load_study_config(ROOT / "configs/studies/ardupilot_diagnostic_stabilize_throttle_capture.yaml")
    telemetry_dir = tmp_path / "telemetry"
    paths = {
        "telemetry_dir": telemetry_dir,
        "input_trace_path": telemetry_dir / "input_trace.csv",
    }
    start_ns = 3_000_000_000
    period_ns = int(1_000_000_000 / config.sampling_rate_hz)
    command_trace = _accepted_throttle_trace(35, start_ns, period_ns)
    write_rows_csv(paths["input_trace_path"], command_trace)

    timestamps = [start_ns + index * period_ns for index in range(len(command_trace))]
    write_rows_csv(
        telemetry_dir / "attitude.csv",
        [
            {
                "received_time_ns": timestamp,
                "roll": 0.01,
                "pitch": -0.02,
                "yaw": 0.03,
                "rollspeed": 0.10,
                "pitchspeed": -0.20,
                "yawspeed": 0.30,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "local_position.csv",
        [
            {
                "received_time_ns": timestamp,
                "x": 0.0,
                "y": 0.0,
                "z": -1.5,
                "vx": 0.0,
                "vy": 0.0,
                "vz": 0.0,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "heartbeat.csv",
        [
            {
                "received_time_ns": timestamp,
                "system_status": mavutil.mavlink.MAV_STATE_ACTIVE,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "sys_status.csv",
        [
            {
                "received_time_ns": timestamp,
                "voltage_battery": 15.6,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "bin_att.csv",
        [
            {
                "received_time_ns": timestamp,
                "roll": 0.01,
                "pitch": -0.02,
                "yaw": 0.03,
                "des_roll": 0.02,
                "des_pitch": -0.01,
                "des_yaw": 0.04,
                "err_rp": 0.01,
                "err_yaw": 0.01,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "bin_rate.csv",
        [
            {
                "received_time_ns": timestamp,
                "roll_rate": 0.10,
                "pitch_rate": -0.20,
                "yaw_rate": 0.30,
                "des_roll_rate": 0.11,
                "des_pitch_rate": -0.19,
                "des_yaw_rate": 0.31,
                "roll_out": 0.05,
                "pitch_out": 0.04,
                "yaw_out": 0.03,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "bin_motb.csv",
        [
            {
                "received_time_ns": timestamp,
                "th_limit": 0.10,
            }
            for timestamp in timestamps
        ],
    )
    write_rows_csv(
        telemetry_dir / "bin_rcou.csv",
        [
            {
                "received_time_ns": timestamp,
                "c1": 1500,
                "c2": 1510,
                "c3": 1520,
                "c4": 1530,
            }
            for timestamp in timestamps
        ],
    )

    data_quality = _ardupilot_data_quality(
        paths,
        command_trace,
        config,
        {
            "experiment_start_time_ns": start_ns,
            "completion_reason": "profile_completed",
            "anomalies": [],
        },
        "completed",
    )
    manifest = apply_manifest_research_contract(
        {
            "kind": "linearity_raw_run",
            "run_id": "ardupilot_contract_run",
            "backend": "ardupilot",
            "status": "completed",
            "study_name": config.study_name,
            "study_config": config.to_dict(),
            "flight_mode": config.mode_under_test_for_backend("ardupilot"),
            "scenario": config.scenario,
            "config_profile": config.config_profile,
            "seed": config.seed,
            "input_type": config.input_type,
            "profile_type": config.profile_type,
            "axis": config.axis,
            "parameter_snapshot_after": {"LINEARITY_GAIN": 1.25},
            "data_quality": data_quality,
        },
        research_tier=config.research_tier,
        acceptance=data_quality["acceptance"],
    )
    write_yaml(tmp_path / "manifest.yaml", manifest)
    return tmp_path, config


def test_prepared_sample_identity_columns_match_contract() -> None:
    assert PREPARED_SAMPLE_IDENTITY_COLUMNS == [
        "sample_id",
        "run_id",
        "backend",
        "mode",
        "scenario",
        "config_profile",
        "research_tier",
        "research_acceptance",
        "seed",
        "timestamp",
        "logical_step",
    ]


def test_cross_backend_contracts_match_on_acceptance_and_prepared_schema(tmp_path: Path) -> None:
    px4_run_dir, px4_config = _write_px4_contract_run(tmp_path / "px4_run")
    ardupilot_run_dir, ardupilot_config = _write_ardupilot_contract_run(tmp_path / "ardupilot_run")
    px4_manifest = read_yaml(px4_run_dir / "manifest.yaml")
    ardupilot_manifest = read_yaml(ardupilot_run_dir / "manifest.yaml")

    required_manifest_keys = {
        "raw_schema_version",
        "research_tier",
        "research_acceptance",
        "research_rejection_reasons",
        "data_quality",
        "study_config",
    }
    assert required_manifest_keys <= set(px4_manifest.keys())
    assert required_manifest_keys <= set(ardupilot_manifest.keys())
    assert set(px4_manifest["data_quality"]["acceptance"].keys()) == EXPECTED_ACCEPTANCE_KEYS
    assert set(ardupilot_manifest["data_quality"]["acceptance"].keys()) == EXPECTED_ACCEPTANCE_KEYS
    assert px4_manifest["research_acceptance"] == "accepted"
    assert ardupilot_manifest["research_acceptance"] == "accepted"

    assert px4_manifest["study_config"]["x_schema"] == ardupilot_manifest["study_config"]["x_schema"]
    assert px4_manifest["study_config"]["y_schema"] == ardupilot_manifest["study_config"]["y_schema"]
    assert px4_manifest["study_config"]["x_schema"] in available_x_schemas()
    assert px4_manifest["study_config"]["y_schema"] in available_y_schemas()

    table, inventory = build_prepared_sample_table([px4_run_dir, ardupilot_run_dir], px4_config)
    fieldnames = prepared_sample_table_fieldnames(table.rows)
    assert fieldnames[: len(PREPARED_SAMPLE_IDENTITY_COLUMNS)] == PREPARED_SAMPLE_IDENTITY_COLUMNS
    assert inventory["data_quality"]["accepted_run_count"] == 2
    assert "backend_px4" in table.numeric_columns
    assert "backend_ardupilot" in table.numeric_columns
    assert any(name.startswith("mode_") for name in table.numeric_columns)
    assert any(name.startswith("scenario_") for name in table.numeric_columns)
    assert any(name.startswith("config_profile_") for name in table.numeric_columns)
    assert "param_LINEARITY_GAIN" in table.numeric_columns
    assert px4_config.x_schema == ardupilot_config.x_schema
    assert px4_config.y_schema == ardupilot_config.y_schema


def test_contract_audit_payload_and_artifacts(tmp_path: Path) -> None:
    px4_run_dir, _ = _write_px4_contract_run(tmp_path / "px4_run")
    ardupilot_run_dir, _ = _write_ardupilot_contract_run(tmp_path / "ardupilot_run")

    payload = build_contract_audit_payload(px4_run_dir, ardupilot_run_dir)
    assert payload["status"] == "audit_available"
    assert payload["contract_ok"] is True
    assert payload["acceptance_keys"]["exact_match"] is True
    assert payload["prepared_sample_table"]["identity_columns_match"] is True

    markdown = render_contract_audit_markdown(payload)
    assert "Contract Audit" in markdown
    assert "contract_ok: `true`" in markdown

    study_dir = run_contract_audit(px4_run_dir, ardupilot_run_dir, output_root=tmp_path / "studies")
    assert (study_dir / "prepared/sample_table.csv").exists()
    assert (study_dir / "reports/contract_audit.md").exists()
    assert (study_dir / "summary/contract_audit.json").exists()


def test_contract_audit_smoke_with_real_runs_if_available(tmp_path: Path) -> None:
    px4_run_dir = fixture_path("raw", "px4", "accepted_run")
    ardupilot_run_dir = fixture_path("raw", "ardupilot", "accepted_run")
    if px4_run_dir is None or ardupilot_run_dir is None:
        pytest.skip("fixed accepted PX4/ArduPilot fixtures are unavailable")
    assert (px4_run_dir / "manifest.yaml").exists()
    assert (ardupilot_run_dir / "manifest.yaml").exists()

    study_dir = run_contract_audit(px4_run_dir, ardupilot_run_dir, output_root=tmp_path / "studies")
    assert (study_dir / "reports/contract_audit.md").exists()
    assert (study_dir / "summary/contract_audit.json").exists()
