from __future__ import annotations

import json
from pathlib import Path

from linearity_analysis.backend_compare import run_backend_compare
from linearity_analysis.matrix_gallery import build_matrix_gallery_payload, render_matrix_gallery_markdown, write_matrix_gallery_artifacts
from linearity_core.io import write_rows_csv, write_yaml
from linearity_core.study_artifacts import (
    build_backend_compare_payload,
    build_baseline_stability_payload,
    build_scenario_generalization_payload,
    build_guided_mode_smoke_payload,
    build_diagnostic_gate_payload,
    build_state_evolution_audit_payload,
    render_backend_compare_markdown,
    render_baseline_stability_markdown,
    render_scenario_generalization_markdown,
    render_guided_mode_smoke_markdown,
    render_diagnostic_gate_markdown,
    render_state_evolution_audit_markdown,
)
import linearity_core.study_artifacts as study_artifacts


def _write_summary(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _fake_combo(x_schema: str, y_schema: str, model_name: str, pooling_mode: str, *, r2: float, condition: float) -> dict:
    return {
        "x_schema": x_schema,
        "y_schema": y_schema,
        "model_name": model_name,
        "pooling_mode": pooling_mode,
        "summary": {
            "median_test_r2": r2,
            "effective_condition_number": condition,
        },
    }


def _write_sparsity_mask(path: Path, edges: list[tuple[str, str]]) -> None:
    responses = sorted({response for _feature, response in edges}) or ["response"]
    feature_rows = {}
    for feature, response in edges:
        feature_rows.setdefault(feature, {"feature": feature})
        feature_rows[feature][response] = 1.0
    if not feature_rows:
        feature_rows["placeholder"] = {"feature": "placeholder", "response": 0.0}
    for row in feature_rows.values():
        for response in responses:
            row.setdefault(response, 0.0)
    write_rows_csv(path, list(feature_rows.values()), fieldnames=["feature", *responses])


def _write_metrics(
    path: Path,
    *,
    x_schema: str,
    y_schema: str,
    pooling_mode: str,
    model_name: str,
    median_test_r2: float,
    coefficient_stability: float,
    effective_condition_number: float,
    sparsity_ratio: float = 0.4,
    conditioning_pruned_features: list[str] | None = None,
    extra_fields: dict | None = None,
) -> None:
    payload = {
        "x_schema": x_schema,
        "y_schema": y_schema,
        "pooling_mode": pooling_mode,
        "model_name": model_name,
        "median_test_r2": median_test_r2,
        "coefficient_stability": coefficient_stability,
        "effective_condition_number": effective_condition_number,
        "condition_number": effective_condition_number,
        "sparsity_ratio": sparsity_ratio,
        "conditioning_pruned_features": conditioning_pruned_features or [],
    }
    if extra_fields:
        payload.update(extra_fields)
    _write_summary(
        path,
        payload,
    )


def _write_diagnostic_run(
    base_dir: Path,
    *,
    run_id: str,
    mode: str,
    axis: str,
    tier: str,
    acceptance: str,
    reasons: list[str],
) -> Path:
    run_dir = base_dir / run_id
    write_yaml(
        run_dir / "manifest.yaml",
        {
            "run_id": run_id,
            "flight_mode": mode,
            "axis": axis,
            "research_acceptance": acceptance,
            "research_rejection_reasons": reasons,
            "study_config": {
                "axis": axis,
                "extras": {
                    "amplitude_tier": tier,
                },
            },
        },
    )
    return run_dir


def test_baseline_stability_payload_compares_previous_study(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(study_artifacts, "STUDY_ARTIFACT_ROOT", tmp_path)
    study_name = "px4_real_broad_ablation"
    previous_dir = tmp_path / f"20260408_062436_{study_name}"
    current_dir = tmp_path / f"20260409_180000_{study_name}"
    previous_manifest = {
        "study_name": study_name,
        "source_backends": ["px4"],
        "source_modes": ["OFFBOARD_ATTITUDE", "POSCTL"],
        "source_config_profiles": ["px4_real_offboard_attitude_nominal", "px4_real_posctl_nominal"],
    }
    current_manifest = dict(previous_manifest)
    current_manifest["study_id"] = current_dir.name

    write_yaml(previous_dir / "manifest.yaml", previous_manifest)
    write_yaml(current_dir / "manifest.yaml", current_manifest)
    write_yaml(previous_dir / "prepared" / "schema_inventory.yaml", {"run_count": 6, "data_quality": {"accepted_run_count": 6}})
    write_yaml(current_dir / "prepared" / "schema_inventory.yaml", {"run_count": 10, "data_quality": {"accepted_run_count": 10}})

    previous_best = _fake_combo("commands_plus_state_history", "next_raw_state", "ols_affine", "pooled", r2=0.9980, condition=950000.0)
    current_best = _fake_combo("commands_plus_state_history", "next_raw_state", "ols_affine", "pooled", r2=0.9990, condition=910000.0)
    previous_supported = {
        "x_schema": "commands_plus_state_history",
        "y_schema": "next_raw_state",
        "model_name": "ols_affine",
        "pooling_mode": "pooled",
        "median_test_r2": 0.9980,
        "effective_condition_number": 950000.0,
        "support": "supported",
    }
    current_supported = {
        "x_schema": "commands_plus_state_history",
        "y_schema": "next_raw_state",
        "model_name": "ols_affine",
        "pooling_mode": "pooled",
        "median_test_r2": 0.9990,
        "effective_condition_number": 910000.0,
        "support": "supported",
    }
    previous_summary = {
        "best_result": previous_best,
        "ranking": [previous_supported],
    }
    current_summary = {
        "best_result": current_best,
        "ranking": [current_supported],
    }
    _write_summary(previous_dir / "summary" / "study_summary.json", previous_summary)
    _write_summary(current_dir / "summary" / "study_summary.json", current_summary)

    _write_sparsity_mask(
        previous_dir / "fits" / "commands_plus_state_history__next_raw_state__pooled" / "ols_affine" / "sparsity_mask.csv",
        [("command_roll", "future_state_roll"), ("roll", "future_state_roll")],
    )
    _write_sparsity_mask(
        current_dir / "fits" / "commands_plus_state_history__next_raw_state__pooled" / "ols_affine" / "sparsity_mask.csv",
        [("command_roll", "future_state_roll"), ("pitch", "future_state_pitch")],
    )

    payload = build_baseline_stability_payload(current_dir, study_name, current_summary, {"run_count": 10, "data_quality": {"accepted_run_count": 10}}, current_manifest)
    assert payload["status"] == "comparison_available"
    assert payload["previous"]["accepted_run_count"] == 6
    assert payload["current"]["accepted_run_count"] == 10
    assert payload["deltas"]["best_result"]["median_test_r2_delta"] > 0.0
    assert payload["sparsity_overlap"]["best_result"]["intersection_count"] == 1
    markdown = render_baseline_stability_markdown(payload)
    assert "Baseline Stability" in markdown
    assert "current_accepted_runs: 10" in markdown


def test_diagnostic_gate_payload_splits_attitude_and_throttle(tmp_path: Path) -> None:
    run_specs = [
        ("run_roll_small", "POSCTL", "roll", "small", "accepted", []),
        ("run_roll_medium", "POSCTL", "roll", "medium", "accepted", []),
        ("run_roll_large", "POSCTL", "roll", "large", "accepted", []),
        ("run_throttle_small", "POSCTL", "throttle", "small", "rejected", ["insufficient_active_nonzero_command_samples"]),
    ]
    run_dirs = []
    for run_id, mode, axis, tier, acceptance, reasons in run_specs:
        run_dir = tmp_path / run_id
        write_yaml(
            run_dir / "manifest.yaml",
            {
                "run_id": run_id,
                "flight_mode": mode,
                "axis": axis,
                "research_acceptance": acceptance,
                "research_rejection_reasons": reasons,
                "study_config": {
                    "axis": axis,
                    "extras": {
                        "amplitude_tier": tier,
                    },
                },
            },
        )
        run_dirs.append(run_dir)

    payload = build_diagnostic_gate_payload(run_dirs)
    assert payload["status"] == "diagnostic_available"
    assert payload["attitude_axes"][0]["all_accepted"] is True
    assert payload["throttle"][0]["first_problem_tier"] == "small"
    assert payload["throttle"][0]["dominant_rejection_reasons"] == ["insufficient_active_nonzero_command_samples"]
    markdown = render_diagnostic_gate_markdown(payload)
    assert "## Attitude Axes" in markdown
    assert "## Throttle" in markdown
    assert "insufficient_active_nonzero_command_samples" in markdown


def test_state_evolution_audit_reports_blockers_and_support_changes(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(study_artifacts, "STUDY_ARTIFACT_ROOT", tmp_path)
    study_name = "ardupilot_real_broad_ablation"
    previous_dir = tmp_path / f"20260409_123731_{study_name}"
    current_dir = tmp_path / f"20260409_180000_{study_name}"
    manifest = {
        "study_name": study_name,
        "source_backends": ["ardupilot"],
        "source_modes": ["GUIDED_NOGPS", "STABILIZE"],
        "source_config_profiles": ["ardupilot_real_guided_nogps_nominal", "ardupilot_real_stabilize_nominal"],
    }
    write_yaml(previous_dir / "manifest.yaml", manifest)
    write_yaml(current_dir / "manifest.yaml", manifest)
    write_yaml(previous_dir / "prepared" / "schema_inventory.yaml", {"run_count": 10, "data_quality": {"accepted_run_count": 10}})
    write_yaml(current_dir / "prepared" / "schema_inventory.yaml", {"run_count": 16, "data_quality": {"accepted_run_count": 16}})
    _write_summary(
        previous_dir / "summary" / "study_summary.json",
        {
            "ranking": [
                {
                    "x_schema": "commands_only",
                    "y_schema": "actuator_response",
                    "model_name": "ols_affine",
                    "pooling_mode": "pooled",
                    "support": "supported",
                }
            ]
        },
    )
    _write_summary(
        current_dir / "summary" / "study_summary.json",
        {
            "ranking": [
                {
                    "x_schema": "commands_only",
                    "y_schema": "actuator_response",
                    "model_name": "ols_affine",
                    "pooling_mode": "pooled",
                    "support": "supported",
                },
                {
                    "x_schema": "commands_plus_state",
                    "y_schema": "selected_state_subset",
                    "model_name": "ols_affine",
                    "pooling_mode": "pooled",
                    "support": "partial",
                },
            ]
        },
    )
    _write_metrics(
        previous_dir / "fits" / "commands_plus_state__selected_state_subset__pooled" / "ols_affine" / "metrics.json",
        x_schema="commands_plus_state",
        y_schema="selected_state_subset",
        pooling_mode="pooled",
        model_name="ols_affine",
        median_test_r2=0.99,
        coefficient_stability=1.0,
        effective_condition_number=2.0e8,
        conditioning_pruned_features=["mode_STABILIZE"],
    )
    _write_metrics(
        current_dir / "fits" / "commands_plus_state__selected_state_subset__pooled" / "ols_affine" / "metrics.json",
        x_schema="commands_plus_state",
        y_schema="selected_state_subset",
        pooling_mode="pooled",
        model_name="ols_affine",
        median_test_r2=0.99,
        coefficient_stability=1.0,
        effective_condition_number=2.0e8,
        conditioning_pruned_features=["mode_STABILIZE"],
    )
    _write_metrics(
        current_dir / "fits" / "commands_plus_state_history__next_raw_state__pooled" / "ridge_affine" / "metrics.json",
        x_schema="commands_plus_state_history",
        y_schema="next_raw_state",
        pooling_mode="pooled",
        model_name="ridge_affine",
        median_test_r2=0.92,
        coefficient_stability=0.52,
        effective_condition_number=9.0e5,
        conditioning_pruned_features=["backend_ardupilot"],
    )
    _write_metrics(
        current_dir / "fits" / "full_augmented__delta_state__stratified" / "lasso_affine" / "metrics.json",
        x_schema="full_augmented",
        y_schema="delta_state",
        pooling_mode="stratified",
        model_name="lasso_affine",
        median_test_r2=0.31,
        coefficient_stability=0.41,
        effective_condition_number=3.0e6,
        conditioning_pruned_features=["scenario_nominal"],
    )

    payload = build_state_evolution_audit_payload(
        current_dir,
        study_name,
        {"run_count": 16, "data_quality": {"accepted_run_count": 16}},
        manifest,
    )
    assert payload["status"] == "audit_available"
    assert payload["comparison_status"] == "comparison_available"
    assert payload["entries"][0]["primary_blocker"] == "condition_number"
    blockers = {entry["model_name"]: entry["primary_blocker"] for entry in payload["entries"]}
    assert blockers["ridge_affine"] == "stability"
    assert blockers["lasso_affine"] == "mixed"
    assert payload["conclusion"].startswith("厚化 baseline 没有改变 ArduPilot 当前明确 supported 的主集合")
    markdown = render_state_evolution_audit_markdown(payload)
    assert "State-Evolution Audit" in markdown
    assert "condition_number" in markdown
    assert "stability" in markdown


def test_guided_mode_smoke_payload_requires_three_consecutive_active_phase_runs(tmp_path: Path) -> None:
    run_specs = [
        ("run1", True, True, "", []),
        ("run2", True, True, "", []),
        ("run3", False, False, "arm_failed", ["mode_not_confirmed:GUIDED_NOGPS"]),
        ("run4", True, True, "", []),
    ]
    run_dirs = []
    for run_id, experiment_started, active_phase_present, failure_reason, anomalies in run_specs:
        run_dir = tmp_path / run_id
        write_yaml(
            run_dir / "manifest.yaml",
            {
                "run_id": run_id,
                "flight_mode": "GUIDED_NOGPS",
                "status": "completed" if experiment_started else "failed",
                "failure_reason": failure_reason,
                "research_acceptance": "accepted" if experiment_started and active_phase_present else "rejected",
                "research_rejection_reasons": [] if experiment_started and active_phase_present else ["experiment_not_started"],
                "anomaly_summary": anomalies,
                "runtime_report": {"completion_reason": failure_reason or "profile_completed"},
                "data_quality": {
                    "acceptance": {
                        "experiment_started": experiment_started,
                        "active_phase_present": active_phase_present,
                    }
                },
            },
        )
        run_dirs.append(run_dir)

    payload = build_guided_mode_smoke_payload(run_dirs, target_mode="GUIDED_NOGPS", target_consecutive_runs=3)
    assert payload["status"] == "smoke_available"
    assert payload["passed"] is False
    assert payload["longest_consecutive_active_phase_runs"] == 2
    assert payload["runs"][2]["mode_entry_result"] == "mode_not_confirmed"
    markdown = render_guided_mode_smoke_markdown(payload)
    assert "GUIDED_NOGPS Smoke" in markdown
    assert "longest_consecutive_active_phase_runs: 2" in markdown


def test_matrix_gallery_generates_all_supported_heatmaps(tmp_path: Path) -> None:
    study_dir = tmp_path / "20260409_200000_px4_real_broad_ablation"
    _write_summary(
        study_dir / "summary" / "study_summary.json",
        {
            "ranking": [
                {
                    "x_schema": "commands_plus_state",
                    "y_schema": "delta_state",
                    "model_name": "ols_affine",
                    "pooling_mode": "pooled",
                    "median_test_r2": 0.91,
                    "median_test_mse": 0.01,
                    "median_test_mae": 0.02,
                    "support": "supported",
                },
                {
                    "x_schema": "full_augmented",
                    "y_schema": "next_raw_state",
                    "model_name": "ridge_affine",
                    "pooling_mode": "stratified",
                    "median_test_r2": 0.88,
                    "median_test_mse": 0.02,
                    "median_test_mae": 0.03,
                    "support": "supported",
                },
            ]
        },
    )
    _write_sparsity_mask(
        study_dir / "fits" / "commands_plus_state__delta_state__pooled" / "ols_affine" / "matrix_f.csv",
        [("command_roll", "delta_state_roll"), ("roll", "delta_state_roll")],
    )
    _write_sparsity_mask(
        study_dir / "fits" / "full_augmented__next_raw_state__stratified" / "ridge_affine" / "matrix_f.csv",
        [("command_pitch", "future_state_pitch"), ("pitch", "future_state_pitch")],
    )

    payload = build_matrix_gallery_payload(study_dir)
    assert payload["status"] == "gallery_available"
    assert payload["supported_count"] == 2
    assert payload["entries"][0]["abs_heatmap"].endswith(".png")
    markdown = render_matrix_gallery_markdown(payload)
    assert "Matrix Gallery" in markdown
    assert "supported_count: 2" in markdown

    write_matrix_gallery_artifacts(
        study_dir,
        report_path=study_dir / "reports" / "matrix_gallery.md",
        summary_path=study_dir / "summary" / "matrix_gallery.json",
    )
    assert (study_dir / "reports" / "matrix_gallery.md").exists()
    assert (study_dir / "summary" / "matrix_gallery.json").exists()
    assert list((study_dir / "fits").rglob("matrix_heatmap_abs.png"))
    assert list((study_dir / "fits").rglob("matrix_heatmap_signed.png"))


def test_matrix_gallery_reports_when_no_supported_results(tmp_path: Path) -> None:
    study_dir = tmp_path / "20260409_200100_px4_real_broad_ablation"
    _write_summary(
        study_dir / "summary" / "study_summary.json",
        {
            "ranking": [
                {
                    "x_schema": "commands_only",
                    "y_schema": "delta_state",
                    "model_name": "ols_affine",
                    "pooling_mode": "pooled",
                    "median_test_r2": 0.21,
                    "median_test_mse": 0.2,
                    "median_test_mae": 0.1,
                    "support": "unsupported",
                }
            ]
        },
    )

    payload = build_matrix_gallery_payload(study_dir)
    assert payload["status"] == "no_supported_results"
    markdown = render_matrix_gallery_markdown(payload)
    assert "no_supported_results" in markdown


def test_scenario_generalization_payload_distinguishes_global_vs_local_support(tmp_path: Path) -> None:
    study_dir = tmp_path / "20260410_010000_px4_real_generalization_ablation"
    manifest = {
        "study_name": "px4_real_generalization_ablation",
        "source_scenarios": ["dynamic", "nominal", "throttle_biased"],
    }
    write_yaml(study_dir / "manifest.yaml", manifest)
    fit_root = study_dir / "fits"
    _write_metrics(
        fit_root / "commands_only__actuator_response__pooled" / "lasso_affine" / "metrics.json",
        x_schema="commands_only",
        y_schema="actuator_response",
        pooling_mode="pooled",
        model_name="lasso_affine",
        median_test_r2=0.94,
        coefficient_stability=0.81,
        effective_condition_number=3.2e5,
        extra_fields={
            "support": "supported",
            "scenario_consistency": 0.82,
            "scenario_subgroup_metrics": {
                "dynamic": {"r2": 0.88},
                "nominal": {"r2": 0.93},
                "throttle_biased": {"r2": 0.90},
            },
        },
    )
    _write_metrics(
        fit_root / "commands_plus_state__next_raw_state__pooled" / "ols_affine" / "metrics.json",
        x_schema="commands_plus_state",
        y_schema="next_raw_state",
        pooling_mode="pooled",
        model_name="ols_affine",
        median_test_r2=0.90,
        coefficient_stability=0.73,
        effective_condition_number=7.1e5,
        extra_fields={
            "support": "supported",
            "scenario_consistency": 0.41,
            "scenario_subgroup_metrics": {
                "dynamic": {"r2": 0.92},
                "nominal": {"r2": 0.86},
                "throttle_biased": {"r2": 0.55},
            },
        },
    )
    _write_metrics(
        fit_root / "full_augmented__future_state_horizon__stratified" / "ridge_affine" / "metrics.json",
        x_schema="full_augmented",
        y_schema="future_state_horizon",
        pooling_mode="stratified",
        model_name="ridge_affine",
        median_test_r2=0.58,
        coefficient_stability=0.40,
        effective_condition_number=9.0e6,
        extra_fields={
            "support": "partial",
            "scenario_consistency": 0.25,
            "scenario_subgroup_metrics": {
                "dynamic": {"r2": 0.62},
                "nominal": {"r2": 0.57},
                "throttle_biased": {"r2": 0.49},
            },
        },
    )

    payload = build_scenario_generalization_payload(study_dir, manifest["study_name"], manifest)
    assert payload["status"] == "scenario_available"
    statuses = {entry["generalization_status"] for entry in payload["entries"]}
    assert "generalized_supported" in statuses
    assert "supported_but_local" in statuses
    assert "not_generalized" in statuses
    markdown = render_scenario_generalization_markdown(payload)
    assert "Scenario Generalization" in markdown
    assert "generalized_supported" in markdown
    assert "supported_but_local" in markdown


def test_backend_compare_payload_falls_back_to_existing_study_artifacts(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(study_artifacts, "STUDY_ARTIFACT_ROOT", tmp_path)

    px4_study_name = "px4_real_broad_ablation"
    ap_study_name = "ardupilot_real_broad_ablation"
    px4_previous = tmp_path / f"20260408_060000_{px4_study_name}"
    px4_current = tmp_path / f"20260409_060000_{px4_study_name}"
    ap_previous = tmp_path / f"20260408_070000_{ap_study_name}"
    ap_current = tmp_path / f"20260409_070000_{ap_study_name}"

    baseline_specs = [
        (px4_previous, px4_study_name, ["OFFBOARD_ATTITUDE", "POSCTL"], 6, 0.9980, 920000.0),
        (px4_current, px4_study_name, ["OFFBOARD_ATTITUDE", "POSCTL"], 10, 0.9990, 910000.0),
        (ap_previous, ap_study_name, ["GUIDED_NOGPS", "STABILIZE"], 6, 0.9975, 940000.0),
        (ap_current, ap_study_name, ["GUIDED_NOGPS", "STABILIZE"], 10, 0.9985, 930000.0),
    ]
    for study_dir, study_name, modes, accepted_count, r2, condition in baseline_specs:
        write_yaml(
            study_dir / "manifest.yaml",
            {
                "study_name": study_name,
                "study_id": study_dir.name,
                "source_backends": ["px4"] if study_name.startswith("px4") else ["ardupilot"],
                "source_modes": modes,
                "source_config_profiles": [f"{study_name}_{mode.lower()}" for mode in modes],
            },
        )
        write_yaml(
            study_dir / "prepared" / "schema_inventory.yaml",
            {
                "run_count": accepted_count,
                "data_quality": {"accepted_run_count": accepted_count},
            },
        )
        best = _fake_combo("commands_plus_state_history", "next_raw_state", "ols_affine", "pooled", r2=r2, condition=condition)
        supported = {
            "x_schema": "commands_plus_state_history",
            "y_schema": "next_raw_state",
            "model_name": "ols_affine",
            "pooling_mode": "pooled",
            "median_test_r2": r2,
            "effective_condition_number": condition,
            "support": "supported",
        }
        _write_summary(study_dir / "summary" / "study_summary.json", {"best_result": best, "ranking": [supported]})
        _write_sparsity_mask(
            study_dir / "fits" / "commands_plus_state_history__next_raw_state__pooled" / "ols_affine" / "sparsity_mask.csv",
            [("command_roll", "future_state_roll"), ("roll", "future_state_roll")],
        )

    raw_dir = tmp_path / "raw"
    px4_runs = [
        _write_diagnostic_run(raw_dir, run_id="px4_roll_small", mode="POSCTL", axis="roll", tier="small", acceptance="accepted", reasons=[]),
        _write_diagnostic_run(raw_dir, run_id="px4_roll_medium", mode="POSCTL", axis="roll", tier="medium", acceptance="accepted", reasons=[]),
        _write_diagnostic_run(raw_dir, run_id="px4_roll_large", mode="POSCTL", axis="roll", tier="large", acceptance="accepted", reasons=[]),
        _write_diagnostic_run(raw_dir, run_id="px4_throttle_small", mode="POSCTL", axis="throttle", tier="small", acceptance="accepted", reasons=[]),
        _write_diagnostic_run(raw_dir, run_id="px4_throttle_medium", mode="POSCTL", axis="throttle", tier="medium", acceptance="accepted", reasons=[]),
        _write_diagnostic_run(raw_dir, run_id="px4_throttle_large", mode="POSCTL", axis="throttle", tier="large", acceptance="accepted", reasons=[]),
    ]
    ap_runs = [
        _write_diagnostic_run(raw_dir, run_id="ap_roll_small", mode="STABILIZE", axis="roll", tier="small", acceptance="accepted", reasons=[]),
        _write_diagnostic_run(raw_dir, run_id="ap_roll_medium", mode="STABILIZE", axis="roll", tier="medium", acceptance="accepted", reasons=[]),
        _write_diagnostic_run(raw_dir, run_id="ap_roll_large", mode="STABILIZE", axis="roll", tier="large", acceptance="accepted", reasons=[]),
        _write_diagnostic_run(
            raw_dir,
            run_id="ap_throttle_small",
            mode="STABILIZE",
            axis="throttle",
            tier="small",
            acceptance="rejected",
            reasons=["insufficient_active_nonzero_command_samples"],
        ),
    ]

    px4_diag_dir = tmp_path / "20260409_080000_px4_diagnostic_axis_matrix_balanced"
    ap_diag_dir = tmp_path / "20260409_090000_ardupilot_diagnostic_axis_matrix_balanced"
    write_yaml(
        px4_diag_dir / "manifest.yaml",
        {
            "study_name": "px4_diagnostic_axis_matrix_balanced",
            "source_run_dirs": [str(path) for path in px4_runs],
        },
    )
    write_yaml(
        ap_diag_dir / "manifest.yaml",
        {
            "study_name": "ardupilot_diagnostic_axis_matrix_balanced",
            "source_run_dirs": [str(path) for path in ap_runs],
        },
    )
    _write_summary(
        px4_current / "summary" / "scenario_generalization.json",
        {
            "status": "scenario_available",
            "counts": {"generalized_supported": 5, "supported_but_local": 1, "not_generalized": 2},
            "entries": [
                {
                    "x_schema": "commands_plus_state_history",
                    "y_schema": "next_raw_state",
                    "model_name": "ols_affine",
                    "pooling_mode": "pooled",
                    "generalization_status": "generalized_supported",
                }
            ],
            "conclusion": "px4 baseline generalizes",
        },
    )
    _write_summary(
        ap_current / "summary" / "scenario_generalization.json",
        {
            "status": "scenario_available",
            "counts": {"generalized_supported": 1, "supported_but_local": 0, "not_generalized": 7},
            "entries": [
                {
                    "x_schema": "commands_only",
                    "y_schema": "actuator_response",
                    "model_name": "ols_affine",
                    "pooling_mode": "pooled",
                    "generalization_status": "generalized_supported",
                }
            ],
            "conclusion": "ardupilot baseline generalizes narrowly",
        },
    )
    _write_summary(
        px4_diag_dir / "summary" / "scenario_generalization.json",
        {
            "status": "scenario_available",
            "counts": {"generalized_supported": 7, "supported_but_local": 0, "not_generalized": 3},
            "entries": [
                {
                    "x_schema": "full_augmented",
                    "y_schema": "next_raw_state",
                    "model_name": "ridge_affine",
                    "pooling_mode": "stratified",
                    "generalization_status": "generalized_supported",
                }
            ],
            "conclusion": "px4 diagnostic generalizes",
        },
    )
    _write_summary(
        ap_diag_dir / "summary" / "scenario_generalization.json",
        {
            "status": "scenario_available",
            "counts": {"generalized_supported": 1, "supported_but_local": 0, "not_generalized": 9},
            "entries": [
                {
                    "x_schema": "commands_only",
                    "y_schema": "actuator_response",
                    "model_name": "ridge_affine",
                    "pooling_mode": "pooled",
                    "generalization_status": "generalized_supported",
                }
            ],
            "conclusion": "ardupilot diagnostic generalizes narrowly",
        },
    )

    payload = build_backend_compare_payload(px4_current, ap_current, px4_diag_dir, ap_diag_dir)
    assert payload["status"] == "compare_available"
    assert payload["comparison"]["both_baselines_stable"] is True
    assert payload["comparison"]["throttle_boundary_consistent"] is False
    assert payload["comparison"]["difference_driver"] == "backend_difference_more_likely"
    assert payload["comparison"]["generalization_difference_driver"] == "both_support_cross_scenario_linearity_but_px4_is_broader"
    assert payload["px4"]["baseline"]["scenario_generalization"]["counts"]["generalized_supported"] == 5
    markdown = render_backend_compare_markdown(payload)
    assert "Backend Compare" in markdown
    assert "Scenario Generalization" in markdown
    assert "difference_driver: `backend_difference_more_likely`" in markdown

    study_dir = run_backend_compare(px4_current, ap_current, px4_diag_dir, ap_diag_dir, output_root=tmp_path / "compare")
    assert (study_dir / "reports/backend_compare.md").exists()
    assert (study_dir / "summary/backend_compare.json").exists()
