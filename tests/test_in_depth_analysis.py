from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
import sys

from linearity_analysis.in_depth_analysis import (
    FormalV2InDepthAnalyzer,
    build_mode_mixture_context,
    build_throttle_driver_context,
    choose_minimal_stable_x,
    choose_primary_driver,
    classify_feature_block,
    classify_response_family,
    compute_feature_block_shares,
    extract_top_edges,
    is_same_state_edge,
    response_base_name,
)
from linearity_analysis.matrix_gallery import load_matrix_csv


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "analyze_formal_v2_in_depth.py"


def _load_script_module():
    spec = importlib.util.spec_from_file_location("analyze_formal_v2_in_depth", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_matrix_csv(path: Path, features: list[str], responses: list[str], rows: list[list[float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["feature", *responses])
        for feature, values in zip(features, rows, strict=True):
            writer.writerow([feature, *values])


def _write_combo_artifacts(
    study_dir: Path,
    *,
    x_schema: str,
    y_schema: str,
    model_name: str,
    pooling_mode: str,
    features: list[str] | None = None,
    responses: list[str] | None = None,
    rows: list[list[float]] | None = None,
    metrics_extra: dict | None = None,
) -> None:
    features = features or ["command_roll", "roll", "roll__lag_1"]
    responses = responses or ["future_state_roll", "future_state_pitch"]
    rows = rows or [[1.0, 0.2], [0.5, 0.1], [0.1, 0.0]]
    fit_dir = study_dir / "fits" / f"{x_schema}__{y_schema}__{pooling_mode}" / model_name
    _write_matrix_csv(fit_dir / "matrix_f.csv", features, responses, rows)
    metrics = {
        "x_schema": x_schema,
        "y_schema": y_schema,
        "model_name": model_name,
        "pooling_mode": pooling_mode,
        "median_test_r2": 0.95,
        "effective_condition_number": 10.0,
        "coefficient_stability": 0.9,
        "scenario_consistency": 0.9,
    }
    if metrics_extra:
        metrics.update(metrics_extra)
    _write_json(fit_dir / "metrics.json", metrics)


def _write_scenario_generalization(study_dir: Path, entries: list[dict]) -> None:
    _write_json(
        study_dir / "summary" / "scenario_generalization.json",
        {
            "status": "scenario_available",
            "entries": entries,
        },
    )


def _write_state_evolution_audit(study_dir: Path, entries: list[dict]) -> None:
    _write_json(
        study_dir / "summary" / "state_evolution_audit.json",
        {
            "status": "audit_available",
            "entries": entries,
        },
    )


def _write_study_summary(study_dir: Path, best_result: dict | None = None) -> None:
    _write_json(
        study_dir / "summary" / "study_summary.json",
        {
            "best_result": best_result or {},
            "ranking": [best_result] if best_result else [],
        },
    )


def _write_diagnostic_gate(study_dir: Path, *, throttle_boundary: str = "none") -> None:
    _write_json(study_dir / "summary" / "diagnostic_gate.json", {"throttle_boundary": throttle_boundary})


def _write_targeted_validation(validation_dir: Path, stabilize_baseline: Path, stabilize_diagnostic: Path, guided_baseline: Path, guided_diagnostic: Path) -> None:
    _write_json(
        validation_dir / "summary" / "state_evolution_validation.json",
        {
            "modes": {
                "stabilize": {
                    "baseline_dir": str(stabilize_baseline),
                    "diagnostic_dir": str(stabilize_diagnostic),
                    "representative_combo": "commands_plus_state_history | selected_state_subset | ols_affine | pooled",
                },
                "guided_nogps": {
                    "baseline_dir": str(guided_baseline),
                    "diagnostic_dir": str(guided_diagnostic),
                    "representative_combo": "commands_plus_state_history | selected_state_subset | ols_affine | pooled",
                },
            }
        },
    )


def test_feature_and_response_block_helpers() -> None:
    assert classify_feature_block("command_roll") == "command"
    assert classify_feature_block("roll") == "state_current"
    assert classify_feature_block("command_roll__lag_1") == "state_lag_1"
    assert classify_feature_block("roll__lag_2") == "state_lag_2"
    assert classify_feature_block("mode_STABILIZE") == "other_augmented"
    assert classify_response_family("future_state_roll") == "future_state"
    assert classify_response_family("delta_state_roll") == "delta_state"
    assert classify_response_family("roll__h2") == "future_state_horizon"
    assert response_base_name("roll__h2") == "roll"
    assert is_same_state_edge("roll", "future_state_roll")
    assert not is_same_state_edge("pitch", "future_state_roll")


def test_extract_top_edges_and_block_shares(tmp_path: Path) -> None:
    matrix_csv = tmp_path / "fits" / "commands_plus_state_history__next_raw_state__pooled" / "ols_affine" / "matrix_f.csv"
    _write_matrix_csv(
        matrix_csv,
        ["command_roll", "roll", "roll__lag_1", "mode_STABILIZE"],
        ["future_state_roll", "future_state_pitch"],
        [[2.0, 0.0], [1.0, 0.0], [0.5, 0.0], [0.5, 0.0]],
    )

    matrix_data = load_matrix_csv(matrix_csv)
    top_edges = extract_top_edges(matrix_data, top_k=3)
    shares = compute_feature_block_shares(matrix_data)

    assert top_edges[0]["feature"] == "command_roll"
    assert top_edges[0]["response"] == "future_state_roll"
    assert shares["command"] == 0.5
    assert shares["state_current"] == 0.25
    assert shares["state_lag_1"] == 0.125
    assert shares["other_augmented"] == 0.125


def test_choose_minimal_stable_x_prefers_smallest_x_schema() -> None:
    selected = choose_minimal_stable_x(
        [
            {"x_schema": "full_augmented", "support": "supported", "median_test_r2": 0.99},
            {"x_schema": "commands_plus_state", "support": "supported", "median_test_r2": 0.90},
            {"x_schema": "commands_plus_state_history", "support": "supported", "median_test_r2": 0.95},
        ]
    )

    assert selected["x_schema"] == "commands_plus_state"


def test_choose_primary_driver_priority() -> None:
    assert choose_primary_driver(["stratification", "feature_collinearity", "throttle"]) == "feature_collinearity"
    assert choose_primary_driver(["throttle", "stratification"]) == "throttle"
    assert choose_primary_driver([]) == "none"


def test_mode_mixture_fixture_detects_targeted_improvement() -> None:
    assert build_mode_mixture_context("partial", ["supported", "partial"])
    assert not build_mode_mixture_context("supported", ["partial", "unsupported"])


def test_throttle_only_degradation_fixture_detects_driver() -> None:
    scenario_entry = {
        "scenario_subgroup_r2": {
            "dynamic": 0.95,
            "nominal": 0.96,
            "throttle_biased": 0.70,
        }
    }
    assert build_throttle_driver_context(scenario_entry=scenario_entry, diagnostic_throttle_evidence=True)


def test_build_stable_core_section_uses_intersection(tmp_path: Path) -> None:
    px4_baseline = tmp_path / "px4_baseline"
    px4_diagnostic = tmp_path / "px4_diagnostic"
    ap_baseline = tmp_path / "ap_baseline"
    ap_diagnostic = tmp_path / "ap_diagnostic"
    validation = tmp_path / "validation"
    for study_dir in (px4_baseline, px4_diagnostic, ap_baseline, ap_diagnostic):
        _write_diagnostic_gate(study_dir)
        _write_state_evolution_audit(study_dir, [])
        _write_study_summary(study_dir)

    baseline_entries = [
        {
            "x_schema": "commands_plus_state",
            "y_schema": "selected_state_subset",
            "model_name": "ols_affine",
            "pooling_mode": "pooled",
            "support": "supported",
            "median_test_r2": 0.9,
            "effective_condition_number": 10.0,
            "scenario_consistency": 0.9,
            "generalization_status": "generalized_supported",
        },
        {
            "x_schema": "full_augmented",
            "y_schema": "selected_state_subset",
            "model_name": "ols_affine",
            "pooling_mode": "pooled",
            "support": "supported",
            "median_test_r2": 0.9,
            "effective_condition_number": 10.0,
            "scenario_consistency": 0.9,
            "generalization_status": "generalized_supported",
        },
    ]
    diagnostic_entries = [
        baseline_entries[1],
        {
            "x_schema": "feature_mapped_linear",
            "y_schema": "selected_state_subset",
            "model_name": "ols_affine",
            "pooling_mode": "pooled",
            "support": "supported",
            "median_test_r2": 0.92,
            "effective_condition_number": 10.0,
            "scenario_consistency": 0.9,
            "generalization_status": "generalized_supported",
        },
    ]
    _write_scenario_generalization(px4_baseline, baseline_entries)
    _write_scenario_generalization(px4_diagnostic, diagnostic_entries)
    _write_scenario_generalization(ap_baseline, [])
    _write_scenario_generalization(ap_diagnostic, [])
    _write_combo_artifacts(px4_baseline, x_schema="full_augmented", y_schema="selected_state_subset", model_name="ols_affine", pooling_mode="pooled")
    _write_combo_artifacts(px4_diagnostic, x_schema="full_augmented", y_schema="selected_state_subset", model_name="ols_affine", pooling_mode="pooled")

    analyzer = FormalV2InDepthAnalyzer(
        px4_baseline_dir=px4_baseline,
        px4_diagnostic_dir=px4_diagnostic,
        ardupilot_baseline_dir=ap_baseline,
        ardupilot_diagnostic_dir=ap_diagnostic,
        targeted_validation_dir=validation,
    )

    section = analyzer.build_stable_core_section()

    assert section["px4"]["stable_core_count"] == 1
    assert not section["px4"]["baseline_is_subset_of_diagnostic"]
    assert section["px4"]["diagnostic_only_generalized_supported_count"] == 1
    assert section["px4"]["entries"][0]["combo"] == "full_augmented | selected_state_subset | ols_affine | pooled"


def test_backend_alignment_fixture_has_no_strict_overlap(tmp_path: Path) -> None:
    px4_baseline = tmp_path / "px4_baseline"
    px4_diagnostic = tmp_path / "px4_diagnostic"
    ap_baseline = tmp_path / "ap_baseline"
    ap_diagnostic = tmp_path / "ap_diagnostic"
    validation = tmp_path / "validation"
    for study_dir in (px4_baseline, px4_diagnostic, ap_baseline, ap_diagnostic):
        _write_diagnostic_gate(study_dir)
        _write_state_evolution_audit(study_dir, [])
        _write_study_summary(study_dir)
    _write_combo_artifacts(px4_baseline, x_schema="commands_plus_state", y_schema="selected_state_subset", model_name="ols_affine", pooling_mode="pooled")
    _write_combo_artifacts(ap_baseline, x_schema="commands_only", y_schema="selected_state_subset", model_name="ols_affine", pooling_mode="pooled")

    analyzer = FormalV2InDepthAnalyzer(
        px4_baseline_dir=px4_baseline,
        px4_diagnostic_dir=px4_diagnostic,
        ardupilot_baseline_dir=ap_baseline,
        ardupilot_diagnostic_dir=ap_diagnostic,
        targeted_validation_dir=validation,
    )
    stable_core = {
        "px4": {
            "entries": [
                {
                    "x_schema": "commands_plus_state",
                    "y_schema": "selected_state_subset",
                    "model_name": "ols_affine",
                    "pooling_mode": "pooled",
                    "combo": "commands_plus_state | selected_state_subset | ols_affine | pooled",
                }
            ]
        },
        "ardupilot": {
            "entries": [
                {
                    "x_schema": "commands_only",
                    "y_schema": "selected_state_subset",
                    "model_name": "ols_affine",
                    "pooling_mode": "pooled",
                    "combo": "commands_only | selected_state_subset | ols_affine | pooled",
                }
            ]
        },
    }

    section = analyzer.build_backend_alignment_section(stable_core)

    assert section["strict_schema_overlap_count"] == 0
    assert section["shared_alignment_key_count"] == 1
    assert section["shared_rows"][0]["px4_minimal_x"] == "commands_plus_state"
    assert section["shared_rows"][0]["ardupilot_minimal_x"] == "commands_only"


def test_cli_smoke_runs_on_canonical_artifacts(tmp_path: Path) -> None:
    module = _load_script_module()

    exit_code = module.main(["--output-dir", str(tmp_path / "analysis")])

    assert exit_code == 0
    summary_path = tmp_path / "analysis" / "summary" / "in_depth_analysis.json"
    report_path = tmp_path / "analysis" / "reports" / "in_depth_analysis.md"
    assert summary_path.exists()
    assert report_path.exists()
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    assert payload["stable_core"]["px4"]["stable_core_count"] == 80
    assert payload["stable_core"]["ardupilot"]["stable_core_count"] == 12
    assert payload["backend_alignment"]["shared_alignment_key_count"] == 9
    for table_name in (
        "stable_core_matrix_readout.csv",
        "px4_physical_vs_state_continuation.csv",
        "backend_alignment.csv",
        "ardupilot_conditioning_failure.csv",
        "stability_boundary.csv",
    ):
        assert (tmp_path / "analysis" / "tables" / table_name).exists()
