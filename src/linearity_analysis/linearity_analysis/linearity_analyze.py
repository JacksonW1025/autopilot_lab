from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from linearity_core.config import AblationPlan, StudyConfig, load_ablation_plan, load_study_config
from linearity_core.dataset import PreparedSampleTable, build_prepared_sample_table, prepared_sample_table_fieldnames
from linearity_core.fit import _consistency_score, _group_consistency, fit_schema_combo
from linearity_core.io import ensure_study_directories, read_rows_csv, read_yaml, write_json, write_rows_csv, write_yaml
from linearity_core.research_contract import manifest_acceptance_state
from linearity_core.report import render_comparison_markdown, render_summary_markdown, summarize_results
from linearity_core.schemas import available_x_schemas, available_y_schemas, build_schema_matrices
from linearity_core.study_artifacts import (
    build_baseline_stability_payload,
    build_diagnostic_gate_payload,
    build_scenario_generalization_payload,
    build_state_evolution_audit_payload,
    render_baseline_stability_markdown,
    render_diagnostic_gate_markdown,
    render_scenario_generalization_markdown,
    render_state_evolution_audit_markdown,
)
from linearity_analysis.matrix_gallery import write_matrix_gallery_artifacts


def _discover_run_dirs_from_study_dir(path: Path) -> list[Path]:
    if (path / "manifest.yaml").exists():
        return [path]
    return sorted(child for child in path.iterdir() if child.is_dir() and (child / "manifest.yaml").exists())


def _load_run_dirs(args: argparse.Namespace) -> list[Path]:
    run_dirs: list[Path] = []
    for value in args.run_dirs or []:
        run_dirs.append(Path(value).expanduser().resolve())
    if args.study_dir:
        run_dirs.extend(_discover_run_dirs_from_study_dir(Path(args.study_dir).expanduser().resolve()))
    if args.runs_manifest:
        manifest_path = Path(args.runs_manifest).expanduser().resolve()
        if manifest_path.suffix.lower() == ".csv":
            rows = read_rows_csv(manifest_path)
            for row in rows:
                run_dir = row.get("run_dir") or row.get("artifact_dir")
                status = str(row.get("status", "")).strip().lower()
                if not run_dir:
                    continue
                if status and status not in {"completed", "success"}:
                    continue
                run_dirs.append(Path(run_dir).expanduser().resolve())
    deduped: list[Path] = []
    seen: set[Path] = set()
    for path in run_dirs:
        if path not in seen:
            deduped.append(path)
            seen.add(path)
    return deduped


def _filter_run_dirs(
    run_dirs: list[Path],
    *,
    include_rejected_runs: bool,
) -> tuple[list[Path], list[dict[str, Any]]]:
    selected: list[Path] = []
    excluded: list[dict[str, Any]] = []
    for path in run_dirs:
        manifest = read_yaml(path / "manifest.yaml")
        acceptance_state = manifest_acceptance_state(manifest)
        if include_rejected_runs or acceptance_state == "accepted":
            selected.append(path)
            continue
        excluded.append(
            {
                "run_dir": str(path),
                "run_id": manifest.get("run_id", path.name),
                "backend": manifest.get("backend", ""),
                "research_tier": manifest.get("research_tier", ""),
                "research_acceptance": manifest.get("research_acceptance", ""),
                "filter_reason": "legacy_manifest" if acceptance_state == "legacy" else "research_rejected",
                "research_rejection_reasons": list(manifest.get("research_rejection_reasons", []) or []),
            }
        )
    return selected, excluded


def _drop_zero_variance_features(matrices, run_ids: list[str]) -> tuple[np.ndarray, list[str], np.ndarray, np.ndarray]:
    if matrices.X.size == 0:
        return matrices.X, matrices.feature_names, matrices.valid_mask, np.asarray([], dtype=bool)
    valid_rows = matrices.valid_mask.copy()
    if not np.any(valid_rows):
        return matrices.X[:, :0], [], valid_rows, np.zeros(len(matrices.feature_names), dtype=bool)
    variance = np.nanvar(matrices.X[valid_rows], axis=0)
    keep_mask = np.isfinite(variance) & (variance > 0.0)
    if np.sum(keep_mask) == 0:
        return matrices.X[:, :0], [], valid_rows, keep_mask
    return matrices.X[:, keep_mask], [name for name, keep in zip(matrices.feature_names, keep_mask) if keep], valid_rows, keep_mask


def _subset_result_rows(table: PreparedSampleTable, matrices, valid_mask: np.ndarray) -> tuple[list[str], list[str], list[str], list[str]]:
    run_ids = table.string_column("run_id")
    backends = table.string_column("backend")
    modes = table.string_column("mode")
    scenarios = table.string_column("scenario")
    return run_ids, backends, modes, scenarios


def _save_matrix_csv(path: Path, row_names: list[str], column_names: list[str], matrix: np.ndarray) -> None:
    rows = []
    for row_name, values in zip(row_names, matrix):
        row = {"feature": row_name}
        for column_name, value in zip(column_names, values):
            row[column_name] = float(value)
        rows.append(row)
    write_rows_csv(path, rows, fieldnames=["feature", *column_names])


def _save_bias_csv(path: Path, response_names: list[str], bias: np.ndarray) -> None:
    row = {name: float(value) for name, value in zip(response_names, bias)}
    write_rows_csv(path, [row], fieldnames=response_names)


def _run_stratified_fit(
    table: PreparedSampleTable,
    matrices,
    config: StudyConfig,
    model_name: str,
    stratify_by: list[str],
) -> dict[str, Any]:
    base_run_ids = table.string_column("run_id")
    base_backends = table.string_column("backend")
    base_modes = table.string_column("mode")
    base_scenarios = table.string_column("scenario")
    grouping_keys = stratify_by or ["backend", "mode"]
    group_index: dict[tuple[str, ...], list[int]] = {}
    for index, row in enumerate(table.rows):
        key = tuple(str(row.get(name, "")) for name in grouping_keys)
        group_index.setdefault(key, []).append(index)

    group_results: list[dict[str, Any]] = []
    coef_blocks: list[np.ndarray] = []
    bias_blocks: list[np.ndarray] = []
    mask_blocks: list[np.ndarray] = []
    residual_rows: list[dict[str, Any]] = []
    for key, indices in sorted(group_index.items()):
        subset_mask = np.zeros(len(table.rows), dtype=bool)
        subset_mask[indices] = True
        combined_mask = matrices.valid_mask & subset_mask
        if np.sum(combined_mask) < 10:
            continue
        subset_run_ids = [base_run_ids[index] for index in indices]
        subset_backends = [base_backends[index] for index in indices]
        subset_modes = [base_modes[index] for index in indices]
        subset_scenarios = [base_scenarios[index] for index in indices]
        local_matrices = type(matrices)(
            X=matrices.X[indices],
            Y=matrices.Y[indices],
            feature_names=matrices.feature_names,
            response_names=matrices.response_names,
            valid_mask=matrices.valid_mask[indices],
            schema_metadata=dict(matrices.schema_metadata),
        )
        model_result = fit_schema_combo(subset_run_ids, subset_backends, subset_modes, subset_scenarios, local_matrices, config, model_name)
        group_results.append({"group_key": list(key), "summary": model_result.summary})
        coef_blocks.append(model_result.coefficient_matrix)
        bias_blocks.append(model_result.bias_vector)
        mask_blocks.append(model_result.sparsity_mask)
        residual_rows.extend(model_result.residual_rows)

    if not group_results:
        raise ValueError("stratified fitting 没有足够样本")

    stacked_coef = np.stack(coef_blocks, axis=0)
    stacked_bias = np.stack(bias_blocks, axis=0)
    stacked_mask = np.stack(mask_blocks, axis=0)
    valid_indices = np.flatnonzero(matrices.valid_mask)
    X_valid = matrices.X[valid_indices]
    Y_valid = matrices.Y[valid_indices]
    backends_valid = [base_backends[index] for index in valid_indices]
    modes_valid = [base_modes[index] for index in valid_indices]
    scenarios_valid = [base_scenarios[index] for index in valid_indices]
    all_indices = np.arange(X_valid.shape[0], dtype=int)
    mean_coef = np.mean(stacked_coef, axis=0)
    mean_bias = np.mean(stacked_bias, axis=0)
    backend_consistency = _group_consistency("backend", backends_valid, all_indices, Y_valid, mean_coef, mean_bias, X_valid)
    mode_consistency = _group_consistency("mode", modes_valid, all_indices, Y_valid, mean_coef, mean_bias, X_valid)
    scenario_subgroup_metrics = _group_consistency(
        "scenario",
        scenarios_valid,
        all_indices,
        Y_valid,
        mean_coef,
        mean_bias,
        X_valid,
    )
    scenario_consistency = _consistency_score(scenario_subgroup_metrics)
    aggregate_summary = {
        "model_name": model_name,
        "group_results": group_results,
        "median_test_r2": float(np.median([item["summary"]["median_test_r2"] for item in group_results])),
        "median_test_mse": float(np.median([item["summary"]["median_test_mse"] for item in group_results])),
        "median_test_mae": float(np.median([item["summary"]["median_test_mae"] for item in group_results])),
        "coefficient_stability": float(np.mean([item["summary"]["coefficient_stability"] for item in group_results])),
        "nonzero_count": int(np.sum(np.mean(stacked_mask, axis=0) >= 0.60)),
        "sparsity_ratio": float(1.0 - (np.sum(np.mean(stacked_mask, axis=0) >= 0.60) / max(1, stacked_mask.shape[1] * stacked_mask.shape[2]))),
        "raw_condition_number": float(np.median([item["summary"].get("raw_condition_number", np.nan) for item in group_results])),
        "effective_condition_number": float(np.median([item["summary"].get("effective_condition_number", np.nan) for item in group_results])),
        "condition_number": float(np.median([item["summary"]["condition_number"] for item in group_results])),
        "raw_singular_values": group_results[0]["summary"].get("raw_singular_values", []),
        "singular_values": group_results[0]["summary"].get("singular_values", []),
        "effective_singular_values": group_results[0]["summary"].get("effective_singular_values", []),
        "conditioning_pruned_features": sorted({name for item in group_results for name in item["summary"].get("conditioning_pruned_features", [])}),
        "conditioning_baseline_drops": sorted({name for item in group_results for name in item["summary"].get("conditioning_baseline_drops", [])}),
        "conditioning_extra_pruned_features": sorted(
            {name for item in group_results for name in item["summary"].get("conditioning_extra_pruned_features", [])}
        ),
        "backend_consistency": backend_consistency,
        "mode_consistency": mode_consistency,
        "scenario_consistency": scenario_consistency,
        "scenario_subgroup_metrics": scenario_subgroup_metrics,
        "top_influential": {},
        "selection_frequency": np.mean(stacked_mask, axis=0).tolist(),
    }
    return {
        "summary": aggregate_summary,
        "coefficient_matrix": mean_coef,
        "bias_vector": mean_bias,
        "sparsity_mask": (np.mean(stacked_mask, axis=0) >= 0.60).astype(float),
        "residual_rows": residual_rows,
    }


def _skip_payload(
    x_schema: str,
    y_schema: str,
    pooling_mode: str,
    model_name: str,
    reason: str,
    matrices,
    *,
    valid_row_count: int,
) -> dict[str, Any]:
    return {
        "x_schema": x_schema,
        "y_schema": y_schema,
        "pooling_mode": pooling_mode,
        "model_name": model_name,
        "summary": {
            "status": "skipped",
            "skip_reason": reason,
            "median_test_r2": float("-inf"),
            "median_test_mse": float("inf"),
            "median_test_mae": float("inf"),
            "coefficient_stability": 0.0,
            "nonzero_count": 0,
            "sparsity_ratio": 1.0,
            "condition_number": float("inf"),
            "feature_names": matrices.feature_names,
            "response_names": matrices.response_names,
            "schema_metadata": matrices.schema_metadata,
            "valid_row_count": valid_row_count,
        },
    }


def run_analysis(
    run_dirs: list[Path],
    config: StudyConfig,
    *,
    ablation_plan: AblationPlan | None = None,
    output_root: Path | None = None,
    include_rejected_runs: bool = False,
) -> Path:
    if not run_dirs:
        raise ValueError("没有可分析的 run_dirs")
    filtered_run_dirs, excluded_runs = _filter_run_dirs(run_dirs, include_rejected_runs=include_rejected_runs)
    if not filtered_run_dirs:
        raise ValueError("没有可分析的 accepted run_dirs；如需调试 rejected/legacy runs，请显式开启 include_rejected_runs。")

    study_name = ablation_plan.output_study_name if ablation_plan and ablation_plan.output_study_name else config.study_name
    study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_{study_name}"
    paths = ensure_study_directories(study_id, root=output_root)
    table, inventory = build_prepared_sample_table(filtered_run_dirs, config)
    write_rows_csv(paths["sample_table_path"], table.to_csv_rows(), fieldnames=prepared_sample_table_fieldnames(table.rows))

    plan = ablation_plan
    x_schemas = plan.x_schemas if plan else [config.x_schema]
    y_schemas = plan.y_schemas if plan else [config.y_schema]
    models = plan.models if plan else config.resolved_models()
    pooling_modes = plan.pooling_modes if plan else ([config.pooling_mode] if config.pooling_mode != "compare_both" else ["pooled", "stratified"])
    stratify_by = plan.stratify_by if plan and plan.stratify_by else config.stratify_by

    schema_inventory = {
        **inventory,
        "analysis_filters": {
            "include_rejected_runs": include_rejected_runs,
        },
        "selected_run_dirs": [str(path) for path in filtered_run_dirs],
        "excluded_runs": excluded_runs,
        "requested_x_schemas": x_schemas,
        "requested_y_schemas": y_schemas,
        "models": models,
        "pooling_modes": pooling_modes,
        "available_x_schemas": available_x_schemas(),
        "available_y_schemas": available_y_schemas(),
    }
    write_yaml(paths["schema_inventory_path"], schema_inventory)

    results: list[dict[str, Any]] = []
    skipped_results: list[dict[str, Any]] = []
    appendix_x_schemas = set(plan.reporting.get("appendix_x_schemas", [])) if plan else set()
    for pooling_mode in pooling_modes:
        for x_schema in x_schemas:
            for y_schema in y_schemas:
                matrices = build_schema_matrices(table, config, x_schema, y_schema)
                run_ids, backends, modes, scenarios = _subset_result_rows(table, matrices, matrices.valid_mask)
                X, feature_names, valid_mask, keep_mask = _drop_zero_variance_features(matrices, run_ids)
                matrices = type(matrices)(
                    X=X,
                    Y=matrices.Y,
                    feature_names=feature_names,
                    response_names=matrices.response_names,
                    valid_mask=valid_mask,
                    schema_metadata={**matrices.schema_metadata, "dropped_zero_variance_features": [name for name, keep in zip(matrices.feature_names, keep_mask) if not keep]},
                )
                valid_row_count = int(np.sum(matrices.valid_mask))
                skip_reason = ""
                if matrices.Y.size == 0 or not matrices.response_names:
                    if y_schema == "actuator_response":
                        skip_reason = "actuator_response_unavailable"
                    elif y_schema in {"future_state_horizon", "window_summary_response"}:
                        skip_reason = "future_horizon_unavailable"
                    else:
                        skip_reason = "response_unavailable"
                elif matrices.X.shape[1] == 0:
                    skip_reason = "no_identifiable_features"
                elif valid_row_count < 10:
                    if y_schema == "actuator_response":
                        skip_reason = "actuator_response_unavailable"
                    elif y_schema in {"future_state_horizon", "window_summary_response"}:
                        skip_reason = "future_horizon_unavailable"
                    else:
                        skip_reason = "insufficient_valid_rows"
                if skip_reason:
                    for model_name in models:
                        skipped_results.append(_skip_payload(x_schema, y_schema, pooling_mode, model_name, skip_reason, matrices, valid_row_count=valid_row_count))
                    continue

                combo_dir = paths["fits_dir"] / f"{x_schema}__{y_schema}__{pooling_mode}"
                combo_dir.mkdir(parents=True, exist_ok=True)
                for model_name in models:
                    model_dir = combo_dir / model_name
                    model_dir.mkdir(parents=True, exist_ok=True)
                    if pooling_mode == "stratified":
                        fitted = _run_stratified_fit(table, matrices, config, model_name, stratify_by)
                        summary = fitted["summary"]
                        coefficient_matrix = fitted["coefficient_matrix"]
                        bias_vector = fitted["bias_vector"]
                        sparsity_mask = fitted["sparsity_mask"]
                        residual_rows = fitted["residual_rows"]
                    else:
                        model_result = fit_schema_combo(run_ids, backends, modes, scenarios, matrices, config, model_name)
                        summary = model_result.summary
                        coefficient_matrix = model_result.coefficient_matrix
                        bias_vector = model_result.bias_vector
                        sparsity_mask = model_result.sparsity_mask
                        residual_rows = model_result.residual_rows

                    summary_payload = {
                        "x_schema": x_schema,
                        "y_schema": y_schema,
                        "pooling_mode": pooling_mode,
                        "model_name": model_name,
                        "feature_names": matrices.feature_names,
                        "response_names": matrices.response_names,
                        "schema_metadata": matrices.schema_metadata,
                        **summary,
                    }
                    _save_matrix_csv(model_dir / "matrix_f.csv", matrices.feature_names, matrices.response_names, coefficient_matrix)
                    _save_bias_csv(model_dir / "bias_b.csv", matrices.response_names, bias_vector)
                    _save_matrix_csv(model_dir / "sparsity_mask.csv", matrices.feature_names, matrices.response_names, sparsity_mask)
                    write_json(model_dir / "metrics.json", summary_payload)
                    write_rows_csv(model_dir / "residuals.csv", residual_rows, fieldnames=list(residual_rows[0].keys()) if residual_rows else [])
                    results.append(
                        {
                            "x_schema": x_schema,
                            "y_schema": y_schema,
                            "pooling_mode": pooling_mode,
                            "model_name": model_name,
                            "appendix": x_schema in appendix_x_schemas,
                            "summary": summary_payload,
                        }
                    )

    summary = summarize_results(results, skipped_results=skipped_results, data_quality=inventory.get("data_quality", {}))
    paths["summary_report_path"].write_text(render_summary_markdown(study_name, summary, results, skipped_results=skipped_results), encoding="utf-8")
    paths["comparison_report_path"].write_text(render_comparison_markdown(study_name, results, skipped_results=skipped_results), encoding="utf-8")
    write_json(paths["summary_json_path"], {"study_name": study_name, **summary})
    study_manifest = {
        "study_name": study_name,
        "study_id": study_id,
        "source_run_dirs": [str(path) for path in run_dirs],
        "source_backends": sorted(set(table.string_column("backend"))),
        "source_modes": sorted(set(mode for mode in table.string_column("mode") if mode)),
        "source_scenarios": sorted(set(scenario for scenario in table.string_column("scenario") if scenario)),
        "source_config_profiles": sorted(set(profile for profile in table.string_column("config_profile") if profile)),
        "source_seeds": sorted(set(int(seed) for seed in table.column("seed"))) if table.rows else [],
        "report_matrix": {
            "x_schemas": x_schemas,
            "y_schemas": y_schemas,
            "models": models,
            "pooling_modes": pooling_modes,
            "stratify_by": stratify_by,
            "repeat_count": config.repeat_count,
            "appendix_x_schemas": sorted(appendix_x_schemas),
        },
        "summary": summary,
    }
    write_yaml(paths["manifest_path"], study_manifest)

    baseline_stability = build_baseline_stability_payload(paths["base_dir"], study_name, summary, schema_inventory, study_manifest)
    paths["baseline_stability_report_path"].write_text(render_baseline_stability_markdown(baseline_stability), encoding="utf-8")
    write_json(paths["baseline_stability_json_path"], baseline_stability)

    state_evolution_audit = build_state_evolution_audit_payload(paths["base_dir"], study_name, schema_inventory, study_manifest)
    paths["state_evolution_audit_report_path"].write_text(
        render_state_evolution_audit_markdown(state_evolution_audit),
        encoding="utf-8",
    )
    write_json(paths["state_evolution_audit_json_path"], state_evolution_audit)

    scenario_generalization = build_scenario_generalization_payload(paths["base_dir"], study_name, study_manifest)
    paths["scenario_generalization_report_path"].write_text(
        render_scenario_generalization_markdown(scenario_generalization),
        encoding="utf-8",
    )
    write_json(paths["scenario_generalization_json_path"], scenario_generalization)

    diagnostic_gate = build_diagnostic_gate_payload(run_dirs)
    paths["diagnostic_gate_report_path"].write_text(render_diagnostic_gate_markdown(diagnostic_gate), encoding="utf-8")
    write_json(paths["diagnostic_gate_json_path"], diagnostic_gate)
    write_matrix_gallery_artifacts(
        paths["base_dir"],
        report_path=paths["matrix_gallery_report_path"],
        summary_path=paths["matrix_gallery_json_path"],
    )
    return paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="分析一个或多个 raw run，比较不同 X/Y schema 下的全局线性拟合与稀疏性。")
    parser.add_argument("--config", type=Path, required=True, help="study config YAML 路径。")
    parser.add_argument("--run-dir", action="append", dest="run_dirs", help="raw run 目录，可重复。")
    parser.add_argument("--study-dir", type=Path, help="包含多个 raw run 子目录的目录。")
    parser.add_argument("--runs-manifest", type=Path, help="CSV manifest；至少包含 run_dir 列。")
    parser.add_argument("--ablation-plan", type=Path, help="可选 ablation plan YAML。")
    parser.add_argument("--output-root", type=Path, default=None)
    parser.add_argument("--include-rejected-runs", action="store_true", help="调试时包含 rejected/legacy raw runs。")
    args = parser.parse_args(argv)

    config = load_study_config(args.config)
    plan = load_ablation_plan(args.ablation_plan) if args.ablation_plan else None
    run_dirs = _load_run_dirs(args)
    study_dir = run_analysis(
        run_dirs,
        config,
        ablation_plan=plan,
        output_root=args.output_root,
        include_rejected_runs=args.include_rejected_runs,
    )
    print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
