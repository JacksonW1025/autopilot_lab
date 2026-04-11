from __future__ import annotations

import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .config import StudyConfig
from .dataset import PREPARED_SAMPLE_IDENTITY_COLUMNS, build_prepared_sample_table, prepared_sample_table_fieldnames
from .io import read_rows_csv, read_yaml
from .paths import STUDY_ARTIFACT_ROOT
from .report import classify_support
from .research_contract import manifest_acceptance_state

AMPLITUDE_TIER_ORDER = ["small", "medium", "large"]
ATTITUDE_AXES = ["roll", "pitch", "yaw"]
CONTRACT_REQUIRED_MANIFEST_KEYS = [
    "raw_schema_version",
    "research_tier",
    "research_acceptance",
    "research_rejection_reasons",
    "data_quality",
    "study_config",
]
CONTRACT_PREFIXES = ["backend_", "mode_", "scenario_", "config_profile_", "param_"]
NONZERO_GATE_REASON = "insufficient_active_nonzero_command_samples"
STATE_EVOLUTION_X_SCHEMAS = ["commands_plus_state", "commands_plus_state_history", "full_augmented"]
STATE_EVOLUTION_Y_SCHEMAS = [
    "next_raw_state",
    "selected_state_subset",
    "future_state_horizon",
    "delta_state",
    "window_summary_response",
]
GENERALIZATION_STATUS_ORDER = {
    "generalized_supported": 2,
    "supported_but_local": 1,
    "not_generalized": 0,
}


def _supported_combo_keys(summary: dict[str, Any]) -> list[str]:
    return sorted(
        {
            _combo_key(item)
            for item in summary.get("ranking", [])
            if str(item.get("support", "")).strip().lower() == "supported"
        }
    )


def _combo_key(item: dict[str, Any]) -> str:
    return " | ".join(
        [
            str(item.get("x_schema", "")),
            str(item.get("y_schema", "")),
            str(item.get("model_name", "")),
            str(item.get("pooling_mode", "")),
        ]
    )


def _supported_anchor(summary: dict[str, Any]) -> dict[str, Any]:
    for item in summary.get("ranking", []):
        if str(item.get("support", "")).strip().lower() == "supported":
            return item
    return {}


def _combo_support(summary: dict[str, Any], combo: dict[str, Any]) -> str:
    combo_key = _combo_key(combo)
    for item in summary.get("ranking", []):
        if _combo_key(item) == combo_key:
            return str(item.get("support", ""))
    return ""


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def _load_sparsity_edges(study_dir: Path, combo: dict[str, Any]) -> set[tuple[str, str]]:
    if not combo:
        return set()
    path = (
        study_dir
        / "fits"
        / f"{combo.get('x_schema', '')}__{combo.get('y_schema', '')}__{combo.get('pooling_mode', '')}"
        / str(combo.get("model_name", ""))
        / "sparsity_mask.csv"
    )
    if not path.exists():
        return set()
    rows = read_rows_csv(path)
    edges: set[tuple[str, str]] = set()
    for row in rows:
        feature = str(row.get("feature", ""))
        if not feature:
            continue
        for response, value in row.items():
            if response == "feature":
                continue
            if _safe_float(value) >= 0.5:
                edges.add((feature, response))
    return edges


def _load_combo_metrics(study_dir: Path, combo: dict[str, Any]) -> dict[str, Any]:
    if not combo:
        return {}
    path = (
        study_dir
        / "fits"
        / f"{combo.get('x_schema', '')}__{combo.get('y_schema', '')}__{combo.get('pooling_mode', '')}"
        / str(combo.get("model_name", ""))
        / "metrics.json"
    )
    if not path.exists():
        return {}
    return read_yaml(path)


def _resolve_combo(study_dir: Path, combo: dict[str, Any]) -> dict[str, Any]:
    if not combo:
        return {}
    resolved = dict(combo)
    summary = resolved.get("summary", {})
    if not isinstance(summary, dict) or not summary:
        resolved["summary"] = _load_combo_metrics(study_dir, combo)
    return resolved


def _overlap_payload(current_edges: set[tuple[str, str]], previous_edges: set[tuple[str, str]]) -> dict[str, Any]:
    union = current_edges | previous_edges
    intersection = current_edges & previous_edges
    return {
        "current_nonzero_count": len(current_edges),
        "previous_nonzero_count": len(previous_edges),
        "intersection_count": len(intersection),
        "union_count": len(union),
        "jaccard_overlap": (len(intersection) / len(union)) if union else math.nan,
    }


def _find_previous_comparable_study(
    current_study_dir: Path,
    study_name: str,
    current_manifest: dict[str, Any],
    current_inventory: dict[str, Any],
) -> Path | None:
    current_run_count = int(current_inventory.get("data_quality", {}).get("accepted_run_count", current_inventory.get("run_count", 0)) or 0)
    current_backends = sorted(current_manifest.get("source_backends", []) or [])
    current_modes = sorted(current_manifest.get("source_modes", []) or [])
    current_profiles = sorted(current_manifest.get("source_config_profiles", []) or [])
    candidates: list[tuple[int, str, Path]] = []
    for candidate in sorted(STUDY_ARTIFACT_ROOT.glob(f"*_{study_name}")):
        if candidate.resolve() == current_study_dir.resolve():
            continue
        candidate_manifest_path = candidate / "manifest.yaml"
        candidate_inventory_path = candidate / "prepared" / "schema_inventory.yaml"
        candidate_summary_path = candidate / "summary" / "study_summary.json"
        if not candidate_manifest_path.exists() or not candidate_inventory_path.exists() or not candidate_summary_path.exists():
            continue
        manifest = read_yaml(candidate_manifest_path)
        if str(manifest.get("study_name", "")).strip() != study_name:
            continue
        if sorted(manifest.get("source_backends", []) or []) != current_backends:
            continue
        if sorted(manifest.get("source_modes", []) or []) != current_modes:
            continue
        if sorted(manifest.get("source_config_profiles", []) or []) != current_profiles:
            continue
        inventory = read_yaml(candidate_inventory_path)
        run_count = int(inventory.get("data_quality", {}).get("accepted_run_count", inventory.get("run_count", 0)) or 0)
        if run_count >= current_run_count:
            continue
        candidates.append((run_count, candidate.name, candidate))
    if not candidates:
        return None
    candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return candidates[0][2]


def build_baseline_stability_payload(
    current_study_dir: Path,
    study_name: str,
    current_summary: dict[str, Any],
    current_inventory: dict[str, Any],
    current_manifest: dict[str, Any],
) -> dict[str, Any]:
    current_best = _resolve_combo(current_study_dir, dict(current_summary.get("best_result", {}) or {}))
    current_supported = _resolve_combo(current_study_dir, _supported_anchor(current_summary))
    current_best_support = _combo_support(current_summary, current_best)
    payload: dict[str, Any] = {
        "status": "comparison_unavailable",
        "study_name": study_name,
        "current_study_dir": str(current_study_dir),
        "current": {
            "accepted_run_count": int(
                current_inventory.get("data_quality", {}).get("accepted_run_count", current_inventory.get("run_count", 0)) or 0
            ),
            "best_result": current_best,
            "supported_anchor": current_supported,
            "best_result_support": current_best_support,
        },
        "previous": {},
        "deltas": {},
        "sparsity_overlap": {},
    }
    previous_study_dir = _find_previous_comparable_study(current_study_dir, study_name, current_manifest, current_inventory)
    if previous_study_dir is None:
        return payload

    previous_summary = read_yaml(previous_study_dir / "summary" / "study_summary.json")
    previous_inventory = read_yaml(previous_study_dir / "prepared" / "schema_inventory.yaml")
    previous_best = _resolve_combo(previous_study_dir, dict(previous_summary.get("best_result", {}) or {}))
    previous_supported = _resolve_combo(previous_study_dir, _supported_anchor(previous_summary))
    previous_best_support = _combo_support(previous_summary, previous_best)
    current_best_summary = current_best.get("summary", {})
    previous_best_summary = previous_best.get("summary", {})
    current_supported_summary = current_supported.get("summary", {})
    previous_supported_summary = previous_supported.get("summary", {})

    current_supported_r2 = _safe_float(current_supported.get("median_test_r2", current_supported_summary.get("median_test_r2")))
    previous_supported_r2 = _safe_float(previous_supported.get("median_test_r2", previous_supported_summary.get("median_test_r2")))
    current_supported_condition = _safe_float(
        current_supported.get("effective_condition_number", current_supported_summary.get("effective_condition_number"))
    )
    previous_supported_condition = _safe_float(
        previous_supported.get("effective_condition_number", previous_supported_summary.get("effective_condition_number"))
    )

    current_best_edges = _load_sparsity_edges(current_study_dir, current_best)
    previous_best_edges = _load_sparsity_edges(previous_study_dir, previous_best)
    current_supported_edges = _load_sparsity_edges(current_study_dir, current_supported)
    previous_supported_edges = _load_sparsity_edges(previous_study_dir, previous_supported)

    payload["status"] = "comparison_available"
    payload["previous"] = {
        "study_dir": str(previous_study_dir),
        "accepted_run_count": int(
            previous_inventory.get("data_quality", {}).get("accepted_run_count", previous_inventory.get("run_count", 0)) or 0
        ),
        "best_result": previous_best,
        "supported_anchor": previous_supported,
        "best_result_support": previous_best_support,
    }
    payload["deltas"] = {
        "best_result": {
            "median_test_r2_delta": _safe_float(current_best_summary.get("median_test_r2")) - _safe_float(previous_best_summary.get("median_test_r2")),
            "effective_condition_number_delta": _safe_float(current_best_summary.get("effective_condition_number"))
            - _safe_float(previous_best_summary.get("effective_condition_number")),
            "support_changed": current_best_support != previous_best_support,
            "combo_changed": _combo_key(current_best) != _combo_key(previous_best),
        },
        "supported_anchor": {
            "median_test_r2_delta": current_supported_r2 - previous_supported_r2,
            "effective_condition_number_delta": current_supported_condition - previous_supported_condition,
            "support_changed": str(current_supported.get("support", "")) != str(previous_supported.get("support", "")),
            "combo_changed": _combo_key(current_supported) != _combo_key(previous_supported),
        },
    }
    payload["sparsity_overlap"] = {
        "best_result": _overlap_payload(current_best_edges, previous_best_edges),
        "supported_anchor": _overlap_payload(current_supported_edges, previous_supported_edges),
    }
    return payload


def render_baseline_stability_markdown(payload: dict[str, Any]) -> str:
    if payload.get("status") != "comparison_available":
        return "\n".join(
            [
                "# Baseline Stability",
                "",
                "- comparison_status: `comparison_unavailable`",
                "- reason: no previous comparable study with fewer accepted runs was found.",
            ]
        )

    current = payload.get("current", {})
    previous = payload.get("previous", {})
    deltas = payload.get("deltas", {})
    overlap = payload.get("sparsity_overlap", {})
    current_best = current.get("best_result", {})
    previous_best = previous.get("best_result", {})
    current_supported = current.get("supported_anchor", {})
    previous_supported = previous.get("supported_anchor", {})
    current_best_summary = current_best.get("summary", {})
    previous_best_summary = previous_best.get("summary", {})
    current_supported_summary = current_supported.get("summary", {})
    previous_supported_summary = previous_supported.get("summary", {})

    return "\n".join(
        [
            "# Baseline Stability",
            "",
            "## Scope",
            f"- current_accepted_runs: {current.get('accepted_run_count', 0)}",
            f"- previous_accepted_runs: {previous.get('accepted_run_count', 0)}",
            f"- previous_study_dir: `{previous.get('study_dir', '')}`",
            "",
            "## Best Result",
            f"- current_combo: `{_combo_key(current_best)}`",
            f"- previous_combo: `{_combo_key(previous_best)}`",
            f"- current_support: `{current.get('best_result_support', '')}`",
            f"- previous_support: `{previous.get('best_result_support', '')}`",
            f"- current_median_test_r2: {_safe_float(current_best_summary.get('median_test_r2')):.4f}",
            f"- previous_median_test_r2: {_safe_float(previous_best_summary.get('median_test_r2')):.4f}",
            f"- delta_median_test_r2: {_safe_float(deltas.get('best_result', {}).get('median_test_r2_delta')):.4f}",
            f"- current_effective_condition_number: {_safe_float(current_best_summary.get('effective_condition_number')):.4f}",
            f"- previous_effective_condition_number: {_safe_float(previous_best_summary.get('effective_condition_number')):.4f}",
            f"- delta_effective_condition_number: {_safe_float(deltas.get('best_result', {}).get('effective_condition_number_delta')):.4f}",
            f"- best_result_sparsity_jaccard: {_safe_float(overlap.get('best_result', {}).get('jaccard_overlap')):.4f}",
            "",
            "## Supported Anchor",
            f"- current_combo: `{_combo_key(current_supported)}`",
            f"- previous_combo: `{_combo_key(previous_supported)}`",
            f"- current_support: `{current_supported.get('support', '')}`",
            f"- previous_support: `{previous_supported.get('support', '')}`",
            f"- current_median_test_r2: {_safe_float(current_supported.get('median_test_r2', current_supported_summary.get('median_test_r2'))):.4f}",
            f"- previous_median_test_r2: {_safe_float(previous_supported.get('median_test_r2', previous_supported_summary.get('median_test_r2'))):.4f}",
            f"- delta_median_test_r2: {_safe_float(deltas.get('supported_anchor', {}).get('median_test_r2_delta')):.4f}",
            f"- current_effective_condition_number: {_safe_float(current_supported.get('effective_condition_number', current_supported_summary.get('effective_condition_number'))):.4f}",
            f"- previous_effective_condition_number: {_safe_float(previous_supported.get('effective_condition_number', previous_supported_summary.get('effective_condition_number'))):.4f}",
            f"- delta_effective_condition_number: {_safe_float(deltas.get('supported_anchor', {}).get('effective_condition_number_delta')):.4f}",
            f"- supported_anchor_sparsity_jaccard: {_safe_float(overlap.get('supported_anchor', {}).get('jaccard_overlap')):.4f}",
        ]
    )


def _state_evolution_support_rank(support: str) -> int:
    return {
        "supported": 2,
        "partial": 1,
        "unsupported": 0,
        "skipped": -1,
    }.get(str(support).strip().lower(), -1)


def _iter_fit_metric_payloads(study_dir: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for metrics_path in sorted(study_dir.glob("fits/*/*/metrics.json")):
        combo_dir = metrics_path.parent.parent.name
        if "__" not in combo_dir:
            continue
        payload = read_yaml(metrics_path)
        x_schema = str(payload.get("x_schema", "")).strip()
        y_schema = str(payload.get("y_schema", "")).strip()
        pooling_mode = str(payload.get("pooling_mode", "")).strip()
        model_name = str(payload.get("model_name", metrics_path.parent.name)).strip()
        if not x_schema or not y_schema or not pooling_mode or not model_name:
            try:
                x_schema, y_schema, pooling_mode = combo_dir.split("__", 2)
            except ValueError:
                continue
            model_name = metrics_path.parent.name
        entries.append(
            {
                "metrics_path": metrics_path,
                "x_schema": x_schema,
                "y_schema": y_schema,
                "pooling_mode": pooling_mode,
                "model_name": model_name,
                "summary": payload,
            }
        )
    return entries


def _state_evolution_blockers(summary: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if _safe_float(summary.get("median_test_r2")) < 0.70:
        blockers.append("fit_quality")
    if _safe_float(summary.get("coefficient_stability")) < 0.60:
        blockers.append("stability")
    if _safe_float(summary.get("effective_condition_number")) > 1e6:
        blockers.append("condition_number")
    return blockers


def _primary_state_evolution_blocker(summary: dict[str, Any]) -> str:
    blockers = _state_evolution_blockers(summary)
    if not blockers:
        return "none"
    if len(blockers) == 1:
        return blockers[0]
    return "mixed"


def _state_evolution_entries(study_dir: Path) -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}
    for item in _iter_fit_metric_payloads(study_dir):
        x_schema = item["x_schema"]
        y_schema = item["y_schema"]
        if x_schema not in STATE_EVOLUTION_X_SCHEMAS or y_schema not in STATE_EVOLUTION_Y_SCHEMAS:
            continue
        summary = dict(item.get("summary", {}) or {})
        entry = {
            "x_schema": x_schema,
            "y_schema": y_schema,
            "pooling_mode": item["pooling_mode"],
            "model_name": item["model_name"],
            "support": classify_support(summary),
            "median_test_r2": _safe_float(summary.get("median_test_r2")),
            "effective_condition_number": _safe_float(summary.get("effective_condition_number")),
            "coefficient_stability": _safe_float(summary.get("coefficient_stability")),
            "sparsity_ratio": _safe_float(summary.get("sparsity_ratio")),
            "conditioning_pruned_features": list(summary.get("conditioning_pruned_features", []) or []),
            "primary_blocker": _primary_state_evolution_blocker(summary),
            "metrics_path": str(item["metrics_path"]),
        }
        entries[_combo_key(entry)] = entry
    return entries


def _state_evolution_transition_rows(
    current_entries: dict[str, dict[str, Any]],
    previous_entries: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for combo_key in sorted(set(current_entries) | set(previous_entries)):
        current_support = str(current_entries.get(combo_key, {}).get("support", "missing"))
        previous_support = str(previous_entries.get(combo_key, {}).get("support", "missing"))
        transition = f"{previous_support} -> {current_support}"
        rows.append(
            {
                "combo": combo_key,
                "previous_support": previous_support,
                "current_support": current_support,
                "transition": transition,
                "changed": str(previous_support != current_support).lower(),
            }
        )
    return rows


def build_state_evolution_audit_payload(
    current_study_dir: Path,
    study_name: str,
    current_inventory: dict[str, Any],
    current_manifest: dict[str, Any],
) -> dict[str, Any]:
    current_summary = read_yaml(current_study_dir / "summary" / "study_summary.json")
    current_entries = _state_evolution_entries(current_study_dir)
    current_supported_overall = _supported_combo_keys(current_summary)
    current_supported_state = sorted(
        combo_key for combo_key, entry in current_entries.items() if str(entry.get("support", "")).strip().lower() == "supported"
    )
    payload: dict[str, Any] = {
        "status": "audit_available" if current_entries else "audit_unavailable",
        "study_name": study_name,
        "current_study_dir": str(current_study_dir),
        "current": {
            "accepted_run_count": int(
                current_inventory.get("data_quality", {}).get("accepted_run_count", current_inventory.get("run_count", 0)) or 0
            ),
            "supported_overall": current_supported_overall,
            "supported_state_evolution": current_supported_state,
        },
        "previous": {},
        "comparison_status": "comparison_unavailable",
        "entries": sorted(
            current_entries.values(),
            key=lambda item: (
                _state_evolution_support_rank(str(item.get("support", ""))),
                _safe_float(item.get("median_test_r2")),
                -_safe_float(item.get("effective_condition_number")),
            ),
            reverse=True,
        ),
        "support_changes": [],
        "conclusion": "no targeted state-evolution fits were found in this study.",
    }
    if not current_entries:
        return payload

    previous_study_dir = _find_previous_comparable_study(current_study_dir, study_name, current_manifest, current_inventory)
    previous_entries: dict[str, dict[str, Any]] = {}
    previous_summary: dict[str, Any] = {}
    if previous_study_dir is not None:
        previous_inventory = read_yaml(previous_study_dir / "prepared" / "schema_inventory.yaml")
        previous_summary = read_yaml(previous_study_dir / "summary" / "study_summary.json")
        previous_entries = _state_evolution_entries(previous_study_dir)
        payload["comparison_status"] = "comparison_available"
        payload["previous"] = {
            "study_dir": str(previous_study_dir),
            "accepted_run_count": int(
                previous_inventory.get("data_quality", {}).get("accepted_run_count", previous_inventory.get("run_count", 0)) or 0
            ),
            "supported_overall": _supported_combo_keys(previous_summary),
            "supported_state_evolution": sorted(
                combo_key
                for combo_key, entry in previous_entries.items()
                if str(entry.get("support", "")).strip().lower() == "supported"
            ),
        }
        payload["support_changes"] = _state_evolution_transition_rows(current_entries, previous_entries)

    previous_supported_state = list(payload.get("previous", {}).get("supported_state_evolution", []))
    if current_supported_state and sorted(current_supported_state) != sorted(previous_supported_state):
        conclusion = "baseline 厚化改变了 ArduPilot 的 supported set，之前的 actuator-response-only 判断需要下调为阶段性结论。"
    else:
        dominant_blockers = Counter(entry["primary_blocker"] for entry in current_entries.values() if entry.get("primary_blocker") != "none")
        ordered_blockers = [name for name, _count in dominant_blockers.most_common()]
        blocker_text = "/".join(ordered_blockers[:2]) if ordered_blockers else "condition_number/stability"
        conclusion = (
            "厚化 baseline 没有改变 ArduPilot 当前明确 supported 的主集合，"
            f"state-evolution 路径的主阻塞仍然是 {blocker_text}，而不是单纯 R2 不够。"
        )
    payload["conclusion"] = conclusion
    return payload


def render_state_evolution_audit_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# State-Evolution Audit",
        "",
        f"- audit_status: `{payload.get('status', 'audit_unavailable')}`",
    ]
    if payload.get("status") != "audit_available":
        lines.append("- reason: no targeted state-evolution fits were found in this study.")
        return "\n".join(lines)

    current = payload.get("current", {})
    previous = payload.get("previous", {})
    lines.extend(
        [
            f"- current_accepted_runs: {current.get('accepted_run_count', 0)}",
            f"- comparison_status: `{payload.get('comparison_status', 'comparison_unavailable')}`",
        ]
    )
    if previous:
        lines.extend(
            [
                f"- previous_accepted_runs: {previous.get('accepted_run_count', 0)}",
                f"- previous_study_dir: `{previous.get('study_dir', '')}`",
            ]
        )
    lines.extend(
        [
            "",
            "## Supported Set Snapshot",
            f"- current_supported_overall_count: {len(current.get('supported_overall', []))}",
            f"- current_supported_state_evolution_count: {len(current.get('supported_state_evolution', []))}",
        ]
    )
    if previous:
        lines.extend(
            [
                f"- previous_supported_overall_count: {len(previous.get('supported_overall', []))}",
                f"- previous_supported_state_evolution_count: {len(previous.get('supported_state_evolution', []))}",
            ]
        )

    lines.extend(["", "## Current State-Evolution Combos"])
    for entry in payload.get("entries", []):
        pruned = ", ".join(entry.get("conditioning_pruned_features", [])) or "none"
        lines.append(
            f"- `{_combo_key(entry)}`: support={entry.get('support', '')}; "
            f"median_test_r2={_safe_float(entry.get('median_test_r2')):.4f}; "
            f"effective_condition_number={_safe_float(entry.get('effective_condition_number')):.4f}; "
            f"coefficient_stability={_safe_float(entry.get('coefficient_stability')):.4f}; "
            f"sparsity_ratio={_safe_float(entry.get('sparsity_ratio')):.4f}; "
            f"conditioning_pruned_features={pruned}; "
            f"primary_blocker={entry.get('primary_blocker', 'none')}"
        )

    lines.extend(["", "## Thickening Comparison"])
    changed_rows = [row for row in payload.get("support_changes", []) if row.get("changed") == "true"]
    if not changed_rows:
        lines.append("- no support transitions were observed across the targeted state-evolution combos.")
    else:
        for row in changed_rows:
            lines.append(
                f"- `{row['combo']}`: {row['transition']}"
            )

    lines.extend(["", "## Conclusion", f"- {payload.get('conclusion', '')}"])
    return "\n".join(lines)


def _scenario_generalization_status(
    support: str,
    scenario_consistency: float,
    subgroup_metrics: dict[str, Any],
    expected_scenarios: list[str],
) -> str:
    support_state = str(support).strip().lower()
    if support_state != "supported":
        return "not_generalized"
    subgroup_r2 = [
        _safe_float((subgroup_metrics.get(scenario, {}) or {}).get("r2"))
        for scenario in expected_scenarios
    ]
    if (
        math.isfinite(scenario_consistency)
        and scenario_consistency >= 0.60
        and subgroup_r2
        and all(math.isfinite(value) and value >= 0.70 for value in subgroup_r2)
    ):
        return "generalized_supported"
    return "supported_but_local"


def build_scenario_generalization_payload(
    study_dir: Path,
    study_name: str,
    study_manifest: dict[str, Any],
) -> dict[str, Any]:
    expected_scenarios = sorted(str(item) for item in (study_manifest.get("source_scenarios", []) or []) if str(item).strip())
    payload: dict[str, Any] = {
        "status": "scenario_unavailable",
        "study_name": study_name,
        "study_dir": str(study_dir),
        "expected_scenarios": expected_scenarios,
        "entries": [],
        "counts": {
            "generalized_supported": 0,
            "supported_but_local": 0,
            "not_generalized": 0,
        },
        "conclusion": "study 只覆盖单一 scenario，尚不能判断跨状态泛化。",
    }
    if len(expected_scenarios) < 2:
        return payload

    entries: list[dict[str, Any]] = []
    for item in _iter_fit_metric_payloads(study_dir):
        summary = dict(item.get("summary", {}) or {})
        support = classify_support(summary)
        subgroup_metrics = dict(summary.get("scenario_subgroup_metrics", {}) or {})
        scenario_consistency = _safe_float(summary.get("scenario_consistency"))
        generalization_status = _scenario_generalization_status(support, scenario_consistency, subgroup_metrics, expected_scenarios)
        subgroup_r2 = {
            scenario: _safe_float((subgroup_metrics.get(scenario, {}) or {}).get("r2"))
            for scenario in expected_scenarios
        }
        entries.append(
            {
                "x_schema": item["x_schema"],
                "y_schema": item["y_schema"],
                "pooling_mode": item["pooling_mode"],
                "model_name": item["model_name"],
                "support": support,
                "median_test_r2": _safe_float(summary.get("median_test_r2")),
                "effective_condition_number": _safe_float(summary.get("effective_condition_number")),
                "coefficient_stability": _safe_float(summary.get("coefficient_stability")),
                "scenario_consistency": scenario_consistency,
                "scenario_subgroup_metrics": subgroup_metrics,
                "scenario_subgroup_r2": subgroup_r2,
                "generalization_status": generalization_status,
                "high_local_scenarios": [
                    scenario
                    for scenario, r2_value in subgroup_r2.items()
                    if math.isfinite(r2_value) and r2_value >= 0.70
                ],
                "metrics_path": str(item["metrics_path"]),
            }
        )

    entries.sort(
        key=lambda item: (
            GENERALIZATION_STATUS_ORDER.get(str(item.get("generalization_status", "")), -1),
            _safe_float(item.get("median_test_r2")),
            _safe_float(item.get("scenario_consistency")),
        ),
        reverse=True,
    )
    counts = Counter(str(item.get("generalization_status", "not_generalized")) for item in entries)
    payload["status"] = "scenario_available"
    payload["entries"] = entries
    payload["counts"] = {
        "generalized_supported": int(counts.get("generalized_supported", 0)),
        "supported_but_local": int(counts.get("supported_but_local", 0)),
        "not_generalized": int(counts.get("not_generalized", 0)),
    }

    generalized_supported = [item for item in entries if item.get("generalization_status") == "generalized_supported"]
    supported_but_local = [item for item in entries if item.get("generalization_status") == "supported_but_local"]
    if generalized_supported:
        payload["conclusion"] = "当前 study 里已经出现跨 scenario 仍然保持 supported 的组合，f 更像常见映射而不是单一 operating-point 拟合。"
    elif supported_but_local:
        payload["conclusion"] = "当前 supported 组合更像局部 operating-point 映射；它们 pooled 后仍能过 support，但跨 scenario 的一致性还不够强。"
    else:
        payload["conclusion"] = "当前 study 尚未给出跨 scenario generalized_supported 的组合，高分结果更像局部状态下的线性近似。"
    return payload


def render_scenario_generalization_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Scenario Generalization",
        "",
        f"- status: `{payload.get('status', 'scenario_unavailable')}`",
        f"- expected_scenarios: {', '.join(payload.get('expected_scenarios', [])) or 'none'}",
    ]
    if payload.get("status") != "scenario_available":
        lines.append(f"- reason: {payload.get('conclusion', 'scenario coverage is insufficient.')}")
        return "\n".join(lines)

    counts = payload.get("counts", {})
    lines.extend(
        [
            "",
            "## Status Counts",
            f"- generalized_supported: {int(counts.get('generalized_supported', 0))}",
            f"- supported_but_local: {int(counts.get('supported_but_local', 0))}",
            f"- not_generalized: {int(counts.get('not_generalized', 0))}",
            "",
            "## Combo Reading",
        ]
    )
    for entry in payload.get("entries", []):
        subgroup_text = ", ".join(
            f"{scenario}={_safe_float(value):.4f}"
            for scenario, value in entry.get("scenario_subgroup_r2", {}).items()
        ) or "none"
        lines.append(
            f"- `{_combo_key(entry)}`: generalization_status={entry.get('generalization_status', 'unknown')}; "
            f"support={entry.get('support', '')}; median_test_r2={_safe_float(entry.get('median_test_r2')):.4f}; "
            f"scenario_consistency={_safe_float(entry.get('scenario_consistency')):.4f}; subgroup_r2=[{subgroup_text}]"
        )
    lines.extend(["", "## Conclusion", f"- {payload.get('conclusion', '')}"])
    return "\n".join(lines)


def _diagnostic_records(run_dirs: list[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for run_dir in run_dirs:
        manifest_path = run_dir / "manifest.yaml"
        if not manifest_path.exists():
            continue
        manifest = read_yaml(manifest_path)
        study_config = manifest.get("study_config", {}) or {}
        extras = study_config.get("extras", {}) if isinstance(study_config, dict) else {}
        axis = str(manifest.get("axis", study_config.get("axis", ""))).strip().lower()
        amplitude_tier = str(extras.get("amplitude_tier", "")).strip().lower()
        if not axis or not amplitude_tier:
            continue
        records.append(
            {
                "run_id": str(manifest.get("run_id", run_dir.name)),
                "mode": str(manifest.get("flight_mode", study_config.get("flight_mode", ""))).strip(),
                "axis": axis,
                "amplitude_tier": amplitude_tier,
                "research_acceptance": str(manifest.get("research_acceptance", "")).strip().lower(),
                "research_rejection_reasons": list(manifest.get("research_rejection_reasons", []) or []),
            }
        )
    return records


def build_diagnostic_gate_payload(run_dirs: list[Path]) -> dict[str, Any]:
    records = _diagnostic_records(run_dirs)
    payload: dict[str, Any] = {
        "status": "diagnostic_unavailable",
        "run_count": len(records),
        "attitude_axes": [],
        "throttle": [],
        "conclusion": "no diagnostic gate rows with axis/amplitude_tier were found.",
    }
    if not records:
        return payload

    grouped: dict[tuple[str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for record in records:
        mode = record["mode"]
        axis = record["axis"]
        tier = record["amplitude_tier"]
        tier_bucket = grouped[(mode, axis)].setdefault(
            tier,
            {
                "attempt_count": 0,
                "accepted_count": 0,
                "rejected_count": 0,
                "rejection_reasons": Counter(),
            },
        )
        tier_bucket["attempt_count"] += 1
        if record["research_acceptance"] == "accepted":
            tier_bucket["accepted_count"] += 1
        else:
            tier_bucket["rejected_count"] += 1
            tier_bucket["rejection_reasons"].update(record["research_rejection_reasons"])

    attitude_sections: list[dict[str, Any]] = []
    throttle_sections: list[dict[str, Any]] = []
    for (mode, axis), tier_map in sorted(grouped.items()):
        tiers: list[dict[str, Any]] = []
        first_problem_tier = "none"
        dominant_reasons: list[str] = []
        for tier in AMPLITUDE_TIER_ORDER:
            bucket = tier_map.get(
                tier,
                {
                    "attempt_count": 0,
                    "accepted_count": 0,
                    "rejected_count": 0,
                    "rejection_reasons": Counter(),
                },
            )
            reasons = [reason for reason, _count in bucket["rejection_reasons"].most_common()]
            if first_problem_tier == "none" and bucket["rejected_count"] > 0:
                first_problem_tier = tier
                dominant_reasons = reasons
            tiers.append(
                {
                    "amplitude_tier": tier,
                    "attempt_count": bucket["attempt_count"],
                    "accepted_count": bucket["accepted_count"],
                    "rejected_count": bucket["rejected_count"],
                    "rejection_reasons": reasons,
                }
            )
        section = {
            "mode": mode,
            "axis": axis,
            "tiers": tiers,
            "all_accepted": all(item["attempt_count"] > 0 and item["rejected_count"] == 0 for item in tiers),
            "first_problem_tier": first_problem_tier,
            "dominant_rejection_reasons": dominant_reasons,
        }
        if axis == "throttle":
            throttle_sections.append(section)
        else:
            attitude_sections.append(section)

    attitude_clean = bool(attitude_sections) and all(section["all_accepted"] for section in attitude_sections)
    throttle_problem = any(section["first_problem_tier"] != "none" for section in throttle_sections)
    if attitude_clean and throttle_problem:
        conclusion = "姿态轴在当前诊断矩阵内保持 accepted；throttle 是最早系统性出问题的通道。"
    elif attitude_clean:
        conclusion = "姿态轴在当前诊断矩阵内保持 accepted，throttle 暂未出现系统性拒收。"
    else:
        conclusion = "当前诊断矩阵里不只 throttle，姿态轴也出现了 acceptance 边界问题。"

    payload["status"] = "diagnostic_available"
    payload["attitude_axes"] = attitude_sections
    payload["throttle"] = throttle_sections
    payload["conclusion"] = conclusion
    return payload


def render_diagnostic_gate_markdown(payload: dict[str, Any]) -> str:
    if payload.get("status") != "diagnostic_available":
        return "\n".join(
            [
                "# Diagnostic Gate",
                "",
                "- diagnostic_status: `diagnostic_unavailable`",
                "- reason: no diagnostic rows with `axis` and `amplitude_tier` were found.",
            ]
        )

    lines = [
        "# Diagnostic Gate",
        "",
        "## Attitude Axes",
    ]
    attitude_sections = payload.get("attitude_axes", [])
    if not attitude_sections:
        lines.append("- none")
    for section in attitude_sections:
        tier_text = ", ".join(
            f"{tier['amplitude_tier']}: {tier['accepted_count']}A/{tier['rejected_count']}R"
            for tier in section.get("tiers", [])
        )
        lines.append(
            f"- `{section['mode']} {section['axis']}`: {tier_text}; first_problem_tier={section['first_problem_tier']}"
        )

    lines.extend(["", "## Throttle"])
    throttle_sections = payload.get("throttle", [])
    if not throttle_sections:
        lines.append("- none")
    for section in throttle_sections:
        tier_text = ", ".join(
            f"{tier['amplitude_tier']}: {tier['accepted_count']}A/{tier['rejected_count']}R"
            for tier in section.get("tiers", [])
        )
        reasons = ", ".join(section.get("dominant_rejection_reasons", [])) or "none"
        lines.append(
            f"- `{section['mode']} throttle`: {tier_text}; first_problem_tier={section['first_problem_tier']}; reasons={reasons}"
        )

    lines.extend(["", "## Conclusion", f"- {payload.get('conclusion', '')}"])
    return "\n".join(lines)


def _mode_entry_result(anomalies: list[str], failure_reason: str, target_mode: str, experiment_started: bool) -> str:
    if f"mode_unavailable:{target_mode}" in anomalies:
        return "mode_unavailable"
    if f"mode_not_confirmed:{target_mode}" in anomalies:
        return "mode_not_confirmed"
    if experiment_started:
        return "confirmed"
    if failure_reason:
        return failure_reason
    return "unknown"


def build_guided_mode_smoke_payload(
    run_dirs: list[Path],
    *,
    target_mode: str = "GUIDED_NOGPS",
    target_consecutive_runs: int = 3,
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for run_dir in run_dirs:
        manifest_path = run_dir / "manifest.yaml"
        if not manifest_path.exists():
            continue
        manifest = read_yaml(manifest_path)
        acceptance = ((manifest.get("data_quality", {}) or {}).get("acceptance", {}) or {})
        runtime_report = manifest.get("runtime_report", {}) or {}
        anomalies = list(manifest.get("anomaly_summary", []) or [])
        experiment_started = bool(acceptance.get("experiment_started"))
        active_phase_present = bool(acceptance.get("active_phase_present"))
        records.append(
            {
                "run_id": str(manifest.get("run_id", run_dir.name)),
                "flight_mode": str(manifest.get("flight_mode", "")),
                "status": str(manifest.get("status", "")),
                "research_acceptance": str(manifest.get("research_acceptance", "")),
                "mode_entry_result": _mode_entry_result(
                    anomalies,
                    str(manifest.get("failure_reason", "")),
                    target_mode,
                    experiment_started,
                ),
                "experiment_started": experiment_started,
                "active_phase_present": active_phase_present,
                "failure_reason": str(manifest.get("failure_reason", "")),
                "completion_reason": str(runtime_report.get("completion_reason", "")),
                "research_rejection_reasons": list(manifest.get("research_rejection_reasons", []) or []),
                "anomalies": anomalies,
            }
        )

    payload: dict[str, Any] = {
        "status": "smoke_unavailable",
        "target_mode": target_mode,
        "target_consecutive_runs": int(target_consecutive_runs),
        "longest_consecutive_active_phase_runs": 0,
        "passed": False,
        "runs": records,
        "conclusion": "no raw manifests were available for smoke evaluation.",
    }
    if not records:
        return payload

    longest_streak = 0
    current_streak = 0
    for record in records:
        run_ok = bool(record["experiment_started"] and record["active_phase_present"])
        if run_ok:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 0

    passed = longest_streak >= max(1, int(target_consecutive_runs))
    if passed:
        conclusion = f"{target_mode} mode-entry smoke reached the required active-phase streak."
    else:
        conclusion = (
            f"{target_mode} mode-entry smoke is still blocked before a stable "
            f"{max(1, int(target_consecutive_runs))}-run active-phase streak."
        )

    payload["status"] = "smoke_available"
    payload["longest_consecutive_active_phase_runs"] = longest_streak
    payload["passed"] = passed
    payload["conclusion"] = conclusion
    return payload


def render_guided_mode_smoke_markdown(payload: dict[str, Any]) -> str:
    if payload.get("status") != "smoke_available":
        return "\n".join(
            [
                "# GUIDED_NOGPS Smoke",
                "",
                "- smoke_status: `smoke_unavailable`",
                "- reason: no raw manifests were available for smoke evaluation.",
            ]
        )

    lines = [
        "# GUIDED_NOGPS Smoke",
        "",
        f"- target_mode: `{payload.get('target_mode', '')}`",
        f"- target_consecutive_runs: {payload.get('target_consecutive_runs', 0)}",
        f"- longest_consecutive_active_phase_runs: {payload.get('longest_consecutive_active_phase_runs', 0)}",
        f"- passed: `{str(bool(payload.get('passed'))).lower()}`",
        "",
        "## Runs",
    ]
    for record in payload.get("runs", []):
        reasons = ",".join(record.get("research_rejection_reasons", [])) or "none"
        lines.append(
            f"- `{record['run_id']}`: mode_entry={record['mode_entry_result']}; "
            f"experiment_started={str(bool(record['experiment_started'])).lower()}; "
            f"active_phase_present={str(bool(record['active_phase_present'])).lower()}; "
            f"completion_reason={record['completion_reason'] or 'none'}; "
            f"failure_reason={record['failure_reason'] or 'none'}; "
            f"rejection_reasons={reasons}"
        )
    lines.extend(["", "## Conclusion", f"- {payload.get('conclusion', '')}"])
    return "\n".join(lines)


def _key_diff(left: list[str], right: list[str]) -> dict[str, list[str]]:
    left_set = set(left)
    right_set = set(right)
    return {
        "shared": sorted(left_set & right_set),
        "px4_only": sorted(left_set - right_set),
        "ardupilot_only": sorted(right_set - left_set),
    }


def build_contract_audit_payload(px4_run_dir: Path, ardupilot_run_dir: Path) -> dict[str, Any]:
    px4_manifest = read_yaml(px4_run_dir / "manifest.yaml")
    ardupilot_manifest = read_yaml(ardupilot_run_dir / "manifest.yaml")
    px4_acceptance = ((px4_manifest.get("data_quality", {}) or {}).get("acceptance", {}) or {})
    ardupilot_acceptance = ((ardupilot_manifest.get("data_quality", {}) or {}).get("acceptance", {}) or {})
    px4_config = StudyConfig.from_dict(px4_manifest.get("study_config", {}) or {})
    table, inventory = build_prepared_sample_table([px4_run_dir, ardupilot_run_dir], px4_config)
    fieldnames = prepared_sample_table_fieldnames(table.rows)
    identity_columns = fieldnames[: len(PREPARED_SAMPLE_IDENTITY_COLUMNS)]
    prefix_presence = {prefix: any(name.startswith(prefix) for name in fieldnames) for prefix in CONTRACT_PREFIXES}

    schema_naming = {
        "px4": {
            "x_schema": str((px4_manifest.get("study_config", {}) or {}).get("x_schema", "")),
            "y_schema": str((px4_manifest.get("study_config", {}) or {}).get("y_schema", "")),
        },
        "ardupilot": {
            "x_schema": str((ardupilot_manifest.get("study_config", {}) or {}).get("x_schema", "")),
            "y_schema": str((ardupilot_manifest.get("study_config", {}) or {}).get("y_schema", "")),
        },
    }
    schema_naming["exact_match"] = schema_naming["px4"] == schema_naming["ardupilot"]

    manifest_keys = _key_diff(sorted(px4_manifest.keys()), sorted(ardupilot_manifest.keys()))
    acceptance_keys = _key_diff(sorted(px4_acceptance.keys()), sorted(ardupilot_acceptance.keys()))
    required_manifest_keys_present = all(
        key in px4_manifest and key in ardupilot_manifest for key in CONTRACT_REQUIRED_MANIFEST_KEYS
    )
    identity_columns_match = identity_columns == PREPARED_SAMPLE_IDENTITY_COLUMNS
    prefix_contract_ok = all(prefix_presence.values())
    acceptance_exact_match = not acceptance_keys["px4_only"] and not acceptance_keys["ardupilot_only"]
    contract_ok = all(
        (
            required_manifest_keys_present,
            acceptance_exact_match,
            identity_columns_match,
            prefix_contract_ok,
            bool(schema_naming["exact_match"]),
        )
    )

    if contract_ok:
        conclusion = "Cross-backend contract audit passed on manifest contract keys, acceptance keys, prepared identity columns, prefixes, and schema naming."
    else:
        conclusion = "Cross-backend contract audit found a contract mismatch that needs to be resolved before comparing backend results."

    return {
        "status": "audit_available",
        "px4_run_dir": str(px4_run_dir),
        "ardupilot_run_dir": str(ardupilot_run_dir),
        "run_acceptance": {
            "px4": manifest_acceptance_state(px4_manifest),
            "ardupilot": manifest_acceptance_state(ardupilot_manifest),
        },
        "manifest_keys": {
            **manifest_keys,
            "required_contract_keys": list(CONTRACT_REQUIRED_MANIFEST_KEYS),
            "required_contract_keys_present_in_both": required_manifest_keys_present,
        },
        "acceptance_keys": {
            **acceptance_keys,
            "exact_match": acceptance_exact_match,
        },
        "prepared_sample_table": {
            "row_count": len(table.rows),
            "accepted_run_count": int(inventory.get("data_quality", {}).get("accepted_run_count", 0) or 0),
            "fieldnames": fieldnames,
            "identity_columns": identity_columns,
            "identity_columns_match": identity_columns_match,
            "prefix_presence": prefix_presence,
            "prefix_contract_ok": prefix_contract_ok,
        },
        "schema_naming": schema_naming,
        "contract_ok": contract_ok,
        "conclusion": conclusion,
    }


def render_contract_audit_markdown(payload: dict[str, Any]) -> str:
    if payload.get("status") != "audit_available":
        return "\n".join(
            [
                "# Contract Audit",
                "",
                "- audit_status: `audit_unavailable`",
            ]
        )

    manifest_keys = payload.get("manifest_keys", {})
    acceptance_keys = payload.get("acceptance_keys", {})
    prepared = payload.get("prepared_sample_table", {})
    schema_naming = payload.get("schema_naming", {})
    lines = [
        "# Contract Audit",
        "",
        "## Raw Manifest",
        f"- required_contract_keys_present_in_both: `{str(bool(manifest_keys.get('required_contract_keys_present_in_both'))).lower()}`",
        f"- px4_only_keys: {', '.join(manifest_keys.get('px4_only', [])) or 'none'}",
        f"- ardupilot_only_keys: {', '.join(manifest_keys.get('ardupilot_only', [])) or 'none'}",
        "",
        "## Acceptance Keys",
        f"- exact_match: `{str(bool(acceptance_keys.get('exact_match'))).lower()}`",
        f"- px4_only_keys: {', '.join(acceptance_keys.get('px4_only', [])) or 'none'}",
        f"- ardupilot_only_keys: {', '.join(acceptance_keys.get('ardupilot_only', [])) or 'none'}",
        "",
        "## Prepared Sample Table",
        f"- identity_columns_match: `{str(bool(prepared.get('identity_columns_match'))).lower()}`",
        f"- identity_columns: {', '.join(prepared.get('identity_columns', [])) or 'none'}",
        f"- prefix_contract_ok: `{str(bool(prepared.get('prefix_contract_ok'))).lower()}`",
    ]
    for prefix, present in prepared.get("prefix_presence", {}).items():
        lines.append(f"- prefix `{prefix}` present: `{str(bool(present)).lower()}`")
    lines.extend(
        [
            "",
            "## Schema Naming",
            f"- px4: `{schema_naming.get('px4', {}).get('x_schema', '')} -> {schema_naming.get('px4', {}).get('y_schema', '')}`",
            f"- ardupilot: `{schema_naming.get('ardupilot', {}).get('x_schema', '')} -> {schema_naming.get('ardupilot', {}).get('y_schema', '')}`",
            f"- exact_match: `{str(bool(schema_naming.get('exact_match'))).lower()}`",
            "",
            "## Conclusion",
            f"- contract_ok: `{str(bool(payload.get('contract_ok'))).lower()}`",
            f"- {payload.get('conclusion', '')}",
        ]
    )
    return "\n".join(lines)


def _load_study_inventory(study_dir: Path) -> dict[str, Any]:
    return read_yaml(study_dir / "prepared" / "schema_inventory.yaml")


def _load_study_summary(study_dir: Path) -> dict[str, Any]:
    return read_yaml(study_dir / "summary" / "study_summary.json")


def _load_study_manifest(study_dir: Path) -> dict[str, Any]:
    return read_yaml(study_dir / "manifest.yaml")


def _load_baseline_stability(study_dir: Path) -> dict[str, Any]:
    path = study_dir / "summary" / "baseline_stability.json"
    if path.exists():
        return read_yaml(path)
    manifest = _load_study_manifest(study_dir)
    summary = _load_study_summary(study_dir)
    inventory = _load_study_inventory(study_dir)
    study_name = str(manifest.get("study_name", "")).strip()
    if not study_name or not summary:
        return {}
    return build_baseline_stability_payload(study_dir, study_name, summary, inventory, manifest)


def _load_diagnostic_gate(study_dir: Path) -> dict[str, Any]:
    path = study_dir / "summary" / "diagnostic_gate.json"
    if path.exists():
        return read_yaml(path)
    manifest = _load_study_manifest(study_dir)
    run_dirs = [Path(value).expanduser() for value in manifest.get("source_run_dirs", []) or []]
    return build_diagnostic_gate_payload(run_dirs)


def _load_scenario_generalization(study_dir: Path) -> dict[str, Any]:
    path = study_dir / "summary" / "scenario_generalization.json"
    if path.exists():
        return read_yaml(path)
    manifest = _load_study_manifest(study_dir)
    return build_scenario_generalization_payload(study_dir, str(manifest.get("study_name", "")), manifest)


def _study_acceptance_count(study_dir: Path) -> int:
    inventory = _load_study_inventory(study_dir)
    return int(inventory.get("data_quality", {}).get("accepted_run_count", inventory.get("run_count", 0)) or 0)


def _baseline_stability_state(accepted_run_count: int, expected_run_count: int, payload: dict[str, Any]) -> str:
    if accepted_run_count < expected_run_count or expected_run_count <= 0:
        return "not_ready"
    if payload.get("status") != "comparison_available":
        return "unknown"
    best_delta = payload.get("deltas", {}).get("best_result", {})
    supported_delta = payload.get("deltas", {}).get("supported_anchor", {})
    stable = not any(
        (
            bool(best_delta.get("combo_changed")),
            bool(best_delta.get("support_changed")),
            bool(supported_delta.get("combo_changed")),
            bool(supported_delta.get("support_changed")),
        )
    )
    return "stable" if stable else "changed"


def _inferred_accepted_runs_per_mode(source_modes: list[str], accepted_run_count: int, default: int = 5) -> int:
    mode_count = max(1, len(source_modes))
    if accepted_run_count > 0 and accepted_run_count % mode_count == 0:
        inferred = accepted_run_count // mode_count
        if inferred >= 1:
            return inferred
    return default


def _best_combo_text(summary: dict[str, Any]) -> str:
    best = dict(summary.get("best_result", {}) or {})
    return _combo_key(best)


def _baseline_section(study_dir: Path, *, accepted_runs_per_mode: int = 5) -> dict[str, Any]:
    manifest = _load_study_manifest(study_dir)
    summary = _load_study_summary(study_dir)
    baseline_stability = _load_baseline_stability(study_dir)
    source_modes = sorted(manifest.get("source_modes", []) or [])
    accepted_run_count = _study_acceptance_count(study_dir)
    inferred_runs_per_mode = _inferred_accepted_runs_per_mode(source_modes, accepted_run_count, default=accepted_runs_per_mode)
    expected_run_count = inferred_runs_per_mode * len(source_modes)
    supported_anchor = _supported_anchor(summary)
    state = _baseline_stability_state(accepted_run_count, expected_run_count, baseline_stability)
    return {
        "study_dir": str(study_dir),
        "study_name": str(manifest.get("study_name", "")),
        "source_modes": source_modes,
        "accepted_run_count": accepted_run_count,
        "accepted_runs_per_mode": inferred_runs_per_mode,
        "expected_accepted_run_count": expected_run_count,
        "baseline_stability_state": state,
        "baseline_stability_status": str(baseline_stability.get("status", "comparison_unavailable")),
        "best_combo": _best_combo_text(summary),
        "best_median_test_r2": _safe_float(
            ((summary.get("best_result", {}) or {}).get("summary", {}) or {}).get("median_test_r2")
        ),
        "supported_anchor": _combo_key(supported_anchor),
        "supported_anchor_support": str(supported_anchor.get("support", "")),
    }


def _diagnostic_section(study_dir: Path) -> dict[str, Any]:
    payload = _load_diagnostic_gate(study_dir)
    attitude_sections = list(payload.get("attitude_axes", []) or [])
    throttle_sections = list(payload.get("throttle", []) or [])
    accepted_attitude = sorted(f"{section['mode']} {section['axis']}" for section in attitude_sections if section.get("all_accepted"))
    rejected_attitude = sorted(f"{section['mode']} {section['axis']}" for section in attitude_sections if not section.get("all_accepted"))
    overall_first_problem_tiers = sorted(
        {
            str(section.get("first_problem_tier", "none"))
            for section in throttle_sections
            if str(section.get("first_problem_tier", "none")) != "none"
        }
    )
    dominant_reasons = sorted(
        {
            reason
            for section in throttle_sections
            for reason in section.get("dominant_rejection_reasons", [])
        }
    )
    if not overall_first_problem_tiers:
        throttle_boundary = "none"
    elif len(overall_first_problem_tiers) == 1:
        throttle_boundary = overall_first_problem_tiers[0]
    else:
        throttle_boundary = "mixed"
    return {
        "study_dir": str(study_dir),
        "study_name": str(_load_study_manifest(study_dir).get("study_name", "")),
        "diagnostic_status": str(payload.get("status", "diagnostic_unavailable")),
        "attitude_all_accepted": bool(attitude_sections) and not rejected_attitude,
        "accepted_attitude_axes": accepted_attitude,
        "rejected_attitude_axes": rejected_attitude,
        "throttle_boundary": throttle_boundary,
        "throttle_blocked_by_nonzero_gate": NONZERO_GATE_REASON in dominant_reasons,
        "throttle_rejection_reasons": dominant_reasons,
        "conclusion": str(payload.get("conclusion", "")),
    }


def _scenario_generalization_entry(payload: dict[str, Any], status: str) -> dict[str, Any]:
    for entry in payload.get("entries", []) or []:
        if str(entry.get("generalization_status", "")).strip() == status:
            return dict(entry)
    return {}


def _scenario_generalization_section(study_dir: Path) -> dict[str, Any]:
    payload = _load_scenario_generalization(study_dir)
    counts = dict(payload.get("counts", {}) or {})
    generalized = _scenario_generalization_entry(payload, "generalized_supported")
    local = _scenario_generalization_entry(payload, "supported_but_local")
    return {
        "study_dir": str(study_dir),
        "status": str(payload.get("status", "scenario_unavailable")),
        "expected_scenarios": list(payload.get("expected_scenarios", []) or []),
        "counts": {
            "generalized_supported": int(counts.get("generalized_supported", 0) or 0),
            "supported_but_local": int(counts.get("supported_but_local", 0) or 0),
            "not_generalized": int(counts.get("not_generalized", 0) or 0),
        },
        "representative_generalized_supported": _combo_key(generalized),
        "representative_supported_but_local": _combo_key(local),
        "conclusion": str(payload.get("conclusion", "")),
    }


def _generalization_counts(section: dict[str, Any]) -> tuple[int, int, int]:
    counts = dict(section.get("counts", {}) or {})
    return (
        int(counts.get("generalized_supported", 0) or 0),
        int(counts.get("supported_but_local", 0) or 0),
        int(counts.get("not_generalized", 0) or 0),
    )


def _generalization_difference(
    px4_baseline: dict[str, Any],
    ardupilot_baseline: dict[str, Any],
    px4_diagnostic: dict[str, Any],
    ardupilot_diagnostic: dict[str, Any],
) -> tuple[str, str]:
    px4_baseline_gen, _, _ = _generalization_counts(px4_baseline["scenario_generalization"])
    px4_diag_gen, _, _ = _generalization_counts(px4_diagnostic["scenario_generalization"])
    ap_baseline_gen, _, _ = _generalization_counts(ardupilot_baseline["scenario_generalization"])
    ap_diag_gen, _, _ = _generalization_counts(ardupilot_diagnostic["scenario_generalization"])
    px4_total = px4_baseline_gen + px4_diag_gen
    ap_total = ap_baseline_gen + ap_diag_gen

    if px4_total > 0 and ap_total > 0:
        if px4_total >= (ap_total * 2) and (px4_total - ap_total) >= 10:
            return (
                "both_support_cross_scenario_linearity_but_px4_is_broader",
                "两边都已给出跨 scenario 的正面线性证据，但 PX4 的 generalized-supported 组合明显更多。",
            )
        return (
            "both_support_cross_scenario_linearity",
            "两边都已给出跨 scenario 的正面线性证据，而且 generalized-supported 规模接近。",
        )
    if px4_total > 0:
        return (
            "px4_only_cross_scenario_linearity",
            "当前只有 PX4 明确给出 generalized-supported 证据，ArduPilot 还没有形成对称结论。",
        )
    if ap_total > 0:
        return (
            "ardupilot_only_cross_scenario_linearity",
            "当前只有 ArduPilot 明确给出 generalized-supported 证据，PX4 还没有形成对称结论。",
        )
    return (
        "no_cross_scenario_linearity",
        "当前两边都还没有 generalized-supported 组合，跨 scenario 线性结论仍未站稳。",
    )


def build_backend_compare_payload(
    px4_baseline_dir: Path,
    ardupilot_baseline_dir: Path,
    px4_diagnostic_dir: Path,
    ardupilot_diagnostic_dir: Path,
) -> dict[str, Any]:
    px4_baseline = _baseline_section(px4_baseline_dir)
    ardupilot_baseline = _baseline_section(ardupilot_baseline_dir)
    px4_diagnostic = _diagnostic_section(px4_diagnostic_dir)
    ardupilot_diagnostic = _diagnostic_section(ardupilot_diagnostic_dir)
    px4_baseline["scenario_generalization"] = _scenario_generalization_section(px4_baseline_dir)
    ardupilot_baseline["scenario_generalization"] = _scenario_generalization_section(ardupilot_baseline_dir)
    px4_diagnostic["scenario_generalization"] = _scenario_generalization_section(px4_diagnostic_dir)
    ardupilot_diagnostic["scenario_generalization"] = _scenario_generalization_section(ardupilot_diagnostic_dir)

    throttle_boundary_consistent = px4_diagnostic["throttle_boundary"] == ardupilot_diagnostic["throttle_boundary"]
    both_baselines_stable = (
        px4_baseline["baseline_stability_state"] == "stable"
        and ardupilot_baseline["baseline_stability_state"] == "stable"
    )
    attitude_pattern_consistent = (
        px4_diagnostic["attitude_all_accepted"] == ardupilot_diagnostic["attitude_all_accepted"]
        and len(px4_diagnostic["rejected_attitude_axes"]) == len(ardupilot_diagnostic["rejected_attitude_axes"])
    )

    if not both_baselines_stable:
        difference_driver = "baseline_stability_unresolved"
        conclusion = "当前差异更像 baseline 还不够稳，暂时不适合把 backend 差异当作主解释。"
    elif not throttle_boundary_consistent or not attitude_pattern_consistent:
        difference_driver = "backend_difference_more_likely"
        conclusion = "在 baseline 已稳定的前提下，当前差异更像 backend 差异。"
    else:
        difference_driver = "no_clear_backend_difference_from_gate_reports"
        conclusion = "两边在当前 gate 报告上的边界相近，暂时不能仅凭 gate 报告支持 backend 差异。"

    generalization_difference_driver, generalization_conclusion = _generalization_difference(
        px4_baseline,
        ardupilot_baseline,
        px4_diagnostic,
        ardupilot_diagnostic,
    )

    return {
        "status": "compare_available",
        "px4": {
            "baseline": px4_baseline,
            "diagnostic": px4_diagnostic,
        },
        "ardupilot": {
            "baseline": ardupilot_baseline,
            "diagnostic": ardupilot_diagnostic,
        },
        "comparison": {
            "both_baselines_stable": both_baselines_stable,
            "throttle_boundary_consistent": throttle_boundary_consistent,
            "difference_driver": difference_driver,
            "generalization_difference_driver": generalization_difference_driver,
        },
        "conclusion": f"{conclusion} {generalization_conclusion}".strip(),
    }


def render_backend_compare_markdown(payload: dict[str, Any]) -> str:
    if payload.get("status") != "compare_available":
        return "\n".join(
            [
                "# Backend Compare",
                "",
                "- compare_status: `compare_unavailable`",
            ]
        )

    px4_baseline = payload.get("px4", {}).get("baseline", {})
    ap_baseline = payload.get("ardupilot", {}).get("baseline", {})
    px4_diag = payload.get("px4", {}).get("diagnostic", {})
    ap_diag = payload.get("ardupilot", {}).get("diagnostic", {})
    comparison = payload.get("comparison", {})

    def _axes_text(section: dict[str, Any]) -> str:
        accepted = ", ".join(section.get("accepted_attitude_axes", [])) or "none"
        rejected = ", ".join(section.get("rejected_attitude_axes", [])) or "none"
        return f"accepted={accepted}; rejected={rejected}"

    def _baseline_text(section: dict[str, Any]) -> str:
        return (
            f"accepted_runs={section.get('accepted_run_count', 0)}/{section.get('expected_accepted_run_count', 0)}; "
            f"stability={section.get('baseline_stability_state', 'unknown')}; "
            f"best_combo={section.get('best_combo', '')}"
        )

    def _scenario_text(section: dict[str, Any]) -> str:
        scenario = dict(section.get("scenario_generalization", {}) or {})
        counts = dict(scenario.get("counts", {}) or {})
        return (
            f"generalized_supported={int(counts.get('generalized_supported', 0) or 0)}; "
            f"supported_but_local={int(counts.get('supported_but_local', 0) or 0)}; "
            f"not_generalized={int(counts.get('not_generalized', 0) or 0)}; "
            f"representative={scenario.get('representative_generalized_supported', '') or 'none'}"
        )

    return "\n".join(
        [
            "# Backend Compare",
            "",
            "## Baseline",
            f"- `PX4`: {_baseline_text(px4_baseline)}",
            f"- `ArduPilot`: {_baseline_text(ap_baseline)}",
            f"- both_baselines_stable: `{str(bool(comparison.get('both_baselines_stable'))).lower()}`",
            "",
            "## Diagnostic Gate",
            f"- `PX4` attitude: {_axes_text(px4_diag)}",
            f"- `ArduPilot` attitude: {_axes_text(ap_diag)}",
            f"- `PX4` throttle_boundary: `{px4_diag.get('throttle_boundary', 'none')}`; reasons={', '.join(px4_diag.get('throttle_rejection_reasons', [])) or 'none'}",
            f"- `ArduPilot` throttle_boundary: `{ap_diag.get('throttle_boundary', 'none')}`; reasons={', '.join(ap_diag.get('throttle_rejection_reasons', [])) or 'none'}",
            f"- throttle_boundary_consistent: `{str(bool(comparison.get('throttle_boundary_consistent'))).lower()}`",
            "",
            "## Scenario Generalization",
            f"- `PX4` baseline: {_scenario_text(px4_baseline)}",
            f"- `PX4` diagnostic: {_scenario_text(px4_diag)}",
            f"- `ArduPilot` baseline: {_scenario_text(ap_baseline)}",
            f"- `ArduPilot` diagnostic: {_scenario_text(ap_diag)}",
            f"- generalization_difference_driver: `{comparison.get('generalization_difference_driver', '')}`",
            "",
            "## Conclusion",
            f"- difference_driver: `{comparison.get('difference_driver', '')}`",
            f"- {payload.get('conclusion', '')}",
        ]
    )
