from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

import linearity_analysis.ardupilot_a2_pair_target_readiness as pair_readiness
from linearity_analysis.ardupilot_a2_pair_target_readiness import (
    main,
    run_ardupilot_a2_pair_target_readiness,
)
from linearity_core.io import write_yaml


def _write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _write_target_run(
    run_dir: Path,
    *,
    run_id: str,
    scenario: str,
    tier: str,
    baseline_pwm: tuple[int, int, int, int],
    active_pwm: tuple[int, int, int, int],
) -> None:
    telemetry_dir = run_dir / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
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
    _write_csv(
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
    rcou_rows = []
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
    for received_time_ns, vector in zip(relative_times, pwm_vectors, strict=True):
        rcou_rows.append(
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
        )
    _write_csv(
        telemetry_dir / "bin_rcou.csv",
        rcou_rows,
        fieldnames=["received_time_ns", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"],
    )
    _write_csv(
        telemetry_dir / "bin_att.csv",
        [{"received_time_ns": 4_000_000_000, "roll": 0.0}],
        fieldnames=["received_time_ns", "roll"],
    )
    _write_csv(
        telemetry_dir / "bin_rate.csv",
        [{"received_time_ns": 4_000_000_000, "roll_rate": 0.0}],
        fieldnames=["received_time_ns", "roll_rate"],
    )
    write_yaml(
        run_dir / "manifest.yaml",
        {
            "run_id": run_id,
            "study_name": f"ardupilot_a2_guided_pair_target_{scenario}_{tier}",
            "scenario": scenario,
            "config_profile": f"ardupilot_a2_guided_pair_target_{scenario}_{tier}",
            "status": "completed",
            "research_acceptance": "accepted",
            "research_rejection_reasons": [],
            "anomaly_summary": [],
            "study_config": {
                "scenario": scenario,
                "flight_mode": "GUIDED_NOGPS",
                "reporting": {"max_alignment_error_ms": 150.0},
                "extras": {
                    "amplitude_tier": tier,
                    "readiness_scenario": scenario,
                    "profile_family": "pulse_train",
                },
            },
            "runtime_report": {
                "completion_reason": "profile_completed",
            },
            "data_quality": {
                "acceptance": {
                    "failsafe_during_experiment": False,
                    "accepted": True,
                    "rejection_reasons": [],
                }
            },
            "raw_schema_version": 2,
        },
    )


def _write_runs_manifest(path: Path, rows: list[dict[str, object]]) -> None:
    _write_csv(
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


def test_pair_target_readiness_guided_ready(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(pair_readiness, "ACCEPTED_TARGET", 1)
    rows: list[dict[str, object]] = []
    run_index = 0
    for scenario in ("nominal", "throttle_biased"):
        for tier in ("micro", "probe", "confirm"):
            run_dir = tmp_path / "raw" / f"{scenario}_{tier}"
            _write_target_run(
                run_dir,
                run_id=f"{scenario}_{tier}",
                scenario=scenario,
                tier=tier,
                baseline_pwm=(1588, 1588, 1588, 1588),
                active_pwm=(1550, 1550, 1350, 1350),
            )
            rows.append(
                {
                    "index": run_index,
                    "repeat_index": 0,
                    "config": f"guided_pair_{scenario}_{tier}.yaml",
                    "artifact_dir": str(run_dir),
                    "status": "completed",
                    "exit_code": 0,
                    "session_dir": "",
                    "research_acceptance": "accepted",
                    "accepted_count_for_config": 1,
                }
            )
            run_index += 1
    runs_manifest = tmp_path / "runs.csv"
    _write_runs_manifest(runs_manifest, rows)

    main(["--runs-manifest", str(runs_manifest), "--output-root", str(tmp_path / "studies")])
    captured = capsys.readouterr()
    study_dir = Path(captured.out.strip().split("=", maxsplit=1)[1])
    summary = json.loads((study_dir / "summary" / "a2_pair_target_readiness.json").read_text(encoding="utf-8"))

    assert summary["overall_decision"]["ready_for_pair_attack_v1"] is True
    assert summary["overall_decision"]["recommended_path"] == "start_guided_nogps_pair_attack_v1"
    assert summary["overall_decision"]["dominant_direction"] == "12_gt_34"


def test_pair_target_readiness_guided_collective_only_blocks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pair_readiness, "ACCEPTED_TARGET", 1)
    rows: list[dict[str, object]] = []
    run_index = 0
    for scenario in ("nominal", "throttle_biased"):
        for tier in ("micro", "probe", "confirm"):
            run_dir = tmp_path / "raw" / f"{scenario}_{tier}"
            _write_target_run(
                run_dir,
                run_id=f"{scenario}_{tier}",
                scenario=scenario,
                tier=tier,
                baseline_pwm=(1100, 1100, 1100, 1100),
                active_pwm=(1000, 1000, 1000, 1000),
            )
            rows.append(
                {
                    "index": run_index,
                    "repeat_index": 0,
                    "config": f"guided_collective_{scenario}_{tier}.yaml",
                    "artifact_dir": str(run_dir),
                    "status": "completed",
                    "exit_code": 0,
                    "session_dir": "",
                    "research_acceptance": "accepted",
                    "accepted_count_for_config": 1,
                }
            )
            run_index += 1
    runs_manifest = tmp_path / "runs.csv"
    _write_runs_manifest(runs_manifest, rows)

    study_dir = run_ardupilot_a2_pair_target_readiness(runs_manifest=runs_manifest, output_root=tmp_path / "studies")
    summary = json.loads((study_dir / "summary" / "a2_pair_target_readiness.json").read_text(encoding="utf-8"))

    assert summary["overall_decision"]["ready_for_pair_attack_v1"] is False
    assert summary["overall_decision"]["recommended_path"] == "iterate_pair_target_protocol_only"
    assert any("pair_specificity_below_threshold" in result["blocking_reasons"] for result in summary["scenario_results"])
