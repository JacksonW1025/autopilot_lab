from __future__ import annotations

import json
from pathlib import Path

import pytest

import linearity_analysis.ardupilot_a2_pair_target_readiness as pair_readiness
from linearity_analysis.ardupilot_a2_pair_target_readiness import (
    main,
    run_ardupilot_a2_pair_target_readiness,
)
from tests.support import build_runs_manifest_row, write_a2_target_run, write_runs_manifest


def test_pair_target_readiness_guided_ready(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(pair_readiness, "ACCEPTED_TARGET", 1)
    rows: list[dict[str, object]] = []
    run_index = 0
    for scenario in ("nominal", "throttle_biased"):
        for tier in ("micro", "probe", "confirm"):
            run_dir = tmp_path / "raw" / f"{scenario}_{tier}"
            write_a2_target_run(
                run_dir,
                run_id=f"{scenario}_{tier}",
                scenario=scenario,
                tier=tier,
                baseline_pwm=(1588, 1588, 1588, 1588),
                active_pwm=(1550, 1550, 1350, 1350),
            )
            rows.append(build_runs_manifest_row(run_index, artifact_dir=run_dir, config_name=f"guided_pair_{scenario}_{tier}.yaml"))
            run_index += 1
    runs_manifest = tmp_path / "runs.csv"
    write_runs_manifest(runs_manifest, rows)

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
            write_a2_target_run(
                run_dir,
                run_id=f"{scenario}_{tier}",
                scenario=scenario,
                tier=tier,
                baseline_pwm=(1100, 1100, 1100, 1100),
                active_pwm=(1000, 1000, 1000, 1000),
            )
            rows.append(
                build_runs_manifest_row(run_index, artifact_dir=run_dir, config_name=f"guided_collective_{scenario}_{tier}.yaml")
            )
            run_index += 1
    runs_manifest = tmp_path / "runs.csv"
    write_runs_manifest(runs_manifest, rows)

    study_dir = run_ardupilot_a2_pair_target_readiness(runs_manifest=runs_manifest, output_root=tmp_path / "studies")
    summary = json.loads((study_dir / "summary" / "a2_pair_target_readiness.json").read_text(encoding="utf-8"))

    assert summary["overall_decision"]["ready_for_pair_attack_v1"] is False
    assert summary["overall_decision"]["recommended_path"] == "iterate_pair_target_protocol_only"
    assert any("pair_specificity_below_threshold" in result["blocking_reasons"] for result in summary["scenario_results"])
