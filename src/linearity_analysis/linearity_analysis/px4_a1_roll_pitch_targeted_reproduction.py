from __future__ import annotations

import argparse
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from linearity_core.io import ensure_study_directories, write_json, write_rows_csv, write_yaml

from .matrix_gallery import MatrixData
from .px4_a1_target_scout import (
    DEFAULT_BASELINE_STUDY,
    DEFAULT_DIAGNOSTIC_STUDY,
    _feature_base,
    _format_metric,
    _load_a1_generalization_entry,
    _load_a1_matrix,
    _prefer_workspace_study_path,
    _relative_workspace_path,
    _topk_features,
)

STUDY_NAME = "px4_a1_roll_pitch_targeted_reproduction"
TARGET_RESPONSES = ("future_state_roll", "future_state_pitch")
SCENARIO_CONSISTENCY_MIN = 0.95
SCENARIO_R2_MIN = 0.95
BASELINE_SAME_AXIS_SHARE_MIN = 0.55
DIAGNOSTIC_SAME_AXIS_SHARE_MIN = 0.65
BASELINE_DIRECT_SHARE_MIN = 0.30
DIAGNOSTIC_DIRECT_SHARE_MIN = 0.35
BASELINE_LAG_SHARE_MIN = 0.25
DIAGNOSTIC_LAG_SHARE_MIN = 0.30
COMMAND_SHARE_MAX = 0.15
CROSS_AXIS_SHARE_MAX = 0.05
TOP5_SAME_AXIS_COUNT_MIN = 3
TOPK_FEATURE_COUNT = 10

RESPONSE_FIELDNAMES = [
    "response_name",
    "target_axis",
    "baseline_top1_feature",
    "baseline_top1_value",
    "diagnostic_top1_feature",
    "diagnostic_top1_value",
    "baseline_direct_share",
    "diagnostic_direct_share",
    "baseline_lag_share",
    "diagnostic_lag_share",
    "baseline_same_axis_share",
    "diagnostic_same_axis_share",
    "baseline_command_share",
    "diagnostic_command_share",
    "baseline_cross_axis_share",
    "diagnostic_cross_axis_share",
    "baseline_yaw_heading_share",
    "diagnostic_yaw_heading_share",
    "baseline_top5_same_axis_count",
    "diagnostic_top5_same_axis_count",
    "top1_stable",
    "top1_sign_match",
    "response_ready",
    "blocking_reasons",
    "baseline_top5_features",
    "diagnostic_top5_features",
]

TOP_FEATURE_FIELDNAMES = [
    "response_name",
    "phase",
    "rank",
    "feature_name",
    "coefficient",
    "abs_coefficient",
    "feature_group",
]


def _output_paths(output_root: Path | None) -> dict[str, Path]:
    study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S_%f}_{STUDY_NAME}"
    paths = ensure_study_directories(study_id, root=output_root)
    tables_dir = paths["base_dir"] / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    return {
        **paths,
        "tables_dir": tables_dir,
        "manifest_path": paths["base_dir"] / "manifest.yaml",
        "report_path": paths["reports_dir"] / "a1_roll_pitch_targeted_reproduction.md",
        "summary_path": paths["summary_dir"] / "a1_roll_pitch_targeted_reproduction.json",
        "response_table_path": tables_dir / "response_targeted_reproduction.csv",
        "top_feature_table_path": tables_dir / "top_feature_snapshot.csv",
    }


def _phase_metrics(entry: dict[str, Any]) -> dict[str, float]:
    subgroup = dict(entry.get("scenario_subgroup_r2", {}) or {})
    finite_values = [float(value) for value in subgroup.values() if math.isfinite(float(value))]
    return {
        "scenario_consistency": float(entry.get("scenario_consistency", math.nan)),
        "min_scenario_r2": float(min(finite_values)) if finite_values else math.nan,
    }


def _share_for_features(feature_names: list[str], values: np.ndarray, predicate: Any) -> float:
    total = float(np.sum(np.abs(values)))
    if not math.isfinite(total) or total <= 0.0:
        return math.nan
    selected = float(sum(abs(value) for name, value in zip(feature_names, values, strict=True) if predicate(name)))
    return selected / total


def _response_axis(response_name: str) -> str:
    return response_name.removeprefix("future_state_")


def _same_axis_features(axis: str) -> set[str]:
    return {axis, *(f"{axis}__lag_{lag}" for lag in range(1, 4))}


def _cross_axis_features(axis: str) -> set[str]:
    other_axis = "pitch" if axis == "roll" else "roll"
    return {other_axis, *(f"{other_axis}__lag_{lag}" for lag in range(1, 4))}


def _yaw_heading_features() -> set[str]:
    return {
        "yaw",
        "heading",
        *(f"yaw__lag_{lag}" for lag in range(1, 4)),
        *(f"heading__lag_{lag}" for lag in range(1, 4)),
    }


def _feature_group(axis: str, feature_name: str) -> str:
    other_axis = "pitch" if axis == "roll" else "roll"
    base = _feature_base(feature_name)
    if feature_name == axis:
        return "same_axis_direct"
    if feature_name in {f"{axis}__lag_{lag}" for lag in range(1, 4)}:
        return "same_axis_lag"
    if feature_name.startswith(f"command_{axis}"):
        return "same_axis_command"
    if feature_name == other_axis or feature_name in {f"{other_axis}__lag_{lag}" for lag in range(1, 4)}:
        return "cross_axis_state"
    if base in {"yaw", "heading"}:
        return "yaw_heading_state"
    if feature_name.startswith("command_"):
        return "other_command"
    if feature_name.startswith("mode_"):
        return "mode"
    return "other"


def _top_feature_rows(response_name: str, axis: str, phase: str, matrix: MatrixData) -> list[dict[str, Any]]:
    response_index = matrix.response_names.index(response_name)
    values = matrix.values[:, response_index]
    top_indices = np.argsort(np.abs(values))[::-1][:TOPK_FEATURE_COUNT]
    rows: list[dict[str, Any]] = []
    for rank, feature_index in enumerate(top_indices, start=1):
        feature_name = matrix.feature_names[int(feature_index)]
        coefficient = float(values[int(feature_index)])
        rows.append(
            {
                "response_name": response_name,
                "phase": phase,
                "rank": rank,
                "feature_name": feature_name,
                "coefficient": coefficient,
                "abs_coefficient": abs(coefficient),
                "feature_group": _feature_group(axis, feature_name),
            }
        )
    return rows


def _response_result(response_name: str, baseline: MatrixData, diagnostic: MatrixData) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    axis = _response_axis(response_name)
    same_axis_features = _same_axis_features(axis)
    cross_axis_features = _cross_axis_features(axis)
    yaw_heading_features = _yaw_heading_features()

    baseline_index = baseline.response_names.index(response_name)
    diagnostic_index = diagnostic.response_names.index(response_name)
    baseline_values = baseline.values[:, baseline_index]
    diagnostic_values = diagnostic.values[:, diagnostic_index]

    baseline_top_index = int(np.argmax(np.abs(baseline_values)))
    diagnostic_top_index = int(np.argmax(np.abs(diagnostic_values)))
    baseline_top1_feature = baseline.feature_names[baseline_top_index]
    diagnostic_top1_feature = diagnostic.feature_names[diagnostic_top_index]
    baseline_top1_value = float(baseline_values[baseline_top_index])
    diagnostic_top1_value = float(diagnostic_values[diagnostic_top_index])

    baseline_top5_features = _topk_features(baseline.feature_names, baseline_values)
    diagnostic_top5_features = _topk_features(diagnostic.feature_names, diagnostic_values)
    baseline_top5_same_axis_count = sum(1 for feature_name in baseline_top5_features if feature_name in same_axis_features)
    diagnostic_top5_same_axis_count = sum(1 for feature_name in diagnostic_top5_features if feature_name in same_axis_features)

    baseline_direct_share = _share_for_features(
        baseline.feature_names, baseline_values, lambda feature_name: feature_name == axis
    )
    diagnostic_direct_share = _share_for_features(
        diagnostic.feature_names, diagnostic_values, lambda feature_name: feature_name == axis
    )
    baseline_lag_share = _share_for_features(
        baseline.feature_names, baseline_values, lambda feature_name: feature_name in same_axis_features - {axis}
    )
    diagnostic_lag_share = _share_for_features(
        diagnostic.feature_names, diagnostic_values, lambda feature_name: feature_name in same_axis_features - {axis}
    )
    baseline_same_axis_share = _share_for_features(
        baseline.feature_names, baseline_values, lambda feature_name: feature_name in same_axis_features
    )
    diagnostic_same_axis_share = _share_for_features(
        diagnostic.feature_names, diagnostic_values, lambda feature_name: feature_name in same_axis_features
    )
    baseline_command_share = _share_for_features(
        baseline.feature_names, baseline_values, lambda feature_name: feature_name.startswith("command_")
    )
    diagnostic_command_share = _share_for_features(
        diagnostic.feature_names, diagnostic_values, lambda feature_name: feature_name.startswith("command_")
    )
    baseline_cross_axis_share = _share_for_features(
        baseline.feature_names, baseline_values, lambda feature_name: feature_name in cross_axis_features
    )
    diagnostic_cross_axis_share = _share_for_features(
        diagnostic.feature_names, diagnostic_values, lambda feature_name: feature_name in cross_axis_features
    )
    baseline_yaw_heading_share = _share_for_features(
        baseline.feature_names, baseline_values, lambda feature_name: feature_name in yaw_heading_features
    )
    diagnostic_yaw_heading_share = _share_for_features(
        diagnostic.feature_names, diagnostic_values, lambda feature_name: feature_name in yaw_heading_features
    )

    top1_stable = baseline_top1_feature == diagnostic_top1_feature
    top1_sign_match = top1_stable and math.copysign(1.0, baseline_top1_value) == math.copysign(1.0, diagnostic_top1_value)

    blocking_reasons: list[str] = []
    if baseline_top1_feature != axis:
        blocking_reasons.append("baseline_top1_not_axis_state")
    if diagnostic_top1_feature != axis:
        blocking_reasons.append("diagnostic_top1_not_axis_state")
    if not top1_stable:
        blocking_reasons.append("top1_feature_not_stable")
    if not top1_sign_match:
        blocking_reasons.append("top1_sign_not_stable")
    if not math.isfinite(baseline_direct_share) or baseline_direct_share < BASELINE_DIRECT_SHARE_MIN:
        blocking_reasons.append("baseline_direct_share_below_threshold")
    if not math.isfinite(diagnostic_direct_share) or diagnostic_direct_share < DIAGNOSTIC_DIRECT_SHARE_MIN:
        blocking_reasons.append("diagnostic_direct_share_below_threshold")
    if not math.isfinite(baseline_lag_share) or baseline_lag_share < BASELINE_LAG_SHARE_MIN:
        blocking_reasons.append("baseline_lag_share_below_threshold")
    if not math.isfinite(diagnostic_lag_share) or diagnostic_lag_share < DIAGNOSTIC_LAG_SHARE_MIN:
        blocking_reasons.append("diagnostic_lag_share_below_threshold")
    if not math.isfinite(baseline_same_axis_share) or baseline_same_axis_share < BASELINE_SAME_AXIS_SHARE_MIN:
        blocking_reasons.append("baseline_same_axis_share_below_threshold")
    if not math.isfinite(diagnostic_same_axis_share) or diagnostic_same_axis_share < DIAGNOSTIC_SAME_AXIS_SHARE_MIN:
        blocking_reasons.append("diagnostic_same_axis_share_below_threshold")
    if not math.isfinite(baseline_command_share) or baseline_command_share > COMMAND_SHARE_MAX:
        blocking_reasons.append("baseline_command_share_above_threshold")
    if not math.isfinite(diagnostic_command_share) or diagnostic_command_share > COMMAND_SHARE_MAX:
        blocking_reasons.append("diagnostic_command_share_above_threshold")
    if not math.isfinite(baseline_cross_axis_share) or baseline_cross_axis_share > CROSS_AXIS_SHARE_MAX:
        blocking_reasons.append("baseline_cross_axis_share_above_threshold")
    if not math.isfinite(diagnostic_cross_axis_share) or diagnostic_cross_axis_share > CROSS_AXIS_SHARE_MAX:
        blocking_reasons.append("diagnostic_cross_axis_share_above_threshold")
    if baseline_top5_same_axis_count < TOP5_SAME_AXIS_COUNT_MIN:
        blocking_reasons.append("baseline_top5_same_axis_count_below_threshold")
    if diagnostic_top5_same_axis_count < TOP5_SAME_AXIS_COUNT_MIN:
        blocking_reasons.append("diagnostic_top5_same_axis_count_below_threshold")

    result = {
        "response_name": response_name,
        "target_axis": axis,
        "baseline_top1_feature": baseline_top1_feature,
        "baseline_top1_value": baseline_top1_value,
        "diagnostic_top1_feature": diagnostic_top1_feature,
        "diagnostic_top1_value": diagnostic_top1_value,
        "baseline_direct_share": baseline_direct_share,
        "diagnostic_direct_share": diagnostic_direct_share,
        "baseline_lag_share": baseline_lag_share,
        "diagnostic_lag_share": diagnostic_lag_share,
        "baseline_same_axis_share": baseline_same_axis_share,
        "diagnostic_same_axis_share": diagnostic_same_axis_share,
        "baseline_command_share": baseline_command_share,
        "diagnostic_command_share": diagnostic_command_share,
        "baseline_cross_axis_share": baseline_cross_axis_share,
        "diagnostic_cross_axis_share": diagnostic_cross_axis_share,
        "baseline_yaw_heading_share": baseline_yaw_heading_share,
        "diagnostic_yaw_heading_share": diagnostic_yaw_heading_share,
        "baseline_top5_same_axis_count": baseline_top5_same_axis_count,
        "diagnostic_top5_same_axis_count": diagnostic_top5_same_axis_count,
        "top1_stable": top1_stable,
        "top1_sign_match": top1_sign_match,
        "response_ready": not blocking_reasons,
        "blocking_reasons": blocking_reasons,
        "baseline_top5_features": ",".join(baseline_top5_features),
        "diagnostic_top5_features": ",".join(diagnostic_top5_features),
    }
    top_feature_rows = _top_feature_rows(response_name, axis, "baseline", baseline) + _top_feature_rows(
        response_name, axis, "diagnostic", diagnostic
    )
    return result, top_feature_rows


def analyze_px4_a1_roll_pitch_targeted_reproduction(
    *,
    baseline_study: Path = DEFAULT_BASELINE_STUDY,
    diagnostic_study: Path = DEFAULT_DIAGNOSTIC_STUDY,
) -> dict[str, Any]:
    baseline_matrix = _load_a1_matrix(baseline_study)
    diagnostic_matrix = _load_a1_matrix(diagnostic_study)
    if baseline_matrix.feature_names != diagnostic_matrix.feature_names or baseline_matrix.response_names != diagnostic_matrix.response_names:
        raise ValueError("baseline and diagnostic A1 matrices must share the same axes")

    baseline_entry = _load_a1_generalization_entry(baseline_study)
    diagnostic_entry = _load_a1_generalization_entry(diagnostic_study)
    baseline_phase = _phase_metrics(baseline_entry)
    diagnostic_phase = _phase_metrics(diagnostic_entry)

    response_results: list[dict[str, Any]] = []
    top_feature_rows: list[dict[str, Any]] = []
    for response_name in TARGET_RESPONSES:
        if response_name not in baseline_matrix.response_names or response_name not in diagnostic_matrix.response_names:
            raise ValueError(f"target response missing from A1 matrices: {response_name}")
        response_result, response_top_rows = _response_result(response_name, baseline_matrix, diagnostic_matrix)
        response_results.append(response_result)
        top_feature_rows.extend(response_top_rows)

    blocking_reasons: list[str] = []
    if str(baseline_entry.get("generalization_status")) != "generalized_supported":
        blocking_reasons.append("baseline_combo_not_generalized_supported")
    if str(diagnostic_entry.get("generalization_status")) != "generalized_supported":
        blocking_reasons.append("diagnostic_combo_not_generalized_supported")
    if not math.isfinite(baseline_phase["scenario_consistency"]) or baseline_phase["scenario_consistency"] < SCENARIO_CONSISTENCY_MIN:
        blocking_reasons.append("baseline_scenario_consistency_below_threshold")
    if not math.isfinite(diagnostic_phase["scenario_consistency"]) or diagnostic_phase["scenario_consistency"] < SCENARIO_CONSISTENCY_MIN:
        blocking_reasons.append("diagnostic_scenario_consistency_below_threshold")
    if not math.isfinite(baseline_phase["min_scenario_r2"]) or baseline_phase["min_scenario_r2"] < SCENARIO_R2_MIN:
        blocking_reasons.append("baseline_min_scenario_r2_below_threshold")
    if not math.isfinite(diagnostic_phase["min_scenario_r2"]) or diagnostic_phase["min_scenario_r2"] < SCENARIO_R2_MIN:
        blocking_reasons.append("diagnostic_min_scenario_r2_below_threshold")
    for result in response_results:
        blocking_reasons.extend(result["blocking_reasons"])

    ready = not blocking_reasons
    overall_decision = {
        "selected_family": "attitude_roll_pitch_continuation",
        "selected_responses": list(TARGET_RESPONSES),
        "ready_for_targeted_reproduction_v1": ready,
        "recommended_path": "lock_px4_a1_roll_pitch_targeted_scope" if ready else "iterate_px4_a1_roll_pitch_selection_only",
    }
    study_scope = {
        "backend": "px4",
        "anchor_id": "A1",
        "combo": "full_augmented | next_raw_state | ols_affine | stratified",
        "family_id": "attitude_roll_pitch_continuation",
        "target_responses": list(TARGET_RESPONSES),
        "target_capture_scope": {
            "mode_family": "OFFBOARD_ATTITUDE",
            "axes": ["roll", "pitch"],
            "scenarios": ["nominal", "dynamic", "throttle_biased"],
        },
        "baseline_study": str(_prefer_workspace_study_path(baseline_study)),
        "diagnostic_study": str(_prefer_workspace_study_path(diagnostic_study)),
    }
    payload = {
        "study_scope": study_scope,
        "phase_generalization": {
            "baseline": baseline_entry,
            "diagnostic": diagnostic_entry,
        },
        "response_results": response_results,
        "overall_decision": overall_decision,
        "blocking_reasons": blocking_reasons,
    }
    return payload, top_feature_rows


def render_px4_a1_roll_pitch_targeted_reproduction_markdown(
    payload: dict[str, Any], top_feature_rows: list[dict[str, Any]]
) -> str:
    overall = payload["overall_decision"]
    baseline_phase = _phase_metrics(payload["phase_generalization"]["baseline"])
    diagnostic_phase = _phase_metrics(payload["phase_generalization"]["diagnostic"])
    lines = [
        "# PX4 A1 Roll/Pitch Targeted Reproduction",
        "",
        f"- selected_family: {overall['selected_family']}",
        f"- selected_responses: {', '.join(overall['selected_responses'])}",
        f"- ready_for_targeted_reproduction_v1: {'yes' if overall['ready_for_targeted_reproduction_v1'] else 'no'}",
        f"- recommended_path: {overall['recommended_path']}",
        f"- blocking_reasons: {', '.join(payload['blocking_reasons']) if payload['blocking_reasons'] else 'none'}",
        "",
        "## Phase Generalization",
        "",
        f"- baseline_scenario_consistency={_format_metric(baseline_phase['scenario_consistency'])}, "
        f"baseline_min_scenario_r2={_format_metric(baseline_phase['min_scenario_r2'])}",
        f"- diagnostic_scenario_consistency={_format_metric(diagnostic_phase['scenario_consistency'])}, "
        f"diagnostic_min_scenario_r2={_format_metric(diagnostic_phase['min_scenario_r2'])}",
        "",
        "## Responses",
        "",
    ]
    for result in payload["response_results"]:
        lines.append(
            f"- {result['response_name']}: "
            f"top1={result['baseline_top1_feature']}/{result['diagnostic_top1_feature']}, "
            f"direct={_format_metric(result['baseline_direct_share'])}/{_format_metric(result['diagnostic_direct_share'])}, "
            f"lag={_format_metric(result['baseline_lag_share'])}/{_format_metric(result['diagnostic_lag_share'])}, "
            f"same_axis={_format_metric(result['baseline_same_axis_share'])}/{_format_metric(result['diagnostic_same_axis_share'])}, "
            f"command={_format_metric(result['baseline_command_share'])}/{_format_metric(result['diagnostic_command_share'])}, "
            f"cross_axis={_format_metric(result['baseline_cross_axis_share'])}/{_format_metric(result['diagnostic_cross_axis_share'])}, "
            f"top5_same_axis={result['baseline_top5_same_axis_count']}/{result['diagnostic_top5_same_axis_count']}, "
            f"blocking={', '.join(result['blocking_reasons']) if result['blocking_reasons'] else 'none'}"
        )
    lines.extend(
        [
            "",
            "## Top Features",
            "",
        ]
    )
    for response_name in TARGET_RESPONSES:
        response_rows = [row for row in top_feature_rows if row["response_name"] == response_name]
        baseline_rows = [row for row in response_rows if row["phase"] == "baseline"][:5]
        diagnostic_rows = [row for row in response_rows if row["phase"] == "diagnostic"][:5]
        lines.append(f"- {response_name} baseline_top5: " + ", ".join(f"{row['feature_name']} ({_format_metric(row['coefficient'])})" for row in baseline_rows))
        lines.append(f"- {response_name} diagnostic_top5: " + ", ".join(f"{row['feature_name']} ({_format_metric(row['coefficient'])})" for row in diagnostic_rows))
    return "\n".join(lines).rstrip() + "\n"


def run_px4_a1_roll_pitch_targeted_reproduction(
    *,
    baseline_study: Path = DEFAULT_BASELINE_STUDY,
    diagnostic_study: Path = DEFAULT_DIAGNOSTIC_STUDY,
    output_root: Path | None = None,
) -> Path:
    payload, top_feature_rows = analyze_px4_a1_roll_pitch_targeted_reproduction(
        baseline_study=baseline_study,
        diagnostic_study=diagnostic_study,
    )
    response_rows = []
    for result in payload["response_results"]:
        row = dict(result)
        row["blocking_reasons"] = ",".join(result["blocking_reasons"])
        response_rows.append(row)
    paths = _output_paths(output_root.expanduser().resolve() if output_root else None)
    paths["report_path"].write_text(
        render_px4_a1_roll_pitch_targeted_reproduction_markdown(payload, top_feature_rows), encoding="utf-8"
    )
    write_json(paths["summary_path"], payload)
    write_rows_csv(paths["response_table_path"], response_rows, fieldnames=RESPONSE_FIELDNAMES)
    write_rows_csv(paths["top_feature_table_path"], top_feature_rows, fieldnames=TOP_FEATURE_FIELDNAMES)
    write_yaml(
        paths["manifest_path"],
        {
            "study_name": STUDY_NAME,
            "study_id": paths["base_dir"].name,
            "baseline_study": payload["study_scope"]["baseline_study"],
            "diagnostic_study": payload["study_scope"]["diagnostic_study"],
            "family_id": payload["study_scope"]["family_id"],
            "target_responses": payload["study_scope"]["target_responses"],
            "output_files": {
                "report": _relative_workspace_path(paths["report_path"]),
                "summary": _relative_workspace_path(paths["summary_path"]),
                "response_targeted_reproduction": _relative_workspace_path(paths["response_table_path"]),
                "top_feature_snapshot": _relative_workspace_path(paths["top_feature_table_path"]),
            },
            "summary": payload,
        },
    )
    return paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Assess PX4 A1 roll/pitch targeted reproduction from canonical fit artifacts.")
    parser.add_argument("--baseline-study", type=Path, default=DEFAULT_BASELINE_STUDY)
    parser.add_argument("--diagnostic-study", type=Path, default=DEFAULT_DIAGNOSTIC_STUDY)
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args(argv)

    study_dir = run_px4_a1_roll_pitch_targeted_reproduction(
        baseline_study=args.baseline_study,
        diagnostic_study=args.diagnostic_study,
        output_root=args.output_root,
    )
    print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
