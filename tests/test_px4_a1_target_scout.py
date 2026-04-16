from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from linearity_analysis.px4_a1_target_scout import (
    DEFAULT_BASELINE_STUDY,
    DEFAULT_DIAGNOSTIC_STUDY,
    run_px4_a1_target_scout,
)


def _write_matrix_csv(path: Path, feature_names: list[str], response_names: list[str], values: list[list[float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["feature", *response_names])
        for feature_name, row in zip(feature_names, values, strict=True):
            writer.writerow([feature_name, *row])


def _write_scenario_generalization(path: Path, *, scenario_consistency: float, subgroup_r2: dict[str, float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": "ok",
        "study_name": path.parent.parent.name,
        "entries": [
            {
                "x_schema": "full_augmented",
                "y_schema": "next_raw_state",
                "pooling_mode": "stratified",
                "model_name": "ols_affine",
                "support": "supported",
                "median_test_r2": 0.99,
                "effective_condition_number": 1000.0,
                "coefficient_stability": 0.9,
                "scenario_consistency": scenario_consistency,
                "scenario_subgroup_metrics": {key: {"r2": value} for key, value in subgroup_r2.items()},
                "scenario_subgroup_r2": subgroup_r2,
                "generalization_status": "generalized_supported",
                "high_local_scenarios": list(subgroup_r2.keys()),
                "metrics_path": str(path.parent.parent / "fits" / "full_augmented__next_raw_state__stratified" / "ols_affine" / "metrics.json"),
            }
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_a1_study(tmp_path: Path, name: str, matrix_values: list[list[float]], *, scenario_consistency: float) -> Path:
    study_dir = tmp_path / name
    feature_names = [
        "command_roll",
        "command_pitch",
        "roll",
        "pitch",
        "roll__lag_1",
        "pitch__lag_1",
        "position_x",
        "position_x__lag_1",
        "mode_offboard_attitude",
        "mode_posctl",
    ]
    response_names = [
        "future_state_roll",
        "future_state_pitch",
        "future_state_position_x",
    ]
    _write_matrix_csv(
        study_dir / "fits" / "full_augmented__next_raw_state__stratified" / "ols_affine" / "matrix_f.csv",
        feature_names,
        response_names,
        matrix_values,
    )
    _write_scenario_generalization(
        study_dir / "summary" / "scenario_generalization.json",
        scenario_consistency=scenario_consistency,
        subgroup_r2={"dynamic": 0.97, "nominal": 0.96, "throttle_biased": 0.965},
    )
    return study_dir


def test_px4_a1_target_scout_selects_attitude_family_on_synthetic_studies(tmp_path: Path) -> None:
    baseline = _write_a1_study(
        tmp_path,
        "baseline",
        [
            [0.10, 0.02, 0.55],
            [0.05, 0.10, 0.05],
            [2.00, 0.03, 0.04],
            [0.01, 1.90, 0.02],
            [-1.10, 0.00, 0.00],
            [0.00, -1.00, 0.00],
            [0.00, 0.00, 0.35],
            [0.00, 0.00, -0.10],
            [0.00, 0.00, 0.01],
            [0.00, 0.00, 0.01],
        ],
        scenario_consistency=0.98,
    )
    diagnostic = _write_a1_study(
        tmp_path,
        "diagnostic",
        [
            [0.08, 0.03, 0.45],
            [0.04, 0.08, 0.06],
            [1.90, 0.02, 0.03],
            [0.01, 1.80, 0.01],
            [-0.95, 0.00, 0.00],
            [0.00, -0.92, 0.00],
            [0.00, 0.00, 0.30],
            [0.00, 0.00, -0.08],
            [0.00, 0.00, 0.01],
            [0.00, 0.00, 0.01],
        ],
        scenario_consistency=0.99,
    )

    study_dir = run_px4_a1_target_scout(
        baseline_study=baseline,
        diagnostic_study=diagnostic,
        output_root=tmp_path / "studies",
    )
    summary = json.loads((study_dir / "summary" / "a1_target_scout.json").read_text(encoding="utf-8"))

    assert summary["overall_decision"]["recommended_next_target"] == "attitude_roll_pitch_continuation"
    assert summary["overall_decision"]["recommended_next_step"] == "start_px4_a1_attitude_family_readiness"
    assert summary["overall_decision"]["combo_ready"] is True


def test_px4_a1_target_scout_real_artifacts(tmp_path: Path) -> None:
    if not DEFAULT_BASELINE_STUDY.exists() or not DEFAULT_DIAGNOSTIC_STUDY.exists():
        pytest.skip("canonical PX4 A1 studies are not available")

    study_dir = run_px4_a1_target_scout(output_root=tmp_path / "studies")
    summary = json.loads((study_dir / "summary" / "a1_target_scout.json").read_text(encoding="utf-8"))

    assert summary["overall_decision"]["recommended_next_target"] == "attitude_roll_pitch_continuation"
    assert summary["overall_decision"]["recommended_next_step"] == "start_px4_a1_attitude_family_readiness"
