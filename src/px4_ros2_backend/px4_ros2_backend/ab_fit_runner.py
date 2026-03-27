from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from fep_core.paths import PX4_IDENTIFICATION_ROOT as IDENTIFICATION_ROOT

from .artifacts import write_rows_csv, write_yaml

STATE_FIELDS = ("state_roll", "state_pitch", "state_roll_rate", "state_pitch_rate")
TARGET_FIELDS = tuple(f"next_{field}" for field in STATE_FIELDS)
SCHEMA_INPUTS = {
    "command_body": ("command_roll_body", "command_pitch_body"),
    "attitude_setpoint": ("attitude_sp_roll", "attitude_sp_pitch"),
    "rates_setpoint": ("rates_sp_roll", "rates_sp_pitch"),
    "torque_setpoint": ("torque_sp_x", "torque_sp_y"),
}
WINDOW_MODES = {
    "active": ("active_window",),
    "active_recover": ("active_window", "recover_window"),
    "stabilize_active_recover": ("stabilize_window", "active_window", "recover_window"),
    "all": (),
}


@dataclass(slots=True)
class FitResult:
    schema_name: str
    input_fields: tuple[str, ...]
    feature_names: list[str]
    coefficients: np.ndarray
    train_predictions: np.ndarray
    target_names: tuple[str, ...]
    train_rmse: np.ndarray
    train_mae: np.ndarray
    rollout_rmse: np.ndarray
    loo_rmse: np.ndarray
    coefficient_std: np.ndarray
    standardized_coefficients: np.ndarray
    condition_number: float
    row_count: int
    run_count: int


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


def _load_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def _rows_to_arrays(rows: list[dict[str, Any]], schema_name: str) -> tuple[np.ndarray, np.ndarray, list[str], np.ndarray]:
    input_fields = list(SCHEMA_INPUTS[schema_name])
    feature_names = input_fields + list(STATE_FIELDS)
    design_rows: list[list[float]] = []
    target_rows: list[list[float]] = []
    run_ids: list[str] = []
    sample_index: list[int] = []
    for row in rows:
        feature_values = [_float_value(row.get(name)) for name in feature_names]
        target_values = [_float_value(row.get(name)) for name in TARGET_FIELDS]
        dt_value = _float_value(row.get("dt_next_s"))
        if any(math.isnan(value) for value in feature_values + target_values):
            continue
        if math.isnan(dt_value) or dt_value <= 0.0:
            continue
        design_rows.append([1.0] + feature_values)
        target_rows.append(target_values)
        run_ids.append(str(row["run_id"]))
        sample_index.append(int(float(row["sample_index"])))
    if not design_rows:
        raise RuntimeError(f"schema={schema_name} 过滤后没有可用样本")
    return (
        np.asarray(design_rows, dtype=float),
        np.asarray(target_rows, dtype=float),
        run_ids,
        np.asarray(sample_index, dtype=int),
    )


def _fit_linear_model(design: np.ndarray, targets: np.ndarray, ridge_alpha: float) -> np.ndarray:
    if ridge_alpha <= 0.0:
        coefficients, *_ = np.linalg.lstsq(design, targets, rcond=None)
        return coefficients
    penalty = np.sqrt(ridge_alpha) * np.eye(design.shape[1], dtype=float)
    penalty[0, 0] = 0.0
    augmented_design = np.vstack([design, penalty])
    augmented_targets = np.vstack([targets, np.zeros((design.shape[1], targets.shape[1]), dtype=float)])
    coefficients, *_ = np.linalg.lstsq(augmented_design, augmented_targets, rcond=None)
    return coefficients


def _rmse(errors: np.ndarray) -> np.ndarray:
    return np.sqrt(np.mean(np.square(errors), axis=0))


def _mae(errors: np.ndarray) -> np.ndarray:
    return np.mean(np.abs(errors), axis=0)


def _rollout_rmse(
    rows: list[dict[str, Any]],
    schema_name: str,
    coefficients: np.ndarray,
) -> np.ndarray:
    errors_by_target: list[np.ndarray] = []
    input_fields = SCHEMA_INPUTS[schema_name]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["run_id"])].append(row)

    for run_rows in grouped.values():
        ordered = sorted(run_rows, key=lambda item: int(float(item["sample_index"])))
        if not ordered:
            continue
        # rollout 用模型自己的前一步预测作为下一步状态输入，用来检查递推是否会发散。
        predicted_state = np.asarray([_float_value(ordered[0].get(field)) for field in STATE_FIELDS], dtype=float)
        if np.any(np.isnan(predicted_state)):
            continue
        for row in ordered:
            input_values = np.asarray([_float_value(row.get(name)) for name in input_fields], dtype=float)
            actual_next = np.asarray([_float_value(row.get(name)) for name in TARGET_FIELDS], dtype=float)
            if np.any(np.isnan(input_values)) or np.any(np.isnan(actual_next)):
                continue
            design_row = np.concatenate(([1.0], input_values, predicted_state))
            predicted_next = design_row @ coefficients
            errors_by_target.append(predicted_next - actual_next)
            predicted_state = predicted_next

    if not errors_by_target:
        return np.full(len(TARGET_FIELDS), np.nan, dtype=float)
    return _rmse(np.asarray(errors_by_target, dtype=float))


def _loo_metrics(
    design: np.ndarray,
    targets: np.ndarray,
    run_ids: list[str],
    ridge_alpha: float,
) -> tuple[np.ndarray, np.ndarray]:
    unique_runs = sorted(set(run_ids))
    if len(unique_runs) < 2:
        target_dim = targets.shape[1]
        coeff_shape = (design.shape[1], target_dim)
        return (
            np.full(target_dim, np.nan, dtype=float),
            np.full(coeff_shape, np.nan, dtype=float),
        )

    heldout_errors: list[np.ndarray] = []
    coefficients: list[np.ndarray] = []
    run_ids_arr = np.asarray(run_ids)
    for run_id in unique_runs:
        # 以整条 run 为单位留一，避免相邻样本泄漏到训练集里。
        train_mask = run_ids_arr != run_id
        test_mask = ~train_mask
        if np.count_nonzero(train_mask) <= design.shape[1] or np.count_nonzero(test_mask) == 0:
            continue
        fold_coefficients = _fit_linear_model(design[train_mask], targets[train_mask], ridge_alpha)
        coefficients.append(fold_coefficients)
        heldout_errors.append((design[test_mask] @ fold_coefficients) - targets[test_mask])

    if not heldout_errors or not coefficients:
        target_dim = targets.shape[1]
        coeff_shape = (design.shape[1], target_dim)
        return (
            np.full(target_dim, np.nan, dtype=float),
            np.full(coeff_shape, np.nan, dtype=float),
        )

    stacked_errors = np.vstack(heldout_errors)
    stacked_coefficients = np.stack(coefficients, axis=0)
    return _rmse(stacked_errors), np.std(stacked_coefficients, axis=0, ddof=0)


def _standardized_coefficients(coefficients: np.ndarray, design: np.ndarray, targets: np.ndarray) -> np.ndarray:
    standardized = np.full(coefficients.shape, np.nan, dtype=float)
    feature_std = np.std(design[:, 1:], axis=0, ddof=0)
    target_std = np.std(targets, axis=0, ddof=0)
    for feature_index in range(1, coefficients.shape[0]):
        feature_scale = feature_std[feature_index - 1]
        if feature_scale <= 0.0:
            continue
        for target_index in range(coefficients.shape[1]):
            if target_std[target_index] <= 0.0:
                continue
            standardized[feature_index, target_index] = (
                coefficients[feature_index, target_index] * feature_scale / target_std[target_index]
            )
    return standardized


def fit_schema(rows: list[dict[str, Any]], schema_name: str, ridge_alpha: float) -> FitResult:
    design, targets, run_ids, _sample_index = _rows_to_arrays(rows, schema_name)
    coefficients = _fit_linear_model(design, targets, ridge_alpha)
    predictions = design @ coefficients
    train_errors = predictions - targets
    train_rmse = _rmse(train_errors)
    train_mae = _mae(train_errors)
    loo_rmse, coefficient_std = _loo_metrics(design, targets, run_ids, ridge_alpha)
    rollout_rmse = _rollout_rmse(rows, schema_name, coefficients)
    standardized = _standardized_coefficients(coefficients, design, targets)
    try:
        condition_number = float(np.linalg.cond(design[:, 1:]))
    except np.linalg.LinAlgError:
        condition_number = math.nan
    return FitResult(
        schema_name=schema_name,
        input_fields=SCHEMA_INPUTS[schema_name],
        feature_names=["intercept"] + list(SCHEMA_INPUTS[schema_name]) + list(STATE_FIELDS),
        coefficients=coefficients,
        train_predictions=predictions,
        target_names=TARGET_FIELDS,
        train_rmse=train_rmse,
        train_mae=train_mae,
        rollout_rmse=rollout_rmse,
        loo_rmse=loo_rmse,
        coefficient_std=coefficient_std,
        standardized_coefficients=standardized,
        condition_number=condition_number,
        row_count=design.shape[0],
        run_count=len(set(run_ids)),
    )


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


def _coefficients_rows(result: FitResult) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for feature_index, feature_name in enumerate(result.feature_names):
        if feature_name == "intercept":
            term_kind = "intercept"
        elif feature_name in result.input_fields:
            term_kind = "input"
        else:
            term_kind = "state"
        for target_index, target_name in enumerate(result.target_names):
            rows.append(
                {
                    "schema": result.schema_name,
                    "target": target_name,
                    "term_kind": term_kind,
                    "term_name": feature_name,
                    "coefficient": _csv_value(result.coefficients[feature_index, target_index]),
                    "coefficient_std_loo": _csv_value(result.coefficient_std[feature_index, target_index]),
                    "standardized_coefficient": _csv_value(result.standardized_coefficients[feature_index, target_index]),
                    "abs_standardized_coefficient": _csv_value(
                        abs(result.standardized_coefficients[feature_index, target_index])
                        if not math.isnan(result.standardized_coefficients[feature_index, target_index])
                        else math.nan
                    ),
                }
            )
    return rows


def _sensitivity_rows(result: FitResult) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    feature_names = result.feature_names[1:]
    for feature_offset, feature_name in enumerate(feature_names, start=1):
        term_kind = "input" if feature_name in result.input_fields else "state"
        values = [
            abs(result.standardized_coefficients[feature_offset, target_index])
            for target_index in range(len(result.target_names))
            if not math.isnan(result.standardized_coefficients[feature_offset, target_index])
        ]
        rows.append(
            {
                "schema": result.schema_name,
                "term_kind": term_kind,
                "term_name": feature_name,
                "mean_abs_standardized_coefficient": _csv_value(float(np.mean(values)) if values else math.nan),
                "max_abs_standardized_coefficient": _csv_value(float(np.max(values)) if values else math.nan),
            }
        )
    rows.sort(
        key=lambda row: (
            row["schema"],
            -(float(row["mean_abs_standardized_coefficient"]) if row["mean_abs_standardized_coefficient"] != "" else -math.inf),
        )
    )
    return rows


def _validation_rows(result: FitResult) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target_index, target_name in enumerate(result.target_names):
        rows.append(
            {
                "schema": result.schema_name,
                "target": target_name,
                "row_count": result.row_count,
                "run_count": result.run_count,
                "condition_number": _csv_value(result.condition_number),
                "train_rmse": _csv_value(result.train_rmse[target_index]),
                "train_mae": _csv_value(result.train_mae[target_index]),
                "loo_rmse": _csv_value(result.loo_rmse[target_index]),
                "rollout_rmse": _csv_value(result.rollout_rmse[target_index]),
            }
        )
    return rows


def _schema_comparison_rows(results: list[FitResult]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in results:
        sensitivity_values = [
            abs(result.standardized_coefficients[feature_index, target_index])
            for feature_index, feature_name in enumerate(result.feature_names)
            if feature_name in result.input_fields
            for target_index in range(len(result.target_names))
            if not math.isnan(result.standardized_coefficients[feature_index, target_index])
        ]
        rows.append(
            {
                "schema": result.schema_name,
                "row_count": result.row_count,
                "run_count": result.run_count,
                "condition_number": _csv_value(result.condition_number),
                "mean_train_rmse": _csv_value(float(np.nanmean(result.train_rmse))),
                "mean_loo_rmse": _csv_value(float(np.nanmean(result.loo_rmse))),
                "mean_rollout_rmse": _csv_value(float(np.nanmean(result.rollout_rmse))),
                "mean_abs_input_standardized_coefficient": _csv_value(
                    float(np.mean(sensitivity_values)) if sensitivity_values else math.nan
                ),
                "max_abs_input_standardized_coefficient": _csv_value(
                    float(np.max(sensitivity_values)) if sensitivity_values else math.nan
                ),
            }
        )
    rows.sort(
        key=lambda row: (
            float(row["mean_loo_rmse"]) if row["mean_loo_rmse"] != "" else math.inf,
            float(row["mean_rollout_rmse"]) if row["mean_rollout_rmse"] != "" else math.inf,
        )
    )
    return rows


def _write_summary(
    output_dir: Path,
    dataset_dir: Path,
    args: argparse.Namespace,
    filtered_rows: list[dict[str, Any]],
    comparison_rows: list[dict[str, Any]],
) -> None:
    summary_lines = [
        "# a/b Fit Summary",
        "",
        f"- dataset_dir: {dataset_dir}",
        f"- fit_dir: {output_dir}",
        f"- schemas: {', '.join(args.schemas)}",
        f"- window_mode: {args.window_mode}",
        f"- ridge_alpha: {args.ridge_alpha}",
        f"- profile_type: {args.profile_type}",
        f"- axis: {args.axis}",
        f"- filtered_rows: {len(filtered_rows)}",
        f"- filtered_runs: {len(set(row['run_id'] for row in filtered_rows))}",
        "",
        "## Schema Comparison",
    ]
    for row in comparison_rows:
        summary_lines.append(
            "- "
            f"{row['schema']}: mean_loo_rmse={row['mean_loo_rmse']}, "
            f"mean_rollout_rmse={row['mean_rollout_rmse']}, "
            f"mean_abs_input_std_coef={row['mean_abs_input_standardized_coefficient']}"
        )
    summary_lines.extend(
        [
            "",
            "## Notes",
            "- current fit is one-step discrete-time identification on `[roll, pitch, p, q]` targets.",
            "- `a` corresponds to the selected input schema (`command_body` / `attitude_setpoint` / `rates_setpoint` / `torque_setpoint`).",
            "- `b` corresponds to current state terms `[state_roll, state_pitch, state_roll_rate, state_pitch_rate]`.",
            "- `loo_rmse` is leave-one-run-out one-step validation; `rollout_rmse` is recursive per-run rollout using predicted previous state.",
        ]
    )
    (output_dir / "fit_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


def _resolve_output_dir(dataset_dir: Path, explicit_output: str) -> Path:
    if explicit_output:
        return Path(explicit_output).expanduser().resolve()
    stamp = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d_%H%M%S")
    return dataset_dir / f"fit_{stamp}"


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="基于 identification dataset 做第一版 nominal hover-local a/b one-step 拟合。")
    parser.add_argument("--dataset-dir", default="", help="identification dataset 目录；默认使用最新一次导出。")
    parser.add_argument(
        "--schemas",
        nargs="+",
        default=["command_body", "attitude_setpoint", "rates_setpoint", "torque_setpoint"],
        choices=tuple(SCHEMA_INPUTS.keys()),
        help="要比较的 x_t 定义。",
    )
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
    parser.add_argument("--output-dir", default="", help="fit 输出目录；默认写入 dataset_dir/fit_<timestamp>。")
    return parser


def run_fit(args: argparse.Namespace) -> Path:
    dataset_dir = Path(args.dataset_dir).expanduser().resolve() if args.dataset_dir else _latest_dataset_dir()
    rows = _load_rows(dataset_dir / "samples.csv")
    filtered_rows = _filter_rows(rows, args)

    output_dir = _resolve_output_dir(dataset_dir, args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest_payload = {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "dataset_dir": str(dataset_dir),
        "schemas": list(args.schemas),
        "window_mode": args.window_mode,
        "ridge_alpha": args.ridge_alpha,
        "profile_type": args.profile_type,
        "axis": args.axis,
        "max_dt": args.max_dt,
    }
    write_yaml(output_dir / "manifest.yaml", manifest_payload)

    results = [fit_schema(filtered_rows, schema_name, args.ridge_alpha) for schema_name in args.schemas]

    coefficient_rows = [row for result in results for row in _coefficients_rows(result)]
    sensitivity_rows = [row for result in results for row in _sensitivity_rows(result)]
    validation_rows = [row for result in results for row in _validation_rows(result)]
    comparison_rows = _schema_comparison_rows(results)

    write_rows_csv(output_dir / "ab_coefficients.csv", coefficient_rows, list(coefficient_rows[0].keys()))
    write_rows_csv(output_dir / "ab_sensitivity.csv", sensitivity_rows, list(sensitivity_rows[0].keys()))
    write_rows_csv(output_dir / "validation_metrics.csv", validation_rows, list(validation_rows[0].keys()))
    write_rows_csv(output_dir / "schema_comparison.csv", comparison_rows, list(comparison_rows[0].keys()))
    _write_summary(output_dir, dataset_dir, args, filtered_rows, comparison_rows)
    return output_dir


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    output_dir = run_fit(args)
    print(f"fit_dir={output_dir}")


if __name__ == "__main__":
    main()
