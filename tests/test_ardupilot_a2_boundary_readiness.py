from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import pytest

from linearity_analysis.ardupilot_a2_boundary_readiness import (
    _build_aligned_samples,
    _compute_run_boundary_metrics,
    main,
    run_ardupilot_a2_boundary_readiness,
)
from linearity_core.io import read_yaml, write_yaml


def _write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _write_boundary_run(
    run_dir: Path,
    *,
    run_id: str,
    scenario: str,
    tier: str,
    flight_mode: str = "STABILIZE",
    accepted: bool = True,
    completion_reason: str = "profile_completed",
    failsafe: bool = False,
    active_command: float = 0.57,
    trigger: bool = True,
    hit_pattern: tuple[int, int, int, int] = (1, 1, 0, 0),
) -> None:
    telemetry_dir = run_dir / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    baseline_command = 0.55 if scenario == "nominal" else 0.60
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
    baseline_pwm = [1120, 1130, 1140, 1150]
    if trigger:
        active_pwm = [1000 if flag else 1060 + 10 * index for index, flag in enumerate(hit_pattern, start=0)]
    else:
        active_pwm = [1080, 1090, 1100, 1110]
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
            "study_name": f"ardupilot_a2_stabilize_boundary_readiness_{scenario}_{tier}",
            "scenario": scenario,
            "config_profile": f"ardupilot_a2_stabilize_boundary_readiness_{scenario}_{tier}",
            "status": "completed",
            "research_acceptance": "accepted" if accepted else "rejected",
            "research_rejection_reasons": [] if accepted else ["insufficient_active_nonzero_command_samples"],
            "anomaly_summary": [],
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
                    "failsafe_during_experiment": failsafe,
                    "accepted": accepted,
                    "rejection_reasons": [] if accepted else ["insufficient_active_nonzero_command_samples"],
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


def test_boundary_metrics_detect_trigger_and_recovery(tmp_path: Path) -> None:
    run_dir = tmp_path / "raw" / "probe"
    _write_boundary_run(run_dir, run_id="probe", scenario="nominal", tier="probe", trigger=True)

    samples = _build_aligned_samples(run_dir, read_yaml(run_dir / "manifest.yaml"))
    metrics = _compute_run_boundary_metrics(samples)

    assert metrics["analysis_status"] == "ok"
    assert metrics["pulse_count_seen"] == 2
    assert metrics["triggered_pulse_count"] == 2
    assert metrics["pulse_trigger_rate"] == pytest.approx(1.0)
    assert metrics["floor_hit_rate"] == pytest.approx(1.0)
    assert metrics["baseline_false_trigger_rate"] == pytest.approx(0.0)
    assert metrics["median_hit_latency_ms"] == pytest.approx(0.0)
    assert metrics["recovery_rate"] == pytest.approx(1.0)
    assert metrics["hit_pattern_consistency"] == pytest.approx(1.0)


def test_boundary_metrics_detect_micro_non_trigger(tmp_path: Path) -> None:
    run_dir = tmp_path / "raw" / "micro"
    _write_boundary_run(run_dir, run_id="micro", scenario="nominal", tier="micro", trigger=False, active_command=0.56)

    samples = _build_aligned_samples(run_dir, read_yaml(run_dir / "manifest.yaml"))
    metrics = _compute_run_boundary_metrics(samples)

    assert metrics["analysis_status"] == "ok"
    assert metrics["pulse_count_seen"] == 2
    assert metrics["triggered_pulse_count"] == 0
    assert metrics["pulse_trigger_rate"] == pytest.approx(0.0)
    assert metrics["floor_hit_rate"] == pytest.approx(0.0)
    assert metrics["baseline_false_trigger_rate"] == pytest.approx(0.0)
    assert math.isnan(metrics["median_hit_latency_ms"])
    assert math.isnan(metrics["hit_pattern_consistency"])


def test_boundary_readiness_cli_smoke_writes_expected_outputs(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    raw_root = tmp_path / "raw"
    rows: list[dict[str, object]] = []
    run_index = 1
    trigger_by_tier = {"micro": False, "probe": True, "confirm": True}
    active_command_by_tier = {"micro": 0.56, "probe": 0.57, "confirm": 0.59}
    for scenario in ("nominal", "throttle_biased"):
        for tier in ("micro", "probe", "confirm"):
            for repeat in range(1, 6):
                run_dir = raw_root / f"{scenario}_{tier}_{repeat}"
                _write_boundary_run(
                    run_dir,
                    run_id=f"{scenario}_{tier}_{repeat}",
                    scenario=scenario,
                    tier=tier,
                    trigger=trigger_by_tier[tier],
                    active_command=active_command_by_tier[tier],
                )
                rows.append(
                    {
                        "index": run_index,
                        "repeat_index": repeat,
                        "config": f"ardupilot_a2_stabilize_boundary_readiness_{scenario}_{tier}.yaml",
                        "artifact_dir": str(run_dir),
                        "status": "completed",
                        "exit_code": 0,
                        "session_dir": str(tmp_path / f"session_{run_index}"),
                        "research_acceptance": "accepted",
                        "accepted_count_for_config": repeat,
                    }
                )
                run_index += 1
    runs_manifest = tmp_path / "runs.csv"
    _write_runs_manifest(runs_manifest, rows)

    main(
        [
            "--runs-manifest",
            str(runs_manifest),
            "--output-root",
            str(tmp_path / "studies"),
        ]
    )
    captured = capsys.readouterr()
    study_dir = Path(captured.out.strip().split("=", 1)[1])

    assert (study_dir / "summary" / "a2_boundary_readiness.json").exists()
    assert (study_dir / "reports" / "a2_boundary_readiness.md").exists()
    assert (study_dir / "tables" / "run_level_boundary_effects.csv").exists()
    assert (study_dir / "tables" / "config_threshold_matrix.csv").exists()

    summary = json.loads((study_dir / "summary" / "a2_boundary_readiness.json").read_text(encoding="utf-8"))
    assert summary["overall_decision"]["ready_for_binary_attack_v1"] is True
    assert summary["overall_decision"]["recommended_path"] == "start_ardupilot_a2_binary_attack_v1"
    assert summary["study_scope"]["mode_scope"] == ["STABILIZE"]


def test_boundary_readiness_scopes_to_present_scenarios(tmp_path: Path) -> None:
    raw_root = tmp_path / "raw"
    rows: list[dict[str, object]] = []
    run_index = 1
    trigger_by_tier = {"micro": False, "probe": True, "confirm": True}
    active_command_by_tier = {"micro": 0.56, "probe": 0.57, "confirm": 0.59}
    for tier in ("micro", "probe", "confirm"):
        for repeat in range(1, 6):
            run_dir = raw_root / f"nominal_{tier}_{repeat}"
            _write_boundary_run(
                run_dir,
                run_id=f"nominal_{tier}_{repeat}",
                scenario="nominal",
                tier=tier,
                trigger=trigger_by_tier[tier],
                active_command=active_command_by_tier[tier],
            )
            rows.append(
                {
                    "index": run_index,
                    "repeat_index": repeat,
                    "config": f"ardupilot_a2_stabilize_boundary_readiness_nominal_{tier}.yaml",
                    "artifact_dir": str(run_dir),
                    "status": "completed",
                    "exit_code": 0,
                    "session_dir": str(tmp_path / f"session_{run_index}"),
                    "research_acceptance": "accepted",
                    "accepted_count_for_config": repeat,
                }
            )
            run_index += 1
    runs_manifest = tmp_path / "runs.csv"
    _write_runs_manifest(runs_manifest, rows)

    study_dir = run_ardupilot_a2_boundary_readiness(
        runs_manifest=runs_manifest,
        output_root=tmp_path / "studies",
    )
    summary = json.loads((study_dir / "summary" / "a2_boundary_readiness.json").read_text(encoding="utf-8"))

    assert summary["study_scope"]["scenario_scope"] == ["nominal"]
    assert summary["study_scope"]["mode_scope"] == ["STABILIZE"]
    assert [item["scenario"] for item in summary["config_results"]] == ["nominal"]


def test_boundary_readiness_scopes_guided_nogps_mode(tmp_path: Path) -> None:
    raw_root = tmp_path / "raw"
    rows: list[dict[str, object]] = []
    run_index = 1
    for tier, trigger, active_command in (("micro", False, 0.56), ("probe", True, 0.57), ("confirm", True, 0.59)):
        for repeat in range(1, 6):
            run_dir = raw_root / f"nominal_{tier}_{repeat}"
            _write_boundary_run(
                run_dir,
                run_id=f"nominal_{tier}_{repeat}",
                scenario="nominal",
                tier=tier,
                flight_mode="GUIDED_NOGPS",
                trigger=trigger,
                active_command=active_command,
            )
            rows.append(
                {
                    "index": run_index,
                    "repeat_index": repeat,
                    "config": f"ardupilot_a2_stabilize_boundary_readiness_nominal_{tier}.yaml",
                    "artifact_dir": str(run_dir),
                    "status": "completed",
                    "exit_code": 0,
                    "session_dir": str(tmp_path / f"session_{run_index}"),
                    "research_acceptance": "accepted",
                    "accepted_count_for_config": repeat,
                }
            )
            run_index += 1
    runs_manifest = tmp_path / "runs.csv"
    _write_runs_manifest(runs_manifest, rows)

    study_dir = run_ardupilot_a2_boundary_readiness(
        runs_manifest=runs_manifest,
        output_root=tmp_path / "studies",
    )
    summary = json.loads((study_dir / "summary" / "a2_boundary_readiness.json").read_text(encoding="utf-8"))

    assert summary["study_scope"]["mode_scope"] == ["GUIDED_NOGPS"]
