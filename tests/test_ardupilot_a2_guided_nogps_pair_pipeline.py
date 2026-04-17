from __future__ import annotations

import json
from pathlib import Path

import pytest

import linearity_analysis.ardupilot_a2_guided_nogps_pair_pipeline as pair_pipeline
import linearity_analysis.ardupilot_a2_pair_target_readiness as pair_readiness
import linearity_analysis.ardupilot_a2_target_scout as target_scout
from linearity_core.io import write_json
from tests.support import build_runs_manifest_row, write_a2_target_run, write_runs_manifest


def _build_matrix_dir(
    base_dir: Path,
    *,
    baseline_pwm: tuple[int, int, int, int],
    active_pwm: tuple[int, int, int, int],
) -> Path:
    matrix_dir = base_dir / "matrix"
    rows: list[dict[str, object]] = []
    run_index = 0
    for scenario in ("nominal", "throttle_biased"):
        for tier in ("micro", "probe", "confirm"):
            run_dir = base_dir / "raw" / f"{scenario}_{tier}"
            write_a2_target_run(
                run_dir,
                run_id=f"{scenario}_{tier}",
                scenario=scenario,
                tier=tier,
                baseline_pwm=baseline_pwm,
                active_pwm=active_pwm,
            )
            rows.append(
                build_runs_manifest_row(
                    run_index,
                    artifact_dir=run_dir,
                    config_name=f"ardupilot_a2_guided_nogps_pair_pipeline_{scenario}_{tier}.yaml",
                )
            )
            run_index += 1
    write_runs_manifest(matrix_dir / "runs.csv", rows)
    return matrix_dir


def _parse_key_values(output: str) -> dict[str, str]:
    payload: dict[str, str] = {}
    for line in output.strip().splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", maxsplit=1)
        payload[key.strip()] = value.strip()
    return payload


def _fake_study_dir(base_dir: Path, name: str) -> Path:
    study_dir = base_dir / name
    study_dir.mkdir(parents=True, exist_ok=True)
    return study_dir


def _lower_a2_acceptance_thresholds(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(target_scout, "ACCEPTED_TARGET", 1)
    monkeypatch.setattr(pair_readiness, "ACCEPTED_TARGET", 1)


def test_pipeline_skip_capture_success_refreshes_decision_layer(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    matrix_dir = _build_matrix_dir(
        tmp_path,
        baseline_pwm=(1588, 1588, 1588, 1588),
        active_pwm=(1550, 1550, 1350, 1350),
    )
    source_dirs = {
        "formal_v2_anchor_deep_dive": _fake_study_dir(tmp_path / "sources", "anchor"),
        "formal_v2_in_depth_analysis": _fake_study_dir(tmp_path / "sources", "in_depth"),
        "px4_a1_roll_pitch_targeted_reproduction": _fake_study_dir(tmp_path / "sources", "a1"),
    }
    _lower_a2_acceptance_thresholds(monkeypatch)
    monkeypatch.setattr(pair_pipeline, "latest_study_dir_by_name", lambda study_name: source_dirs.get(study_name))
    captured_kwargs: dict[str, Path] = {}

    def _fake_decision_refresh(**kwargs):
        captured_kwargs.update(kwargs)
        output_dir = Path(kwargs["output_dir"]).expanduser().resolve()
        (output_dir / "summary").mkdir(parents=True, exist_ok=True)
        write_json(
            output_dir / "summary" / "next_phase_decision_layer.json",
            {"overall_recommendation": {"default_entry": "A2"}},
        )
        return output_dir

    monkeypatch.setattr(pair_pipeline, "run_formal_v2_next_phase_decision_layer", _fake_decision_refresh)

    pair_pipeline.main(
        [
            "--skip-smoke",
            "--skip-capture",
            "--matrix-dir",
            str(matrix_dir),
            "--output-root",
            str(tmp_path / "studies"),
        ]
    )
    payload = _parse_key_values(capsys.readouterr().out)

    assert payload["guided_nogps_smoke_passed"] == "skipped"
    assert payload["smoke_matrix_dir"] == ""
    assert payload["matrix_dir"] == str(matrix_dir.resolve())
    assert Path(payload["a2_target_scout_dir"]).exists()
    assert Path(payload["a2_pair_target_dir"]).exists()
    assert Path(payload["decision_layer_dir"]).exists()
    assert captured_kwargs["anchor_deep_dive_dir"] == source_dirs["formal_v2_anchor_deep_dive"].resolve()
    assert captured_kwargs["in_depth_analysis_dir"] == source_dirs["formal_v2_in_depth_analysis"].resolve()
    assert captured_kwargs["a1_targeted_reproduction_dir"] == source_dirs["px4_a1_roll_pitch_targeted_reproduction"].resolve()
    assert captured_kwargs["a2_pair_target_dir"] == Path(payload["a2_pair_target_dir"]).resolve()
    assert Path(payload["decision_layer_dir"]).resolve().parent == (tmp_path / "studies").resolve()


def test_pipeline_smoke_failure_stops_before_target_scout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
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

    captured_kwargs: dict[str, object] = {}

    def _fake_run_matrix(*args, **kwargs):
        captured_kwargs.update(kwargs)
        return smoke_matrix_dir, [
            {
                "artifact_dir": str(run_dir),
            }
        ]

    monkeypatch.setattr(pair_pipeline, "run_matrix", _fake_run_matrix)
    monkeypatch.setattr(
        pair_pipeline,
        "run_ardupilot_a2_target_scout",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("target scout should not run")),
    )

    with pytest.raises(RuntimeError, match="GUIDED_NOGPS smoke gate failed"):
        pair_pipeline.run_ardupilot_a2_guided_nogps_pair_pipeline(skip_decision_layer=True)
    assert captured_kwargs["enable_visualization"] is False


def test_pipeline_target_scout_gate_failure_stops_before_pair_readiness(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    matrix_dir = _build_matrix_dir(
        tmp_path,
        baseline_pwm=(1100, 1100, 1100, 1100),
        active_pwm=(1000, 1000, 1000, 1000),
    )
    _lower_a2_acceptance_thresholds(monkeypatch)
    monkeypatch.setattr(
        pair_pipeline,
        "run_ardupilot_a2_pair_target_readiness",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("pair readiness should not run")),
    )

    with pytest.raises(RuntimeError, match="A2 target scout gate failed"):
        pair_pipeline.run_ardupilot_a2_guided_nogps_pair_pipeline(
            skip_smoke=True,
            skip_capture=True,
            matrix_dir=matrix_dir,
            skip_decision_layer=True,
            output_root=tmp_path / "studies",
        )


def test_pipeline_pair_readiness_gate_failure_stops_before_decision_layer(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    matrix_dir = _build_matrix_dir(
        tmp_path,
        baseline_pwm=(1588, 1588, 1588, 1588),
        active_pwm=(1550, 1550, 1350, 1350),
    )
    source_dirs = {
        "formal_v2_anchor_deep_dive": _fake_study_dir(tmp_path / "sources", "anchor"),
        "formal_v2_in_depth_analysis": _fake_study_dir(tmp_path / "sources", "in_depth"),
        "px4_a1_roll_pitch_targeted_reproduction": _fake_study_dir(tmp_path / "sources", "a1"),
    }
    _lower_a2_acceptance_thresholds(monkeypatch)
    monkeypatch.setattr(pair_pipeline, "latest_study_dir_by_name", lambda study_name: source_dirs.get(study_name))

    def _fake_pair_target_readiness(*args, **kwargs):
        study_dir = tmp_path / "studies" / "bad_pair_target"
        (study_dir / "summary").mkdir(parents=True, exist_ok=True)
        write_json(
            study_dir / "summary" / "a2_pair_target_readiness.json",
            {
                "overall_decision": {
                    "ready_for_pair_attack_v1": False,
                    "recommended_path": "iterate_pair_target_protocol_only",
                    "dominant_direction": "mixed",
                    "scenario_status": {
                        "nominal": False,
                        "throttle_biased": True,
                    },
                }
            },
        )
        return study_dir

    monkeypatch.setattr(pair_pipeline, "run_ardupilot_a2_pair_target_readiness", _fake_pair_target_readiness)
    monkeypatch.setattr(
        pair_pipeline,
        "run_formal_v2_next_phase_decision_layer",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("decision layer should not run")),
    )

    with pytest.raises(RuntimeError, match="A2 pair readiness gate failed"):
        pair_pipeline.run_ardupilot_a2_guided_nogps_pair_pipeline(
            skip_smoke=True,
            skip_capture=True,
            matrix_dir=matrix_dir,
            output_root=tmp_path / "studies",
        )


def test_pipeline_skip_decision_layer_stops_after_pair_readiness(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    matrix_dir = _build_matrix_dir(
        tmp_path,
        baseline_pwm=(1588, 1588, 1588, 1588),
        active_pwm=(1550, 1550, 1350, 1350),
    )
    _lower_a2_acceptance_thresholds(monkeypatch)
    monkeypatch.setattr(
        pair_pipeline,
        "latest_study_dir_by_name",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("decision precheck should be skipped")),
    )

    pair_pipeline.main(
        [
            "--skip-smoke",
            "--skip-capture",
            "--matrix-dir",
            str(matrix_dir),
            "--skip-decision-layer",
            "--output-root",
            str(tmp_path / "studies"),
        ]
    )
    payload = _parse_key_values(capsys.readouterr().out)

    assert payload["guided_nogps_smoke_passed"] == "skipped"
    assert Path(payload["a2_target_scout_dir"]).exists()
    assert Path(payload["a2_pair_target_dir"]).exists()
    assert payload["decision_layer_dir"] == ""
