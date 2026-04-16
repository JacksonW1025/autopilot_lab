from __future__ import annotations

import math
import os
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from linearity_core.canonical import STATE_COLUMNS, STRICT_RAW_X_SCHEMAS
from linearity_core.io import read_yaml, write_json, write_rows_csv, write_yaml
from linearity_core.paths import STUDY_ARTIFACT_ROOT

from .matrix_gallery import MatrixData, load_matrix_csv

DEFAULT_TOP_K = 10
STUDY_NAME = "formal_v2_in_depth_analysis"
TARGETED_MODE_KEYS = ("stabilize", "guided_nogps")
X_SCHEMA_ORDER = {
    "commands_only": 0,
    "commands_plus_state": 1,
    "commands_plus_controller_params": 2,
    "commands_plus_state_history": 3,
    "commands_plus_state_plus_params": 4,
    "pooled_backend_mode_augmented": 5,
    "full_augmented": 6,
    "feature_mapped_linear": 7,
}
PRIMARY_DRIVER_PRIORITY = [
    "feature_collinearity",
    "mode_mixture",
    "throttle",
    "stratification",
]
TARGET_ALIGNMENT_KEYS = [
    ("future_state_horizon", "pooled", "ols_affine"),
    ("future_state_horizon", "pooled", "ridge_affine"),
    ("future_state_horizon", "pooled", "lasso_affine"),
    ("selected_state_subset", "pooled", "ols_affine"),
    ("selected_state_subset", "pooled", "ridge_affine"),
    ("selected_state_subset", "pooled", "lasso_affine"),
    ("window_summary_response", "pooled", "ols_affine"),
    ("window_summary_response", "pooled", "ridge_affine"),
    ("window_summary_response", "pooled", "lasso_affine"),
]
DEFAULT_CANONICAL_STUDIES = {
    "px4_baseline": STUDY_ARTIFACT_ROOT / "20260410_224818_px4_real_generalization_ablation",
    "px4_diagnostic": STUDY_ARTIFACT_ROOT / "20260411_021910_px4_generalization_diagnostic_matrix",
    "ardupilot_baseline": STUDY_ARTIFACT_ROOT / "20260413_070802_ardupilot_real_generalization_ablation",
    "ardupilot_diagnostic": STUDY_ARTIFACT_ROOT / "20260413_091420_ardupilot_generalization_diagnostic_matrix",
    "targeted_validation": STUDY_ARTIFACT_ROOT / "20260413_134505_ardupilot_state_evolution_validation",
}
FUTURE_LIKE_RESPONSE_FAMILIES = {"future_state", "delta_state", "future_state_horizon", "window_mean", "window_peak"}
BASELINE_DIAGNOSTIC_KEYS = {
    "px4": ("px4_baseline", "px4_diagnostic"),
    "ardupilot": ("ardupilot_baseline", "ardupilot_diagnostic"),
}


@dataclass(frozen=True)
class ComboRef:
    x_schema: str
    y_schema: str
    model_name: str
    pooling_mode: str

    def as_key(self) -> tuple[str, str, str, str]:
        return (self.x_schema, self.y_schema, self.model_name, self.pooling_mode)

    def as_display(self) -> str:
        return " | ".join(self.as_key())


def _combo_ref_from_entry(entry: dict[str, Any]) -> ComboRef:
    return ComboRef(
        x_schema=str(entry.get("x_schema", "")),
        y_schema=str(entry.get("y_schema", "")),
        model_name=str(entry.get("model_name", "")),
        pooling_mode=str(entry.get("pooling_mode", "")),
    )


def _combo_dict_from_ref(combo: ComboRef) -> dict[str, str]:
    return {
        "x_schema": combo.x_schema,
        "y_schema": combo.y_schema,
        "model_name": combo.model_name,
        "pooling_mode": combo.pooling_mode,
    }


def combo_ref_from_display(combo_text: str) -> ComboRef:
    x_schema, y_schema, model_name, pooling_mode = [part.strip() for part in str(combo_text).split(" | ", 3)]
    return ComboRef(
        x_schema=x_schema,
        y_schema=y_schema,
        model_name=model_name,
        pooling_mode=pooling_mode,
    )


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def _support_rank(support: str) -> int:
    return {
        "supported": 2,
        "partial": 1,
        "unsupported": 0,
        "skipped": -1,
        "missing": -2,
    }.get(str(support).strip().lower(), -2)


def _generalization_rank(status: str) -> int:
    return {
        "generalized_supported": 2,
        "supported_but_local": 1,
        "not_generalized": 0,
    }.get(str(status).strip().lower(), -1)


def _read_optional_yaml(path: Path) -> dict[str, Any]:
    return read_yaml(path) if path.exists() else {}


def _output_paths(output_dir: Path | None) -> dict[str, Path]:
    if output_dir is None:
        study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_{STUDY_NAME}"
        base_dir = STUDY_ARTIFACT_ROOT / study_id
    else:
        base_dir = output_dir.expanduser().resolve()
    prepared_dir = base_dir / "prepared"
    fits_dir = base_dir / "fits"
    reports_dir = base_dir / "reports"
    summary_dir = base_dir / "summary"
    tables_dir = base_dir / "tables"
    for path in (base_dir, prepared_dir, fits_dir, reports_dir, summary_dir, tables_dir):
        path.mkdir(parents=True, exist_ok=True)
    return {
        "base_dir": base_dir,
        "prepared_dir": prepared_dir,
        "fits_dir": fits_dir,
        "reports_dir": reports_dir,
        "summary_dir": summary_dir,
        "tables_dir": tables_dir,
        "manifest_path": base_dir / "manifest.yaml",
        "report_path": reports_dir / "in_depth_analysis.md",
        "summary_path": summary_dir / "in_depth_analysis.json",
        "stable_core_table_path": tables_dir / "stable_core_matrix_readout.csv",
        "px4_physical_table_path": tables_dir / "px4_physical_vs_state_continuation.csv",
        "backend_alignment_table_path": tables_dir / "backend_alignment.csv",
        "ardupilot_conditioning_table_path": tables_dir / "ardupilot_conditioning_failure.csv",
        "stability_boundary_table_path": tables_dir / "stability_boundary.csv",
    }


def _path_exists_str(path: Path) -> str:
    return str(path.resolve()) if path.exists() else ""


def _relative_path(target: Path | str, start: Path) -> str:
    return os.path.relpath(Path(target).resolve(), start=start.resolve())


def _fit_dir(study_dir: Path, combo: ComboRef) -> Path:
    return study_dir / "fits" / f"{combo.x_schema}__{combo.y_schema}__{combo.pooling_mode}" / combo.model_name


def _metrics_path(study_dir: Path, combo: ComboRef) -> Path:
    return _fit_dir(study_dir, combo) / "metrics.json"


def _matrix_path(study_dir: Path, combo: ComboRef) -> Path:
    return _fit_dir(study_dir, combo) / "matrix_f.csv"


def _heatmap_paths(study_dir: Path, combo: ComboRef) -> dict[str, str]:
    fit_dir = _fit_dir(study_dir, combo)
    abs_path = fit_dir / "matrix_heatmap_abs.png"
    signed_path = fit_dir / "matrix_heatmap_signed.png"
    return {
        "abs_heatmap_path": _path_exists_str(abs_path),
        "signed_heatmap_path": _path_exists_str(signed_path),
        "heatmap_status": "available" if abs_path.exists() and signed_path.exists() else "missing",
    }


def _strip_feature_prefixes(feature_name: str) -> str:
    name = str(feature_name)
    for prefix in ("sq__", "clip__"):
        if name.startswith(prefix):
            return _strip_feature_prefixes(name[len(prefix) :])
    return name


def _feature_lag(feature_name: str) -> int | None:
    name = _strip_feature_prefixes(feature_name)
    if "__lag_" not in name:
        return None
    _, lag_value = name.rsplit("__lag_", 1)
    try:
        return int(lag_value)
    except ValueError:
        return None


def feature_base_name(feature_name: str) -> str:
    name = _strip_feature_prefixes(feature_name)
    if "__lag_" in name:
        name = name.rsplit("__lag_", 1)[0]
    return name


def classify_feature_block(feature_name: str) -> str:
    lag = _feature_lag(feature_name)
    if lag is not None and 1 <= lag <= 3:
        return f"state_lag_{lag}"
    base_name = feature_base_name(feature_name)
    if base_name.startswith("command_"):
        return "command"
    if base_name in STATE_COLUMNS:
        return "state_current"
    return "other_augmented"


def classify_response_family(response_name: str) -> str:
    name = str(response_name)
    if name.startswith("future_state_"):
        return "future_state"
    if name.startswith("delta_state_"):
        return "delta_state"
    if "__h" in name:
        stem, _, horizon_value = name.rpartition("__h")
        if stem and horizon_value.isdigit():
            return "future_state_horizon"
    if name.startswith("window_mean_"):
        return "window_mean"
    if name.startswith("window_peak_"):
        return "window_peak"
    if name.startswith("actuator_"):
        return "actuator"
    return "other"


def response_base_name(response_name: str) -> str:
    name = str(response_name)
    if name.startswith("future_state_"):
        return name[len("future_state_") :]
    if name.startswith("delta_state_"):
        return name[len("delta_state_") :]
    if name.startswith("window_mean_"):
        return name[len("window_mean_") :]
    if name.startswith("window_peak_"):
        return name[len("window_peak_") :]
    if "__h" in name:
        stem, _, horizon_value = name.rpartition("__h")
        if stem and horizon_value.isdigit():
            return stem
    return name


def is_same_state_edge(feature_name: str, response_name: str) -> bool:
    return (
        classify_feature_block(feature_name) == "state_current"
        and classify_response_family(response_name) in FUTURE_LIKE_RESPONSE_FAMILIES
        and feature_base_name(feature_name) == response_base_name(response_name)
    )


def _is_future_like_response(response_name: str) -> bool:
    return classify_response_family(response_name) in FUTURE_LIKE_RESPONSE_FAMILIES


def extract_top_edges(matrix_data: MatrixData, top_k: int = DEFAULT_TOP_K) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for feature_index, feature_name in enumerate(matrix_data.feature_names):
        for response_index, response_name in enumerate(matrix_data.response_names):
            weight = _safe_float(matrix_data.values[feature_index, response_index])
            if not math.isfinite(weight):
                continue
            rows.append(
                {
                    "feature": feature_name,
                    "response": response_name,
                    "weight": weight,
                    "abs_weight": abs(weight),
                    "feature_block": classify_feature_block(feature_name),
                    "feature_base": feature_base_name(feature_name),
                    "response_family": classify_response_family(response_name),
                    "response_base": response_base_name(response_name),
                    "same_state": is_same_state_edge(feature_name, response_name),
                }
            )
    rows.sort(key=lambda item: (-item["abs_weight"], item["feature"], item["response"]))
    return rows[:top_k]


def compute_feature_block_shares(matrix_data: MatrixData) -> dict[str, float]:
    totals = {
        "command": 0.0,
        "state_current": 0.0,
        "state_lag_1": 0.0,
        "state_lag_2": 0.0,
        "state_lag_3": 0.0,
        "other_augmented": 0.0,
    }
    values = np.asarray(matrix_data.values, dtype=float)
    if values.size == 0:
        return totals
    total_mass = float(np.nansum(np.abs(values)))
    if not math.isfinite(total_mass) or total_mass <= 0.0:
        return totals
    for feature_index, feature_name in enumerate(matrix_data.feature_names):
        block = classify_feature_block(feature_name)
        block_mass = float(np.nansum(np.abs(values[feature_index, :])))
        if math.isfinite(block_mass):
            totals[block] = totals.get(block, 0.0) + block_mass
    return {key: value / total_mass for key, value in totals.items()}


def compute_px4_physical_category_shares(matrix_data: MatrixData) -> dict[str, float]:
    values = np.asarray(matrix_data.values, dtype=float)
    total_mass = float(np.nansum(np.abs(values)))
    categories = {
        "command_to_future": 0.0,
        "state_current_to_same_state": 0.0,
        "lag_to_future": 0.0,
    }
    if not math.isfinite(total_mass) or total_mass <= 0.0:
        return categories
    for feature_index, feature_name in enumerate(matrix_data.feature_names):
        feature_block = classify_feature_block(feature_name)
        for response_index, response_name in enumerate(matrix_data.response_names):
            weight = _safe_float(values[feature_index, response_index])
            if not math.isfinite(weight):
                continue
            mass = abs(weight)
            if feature_block == "command" and _is_future_like_response(response_name):
                categories["command_to_future"] += mass
            if is_same_state_edge(feature_name, response_name):
                categories["state_current_to_same_state"] += mass
            if feature_block.startswith("state_lag_") and _is_future_like_response(response_name):
                categories["lag_to_future"] += mass
    return {key: value / total_mass for key, value in categories.items()}


def compute_top_edge_overlap(
    current_edges: list[dict[str, Any]],
    comparison_edges: list[dict[str, Any]],
) -> dict[str, Any]:
    current = {(entry["feature"], entry["response"]) for entry in current_edges}
    comparison = {(entry["feature"], entry["response"]) for entry in comparison_edges}
    union = current | comparison
    intersection = current & comparison
    return {
        "current_nonzero_count": len(current),
        "comparison_nonzero_count": len(comparison),
        "intersection_count": len(intersection),
        "union_count": len(union),
        "jaccard_overlap": (len(intersection) / len(union)) if union else math.nan,
    }


def summarize_edges(edges: list[dict[str, Any]], *, limit: int = 5) -> str:
    entries: list[str] = []
    for edge in edges[:limit]:
        entries.append(f"{edge['feature']}->{edge['response']} ({edge['abs_weight']:.3g})")
    return "; ".join(entries)


def choose_minimal_stable_x(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    if not candidates:
        return {}
    return sorted(
        candidates,
        key=lambda item: (
            X_SCHEMA_ORDER.get(str(item.get("x_schema", "")), 999),
            str(item.get("x_schema", "")),
            -_support_rank(str(item.get("support", ""))),
            -_safe_float(item.get("median_test_r2")),
        ),
    )[0]


def choose_primary_driver(drivers: list[str]) -> str:
    unique = []
    for driver in drivers:
        if driver not in unique:
            unique.append(driver)
    for driver in PRIMARY_DRIVER_PRIORITY:
        if driver in unique:
            return driver
    return "other" if unique else "none"


def build_mode_mixture_context(
    current_support: str,
    targeted_supports: list[str],
) -> bool:
    return max((_support_rank(item) for item in targeted_supports), default=-2) > _support_rank(current_support)


def build_throttle_driver_context(
    *,
    scenario_entry: dict[str, Any] | None = None,
    diagnostic_throttle_evidence: bool = False,
) -> bool:
    if scenario_entry:
        subgroup_r2 = dict(scenario_entry.get("scenario_subgroup_r2", {}) or {})
        throttle_r2 = _safe_float(subgroup_r2.get("throttle_biased"))
        other_r2 = [_safe_float(subgroup_r2.get(name)) for name in subgroup_r2 if name != "throttle_biased"]
        finite_other = [value for value in other_r2 if math.isfinite(value)]
        if finite_other and math.isfinite(throttle_r2) and (max(finite_other) - throttle_r2) >= 0.05 and diagnostic_throttle_evidence:
            return True
    return False


def build_stratification_context(
    current_entry: dict[str, Any],
    counterpart_entry: dict[str, Any] | None,
) -> bool:
    if counterpart_entry is None:
        return False
    return _generalization_rank(str(current_entry.get("generalization_status", ""))) != _generalization_rank(
        str(counterpart_entry.get("generalization_status", ""))
    )


class FormalV2InDepthAnalyzer:
    def __init__(
        self,
        *,
        px4_baseline_dir: Path,
        px4_diagnostic_dir: Path,
        ardupilot_baseline_dir: Path,
        ardupilot_diagnostic_dir: Path,
        targeted_validation_dir: Path,
        top_k: int = DEFAULT_TOP_K,
    ) -> None:
        self.study_dirs = {
            "px4_baseline": px4_baseline_dir.expanduser().resolve(),
            "px4_diagnostic": px4_diagnostic_dir.expanduser().resolve(),
            "ardupilot_baseline": ardupilot_baseline_dir.expanduser().resolve(),
            "ardupilot_diagnostic": ardupilot_diagnostic_dir.expanduser().resolve(),
            "targeted_validation": targeted_validation_dir.expanduser().resolve(),
        }
        self.top_k = int(top_k)
        self._matrix_cache: dict[Path, MatrixData] = {}
        self._scenario_cache: dict[Path, dict[str, Any]] = {}
        self._scenario_map_cache: dict[Path, dict[tuple[str, str, str, str], dict[str, Any]]] = {}
        self._summary_cache: dict[Path, dict[str, Any]] = {}
        self._audit_cache: dict[Path, dict[str, Any]] = {}
        self._audit_map_cache: dict[Path, dict[tuple[str, str, str, str], dict[str, Any]]] = {}
        self._targeted_validation_cache: dict[str, Any] | None = None

    def load_matrix(self, matrix_path: Path) -> MatrixData:
        resolved = matrix_path.expanduser().resolve()
        if resolved not in self._matrix_cache:
            self._matrix_cache[resolved] = load_matrix_csv(resolved)
        return self._matrix_cache[resolved]

    def scenario_payload(self, study_dir: Path) -> dict[str, Any]:
        resolved = study_dir.resolve()
        if resolved not in self._scenario_cache:
            self._scenario_cache[resolved] = _read_optional_yaml(resolved / "summary" / "scenario_generalization.json")
        return self._scenario_cache[resolved]

    def scenario_map(self, study_dir: Path) -> dict[tuple[str, str, str, str], dict[str, Any]]:
        resolved = study_dir.resolve()
        if resolved not in self._scenario_map_cache:
            entries = {}
            for entry in list(self.scenario_payload(resolved).get("entries", []) or []):
                combo = _combo_ref_from_entry(entry)
                entries[combo.as_key()] = dict(entry)
            self._scenario_map_cache[resolved] = entries
        return self._scenario_map_cache[resolved]

    def study_summary(self, study_dir: Path) -> dict[str, Any]:
        resolved = study_dir.resolve()
        if resolved not in self._summary_cache:
            self._summary_cache[resolved] = _read_optional_yaml(resolved / "summary" / "study_summary.json")
        return self._summary_cache[resolved]

    def audit_payload(self, study_dir: Path) -> dict[str, Any]:
        resolved = study_dir.resolve()
        if resolved not in self._audit_cache:
            self._audit_cache[resolved] = _read_optional_yaml(resolved / "summary" / "state_evolution_audit.json")
        return self._audit_cache[resolved]

    def audit_map(self, study_dir: Path) -> dict[tuple[str, str, str, str], dict[str, Any]]:
        resolved = study_dir.resolve()
        if resolved not in self._audit_map_cache:
            entries = {}
            for entry in list(self.audit_payload(resolved).get("entries", []) or []):
                combo = _combo_ref_from_entry(entry)
                entries[combo.as_key()] = dict(entry)
            self._audit_map_cache[resolved] = entries
        return self._audit_map_cache[resolved]

    def targeted_validation_payload(self) -> dict[str, Any]:
        if self._targeted_validation_cache is None:
            self._targeted_validation_cache = _read_optional_yaml(
                self.study_dirs["targeted_validation"] / "summary" / "state_evolution_validation.json"
            )
        return self._targeted_validation_cache

    def targeted_mode_dir(self, mode_key: str, phase: str) -> Path:
        payload = self.targeted_validation_payload()
        section = dict(payload.get("modes", {}).get(mode_key, {}) or {})
        field = f"{phase}_dir"
        value = str(section.get(field, "") or "").strip()
        if not value:
            raise FileNotFoundError(f"targeted validation missing {mode_key}.{field}")
        return Path(value).expanduser().resolve()

    def entry_matrix(self, study_dir: Path, entry: dict[str, Any]) -> MatrixData:
        combo = _combo_ref_from_entry(entry)
        return self.load_matrix(_matrix_path(study_dir, combo))

    def top_edges(self, study_dir: Path, entry: dict[str, Any]) -> list[dict[str, Any]]:
        return extract_top_edges(self.entry_matrix(study_dir, entry), top_k=self.top_k)

    def block_shares(self, study_dir: Path, entry: dict[str, Any]) -> dict[str, float]:
        return compute_feature_block_shares(self.entry_matrix(study_dir, entry))

    def stable_core_entries(self, backend: str) -> list[dict[str, Any]]:
        baseline_key, diagnostic_key = BASELINE_DIAGNOSTIC_KEYS[backend]
        baseline_dir = self.study_dirs[baseline_key]
        diagnostic_dir = self.study_dirs[diagnostic_key]
        baseline_entries = {
            key: value
            for key, value in self.scenario_map(baseline_dir).items()
            if str(value.get("generalization_status", "")) == "generalized_supported"
        }
        diagnostic_entries = {
            key: value
            for key, value in self.scenario_map(diagnostic_dir).items()
            if str(value.get("generalization_status", "")) == "generalized_supported"
        }
        rows: list[dict[str, Any]] = []
        for key in sorted(baseline_entries.keys() & diagnostic_entries.keys()):
            baseline_entry = dict(baseline_entries[key])
            diagnostic_entry = dict(diagnostic_entries[key])
            combo = _combo_ref_from_entry(baseline_entry)
            baseline_matrix = self.entry_matrix(baseline_dir, baseline_entry)
            diagnostic_matrix = self.entry_matrix(diagnostic_dir, diagnostic_entry)
            baseline_top_edges = extract_top_edges(baseline_matrix, top_k=self.top_k)
            diagnostic_top_edges = extract_top_edges(diagnostic_matrix, top_k=self.top_k)
            row = {
                "backend": backend,
                "combo": combo.as_display(),
                "x_schema": combo.x_schema,
                "y_schema": combo.y_schema,
                "model_name": combo.model_name,
                "pooling_mode": combo.pooling_mode,
                "baseline_support": str(baseline_entry.get("support", "")),
                "diagnostic_support": str(diagnostic_entry.get("support", "")),
                "baseline_median_test_r2": _safe_float(baseline_entry.get("median_test_r2")),
                "diagnostic_median_test_r2": _safe_float(diagnostic_entry.get("median_test_r2")),
                "baseline_effective_condition_number": _safe_float(baseline_entry.get("effective_condition_number")),
                "diagnostic_effective_condition_number": _safe_float(diagnostic_entry.get("effective_condition_number")),
                "baseline_scenario_consistency": _safe_float(baseline_entry.get("scenario_consistency")),
                "diagnostic_scenario_consistency": _safe_float(diagnostic_entry.get("scenario_consistency")),
                "baseline_top_edge_overlap_jaccard": compute_top_edge_overlap(baseline_top_edges, diagnostic_top_edges)["jaccard_overlap"],
                "dominant_edges": baseline_top_edges,
                "block_shares": compute_feature_block_shares(baseline_matrix),
                "baseline_metrics_path": str(_metrics_path(baseline_dir, combo)),
                "diagnostic_metrics_path": str(_metrics_path(diagnostic_dir, combo)),
                "baseline_matrix_path": str(_matrix_path(baseline_dir, combo)),
                "diagnostic_matrix_path": str(_matrix_path(diagnostic_dir, combo)),
                "baseline_heatmaps": _heatmap_paths(baseline_dir, combo),
                "diagnostic_heatmaps": _heatmap_paths(diagnostic_dir, combo),
            }
            rows.append(row)
        return rows

    def build_stable_core_section(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        for backend in ("px4", "ardupilot"):
            baseline_key, diagnostic_key = BASELINE_DIAGNOSTIC_KEYS[backend]
            baseline_dir = self.study_dirs[baseline_key]
            diagnostic_dir = self.study_dirs[diagnostic_key]
            stable_entries = self.stable_core_entries(backend)
            baseline_generalized = {
                key
                for key, value in self.scenario_map(baseline_dir).items()
                if str(value.get("generalization_status", "")) == "generalized_supported"
            }
            diagnostic_generalized = {
                key
                for key, value in self.scenario_map(diagnostic_dir).items()
                if str(value.get("generalization_status", "")) == "generalized_supported"
            }
            payload[backend] = {
                "baseline_dir": str(baseline_dir),
                "diagnostic_dir": str(diagnostic_dir),
                "stable_core_count": len(stable_entries),
                "baseline_generalized_supported_count": len(baseline_generalized),
                "diagnostic_generalized_supported_count": len(diagnostic_generalized),
                "baseline_is_subset_of_diagnostic": baseline_generalized <= diagnostic_generalized,
                "diagnostic_only_generalized_supported_count": len(diagnostic_generalized - baseline_generalized),
                "entries": stable_entries,
            }
        return payload

    def build_px4_physical_vs_continuation_section(self, stable_core: dict[str, Any]) -> dict[str, Any]:
        px4_entries = list(stable_core["px4"]["entries"])
        main_rows: list[dict[str, Any]] = []
        appendix_rows: list[dict[str, Any]] = []
        pattern_counts: Counter[str] = Counter()
        baseline_dir = self.study_dirs["px4_baseline"]
        for entry in px4_entries:
            x_schema = str(entry.get("x_schema", ""))
            combo = ComboRef(
                x_schema=x_schema,
                y_schema=str(entry.get("y_schema", "")),
                model_name=str(entry.get("model_name", "")),
                pooling_mode=str(entry.get("pooling_mode", "")),
            )
            baseline_entry = _combo_dict_from_ref(combo)
            matrix = self.entry_matrix(baseline_dir, baseline_entry)
            category_shares = compute_px4_physical_category_shares(matrix)
            top_edges = extract_top_edges(matrix, top_k=self.top_k)
            for edge in top_edges:
                if edge["feature_block"] == "command" and _is_future_like_response(edge["response"]):
                    pattern_counts[f"command:{edge['feature_base']}->{edge['response_base']}"] += 1
                if edge["same_state"]:
                    pattern_counts[f"same_state:{edge['feature_base']}->{edge['response_base']}"] += 1
                if edge["feature_block"].startswith("state_lag_") and _is_future_like_response(edge["response"]):
                    pattern_counts[f"lag:{edge['feature_base']}->{edge['response_base']}"] += 1
            row = {
                "combo": combo.as_display(),
                "x_schema": combo.x_schema,
                "y_schema": combo.y_schema,
                "model_name": combo.model_name,
                "pooling_mode": combo.pooling_mode,
                "scope": "appendix" if x_schema in {"feature_mapped_linear", "pooled_backend_mode_augmented"} else "main",
                "command_to_future_share": category_shares["command_to_future"],
                "state_current_to_same_state_share": category_shares["state_current_to_same_state"],
                "lag_to_future_share": category_shares["lag_to_future"],
                "dominant_edges": top_edges,
                "baseline_matrix_path": str(_matrix_path(baseline_dir, combo)),
                "baseline_metrics_path": str(_metrics_path(baseline_dir, combo)),
                **_heatmap_paths(baseline_dir, combo),
            }
            if row["scope"] == "main" and x_schema in STRICT_RAW_X_SCHEMAS:
                main_rows.append(row)
            else:
                appendix_rows.append(row)
        return {
            "main_count": len(main_rows),
            "appendix_count": len(appendix_rows),
            "main_entries": main_rows,
            "appendix_entries": appendix_rows,
            "repeated_patterns": [
                {"pattern": pattern, "count": count}
                for pattern, count in pattern_counts.most_common(12)
            ],
        }

    def build_backend_alignment_section(self, stable_core: dict[str, Any]) -> dict[str, Any]:
        per_backend_entries = {
            "px4": list(stable_core["px4"]["entries"]),
            "ardupilot": list(stable_core["ardupilot"]["entries"]),
        }
        strict_schema_overlap = {
            (entry["x_schema"], entry["y_schema"], entry["model_name"], entry["pooling_mode"])
            for entry in per_backend_entries["px4"]
        } & {
            (entry["x_schema"], entry["y_schema"], entry["model_name"], entry["pooling_mode"])
            for entry in per_backend_entries["ardupilot"]
        }
        shared_rows: list[dict[str, Any]] = []
        for y_schema, pooling_mode, model_name in TARGET_ALIGNMENT_KEYS:
            px4_candidates = [
                entry
                for entry in per_backend_entries["px4"]
                if (entry["y_schema"], entry["pooling_mode"], entry["model_name"]) == (y_schema, pooling_mode, model_name)
            ]
            ap_candidates = [
                entry
                for entry in per_backend_entries["ardupilot"]
                if (entry["y_schema"], entry["pooling_mode"], entry["model_name"]) == (y_schema, pooling_mode, model_name)
            ]
            px4_entry = choose_minimal_stable_x(px4_candidates)
            ap_entry = choose_minimal_stable_x(ap_candidates)
            if not px4_entry or not ap_entry:
                continue
            px4_combo = _combo_ref_from_entry(px4_entry)
            ap_combo = _combo_ref_from_entry(ap_entry)
            px4_top_edges = self.top_edges(self.study_dirs["px4_baseline"], _combo_dict_from_ref(px4_combo))
            ap_top_edges = self.top_edges(self.study_dirs["ardupilot_baseline"], _combo_dict_from_ref(ap_combo))
            shared_rows.append(
                {
                    "alignment_type": "shared",
                    "alignment_key": f"{y_schema} | {pooling_mode} | {model_name}",
                    "px4_combo": px4_combo.as_display(),
                    "ardupilot_combo": ap_combo.as_display(),
                    "px4_minimal_x": px4_combo.x_schema,
                    "ardupilot_minimal_x": ap_combo.x_schema,
                    "top_edge_overlap_jaccard": compute_top_edge_overlap(px4_top_edges, ap_top_edges)["jaccard_overlap"],
                    "px4_dominant_edges": px4_top_edges,
                    "ardupilot_dominant_edges": ap_top_edges,
                    "px4_block_shares": self.block_shares(self.study_dirs["px4_baseline"], _combo_dict_from_ref(px4_combo)),
                    "ardupilot_block_shares": self.block_shares(self.study_dirs["ardupilot_baseline"], _combo_dict_from_ref(ap_combo)),
                    "px4_matrix_path": str(_matrix_path(self.study_dirs["px4_baseline"], px4_combo)),
                    "ardupilot_matrix_path": str(_matrix_path(self.study_dirs["ardupilot_baseline"], ap_combo)),
                }
            )
        px4_only_rows: list[dict[str, Any]] = []
        ap_only_rows: list[dict[str, Any]] = []
        for model_name in ("ols_affine", "ridge_affine", "lasso_affine"):
            for pooling_mode in ("pooled", "stratified"):
                candidates = [
                    entry
                    for entry in per_backend_entries["px4"]
                    if (entry["y_schema"], entry["pooling_mode"], entry["model_name"]) == ("next_raw_state", pooling_mode, model_name)
                ]
                selected = choose_minimal_stable_x(candidates)
                if not selected:
                    continue
                combo = _combo_ref_from_entry(selected)
                px4_only_rows.append(
                    {
                        "alignment_type": "px4_only",
                        "alignment_key": f"next_raw_state | {pooling_mode} | {model_name}",
                        "px4_combo": combo.as_display(),
                        "px4_minimal_x": combo.x_schema,
                        "px4_dominant_edges": self.top_edges(self.study_dirs["px4_baseline"], _combo_dict_from_ref(combo)),
                        "px4_matrix_path": str(_matrix_path(self.study_dirs["px4_baseline"], combo)),
                    }
                )
        for model_name in ("ols_affine", "ridge_affine", "lasso_affine"):
            candidates = [
                entry
                for entry in per_backend_entries["ardupilot"]
                if (entry["y_schema"], entry["pooling_mode"], entry["model_name"]) == ("actuator_response", "pooled", model_name)
            ]
            selected = choose_minimal_stable_x(candidates)
            if not selected:
                continue
            combo = _combo_ref_from_entry(selected)
            ap_only_rows.append(
                {
                    "alignment_type": "ardupilot_only",
                    "alignment_key": f"actuator_response | pooled | {model_name}",
                    "ardupilot_combo": combo.as_display(),
                    "ardupilot_minimal_x": combo.x_schema,
                    "ardupilot_dominant_edges": self.top_edges(self.study_dirs["ardupilot_baseline"], _combo_dict_from_ref(combo)),
                    "ardupilot_matrix_path": str(_matrix_path(self.study_dirs["ardupilot_baseline"], combo)),
                }
            )
        return {
            "strict_schema_overlap_count": len(strict_schema_overlap),
            "shared_alignment_key_count": len(shared_rows),
            "shared_rows": shared_rows,
            "backend_specific": {
                "px4_only_next_raw_state": px4_only_rows,
                "ardupilot_only_actuator_response": ap_only_rows,
            },
        }

    def _scenario_for_combo(self, study_dir: Path, combo: ComboRef) -> dict[str, Any]:
        return dict(self.scenario_map(study_dir).get(combo.as_key(), {}) or {})

    def _audit_for_combo(self, study_dir: Path, combo: ComboRef) -> dict[str, Any]:
        return dict(self.audit_map(study_dir).get(combo.as_key(), {}) or {})

    def _select_mixed_mode_representative(self) -> ComboRef:
        baseline_summary = self.study_summary(self.study_dirs["ardupilot_baseline"])
        candidate = dict(baseline_summary.get("best_result", {}) or {})
        combo = _combo_ref_from_entry(candidate)
        if combo.as_key() in self.scenario_map(self.study_dirs["ardupilot_diagnostic"]):
            return combo
        intersection = set(self.audit_map(self.study_dirs["ardupilot_baseline"])) & set(self.audit_map(self.study_dirs["ardupilot_diagnostic"]))
        if not intersection:
            raise ValueError("no mixed-mode ArduPilot state-evolution overlap found")
        best_key = sorted(
            intersection,
            key=lambda key: (
                -_support_rank(str(self.audit_map(self.study_dirs["ardupilot_baseline"])[key].get("support", "")))
                - _support_rank(str(self.audit_map(self.study_dirs["ardupilot_diagnostic"])[key].get("support", ""))),
                -_safe_float(self.audit_map(self.study_dirs["ardupilot_baseline"])[key].get("median_test_r2")),
                str(key),
            ),
        )[0]
        return ComboRef(*best_key)

    def _conditioning_failure_row(
        self,
        *,
        failure_path: str,
        baseline_dir: Path,
        diagnostic_dir: Path,
        combo: ComboRef,
    ) -> dict[str, Any]:
        baseline_scenario = self._scenario_for_combo(baseline_dir, combo)
        diagnostic_scenario = self._scenario_for_combo(diagnostic_dir, combo)
        baseline_audit = self._audit_for_combo(baseline_dir, combo)
        diagnostic_audit = self._audit_for_combo(diagnostic_dir, combo)
        baseline_top_edges = self.top_edges(baseline_dir, _combo_dict_from_ref(combo))
        diagnostic_top_edges = self.top_edges(diagnostic_dir, _combo_dict_from_ref(combo))
        return {
            "failure_path": failure_path,
            "combo": combo.as_display(),
            "baseline_dir": str(baseline_dir),
            "diagnostic_dir": str(diagnostic_dir),
            "baseline_support": str((baseline_audit or baseline_scenario).get("support", "")),
            "diagnostic_support": str((diagnostic_audit or diagnostic_scenario).get("support", "")),
            "baseline_effective_condition_number": _safe_float((baseline_audit or baseline_scenario).get("effective_condition_number")),
            "diagnostic_effective_condition_number": _safe_float((diagnostic_audit or diagnostic_scenario).get("effective_condition_number")),
            "baseline_median_test_r2": _safe_float((baseline_audit or baseline_scenario).get("median_test_r2")),
            "diagnostic_median_test_r2": _safe_float((diagnostic_audit or diagnostic_scenario).get("median_test_r2")),
            "baseline_conditioning_pruned_features": list((baseline_audit or {}).get("conditioning_pruned_features", []) or []),
            "diagnostic_conditioning_pruned_features": list((diagnostic_audit or {}).get("conditioning_pruned_features", []) or []),
            "top_edge_overlap_jaccard": compute_top_edge_overlap(baseline_top_edges, diagnostic_top_edges)["jaccard_overlap"],
            "baseline_dominant_edges": baseline_top_edges,
            "diagnostic_dominant_edges": diagnostic_top_edges,
            "baseline_matrix_path": str(_matrix_path(baseline_dir, combo)),
            "diagnostic_matrix_path": str(_matrix_path(diagnostic_dir, combo)),
            "baseline_metrics_path": str(_metrics_path(baseline_dir, combo)),
            "diagnostic_metrics_path": str(_metrics_path(diagnostic_dir, combo)),
            "baseline_heatmaps": _heatmap_paths(baseline_dir, combo),
            "diagnostic_heatmaps": _heatmap_paths(diagnostic_dir, combo),
        }

    def build_ardupilot_conditioning_failure_section(self) -> dict[str, Any]:
        validation_payload = self.targeted_validation_payload()
        mixed_mode_combo = self._select_mixed_mode_representative()
        stabilize_combo = combo_ref_from_display(validation_payload["modes"]["stabilize"]["representative_combo"])
        guided_combo = combo_ref_from_display(validation_payload["modes"]["guided_nogps"]["representative_combo"])
        rows = [
            self._conditioning_failure_row(
                failure_path="mixed_mode_full",
                baseline_dir=self.study_dirs["ardupilot_baseline"],
                diagnostic_dir=self.study_dirs["ardupilot_diagnostic"],
                combo=mixed_mode_combo,
            ),
            self._conditioning_failure_row(
                failure_path="stabilize_baseline_to_diagnostic_collapse",
                baseline_dir=self.targeted_mode_dir("stabilize", "baseline"),
                diagnostic_dir=self.targeted_mode_dir("stabilize", "diagnostic"),
                combo=stabilize_combo,
            ),
            self._conditioning_failure_row(
                failure_path="guided_nogps_persistent_high_r2_high_cond",
                baseline_dir=self.targeted_mode_dir("guided_nogps", "baseline"),
                diagnostic_dir=self.targeted_mode_dir("guided_nogps", "diagnostic"),
                combo=guided_combo,
            ),
        ]
        return {"paths": rows}

    def _targeted_family_supports(self) -> dict[tuple[str, str, str], list[str]]:
        supports: dict[tuple[str, str, str], list[str]] = {}
        for mode_key in TARGETED_MODE_KEYS:
            for phase in ("baseline", "diagnostic"):
                study_dir = self.targeted_mode_dir(mode_key, phase)
                for entry in list(self.scenario_payload(study_dir).get("entries", []) or []):
                    key = (str(entry.get("y_schema", "")), str(entry.get("model_name", "")), str(entry.get("pooling_mode", "")))
                    supports.setdefault(key, []).append(str(entry.get("support", "")))
        return supports

    def _diagnostic_throttle_evidence(self) -> dict[str, bool]:
        evidence: dict[str, bool] = {}
        for study_key in ("px4_diagnostic", "ardupilot_diagnostic"):
            payload = _read_optional_yaml(self.study_dirs[study_key] / "summary" / "diagnostic_gate.json")
            evidence[study_key] = str(payload.get("throttle_boundary", "")) not in {"", "none"}
        for mode_key in TARGETED_MODE_KEYS:
            study_dir = self.targeted_mode_dir(mode_key, "diagnostic")
            payload = _read_optional_yaml(study_dir / "summary" / "diagnostic_gate.json")
            evidence[str(study_dir)] = str(payload.get("throttle_boundary", "")) not in {"", "none"}
        return evidence

    def build_stability_boundary_section(self) -> dict[str, Any]:
        rows: list[dict[str, Any]] = []
        targeted_supports = self._targeted_family_supports()
        throttle_evidence = self._diagnostic_throttle_evidence()
        px4_baseline_map = self.scenario_map(self.study_dirs["px4_baseline"])
        px4_diag_map = self.scenario_map(self.study_dirs["px4_diagnostic"])
        for key, diag_entry in sorted(px4_diag_map.items()):
            if str(diag_entry.get("generalization_status", "")) != "generalized_supported":
                continue
            if str(px4_baseline_map.get(key, {}).get("generalization_status", "")) == "generalized_supported":
                continue
            combo = _combo_ref_from_entry(diag_entry)
            baseline_entry = dict(px4_baseline_map.get(key, {}) or {})
            counterpart_key = (combo.x_schema, combo.y_schema, combo.model_name, "pooled" if combo.pooling_mode == "stratified" else "stratified")
            other_pooling = px4_diag_map.get(counterpart_key)
            drivers: list[str] = []
            if build_throttle_driver_context(
                scenario_entry=diag_entry,
                diagnostic_throttle_evidence=throttle_evidence["px4_diagnostic"],
            ):
                drivers.append("throttle")
            if build_stratification_context(diag_entry, other_pooling):
                drivers.append("stratification")
            row = {
                "source_category": "px4_diagnostic_only_generalized_supported",
                "backend": "px4",
                "study_dir": str(self.study_dirs["px4_diagnostic"]),
                "combo": combo.as_display(),
                "support": str(diag_entry.get("support", "")),
                "generalization_status": str(diag_entry.get("generalization_status", "")),
                "comparison_generalization_status": str(baseline_entry.get("generalization_status", "")),
                "effective_condition_number": _safe_float(diag_entry.get("effective_condition_number")),
                "drivers": drivers,
                "primary_driver": choose_primary_driver(drivers),
                "matrix_path": str(_matrix_path(self.study_dirs["px4_diagnostic"], combo)),
                "metrics_path": str(_metrics_path(self.study_dirs["px4_diagnostic"], combo)),
                **_heatmap_paths(self.study_dirs["px4_diagnostic"], combo),
            }
            rows.append(row)
        for study_key in ("px4_baseline", "px4_diagnostic"):
            study_dir = self.study_dirs[study_key]
            scenario_map = self.scenario_map(study_dir)
            for key, entry in sorted(scenario_map.items()):
                if str(entry.get("generalization_status", "")) != "supported_but_local":
                    continue
                combo = _combo_ref_from_entry(entry)
                counterpart_key = (combo.x_schema, combo.y_schema, combo.model_name, "pooled" if combo.pooling_mode == "stratified" else "stratified")
                other_pooling = scenario_map.get(counterpart_key)
                drivers: list[str] = []
                if build_throttle_driver_context(
                    scenario_entry=entry,
                    diagnostic_throttle_evidence=throttle_evidence.get("px4_diagnostic", False),
                ):
                    drivers.append("throttle")
                if build_stratification_context(entry, other_pooling):
                    drivers.append("stratification")
                rows.append(
                    {
                        "source_category": "supported_but_local",
                        "backend": "px4" if study_key.startswith("px4") else "ardupilot",
                        "study_dir": str(study_dir),
                        "combo": combo.as_display(),
                        "support": str(entry.get("support", "")),
                        "generalization_status": str(entry.get("generalization_status", "")),
                        "comparison_generalization_status": str((other_pooling or {}).get("generalization_status", "")),
                        "effective_condition_number": _safe_float(entry.get("effective_condition_number")),
                        "drivers": drivers,
                        "primary_driver": choose_primary_driver(drivers),
                        "matrix_path": str(_matrix_path(study_dir, combo)),
                        "metrics_path": str(_metrics_path(study_dir, combo)),
                        **_heatmap_paths(study_dir, combo),
                    }
                )
        for study_key in ("ardupilot_baseline", "ardupilot_diagnostic"):
            study_dir = self.study_dirs[study_key]
            scenario_map = self.scenario_map(study_dir)
            for key, entry in sorted(scenario_map.items()):
                combo = _combo_ref_from_entry(entry)
                if combo.x_schema not in {"commands_plus_state", "commands_plus_state_history", "full_augmented"}:
                    continue
                if combo.y_schema not in {"next_raw_state", "selected_state_subset", "future_state_horizon", "delta_state", "window_summary_response"}:
                    continue
                if str(entry.get("generalization_status", "")) != "not_generalized" and str(entry.get("support", "")) != "partial":
                    continue
                drivers: list[str] = []
                if _safe_float(entry.get("effective_condition_number")) >= 1e6:
                    drivers.append("feature_collinearity")
                family_key = (combo.y_schema, combo.model_name, combo.pooling_mode)
                if build_mode_mixture_context(str(entry.get("support", "")), targeted_supports.get(family_key, [])):
                    drivers.append("mode_mixture")
                if build_throttle_driver_context(
                    scenario_entry=entry,
                    diagnostic_throttle_evidence=throttle_evidence.get(study_key, False),
                ):
                    drivers.append("throttle")
                counterpart_key = (combo.x_schema, combo.y_schema, combo.model_name, "pooled" if combo.pooling_mode == "stratified" else "stratified")
                other_pooling = scenario_map.get(counterpart_key)
                if build_stratification_context(entry, other_pooling):
                    drivers.append("stratification")
                rows.append(
                    {
                        "source_category": "ardupilot_partial_not_generalized_state_evolution",
                        "backend": "ardupilot",
                        "study_dir": str(study_dir),
                        "combo": combo.as_display(),
                        "support": str(entry.get("support", "")),
                        "generalization_status": str(entry.get("generalization_status", "")),
                        "comparison_generalization_status": str((other_pooling or {}).get("generalization_status", "")),
                        "effective_condition_number": _safe_float(entry.get("effective_condition_number")),
                        "drivers": drivers,
                        "primary_driver": choose_primary_driver(drivers),
                        "matrix_path": str(_matrix_path(study_dir, combo)),
                        "metrics_path": str(_metrics_path(study_dir, combo)),
                        **_heatmap_paths(study_dir, combo),
                    }
                )
        validation_payload = self.targeted_validation_payload()
        for mode_key in TARGETED_MODE_KEYS:
            representative_combo = str(validation_payload.get("modes", {}).get(mode_key, {}).get("representative_combo", "") or "")
            if not representative_combo:
                continue
            combo = combo_ref_from_display(representative_combo)
            for phase in ("baseline", "diagnostic"):
                study_dir = self.targeted_mode_dir(mode_key, phase)
                scenario_entry = dict(self.scenario_map(study_dir).get(combo.as_key(), {}) or {})
                audit_entry = dict(self.audit_map(study_dir).get(combo.as_key(), {}) or {})
                drivers: list[str] = []
                if str(audit_entry.get("primary_blocker", "")) == "condition_number" or _safe_float(audit_entry.get("effective_condition_number")) >= 1e6:
                    drivers.append("feature_collinearity")
                if build_throttle_driver_context(
                    scenario_entry=scenario_entry,
                    diagnostic_throttle_evidence=throttle_evidence.get(str(self.targeted_mode_dir(mode_key, "diagnostic")), False),
                ):
                    drivers.append("throttle")
                rows.append(
                    {
                        "source_category": "targeted_inconclusive_family",
                        "backend": "ardupilot",
                        "study_dir": str(study_dir),
                        "combo": combo.as_display(),
                        "support": str((audit_entry or scenario_entry).get("support", "")),
                        "generalization_status": str((scenario_entry or {}).get("generalization_status", "")),
                        "comparison_generalization_status": mode_key,
                        "effective_condition_number": _safe_float((audit_entry or scenario_entry).get("effective_condition_number")),
                        "drivers": drivers,
                        "primary_driver": choose_primary_driver(drivers),
                        "matrix_path": str(_matrix_path(study_dir, combo)),
                        "metrics_path": str(_metrics_path(study_dir, combo)),
                        **_heatmap_paths(study_dir, combo),
                    }
                )
        driver_counts = Counter(row["primary_driver"] for row in rows)
        return {
            "row_count": len(rows),
            "primary_driver_counts": dict(driver_counts),
            "rows": rows,
        }

    def build_source_studies_section(self) -> dict[str, Any]:
        validation_payload = self.targeted_validation_payload()
        targeted_modes: dict[str, dict[str, str]] = {}
        for mode_key in TARGETED_MODE_KEYS:
            targeted_modes[mode_key] = {
                "baseline_dir": str(self.targeted_mode_dir(mode_key, "baseline")),
                "diagnostic_dir": str(self.targeted_mode_dir(mode_key, "diagnostic")),
                "representative_combo": str(validation_payload.get("modes", {}).get(mode_key, {}).get("representative_combo", "")),
            }
        return {
            "px4_baseline": str(self.study_dirs["px4_baseline"]),
            "px4_diagnostic": str(self.study_dirs["px4_diagnostic"]),
            "ardupilot_baseline": str(self.study_dirs["ardupilot_baseline"]),
            "ardupilot_diagnostic": str(self.study_dirs["ardupilot_diagnostic"]),
            "targeted_validation": str(self.study_dirs["targeted_validation"]),
            "targeted_modes": targeted_modes,
            "top_k": self.top_k,
        }

    def build_payload(self) -> dict[str, Any]:
        stable_core = self.build_stable_core_section()
        return {
            "source_studies": self.build_source_studies_section(),
            "stable_core": stable_core,
            "px4_physical_vs_continuation": self.build_px4_physical_vs_continuation_section(stable_core),
            "backend_alignment": self.build_backend_alignment_section(stable_core),
            "ardupilot_conditioning_failure": self.build_ardupilot_conditioning_failure_section(),
            "stability_boundary": self.build_stability_boundary_section(),
        }


def _stable_core_csv_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for backend in ("px4", "ardupilot"):
        for entry in payload["stable_core"][backend]["entries"]:
            block_shares = dict(entry.get("block_shares", {}) or {})
            heatmaps = dict(entry.get("baseline_heatmaps", {}) or {})
            rows.append(
                {
                    "backend": backend,
                    "combo": entry["combo"],
                    "x_schema": entry["x_schema"],
                    "y_schema": entry["y_schema"],
                    "model_name": entry["model_name"],
                    "pooling_mode": entry["pooling_mode"],
                    "baseline_median_test_r2": entry["baseline_median_test_r2"],
                    "diagnostic_median_test_r2": entry["diagnostic_median_test_r2"],
                    "baseline_effective_condition_number": entry["baseline_effective_condition_number"],
                    "diagnostic_effective_condition_number": entry["diagnostic_effective_condition_number"],
                    "baseline_top_edge_overlap_jaccard": entry["baseline_top_edge_overlap_jaccard"],
                    "command_share": block_shares.get("command", 0.0),
                    "state_current_share": block_shares.get("state_current", 0.0),
                    "state_lag_1_share": block_shares.get("state_lag_1", 0.0),
                    "state_lag_2_share": block_shares.get("state_lag_2", 0.0),
                    "state_lag_3_share": block_shares.get("state_lag_3", 0.0),
                    "other_augmented_share": block_shares.get("other_augmented", 0.0),
                    "dominant_edges": summarize_edges(list(entry.get("dominant_edges", []) or []), limit=5),
                    "baseline_matrix_path": entry["baseline_matrix_path"],
                    "diagnostic_matrix_path": entry["diagnostic_matrix_path"],
                    "baseline_metrics_path": entry["baseline_metrics_path"],
                    "diagnostic_metrics_path": entry["diagnostic_metrics_path"],
                    "baseline_abs_heatmap_path": heatmaps.get("abs_heatmap_path", ""),
                    "baseline_signed_heatmap_path": heatmaps.get("signed_heatmap_path", ""),
                }
            )
    return rows


def _px4_physical_csv_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    section = payload["px4_physical_vs_continuation"]
    for group_name, entries_key in (("main", "main_entries"), ("appendix", "appendix_entries")):
        for entry in section[entries_key]:
            rows.append(
                {
                    "scope": group_name,
                    "combo": entry["combo"],
                    "x_schema": entry["x_schema"],
                    "y_schema": entry["y_schema"],
                    "model_name": entry["model_name"],
                    "pooling_mode": entry["pooling_mode"],
                    "command_to_future_share": entry["command_to_future_share"],
                    "state_current_to_same_state_share": entry["state_current_to_same_state_share"],
                    "lag_to_future_share": entry["lag_to_future_share"],
                    "dominant_edges": summarize_edges(list(entry.get("dominant_edges", []) or []), limit=5),
                    "baseline_matrix_path": entry["baseline_matrix_path"],
                    "baseline_metrics_path": entry["baseline_metrics_path"],
                    "abs_heatmap_path": entry.get("abs_heatmap_path", ""),
                    "signed_heatmap_path": entry.get("signed_heatmap_path", ""),
                }
            )
    return rows


def _backend_alignment_csv_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    section = payload["backend_alignment"]
    for entry in section["shared_rows"]:
        rows.append(
            {
                "alignment_type": "shared",
                "alignment_key": entry["alignment_key"],
                "px4_combo": entry["px4_combo"],
                "ardupilot_combo": entry["ardupilot_combo"],
                "px4_minimal_x": entry["px4_minimal_x"],
                "ardupilot_minimal_x": entry["ardupilot_minimal_x"],
                "top_edge_overlap_jaccard": entry["top_edge_overlap_jaccard"],
                "px4_dominant_edges": summarize_edges(list(entry.get("px4_dominant_edges", []) or []), limit=5),
                "ardupilot_dominant_edges": summarize_edges(list(entry.get("ardupilot_dominant_edges", []) or []), limit=5),
                "px4_matrix_path": entry["px4_matrix_path"],
                "ardupilot_matrix_path": entry["ardupilot_matrix_path"],
            }
        )
    for entry in section["backend_specific"]["px4_only_next_raw_state"]:
        rows.append(
            {
                "alignment_type": "px4_only",
                "alignment_key": entry["alignment_key"],
                "px4_combo": entry["px4_combo"],
                "ardupilot_combo": "",
                "px4_minimal_x": entry["px4_minimal_x"],
                "ardupilot_minimal_x": "",
                "top_edge_overlap_jaccard": math.nan,
                "px4_dominant_edges": summarize_edges(list(entry.get("px4_dominant_edges", []) or []), limit=5),
                "ardupilot_dominant_edges": "",
                "px4_matrix_path": entry["px4_matrix_path"],
                "ardupilot_matrix_path": "",
            }
        )
    for entry in section["backend_specific"]["ardupilot_only_actuator_response"]:
        rows.append(
            {
                "alignment_type": "ardupilot_only",
                "alignment_key": entry["alignment_key"],
                "px4_combo": "",
                "ardupilot_combo": entry["ardupilot_combo"],
                "px4_minimal_x": "",
                "ardupilot_minimal_x": entry["ardupilot_minimal_x"],
                "top_edge_overlap_jaccard": math.nan,
                "px4_dominant_edges": "",
                "ardupilot_dominant_edges": summarize_edges(list(entry.get("ardupilot_dominant_edges", []) or []), limit=5),
                "px4_matrix_path": "",
                "ardupilot_matrix_path": entry["ardupilot_matrix_path"],
            }
        )
    return rows


def _ardupilot_conditioning_csv_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entry in payload["ardupilot_conditioning_failure"]["paths"]:
        rows.append(
            {
                "failure_path": entry["failure_path"],
                "combo": entry["combo"],
                "baseline_support": entry["baseline_support"],
                "diagnostic_support": entry["diagnostic_support"],
                "baseline_median_test_r2": entry["baseline_median_test_r2"],
                "diagnostic_median_test_r2": entry["diagnostic_median_test_r2"],
                "baseline_effective_condition_number": entry["baseline_effective_condition_number"],
                "diagnostic_effective_condition_number": entry["diagnostic_effective_condition_number"],
                "baseline_conditioning_pruned_features": "; ".join(entry["baseline_conditioning_pruned_features"]),
                "diagnostic_conditioning_pruned_features": "; ".join(entry["diagnostic_conditioning_pruned_features"]),
                "top_edge_overlap_jaccard": entry["top_edge_overlap_jaccard"],
                "baseline_dominant_edges": summarize_edges(list(entry.get("baseline_dominant_edges", []) or []), limit=5),
                "diagnostic_dominant_edges": summarize_edges(list(entry.get("diagnostic_dominant_edges", []) or []), limit=5),
                "baseline_matrix_path": entry["baseline_matrix_path"],
                "diagnostic_matrix_path": entry["diagnostic_matrix_path"],
                "baseline_metrics_path": entry["baseline_metrics_path"],
                "diagnostic_metrics_path": entry["diagnostic_metrics_path"],
                "baseline_abs_heatmap_path": entry["baseline_heatmaps"].get("abs_heatmap_path", ""),
                "diagnostic_abs_heatmap_path": entry["diagnostic_heatmaps"].get("abs_heatmap_path", ""),
                "baseline_heatmap_status": entry["baseline_heatmaps"].get("heatmap_status", ""),
                "diagnostic_heatmap_status": entry["diagnostic_heatmaps"].get("heatmap_status", ""),
            }
        )
    return rows


def _stability_boundary_csv_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entry in payload["stability_boundary"]["rows"]:
        rows.append(
            {
                "source_category": entry["source_category"],
                "backend": entry["backend"],
                "study_dir": entry["study_dir"],
                "combo": entry["combo"],
                "support": entry["support"],
                "generalization_status": entry["generalization_status"],
                "comparison_generalization_status": entry["comparison_generalization_status"],
                "effective_condition_number": entry["effective_condition_number"],
                "drivers": "; ".join(entry["drivers"]),
                "primary_driver": entry["primary_driver"],
                "matrix_path": entry["matrix_path"],
                "metrics_path": entry["metrics_path"],
                "abs_heatmap_path": entry.get("abs_heatmap_path", ""),
                "signed_heatmap_path": entry.get("signed_heatmap_path", ""),
                "heatmap_status": entry.get("heatmap_status", ""),
            }
        )
    return rows


def write_in_depth_analysis_artifacts(
    payload: dict[str, Any],
    *,
    output_dir: Path | None = None,
) -> Path:
    paths = _output_paths(output_dir)
    report_text = render_in_depth_analysis_markdown(payload, report_path=paths["report_path"])
    paths["report_path"].write_text(report_text, encoding="utf-8")
    write_json(paths["summary_path"], payload)
    write_rows_csv(paths["stable_core_table_path"], _stable_core_csv_rows(payload))
    write_rows_csv(paths["px4_physical_table_path"], _px4_physical_csv_rows(payload))
    write_rows_csv(paths["backend_alignment_table_path"], _backend_alignment_csv_rows(payload))
    write_rows_csv(paths["ardupilot_conditioning_table_path"], _ardupilot_conditioning_csv_rows(payload))
    write_rows_csv(paths["stability_boundary_table_path"], _stability_boundary_csv_rows(payload))
    write_yaml(
        paths["manifest_path"],
        {
            "study_name": STUDY_NAME,
            "study_id": paths["base_dir"].name,
            "source_studies": payload["source_studies"],
            "summary": {
                "px4_stable_core_count": payload["stable_core"]["px4"]["stable_core_count"],
                "ardupilot_stable_core_count": payload["stable_core"]["ardupilot"]["stable_core_count"],
                "shared_alignment_key_count": payload["backend_alignment"]["shared_alignment_key_count"],
            },
        },
    )
    return paths["base_dir"]


def render_in_depth_analysis_markdown(payload: dict[str, Any], *, report_path: Path | None = None) -> str:
    start_dir = report_path.parent if report_path is not None else Path.cwd()
    source = payload["source_studies"]
    stable_core = payload["stable_core"]
    px4_physical = payload["px4_physical_vs_continuation"]
    backend_alignment = payload["backend_alignment"]
    conditioning = payload["ardupilot_conditioning_failure"]
    boundary = payload["stability_boundary"]
    lines = [
        "# Formal V2 In-Depth Analysis",
        "",
        "## Inputs",
        f"- px4_baseline: `{_relative_path(source['px4_baseline'], start_dir)}`",
        f"- px4_diagnostic: `{_relative_path(source['px4_diagnostic'], start_dir)}`",
        f"- ardupilot_baseline: `{_relative_path(source['ardupilot_baseline'], start_dir)}`",
        f"- ardupilot_diagnostic: `{_relative_path(source['ardupilot_diagnostic'], start_dir)}`",
        f"- targeted_validation: `{_relative_path(source['targeted_validation'], start_dir)}`",
        f"- top_k: `{source['top_k']}`",
        "",
        "## 1. Stable-core Matrix Readout",
        f"- px4 stable_core_count: `{stable_core['px4']['stable_core_count']}`; baseline_subset_of_diagnostic=`{str(stable_core['px4']['baseline_is_subset_of_diagnostic']).lower()}`; diagnostic_only=`{stable_core['px4']['diagnostic_only_generalized_supported_count']}`",
        f"- ardupilot stable_core_count: `{stable_core['ardupilot']['stable_core_count']}`; baseline_subset_of_diagnostic=`{str(stable_core['ardupilot']['baseline_is_subset_of_diagnostic']).lower()}`; diagnostic_only=`{stable_core['ardupilot']['diagnostic_only_generalized_supported_count']}`",
        f"- table: `{_relative_path(start_dir.parent / 'tables' / 'stable_core_matrix_readout.csv', start_dir)}`",
    ]
    if stable_core["px4"]["entries"]:
        representative = stable_core["px4"]["entries"][0]
        lines.extend(
            [
                f"- representative_px4_combo: `{representative['combo']}`",
                f"- representative_px4_matrix: `{_relative_path(representative['baseline_matrix_path'], start_dir)}`",
                f"- representative_px4_metrics: `{_relative_path(representative['baseline_metrics_path'], start_dir)}`",
            ]
        )
    if stable_core["ardupilot"]["entries"]:
        representative = stable_core["ardupilot"]["entries"][0]
        lines.extend(
            [
                f"- representative_ardupilot_combo: `{representative['combo']}`",
                f"- representative_ardupilot_matrix: `{_relative_path(representative['baseline_matrix_path'], start_dir)}`",
                f"- representative_ardupilot_metrics: `{_relative_path(representative['baseline_metrics_path'], start_dir)}`",
            ]
        )
    lines.extend(
        [
            "",
            "## 2. PX4 Physical vs State Continuation",
            f"- main_scope_count: `{px4_physical['main_count']}`; appendix_scope_count: `{px4_physical['appendix_count']}`",
            f"- table: `{_relative_path(start_dir.parent / 'tables' / 'px4_physical_vs_state_continuation.csv', start_dir)}`",
        ]
    )
    for item in px4_physical["repeated_patterns"][:5]:
        lines.append(f"- repeated_pattern: `{item['pattern']}` count=`{item['count']}`")
    lines.extend(
        [
            "",
            "## 3. Backend Alignment",
            f"- strict_schema_overlap_count: `{backend_alignment['strict_schema_overlap_count']}`",
            f"- shared_alignment_key_count: `{backend_alignment['shared_alignment_key_count']}`",
            f"- table: `{_relative_path(start_dir.parent / 'tables' / 'backend_alignment.csv', start_dir)}`",
        ]
    )
    for item in backend_alignment["shared_rows"][:3]:
        lines.append(
            f"- shared_alignment: `{item['alignment_key']}` => px4=`{item['px4_combo']}` vs ardupilot=`{item['ardupilot_combo']}`; top_edge_jaccard=`{_safe_float(item['top_edge_overlap_jaccard']):.4f}`"
        )
    lines.extend(
        [
            "",
            "## 4. ArduPilot Conditioning Failure",
            f"- table: `{_relative_path(start_dir.parent / 'tables' / 'ardupilot_conditioning_failure.csv', start_dir)}`",
        ]
    )
    for item in conditioning["paths"]:
        lines.extend(
            [
                f"- `{item['failure_path']}` combo=`{item['combo']}`",
                f"  baseline_metrics=`{_relative_path(item['baseline_metrics_path'], start_dir)}` diagnostic_metrics=`{_relative_path(item['diagnostic_metrics_path'], start_dir)}` top_edge_jaccard=`{_safe_float(item['top_edge_overlap_jaccard']):.4f}`",
            ]
        )
    lines.extend(
        [
            "",
            "## 5. Stability Boundary",
            f"- row_count: `{boundary['row_count']}`",
            f"- primary_driver_counts: `{boundary['primary_driver_counts']}`",
            f"- table: `{_relative_path(start_dir.parent / 'tables' / 'stability_boundary.csv', start_dir)}`",
        ]
    )
    for driver, count in sorted(boundary["primary_driver_counts"].items()):
        lines.append(f"- primary_driver `{driver}`: `{count}`")
    return "\n".join(lines) + "\n"


def run_formal_v2_in_depth_analysis(
    *,
    px4_baseline_dir: Path | None = None,
    px4_diagnostic_dir: Path | None = None,
    ardupilot_baseline_dir: Path | None = None,
    ardupilot_diagnostic_dir: Path | None = None,
    targeted_validation_dir: Path | None = None,
    output_dir: Path | None = None,
    top_k: int = DEFAULT_TOP_K,
) -> Path:
    analyzer = FormalV2InDepthAnalyzer(
        px4_baseline_dir=px4_baseline_dir or DEFAULT_CANONICAL_STUDIES["px4_baseline"],
        px4_diagnostic_dir=px4_diagnostic_dir or DEFAULT_CANONICAL_STUDIES["px4_diagnostic"],
        ardupilot_baseline_dir=ardupilot_baseline_dir or DEFAULT_CANONICAL_STUDIES["ardupilot_baseline"],
        ardupilot_diagnostic_dir=ardupilot_diagnostic_dir or DEFAULT_CANONICAL_STUDIES["ardupilot_diagnostic"],
        targeted_validation_dir=targeted_validation_dir or DEFAULT_CANONICAL_STUDIES["targeted_validation"],
        top_k=top_k,
    )
    payload = analyzer.build_payload()
    return write_in_depth_analysis_artifacts(payload, output_dir=output_dir)
