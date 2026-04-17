from __future__ import annotations

from pathlib import Path

from pymavlink import mavutil

from ardupilot_mavlink_backend.experiment_runner import _ardupilot_data_quality
from linearity_core.config import load_study_config
from linearity_core.io import write_rows_csv


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


def _write_ardupilot_acceptance_fixture(
    tmp_path: Path,
    *,
    active_nonzero_samples: int,
    experiment_started: bool,
    completion_reason: str = "profile_completed",
    heartbeat_statuses: list[int] | None = None,
):
    config = load_study_config(ROOT / "configs/studies/ardupilot_diagnostic_stabilize_throttle_capture.yaml")
    telemetry_dir = tmp_path / "telemetry"
    paths = {
        "telemetry_dir": telemetry_dir,
        "input_trace_path": telemetry_dir / "input_trace.csv",
    }
    start_ns = 1_000_000_000
    period_ns = int(1_000_000_000 / config.sampling_rate_hz)
    command_trace = [
        {
            "publish_time_ns": start_ns + index * period_ns,
            "elapsed_s": index / config.sampling_rate_hz,
            "profile_value": config.amplitude,
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
        for index in range(active_nonzero_samples)
    ]
    write_rows_csv(paths["input_trace_path"], command_trace)

    sample_count = max(1, active_nonzero_samples)
    statuses = heartbeat_statuses or [mavutil.mavlink.MAV_STATE_ACTIVE] * sample_count
    telemetry_rows = [
        {
            "received_time_ns": start_ns + index * period_ns,
        }
        for index in range(len(statuses))
    ]
    write_rows_csv(
        telemetry_dir / "attitude.csv",
        [
            {
                **row,
                "roll": 0.01,
                "pitch": -0.02,
                "yaw": 0.03,
                "rollspeed": 0.1,
                "pitchspeed": -0.2,
                "yawspeed": 0.3,
            }
            for row in telemetry_rows
        ],
    )
    write_rows_csv(
        telemetry_dir / "local_position.csv",
        [
            {
                **row,
                "x": 0.0,
                "y": 0.0,
                "z": -1.5,
                "vx": 0.0,
                "vy": 0.0,
                "vz": 0.0,
            }
            for row in telemetry_rows
        ],
    )
    write_rows_csv(
        telemetry_dir / "heartbeat.csv",
        [
            {
                **row,
                "system_status": statuses[index],
            }
            for index, row in enumerate(telemetry_rows)
        ],
    )
    write_rows_csv(
        telemetry_dir / "sys_status.csv",
        [
            {
                **row,
                "voltage_battery": 15.6,
            }
            for row in telemetry_rows
        ],
    )

    runtime_report = {
        "experiment_start_time_ns": start_ns if experiment_started else 0,
        "completion_time_ns": start_ns + len(statuses) * period_ns,
        "completion_reason": completion_reason,
        "anomalies": [],
    }
    return paths, command_trace, config, runtime_report


def test_ardupilot_acceptance_marks_valid_pulse_train_run_accepted(tmp_path: Path) -> None:
    paths, command_trace, config, runtime_report = _write_ardupilot_acceptance_fixture(
        tmp_path,
        active_nonzero_samples=35,
        experiment_started=True,
    )

    quality = _ardupilot_data_quality(paths, command_trace, config, runtime_report, "completed")
    acceptance = quality["acceptance"]

    assert set(acceptance.keys()) == EXPECTED_ACCEPTANCE_KEYS
    assert acceptance["accepted"] is True
    assert acceptance["rejection_reasons"] == []
    assert acceptance["expected_active_samples"] == 120
    assert acceptance["active_nonzero_command_samples"] == 35


def test_ardupilot_acceptance_rejects_when_experiment_never_started(tmp_path: Path) -> None:
    paths, command_trace, config, runtime_report = _write_ardupilot_acceptance_fixture(
        tmp_path,
        active_nonzero_samples=35,
        experiment_started=False,
    )

    quality = _ardupilot_data_quality(paths, command_trace, config, runtime_report, "completed")
    acceptance = quality["acceptance"]

    assert acceptance["accepted"] is False
    assert acceptance["rejection_reasons"] == ["experiment_not_started"]


def test_ardupilot_acceptance_rejects_insufficient_nonzero_samples(tmp_path: Path) -> None:
    paths, command_trace, config, runtime_report = _write_ardupilot_acceptance_fixture(
        tmp_path,
        active_nonzero_samples=7,
        experiment_started=True,
    )

    quality = _ardupilot_data_quality(paths, command_trace, config, runtime_report, "completed")
    acceptance = quality["acceptance"]

    assert acceptance["accepted"] is False
    assert acceptance["rejection_reasons"] == ["insufficient_active_nonzero_command_samples"]
    assert acceptance["active_nonzero_command_samples"] == 7


def test_ardupilot_acceptance_rejects_failsafe_truncation(tmp_path: Path) -> None:
    heartbeat_statuses = [mavutil.mavlink.MAV_STATE_ACTIVE] * 34 + [mavutil.mavlink.MAV_STATE_CRITICAL]
    paths, command_trace, config, runtime_report = _write_ardupilot_acceptance_fixture(
        tmp_path,
        active_nonzero_samples=35,
        experiment_started=True,
        completion_reason="failsafe_abort",
        heartbeat_statuses=heartbeat_statuses,
    )

    quality = _ardupilot_data_quality(paths, command_trace, config, runtime_report, "completed")
    acceptance = quality["acceptance"]

    assert acceptance["accepted"] is False
    assert set(acceptance["rejection_reasons"]) == {
        "experiment_truncated_before_expected_active_samples",
        "failsafe_during_experiment",
    }
    assert acceptance["failsafe_during_experiment"] is True


def test_ardupilot_acceptance_accepts_alternating_pulse_train_active_phases(tmp_path: Path) -> None:
    paths, command_trace, config, runtime_report = _write_ardupilot_acceptance_fixture(
        tmp_path,
        active_nonzero_samples=35,
        experiment_started=True,
    )
    alternating_trace = []
    for index, row in enumerate(command_trace):
        alternating_trace.append(
            {
                **row,
                "phase": "alternating_pulse_active_pos" if index % 2 == 0 else "alternating_pulse_active_neg",
            }
        )
    write_rows_csv(paths["input_trace_path"], alternating_trace)

    quality = _ardupilot_data_quality(paths, alternating_trace, config, runtime_report, "completed")
    acceptance = quality["acceptance"]

    assert acceptance["accepted"] is True
    assert acceptance["active_phase_present"] is True
    assert acceptance["active_nonzero_command_samples"] == 35
    assert acceptance["rejection_reasons"] == []


def test_ardupilot_data_quality_normalizes_bin_alignment_and_excludes_heartbeat_from_alignment_flag(
    tmp_path: Path,
) -> None:
    paths, command_trace, config, runtime_report = _write_ardupilot_acceptance_fixture(
        tmp_path,
        active_nonzero_samples=35,
        experiment_started=True,
    )
    telemetry_dir = paths["telemetry_dir"]
    start_ns = 1_000_000_000
    period_ns = int(1_000_000_000 / config.sampling_rate_hz)

    write_rows_csv(
        telemetry_dir / "heartbeat.csv",
        [
            {
                "received_time_ns": start_ns + index * 1_000_000_000,
                "system_status": mavutil.mavlink.MAV_STATE_ACTIVE,
            }
            for index in range(3)
        ],
    )
    for filename, fieldnames, payload in (
        (
            "bin_att.csv",
            ["received_time_ns", "des_roll", "roll", "des_pitch", "pitch", "des_yaw", "yaw", "err_rp", "err_yaw"],
            {
                "des_roll": 0.0,
                "roll": 0.0,
                "des_pitch": 0.0,
                "pitch": 0.0,
                "des_yaw": 0.0,
                "yaw": 0.0,
                "err_rp": 0.0,
                "err_yaw": 0.0,
            },
        ),
        (
            "bin_rate.csv",
            [
                "received_time_ns",
                "des_roll_rate",
                "roll_rate",
                "roll_out",
                "des_pitch_rate",
                "pitch_rate",
                "pitch_out",
                "des_yaw_rate",
                "yaw_rate",
                "yaw_out",
            ],
            {
                "des_roll_rate": 0.0,
                "roll_rate": 0.0,
                "roll_out": 0.0,
                "des_pitch_rate": 0.0,
                "pitch_rate": 0.0,
                "pitch_out": 0.0,
                "des_yaw_rate": 0.0,
                "yaw_rate": 0.0,
                "yaw_out": 0.0,
            },
        ),
        (
            "bin_motb.csv",
            ["received_time_ns", "th_limit"],
            {
                "th_limit": 0.10,
            },
        ),
        (
            "bin_rcou.csv",
            ["received_time_ns", "c1", "c2", "c3", "c4"],
            {
                "c1": 1500,
                "c2": 1500,
                "c3": 1500,
                "c4": 1500,
            },
        ),
    ):
        write_rows_csv(
            telemetry_dir / filename,
            [
                {
                    "received_time_ns": 5_000_000 + index * period_ns,
                    **payload,
                }
                for index in range(35)
            ],
            fieldnames=fieldnames,
        )

    quality = _ardupilot_data_quality(paths, command_trace, config, runtime_report, "completed")

    assert quality["input_alignment_ns"]["bin_rcou"]["p95_ns"] < 150_000_000.0
    assert "bin_rcou" not in quality["quality_flags"]["alignment_p95_exceeded_streams"]
    assert "heartbeat" not in quality["quality_flags"]["alignment_p95_exceeded_streams"]
