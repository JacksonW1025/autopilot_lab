from __future__ import annotations

import csv
import math
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from linearity_core.io import read_yaml, write_json, write_rows_csv, write_yaml
from linearity_core.paths import STUDY_ARTIFACT_ROOT, WORKSPACE_ROOT

from .in_depth_analysis import classify_feature_block, compute_feature_block_shares
from .matrix_gallery import MatrixData, load_matrix_csv

STUDY_NAME = "formal_v2_anchor_deep_dive"
DEFAULT_RAW_TOP_K = 4
TOPK_SORT_ROUND_DECIMALS = 12
DOMINANT_TOP1_THRESHOLD = 0.8
SCENARIO_NAMES = ("dynamic", "nominal", "throttle_biased")
DEFAULT_CANONICAL_STUDIES = {
    "px4_baseline": STUDY_ARTIFACT_ROOT / "20260410_224818_px4_real_generalization_ablation",
    "px4_diagnostic": STUDY_ARTIFACT_ROOT / "20260411_021910_px4_generalization_diagnostic_matrix",
    "ardupilot_baseline": STUDY_ARTIFACT_ROOT / "20260413_070802_ardupilot_real_generalization_ablation",
    "ardupilot_diagnostic": STUDY_ARTIFACT_ROOT / "20260413_091420_ardupilot_generalization_diagnostic_matrix",
    "targeted_validation": STUDY_ARTIFACT_ROOT / "20260413_134505_ardupilot_state_evolution_validation",
}
PX4_TABLE_FIELDNAMES = [
    "anchor_id",
    "study_phase",
    "backend",
    "mode_scope",
    "scenario_scope",
    "x_schema",
    "y_schema",
    "model_name",
    "pooling_mode",
    "support",
    "generalization_status",
    "median_test_r2",
    "coefficient_stability",
    "scenario_consistency",
    "scenario_r2_dynamic",
    "scenario_r2_nominal",
    "scenario_r2_throttle_biased",
    "x_effective_condition_number",
    "f_rank",
    "f_effective_rank",
    "f_condition_number",
    "mask_nonzero_count",
    "active_feature_count",
    "active_response_count",
    "row_nnz_min",
    "row_nnz_median",
    "row_nnz_max",
    "col_nnz_min",
    "col_nnz_median",
    "col_nnz_max",
    "abs_mass_command",
    "abs_mass_state_current",
    "abs_mass_state_lag_1",
    "abs_mass_state_lag_2",
    "abs_mass_state_lag_3",
    "abs_mass_other_augmented",
    "mean_top1_share",
    "mean_top3_share",
    "mean_top5_share",
    "mean_gini",
    "mean_effective_support_size",
    "same_combo_mask_jaccard_to_pair",
    "same_combo_raw_top4_jaccard_to_pair",
    "same_combo_raw_top4_sign_match_to_pair",
]
ARDUPILOT_TABLE_FIELDNAMES = [
    "anchor_id",
    "family_id",
    "study_phase",
    "backend",
    "mode_scope",
    "scenario_scope",
    "x_schema",
    "y_schema",
    "model_name",
    "pooling_mode",
    "support",
    "generalization_status",
    "median_test_r2",
    "coefficient_stability",
    "scenario_consistency",
    "scenario_r2_dynamic",
    "scenario_r2_nominal",
    "scenario_r2_throttle_biased",
    "x_effective_condition_number",
    "f_rank",
    "f_effective_rank",
    "f_condition_number",
    "mask_nonzero_count",
    "active_feature_count",
    "active_response_count",
    "mask_empty_flag",
    "partial_mask_flag",
    "mean_top1_share",
    "mean_top3_share",
    "mean_top5_share",
    "mean_gini",
    "mean_effective_support_size",
    "pair_mask_jaccard",
    "pair_raw_top4_jaccard",
    "pair_raw_top4_sign_match",
    "dominant_response_count",
    "notes_source_matrix_path",
    "notes_source_mask_path",
    "notes_source_metrics_path",
]


@dataclass(frozen=True)
class ComboRef:
    x_schema: str
    y_schema: str
    model_name: str
    pooling_mode: str

    def fit_dir_name(self) -> str:
        return f"{self.x_schema}__{self.y_schema}__{self.pooling_mode}"


@dataclass(frozen=True)
class AnchorFamilySpec:
    family_id: str
    backend: str
    mode_scope: str
    scenario_scope: str
    combo: ComboRef
    baseline_study_key: str
    diagnostic_study_key: str


@dataclass(frozen=True)
class LabeledMatrix:
    path: Path
    feature_names: list[str]
    response_names: list[str]
    values: np.ndarray


ANCHOR_FAMILIES = [
    AnchorFamilySpec(
        family_id="A1",
        backend="px4",
        mode_scope="OFFBOARD_ATTITUDE, POSCTL",
        scenario_scope="dynamic, nominal, throttle_biased",
        combo=ComboRef("full_augmented", "next_raw_state", "ols_affine", "stratified"),
        baseline_study_key="px4_baseline",
        diagnostic_study_key="px4_diagnostic",
    ),
    AnchorFamilySpec(
        family_id="B1",
        backend="px4",
        mode_scope="OFFBOARD_ATTITUDE, POSCTL",
        scenario_scope="dynamic, nominal, throttle_biased",
        combo=ComboRef("full_augmented", "delta_state", "ols_affine", "stratified"),
        baseline_study_key="px4_baseline",
        diagnostic_study_key="px4_diagnostic",
    ),
    AnchorFamilySpec(
        family_id="A2",
        backend="ardupilot",
        mode_scope="GUIDED_NOGPS, STABILIZE",
        scenario_scope="dynamic, nominal, throttle_biased",
        combo=ComboRef("commands_only", "actuator_response", "ridge_affine", "pooled"),
        baseline_study_key="ardupilot_baseline",
        diagnostic_study_key="ardupilot_diagnostic",
    ),
    AnchorFamilySpec(
        family_id="C1",
        backend="ardupilot",
        mode_scope="GUIDED_NOGPS, STABILIZE",
        scenario_scope="dynamic, nominal, throttle_biased",
        combo=ComboRef("commands_plus_state_history", "selected_state_subset", "ols_affine", "pooled"),
        baseline_study_key="ardupilot_baseline",
        diagnostic_study_key="ardupilot_diagnostic",
    ),
    AnchorFamilySpec(
        family_id="D1",
        backend="ardupilot",
        mode_scope="STABILIZE",
        scenario_scope="dynamic, nominal, throttle_biased",
        combo=ComboRef("commands_plus_state_history", "selected_state_subset", "ols_affine", "pooled"),
        baseline_study_key="stabilize_baseline",
        diagnostic_study_key="stabilize_diagnostic",
    ),
    AnchorFamilySpec(
        family_id="D2",
        backend="ardupilot",
        mode_scope="GUIDED_NOGPS",
        scenario_scope="dynamic, nominal, throttle_biased",
        combo=ComboRef("commands_plus_state_history", "selected_state_subset", "ols_affine", "pooled"),
        baseline_study_key="guided_nogps_baseline",
        diagnostic_study_key="guided_nogps_diagnostic",
    ),
]


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def _read_optional_payload(path: Path) -> dict[str, Any]:
    return read_yaml(path) if path.exists() else {}


def _prefer_workspace_study_path(path: Path) -> Path:
    candidate = path.expanduser()
    workspace_candidate = STUDY_ARTIFACT_ROOT / candidate.name
    return workspace_candidate if workspace_candidate.exists() else candidate


def _workspace_relative_path(path: Path) -> str:
    absolute = path.expanduser().absolute()
    try:
        return str(absolute.relative_to(WORKSPACE_ROOT))
    except ValueError:
        return str(absolute)


def _relative_output_path(target: Path, start: Path) -> str:
    return os.path.relpath(target.absolute(), start.absolute())


def _fit_dir(study_dir: Path, combo: ComboRef) -> Path:
    return study_dir / "fits" / combo.fit_dir_name() / combo.model_name


def _metrics_path(study_dir: Path, combo: ComboRef) -> Path:
    return _fit_dir(study_dir, combo) / "metrics.json"


def _matrix_path(study_dir: Path, combo: ComboRef) -> Path:
    return _fit_dir(study_dir, combo) / "matrix_f.csv"


def _mask_path(study_dir: Path, combo: ComboRef) -> Path:
    return _fit_dir(study_dir, combo) / "sparsity_mask.csv"


def _load_labeled_csv(path: Path) -> LabeledMatrix:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if not header or len(header) < 2:
            raise ValueError(f"invalid csv header: {path}")
        response_names = [str(item) for item in header[1:]]
        feature_names: list[str] = []
        rows: list[list[float]] = []
        for row in reader:
            if not row:
                continue
            feature_names.append(str(row[0]))
            rows.append([float(value) for value in row[1:]])
    values = np.asarray(rows, dtype=float)
    return LabeledMatrix(
        path=path,
        feature_names=feature_names,
        response_names=response_names,
        values=values,
    )


def _output_paths(output_dir: Path | None) -> dict[str, Path]:
    if output_dir is None:
        study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_{STUDY_NAME}"
        base_dir = STUDY_ARTIFACT_ROOT / study_id
    else:
        base_dir = output_dir.expanduser().absolute()
    summary_dir = base_dir / "summary"
    tables_dir = base_dir / "tables"
    for path in (base_dir, summary_dir, tables_dir):
        path.mkdir(parents=True, exist_ok=True)
    return {
        "base_dir": base_dir,
        "summary_dir": summary_dir,
        "tables_dir": tables_dir,
        "manifest_path": base_dir / "manifest.yaml",
        "summary_path": summary_dir / "anchor_deep_dive.json",
        "px4_table_path": tables_dir / "px4_a1_b1_matrix_comparison.csv",
        "ardupilot_table_path": tables_dir / "ardupilot_a2_c1_d1_d2_boundary.csv",
    }


def _mask_edge_set(mask_data: LabeledMatrix) -> set[tuple[str, str]]:
    values = np.asarray(mask_data.values, dtype=float)
    edges: set[tuple[str, str]] = set()
    for feature_index, feature_name in enumerate(mask_data.feature_names):
        for response_index, response_name in enumerate(mask_data.response_names):
            if _safe_float(values[feature_index, response_index]) >= 0.5:
                edges.add((feature_name, response_name))
    return edges


def _rounded_abs_weight(weight: float) -> float:
    return round(abs(weight), TOPK_SORT_ROUND_DECIMALS)


def _raw_topk_edge_signs(matrix_data: MatrixData, top_k: int) -> dict[tuple[str, str], int]:
    values = np.asarray(matrix_data.values, dtype=float)
    edges: dict[tuple[str, str], int] = {}
    for response_index, response_name in enumerate(matrix_data.response_names):
        ranked: list[tuple[float, str, float]] = []
        for feature_index, feature_name in enumerate(matrix_data.feature_names):
            weight = _safe_float(values[feature_index, response_index])
            if not math.isfinite(weight) or weight == 0.0:
                continue
            ranked.append((-_rounded_abs_weight(weight), feature_name, weight))
        ranked.sort(key=lambda item: (item[0], item[1]))
        for _, feature_name, weight in ranked[:top_k]:
            edges[(feature_name, response_name)] = 1 if weight > 0.0 else -1
    return edges


def _jaccard(left: set[Any], right: set[Any]) -> float:
    union = left | right
    return (len(left & right) / len(union)) if union else math.nan


def _pair_overlap(
    baseline_mask: LabeledMatrix,
    diagnostic_mask: LabeledMatrix,
    baseline_matrix: MatrixData,
    diagnostic_matrix: MatrixData,
    *,
    raw_top_k: int,
) -> dict[str, float]:
    baseline_mask_edges = _mask_edge_set(baseline_mask)
    diagnostic_mask_edges = _mask_edge_set(diagnostic_mask)
    mask_jaccard = (
        math.nan
        if not baseline_mask_edges or not diagnostic_mask_edges
        else _jaccard(baseline_mask_edges, diagnostic_mask_edges)
    )

    baseline_raw = _raw_topk_edge_signs(baseline_matrix, raw_top_k)
    diagnostic_raw = _raw_topk_edge_signs(diagnostic_matrix, raw_top_k)
    baseline_raw_edges = set(baseline_raw.keys())
    diagnostic_raw_edges = set(diagnostic_raw.keys())
    raw_jaccard = _jaccard(baseline_raw_edges, diagnostic_raw_edges)
    raw_intersection = baseline_raw_edges & diagnostic_raw_edges
    raw_sign_match = (
        sum(1 for edge in raw_intersection if baseline_raw[edge] == diagnostic_raw[edge]) / len(raw_intersection)
        if raw_intersection
        else math.nan
    )
    return {
        "mask_jaccard": mask_jaccard,
        "raw_topk_jaccard": raw_jaccard,
        "raw_topk_sign_match": raw_sign_match,
    }


def _gini_from_weights(weights: np.ndarray) -> float:
    values = np.asarray(weights, dtype=float)
    values = values[np.isfinite(values)]
    values = values[values > 0.0]
    if values.size == 0:
        return 0.0
    sorted_values = np.sort(values)
    n = float(sorted_values.size)
    total = float(np.sum(sorted_values))
    if total <= 0.0:
        return 0.0
    index = np.arange(1, sorted_values.size + 1, dtype=float)
    return float(np.sum((2.0 * index - n - 1.0) * sorted_values) / (n * total))


def _matrix_mass_stats(matrix_data: MatrixData) -> dict[str, float]:
    values = np.asarray(matrix_data.values, dtype=float)
    top1_list: list[float] = []
    top3_list: list[float] = []
    top5_list: list[float] = []
    gini_list: list[float] = []
    eff_support_list: list[float] = []
    dominant_response_count = 0
    for response_index in range(values.shape[1]):
        column = np.abs(values[:, response_index])
        column = column[np.isfinite(column)]
        total = float(np.sum(column))
        if total <= 0.0:
            top1_list.append(0.0)
            top3_list.append(0.0)
            top5_list.append(0.0)
            gini_list.append(0.0)
            eff_support_list.append(0.0)
            continue
        sorted_column = np.sort(column)[::-1]
        probabilities = column / total
        top1 = float(np.sum(sorted_column[:1]) / total)
        top3 = float(np.sum(sorted_column[:3]) / total)
        top5 = float(np.sum(sorted_column[:5]) / total)
        if top1 >= DOMINANT_TOP1_THRESHOLD:
            dominant_response_count += 1
        top1_list.append(top1)
        top3_list.append(top3)
        top5_list.append(top5)
        gini_list.append(_gini_from_weights(column))
        eff_support_list.append(float(1.0 / np.sum(np.square(probabilities))))
    return {
        "mean_top1_share": float(np.mean(top1_list)) if top1_list else math.nan,
        "mean_top3_share": float(np.mean(top3_list)) if top3_list else math.nan,
        "mean_top5_share": float(np.mean(top5_list)) if top5_list else math.nan,
        "mean_gini": float(np.mean(gini_list)) if gini_list else math.nan,
        "mean_effective_support_size": float(np.mean(eff_support_list)) if eff_support_list else math.nan,
        "dominant_response_count": dominant_response_count,
    }


def _mask_stats(mask_data: LabeledMatrix) -> dict[str, float | int | bool]:
    active = np.asarray(mask_data.values, dtype=float) >= 0.5
    row_counts = np.sum(active, axis=1)
    col_counts = np.sum(active, axis=0)
    total_edges = int(active.size)
    nonzero_count = int(np.sum(active))
    return {
        "mask_nonzero_count": nonzero_count,
        "active_feature_count": int(np.sum(row_counts > 0)),
        "active_response_count": int(np.sum(col_counts > 0)),
        "row_nnz_min": int(np.min(row_counts)) if row_counts.size else 0,
        "row_nnz_median": float(np.median(row_counts)) if row_counts.size else 0.0,
        "row_nnz_max": int(np.max(row_counts)) if row_counts.size else 0,
        "col_nnz_min": int(np.min(col_counts)) if col_counts.size else 0,
        "col_nnz_median": float(np.median(col_counts)) if col_counts.size else 0.0,
        "col_nnz_max": int(np.max(col_counts)) if col_counts.size else 0,
        "mask_empty_flag": nonzero_count == 0,
        "partial_mask_flag": 0 < nonzero_count < total_edges,
    }


def _f_svd_stats(matrix_data: MatrixData) -> dict[str, float | int]:
    values = np.asarray(matrix_data.values, dtype=float)
    if values.size == 0:
        return {"f_rank": 0, "f_effective_rank": 0.0, "f_condition_number": math.nan}
    singular_values = np.linalg.svd(values, compute_uv=False)
    singular_values = singular_values[np.isfinite(singular_values)]
    if singular_values.size == 0:
        return {"f_rank": 0, "f_effective_rank": 0.0, "f_condition_number": math.nan}
    positive = singular_values[singular_values > 0.0]
    if positive.size == 0:
        return {"f_rank": 0, "f_effective_rank": 0.0, "f_condition_number": math.nan}
    probabilities = positive / np.sum(positive)
    entropy = -float(np.sum(probabilities * np.log(probabilities)))
    return {
        "f_rank": int(np.linalg.matrix_rank(values)),
        "f_effective_rank": float(math.exp(entropy)),
        "f_condition_number": float(positive[0] / positive[-1]),
    }


class AnchorDeepDiveAnalyzer:
    def __init__(
        self,
        *,
        px4_baseline_dir: Path,
        px4_diagnostic_dir: Path,
        ardupilot_baseline_dir: Path,
        ardupilot_diagnostic_dir: Path,
        targeted_validation_dir: Path,
        stabilize_baseline_dir: Path | None = None,
        stabilize_diagnostic_dir: Path | None = None,
        guided_nogps_baseline_dir: Path | None = None,
        guided_nogps_diagnostic_dir: Path | None = None,
        raw_top_k: int = DEFAULT_RAW_TOP_K,
    ) -> None:
        self.raw_top_k = int(raw_top_k)
        self.targeted_validation_dir = _prefer_workspace_study_path(targeted_validation_dir)
        self.study_dirs = {
            "px4_baseline": _prefer_workspace_study_path(px4_baseline_dir),
            "px4_diagnostic": _prefer_workspace_study_path(px4_diagnostic_dir),
            "ardupilot_baseline": _prefer_workspace_study_path(ardupilot_baseline_dir),
            "ardupilot_diagnostic": _prefer_workspace_study_path(ardupilot_diagnostic_dir),
        }
        targeted_map = self._resolve_targeted_study_dirs(
            stabilize_baseline_dir=stabilize_baseline_dir,
            stabilize_diagnostic_dir=stabilize_diagnostic_dir,
            guided_nogps_baseline_dir=guided_nogps_baseline_dir,
            guided_nogps_diagnostic_dir=guided_nogps_diagnostic_dir,
        )
        self.study_dirs.update(targeted_map)
        self._scenario_cache: dict[Path, dict[str, dict[str, Any]]] = {}
        self._matrix_cache: dict[Path, MatrixData] = {}
        self._mask_cache: dict[Path, LabeledMatrix] = {}
        self._metrics_cache: dict[Path, dict[str, Any]] = {}

    def _resolve_targeted_study_dirs(
        self,
        *,
        stabilize_baseline_dir: Path | None,
        stabilize_diagnostic_dir: Path | None,
        guided_nogps_baseline_dir: Path | None,
        guided_nogps_diagnostic_dir: Path | None,
    ) -> dict[str, Path]:
        provided = {
            "stabilize_baseline": stabilize_baseline_dir,
            "stabilize_diagnostic": stabilize_diagnostic_dir,
            "guided_nogps_baseline": guided_nogps_baseline_dir,
            "guided_nogps_diagnostic": guided_nogps_diagnostic_dir,
        }
        if all(path is not None for path in provided.values()):
            return {key: _prefer_workspace_study_path(path) for key, path in provided.items() if path is not None}

        payload = _read_optional_payload(self.targeted_validation_dir / "summary" / "state_evolution_validation.json")
        modes = dict(payload.get("modes", {}) or {})
        if not modes:
            raise FileNotFoundError(
                f"targeted validation summary missing modes in {self.targeted_validation_dir / 'summary' / 'state_evolution_validation.json'}"
            )
        resolved = {
            "stabilize_baseline": _prefer_workspace_study_path(Path(str(modes["stabilize"]["baseline_dir"]))),
            "stabilize_diagnostic": _prefer_workspace_study_path(Path(str(modes["stabilize"]["diagnostic_dir"]))),
            "guided_nogps_baseline": _prefer_workspace_study_path(Path(str(modes["guided_nogps"]["baseline_dir"]))),
            "guided_nogps_diagnostic": _prefer_workspace_study_path(Path(str(modes["guided_nogps"]["diagnostic_dir"]))),
        }
        for key, value in provided.items():
            if value is not None:
                resolved[key] = _prefer_workspace_study_path(value)
        return resolved

    def scenario_map(self, study_dir: Path) -> dict[str, dict[str, Any]]:
        key = study_dir.absolute()
        if key not in self._scenario_cache:
            payload = _read_optional_payload(study_dir / "summary" / "scenario_generalization.json")
            entries = {}
            for entry in list(payload.get("entries", []) or []):
                combo_key = "|".join(
                    [
                        str(entry.get("x_schema", "")),
                        str(entry.get("y_schema", "")),
                        str(entry.get("model_name", "")),
                        str(entry.get("pooling_mode", "")),
                    ]
                )
                entries[combo_key] = dict(entry)
            self._scenario_cache[key] = entries
        return self._scenario_cache[key]

    def scenario_entry(self, study_dir: Path, combo: ComboRef) -> dict[str, Any]:
        combo_key = "|".join([combo.x_schema, combo.y_schema, combo.model_name, combo.pooling_mode])
        try:
            return self.scenario_map(study_dir)[combo_key]
        except KeyError as exc:
            raise KeyError(f"missing scenario_generalization entry for {combo_key} in {study_dir}") from exc

    def matrix_data(self, study_dir: Path, combo: ComboRef) -> MatrixData:
        path = _matrix_path(study_dir, combo).absolute()
        if path not in self._matrix_cache:
            self._matrix_cache[path] = load_matrix_csv(path)
        return self._matrix_cache[path]

    def mask_data(self, study_dir: Path, combo: ComboRef) -> LabeledMatrix:
        path = _mask_path(study_dir, combo).absolute()
        if path not in self._mask_cache:
            self._mask_cache[path] = _load_labeled_csv(path)
        return self._mask_cache[path]

    def metrics_payload(self, study_dir: Path, combo: ComboRef) -> dict[str, Any]:
        path = _metrics_path(study_dir, combo).absolute()
        if path not in self._metrics_cache:
            self._metrics_cache[path] = _read_optional_payload(path)
        return self._metrics_cache[path]

    def pair_metrics(self, family: AnchorFamilySpec) -> dict[str, float]:
        baseline_dir = self.study_dirs[family.baseline_study_key]
        diagnostic_dir = self.study_dirs[family.diagnostic_study_key]
        return _pair_overlap(
            self.mask_data(baseline_dir, family.combo),
            self.mask_data(diagnostic_dir, family.combo),
            self.matrix_data(baseline_dir, family.combo),
            self.matrix_data(diagnostic_dir, family.combo),
            raw_top_k=self.raw_top_k,
        )

    def _base_row(self, family: AnchorFamilySpec, *, study_phase: str) -> dict[str, Any]:
        study_key = family.baseline_study_key if study_phase == "baseline" else family.diagnostic_study_key
        study_dir = self.study_dirs[study_key]
        scenario_entry = self.scenario_entry(study_dir, family.combo)
        matrix_data = self.matrix_data(study_dir, family.combo)
        mask_data = self.mask_data(study_dir, family.combo)
        metrics_payload = self.metrics_payload(study_dir, family.combo)
        mask_stats = _mask_stats(mask_data)
        block_shares = compute_feature_block_shares(matrix_data)
        mass_stats = _matrix_mass_stats(matrix_data)
        svd_stats = _f_svd_stats(matrix_data)
        subgroup_r2 = dict(scenario_entry.get("scenario_subgroup_r2", {}) or {})
        row = {
            "study_phase": study_phase,
            "backend": family.backend,
            "mode_scope": family.mode_scope,
            "scenario_scope": family.scenario_scope,
            "x_schema": family.combo.x_schema,
            "y_schema": family.combo.y_schema,
            "model_name": family.combo.model_name,
            "pooling_mode": family.combo.pooling_mode,
            "support": str(scenario_entry.get("support", "")),
            "generalization_status": str(scenario_entry.get("generalization_status", "")),
            "median_test_r2": _safe_float(scenario_entry.get("median_test_r2", metrics_payload.get("median_test_r2"))),
            "coefficient_stability": _safe_float(
                scenario_entry.get("coefficient_stability", metrics_payload.get("coefficient_stability"))
            ),
            "scenario_consistency": _safe_float(
                scenario_entry.get("scenario_consistency", metrics_payload.get("scenario_consistency"))
            ),
            "scenario_r2_dynamic": _safe_float(subgroup_r2.get("dynamic")),
            "scenario_r2_nominal": _safe_float(subgroup_r2.get("nominal")),
            "scenario_r2_throttle_biased": _safe_float(subgroup_r2.get("throttle_biased")),
            "x_effective_condition_number": _safe_float(
                scenario_entry.get("effective_condition_number", metrics_payload.get("effective_condition_number"))
            ),
            "abs_mass_command": block_shares["command"],
            "abs_mass_state_current": block_shares["state_current"],
            "abs_mass_state_lag_1": block_shares["state_lag_1"],
            "abs_mass_state_lag_2": block_shares["state_lag_2"],
            "abs_mass_state_lag_3": block_shares["state_lag_3"],
            "abs_mass_other_augmented": block_shares["other_augmented"],
            "notes_source_matrix_path": _workspace_relative_path(_matrix_path(study_dir, family.combo)),
            "notes_source_mask_path": _workspace_relative_path(_mask_path(study_dir, family.combo)),
            "notes_source_metrics_path": _workspace_relative_path(_metrics_path(study_dir, family.combo)),
        }
        row.update(mask_stats)
        row.update(mass_stats)
        row.update(svd_stats)
        return row

    def build_px4_rows(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for family_id in ("A1", "B1"):
            family = next(item for item in ANCHOR_FAMILIES if item.family_id == family_id)
            pair_metrics = self.pair_metrics(family)
            for phase in ("baseline", "diagnostic"):
                row = self._base_row(family, study_phase=phase)
                row.update(
                    {
                        "anchor_id": f"{family.family_id}_{phase}",
                        "same_combo_mask_jaccard_to_pair": pair_metrics["mask_jaccard"],
                        "same_combo_raw_top4_jaccard_to_pair": pair_metrics["raw_topk_jaccard"],
                        "same_combo_raw_top4_sign_match_to_pair": pair_metrics["raw_topk_sign_match"],
                    }
                )
                rows.append({name: row.get(name) for name in PX4_TABLE_FIELDNAMES})
        return rows

    def build_ardupilot_rows(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for family_id in ("A2", "C1", "D1", "D2"):
            family = next(item for item in ANCHOR_FAMILIES if item.family_id == family_id)
            pair_metrics = self.pair_metrics(family)
            for phase in ("baseline", "diagnostic"):
                row = self._base_row(family, study_phase=phase)
                row.update(
                    {
                        "anchor_id": f"{family.family_id}_{phase}",
                        "family_id": family.family_id,
                        "pair_mask_jaccard": pair_metrics["mask_jaccard"],
                        "pair_raw_top4_jaccard": pair_metrics["raw_topk_jaccard"],
                        "pair_raw_top4_sign_match": pair_metrics["raw_topk_sign_match"],
                    }
                )
                rows.append({name: row.get(name) for name in ARDUPILOT_TABLE_FIELDNAMES})
        return rows

    def build_summary(self, px4_rows: list[dict[str, Any]], ardupilot_rows: list[dict[str, Any]]) -> dict[str, Any]:
        px4_lookup = {row["anchor_id"]: row for row in px4_rows}
        ardupilot_lookup = {row["anchor_id"]: row for row in ardupilot_rows}
        mask_empty_families = sorted(
            {
                row["family_id"]
                for row in ardupilot_rows
                if bool(row.get("mask_empty_flag"))
            }
        )
        raw_stable_but_formally_blocked = sorted(
            {
                row["family_id"]
                for row in ardupilot_rows
                if row.get("generalization_status") != "generalized_supported"
                and _safe_float(row.get("pair_raw_top4_jaccard")) >= 0.9
            }
        )
        return {
            "px4_line": {
                "a1_support": px4_lookup["A1_baseline"]["support"],
                "a1_generalization_status": px4_lookup["A1_baseline"]["generalization_status"],
                "a1_same_combo_mask_jaccard": px4_lookup["A1_baseline"]["same_combo_mask_jaccard_to_pair"],
                "a1_same_combo_raw_top4_jaccard": px4_lookup["A1_baseline"]["same_combo_raw_top4_jaccard_to_pair"],
                "b1_support": px4_lookup["B1_baseline"]["support"],
                "b1_generalization_status": px4_lookup["B1_baseline"]["generalization_status"],
                "b1_same_combo_mask_jaccard": px4_lookup["B1_baseline"]["same_combo_mask_jaccard_to_pair"],
                "b1_same_combo_raw_top4_jaccard": px4_lookup["B1_baseline"]["same_combo_raw_top4_jaccard_to_pair"],
                "contrast_driver": "scenario_stability_gap dominates over raw sparsity differences between A1 and B1",
            },
            "ardupilot_line": {
                "a2_structure_type": "single-row direct-control actuator mapping dominated by command_throttle",
                "c1_blocking_driver": "raw autoregressive template stays stable but billion-scale X conditioning limits formal support",
                "d1_transition_driver": "mode-isolated baseline survives only locally before diagnostic-phase raw support collapses under worse conditioning",
                "d2_blocking_driver": "persistent autoregressive raw template remains formally blocked because masks stay empty under pathological conditioning",
                "mask_empty_families": mask_empty_families,
                "raw_stable_but_formally_blocked_families": raw_stable_but_formally_blocked,
            },
        }


def run_formal_v2_anchor_deep_dive(
    *,
    px4_baseline_dir: Path | None = None,
    px4_diagnostic_dir: Path | None = None,
    ardupilot_baseline_dir: Path | None = None,
    ardupilot_diagnostic_dir: Path | None = None,
    targeted_validation_dir: Path | None = None,
    stabilize_baseline_dir: Path | None = None,
    stabilize_diagnostic_dir: Path | None = None,
    guided_nogps_baseline_dir: Path | None = None,
    guided_nogps_diagnostic_dir: Path | None = None,
    output_dir: Path | None = None,
    raw_top_k: int = DEFAULT_RAW_TOP_K,
) -> Path:
    analyzer = AnchorDeepDiveAnalyzer(
        px4_baseline_dir=px4_baseline_dir or DEFAULT_CANONICAL_STUDIES["px4_baseline"],
        px4_diagnostic_dir=px4_diagnostic_dir or DEFAULT_CANONICAL_STUDIES["px4_diagnostic"],
        ardupilot_baseline_dir=ardupilot_baseline_dir or DEFAULT_CANONICAL_STUDIES["ardupilot_baseline"],
        ardupilot_diagnostic_dir=ardupilot_diagnostic_dir or DEFAULT_CANONICAL_STUDIES["ardupilot_diagnostic"],
        targeted_validation_dir=targeted_validation_dir or DEFAULT_CANONICAL_STUDIES["targeted_validation"],
        stabilize_baseline_dir=stabilize_baseline_dir,
        stabilize_diagnostic_dir=stabilize_diagnostic_dir,
        guided_nogps_baseline_dir=guided_nogps_baseline_dir,
        guided_nogps_diagnostic_dir=guided_nogps_diagnostic_dir,
        raw_top_k=raw_top_k,
    )
    outputs = _output_paths(output_dir)
    px4_rows = analyzer.build_px4_rows()
    ardupilot_rows = analyzer.build_ardupilot_rows()
    summary = analyzer.build_summary(px4_rows, ardupilot_rows)
    write_rows_csv(outputs["px4_table_path"], px4_rows, fieldnames=PX4_TABLE_FIELDNAMES)
    write_rows_csv(outputs["ardupilot_table_path"], ardupilot_rows, fieldnames=ARDUPILOT_TABLE_FIELDNAMES)
    write_json(outputs["summary_path"], summary)
    manifest = {
        "study_name": STUDY_NAME,
        "generated_at": f"{datetime.now(timezone.utc).astimezone().isoformat()}",
        "raw_top_k": int(raw_top_k),
        "source_studies": {
            "px4_baseline": _workspace_relative_path(analyzer.study_dirs["px4_baseline"]),
            "px4_diagnostic": _workspace_relative_path(analyzer.study_dirs["px4_diagnostic"]),
            "ardupilot_baseline": _workspace_relative_path(analyzer.study_dirs["ardupilot_baseline"]),
            "ardupilot_diagnostic": _workspace_relative_path(analyzer.study_dirs["ardupilot_diagnostic"]),
            "targeted_validation": _workspace_relative_path(analyzer.targeted_validation_dir),
            "stabilize_baseline": _workspace_relative_path(analyzer.study_dirs["stabilize_baseline"]),
            "stabilize_diagnostic": _workspace_relative_path(analyzer.study_dirs["stabilize_diagnostic"]),
            "guided_nogps_baseline": _workspace_relative_path(analyzer.study_dirs["guided_nogps_baseline"]),
            "guided_nogps_diagnostic": _workspace_relative_path(analyzer.study_dirs["guided_nogps_diagnostic"]),
        },
        "anchor_families": [
            {
                "family_id": family.family_id,
                "backend": family.backend,
                "mode_scope": family.mode_scope,
                "scenario_scope": family.scenario_scope,
                "combo": {
                    "x_schema": family.combo.x_schema,
                    "y_schema": family.combo.y_schema,
                    "model_name": family.combo.model_name,
                    "pooling_mode": family.combo.pooling_mode,
                },
                "baseline_study_key": family.baseline_study_key,
                "diagnostic_study_key": family.diagnostic_study_key,
            }
            for family in ANCHOR_FAMILIES
        ],
        "outputs": {
            "summary": _relative_output_path(outputs["summary_path"], outputs["base_dir"]),
            "px4_table": _relative_output_path(outputs["px4_table_path"], outputs["base_dir"]),
            "ardupilot_table": _relative_output_path(outputs["ardupilot_table_path"], outputs["base_dir"]),
        },
    }
    write_yaml(outputs["manifest_path"], manifest)
    return outputs["base_dir"]
