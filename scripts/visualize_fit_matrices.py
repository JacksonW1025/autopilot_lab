#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import yaml


DEFAULT_ABS_CMAP = "magma"
DEFAULT_SIGNED_CMAP = "coolwarm"
DEFAULT_QUANTILE = 0.99
DEFAULT_MAX_ROW_LABELS = 24


@dataclass(frozen=True)
class MatrixSpec:
    path: Path
    x_schema: str
    y_schema: str
    pooling_mode: str
    model_name: str


@dataclass(frozen=True)
class MatrixData:
    spec: MatrixSpec
    feature_names: list[str]
    response_names: list[str]
    values: np.ndarray


def _parse_combo_from_matrix_path(matrix_csv: Path) -> MatrixSpec:
    combo_dir = matrix_csv.parent.parent.name
    parts = combo_dir.split("__")
    if len(parts) != 3:
        raise ValueError(f"无法从路径解析 combo 信息: {matrix_csv}")
    return MatrixSpec(
        path=matrix_csv,
        x_schema=parts[0],
        y_schema=parts[1],
        pooling_mode=parts[2],
        model_name=matrix_csv.parent.name,
    )


def load_matrix_csv(matrix_csv: Path) -> MatrixData:
    path = matrix_csv.expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"matrix_f.csv 不存在: {path}")
    spec = _parse_combo_from_matrix_path(path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if not header or len(header) < 2:
            raise ValueError(f"matrix_f.csv 缺少有效 header: {path}")
        response_names = header[1:]
        feature_names: list[str] = []
        rows: list[list[float]] = []
        for row in reader:
            if not row:
                continue
            feature_names.append(row[0])
            rows.append([float(value) for value in row[1:]])
    values = np.asarray(rows, dtype=float)
    if values.ndim != 2:
        raise ValueError(f"matrix_f.csv 不是二维矩阵: {path}")
    if values.shape[0] != len(feature_names) or values.shape[1] != len(response_names):
        raise ValueError(f"matrix_f.csv 维度与 header 不一致: {path}")
    return MatrixData(
        spec=spec,
        feature_names=feature_names,
        response_names=response_names,
        values=values,
    )


def _load_study_summary(study_dir: Path) -> dict[str, Any]:
    summary_path = study_dir / "summary" / "study_summary.json"
    if not summary_path.exists():
        raise FileNotFoundError(f"study_summary.json 不存在: {summary_path}")
    return json.loads(summary_path.read_text(encoding="utf-8"))


def _load_appendix_x_schemas(study_dir: Path) -> set[str]:
    manifest_path = study_dir / "manifest.yaml"
    if not manifest_path.exists():
        return set()
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    report_matrix = manifest.get("report_matrix", {}) or {}
    appendix = report_matrix.get("appendix_x_schemas", []) or []
    return {str(item) for item in appendix}


def _entry_to_spec(study_dir: Path, entry: dict[str, Any]) -> MatrixSpec:
    spec = MatrixSpec(
        path=(
            study_dir
            / "fits"
            / f"{entry['x_schema']}__{entry['y_schema']}__{entry['pooling_mode']}"
            / str(entry["model_name"])
            / "matrix_f.csv"
        ).resolve(),
        x_schema=str(entry["x_schema"]),
        y_schema=str(entry["y_schema"]),
        pooling_mode=str(entry["pooling_mode"]),
        model_name=str(entry["model_name"]),
    )
    if not spec.path.exists():
        raise FileNotFoundError(f"选中的矩阵文件不存在: {spec.path}")
    return spec


def _is_appendix_entry(entry: dict[str, Any], appendix_x_schemas: set[str]) -> bool:
    if "appendix" in entry:
        return bool(entry["appendix"])
    return str(entry.get("x_schema", "")) in appendix_x_schemas


def _entry_key(entry: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(entry.get("x_schema", "")),
        str(entry.get("y_schema", "")),
        str(entry.get("pooling_mode", "")),
        str(entry.get("model_name", "")),
    )


def select_default_matrix_specs(study_dir: Path) -> list[MatrixSpec]:
    summary = _load_study_summary(study_dir)
    appendix_x_schemas = _load_appendix_x_schemas(study_dir)

    best_result = summary.get("best_result") or {}
    if not best_result:
        raise ValueError("study_summary.json 缺少 best_result")
    selected_best = _entry_to_spec(study_dir, best_result)
    selected_keys = {_entry_key(best_result)}

    ranking = list(summary.get("ranking", []) or [])

    def _pick(predicate) -> dict[str, Any] | None:
        for item in ranking:
            if _entry_key(item) in selected_keys:
                continue
            if predicate(item):
                return item
        return None

    second = _pick(
        lambda item: (
            not _is_appendix_entry(item, appendix_x_schemas)
            and str(item.get("pooling_mode", "")) == "pooled"
            and str(item.get("y_schema", "")) == "next_raw_state"
            and str(item.get("support", "")) == "supported"
        )
    )
    if second is None:
        second = _pick(
            lambda item: (
                not _is_appendix_entry(item, appendix_x_schemas)
                and str(item.get("support", "")) == "supported"
            )
        )
    if second is None:
        best_sparse = summary.get("best_sparse_result") or {}
        if best_sparse and _entry_key(best_sparse) not in selected_keys:
            second = best_sparse
    if second is None:
        raise ValueError("无法从 study_summary.json 选出第二张默认矩阵")
    return [selected_best, _entry_to_spec(study_dir, second)]


def _shared_quantile_limit(matrices: list[np.ndarray], quantile: float) -> float:
    finite_values = []
    for matrix in matrices:
        values = np.asarray(matrix, dtype=float)
        mask = np.isfinite(values)
        if np.any(mask):
            finite_values.append(values[mask])
    if not finite_values:
        return 1.0
    merged = np.concatenate(finite_values)
    limit = float(np.quantile(merged, quantile))
    if not math.isfinite(limit) or limit <= 0.0:
        limit = float(np.max(merged))
    if not math.isfinite(limit) or limit <= 0.0:
        return 1.0
    return limit


def compute_shared_limits(matrices: list[MatrixData], quantile: float = DEFAULT_QUANTILE) -> tuple[float, float]:
    abs_limit = _shared_quantile_limit([np.abs(item.values) for item in matrices], quantile)
    signed_limit = _shared_quantile_limit([np.abs(item.values) for item in matrices], quantile)
    return abs_limit, signed_limit


def compute_row_tick_positions(row_count: int, max_labels: int = DEFAULT_MAX_ROW_LABELS) -> np.ndarray:
    if row_count <= 0:
        return np.asarray([], dtype=int)
    if row_count <= max_labels:
        return np.arange(row_count, dtype=int)
    positions = np.linspace(0, row_count - 1, num=max_labels, dtype=int)
    return np.unique(positions)


def _figure_size(matrix: np.ndarray) -> tuple[float, float]:
    rows, cols = matrix.shape
    width = min(14.0, max(8.0, 0.55 * cols + 2.5))
    height = min(18.0, max(8.0, 0.14 * rows + 2.5))
    return width, height


def render_heatmap_figure(
    matrix_data: MatrixData,
    *,
    signed: bool,
    limit: float,
    max_row_labels: int = DEFAULT_MAX_ROW_LABELS,
):
    values = np.asarray(matrix_data.values, dtype=float)
    display_values = values if signed else np.abs(values)
    masked_values = np.ma.masked_invalid(display_values)

    cmap = plt.get_cmap(DEFAULT_SIGNED_CMAP if signed else DEFAULT_ABS_CMAP).copy()
    cmap.set_bad("#f2f2f2")
    norm = (
        mcolors.TwoSlopeNorm(vmin=-limit, vcenter=0.0, vmax=limit)
        if signed
        else mcolors.Normalize(vmin=0.0, vmax=limit)
    )

    fig, ax = plt.subplots(figsize=_figure_size(values), constrained_layout=True)
    image = ax.imshow(masked_values, aspect="auto", interpolation="nearest", cmap=cmap, norm=norm)

    ax.set_xticks(np.arange(len(matrix_data.response_names)))
    ax.set_xticklabels(matrix_data.response_names, rotation=45, ha="right", fontsize=8)

    y_positions = compute_row_tick_positions(len(matrix_data.feature_names), max_labels=max_row_labels)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([matrix_data.feature_names[index] for index in y_positions], fontsize=7)

    ax.set_xlabel("Responses")
    ax.set_ylabel("Features")
    ax.set_title(
        f"{matrix_data.spec.x_schema} -> {matrix_data.spec.y_schema} | "
        f"{matrix_data.spec.model_name} | {matrix_data.spec.pooling_mode}"
    )

    colorbar = fig.colorbar(image, ax=ax, fraction=0.03, pad=0.02)
    colorbar.set_ticks([])
    colorbar.set_label("negative -> zero -> positive" if signed else "low -> high", rotation=90)

    return fig, ax, colorbar


def save_matrix_heatmaps(
    matrix_data: MatrixData,
    *,
    abs_limit: float,
    signed_limit: float,
    max_row_labels: int = DEFAULT_MAX_ROW_LABELS,
) -> list[Path]:
    outputs = [
        (matrix_data.spec.path.parent / "matrix_heatmap_abs.png", False, abs_limit),
        (matrix_data.spec.path.parent / "matrix_heatmap_signed.png", True, signed_limit),
    ]
    written: list[Path] = []
    for output_path, signed, limit in outputs:
        fig, _, _ = render_heatmap_figure(
            matrix_data,
            signed=signed,
            limit=limit,
            max_row_labels=max_row_labels,
        )
        fig.savefig(output_path, dpi=200)
        plt.close(fig)
        written.append(output_path)
    return written


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="为 fit 矩阵生成热力图，不展示具体数值，只展示稀疏性与相对强弱。"
    )
    parser.add_argument("--study-dir", type=Path, help="study 目录；默认从 study_summary.json 中自动挑两张矩阵。")
    parser.add_argument(
        "--matrix-csv",
        action="append",
        dest="matrix_csvs",
        default=[],
        help="显式传入 matrix_f.csv 路径；需要恰好传两次。",
    )
    parser.add_argument("--quantile", type=float, default=DEFAULT_QUANTILE, help="共享色阶截断分位数，默认 0.99。")
    parser.add_argument(
        "--max-row-labels",
        type=int,
        default=DEFAULT_MAX_ROW_LABELS,
        help="纵轴最多显示多少个 feature 标签，默认 24。",
    )
    args = parser.parse_args(argv)
    if bool(args.study_dir) == bool(args.matrix_csvs):
        parser.error("必须二选一：要么传 --study-dir，要么显式传两个 --matrix-csv。")
    if args.matrix_csvs and len(args.matrix_csvs) != 2:
        parser.error("显式模式需要恰好两个 --matrix-csv。")
    if not (0.0 < float(args.quantile) <= 1.0):
        parser.error("--quantile 必须在 (0, 1] 内。")
    if int(args.max_row_labels) <= 0:
        parser.error("--max-row-labels 必须为正整数。")
    return args


def _load_selected_matrices(args: argparse.Namespace) -> list[MatrixData]:
    if args.study_dir:
        specs = select_default_matrix_specs(args.study_dir.expanduser().resolve())
    else:
        specs = [_parse_combo_from_matrix_path(Path(item).expanduser().resolve()) for item in args.matrix_csvs]
    return [load_matrix_csv(spec.path) for spec in specs]


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    matrices = _load_selected_matrices(args)
    abs_limit, signed_limit = compute_shared_limits(matrices, quantile=float(args.quantile))
    written_paths: list[Path] = []
    for matrix_data in matrices:
        written_paths.extend(
            save_matrix_heatmaps(
                matrix_data,
                abs_limit=abs_limit,
                signed_limit=signed_limit,
                max_row_labels=int(args.max_row_labels),
            )
        )
    for path in written_paths:
        print(f"generated={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
