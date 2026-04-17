from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from linearity_core.config import StudyConfig, load_study_config
from linearity_core.io import write_yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "tests" / "fixtures"


def synthetic_config_payload(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "study_name": "synthetic_linear_f",
        "backend": "synthetic",
        "flight_mode": "POSCTL",
        "scenario": "nominal",
        "config_profile": "synthetic_linear_f",
        "seed": 7,
        "repeat_count": 1,
        "sampling_rate_hz": 20.0,
        "x_schema": "commands_plus_state",
        "y_schema": "delta_state",
        "model": ["ols_affine"],
        "research_tier": "authoritative_research",
        "pooling_mode": "compare_both",
        "output_semantics": "future_state",
        "history_length": 3,
        "prediction_horizon": 2,
        "prediction_horizon_unit": "steps",
        "run_level_covariates_as_inputs": True,
        "stratify_by": ["backend", "mode"],
        "internal_signals_enabled": True,
        "reporting": {"stability_repeats": 1},
        "sparsity": {
            "threshold": 0.05,
            "ridge_alpha": 0.6,
            "lasso_alpha": 0.04,
            "bootstrap_repeats": 4,
            "stability_selection_threshold": 0.5,
        },
        "synthetic": {"sample_count": 96, "noise_std": 0.02, "sparse_matrix_density": 0.18},
    }
    payload.update(overrides)
    return payload


def write_synthetic_config(tmp_path: Path, filename: str = "synthetic_config.json", **overrides: Any) -> Path:
    path = tmp_path / filename
    path.write_text(json.dumps(synthetic_config_payload(**overrides), ensure_ascii=False), encoding="utf-8")
    return path


def load_synthetic_config(tmp_path: Path, filename: str = "synthetic_config.json", **overrides: Any) -> StudyConfig:
    return load_study_config(write_synthetic_config(tmp_path, filename=filename, **overrides))


def fixture_path(*parts: str) -> Path:
    return FIXTURE_ROOT.joinpath(*parts)


def write_csv_rows(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_a2_target_run(
    run_dir: Path,
    *,
    run_id: str,
    scenario: str,
    tier: str,
    baseline_pwm: tuple[int, int, int, int],
    active_pwm: tuple[int, int, int, int],
    flight_mode: str = "GUIDED_NOGPS",
    accepted: bool = True,
    experiment_started: bool = True,
    active_phase_present: bool = True,
    completion_reason: str = "profile_completed",
    failure_reason: str = "",
    rejection_reasons: list[str] | None = None,
    anomalies: list[str] | None = None,
    study_name_prefix: str = "ardupilot_a2_guided_pair_target",
    config_profile_prefix: str = "ardupilot_a2_guided_pair_target",
) -> None:
    telemetry_dir = run_dir / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    rejection_reasons = list(rejection_reasons or [])
    anomalies = list(anomalies or [])
    baseline_command = 0.55 if scenario == "nominal" else 0.60
    active_command = baseline_command + 0.02
    input_rows = [
        {"publish_time_ns": 1_000_000_000, "command_throttle": baseline_command, "phase": "stabilize"},
        {"publish_time_ns": 1_100_000_000, "command_throttle": baseline_command, "phase": "stabilize"},
        {"publish_time_ns": 1_200_000_000, "command_throttle": baseline_command, "phase": "stabilize"},
        {"publish_time_ns": 1_300_000_000, "command_throttle": active_command, "phase": "pulse_active"},
        {"publish_time_ns": 1_400_000_000, "command_throttle": active_command, "phase": "pulse_active"},
        {"publish_time_ns": 1_500_000_000, "command_throttle": baseline_command, "phase": "pulse_gap"},
        {"publish_time_ns": 1_600_000_000, "command_throttle": baseline_command, "phase": "pulse_gap"},
        {"publish_time_ns": 1_700_000_000, "command_throttle": active_command, "phase": "pulse_active"},
        {"publish_time_ns": 1_800_000_000, "command_throttle": active_command, "phase": "pulse_active"},
        {"publish_time_ns": 1_900_000_000, "command_throttle": baseline_command, "phase": "recover"},
        {"publish_time_ns": 2_000_000_000, "command_throttle": baseline_command, "phase": "recover"},
    ]
    write_csv_rows(
        telemetry_dir / "input_trace.csv",
        [
            {
                "publish_time_ns": row["publish_time_ns"],
                "elapsed_s": (row["publish_time_ns"] - input_rows[0]["publish_time_ns"]) / 1_000_000_000.0,
                "profile_value": 0.0,
                "roll_body": 0.0,
                "pitch_body": 0.0,
                "yaw_body": 0.0,
                "thrust_z": row["command_throttle"],
                "command_roll": 0.0,
                "command_pitch": 0.0,
                "command_yaw": 0.0,
                "command_throttle": row["command_throttle"],
                "phase": row["phase"],
            }
            for row in input_rows
        ],
        fieldnames=[
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
        ],
    )
    relative_times = [
        4_000_000_000,
        4_100_000_000,
        4_200_000_000,
        4_300_000_000,
        4_400_000_000,
        4_500_000_000,
        4_600_000_000,
        4_700_000_000,
        4_800_000_000,
        4_900_000_000,
        5_000_000_000,
    ]
    pwm_vectors = [
        baseline_pwm,
        baseline_pwm,
        baseline_pwm,
        active_pwm,
        active_pwm,
        baseline_pwm,
        baseline_pwm,
        active_pwm,
        active_pwm,
        baseline_pwm,
        baseline_pwm,
    ]
    write_csv_rows(
        telemetry_dir / "bin_rcou.csv",
        [
            {
                "received_time_ns": received_time_ns,
                "c1": vector[0],
                "c2": vector[1],
                "c3": vector[2],
                "c4": vector[3],
                "c5": 0,
                "c6": 0,
                "c7": 0,
                "c8": 0,
            }
            for received_time_ns, vector in zip(relative_times, pwm_vectors, strict=True)
        ],
        fieldnames=["received_time_ns", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"],
    )
    write_csv_rows(
        telemetry_dir / "bin_att.csv",
        [{"received_time_ns": 4_000_000_000, "roll": 0.0}],
        fieldnames=["received_time_ns", "roll"],
    )
    write_csv_rows(
        telemetry_dir / "bin_rate.csv",
        [{"received_time_ns": 4_000_000_000, "roll_rate": 0.0}],
        fieldnames=["received_time_ns", "roll_rate"],
    )
    write_yaml(
        run_dir / "manifest.yaml",
        {
            "run_id": run_id,
            "study_name": f"{study_name_prefix}_{scenario}_{tier}",
            "scenario": scenario,
            "flight_mode": flight_mode,
            "config_profile": f"{config_profile_prefix}_{scenario}_{tier}",
            "status": "completed",
            "research_acceptance": "accepted" if accepted else "rejected",
            "research_rejection_reasons": [] if accepted else rejection_reasons,
            "anomaly_summary": anomalies,
            "failure_reason": failure_reason,
            "study_config": {
                "scenario": scenario,
                "flight_mode": flight_mode,
                "reporting": {"max_alignment_error_ms": 150.0},
                "extras": {
                    "amplitude_tier": tier,
                    "readiness_scenario": scenario,
                    "profile_family": "pulse_train",
                },
            },
            "runtime_report": {
                "completion_reason": completion_reason,
            },
            "data_quality": {
                "acceptance": {
                    "failsafe_during_experiment": False,
                    "accepted": accepted,
                    "experiment_started": experiment_started,
                    "active_phase_present": active_phase_present,
                    "rejection_reasons": [] if accepted else rejection_reasons,
                }
            },
            "raw_schema_version": 2,
        },
    )


def build_runs_manifest_row(
    index: int,
    *,
    artifact_dir: Path,
    config_name: str,
    repeat_index: int = 0,
    status: str = "completed",
    exit_code: int = 0,
    session_dir: str = "",
    research_acceptance: str = "accepted",
    accepted_count_for_config: int = 1,
) -> dict[str, object]:
    return {
        "index": index,
        "repeat_index": repeat_index,
        "config": config_name,
        "artifact_dir": str(artifact_dir),
        "status": status,
        "exit_code": exit_code,
        "session_dir": session_dir,
        "research_acceptance": research_acceptance,
        "accepted_count_for_config": accepted_count_for_config,
    }


def write_runs_manifest(path: Path, rows: list[dict[str, object]]) -> None:
    write_csv_rows(
        path,
        rows,
        fieldnames=[
            "index",
            "repeat_index",
            "config",
            "artifact_dir",
            "status",
            "exit_code",
            "session_dir",
            "research_acceptance",
            "accepted_count_for_config",
        ],
    )
