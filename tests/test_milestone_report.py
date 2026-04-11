from __future__ import annotations

import json
from pathlib import Path

from linearity_analysis.milestone_report import write_milestone_docs
from linearity_core.io import write_yaml


def _write_summary(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_baseline_study(
    study_dir: Path,
    study_name: str,
    *,
    accepted_run_count: int,
    supported_combo: dict,
    baseline_stability: dict,
) -> None:
    write_yaml(
        study_dir / "manifest.yaml",
        {
            "study_name": study_name,
            "source_modes": ["GUIDED_NOGPS", "STABILIZE"] if study_name.startswith("ardupilot") else ["OFFBOARD_ATTITUDE", "POSCTL"],
        },
    )
    write_yaml(
        study_dir / "prepared" / "schema_inventory.yaml",
        {
            "run_count": accepted_run_count,
            "data_quality": {"accepted_run_count": accepted_run_count},
        },
    )
    _write_summary(study_dir / "summary" / "study_summary.json", {"best_result": {**supported_combo, "summary": supported_combo}, "ranking": [supported_combo]})
    _write_summary(study_dir / "summary" / "baseline_stability.json", baseline_stability)
    _write_summary(study_dir / "summary" / "matrix_gallery.json", {"supported_count": 1})
    fit_dir = (
        study_dir
        / "fits"
        / f"{supported_combo['x_schema']}__{supported_combo['y_schema']}__{supported_combo['pooling_mode']}"
        / supported_combo["model_name"]
    )
    fit_dir.mkdir(parents=True, exist_ok=True)
    (fit_dir / "matrix_f.csv").write_text("feature,response\n", encoding="utf-8")
    (fit_dir / "matrix_heatmap_abs.png").write_text("", encoding="utf-8")


def _write_diagnostic_study(study_dir: Path, study_name: str, *, mode: str) -> None:
    write_yaml(study_dir / "manifest.yaml", {"study_name": study_name})
    _write_summary(
        study_dir / "summary" / "diagnostic_gate.json",
        {
            "status": "diagnostic_available",
            "attitude_axes": [
                {
                    "mode": mode,
                    "axis": "roll",
                    "tiers": [],
                    "all_accepted": True,
                    "first_problem_tier": "none",
                    "dominant_rejection_reasons": [],
                }
            ],
            "throttle": [
                {
                    "mode": mode,
                    "axis": "throttle",
                    "tiers": [],
                    "all_accepted": True,
                    "first_problem_tier": "none",
                    "dominant_rejection_reasons": [],
                }
            ],
            "conclusion": "ok",
        },
    )


def test_write_milestone_docs_renders_current_artifact_context(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    px4_baseline = tmp_path / "20260409_060620_px4_real_broad_ablation"
    ap_baseline = tmp_path / "20260409_180000_ardupilot_real_broad_ablation"
    px4_diag = tmp_path / "20260409_112322_px4_diagnostic_axis_matrix_balanced"
    ap_diag = tmp_path / "20260409_125954_ardupilot_diagnostic_axis_matrix_balanced"
    compare_dir = tmp_path / "20260409_190000_px4_vs_ardupilot_compare"
    guided_smoke_dir = tmp_path / "20260409_121755_ardupilot"
    partial_baseline_dir = tmp_path / "20260409_122239_ardupilot_stabilize_partial_baseline"
    throttle_dir = tmp_path / "20260409_122955_ardupilot_diagnostic_stabilize_throttle"
    contract_dir = tmp_path / "20260409_123128_cross_backend_contract_audit"

    px4_combo = {
        "x_schema": "commands_plus_state_history",
        "y_schema": "next_raw_state",
        "model_name": "ols_affine",
        "pooling_mode": "pooled",
        "median_test_r2": 0.999,
        "effective_condition_number": 9.1e5,
        "support": "supported",
    }
    ap_combo = {
        "x_schema": "commands_only",
        "y_schema": "actuator_response",
        "model_name": "ols_affine",
        "pooling_mode": "pooled",
        "median_test_r2": 0.995,
        "effective_condition_number": 1.5,
        "support": "supported",
    }
    _write_baseline_study(
        px4_baseline,
        "px4_real_broad_ablation",
        accepted_run_count=10,
        supported_combo=px4_combo,
        baseline_stability={"status": "comparison_available"},
    )
    _write_baseline_study(
        ap_baseline,
        "ardupilot_real_broad_ablation",
        accepted_run_count=16,
        supported_combo=ap_combo,
        baseline_stability={"status": "comparison_available"},
    )
    _write_summary(
        ap_baseline / "summary" / "state_evolution_audit.json",
        {
            "status": "audit_available",
            "comparison_status": "comparison_available",
            "current": {"supported_state_evolution": []},
            "conclusion": "厚化 baseline 没有改变 ArduPilot 当前明确 supported 的主集合。",
        },
    )
    _write_diagnostic_study(px4_diag, "px4_diagnostic_axis_matrix_balanced", mode="POSCTL")
    _write_diagnostic_study(ap_diag, "ardupilot_diagnostic_axis_matrix_balanced", mode="STABILIZE")
    _write_summary(
        compare_dir / "summary" / "backend_compare.json",
        {
            "px4": {
                "baseline": {
                    "scenario_generalization": {
                        "counts": {"generalized_supported": 8, "supported_but_local": 1, "not_generalized": 2},
                        "representative_generalized_supported": "commands_plus_state_history | next_raw_state | ols_affine | pooled",
                        "conclusion": "px4 baseline generalizes",
                    }
                },
                "diagnostic": {
                    "scenario_generalization": {
                        "counts": {"generalized_supported": 9, "supported_but_local": 0, "not_generalized": 1},
                        "representative_generalized_supported": "full_augmented | next_raw_state | ridge_affine | stratified",
                        "conclusion": "px4 diagnostic generalizes",
                    }
                },
            },
            "ardupilot": {
                "baseline": {
                    "scenario_generalization": {
                        "counts": {"generalized_supported": 2, "supported_but_local": 0, "not_generalized": 8},
                        "representative_generalized_supported": "commands_only | actuator_response | ols_affine | pooled",
                        "conclusion": "ardupilot baseline generalizes narrowly",
                    }
                },
                "diagnostic": {
                    "scenario_generalization": {
                        "counts": {"generalized_supported": 2, "supported_but_local": 0, "not_generalized": 8},
                        "representative_generalized_supported": "commands_only | actuator_response | ridge_affine | pooled",
                        "conclusion": "ardupilot diagnostic generalizes narrowly",
                    }
                },
            },
            "comparison": {
                "difference_driver": "baseline_stability_unresolved",
                "generalization_difference_driver": "both_support_cross_scenario_linearity_but_px4_is_broader",
                "both_baselines_stable": False,
                "throttle_boundary_consistent": True,
            },
        },
    )
    for path in (guided_smoke_dir, partial_baseline_dir, throttle_dir, contract_dir):
        path.mkdir(parents=True, exist_ok=True)

    outputs = write_milestone_docs(
        px4_baseline_dir=px4_baseline,
        ardupilot_baseline_dir=ap_baseline,
        px4_diagnostic_dir=px4_diag,
        ardupilot_diagnostic_dir=ap_diag,
        compare_dir=compare_dir,
        guided_smoke_dir=guided_smoke_dir,
        partial_baseline_dir=partial_baseline_dir,
        throttle_diagnostic_dir=throttle_dir,
        contract_audit_dir=contract_dir,
        docs_dir=docs_dir,
    )
    report_text = Path(outputs["report_path"]).read_text(encoding="utf-8")
    appendix_text = Path(outputs["appendix_path"]).read_text(encoding="utf-8")
    assert "里程碑报告" in report_text
    assert "generalization full" in report_text
    assert "state-evolution audit" in report_text
    assert "技术附录" in appendix_text
    assert "厚化 baseline 没有改变 ArduPilot 当前明确 supported 的主集合" in appendix_text
    assert "generalized_supported" in appendix_text
