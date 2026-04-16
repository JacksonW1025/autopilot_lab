from __future__ import annotations

import csv
import json
from pathlib import Path
import shutil

import pytest

from linearity_analysis.next_phase_decision_layer import (
    A1_TARGETED_REPRODUCTION_SUFFIX,
    A2_PAIR_TARGET_SUFFIX,
    ANCHOR_DEEP_DIVE_SUFFIX,
    IN_DEPTH_ANALYSIS_SUFFIX,
    NextPhaseDecisionAnalyzer,
    run_formal_v2_next_phase_decision_layer,
)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _anchor_deep_dive_rows() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    px4_rows = [
        {
            "anchor_id": "A1_baseline",
            "study_phase": "baseline",
            "backend": "px4",
            "x_schema": "full_augmented",
            "y_schema": "next_raw_state",
            "model_name": "ols_affine",
            "pooling_mode": "stratified",
            "support": "supported",
            "generalization_status": "generalized_supported",
            "x_effective_condition_number": 3435.59,
            "mask_nonzero_count": 47,
            "active_feature_count": 22,
            "abs_mass_command": 0.025,
            "abs_mass_state_current": 0.309,
            "abs_mass_state_lag_1": 0.233,
            "abs_mass_state_lag_2": 0.203,
            "abs_mass_state_lag_3": 0.168,
            "same_combo_mask_jaccard_to_pair": 0.625,
            "same_combo_raw_top4_jaccard_to_pair": 0.2903,
        },
        {
            "anchor_id": "A1_diagnostic",
            "study_phase": "diagnostic",
            "backend": "px4",
            "x_schema": "full_augmented",
            "y_schema": "next_raw_state",
            "model_name": "ols_affine",
            "pooling_mode": "stratified",
            "support": "supported",
            "generalization_status": "generalized_supported",
            "x_effective_condition_number": 2455.38,
            "mask_nonzero_count": 31,
            "active_feature_count": 18,
            "abs_mass_command": 0.011,
            "abs_mass_state_current": 0.352,
            "abs_mass_state_lag_1": 0.237,
            "abs_mass_state_lag_2": 0.183,
            "abs_mass_state_lag_3": 0.138,
            "same_combo_mask_jaccard_to_pair": 0.625,
            "same_combo_raw_top4_jaccard_to_pair": 0.2903,
        },
        {
            "anchor_id": "B1_baseline",
            "study_phase": "baseline",
            "backend": "px4",
            "x_schema": "full_augmented",
            "y_schema": "delta_state",
            "model_name": "ols_affine",
            "pooling_mode": "stratified",
            "support": "supported",
            "generalization_status": "supported_but_local",
            "x_effective_condition_number": 3435.59,
            "mask_nonzero_count": 45,
            "active_feature_count": 20,
            "abs_mass_command": 0.027,
            "abs_mass_state_current": 0.308,
            "abs_mass_state_lag_1": 0.233,
            "abs_mass_state_lag_2": 0.202,
            "abs_mass_state_lag_3": 0.165,
            "same_combo_mask_jaccard_to_pair": 0.6087,
            "same_combo_raw_top4_jaccard_to_pair": 0.25,
        },
        {
            "anchor_id": "B1_diagnostic",
            "study_phase": "diagnostic",
            "backend": "px4",
            "x_schema": "full_augmented",
            "y_schema": "delta_state",
            "model_name": "ols_affine",
            "pooling_mode": "stratified",
            "support": "supported",
            "generalization_status": "supported_but_local",
            "x_effective_condition_number": 2455.38,
            "mask_nonzero_count": 29,
            "active_feature_count": 18,
            "abs_mass_command": 0.012,
            "abs_mass_state_current": 0.351,
            "abs_mass_state_lag_1": 0.236,
            "abs_mass_state_lag_2": 0.182,
            "abs_mass_state_lag_3": 0.13,
            "same_combo_mask_jaccard_to_pair": 0.6087,
            "same_combo_raw_top4_jaccard_to_pair": 0.25,
        },
    ]
    ap_rows = [
        {
            "anchor_id": "A2_baseline",
            "family_id": "A2",
            "study_phase": "baseline",
            "backend": "ardupilot",
            "x_schema": "commands_only",
            "y_schema": "actuator_response",
            "model_name": "ridge_affine",
            "pooling_mode": "pooled",
            "support": "supported",
            "generalization_status": "generalized_supported",
            "x_effective_condition_number": 1.51,
            "mask_nonzero_count": 4,
            "active_feature_count": 1,
            "pair_mask_jaccard": 1.0,
            "pair_raw_top4_jaccard": 1.0,
            "abs_mass_command": 1.0,
            "abs_mass_state_current": 0.0,
            "abs_mass_state_lag_1": 0.0,
            "abs_mass_state_lag_2": 0.0,
            "abs_mass_state_lag_3": 0.0,
            "notes_source_matrix_path": "/tmp/a2_baseline_matrix.csv",
            "notes_source_mask_path": "/tmp/a2_baseline_mask.csv",
            "notes_source_metrics_path": "/tmp/a2_baseline_metrics.json",
        },
        {
            "anchor_id": "A2_diagnostic",
            "family_id": "A2",
            "study_phase": "diagnostic",
            "backend": "ardupilot",
            "x_schema": "commands_only",
            "y_schema": "actuator_response",
            "model_name": "ridge_affine",
            "pooling_mode": "pooled",
            "support": "supported",
            "generalization_status": "generalized_supported",
            "x_effective_condition_number": 1.03,
            "mask_nonzero_count": 4,
            "active_feature_count": 1,
            "pair_mask_jaccard": 1.0,
            "pair_raw_top4_jaccard": 1.0,
            "abs_mass_command": 1.0,
            "abs_mass_state_current": 0.0,
            "abs_mass_state_lag_1": 0.0,
            "abs_mass_state_lag_2": 0.0,
            "abs_mass_state_lag_3": 0.0,
            "notes_source_matrix_path": "/tmp/a2_diagnostic_matrix.csv",
            "notes_source_mask_path": "/tmp/a2_diagnostic_mask.csv",
            "notes_source_metrics_path": "/tmp/a2_diagnostic_metrics.json",
        },
        {
            "anchor_id": "C1_baseline",
            "family_id": "C1",
            "study_phase": "baseline",
            "backend": "ardupilot",
            "x_schema": "commands_plus_state_history",
            "y_schema": "selected_state_subset",
            "model_name": "ols_affine",
            "pooling_mode": "pooled",
            "support": "partial",
            "generalization_status": "not_generalized",
            "x_effective_condition_number": 2.16e9,
            "mask_nonzero_count": 16,
            "active_feature_count": 8,
            "pair_mask_jaccard": 1.0,
            "pair_raw_top4_jaccard": 1.0,
            "abs_mass_command": 0.05,
            "abs_mass_state_current": 0.35,
            "abs_mass_state_lag_1": 0.25,
            "abs_mass_state_lag_2": 0.2,
            "abs_mass_state_lag_3": 0.15,
            "notes_source_matrix_path": "/tmp/c1_baseline_matrix.csv",
            "notes_source_mask_path": "/tmp/c1_baseline_mask.csv",
            "notes_source_metrics_path": "/tmp/c1_baseline_metrics.json",
        },
        {
            "anchor_id": "C1_diagnostic",
            "family_id": "C1",
            "study_phase": "diagnostic",
            "backend": "ardupilot",
            "x_schema": "commands_plus_state_history",
            "y_schema": "selected_state_subset",
            "model_name": "ols_affine",
            "pooling_mode": "pooled",
            "support": "partial",
            "generalization_status": "not_generalized",
            "x_effective_condition_number": 8.99e8,
            "mask_nonzero_count": 16,
            "active_feature_count": 8,
            "pair_mask_jaccard": 1.0,
            "pair_raw_top4_jaccard": 1.0,
            "abs_mass_command": 0.05,
            "abs_mass_state_current": 0.35,
            "abs_mass_state_lag_1": 0.25,
            "abs_mass_state_lag_2": 0.2,
            "abs_mass_state_lag_3": 0.15,
            "notes_source_matrix_path": "/tmp/c1_diagnostic_matrix.csv",
            "notes_source_mask_path": "/tmp/c1_diagnostic_mask.csv",
            "notes_source_metrics_path": "/tmp/c1_diagnostic_metrics.json",
        },
        {
            "anchor_id": "D1_baseline",
            "family_id": "D1",
            "study_phase": "baseline",
            "backend": "ardupilot",
            "x_schema": "commands_plus_state_history",
            "y_schema": "selected_state_subset",
            "model_name": "ols_affine",
            "pooling_mode": "pooled",
            "support": "supported",
            "generalization_status": "generalized_supported",
            "x_effective_condition_number": 5.50e5,
            "mask_nonzero_count": 0,
            "active_feature_count": 0,
            "pair_mask_jaccard": "",
            "pair_raw_top4_jaccard": 0.0,
            "abs_mass_command": 0.1,
            "abs_mass_state_current": 0.4,
            "abs_mass_state_lag_1": 0.2,
            "abs_mass_state_lag_2": 0.15,
            "abs_mass_state_lag_3": 0.1,
            "notes_source_matrix_path": "/tmp/d1_baseline_matrix.csv",
            "notes_source_mask_path": "/tmp/d1_baseline_mask.csv",
            "notes_source_metrics_path": "/tmp/d1_baseline_metrics.json",
        },
        {
            "anchor_id": "D1_diagnostic",
            "family_id": "D1",
            "study_phase": "diagnostic",
            "backend": "ardupilot",
            "x_schema": "commands_plus_state_history",
            "y_schema": "selected_state_subset",
            "model_name": "ols_affine",
            "pooling_mode": "pooled",
            "support": "partial",
            "generalization_status": "not_generalized",
            "x_effective_condition_number": 7.54e6,
            "mask_nonzero_count": 0,
            "active_feature_count": 0,
            "pair_mask_jaccard": "",
            "pair_raw_top4_jaccard": 0.0,
            "abs_mass_command": 0.1,
            "abs_mass_state_current": 0.4,
            "abs_mass_state_lag_1": 0.2,
            "abs_mass_state_lag_2": 0.15,
            "abs_mass_state_lag_3": 0.1,
            "notes_source_matrix_path": "/tmp/d1_diagnostic_matrix.csv",
            "notes_source_mask_path": "/tmp/d1_diagnostic_mask.csv",
            "notes_source_metrics_path": "/tmp/d1_diagnostic_metrics.json",
        },
        {
            "anchor_id": "D2_baseline",
            "family_id": "D2",
            "study_phase": "baseline",
            "backend": "ardupilot",
            "x_schema": "commands_plus_state_history",
            "y_schema": "selected_state_subset",
            "model_name": "ols_affine",
            "pooling_mode": "pooled",
            "support": "partial",
            "generalization_status": "not_generalized",
            "x_effective_condition_number": 1.60e9,
            "mask_nonzero_count": 0,
            "active_feature_count": 0,
            "pair_mask_jaccard": "",
            "pair_raw_top4_jaccard": 1.0,
            "abs_mass_command": 0.05,
            "abs_mass_state_current": 0.35,
            "abs_mass_state_lag_1": 0.25,
            "abs_mass_state_lag_2": 0.2,
            "abs_mass_state_lag_3": 0.15,
            "notes_source_matrix_path": "/tmp/d2_baseline_matrix.csv",
            "notes_source_mask_path": "/tmp/d2_baseline_mask.csv",
            "notes_source_metrics_path": "/tmp/d2_baseline_metrics.json",
        },
        {
            "anchor_id": "D2_diagnostic",
            "family_id": "D2",
            "study_phase": "diagnostic",
            "backend": "ardupilot",
            "x_schema": "commands_plus_state_history",
            "y_schema": "selected_state_subset",
            "model_name": "ols_affine",
            "pooling_mode": "pooled",
            "support": "partial",
            "generalization_status": "not_generalized",
            "x_effective_condition_number": 5.57e8,
            "mask_nonzero_count": 0,
            "active_feature_count": 0,
            "pair_mask_jaccard": "",
            "pair_raw_top4_jaccard": 1.0,
            "abs_mass_command": 0.05,
            "abs_mass_state_current": 0.35,
            "abs_mass_state_lag_1": 0.25,
            "abs_mass_state_lag_2": 0.2,
            "abs_mass_state_lag_3": 0.15,
            "notes_source_matrix_path": "/tmp/d2_diagnostic_matrix.csv",
            "notes_source_mask_path": "/tmp/d2_diagnostic_mask.csv",
            "notes_source_metrics_path": "/tmp/d2_diagnostic_metrics.json",
        },
    ]
    return px4_rows, ap_rows


def _write_anchor_deep_dive(study_dir: Path) -> None:
    px4_rows, ap_rows = _anchor_deep_dive_rows()
    _write_json(
        study_dir / "summary" / "anchor_deep_dive.json",
        {
            "px4_line": {"contrast_driver": "scenario_stability_gap dominates"},
            "ardupilot_line": {
                "mask_empty_families": ["D1", "D2"],
                "raw_stable_but_formally_blocked_families": ["C1", "D2"],
            },
        },
    )
    _write_csv(study_dir / "tables" / "px4_a1_b1_matrix_comparison.csv", px4_rows)
    _write_csv(study_dir / "tables" / "ardupilot_a2_c1_d1_d2_boundary.csv", ap_rows)


def _write_in_depth_analysis(study_dir: Path) -> None:
    _write_json(study_dir / "summary" / "in_depth_analysis.json", {"stable_core": {"px4": {"stable_core_count": 80}}})
    _write_csv(
        study_dir / "tables" / "stable_core_matrix_readout.csv",
        [
            {
                "backend": "px4",
                "combo": "full_augmented | next_raw_state | ols_affine | stratified",
                "x_schema": "full_augmented",
                "y_schema": "next_raw_state",
                "model_name": "ols_affine",
                "pooling_mode": "stratified",
                "baseline_effective_condition_number": 3435.59,
                "diagnostic_effective_condition_number": 2455.38,
                "baseline_top_edge_overlap_jaccard": 0.62,
                "command_share": 0.02,
                "state_current_share": 0.31,
                "state_lag_1_share": 0.23,
                "state_lag_2_share": 0.20,
                "state_lag_3_share": 0.17,
                "baseline_matrix_path": "/tmp/a1_baseline_matrix.csv",
                "diagnostic_matrix_path": "/tmp/a1_diagnostic_matrix.csv",
            },
            {
                "backend": "ardupilot",
                "combo": "commands_only | actuator_response | ridge_affine | pooled",
                "x_schema": "commands_only",
                "y_schema": "actuator_response",
                "model_name": "ridge_affine",
                "pooling_mode": "pooled",
                "baseline_effective_condition_number": 1.51,
                "diagnostic_effective_condition_number": 1.03,
                "baseline_top_edge_overlap_jaccard": 1.0,
                "command_share": 1.0,
                "state_current_share": 0.0,
                "state_lag_1_share": 0.0,
                "state_lag_2_share": 0.0,
                "state_lag_3_share": 0.0,
                "baseline_matrix_path": "/tmp/a2_baseline_matrix.csv",
                "diagnostic_matrix_path": "/tmp/a2_diagnostic_matrix.csv",
            },
            {
                "backend": "px4",
                "combo": "commands_plus_state | future_state_horizon | lasso_affine | pooled",
                "x_schema": "commands_plus_state",
                "y_schema": "future_state_horizon",
                "model_name": "lasso_affine",
                "pooling_mode": "pooled",
                "baseline_effective_condition_number": 1123.64,
                "diagnostic_effective_condition_number": 610.44,
                "baseline_top_edge_overlap_jaccard": 1.0,
                "command_share": 0.09,
                "state_current_share": 0.91,
                "state_lag_1_share": 0.0,
                "state_lag_2_share": 0.0,
                "state_lag_3_share": 0.0,
                "baseline_matrix_path": "/tmp/watch_baseline_matrix.csv",
                "diagnostic_matrix_path": "/tmp/watch_diagnostic_matrix.csv",
            },
        ],
    )
    _write_csv(
        study_dir / "tables" / "ardupilot_conditioning_failure.csv",
        [
            {
                "failure_path": "mixed_mode_full",
                "baseline_metrics_path": "/tmp/c1_baseline_metrics.json",
                "diagnostic_metrics_path": "/tmp/c1_diagnostic_metrics.json",
            },
            {
                "failure_path": "stabilize_baseline_to_diagnostic_collapse",
                "baseline_metrics_path": "/tmp/d1_baseline_metrics.json",
                "diagnostic_metrics_path": "/tmp/d1_diagnostic_metrics.json",
            },
            {
                "failure_path": "guided_nogps_persistent_high_r2_high_cond",
                "baseline_metrics_path": "/tmp/d2_baseline_metrics.json",
                "diagnostic_metrics_path": "/tmp/d2_diagnostic_metrics.json",
            },
        ],
    )
    _write_csv(
        study_dir / "tables" / "stability_boundary.csv",
        [
            {
                "source_category": "supported_but_local",
                "comparison_generalization_status": "local",
                "primary_driver": "stratification",
                "study_dir": "/tmp/b1",
            },
            {
                "source_category": "ardupilot_partial_not_generalized_state_evolution",
                "comparison_generalization_status": "mixed_mode",
                "primary_driver": "feature_collinearity",
                "study_dir": "/tmp/c1",
            },
            {
                "source_category": "targeted_inconclusive_family",
                "comparison_generalization_status": "stabilize",
                "primary_driver": "none",
                "study_dir": "/tmp/d1_baseline",
            },
            {
                "source_category": "targeted_inconclusive_family",
                "comparison_generalization_status": "stabilize",
                "primary_driver": "feature_collinearity",
                "study_dir": "/tmp/d1_diagnostic",
            },
            {
                "source_category": "targeted_inconclusive_family",
                "comparison_generalization_status": "guided_nogps",
                "primary_driver": "feature_collinearity",
                "study_dir": "/tmp/d2_baseline",
            },
            {
                "source_category": "targeted_inconclusive_family",
                "comparison_generalization_status": "guided_nogps",
                "primary_driver": "feature_collinearity",
                "study_dir": "/tmp/d2_diagnostic",
            },
        ],
    )


def _write_a2_pair_target(study_dir: Path) -> None:
    _write_json(
        study_dir / "summary" / "a2_pair_target_readiness.json",
        {
            "overall_decision": {
                "ready_for_pair_attack_v1": True,
                "recommended_path": "start_guided_nogps_pair_attack_v1",
            }
        },
    )


def _write_a1_targeted_reproduction(study_dir: Path) -> None:
    _write_json(
        study_dir / "summary" / "a1_roll_pitch_targeted_reproduction.json",
        {
            "study_scope": {
                "combo": "full_augmented | next_raw_state | ols_affine | stratified",
            },
            "response_results": [
                {
                    "baseline_same_axis_share": 0.595,
                    "diagnostic_same_axis_share": 0.738,
                },
                {
                    "baseline_same_axis_share": 0.59,
                    "diagnostic_same_axis_share": 0.682,
                },
            ],
            "overall_decision": {
                "ready_for_targeted_reproduction_v1": True,
                "recommended_path": "lock_px4_a1_roll_pitch_targeted_scope",
            },
        },
    )


def _write_source_bundle(root: Path, *, prefix: str = "20260416") -> dict[str, Path]:
    anchor_dir = root / f"{prefix}_000001{ANCHOR_DEEP_DIVE_SUFFIX}"
    in_depth_dir = root / f"{prefix}_000002{IN_DEPTH_ANALYSIS_SUFFIX}"
    a2_dir = root / f"{prefix}_000003{A2_PAIR_TARGET_SUFFIX}"
    a1_dir = root / f"{prefix}_000004{A1_TARGETED_REPRODUCTION_SUFFIX}"
    _write_anchor_deep_dive(anchor_dir)
    _write_in_depth_analysis(in_depth_dir)
    _write_a2_pair_target(a2_dir)
    _write_a1_targeted_reproduction(a1_dir)
    return {
        "anchor": anchor_dir,
        "in_depth": in_depth_dir,
        "a2": a2_dir,
        "a1": a1_dir,
    }


def test_next_phase_decision_layer_auto_discovers_and_ranks(tmp_path: Path) -> None:
    _write_source_bundle(tmp_path)

    study_dir = run_formal_v2_next_phase_decision_layer(
        artifact_root=tmp_path,
        output_dir=tmp_path / "decision_layer",
    )
    summary = json.loads((study_dir / "summary" / "next_phase_decision_layer.json").read_text(encoding="utf-8"))
    rows = list(csv.DictReader((study_dir / "tables" / "candidate_board.csv").open(encoding="utf-8")))

    assert [row["candidate_id"] for row in rows] == ["A2", "A1", "B1", "C1", "D2", "D1"]
    assert {row["candidate_id"]: row["decision_bucket"] for row in rows} == {
        "A2": "primary_entry_ready",
        "A1": "mechanism_rich_hard_mode",
        "B1": "contrast_non_entry",
        "C1": "boundary_or_pathology",
        "D2": "boundary_or_pathology",
        "D1": "boundary_or_pathology",
    }
    lookup = {row["candidate_id"]: row for row in rows}
    assert "stable partial + extreme conditioning" in lookup["C1"]["rationale"]
    assert "stable raw template + empty mask" in lookup["D2"]["rationale"]
    assert "diagnostic raw collapse" in lookup["D1"]["rationale"]
    assert lookup["A2"]["explicit_ready_signal"] == "pair_target_ready"
    assert lookup["A1"]["explicit_ready_signal"] == "targeted_reproduction_ready"
    assert summary["overall_recommendation"]["default_entry"] == "A2"
    assert (study_dir / "reports" / "next_phase_decision_layer.md").exists()
    assert (study_dir / "tables" / "stable_core_watchlist.csv").exists()


def test_next_phase_decision_layer_explicit_paths_override_discovery(tmp_path: Path) -> None:
    _write_source_bundle(tmp_path, prefix="20260416")
    manual = tmp_path / "manual"
    manual.mkdir()
    manual_sources = {
        "anchor": manual / "anchor_override",
        "in_depth": manual / "in_depth_override",
        "a2": manual / "a2_override",
        "a1": manual / "a1_override",
    }
    _write_anchor_deep_dive(manual_sources["anchor"])
    _write_in_depth_analysis(manual_sources["in_depth"])
    _write_a2_pair_target(manual_sources["a2"])
    _write_a1_targeted_reproduction(manual_sources["a1"])

    study_dir = run_formal_v2_next_phase_decision_layer(
        artifact_root=tmp_path,
        anchor_deep_dive_dir=manual_sources["anchor"],
        in_depth_analysis_dir=manual_sources["in_depth"],
        a2_pair_target_dir=manual_sources["a2"],
        a1_targeted_reproduction_dir=manual_sources["a1"],
        output_dir=tmp_path / "explicit_decision_layer",
    )
    summary = json.loads((study_dir / "summary" / "next_phase_decision_layer.json").read_text(encoding="utf-8"))

    assert summary["source_studies"]["anchor_deep_dive_dir"] == str(manual_sources["anchor"].resolve())
    assert summary["source_studies"]["a1_targeted_reproduction_dir"] == str(manual_sources["a1"].resolve())


def test_next_phase_decision_layer_missing_required_suffix_fails_fast(tmp_path: Path) -> None:
    _write_source_bundle(tmp_path)
    target = next(path for path in tmp_path.iterdir() if path.name.endswith(A2_PAIR_TARGET_SUFFIX))
    shutil.rmtree(target)

    with pytest.raises(FileNotFoundError):
        NextPhaseDecisionAnalyzer(artifact_root=tmp_path)


def test_next_phase_decision_layer_real_artifacts(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive",
        root / "artifacts/studies/20260414_064902_formal_v2_in_depth_analysis",
        root / "artifacts/studies/20260416_003634_371133_ardupilot_a2_pair_target_readiness",
        root / "artifacts/studies/20260416_010626_381143_px4_a1_roll_pitch_targeted_reproduction",
    ]
    if not all(path.exists() for path in required):
        pytest.skip("canonical next-phase decision inputs are not available")

    study_dir = run_formal_v2_next_phase_decision_layer(output_dir=tmp_path / "real_decision_layer")
    rows = list(csv.DictReader((study_dir / "tables" / "candidate_board.csv").open(encoding="utf-8")))

    assert [row["candidate_id"] for row in rows] == ["A2", "A1", "B1", "C1", "D2", "D1"]
    assert rows[0]["decision_bucket"] == "primary_entry_ready"
    assert rows[1]["decision_bucket"] == "mechanism_rich_hard_mode"
