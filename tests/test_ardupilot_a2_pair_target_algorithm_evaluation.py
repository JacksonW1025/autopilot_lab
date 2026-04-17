from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import linearity_analysis.ardupilot_a2_pair_target_algorithm_evaluation as algorithm_eval
import linearity_analysis.ardupilot_a2_pair_target_readiness as pair_readiness
import linearity_analysis.ardupilot_a2_target_scout as target_scout
from linearity_core.io import read_yaml, write_yaml
from tests.support import build_runs_manifest_row, write_a2_target_run, write_runs_manifest


def _build_ready_artifacts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[Path, Path, Path]:
    monkeypatch.setattr(target_scout, "ACCEPTED_TARGET", 1)
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
            rows.append(
                build_runs_manifest_row(
                    run_index,
                    artifact_dir=run_dir,
                    config_name=f"ardupilot_a2_target_scout_{scenario}_{tier}.yaml",
                )
            )
            run_index += 1
    runs_manifest = tmp_path / "runs.csv"
    write_runs_manifest(runs_manifest, rows)
    studies_root = tmp_path / "studies"
    target_dir = target_scout.run_ardupilot_a2_target_scout(runs_manifest=runs_manifest, output_root=studies_root)
    pair_dir = pair_readiness.run_ardupilot_a2_pair_target_readiness(runs_manifest=runs_manifest, output_root=studies_root)
    return target_dir, pair_dir, runs_manifest


def _rewrite_summary(study_dir: Path, summary_name: str, mutate: Any) -> None:
    summary_path = study_dir / "summary" / summary_name
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    mutate(payload)
    summary_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest_path = study_dir / "manifest.yaml"
    manifest = read_yaml(manifest_path)
    if isinstance(manifest, dict):
        manifest["summary"] = payload
        write_yaml(manifest_path, manifest)


def test_algorithm_evaluation_real_canonical_artifacts(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    target_dir = root / "artifacts/studies/20260417_001924_151397_ardupilot_a2_target_scout"
    pair_dir = root / "artifacts/studies/20260417_001925_356349_ardupilot_a2_pair_target_readiness"
    if not target_dir.exists() or not pair_dir.exists():
        pytest.skip("canonical A2 artifacts are not available")

    study_dir = algorithm_eval.run_ardupilot_a2_pair_target_algorithm_evaluation(
        a2_target_scout_dir=target_dir,
        a2_pair_target_dir=pair_dir,
        output_root=tmp_path / "eval",
    )
    summary = json.loads((study_dir / "summary" / "a2_pair_target_algorithm_evaluation.json").read_text(encoding="utf-8"))

    assert summary["overall_decision"]["offline_ready_for_live_eval_v1"] is True
    assert summary["overall_decision"]["live_eval_required"] is True
    assert summary["overall_decision"]["hard_regression_detected"] is False
    assert summary["overall_decision"]["recommended_next_step"] == "hold_for_live_eval"
    assert (study_dir / "reports" / "a2_pair_target_algorithm_evaluation.md").exists()
    assert (study_dir / "tables" / "scenario_evaluation_matrix.csv").exists()
    assert (study_dir / "tables" / "run_level_reference_alignment.csv").exists()
    assert (study_dir / "tables" / "generated_schedule.csv").exists()


def test_algorithm_evaluation_direction_mismatch_detects_hard_regression(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_dir, pair_dir, runs_manifest = _build_ready_artifacts(tmp_path, monkeypatch)
    study_dir = algorithm_eval.run_ardupilot_a2_pair_target_algorithm_evaluation(
        a2_target_scout_dir=target_dir,
        a2_pair_target_dir=pair_dir,
        runs_manifest=runs_manifest,
        output_root=tmp_path / "eval",
        direction="34_gt_12",
    )
    summary = json.loads((study_dir / "summary" / "a2_pair_target_algorithm_evaluation.json").read_text(encoding="utf-8"))

    assert summary["overall_decision"]["hard_regression_detected"] is True
    assert "pair_readiness_direction_mismatch" in summary["blocking_reasons"]
    assert "algorithm_direction_mismatch" in summary["blocking_reasons"]
    assert summary["overall_decision"]["recommended_next_step"] == "fix_artifact_or_protocol_mismatch"


def test_algorithm_evaluation_target_scout_mismatch_detects_hard_regression(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_dir, pair_dir, runs_manifest = _build_ready_artifacts(tmp_path, monkeypatch)

    def _mutate(payload: dict[str, Any]) -> None:
        payload["overall_decision"]["recommended_mode"] = "STABILIZE"
        payload["overall_decision"]["recommended_next_target"] = "collective_floor_state"

    _rewrite_summary(target_dir, "a2_target_scout.json", _mutate)

    study_dir = algorithm_eval.run_ardupilot_a2_pair_target_algorithm_evaluation(
        a2_target_scout_dir=target_dir,
        a2_pair_target_dir=pair_dir,
        runs_manifest=runs_manifest,
        output_root=tmp_path / "eval",
    )
    summary = json.loads((study_dir / "summary" / "a2_pair_target_algorithm_evaluation.json").read_text(encoding="utf-8"))

    assert summary["overall_decision"]["hard_regression_detected"] is True
    assert "target_scout_recommended_mode_mismatch" in summary["blocking_reasons"]
    assert "target_scout_recommended_target_mismatch" in summary["blocking_reasons"]


def test_algorithm_evaluation_missing_runs_manifest_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_dir, pair_dir, _runs_manifest = _build_ready_artifacts(tmp_path, monkeypatch)
    target_manifest = read_yaml(target_dir / "manifest.yaml")
    pair_manifest = read_yaml(pair_dir / "manifest.yaml")
    target_manifest.pop("runs_manifest", None)
    pair_manifest.pop("runs_manifest", None)
    write_yaml(target_dir / "manifest.yaml", target_manifest)
    write_yaml(pair_dir / "manifest.yaml", pair_manifest)

    with pytest.raises(FileNotFoundError):
        algorithm_eval.run_ardupilot_a2_pair_target_algorithm_evaluation(
            a2_target_scout_dir=target_dir,
            a2_pair_target_dir=pair_dir,
            output_root=tmp_path / "eval",
        )


def test_algorithm_evaluation_parameter_out_of_envelope_detects_hard_regression(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_dir, pair_dir, runs_manifest = _build_ready_artifacts(tmp_path, monkeypatch)
    study_dir = algorithm_eval.run_ardupilot_a2_pair_target_algorithm_evaluation(
        a2_target_scout_dir=target_dir,
        a2_pair_target_dir=pair_dir,
        runs_manifest=runs_manifest,
        output_root=tmp_path / "eval",
        pulse_amplitude=0.20,
    )
    summary = json.loads((study_dir / "summary" / "a2_pair_target_algorithm_evaluation.json").read_text(encoding="utf-8"))

    assert summary["overall_decision"]["hard_regression_detected"] is True
    assert "pulse_amplitude_out_of_envelope" in summary["blocking_reasons"]


def test_algorithm_evaluation_soft_regression_detected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_dir, pair_dir, runs_manifest = _build_ready_artifacts(tmp_path, monkeypatch)

    def _mutate(payload: dict[str, Any]) -> None:
        for result in payload["scenario_results"]:
            result["median_active_pair_rate"] = 1.2
            result["median_pair_specificity"] = 1.2
            result["median_pair_to_collective_ratio"] = 2000.0

    _rewrite_summary(pair_dir, "a2_pair_target_readiness.json", _mutate)

    study_dir = algorithm_eval.run_ardupilot_a2_pair_target_algorithm_evaluation(
        a2_target_scout_dir=target_dir,
        a2_pair_target_dir=pair_dir,
        runs_manifest=runs_manifest,
        output_root=tmp_path / "eval",
    )
    summary = json.loads((study_dir / "summary" / "a2_pair_target_algorithm_evaluation.json").read_text(encoding="utf-8"))

    assert summary["overall_decision"]["hard_regression_detected"] is False
    assert summary["overall_decision"]["soft_regression_detected"] is True
    assert summary["overall_decision"]["recommended_next_step"] == "tighten_algorithm_spec"
    assert any(reason.startswith("soft_regression_") for reason in summary["blocking_reasons"])


def test_algorithm_evaluation_main_writes_study_dir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    target_dir, pair_dir, runs_manifest = _build_ready_artifacts(tmp_path, monkeypatch)
    algorithm_eval.main(
        [
            "--a2-target-scout-dir",
            str(target_dir),
            "--a2-pair-target-dir",
            str(pair_dir),
            "--runs-manifest",
            str(runs_manifest),
            "--output-root",
            str(tmp_path / "eval"),
        ]
    )
    captured = capsys.readouterr()
    study_dir = Path(captured.out.strip().split("=", maxsplit=1)[1])
    summary = json.loads((study_dir / "summary" / "a2_pair_target_algorithm_evaluation.json").read_text(encoding="utf-8"))

    assert summary["overall_decision"]["offline_ready_for_live_eval_v1"] is True
