from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import linearity_analysis.ardupilot_a2_pair_target_algorithm_evaluation as algorithm_eval
import linearity_analysis.ardupilot_a2_pair_target_live_evaluation as live_eval
import linearity_analysis.ardupilot_a2_pair_target_readiness as pair_readiness
import linearity_analysis.ardupilot_a2_target_scout as target_scout
from linearity_core.io import read_yaml, write_yaml
from tests.support import build_runs_manifest_row, write_a2_target_run, write_runs_manifest


def _parse_key_values(output: str) -> dict[str, str]:
    payload: dict[str, str] = {}
    for line in output.strip().splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", maxsplit=1)
        payload[key.strip()] = value.strip()
    return payload


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
            run_dir = tmp_path / "raw" / f"source_{scenario}_{tier}"
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
    runs_manifest = tmp_path / "source_runs.csv"
    write_runs_manifest(runs_manifest, rows)
    studies_root = tmp_path / "studies"
    target_dir = target_scout.run_ardupilot_a2_target_scout(runs_manifest=runs_manifest, output_root=studies_root)
    pair_dir = pair_readiness.run_ardupilot_a2_pair_target_readiness(runs_manifest=runs_manifest, output_root=studies_root)
    return target_dir, pair_dir, runs_manifest


def _build_live_matrix_dir(
    base_dir: Path,
    *,
    baseline_pwm: tuple[int, int, int, int],
    active_pwm: tuple[int, int, int, int],
    repeats_per_scenario: int = 5,
    tier: str = "probe",
) -> Path:
    matrix_dir = base_dir / "matrix"
    rows: list[dict[str, object]] = []
    run_index = 0
    for scenario in ("nominal", "throttle_biased"):
        for repeat_index in range(1, repeats_per_scenario + 1):
            run_dir = base_dir / "raw" / f"live_{scenario}_{repeat_index}"
            write_a2_target_run(
                run_dir,
                run_id=f"{scenario}_{repeat_index}",
                scenario=scenario,
                tier=tier,
                baseline_pwm=baseline_pwm,
                active_pwm=active_pwm,
                study_name_prefix="ardupilot_a2_pair_target_live_evaluation",
                config_profile_prefix="ardupilot_a2_pair_target_live_evaluation",
            )
            rows.append(
                build_runs_manifest_row(
                    run_index,
                    artifact_dir=run_dir,
                    config_name=f"ardupilot_a2_pair_target_live_evaluation_{scenario}_{tier}.yaml",
                    accepted_count_for_config=repeat_index,
                )
            )
            run_index += 1
    write_runs_manifest(matrix_dir / "runs.csv", rows)
    return matrix_dir


def _build_algorithm_eval_artifact(
    tmp_path: Path,
    *,
    a2_target_scout_dir: Path,
    a2_pair_target_dir: Path,
    runs_manifest: Path,
) -> Path:
    return algorithm_eval.run_ardupilot_a2_pair_target_algorithm_evaluation(
        a2_target_scout_dir=a2_target_scout_dir,
        a2_pair_target_dir=a2_pair_target_dir,
        runs_manifest=runs_manifest,
        output_root=tmp_path / "algorithm_eval",
    )


def _rewrite_summary(study_dir: Path, summary_name: str, mutate: Any) -> None:
    summary_path = study_dir / "summary" / summary_name
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    mutate(payload)
    summary_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest_path = study_dir / "manifest.yaml"
    manifest = read_yaml(manifest_path)
    manifest["summary"] = payload
    write_yaml(manifest_path, manifest)


def test_live_evaluation_skip_capture_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    target_dir, pair_dir, source_runs_manifest = _build_ready_artifacts(tmp_path, monkeypatch)
    algorithm_eval_dir = _build_algorithm_eval_artifact(
        tmp_path,
        a2_target_scout_dir=target_dir,
        a2_pair_target_dir=pair_dir,
        runs_manifest=source_runs_manifest,
    )
    matrix_dir = _build_live_matrix_dir(
        tmp_path / "live_capture",
        baseline_pwm=(1588, 1588, 1588, 1588),
        active_pwm=(1550, 1550, 1350, 1350),
    )

    live_eval.main(
        [
            "--a2-target-scout-dir",
            str(target_dir),
            "--a2-pair-target-dir",
            str(pair_dir),
            "--a2-algorithm-eval-dir",
            str(algorithm_eval_dir),
            "--skip-smoke",
            "--skip-capture",
            "--matrix-dir",
            str(matrix_dir),
            "--output-root",
            str(tmp_path / "live_eval"),
        ]
    )
    payload = _parse_key_values(capsys.readouterr().out)
    study_dir = Path(payload["live_evaluation_dir"])
    summary = json.loads((study_dir / "summary" / "a2_pair_target_live_evaluation.json").read_text(encoding="utf-8"))

    assert payload["guided_nogps_smoke_passed"] == "skipped"
    assert payload["matrix_dir"] == str(matrix_dir.resolve())
    assert payload["live_pair_target_success_v1"] == "true"
    assert summary["overall_decision"]["live_pair_target_success_v1"] is True
    assert summary["overall_decision"]["recommended_next_step"] == "promote_live_artifact_for_review"
    assert (study_dir / "reports" / "a2_pair_target_live_evaluation.md").exists()
    assert (study_dir / "tables" / "scenario_live_matrix.csv").exists()
    assert (study_dir / "tables" / "run_level_live_metrics.csv").exists()
    assert (study_dir / "tables" / "generated_schedule.csv").exists()


def test_live_evaluation_algorithm_eval_preflight_failure_raises(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_dir, pair_dir, source_runs_manifest = _build_ready_artifacts(tmp_path, monkeypatch)
    algorithm_eval_dir = _build_algorithm_eval_artifact(
        tmp_path,
        a2_target_scout_dir=target_dir,
        a2_pair_target_dir=pair_dir,
        runs_manifest=source_runs_manifest,
    )

    def _mutate(payload: dict[str, Any]) -> None:
        payload["overall_decision"]["soft_regression_detected"] = True
        payload["overall_decision"]["recommended_next_step"] = "tighten_algorithm_spec"

    _rewrite_summary(algorithm_eval_dir, "a2_pair_target_algorithm_evaluation.json", _mutate)

    with pytest.raises(RuntimeError, match="A2 live evaluation preflight failed"):
        live_eval.run_ardupilot_a2_pair_target_live_evaluation(
            a2_target_scout_dir=target_dir,
            a2_pair_target_dir=pair_dir,
            a2_algorithm_eval_dir=algorithm_eval_dir,
            skip_smoke=True,
            skip_capture=True,
            matrix_dir=tmp_path / "missing_matrix",
            output_root=tmp_path / "live_eval",
        )


def test_live_evaluation_capture_regression_writes_failure_artifact(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_dir, pair_dir, source_runs_manifest = _build_ready_artifacts(tmp_path, monkeypatch)
    algorithm_eval_dir = _build_algorithm_eval_artifact(
        tmp_path,
        a2_target_scout_dir=target_dir,
        a2_pair_target_dir=pair_dir,
        runs_manifest=source_runs_manifest,
    )
    matrix_dir = _build_live_matrix_dir(
        tmp_path / "live_capture_bad",
        baseline_pwm=(1588, 1588, 1588, 1588),
        active_pwm=(1350, 1350, 1550, 1550),
    )

    result = live_eval.run_ardupilot_a2_pair_target_live_evaluation(
        a2_target_scout_dir=target_dir,
        a2_pair_target_dir=pair_dir,
        a2_algorithm_eval_dir=algorithm_eval_dir,
        skip_smoke=True,
        skip_capture=True,
        matrix_dir=matrix_dir,
        output_root=tmp_path / "live_eval",
    )
    summary = json.loads(
        (Path(result["live_evaluation_dir"]) / "summary" / "a2_pair_target_live_evaluation.json").read_text(
            encoding="utf-8"
        )
    )

    assert result["live_pair_target_success_v1"] is False
    assert summary["overall_decision"]["live_pair_target_success_v1"] is False
    assert summary["overall_decision"]["hard_regression_detected"] is True
    assert summary["overall_decision"]["recommended_next_step"] == "fix_live_protocol_or_capture"
    assert any("scenario_direction_mismatch" in reason for reason in summary["blocking_reasons"])


def test_live_evaluation_smoke_failure_stops_before_capture(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_dir, pair_dir, source_runs_manifest = _build_ready_artifacts(tmp_path, monkeypatch)
    algorithm_eval_dir = _build_algorithm_eval_artifact(
        tmp_path,
        a2_target_scout_dir=target_dir,
        a2_pair_target_dir=pair_dir,
        runs_manifest=source_runs_manifest,
    )
    smoke_matrix_dir = tmp_path / "smoke_matrix"
    run_dir = tmp_path / "raw" / "smoke_blocked"
    write_a2_target_run(
        run_dir,
        run_id="smoke_blocked",
        scenario="nominal",
        tier="probe",
        baseline_pwm=(1588, 1588, 1588, 1588),
        active_pwm=(1550, 1550, 1350, 1350),
        experiment_started=False,
        active_phase_present=False,
        accepted=False,
        rejection_reasons=["mode_entry_failed"],
        failure_reason="mode_entry_failed",
    )

    def _fake_run_matrix(*args, **kwargs):
        return smoke_matrix_dir, [{"artifact_dir": str(run_dir)}]

    monkeypatch.setattr(live_eval, "run_matrix", _fake_run_matrix)

    with pytest.raises(RuntimeError, match="GUIDED_NOGPS smoke gate failed"):
        live_eval.run_ardupilot_a2_pair_target_live_evaluation(
            a2_target_scout_dir=target_dir,
            a2_pair_target_dir=pair_dir,
            a2_algorithm_eval_dir=algorithm_eval_dir,
            output_root=tmp_path / "live_eval",
        )
