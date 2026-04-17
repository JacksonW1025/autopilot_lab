from __future__ import annotations

import json
from pathlib import Path

import pytest

import linearity_analysis.ardupilot_a2_target_scout as target_scout
from linearity_analysis.ardupilot_a2_readiness import _build_aligned_samples
from linearity_analysis.ardupilot_a2_target_scout import (
    _compute_run_target_metrics,
    main,
    run_ardupilot_a2_target_scout,
)
from linearity_core.io import read_yaml
from tests.support import build_runs_manifest_row, write_a2_target_run, write_runs_manifest


def test_target_metrics_detect_pair_split_candidate(tmp_path: Path) -> None:
    run_dir = tmp_path / "raw" / "guided_pair"
    write_a2_target_run(
        run_dir,
        run_id="guided_pair",
        scenario="nominal",
        tier="probe",
        flight_mode="GUIDED_NOGPS",
        baseline_pwm=(1588, 1588, 1588, 1588),
        active_pwm=(1550, 1550, 1350, 1350),
    )

    samples = _build_aligned_samples(run_dir, read_yaml(run_dir / "manifest.yaml"))
    metrics = _compute_run_target_metrics(samples)

    assert metrics["analysis_status"] == "ok"
    assert metrics["collective_floor_specificity"] == pytest.approx(0.0)
    assert metrics["active_pair_split_rate"] == pytest.approx(1.0)
    assert metrics["baseline_pair_split_rate"] == pytest.approx(0.0)
    assert metrics["pair_split_specificity"] == pytest.approx(1.0)
    assert metrics["pair_split_sign_consistency"] == pytest.approx(1.0)
    assert metrics["pair_split_direction"] == "12_gt_34"


def test_target_scout_guided_recommends_pair_target(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(target_scout, "ACCEPTED_TARGET", 1)
    runs_rows: list[dict[str, object]] = []
    run_index = 0
    for scenario in ("nominal", "throttle_biased"):
        for tier in ("micro", "probe", "confirm"):
            run_dir = tmp_path / "raw" / f"{scenario}_{tier}"
            write_a2_target_run(
                run_dir,
                run_id=f"{scenario}_{tier}",
                scenario=scenario,
                tier=tier,
                flight_mode="GUIDED_NOGPS",
                baseline_pwm=(1588, 1588, 1588, 1588),
                active_pwm=(1550, 1550, 1350, 1350),
            )
            runs_rows.append(
                build_runs_manifest_row(run_index, artifact_dir=run_dir, config_name=f"ardupilot_a2_target_scout_{scenario}_{tier}.yaml")
            )
            run_index += 1
    runs_manifest = tmp_path / "runs.csv"
    write_runs_manifest(runs_manifest, runs_rows)

    main(["--runs-manifest", str(runs_manifest), "--output-root", str(tmp_path / "studies")])
    captured = capsys.readouterr()
    study_dir = Path(captured.out.strip().split("=", maxsplit=1)[1])

    assert (study_dir / "summary" / "a2_target_scout.json").exists()
    assert (study_dir / "reports" / "a2_target_scout.md").exists()
    assert (study_dir / "tables" / "run_level_target_scout.csv").exists()
    assert (study_dir / "tables" / "scenario_target_matrix.csv").exists()

    summary = json.loads((study_dir / "summary" / "a2_target_scout.json").read_text(encoding="utf-8"))
    assert summary["overall_decision"]["recommended_next_target"] == "pair_imbalance_12_vs_34"
    assert summary["overall_decision"]["recommended_next_step"] == "guided_nogps_pair_target_readiness"
    assert summary["overall_decision"]["recommended_mode"] == "GUIDED_NOGPS"
    assert {result["recommended_target"] for result in summary["scenario_results"]} == {"pair_imbalance_12_vs_34"}


def test_target_scout_stabilize_collective_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(target_scout, "ACCEPTED_TARGET", 1)
    runs_rows: list[dict[str, object]] = []
    run_index = 0
    for scenario in ("nominal", "throttle_biased"):
        for tier in ("micro", "probe", "confirm"):
            run_dir = tmp_path / "raw" / f"{scenario}_{tier}"
            write_a2_target_run(
                run_dir,
                run_id=f"{scenario}_{tier}",
                scenario=scenario,
                tier=tier,
                flight_mode="STABILIZE",
                baseline_pwm=(1100, 1100, 1100, 1100),
                active_pwm=(1000, 1000, 1000, 1000),
            )
            runs_rows.append(
                build_runs_manifest_row(run_index, artifact_dir=run_dir, config_name=f"ardupilot_a2_target_scout_{scenario}_{tier}.yaml")
            )
            run_index += 1
    runs_manifest = tmp_path / "runs.csv"
    write_runs_manifest(runs_manifest, runs_rows)

    study_dir = run_ardupilot_a2_target_scout(runs_manifest=runs_manifest, output_root=tmp_path / "studies")
    summary = json.loads((study_dir / "summary" / "a2_target_scout.json").read_text(encoding="utf-8"))

    assert summary["overall_decision"]["recommended_next_target"] == "none"
    assert summary["overall_decision"]["recommended_next_step"] == "no_target_signal_identified"
    assert summary["overall_decision"]["recommended_mode"] == "none"
    assert {result["recommended_target"] for result in summary["scenario_results"]} == {"collective_floor_state"}
