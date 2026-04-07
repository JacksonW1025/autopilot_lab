from __future__ import annotations

import math
from typing import Any


def classify_support(result: dict[str, Any]) -> str:
    if result.get("status") == "skipped":
        return "skipped"
    r2 = float(result.get("median_test_r2", math.nan))
    stability = float(result.get("coefficient_stability", math.nan))
    condition_number = float(result.get("condition_number", math.inf))
    if r2 >= 0.70 and stability >= 0.60 and condition_number <= 1e6:
        return "supported"
    if r2 >= 0.40:
        return "partial"
    return "unsupported"


def _result_sort_key(item: dict[str, Any]) -> tuple[float, float, float]:
    summary = item["summary"]
    return (
        0.0 if item.get("appendix") else 1.0,
        float(summary.get("median_test_r2", float("-inf"))),
        float(summary.get("coefficient_stability", 0.0)),
        float(summary.get("sparsity_ratio", 0.0)),
    )


def summarize_results(
    results: list[dict[str, Any]],
    *,
    skipped_results: list[dict[str, Any]] | None = None,
    data_quality: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ordered = sorted(results, key=_result_sort_key, reverse=True)
    best = ordered[0] if ordered else {}
    skipped_results = skipped_results or []
    data_quality = data_quality or {}

    def _best_for_x_schema(name: str) -> dict[str, Any] | None:
        matching = [item for item in ordered if item.get("x_schema") == name]
        return matching[0] if matching else None

    def _best_for_y_schema(name: str) -> dict[str, Any] | None:
        matching = [item for item in ordered if item.get("y_schema") == name]
        return matching[0] if matching else None

    diagnostics: list[str] = []
    failure_attribution: list[str] = []
    best_commands_only = _best_for_x_schema("commands_only")
    best_commands_plus_state = _best_for_x_schema("commands_plus_state")
    best_history = _best_for_x_schema("commands_plus_state_history")
    best_pooled = _best_for_x_schema("pooled_backend_mode_augmented")
    best_delta = _best_for_y_schema("delta_state")
    best_next_raw = _best_for_y_schema("next_raw_state")
    best_window = _best_for_y_schema("window_summary_response")

    if best_commands_only and best_commands_plus_state:
        delta = float(best_commands_plus_state["summary"].get("median_test_r2", 0.0)) - float(best_commands_only["summary"].get("median_test_r2", 0.0))
        if delta >= 0.10:
            diagnostics.append("缺少必要 state/context；把当前状态并入 X 后显著提高了全局拟合效果。")
            failure_attribution.append("更像缺 state/context，而不是纯 command 输入本身不足。")
    if best_history and best_commands_plus_state:
        delta = float(best_history["summary"].get("median_test_r2", 0.0)) - float(best_commands_plus_state["summary"].get("median_test_r2", 0.0))
        if delta >= 0.10:
            diagnostics.append("需要 history/temporal context；静态单时刻回归不足。")
            failure_attribution.append("更像缺 history，而不是只差稀疏正则化。")
    if best_pooled and best_commands_plus_state:
        delta = float(best_commands_plus_state["summary"].get("median_test_r2", 0.0)) - float(best_pooled["summary"].get("median_test_r2", 0.0))
        if delta >= 0.10:
            diagnostics.append("pooled backend/mode 异质性较强；需要显式 stratification 或 covariate augmentation。")
    if best_delta and best_next_raw:
        delta = float(best_delta["summary"].get("median_test_r2", 0.0)) - float(best_next_raw["summary"].get("median_test_r2", 0.0))
        if delta >= 0.10:
            failure_attribution.append("更像当前 Y 定义不合适；状态增量比原始下一状态更接近线性。")
    if best_window and best:
        delta = float(best_window["summary"].get("median_test_r2", 0.0)) - float(best["summary"].get("median_test_r2", 0.0))
        if delta >= 0.10:
            failure_attribution.append("短窗统计响应可能比瞬时状态更可线性解释。")
    if best and classify_support(best.get("summary", {})) == "unsupported":
        diagnostics.append("当前 study scope 下，全局固定线性/仿射映射解释力不足，可能需要更强上下文、更多历史，或线性假设本身不成立。")
        failure_attribution.append("更像全局线性假设不足或噪声/异质性仍然过强。")
    if best:
        raw_condition = float(best.get("summary", {}).get("raw_condition_number", math.nan))
        effective_condition = float(best.get("summary", {}).get("effective_condition_number", math.nan))
        if math.isinf(raw_condition) and math.isfinite(effective_condition):
            diagnostics.append("raw feature matrix 含有精确别名或 one-hot 依赖；报告已同时输出 effective conditioning 以避免把可解释 schema 误判为病态。")

    missing_actuator_ratio = float(data_quality.get("missing_actuator_ratio", 0.0) or 0.0)
    if missing_actuator_ratio >= 0.95:
        diagnostics.append("真实 PX4 run 基本未记录 actuator 响应，actuator_response 相关组合只能跳过或视为 unsupported。")
    alignment_failure_ratio = float(data_quality.get("alignment_failure_ratio", 0.0) or 0.0)
    if alignment_failure_ratio >= 0.10:
        diagnostics.append("存在显著时间对齐失败样本，低 R² 需要结合对齐质量一起解释。")
    if not ordered and skipped_results:
        failure_attribution.append("当前更像 telemetry 可用性不足或 schema 依赖列缺失，而不是已经完成了对全局线性假设的有效否定。")

    best_sparse = {}
    if ordered:
        sparse_candidates = [
            item
            for item in ordered
            if float(item["summary"].get("median_test_r2", 0.0)) >= 0.40 and int(item["summary"].get("nonzero_count", 0)) > 0
        ]
        if not sparse_candidates:
            sparse_candidates = [item for item in ordered if int(item["summary"].get("nonzero_count", 0)) > 0]
        best_sparse = max(
            sparse_candidates or ordered,
            key=lambda item: (
                float(item["summary"].get("sparsity_ratio", 0.0)),
                float(item["summary"].get("coefficient_stability", 0.0)),
                float(item["summary"].get("median_test_r2", float("-inf"))),
            ),
        )

    best_y = {}
    if ordered:
        grouped_y = sorted(
            {item["y_schema"] for item in ordered},
            key=lambda name: _result_sort_key(_best_for_y_schema(name) or {"summary": {}}),
            reverse=True,
        )
        if grouped_y:
            best_y = _best_for_y_schema(grouped_y[0]) or {}

    schema_stepups = {}
    if best_commands_only and best_commands_plus_state:
        schema_stepups["commands_only_to_commands_plus_state_r2_gain"] = float(best_commands_plus_state["summary"].get("median_test_r2", 0.0)) - float(best_commands_only["summary"].get("median_test_r2", 0.0))
    if best_commands_plus_state and best_history:
        schema_stepups["commands_plus_state_to_history_r2_gain"] = float(best_history["summary"].get("median_test_r2", 0.0)) - float(best_commands_plus_state["summary"].get("median_test_r2", 0.0))

    return {
        "best_result": best,
        "best_sparse_result": best_sparse,
        "best_y_result": best_y,
        "schema_stepups": schema_stepups,
        "ranking": [
            {
                "x_schema": item["x_schema"],
                "y_schema": item["y_schema"],
                "model_name": item["model_name"],
                "pooling_mode": item["pooling_mode"],
                "median_test_r2": item["summary"]["median_test_r2"],
                "median_test_mse": item["summary"]["median_test_mse"],
                "median_test_mae": item["summary"]["median_test_mae"],
                "support": classify_support(item["summary"]),
            }
            for item in ordered
        ],
        "diagnostics": diagnostics,
        "failure_attribution": failure_attribution,
        "data_quality": data_quality,
        "skipped": [
            {
                "x_schema": item["x_schema"],
                "y_schema": item["y_schema"],
                "model_name": item["model_name"],
                "pooling_mode": item["pooling_mode"],
                "reason": item["summary"].get("skip_reason", "unknown"),
            }
            for item in skipped_results
        ],
    }


def render_summary_markdown(
    study_name: str,
    summary: dict[str, Any],
    results: list[dict[str, Any]],
    *,
    skipped_results: list[dict[str, Any]] | None = None,
) -> str:
    best = summary.get("best_result", {})
    best_sparse = summary.get("best_sparse_result", {})
    best_y = summary.get("best_y_result", {})
    best_summary = best.get("summary", {})
    ranking_lines = [
        f"- `{item['x_schema']} x {item['y_schema']} | {item['model_name']} | {item['pooling_mode']}`"
        f"{' (appendix)' if item.get('appendix') else ''}: "
        f"test R2={item['summary']['median_test_r2']:.4f}, sparsity={item['summary']['sparsity_ratio']:.4f}, "
        f"support={classify_support(item['summary'])}"
        for item in sorted(results, key=_result_sort_key, reverse=True)
    ]
    diagnostics_lines = [f"- {item}" for item in summary.get("diagnostics", [])] or ["- 暂无额外诊断。"]
    failure_lines = [f"- {item}" for item in summary.get("failure_attribution", [])] or ["- 暂无明确失败归因。"]
    skipped_lines = [
        f"- `{item['x_schema']} x {item['y_schema']} | {item['model_name']} | {item['pooling_mode']}`: {item['summary'].get('skip_reason', 'unknown')}"
        for item in (skipped_results or [])
    ] or ["- 无。"]
    data_quality = summary.get("data_quality", {})
    data_quality_lines = [
        f"- alignment_failure_ratio: {float(data_quality.get('alignment_failure_ratio', math.nan)):.4f}",
        f"- missing_attitude_ratio: {float(data_quality.get('missing_attitude_ratio', math.nan)):.4f}",
        f"- missing_local_position_ratio: {float(data_quality.get('missing_local_position_ratio', math.nan)):.4f}",
        f"- missing_actuator_ratio: {float(data_quality.get('missing_actuator_ratio', math.nan)):.4f}",
        f"- future_horizon_available_ratio: {float(data_quality.get('future_horizon_available_ratio', math.nan)):.4f}",
        f"- window_summary_available_ratio: {float(data_quality.get('window_summary_available_ratio', math.nan)):.4f}",
        f"- median_alignment_attitude_ms: {float(data_quality.get('median_alignment_attitude_ms', math.nan)):.4f}",
        f"- median_alignment_position_ms: {float(data_quality.get('median_alignment_position_ms', math.nan)):.4f}",
    ]
    conditioning_lines = [
        f"- raw_condition_number: {float(best_summary.get('raw_condition_number', math.nan)):.4f}",
        f"- effective_condition_number: {float(best_summary.get('effective_condition_number', math.nan)):.4f}",
        f"- conditioning_pruned_features: {', '.join(best_summary.get('conditioning_pruned_features', [])) or 'none'}",
        f"- conditioning_baseline_drops: {', '.join(best_summary.get('conditioning_baseline_drops', [])) or 'none'}",
        f"- conditioning_extra_pruned_features: {', '.join(best_summary.get('conditioning_extra_pruned_features', [])) or 'none'}",
    ]

    best_combo = "n/a"
    if best:
        best_combo = f"{best['x_schema']} x {best['y_schema']} | {best['model_name']} | {best['pooling_mode']}"
    best_sparse_combo = "n/a"
    if best_sparse:
        best_sparse_combo = f"{best_sparse['x_schema']} x {best_sparse['y_schema']} | {best_sparse['model_name']} | {best_sparse['pooling_mode']}"
    best_y_label = best_y.get("y_schema", "n/a") if best_y else "n/a"

    return "\n".join(
        [
            f"# Global Linearity Study Summary: {study_name}",
            "",
            "## 研究目标",
            "- 主线固定为：数据采集 -> X/Y 构造 -> 全局拟合 -> 稀疏性分析 -> 结论。",
            "- 研究问题是：在当前 study scope 下，是否存在固定的全局线性/仿射映射 `Y ≈ fX (+ b)`。",
            "",
            "## 真实 PX4 Broad Ablation 结论模板",
            f"- best_linear_schema: `{best_combo}`",
            f"- best_sparse_and_stable_schema: `{best_sparse_combo}`",
            f"- best_y_definition: `{best_y_label}`",
            f"- commands_only_to_commands_plus_state_r2_gain: {summary.get('schema_stepups', {}).get('commands_only_to_commands_plus_state_r2_gain', math.nan):.4f}",
            f"- commands_plus_state_to_history_r2_gain: {summary.get('schema_stepups', {}).get('commands_plus_state_to_history_r2_gain', math.nan):.4f}",
            "",
            "## 最优组合",
            f"- best_combo: `{best_combo}`",
            f"- support: `{classify_support(best_summary)}`",
            f"- median_test_r2: {best_summary.get('median_test_r2', math.nan):.4f}",
            f"- median_test_mse: {best_summary.get('median_test_mse', math.nan):.6f}",
            f"- median_test_mae: {best_summary.get('median_test_mae', math.nan):.6f}",
            f"- sparsity_ratio: {best_summary.get('sparsity_ratio', math.nan):.4f}",
            f"- coefficient_stability: {best_summary.get('coefficient_stability', math.nan):.4f}",
            "",
            "## Conditioning",
            *conditioning_lines,
            "",
            "## Data Quality",
            *data_quality_lines,
            "",
            "## Schema Ranking",
            *ranking_lines,
            "",
            "## Diagnostics",
            *diagnostics_lines,
            "",
            "## Failure Attribution",
            *failure_lines,
            "",
            "## Skipped Or Unsupported Combos",
            *skipped_lines,
        ]
    )


def render_comparison_markdown(
    study_name: str,
    results: list[dict[str, Any]],
    *,
    skipped_results: list[dict[str, Any]] | None = None,
) -> str:
    lines = [f"# Schema Comparison: {study_name}", "", "## Results"]
    for item in sorted(results, key=_result_sort_key, reverse=True):
        lines.extend(
            [
                f"### {item['x_schema']} x {item['y_schema']} | {item['model_name']} | {item['pooling_mode']}",
                *([f"- appendix: `true`"] if item.get("appendix") else []),
                f"- support: `{classify_support(item['summary'])}`",
                f"- median_test_r2: {item['summary']['median_test_r2']:.4f}",
                f"- median_test_mse: {item['summary']['median_test_mse']:.6f}",
                f"- median_test_mae: {item['summary']['median_test_mae']:.6f}",
                f"- coefficient_stability: {item['summary']['coefficient_stability']:.4f}",
                f"- nonzero_count: {item['summary']['nonzero_count']}",
                f"- sparsity_ratio: {item['summary']['sparsity_ratio']:.4f}",
                f"- raw_condition_number: {item['summary'].get('raw_condition_number', math.nan):.4f}",
                f"- effective_condition_number: {item['summary'].get('effective_condition_number', item['summary']['condition_number']):.4f}",
                f"- conditioning_pruned_features: {', '.join(item['summary'].get('conditioning_pruned_features', [])) or 'none'}",
                f"- conditioning_baseline_drops: {', '.join(item['summary'].get('conditioning_baseline_drops', [])) or 'none'}",
                f"- conditioning_extra_pruned_features: {', '.join(item['summary'].get('conditioning_extra_pruned_features', [])) or 'none'}",
                "",
            ]
        )
    lines.extend(["## Skipped"])
    skipped = skipped_results or []
    if not skipped:
        lines.append("- 无。")
    else:
        for item in skipped:
            lines.append(
                f"- `{item['x_schema']} x {item['y_schema']} | {item['model_name']} | {item['pooling_mode']}`: {item['summary'].get('skip_reason', 'unknown')}"
            )
    return "\n".join(lines)
