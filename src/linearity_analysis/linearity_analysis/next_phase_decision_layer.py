from __future__ import annotations

import csv
import math
import os
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from linearity_core.io import ensure_study_directories, read_rows_csv, read_yaml, write_json, write_rows_csv, write_yaml
from linearity_core.paths import STUDY_ARTIFACT_ROOT, WORKSPACE_ROOT

STUDY_NAME = "formal_v2_next_phase_decision_layer"
ANCHOR_DEEP_DIVE_SUFFIX = "_formal_v2_anchor_deep_dive"
IN_DEPTH_ANALYSIS_SUFFIX = "_formal_v2_in_depth_analysis"
A2_PAIR_TARGET_SUFFIX = "_ardupilot_a2_pair_target_readiness"
A1_TARGETED_REPRODUCTION_SUFFIX = "_px4_a1_roll_pitch_targeted_reproduction"
PRIMARY_CANDIDATE_ORDER = ("A2", "A1", "B1", "C1", "D1", "D2")
BOUNDARY_SOURCE_PRIORITY = {
    "ardupilot_partial_not_generalized_state_evolution": 0,
    "targeted_inconclusive_family": 1,
}
BUCKET_PRIORITY = {
    "primary_entry_ready": 0,
    "mechanism_rich_hard_mode": 1,
    "contrast_non_entry": 2,
    "boundary_or_pathology": 3,
}
READY_SIGNAL_PRIORITY = {
    "pair_target_ready": 0,
    "targeted_reproduction_ready": 1,
    "none": 2,
}
CONDITIONING_BAND_ORDER = {
    "low": 0,
    "medium": 1,
    "high": 2,
    "extreme": 3,
    "unknown": 4,
}
CONDITIONING_BANDS = (
    ("low", 1.0e2),
    ("medium", 1.0e5),
    ("high", 1.0e8),
)
PRIMARY_FIELDNAMES = [
    "candidate_id",
    "anchor_family",
    "backend",
    "combo",
    "structure_type",
    "support_status",
    "generalization_status",
    "explicit_ready_signal",
    "conditioning_band",
    "mask_state",
    "decision_bucket",
    "decision_score",
    "decision_priority",
    "recommended_role",
    "recommended_next_phase",
    "downgrade_reasons",
    "rationale",
    "evidence_sources",
]
ROUTING_FIELDNAMES = [
    "candidate_id",
    "decision_priority",
    "decision_bucket",
    "explicit_ready_signal",
    "recommended_role",
    "recommended_next_phase",
    "rationale",
    "downgrade_reasons",
    "evidence_sources",
]
BOUNDARY_FIELDNAMES = [
    "candidate_id",
    "structure_type",
    "support_status",
    "generalization_status",
    "conditioning_band",
    "mask_state",
    "failure_mechanism",
    "primary_driver",
    "downgrade_reasons",
    "rationale",
    "evidence_sources",
]
WATCHLIST_FIELDNAMES = [
    "backend",
    "combo",
    "structure_type",
    "conditioning_band",
    "command_share",
    "state_share",
    "baseline_top_edge_overlap_jaccard",
    "watch_reason",
    "evidence_sources",
]


@dataclass(frozen=True)
class SourceBundle:
    anchor_deep_dive_dir: Path
    in_depth_analysis_dir: Path
    a2_pair_target_dir: Path
    a1_targeted_reproduction_dir: Path


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def _safe_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def _read_required_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return read_yaml(path)


def _read_required_rows_csv(path: Path) -> list[dict[str, str]]:
    rows = read_rows_csv(path)
    if not rows:
        raise FileNotFoundError(path)
    return rows


def _workspace_relative_path(path: Path) -> str:
    absolute = path.expanduser().resolve()
    try:
        return str(absolute.relative_to(WORKSPACE_ROOT))
    except ValueError:
        return str(absolute)


def _absolute_path_string(path: Path | str) -> str:
    return str(Path(path).expanduser().resolve())


def _join_text(values: list[str]) -> str:
    return "; ".join(value for value in values if value)


def _output_paths(output_dir: Path | None) -> dict[str, Path]:
    if output_dir is None:
        study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_{STUDY_NAME}"
        paths = ensure_study_directories(study_id)
        base_dir = paths["base_dir"]
    else:
        base_dir = output_dir.expanduser().resolve()
        paths = ensure_study_directories(base_dir.name, root=base_dir.parent)
        if paths["base_dir"] != base_dir:
            raise ValueError(f"unexpected output directory resolution: {base_dir}")
    tables_dir = base_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    return {
        **paths,
        "tables_dir": tables_dir,
        "report_path": paths["reports_dir"] / "next_phase_decision_layer.md",
        "summary_path": paths["summary_dir"] / "next_phase_decision_layer.json",
        "candidate_board_path": tables_dir / "candidate_board.csv",
        "decision_routing_path": tables_dir / "decision_routing.csv",
        "boundary_catalog_path": tables_dir / "boundary_catalog.csv",
        "stable_core_watchlist_path": tables_dir / "stable_core_watchlist.csv",
    }


def _discover_latest_study(*, artifact_root: Path, suffix: str) -> Path:
    candidates = [path for path in artifact_root.iterdir() if path.is_dir() and path.name.endswith(suffix)]
    if not candidates:
        raise FileNotFoundError(f"missing study with suffix {suffix} under {artifact_root}")
    return sorted(candidates, key=lambda item: item.name, reverse=True)[0]


def _resolve_source_bundle(
    *,
    artifact_root: Path,
    anchor_deep_dive_dir: Path | None,
    in_depth_analysis_dir: Path | None,
    a2_pair_target_dir: Path | None,
    a1_targeted_reproduction_dir: Path | None,
) -> SourceBundle:
    return SourceBundle(
        anchor_deep_dive_dir=(anchor_deep_dive_dir or _discover_latest_study(artifact_root=artifact_root, suffix=ANCHOR_DEEP_DIVE_SUFFIX)).expanduser().resolve(),
        in_depth_analysis_dir=(in_depth_analysis_dir or _discover_latest_study(artifact_root=artifact_root, suffix=IN_DEPTH_ANALYSIS_SUFFIX)).expanduser().resolve(),
        a2_pair_target_dir=(a2_pair_target_dir or _discover_latest_study(artifact_root=artifact_root, suffix=A2_PAIR_TARGET_SUFFIX)).expanduser().resolve(),
        a1_targeted_reproduction_dir=(a1_targeted_reproduction_dir or _discover_latest_study(artifact_root=artifact_root, suffix=A1_TARGETED_REPRODUCTION_SUFFIX)).expanduser().resolve(),
    )


def _combine_status(baseline_value: str, diagnostic_value: str) -> str:
    baseline = str(baseline_value or "").strip()
    diagnostic = str(diagnostic_value or "").strip()
    if baseline == diagnostic:
        return baseline
    if baseline and diagnostic:
        return f"{baseline}_to_{diagnostic}"
    return baseline or diagnostic or "unknown"


def _conditioning_band(value: float) -> str:
    if not math.isfinite(value):
        return "unknown"
    for label, upper_bound in CONDITIONING_BANDS:
        if value < upper_bound:
            return label
    return "extreme"


def _generalization_score(value: str) -> int:
    return {
        "generalized_supported": 2,
        "supported_but_local": 1,
    }.get(str(value).strip(), 0)


def _mask_state_score(value: str) -> int:
    return {
        "stable_non_empty": 2,
        "partial_non_empty": 1,
        "empty": -2,
    }.get(str(value).strip(), 0)


def _conditioning_score(value: str) -> int:
    return {
        "low": 2,
        "medium": 1,
        "high": -1,
        "extreme": -2,
    }.get(str(value).strip(), 0)


def _structure_score(value: str) -> int:
    return {
        "direct_control": 2,
        "state_continuation": 1,
        "autoregressive_blocked": -1,
        "collapse_boundary": -2,
    }.get(str(value).strip(), 0)


def _active_feature_score(value: int) -> int:
    if value <= 2:
        return 1
    if value <= 5:
        return 0
    return -1


def _explicit_ready_signal(candidate_id: str, payload: dict[str, Any]) -> str:
    if candidate_id == "A2" and bool(payload.get("overall_decision", {}).get("ready_for_pair_attack_v1")):
        return "pair_target_ready"
    if candidate_id == "A1" and bool(payload.get("overall_decision", {}).get("ready_for_targeted_reproduction_v1")):
        return "targeted_reproduction_ready"
    return "none"


def _ready_signal_score(value: str) -> int:
    return {
        "pair_target_ready": 4,
        "targeted_reproduction_ready": 3,
    }.get(str(value).strip(), 0)


def _status_for_bucket(value: str) -> str:
    text = str(value).strip()
    return text if text in {"generalized_supported", "supported_but_local"} else "other"


def _mask_state_from_pair_rows(
    *,
    baseline_row: dict[str, Any],
    diagnostic_row: dict[str, Any],
    pair_jaccard_field: str,
) -> str:
    baseline_nnz = _safe_int(baseline_row.get("mask_nonzero_count"))
    diagnostic_nnz = _safe_int(diagnostic_row.get("mask_nonzero_count"))
    if baseline_nnz == 0 and diagnostic_nnz == 0:
        return "empty"
    pair_jaccard = _safe_float(baseline_row.get(pair_jaccard_field))
    if baseline_nnz > 0 and diagnostic_nnz > 0 and math.isfinite(pair_jaccard) and pair_jaccard >= 0.5:
        return "stable_non_empty"
    return "partial_non_empty"


def _px4_structure_type(
    *,
    baseline_row: dict[str, Any],
    targeted_payload: dict[str, Any] | None = None,
) -> str:
    command_share = _safe_float(baseline_row.get("abs_mass_command"))
    state_share = (
        _safe_float(baseline_row.get("abs_mass_state_current"))
        + _safe_float(baseline_row.get("abs_mass_state_lag_1"))
        + _safe_float(baseline_row.get("abs_mass_state_lag_2"))
        + _safe_float(baseline_row.get("abs_mass_state_lag_3"))
    )
    if math.isfinite(command_share) and math.isfinite(state_share) and command_share >= 0.8 and state_share <= 0.2:
        return "direct_control"
    if targeted_payload:
        response_rows = list(targeted_payload.get("response_results", []) or [])
        if response_rows:
            same_axis_share = sum(
                _safe_float(row.get("baseline_same_axis_share")) + _safe_float(row.get("diagnostic_same_axis_share"))
                for row in response_rows
            ) / (2.0 * len(response_rows))
            if math.isfinite(same_axis_share) and same_axis_share >= 0.5:
                return "state_continuation"
    if math.isfinite(state_share) and math.isfinite(command_share) and state_share > command_share:
        return "state_continuation"
    return "state_continuation"


def _ardupilot_structure_type(*, baseline_row: dict[str, Any], diagnostic_row: dict[str, Any]) -> str:
    command_share = _safe_float(baseline_row.get("abs_mass_command"))
    state_share = (
        _safe_float(baseline_row.get("abs_mass_state_current"))
        + _safe_float(baseline_row.get("abs_mass_state_lag_1"))
        + _safe_float(baseline_row.get("abs_mass_state_lag_2"))
        + _safe_float(baseline_row.get("abs_mass_state_lag_3"))
    )
    pair_raw_top4 = _safe_float(baseline_row.get("pair_raw_top4_jaccard"))
    mask_state = _mask_state_from_pair_rows(
        baseline_row=baseline_row,
        diagnostic_row=diagnostic_row,
        pair_jaccard_field="pair_mask_jaccard",
    )
    y_schema = str(baseline_row.get("y_schema", "")).strip()
    active_feature_count = max(
        _safe_int(baseline_row.get("active_feature_count")),
        _safe_int(diagnostic_row.get("active_feature_count")),
    )
    generalization_status = _combine_status(
        str(baseline_row.get("generalization_status", "")),
        str(diagnostic_row.get("generalization_status", "")),
    )
    if math.isfinite(command_share) and math.isfinite(state_share) and command_share >= 0.8 and state_share <= 0.2:
        return "direct_control"
    if y_schema == "actuator_response" and mask_state != "empty" and active_feature_count <= 2:
        return "direct_control"
    if mask_state == "empty" and math.isfinite(pair_raw_top4) and pair_raw_top4 <= 0.05:
        return "collapse_boundary"
    if "generalized_supported" not in generalization_status and math.isfinite(pair_raw_top4) and pair_raw_top4 >= 0.75:
        return "autoregressive_blocked"
    return "state_continuation"


def _bucket_for_candidate(
    *,
    candidate_id: str,
    structure_type: str,
    generalization_status: str,
    explicit_ready_signal: str,
    mask_state: str,
    conditioning_band: str,
) -> str:
    generalization_gate = _status_for_bucket(generalization_status)
    if explicit_ready_signal == "pair_target_ready":
        return "primary_entry_ready"
    if (
        generalization_gate == "generalized_supported"
        and structure_type == "direct_control"
        and mask_state == "stable_non_empty"
        and conditioning_band in {"low", "medium"}
    ):
        return "primary_entry_ready"
    if (
        generalization_gate == "generalized_supported"
        and explicit_ready_signal == "targeted_reproduction_ready"
        and structure_type == "state_continuation"
    ):
        return "mechanism_rich_hard_mode"
    if candidate_id == "B1" or generalization_gate == "supported_but_local":
        return "contrast_non_entry"
    return "boundary_or_pathology"


def _score_candidate(
    *,
    explicit_ready_signal: str,
    generalization_status: str,
    mask_state: str,
    conditioning_band: str,
    structure_type: str,
    active_feature_count: int,
    stable_raw_blocked: bool,
    raw_collapse: bool,
) -> int:
    score = 0
    score += _ready_signal_score(explicit_ready_signal)
    score += _generalization_score(_status_for_bucket(generalization_status))
    score += _mask_state_score(mask_state)
    score += _conditioning_score(conditioning_band)
    score += _structure_score(structure_type)
    score += _active_feature_score(active_feature_count)
    if stable_raw_blocked:
        score -= 1
    if raw_collapse:
        score -= 2
    return score


def _recommended_role(candidate_id: str, bucket: str) -> str:
    if candidate_id == "A2":
        return "default_entry_candidate"
    if candidate_id == "A1":
        return "hard_mode_backup_line"
    if bucket == "contrast_non_entry":
        return "contrast_only_candidate"
    if candidate_id == "D1":
        return "failure_boundary_exemplar"
    return "boundary_explainer"


def _recommended_next_phase(candidate_id: str, bucket: str) -> str:
    if candidate_id == "A2":
        return "design_a2_pair_target_algorithm"
    if candidate_id == "A1":
        return "keep_as_targeted_reproduction_backup"
    if bucket == "contrast_non_entry":
        return "use_for_mainline_exclusion_and_scenario_contrast"
    if candidate_id == "D1":
        return "retain_as_diagnostic_collapse_boundary_only"
    return "retain_as_boundary_evidence_only"


def _relative_sort_key(candidate: dict[str, Any]) -> tuple[int, int, int, int, str]:
    return (
        BUCKET_PRIORITY.get(str(candidate.get("decision_bucket")), 99),
        -_safe_int(candidate.get("decision_score")),
        READY_SIGNAL_PRIORITY.get(str(candidate.get("explicit_ready_signal")), 99),
        CONDITIONING_BAND_ORDER.get(str(candidate.get("conditioning_band")), 99),
        _safe_int(candidate.get("active_feature_count")),
        str(candidate.get("candidate_id")),
    )


def _csv_row_from_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": candidate["candidate_id"],
        "anchor_family": candidate["anchor_family"],
        "backend": candidate["backend"],
        "combo": candidate["combo"],
        "structure_type": candidate["structure_type"],
        "support_status": candidate["support_status"],
        "generalization_status": candidate["generalization_status"],
        "explicit_ready_signal": candidate["explicit_ready_signal"],
        "conditioning_band": candidate["conditioning_band"],
        "mask_state": candidate["mask_state"],
        "decision_bucket": candidate["decision_bucket"],
        "decision_score": candidate["decision_score"],
        "decision_priority": candidate["decision_priority"],
        "recommended_role": candidate["recommended_role"],
        "recommended_next_phase": candidate["recommended_next_phase"],
        "downgrade_reasons": _join_text(list(candidate["downgrade_reasons"])),
        "rationale": candidate["rationale"],
        "evidence_sources": _join_text(list(candidate["evidence_sources"])),
    }


def _routing_row(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": candidate["candidate_id"],
        "decision_priority": candidate["decision_priority"],
        "decision_bucket": candidate["decision_bucket"],
        "explicit_ready_signal": candidate["explicit_ready_signal"],
        "recommended_role": candidate["recommended_role"],
        "recommended_next_phase": candidate["recommended_next_phase"],
        "rationale": candidate["rationale"],
        "downgrade_reasons": _join_text(list(candidate["downgrade_reasons"])),
        "evidence_sources": _join_text(list(candidate["evidence_sources"])),
    }


def _boundary_row(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": candidate["candidate_id"],
        "structure_type": candidate["structure_type"],
        "support_status": candidate["support_status"],
        "generalization_status": candidate["generalization_status"],
        "conditioning_band": candidate["conditioning_band"],
        "mask_state": candidate["mask_state"],
        "failure_mechanism": candidate["failure_mechanism"],
        "primary_driver": candidate["primary_driver"],
        "downgrade_reasons": _join_text(list(candidate["downgrade_reasons"])),
        "rationale": candidate["rationale"],
        "evidence_sources": _join_text(list(candidate["evidence_sources"])),
    }


def _watchlist_row(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "backend": entry["backend"],
        "combo": entry["combo"],
        "structure_type": entry["structure_type"],
        "conditioning_band": entry["conditioning_band"],
        "command_share": entry["command_share"],
        "state_share": entry["state_share"],
        "baseline_top_edge_overlap_jaccard": entry["baseline_top_edge_overlap_jaccard"],
        "watch_reason": entry["watch_reason"],
        "evidence_sources": _join_text(list(entry["evidence_sources"])),
    }


def render_next_phase_decision_layer_markdown(payload: dict[str, Any]) -> str:
    overall = payload["overall_recommendation"]
    lines = [
        "# Formal V2 Next-Phase Decision Layer",
        "",
        "## Overall Recommendation",
        "",
        f"- default_entry: {overall['default_entry']}",
        f"- hard_mode: {overall['hard_mode']}",
        f"- contrast_only: {overall['contrast_only']}",
        f"- boundary_candidates: {', '.join(overall['boundary_candidates'])}",
        f"- recommendation: {overall['recommendation']}",
        "",
        "## Candidate Board",
        "",
        "| priority | candidate | bucket | score | signal | structure | role |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in payload["candidate_board"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["decision_priority"]),
                    row["candidate_id"],
                    row["decision_bucket"],
                    str(row["decision_score"]),
                    row["explicit_ready_signal"],
                    row["structure_type"],
                    row["recommended_role"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Why A2 Is The Default Entry",
            "",
            f"- {payload['candidate_lookup']['A2']['rationale']}",
            f"- evidence_sources: {_join_text(payload['candidate_lookup']['A2']['evidence_sources'])}",
            "",
            "## Why A1 Is Hard Mode, Not Baseline",
            "",
            f"- {payload['candidate_lookup']['A1']['rationale']}",
            f"- downgrade_reasons: {_join_text(payload['candidate_lookup']['A1']['downgrade_reasons']) or 'none'}",
            "",
            "## Why B1/C1/D1/D2 Are Not Mainline Entries",
            "",
        ]
    )
    for candidate_id in ("B1", "C1", "D1", "D2"):
        candidate = payload["candidate_lookup"][candidate_id]
        lines.append(
            f"- {candidate_id}: {candidate['rationale']} | downgrade_reasons={_join_text(candidate['downgrade_reasons']) or 'none'}"
        )
    lines.extend(
        [
            "",
            "## Residual Unknowns And Evidence Boundary",
            "",
        ]
    )
    for item in payload["residual_unknowns"]:
        lines.append(f"- {item}")
    return "\n".join(lines).rstrip() + "\n"


class NextPhaseDecisionAnalyzer:
    def __init__(
        self,
        *,
        anchor_deep_dive_dir: Path | None = None,
        in_depth_analysis_dir: Path | None = None,
        a2_pair_target_dir: Path | None = None,
        a1_targeted_reproduction_dir: Path | None = None,
        artifact_root: Path = STUDY_ARTIFACT_ROOT,
    ) -> None:
        self.artifact_root = artifact_root.expanduser().resolve()
        self.sources = _resolve_source_bundle(
            artifact_root=self.artifact_root,
            anchor_deep_dive_dir=anchor_deep_dive_dir,
            in_depth_analysis_dir=in_depth_analysis_dir,
            a2_pair_target_dir=a2_pair_target_dir,
            a1_targeted_reproduction_dir=a1_targeted_reproduction_dir,
        )
        self._anchor_summary = _read_required_yaml(self.sources.anchor_deep_dive_dir / "summary" / "anchor_deep_dive.json")
        self._px4_anchor_rows = _read_required_rows_csv(
            self.sources.anchor_deep_dive_dir / "tables" / "px4_a1_b1_matrix_comparison.csv"
        )
        self._ardupilot_anchor_rows = _read_required_rows_csv(
            self.sources.anchor_deep_dive_dir / "tables" / "ardupilot_a2_c1_d1_d2_boundary.csv"
        )
        self._in_depth_summary = _read_required_yaml(
            self.sources.in_depth_analysis_dir / "summary" / "in_depth_analysis.json"
        )
        self._stable_core_rows = _read_required_rows_csv(
            self.sources.in_depth_analysis_dir / "tables" / "stable_core_matrix_readout.csv"
        )
        self._conditioning_rows = _read_required_rows_csv(
            self.sources.in_depth_analysis_dir / "tables" / "ardupilot_conditioning_failure.csv"
        )
        self._stability_boundary_rows = _read_required_rows_csv(
            self.sources.in_depth_analysis_dir / "tables" / "stability_boundary.csv"
        )
        self._a2_pair_summary = _read_required_yaml(
            self.sources.a2_pair_target_dir / "summary" / "a2_pair_target_readiness.json"
        )
        self._a1_targeted_reproduction_summary = _read_required_yaml(
            self.sources.a1_targeted_reproduction_dir / "summary" / "a1_roll_pitch_targeted_reproduction.json"
        )

    def _pair_rows_by_anchor(self, rows: list[dict[str, str]], anchor_id: str) -> tuple[dict[str, str], dict[str, str]]:
        baseline = next((row for row in rows if row.get("anchor_id") == f"{anchor_id}_baseline"), None)
        diagnostic = next((row for row in rows if row.get("anchor_id") == f"{anchor_id}_diagnostic"), None)
        if baseline is None or diagnostic is None:
            raise ValueError(f"missing baseline/diagnostic rows for {anchor_id}")
        return baseline, diagnostic

    def _pair_rows_by_family(self, family_id: str) -> tuple[dict[str, str], dict[str, str]]:
        baseline = next(
            (
                row
                for row in self._ardupilot_anchor_rows
                if row.get("family_id") == family_id and row.get("study_phase") == "baseline"
            ),
            None,
        )
        diagnostic = next(
            (
                row
                for row in self._ardupilot_anchor_rows
                if row.get("family_id") == family_id and row.get("study_phase") == "diagnostic"
            ),
            None,
        )
        if baseline is None or diagnostic is None:
            raise ValueError(f"missing baseline/diagnostic rows for {family_id}")
        return baseline, diagnostic

    def _conditioning_row(self, failure_path: str) -> dict[str, str]:
        row = next((item for item in self._conditioning_rows if item.get("failure_path") == failure_path), None)
        if row is None:
            raise ValueError(f"missing conditioning failure row for {failure_path}")
        return row

    def _boundary_rows_for_candidate(self, candidate_id: str) -> list[dict[str, str]]:
        if candidate_id == "B1":
            candidates = [row for row in self._stability_boundary_rows if row.get("source_category") == "supported_but_local"]
        elif candidate_id == "C1":
            candidates = [
                row
                for row in self._stability_boundary_rows
                if row.get("source_category") == "ardupilot_partial_not_generalized_state_evolution"
            ]
        elif candidate_id == "D1":
            candidates = [
                row
                for row in self._stability_boundary_rows
                if row.get("source_category") == "targeted_inconclusive_family"
                and "stabilize" in str(row.get("comparison_generalization_status", "")).lower()
            ]
        elif candidate_id == "D2":
            candidates = [
                row
                for row in self._stability_boundary_rows
                if row.get("source_category") == "targeted_inconclusive_family"
                and "guided_nogps" in str(row.get("comparison_generalization_status", "")).lower()
            ]
        else:
            return []
        return sorted(
            candidates,
            key=lambda row: (
                BOUNDARY_SOURCE_PRIORITY.get(str(row.get("source_category")), 99),
                str(row.get("study_dir", "")),
            ),
        )

    def _primary_driver_for_candidate(self, candidate_id: str) -> str:
        rows = self._boundary_rows_for_candidate(candidate_id)
        if not rows:
            return "none"
        counts = Counter(str(row.get("primary_driver", "none")) for row in rows)
        return counts.most_common(1)[0][0]

    def _base_candidate(
        self,
        *,
        candidate_id: str,
        backend: str,
        combo: str,
        support_status: str,
        generalization_status: str,
        explicit_ready_signal: str,
        conditioning_band: str,
        mask_state: str,
        structure_type: str,
        active_feature_count: int,
        stable_raw_blocked: bool,
        raw_collapse: bool,
        downgrade_reasons: list[str],
        rationale: str,
        evidence_sources: list[str],
        failure_mechanism: str = "not_applicable",
        primary_driver: str = "none",
    ) -> dict[str, Any]:
        bucket = _bucket_for_candidate(
            candidate_id=candidate_id,
            structure_type=structure_type,
            generalization_status=generalization_status,
            explicit_ready_signal=explicit_ready_signal,
            mask_state=mask_state,
            conditioning_band=conditioning_band,
        )
        score = _score_candidate(
            explicit_ready_signal=explicit_ready_signal,
            generalization_status=generalization_status,
            mask_state=mask_state,
            conditioning_band=conditioning_band,
            structure_type=structure_type,
            active_feature_count=active_feature_count,
            stable_raw_blocked=stable_raw_blocked,
            raw_collapse=raw_collapse,
        )
        return {
            "candidate_id": candidate_id,
            "anchor_family": candidate_id,
            "backend": backend,
            "combo": combo,
            "structure_type": structure_type,
            "support_status": support_status,
            "generalization_status": generalization_status,
            "explicit_ready_signal": explicit_ready_signal,
            "conditioning_band": conditioning_band,
            "mask_state": mask_state,
            "decision_bucket": bucket,
            "decision_score": score,
            "decision_priority": 0,
            "recommended_role": _recommended_role(candidate_id, bucket),
            "recommended_next_phase": _recommended_next_phase(candidate_id, bucket),
            "downgrade_reasons": downgrade_reasons,
            "rationale": rationale,
            "evidence_sources": evidence_sources,
            "active_feature_count": active_feature_count,
            "stable_raw_blocked": stable_raw_blocked,
            "raw_collapse": raw_collapse,
            "failure_mechanism": failure_mechanism,
            "primary_driver": primary_driver,
        }

    def _build_a2_candidate(self) -> dict[str, Any]:
        baseline, diagnostic = self._pair_rows_by_family("A2")
        generalization_status = _combine_status(
            str(baseline.get("generalization_status", "")),
            str(diagnostic.get("generalization_status", "")),
        )
        support_status = _combine_status(str(baseline.get("support", "")), str(diagnostic.get("support", "")))
        conditioning_band = _conditioning_band(
            max(
                _safe_float(baseline.get("x_effective_condition_number")),
                _safe_float(diagnostic.get("x_effective_condition_number")),
            )
        )
        mask_state = _mask_state_from_pair_rows(
            baseline_row=baseline,
            diagnostic_row=diagnostic,
            pair_jaccard_field="pair_mask_jaccard",
        )
        explicit_ready_signal = _explicit_ready_signal("A2", self._a2_pair_summary)
        evidence_sources = [
            _absolute_path_string(self.sources.anchor_deep_dive_dir / "tables" / "ardupilot_a2_c1_d1_d2_boundary.csv"),
            _absolute_path_string(self.sources.a2_pair_target_dir / "summary" / "a2_pair_target_readiness.json"),
            str(baseline.get("notes_source_matrix_path", "")),
            str(baseline.get("notes_source_mask_path", "")),
            str(baseline.get("notes_source_metrics_path", "")),
        ]
        return self._base_candidate(
            candidate_id="A2",
            backend="ardupilot",
            combo=" | ".join(
                [
                    str(baseline.get("x_schema", "")),
                    str(baseline.get("y_schema", "")),
                    str(baseline.get("model_name", "")),
                    str(baseline.get("pooling_mode", "")),
                ]
            ),
            support_status=support_status,
            generalization_status=generalization_status,
            explicit_ready_signal=explicit_ready_signal,
            conditioning_band=conditioning_band,
            mask_state=mask_state,
            structure_type=_ardupilot_structure_type(baseline_row=baseline, diagnostic_row=diagnostic),
            active_feature_count=max(
                _safe_int(baseline.get("active_feature_count")),
                _safe_int(diagnostic.get("active_feature_count")),
            ),
            stable_raw_blocked=False,
            raw_collapse=False,
            downgrade_reasons=[],
            rationale=(
                "A2 is the default entry because it is pair-target-ready, low-conditioning, "
                "stable_non_empty, and still dominated by a direct-control throttle-to-actuator path."
            ),
            evidence_sources=[item for item in evidence_sources if item],
        )

    def _build_a1_candidate(self) -> dict[str, Any]:
        baseline, diagnostic = self._pair_rows_by_anchor(self._px4_anchor_rows, "A1")
        generalization_status = _combine_status(
            str(baseline.get("generalization_status", "")),
            str(diagnostic.get("generalization_status", "")),
        )
        support_status = _combine_status(str(baseline.get("support", "")), str(diagnostic.get("support", "")))
        conditioning_band = _conditioning_band(
            max(
                _safe_float(baseline.get("x_effective_condition_number")),
                _safe_float(diagnostic.get("x_effective_condition_number")),
            )
        )
        mask_state = _mask_state_from_pair_rows(
            baseline_row=baseline,
            diagnostic_row=diagnostic,
            pair_jaccard_field="same_combo_mask_jaccard_to_pair",
        )
        explicit_ready_signal = _explicit_ready_signal("A1", self._a1_targeted_reproduction_summary)
        downgrade_reasons = [
            "state_continuation_not_direct_control",
            "requires_state_feedback_channel_assumption",
        ]
        evidence_sources = [
            _absolute_path_string(self.sources.anchor_deep_dive_dir / "tables" / "px4_a1_b1_matrix_comparison.csv"),
            _absolute_path_string(
                self.sources.a1_targeted_reproduction_dir / "summary" / "a1_roll_pitch_targeted_reproduction.json"
            ),
        ]
        return self._base_candidate(
            candidate_id="A1",
            backend="px4",
            combo=" | ".join(
                [
                    str(baseline.get("x_schema", "")),
                    str(baseline.get("y_schema", "")),
                    str(baseline.get("model_name", "")),
                    str(baseline.get("pooling_mode", "")),
                ]
            ),
            support_status=support_status,
            generalization_status=generalization_status,
            explicit_ready_signal=explicit_ready_signal,
            conditioning_band=conditioning_band,
            mask_state=mask_state,
            structure_type=_px4_structure_type(
                baseline_row=baseline,
                targeted_payload=self._a1_targeted_reproduction_summary,
            ),
            active_feature_count=max(
                _safe_int(baseline.get("active_feature_count")),
                _safe_int(diagnostic.get("active_feature_count")),
            ),
            stable_raw_blocked=False,
            raw_collapse=False,
            downgrade_reasons=downgrade_reasons,
            rationale=(
                "A1 is generalized-supported and targeted-reproduction-ready, but it stays in hard mode because "
                "the stable signal is a state-continuation path rather than a low-dimensional direct-control entry."
            ),
            evidence_sources=evidence_sources,
        )

    def _build_b1_candidate(self) -> dict[str, Any]:
        baseline, diagnostic = self._pair_rows_by_anchor(self._px4_anchor_rows, "B1")
        generalization_status = _combine_status(
            str(baseline.get("generalization_status", "")),
            str(diagnostic.get("generalization_status", "")),
        )
        support_status = _combine_status(str(baseline.get("support", "")), str(diagnostic.get("support", "")))
        conditioning_band = _conditioning_band(
            max(
                _safe_float(baseline.get("x_effective_condition_number")),
                _safe_float(diagnostic.get("x_effective_condition_number")),
            )
        )
        mask_state = _mask_state_from_pair_rows(
            baseline_row=baseline,
            diagnostic_row=diagnostic,
            pair_jaccard_field="same_combo_mask_jaccard_to_pair",
        )
        primary_driver = self._primary_driver_for_candidate("B1")
        evidence_sources = [
            _absolute_path_string(self.sources.anchor_deep_dive_dir / "tables" / "px4_a1_b1_matrix_comparison.csv"),
            _absolute_path_string(self.sources.in_depth_analysis_dir / "tables" / "stability_boundary.csv"),
        ]
        return self._base_candidate(
            candidate_id="B1",
            backend="px4",
            combo=" | ".join(
                [
                    str(baseline.get("x_schema", "")),
                    str(baseline.get("y_schema", "")),
                    str(baseline.get("model_name", "")),
                    str(baseline.get("pooling_mode", "")),
                ]
            ),
            support_status=support_status,
            generalization_status=generalization_status,
            explicit_ready_signal="none",
            conditioning_band=conditioning_band,
            mask_state=mask_state,
            structure_type=_px4_structure_type(baseline_row=baseline),
            active_feature_count=max(
                _safe_int(baseline.get("active_feature_count")),
                _safe_int(diagnostic.get("active_feature_count")),
            ),
            stable_raw_blocked=False,
            raw_collapse=False,
            downgrade_reasons=["supported_but_local_only", f"primary_driver={primary_driver}"],
            rationale=(
                "B1 remains a contrast-only candidate because its state-continuation template is local rather than "
                "scenario-stable, so it explains A1 but does not justify a mainline entry."
            ),
            evidence_sources=evidence_sources,
            failure_mechanism="local_only_without_cross_scenario_stability",
            primary_driver=primary_driver,
        )

    def _build_c1_candidate(self) -> dict[str, Any]:
        baseline, diagnostic = self._pair_rows_by_family("C1")
        conditioning_row = self._conditioning_row("mixed_mode_full")
        generalization_status = _combine_status(
            str(baseline.get("generalization_status", "")),
            str(diagnostic.get("generalization_status", "")),
        )
        support_status = _combine_status(str(baseline.get("support", "")), str(diagnostic.get("support", "")))
        conditioning_band = _conditioning_band(
            max(
                _safe_float(baseline.get("x_effective_condition_number")),
                _safe_float(diagnostic.get("x_effective_condition_number")),
            )
        )
        primary_driver = self._primary_driver_for_candidate("C1")
        evidence_sources = [
            _absolute_path_string(self.sources.anchor_deep_dive_dir / "tables" / "ardupilot_a2_c1_d1_d2_boundary.csv"),
            _absolute_path_string(self.sources.in_depth_analysis_dir / "tables" / "ardupilot_conditioning_failure.csv"),
            _absolute_path_string(self.sources.in_depth_analysis_dir / "tables" / "stability_boundary.csv"),
            str(conditioning_row.get("baseline_metrics_path", "")),
            str(conditioning_row.get("diagnostic_metrics_path", "")),
        ]
        return self._base_candidate(
            candidate_id="C1",
            backend="ardupilot",
            combo=" | ".join(
                [
                    str(baseline.get("x_schema", "")),
                    str(baseline.get("y_schema", "")),
                    str(baseline.get("model_name", "")),
                    str(baseline.get("pooling_mode", "")),
                ]
            ),
            support_status=support_status,
            generalization_status=generalization_status,
            explicit_ready_signal="none",
            conditioning_band=conditioning_band,
            mask_state=_mask_state_from_pair_rows(
                baseline_row=baseline,
                diagnostic_row=diagnostic,
                pair_jaccard_field="pair_mask_jaccard",
            ),
            structure_type="autoregressive_blocked",
            active_feature_count=max(
                _safe_int(baseline.get("active_feature_count")),
                _safe_int(diagnostic.get("active_feature_count")),
            ),
            stable_raw_blocked=True,
            raw_collapse=False,
            downgrade_reasons=["stable_partial_mask_only", "extreme_conditioning", f"primary_driver={primary_driver}"],
            rationale=(
                "C1 stays out of the mainline because it is a stable partial + extreme conditioning sample: "
                "the raw autoregressive template persists, but formal support never matures into an entry path."
            ),
            evidence_sources=[item for item in evidence_sources if item],
            failure_mechanism="stable_partial_mask_with_extreme_conditioning",
            primary_driver=primary_driver,
        )

    def _build_d1_candidate(self) -> dict[str, Any]:
        baseline, diagnostic = self._pair_rows_by_family("D1")
        conditioning_row = self._conditioning_row("stabilize_baseline_to_diagnostic_collapse")
        generalization_status = _combine_status(
            str(baseline.get("generalization_status", "")),
            str(diagnostic.get("generalization_status", "")),
        )
        support_status = _combine_status(str(baseline.get("support", "")), str(diagnostic.get("support", "")))
        conditioning_band = _conditioning_band(
            max(
                _safe_float(baseline.get("x_effective_condition_number")),
                _safe_float(diagnostic.get("x_effective_condition_number")),
            )
        )
        primary_driver = self._primary_driver_for_candidate("D1")
        evidence_sources = [
            _absolute_path_string(self.sources.anchor_deep_dive_dir / "tables" / "ardupilot_a2_c1_d1_d2_boundary.csv"),
            _absolute_path_string(self.sources.in_depth_analysis_dir / "tables" / "ardupilot_conditioning_failure.csv"),
            _absolute_path_string(self.sources.in_depth_analysis_dir / "tables" / "stability_boundary.csv"),
            str(conditioning_row.get("baseline_metrics_path", "")),
            str(conditioning_row.get("diagnostic_metrics_path", "")),
        ]
        return self._base_candidate(
            candidate_id="D1",
            backend="ardupilot",
            combo=" | ".join(
                [
                    str(baseline.get("x_schema", "")),
                    str(baseline.get("y_schema", "")),
                    str(baseline.get("model_name", "")),
                    str(baseline.get("pooling_mode", "")),
                ]
            ),
            support_status=support_status,
            generalization_status=generalization_status,
            explicit_ready_signal="none",
            conditioning_band=conditioning_band,
            mask_state=_mask_state_from_pair_rows(
                baseline_row=baseline,
                diagnostic_row=diagnostic,
                pair_jaccard_field="pair_mask_jaccard",
            ),
            structure_type="collapse_boundary",
            active_feature_count=max(
                _safe_int(baseline.get("active_feature_count")),
                _safe_int(diagnostic.get("active_feature_count")),
            ),
            stable_raw_blocked=False,
            raw_collapse=True,
            downgrade_reasons=["empty_mask", "diagnostic_raw_collapse", f"primary_driver={primary_driver}"],
            rationale=(
                "D1 is not a mainline entry because it is a diagnostic raw collapse boundary: the mask stays empty "
                "and the baseline support template does not survive the diagnostic phase."
            ),
            evidence_sources=[item for item in evidence_sources if item],
            failure_mechanism="empty_mask_with_raw_collapse",
            primary_driver=primary_driver,
        )

    def _build_d2_candidate(self) -> dict[str, Any]:
        baseline, diagnostic = self._pair_rows_by_family("D2")
        conditioning_row = self._conditioning_row("guided_nogps_persistent_high_r2_high_cond")
        generalization_status = _combine_status(
            str(baseline.get("generalization_status", "")),
            str(diagnostic.get("generalization_status", "")),
        )
        support_status = _combine_status(str(baseline.get("support", "")), str(diagnostic.get("support", "")))
        conditioning_band = _conditioning_band(
            max(
                _safe_float(baseline.get("x_effective_condition_number")),
                _safe_float(diagnostic.get("x_effective_condition_number")),
            )
        )
        primary_driver = self._primary_driver_for_candidate("D2")
        evidence_sources = [
            _absolute_path_string(self.sources.anchor_deep_dive_dir / "tables" / "ardupilot_a2_c1_d1_d2_boundary.csv"),
            _absolute_path_string(self.sources.in_depth_analysis_dir / "tables" / "ardupilot_conditioning_failure.csv"),
            _absolute_path_string(self.sources.in_depth_analysis_dir / "tables" / "stability_boundary.csv"),
            str(conditioning_row.get("baseline_metrics_path", "")),
            str(conditioning_row.get("diagnostic_metrics_path", "")),
        ]
        return self._base_candidate(
            candidate_id="D2",
            backend="ardupilot",
            combo=" | ".join(
                [
                    str(baseline.get("x_schema", "")),
                    str(baseline.get("y_schema", "")),
                    str(baseline.get("model_name", "")),
                    str(baseline.get("pooling_mode", "")),
                ]
            ),
            support_status=support_status,
            generalization_status=generalization_status,
            explicit_ready_signal="none",
            conditioning_band=conditioning_band,
            mask_state=_mask_state_from_pair_rows(
                baseline_row=baseline,
                diagnostic_row=diagnostic,
                pair_jaccard_field="pair_mask_jaccard",
            ),
            structure_type="autoregressive_blocked",
            active_feature_count=max(
                _safe_int(baseline.get("active_feature_count")),
                _safe_int(diagnostic.get("active_feature_count")),
            ),
            stable_raw_blocked=True,
            raw_collapse=False,
            downgrade_reasons=["empty_mask", "stable_raw_template_but_formally_blocked", f"primary_driver={primary_driver}"],
            rationale=(
                "D2 is not a mainline entry because it is a stable raw template + empty mask sample under "
                "extreme conditioning, which keeps the structure as boundary evidence rather than a usable entry."
            ),
            evidence_sources=[item for item in evidence_sources if item],
            failure_mechanism="stable_raw_template_with_empty_mask",
            primary_driver=primary_driver,
        )

    def build_primary_candidates(self) -> list[dict[str, Any]]:
        candidates = [
            self._build_a2_candidate(),
            self._build_a1_candidate(),
            self._build_b1_candidate(),
            self._build_c1_candidate(),
            self._build_d1_candidate(),
            self._build_d2_candidate(),
        ]
        unique = {candidate["candidate_id"]: candidate for candidate in candidates}
        if tuple(unique.keys()) != PRIMARY_CANDIDATE_ORDER:
            candidates = [unique[candidate_id] for candidate_id in PRIMARY_CANDIDATE_ORDER]
        else:
            candidates = list(unique.values())
        ordered = sorted(candidates, key=_relative_sort_key)
        for index, candidate in enumerate(ordered, start=1):
            candidate["decision_priority"] = index
        return ordered

    def build_stable_core_watchlist(self) -> list[dict[str, Any]]:
        excluded = {
            self._a1_targeted_reproduction_summary["study_scope"]["combo"],
            "commands_only | actuator_response | ridge_affine | pooled",
        }
        watchlist: list[dict[str, Any]] = []
        for row in self._stable_core_rows:
            combo = str(row.get("combo", "")).strip()
            if not combo or combo in excluded:
                continue
            command_share = _safe_float(row.get("command_share"))
            state_share = (
                _safe_float(row.get("state_current_share"))
                + _safe_float(row.get("state_lag_1_share"))
                + _safe_float(row.get("state_lag_2_share"))
                + _safe_float(row.get("state_lag_3_share"))
            )
            structure_type = "direct_control" if math.isfinite(command_share) and command_share >= 0.8 else "state_continuation"
            conditioning_band = _conditioning_band(
                max(
                    _safe_float(row.get("baseline_effective_condition_number")),
                    _safe_float(row.get("diagnostic_effective_condition_number")),
                )
            )
            watchlist.append(
                {
                    "backend": str(row.get("backend", "")),
                    "combo": combo,
                    "structure_type": structure_type,
                    "conditioning_band": conditioning_band,
                    "command_share": command_share,
                    "state_share": state_share,
                    "baseline_top_edge_overlap_jaccard": _safe_float(row.get("baseline_top_edge_overlap_jaccard")),
                    "watch_reason": (
                        "generalized_supported peer outside the primary anchor board; keep as corroborating structure only"
                    ),
                    "evidence_sources": [
                        _absolute_path_string(self.sources.in_depth_analysis_dir / "tables" / "stable_core_matrix_readout.csv"),
                        str(row.get("baseline_matrix_path", "")),
                        str(row.get("diagnostic_matrix_path", "")),
                    ],
                }
            )
        return sorted(
            watchlist,
            key=lambda item: (
                item["backend"],
                CONDITIONING_BAND_ORDER.get(str(item["conditioning_band"]), 99),
                str(item["combo"]),
            ),
        )

    def build_payload(self) -> dict[str, Any]:
        candidate_board = self.build_primary_candidates()
        boundary_catalog = [_boundary_row(candidate) for candidate in candidate_board if candidate["decision_bucket"] == "boundary_or_pathology"]
        stable_core_watchlist = [_watchlist_row(entry) for entry in self.build_stable_core_watchlist()]
        decision_routing = [_routing_row(candidate) for candidate in candidate_board]
        candidate_lookup = {candidate["candidate_id"]: candidate for candidate in candidate_board}
        payload = {
            "source_studies": {
                "anchor_deep_dive_dir": _absolute_path_string(self.sources.anchor_deep_dive_dir),
                "in_depth_analysis_dir": _absolute_path_string(self.sources.in_depth_analysis_dir),
                "a2_pair_target_dir": _absolute_path_string(self.sources.a2_pair_target_dir),
                "a1_targeted_reproduction_dir": _absolute_path_string(self.sources.a1_targeted_reproduction_dir),
            },
            "overall_recommendation": {
                "default_entry": "A2",
                "hard_mode": "A1",
                "contrast_only": "B1",
                "boundary_candidates": ["C1", "D1", "D2"],
                "recommendation": (
                    "Use A2 as the next-phase default entry, retain A1 as a hard-mode contrast/backup line, "
                    "and keep B1/C1/D1/D2 as explanatory non-entry candidates."
                ),
            },
            "candidate_board": candidate_board,
            "candidate_lookup": candidate_lookup,
            "decision_routing": decision_routing,
            "boundary_catalog": boundary_catalog,
            "stable_core_watchlist": stable_core_watchlist,
            "residual_unknowns": [
                "PX4 A1 still depends on a realistic state/feedback perturbation channel; the current artifact only shows reproducible continuation structure.",
                "ArduPilot state-evolution remains inconclusive; C1 and D2 are boundary evidence, not mature entry paths.",
                "D1 shows that targeted baseline positives can collapse under diagnostic widening, so localized success should not be promoted to a mainline entry.",
            ],
        }
        return payload


def run_formal_v2_next_phase_decision_layer(
    *,
    anchor_deep_dive_dir: Path | None = None,
    in_depth_analysis_dir: Path | None = None,
    a2_pair_target_dir: Path | None = None,
    a1_targeted_reproduction_dir: Path | None = None,
    output_dir: Path | None = None,
    artifact_root: Path = STUDY_ARTIFACT_ROOT,
) -> Path:
    analyzer = NextPhaseDecisionAnalyzer(
        anchor_deep_dive_dir=anchor_deep_dive_dir,
        in_depth_analysis_dir=in_depth_analysis_dir,
        a2_pair_target_dir=a2_pair_target_dir,
        a1_targeted_reproduction_dir=a1_targeted_reproduction_dir,
        artifact_root=artifact_root,
    )
    payload = analyzer.build_payload()
    outputs = _output_paths(output_dir)
    candidate_rows = [_csv_row_from_candidate(row) for row in payload["candidate_board"]]
    outputs["report_path"].write_text(render_next_phase_decision_layer_markdown(payload), encoding="utf-8")
    write_json(outputs["summary_path"], payload)
    write_rows_csv(outputs["candidate_board_path"], candidate_rows, fieldnames=PRIMARY_FIELDNAMES)
    write_rows_csv(outputs["decision_routing_path"], payload["decision_routing"], fieldnames=ROUTING_FIELDNAMES)
    write_rows_csv(outputs["boundary_catalog_path"], payload["boundary_catalog"], fieldnames=BOUNDARY_FIELDNAMES)
    write_rows_csv(outputs["stable_core_watchlist_path"], payload["stable_core_watchlist"], fieldnames=WATCHLIST_FIELDNAMES)
    write_yaml(
        outputs["manifest_path"],
        {
            "study_name": STUDY_NAME,
            "study_id": outputs["base_dir"].name,
            "source_studies": payload["source_studies"],
            "output_files": {
                "report": _workspace_relative_path(outputs["report_path"]),
                "summary": _workspace_relative_path(outputs["summary_path"]),
                "candidate_board": _workspace_relative_path(outputs["candidate_board_path"]),
                "decision_routing": _workspace_relative_path(outputs["decision_routing_path"]),
                "boundary_catalog": _workspace_relative_path(outputs["boundary_catalog_path"]),
                "stable_core_watchlist": _workspace_relative_path(outputs["stable_core_watchlist_path"]),
            },
            "summary": {
                "default_entry": payload["overall_recommendation"]["default_entry"],
                "hard_mode": payload["overall_recommendation"]["hard_mode"],
                "candidate_count": len(payload["candidate_board"]),
            },
        },
    )
    return outputs["base_dir"]
