from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from .ab_fit_runner import IDENTIFICATION_ROOT, SCHEMA_INPUTS, WINDOW_MODES, fit_schema
from .artifacts import write_rows_csv, write_yaml


@dataclass(slots=True)
class RunFitEntry:
    run_id: str
    group_key: str
    scenario_label: str
    profile_type: str
    axis: str
    input_peak: float
    row_count: int
    result: Any


def _load_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _float_value(value: Any, default: float = math.nan) -> float:
    if value in ("", None):
        return default
    return float(value)


def _csv_value(value: Any) -> Any:
    if isinstance(value, (np.floating, float)) and math.isnan(float(value)):
        return ""
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def _finite_mean(values: list[float] | np.ndarray) -> float:
    array = np.asarray(values, dtype=float)
    finite = array[np.isfinite(array)]
    if finite.size == 0:
        return math.nan
    return float(np.mean(finite))


def _finite_std(values: list[float] | np.ndarray) -> float:
    array = np.asarray(values, dtype=float)
    finite = array[np.isfinite(array)]
    if finite.size == 0:
        return math.nan
    return float(np.std(finite, ddof=0))


def _latest_dataset_dir() -> Path:
    candidates = [path for path in IDENTIFICATION_ROOT.iterdir() if path.is_dir()]
    if not candidates:
        raise RuntimeError(f"未找到 identification dataset 目录: {IDENTIFICATION_ROOT}")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def _window_enabled(row: dict[str, Any], window_mode: str) -> bool:
    required_windows = WINDOW_MODES[window_mode]
    if not required_windows:
        return True
    return any(_float_value(row.get(window_key), 0.0) >= 0.5 for window_key in required_windows)


def _filter_rows(rows: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []
    for row in rows:
        if args.profile_type != "all" and row["profile_type"] != args.profile_type:
            continue
        if args.axis != "all" and row["axis"] != args.axis:
            continue
        if not _window_enabled(row, args.window_mode):
            continue
        dt_value = _float_value(row.get("dt_next_s"))
        if math.isnan(dt_value) or dt_value <= 0.0 or dt_value > args.max_dt:
            continue
        filtered.append(row)
    if not filtered:
        raise RuntimeError("过滤后没有剩余样本")
    return filtered


def _parse_signature(raw_value: str) -> dict[str, Any]:
    text = str(raw_value or "").strip()
    if not text:
        return {}
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _scenario_label(meta: dict[str, Any]) -> str:
    profile_type = str(meta.get("profile_type", "unknown"))
    axis = str(meta.get("axis", "unknown"))
    input_peak = _float_value(meta.get("input_peak"))
    parts = [profile_type, axis]
    if not math.isnan(input_peak):
        parts.append(f"{input_peak:.2f}")
    signature = _parse_signature(str(meta.get("config_signature", "")))
    profile_params = signature.get("profile_params", {})
    if isinstance(profile_params, dict):
        duration_s = _float_value(profile_params.get("duration_s"))
        pulse_width_s = _float_value(profile_params.get("pulse_width_s"))
        if not math.isnan(duration_s):
            parts.append(f"T{duration_s:.1f}s")
        if not math.isnan(pulse_width_s):
            parts.append(f"pw{pulse_width_s:.2f}s")
    return "/".join(parts)


def _term_kind(term_name: str, input_fields: tuple[str, ...]) -> str:
    if term_name == "intercept":
        return "intercept"
    if term_name in input_fields:
        return "input"
    return "state"


def _group_key(meta: dict[str, Any], group_field: str) -> str:
    value = str(meta.get(group_field, "")).strip()
    if value:
        return value
    fallback = str(meta.get("config_signature", "")).strip()
    return fallback or str(meta.get("run_id", "")).strip()


def _resolve_output_dir(dataset_dir: Path, explicit_output: str, schema: str) -> Path:
    if explicit_output:
        return Path(explicit_output).expanduser().resolve()
    stamp = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d_%H%M%S")
    return dataset_dir / f"uncertainty_{schema}_{stamp}"


def _mean_abs_input_standardized(result: Any) -> float:
    values: list[float] = []
    for feature_index, feature_name in enumerate(result.feature_names):
        if feature_name not in result.input_fields:
            continue
        for target_index in range(len(result.target_names)):
            value = float(result.standardized_coefficients[feature_index, target_index])
            if not math.isnan(value):
                values.append(abs(value))
    return float(np.mean(values)) if values else math.nan


def _fit_grouped_runs(
    filtered_rows: list[dict[str, Any]],
    metadata_by_run: dict[str, dict[str, Any]],
    args: argparse.Namespace,
) -> tuple[list[RunFitEntry], dict[str, list[dict[str, Any]]]]:
    rows_by_run: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in filtered_rows:
        run_id = str(row["run_id"])
        if run_id in metadata_by_run:
            rows_by_run[run_id].append(row)

    grouped_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    entries: list[RunFitEntry] = []
    for run_id, run_rows in rows_by_run.items():
        meta = metadata_by_run[run_id]
        group_key = _group_key(meta, args.group_field)
        grouped_rows[group_key].extend(run_rows)
        try:
            result = fit_schema(run_rows, args.schema, args.ridge_alpha)
        except RuntimeError:
            continue
        entries.append(
            RunFitEntry(
                run_id=run_id,
                group_key=group_key,
                scenario_label=_scenario_label(meta),
                profile_type=str(meta.get("profile_type", "")),
                axis=str(meta.get("axis", "")),
                input_peak=_float_value(meta.get("input_peak")),
                row_count=len(run_rows),
                result=result,
            )
        )
    return entries, grouped_rows


def _per_run_rows(entries: list[RunFitEntry]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entry in entries:
        rows.append(
            {
                "group_key": entry.group_key,
                "scenario_label": entry.scenario_label,
                "run_id": entry.run_id,
                "profile_type": entry.profile_type,
                "axis": entry.axis,
                "input_peak": _csv_value(entry.input_peak),
                "row_count": entry.row_count,
                "condition_number": _csv_value(entry.result.condition_number),
                "mean_train_rmse": _csv_value(float(np.nanmean(entry.result.train_rmse))),
                "mean_train_mae": _csv_value(float(np.nanmean(entry.result.train_mae))),
                "mean_rollout_rmse": _csv_value(float(np.nanmean(entry.result.rollout_rmse))),
                "mean_abs_input_standardized_coefficient": _csv_value(_mean_abs_input_standardized(entry.result)),
            }
        )
    rows.sort(key=lambda row: (str(row["scenario_label"]), str(row["run_id"])))
    return rows


def _scenario_overview_rows(
    args: argparse.Namespace,
    metadata_by_group: dict[str, dict[str, Any]],
    entries_by_group: dict[str, list[RunFitEntry]],
    pooled_results: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group_key, meta in metadata_by_group.items():
        group_entries = entries_by_group.get(group_key, [])
        if len(group_entries) < args.min_repeats or group_key not in pooled_results:
            continue
        pooled = pooled_results[group_key]
        mean_run_rollout = _finite_mean([_finite_mean(entry.result.rollout_rmse) for entry in group_entries])
        std_run_rollout = _finite_std([_finite_mean(entry.result.rollout_rmse) for entry in group_entries])
        mean_input_std = _finite_mean([_mean_abs_input_standardized(entry.result) for entry in group_entries])
        rows.append(
            {
                "group_key": group_key,
                "scenario_label": _scenario_label(meta),
                "profile_type": meta.get("profile_type", ""),
                "axis": meta.get("axis", ""),
                "input_peak": _csv_value(_float_value(meta.get("input_peak"))),
                "repeat_count": len(group_entries),
                "total_row_count": int(sum(entry.row_count for entry in group_entries)),
                "pooled_row_count": pooled.row_count,
                "mean_run_rollout_rmse": _csv_value(mean_run_rollout),
                "std_run_rollout_rmse": _csv_value(std_run_rollout),
                "pooled_mean_loo_rmse": _csv_value(_finite_mean(pooled.loo_rmse)),
                "pooled_mean_rollout_rmse": _csv_value(_finite_mean(pooled.rollout_rmse)),
                "mean_abs_input_standardized_coefficient": _csv_value(mean_input_std),
            }
        )
    rows.sort(
        key=lambda row: (
            float(row["input_peak"]) if row["input_peak"] != "" else math.inf,
            str(row["profile_type"]),
            str(row["axis"]),
        )
    )
    return rows


def _scenario_validation_rows(
    args: argparse.Namespace,
    metadata_by_group: dict[str, dict[str, Any]],
    entries_by_group: dict[str, list[RunFitEntry]],
    pooled_results: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group_key, pooled in pooled_results.items():
        group_entries = entries_by_group.get(group_key, [])
        if len(group_entries) < args.min_repeats:
            continue
        meta = metadata_by_group[group_key]
        for target_index, target_name in enumerate(pooled.target_names):
            train_values = [float(entry.result.train_rmse[target_index]) for entry in group_entries]
            rollout_values = [float(entry.result.rollout_rmse[target_index]) for entry in group_entries]
            rows.append(
                {
                    "group_key": group_key,
                    "scenario_label": _scenario_label(meta),
                    "profile_type": meta.get("profile_type", ""),
                    "axis": meta.get("axis", ""),
                    "input_peak": _csv_value(_float_value(meta.get("input_peak"))),
                    "repeat_count": len(group_entries),
                    "target": target_name,
                    "mean_run_train_rmse": _csv_value(_finite_mean(train_values)),
                    "std_run_train_rmse": _csv_value(_finite_std(train_values)),
                    "mean_run_rollout_rmse": _csv_value(_finite_mean(rollout_values)),
                    "std_run_rollout_rmse": _csv_value(_finite_std(rollout_values)),
                    "pooled_train_rmse": _csv_value(float(pooled.train_rmse[target_index])),
                    "pooled_loo_rmse": _csv_value(float(pooled.loo_rmse[target_index])),
                    "pooled_rollout_rmse": _csv_value(float(pooled.rollout_rmse[target_index])),
                }
            )
    rows.sort(key=lambda row: (str(row["scenario_label"]), str(row["target"])))
    return rows


def _scenario_coefficient_rows(
    args: argparse.Namespace,
    metadata_by_group: dict[str, dict[str, Any]],
    entries_by_group: dict[str, list[RunFitEntry]],
    pooled_results: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group_key, pooled in pooled_results.items():
        group_entries = entries_by_group.get(group_key, [])
        if len(group_entries) < args.min_repeats:
            continue
        meta = metadata_by_group[group_key]
        feature_names = pooled.feature_names
        target_names = pooled.target_names
        for feature_index, feature_name in enumerate(feature_names):
            term_kind = _term_kind(feature_name, pooled.input_fields)
            for target_index, target_name in enumerate(target_names):
                coeff_values = np.asarray(
                    [entry.result.coefficients[feature_index, target_index] for entry in group_entries],
                    dtype=float,
                )
                standardized_values = np.asarray(
                    [entry.result.standardized_coefficients[feature_index, target_index] for entry in group_entries],
                    dtype=float,
                )
                coeff_mean = _finite_mean(coeff_values)
                coeff_std = _finite_std(coeff_values)
                standardized_mean = _finite_mean(standardized_values)
                standardized_std = _finite_std(standardized_values)
                coeff_cv_abs = math.nan
                if abs(coeff_mean) > 1e-9:
                    coeff_cv_abs = coeff_std / abs(coeff_mean)
                rows.append(
                    {
                        "group_key": group_key,
                        "scenario_label": _scenario_label(meta),
                        "profile_type": meta.get("profile_type", ""),
                        "axis": meta.get("axis", ""),
                        "input_peak": _csv_value(_float_value(meta.get("input_peak"))),
                        "repeat_count": len(group_entries),
                        "target": target_name,
                        "term_kind": term_kind,
                        "term_name": feature_name,
                        "run_coefficient_mean": _csv_value(coeff_mean),
                        "run_coefficient_std": _csv_value(coeff_std),
                        "run_coefficient_cv_abs": _csv_value(coeff_cv_abs),
                        "run_standardized_mean": _csv_value(standardized_mean),
                        "run_standardized_std": _csv_value(standardized_std),
                        "pooled_coefficient": _csv_value(float(pooled.coefficients[feature_index, target_index])),
                        "pooled_standardized_coefficient": _csv_value(
                            float(pooled.standardized_coefficients[feature_index, target_index])
                        ),
                    }
                )
    rows.sort(key=lambda row: (str(row["scenario_label"]), str(row["term_name"]), str(row["target"])))
    return rows


def _write_summary(
    output_dir: Path,
    dataset_dir: Path,
    args: argparse.Namespace,
    overview_rows: list[dict[str, Any]],
    coefficient_rows: list[dict[str, Any]],
) -> None:
    ranked_rows = sorted(
        overview_rows,
        key=lambda row: float(row["std_run_rollout_rmse"]) if row["std_run_rollout_rmse"] != "" else -math.inf,
        reverse=True,
    )
    input_uncertainty_rows = [
        row
        for row in coefficient_rows
        if row["term_kind"] == "input" and row["run_coefficient_cv_abs"] != ""
    ]
    input_uncertainty_rows.sort(
        key=lambda row: float(row["run_coefficient_cv_abs"]),
        reverse=True,
    )

    summary_lines = [
        "# a/b Uncertainty Summary",
        "",
        f"- dataset_dir: {dataset_dir}",
        f"- output_dir: {output_dir}",
        f"- schema: {args.schema}",
        f"- group_field: {args.group_field}",
        f"- min_repeats: {args.min_repeats}",
        f"- window_mode: {args.window_mode}",
        f"- ridge_alpha: {args.ridge_alpha}",
        f"- profile_type: {args.profile_type}",
        f"- axis: {args.axis}",
        "",
        "## Highest Rollout Variability",
    ]
    for row in ranked_rows[:8]:
        summary_lines.append(
            "- "
            f"{row['scenario_label']}: repeats={row['repeat_count']}, "
            f"std_run_rollout_rmse={row['std_run_rollout_rmse']}, "
            f"pooled_mean_rollout_rmse={row['pooled_mean_rollout_rmse']}"
        )
    summary_lines.extend(["", "## Highest Input Coefficient CV"])
    for row in input_uncertainty_rows[:12]:
        summary_lines.append(
            "- "
            f"{row['scenario_label']} {row['term_name']} -> {row['target']}: "
            f"cv_abs={row['run_coefficient_cv_abs']}, std={row['run_coefficient_std']}"
        )
    summary_lines.extend(
        [
            "",
            "## Notes",
            "- per-run fit uses each repeat run independently, so coefficient std directly reflects repeat-to-repeat variation at the same operating point.",
            "- pooled metrics fit all repeats from one operating point together; they should be read together with per-run std, not as a replacement.",
        ]
    )
    (output_dir / "uncertainty_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="对 repeat-inclusive identification dataset 计算 a/b coefficient uncertainty。")
    parser.add_argument("--dataset-dir", default="", help="identification dataset 目录；默认使用最新一次导出。")
    parser.add_argument("--schema", choices=tuple(SCHEMA_INPUTS.keys()), default="attitude_setpoint")
    parser.add_argument(
        "--window-mode",
        choices=tuple(WINDOW_MODES.keys()),
        default="stabilize_active_recover",
        help="拟合使用哪些 phase window。",
    )
    parser.add_argument("--profile-type", choices=("baseline", "step", "pulse", "sweep", "all"), default="all")
    parser.add_argument("--axis", choices=("roll", "pitch", "all"), default="all")
    parser.add_argument("--ridge-alpha", type=float, default=0.0, help="ridge 正则强度，默认 0 表示 OLS。")
    parser.add_argument("--max-dt", type=float, default=0.2, help="保留样本的最大 dt_next_s。")
    parser.add_argument("--min-repeats", type=int, default=2, help="至少需要多少条可拟合 repeats 才输出 scenario 汇总。")
    parser.add_argument(
        "--group-field",
        choices=("scenario_signature", "config_signature"),
        default="scenario_signature",
        help="按哪个 selected_runs 字段聚合同一 operating point。",
    )
    parser.add_argument("--output-dir", default="", help="输出目录；默认写到 dataset_dir/uncertainty_<schema>_<timestamp>。")
    return parser


def run_uncertainty(args: argparse.Namespace) -> Path:
    dataset_dir = Path(args.dataset_dir).expanduser().resolve() if args.dataset_dir else _latest_dataset_dir()
    samples_rows = _load_rows(dataset_dir / "samples.csv")
    selected_rows = _load_rows(dataset_dir / "selected_runs.csv")
    filtered_rows = _filter_rows(samples_rows, args)

    metadata_by_run = {str(row["run_id"]): row for row in selected_rows}
    entries, grouped_rows = _fit_grouped_runs(filtered_rows, metadata_by_run, args)
    if not entries:
        raise RuntimeError("没有可成功拟合的 repeated runs")

    entries_by_group: dict[str, list[RunFitEntry]] = defaultdict(list)
    for entry in entries:
        entries_by_group[entry.group_key].append(entry)

    metadata_by_group: dict[str, dict[str, Any]] = {}
    for row in selected_rows:
        group_key = _group_key(row, args.group_field)
        metadata_by_group.setdefault(group_key, row)

    pooled_results: dict[str, Any] = {}
    for group_key, group_rows in grouped_rows.items():
        if len(entries_by_group.get(group_key, [])) < args.min_repeats:
            continue
        pooled_results[group_key] = fit_schema(group_rows, args.schema, args.ridge_alpha)

    output_dir = _resolve_output_dir(dataset_dir, args.output_dir, args.schema)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_yaml(
        output_dir / "manifest.yaml",
        {
            "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
            "dataset_dir": str(dataset_dir),
            "schema": args.schema,
            "group_field": args.group_field,
            "window_mode": args.window_mode,
            "ridge_alpha": args.ridge_alpha,
            "profile_type": args.profile_type,
            "axis": args.axis,
            "max_dt": args.max_dt,
            "min_repeats": args.min_repeats,
        },
    )

    per_run_rows = _per_run_rows(entries)
    overview_rows = _scenario_overview_rows(args, metadata_by_group, entries_by_group, pooled_results)
    validation_rows = _scenario_validation_rows(args, metadata_by_group, entries_by_group, pooled_results)
    coefficient_rows = _scenario_coefficient_rows(args, metadata_by_group, entries_by_group, pooled_results)
    if per_run_rows:
        write_rows_csv(output_dir / "per_run_fit_metrics.csv", per_run_rows, list(per_run_rows[0].keys()))
    if overview_rows:
        write_rows_csv(output_dir / "scenario_overview.csv", overview_rows, list(overview_rows[0].keys()))
    if validation_rows:
        write_rows_csv(output_dir / "scenario_validation.csv", validation_rows, list(validation_rows[0].keys()))
    if coefficient_rows:
        write_rows_csv(output_dir / "scenario_coefficients.csv", coefficient_rows, list(coefficient_rows[0].keys()))
    _write_summary(output_dir, dataset_dir, args, overview_rows, coefficient_rows)
    return output_dir


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    output_dir = run_uncertainty(args)
    print(f"uncertainty_dir={output_dir}")


if __name__ == "__main__":
    main()
