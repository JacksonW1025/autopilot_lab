from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from linearity_core.io import ensure_study_directories, write_json, write_rows_csv, write_yaml
from linearity_core.paths import STUDY_ARTIFACT_ROOT, WORKSPACE_ROOT

from .matrix_gallery import MatrixData, load_matrix_csv

STUDY_NAME = "px4_a1_target_scout"
DEFAULT_BASELINE_STUDY = STUDY_ARTIFACT_ROOT / "20260410_224818_px4_real_generalization_ablation"
DEFAULT_DIAGNOSTIC_STUDY = STUDY_ARTIFACT_ROOT / "20260411_021910_px4_generalization_diagnostic_matrix"
A1_FIT_RELATIVE_PATH = Path("fits/full_augmented__next_raw_state__stratified/ols_affine/matrix_f.csv")
SAME_FAMILY_SHARE_MIN = 0.45
COMMAND_SHARE_MAX = 0.15
MODE_SHARE_MAX = 0.05
TOP1_STABILITY_MIN = 1.0
TOP1_SIGN_MATCH_MIN = 1.0
TOP5_JACCARD_MIN = 0.40

RESPONSE_LEVEL_FIELDNAMES = [
    "response_name",
    "family_id",
    "baseline_top1_feature",
    "baseline_top1_value",
    "diagnostic_top1_feature",
    "diagnostic_top1_value",
    "baseline_same_family_share",
    "diagnostic_same_family_share",
    "baseline_command_share",
    "diagnostic_command_share",
    "baseline_mode_share",
    "diagnostic_mode_share",
    "top1_stable",
    "top1_sign_match",
    "top5_jaccard",
    "baseline_top5_features",
    "diagnostic_top5_features",
]

FAMILY_MATRIX_FIELDNAMES = [
    "family_id",
    "response_count",
    "baseline_median_same_family_share",
    "diagnostic_median_same_family_share",
    "median_command_share",
    "median_mode_share",
    "top1_stability_rate",
    "top1_sign_match_rate",
    "median_top5_jaccard",
    "supported",
    "blocking_reasons",
]


@dataclass(frozen=True)
class FamilySpec:
    family_id: str
    responses: tuple[str, ...]


FAMILY_SPECS = (
    FamilySpec("attitude_roll_pitch_continuation", ("future_state_roll", "future_state_pitch")),
    FamilySpec("yaw_heading_continuation", ("future_state_yaw", "future_state_heading", "future_state_yaw_rate")),
    FamilySpec("horizontal_position_continuation", ("future_state_position_x", "future_state_position_y")),
    FamilySpec("vertical_dual_continuation", ("future_state_position_z", "future_state_altitude")),
    FamilySpec("horizontal_velocity_continuation", ("future_state_velocity_x", "future_state_velocity_y")),
)


def _prefer_workspace_study_path(path: Path) -> Path:
    candidate = path.expanduser()
    workspace_candidate = STUDY_ARTIFACT_ROOT / candidate.name
    return workspace_candidate if workspace_candidate.exists() else candidate


def _relative_workspace_path(path: Path) -> str:
    absolute = path.expanduser().resolve()
    try:
        return str(absolute.relative_to(WORKSPACE_ROOT))
    except ValueError:
        return str(absolute)


def _output_paths(output_root: Path | None) -> dict[str, Path]:
    study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S_%f}_{STUDY_NAME}"
    paths = ensure_study_directories(study_id, root=output_root)
    tables_dir = paths["base_dir"] / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    return {
        **paths,
        "tables_dir": tables_dir,
        "manifest_path": paths["base_dir"] / "manifest.yaml",
        "report_path": paths["reports_dir"] / "a1_target_scout.md",
        "summary_path": paths["summary_dir"] / "a1_target_scout.json",
        "response_table_path": tables_dir / "response_level_target_scout.csv",
        "family_matrix_path": tables_dir / "family_target_matrix.csv",
    }


def _load_a1_matrix(study_dir: Path) -> MatrixData:
    resolved = _prefer_workspace_study_path(study_dir)
    return load_matrix_csv(resolved / A1_FIT_RELATIVE_PATH)


def _load_a1_generalization_entry(study_dir: Path) -> dict[str, Any]:
    resolved = _prefer_workspace_study_path(study_dir)
    summary_path = resolved / "summary" / "scenario_generalization.json"
    if not summary_path.exists():
        raise FileNotFoundError(summary_path)
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    for entry in list(payload.get("entries", []) or []):
        if (
            str(entry.get("x_schema")) == "full_augmented"
            and str(entry.get("y_schema")) == "next_raw_state"
            and str(entry.get("pooling_mode")) == "stratified"
            and str(entry.get("model_name")) == "ols_affine"
        ):
            return entry
    raise ValueError(f"A1 combo entry missing in {summary_path}")


def _response_core(response_name: str) -> str:
    return response_name.removeprefix("future_state_")


def _feature_base(feature_name: str) -> str:
    for suffix in ("__lag_1", "__lag_2", "__lag_3"):
        if feature_name.endswith(suffix):
            return feature_name.removesuffix(suffix)
    return feature_name


def _response_family_candidates(response_name: str) -> set[str]:
    core = _response_core(response_name)
    aliases = {
        "yaw": {"yaw", "heading"},
        "heading": {"yaw", "heading"},
        "yaw_rate": {"yaw", "heading", "yaw_rate"},
        "position_z": {"position_z", "altitude"},
        "altitude": {"position_z", "altitude"},
        "velocity_z": {"velocity_z", "vertical_speed"},
        "vertical_speed": {"velocity_z", "vertical_speed"},
    }
    return aliases.get(core, {core})


def _share_for_features(feature_names: list[str], values: np.ndarray, predicate: Any) -> float:
    total = float(np.sum(np.abs(values)))
    if not math.isfinite(total) or total <= 0.0:
        return math.nan
    selected = float(sum(abs(value) for name, value in zip(feature_names, values, strict=True) if predicate(name)))
    return selected / total


def _topk_features(feature_names: list[str], values: np.ndarray, k: int = 5) -> list[str]:
    indices = np.argsort(np.abs(values))[::-1][:k]
    return [feature_names[index] for index in indices]


def _format_metric(value: Any, *, digits: int = 3) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    if value in ("", None):
        return "n/a"
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(numeric):
        return "n/a"
    return f"{numeric:.{digits}f}"


def _median(values: list[float]) -> float:
    finite = np.asarray([value for value in values if math.isfinite(value)], dtype=float)
    if finite.size == 0:
        return math.nan
    return float(np.median(finite))


def _response_row(response_name: str, baseline: MatrixData, diagnostic: MatrixData, family_id: str) -> dict[str, Any]:
    if response_name not in baseline.response_names or response_name not in diagnostic.response_names:
        raise ValueError(f"response missing from A1 matrices: {response_name}")
    response_index = baseline.response_names.index(response_name)
    baseline_values = baseline.values[:, response_index]
    diagnostic_values = diagnostic.values[:, response_index]
    family_candidates = _response_family_candidates(response_name)
    baseline_same_family_share = _share_for_features(
        baseline.feature_names,
        baseline_values,
        lambda feature_name: _feature_base(feature_name) in family_candidates,
    )
    diagnostic_same_family_share = _share_for_features(
        diagnostic.feature_names,
        diagnostic_values,
        lambda feature_name: _feature_base(feature_name) in family_candidates,
    )
    baseline_command_share = _share_for_features(
        baseline.feature_names,
        baseline_values,
        lambda feature_name: feature_name.startswith("command_"),
    )
    diagnostic_command_share = _share_for_features(
        diagnostic.feature_names,
        diagnostic_values,
        lambda feature_name: feature_name.startswith("command_"),
    )
    baseline_mode_share = _share_for_features(
        baseline.feature_names,
        baseline_values,
        lambda feature_name: feature_name.startswith("mode_"),
    )
    diagnostic_mode_share = _share_for_features(
        diagnostic.feature_names,
        diagnostic_values,
        lambda feature_name: feature_name.startswith("mode_"),
    )
    baseline_top_index = int(np.argmax(np.abs(baseline_values)))
    diagnostic_top_index = int(np.argmax(np.abs(diagnostic_values)))
    baseline_top1_feature = baseline.feature_names[baseline_top_index]
    diagnostic_top1_feature = diagnostic.feature_names[diagnostic_top_index]
    baseline_top1_value = float(baseline_values[baseline_top_index])
    diagnostic_top1_value = float(diagnostic_values[diagnostic_top_index])
    baseline_top5_features = _topk_features(baseline.feature_names, baseline_values)
    diagnostic_top5_features = _topk_features(diagnostic.feature_names, diagnostic_values)
    top1_stable = baseline_top1_feature == diagnostic_top1_feature
    top1_sign_match = top1_stable and math.copysign(1.0, baseline_top1_value) == math.copysign(1.0, diagnostic_top1_value)
    baseline_top5_set = set(baseline_top5_features)
    diagnostic_top5_set = set(diagnostic_top5_features)
    union = baseline_top5_set | diagnostic_top5_set
    top5_jaccard = float(len(baseline_top5_set & diagnostic_top5_set) / len(union)) if union else math.nan
    return {
        "response_name": response_name,
        "family_id": family_id,
        "baseline_top1_feature": baseline_top1_feature,
        "baseline_top1_value": baseline_top1_value,
        "diagnostic_top1_feature": diagnostic_top1_feature,
        "diagnostic_top1_value": diagnostic_top1_value,
        "baseline_same_family_share": baseline_same_family_share,
        "diagnostic_same_family_share": diagnostic_same_family_share,
        "baseline_command_share": baseline_command_share,
        "diagnostic_command_share": diagnostic_command_share,
        "baseline_mode_share": baseline_mode_share,
        "diagnostic_mode_share": diagnostic_mode_share,
        "top1_stable": top1_stable,
        "top1_sign_match": top1_sign_match,
        "top5_jaccard": top5_jaccard,
        "baseline_top5_features": ",".join(baseline_top5_features),
        "diagnostic_top5_features": ",".join(diagnostic_top5_features),
    }


def _family_result(spec: FamilySpec, response_rows: list[dict[str, Any]]) -> dict[str, Any]:
    family_rows = [row for row in response_rows if row["family_id"] == spec.family_id]
    baseline_same_family_share = _median([float(row["baseline_same_family_share"]) for row in family_rows])
    diagnostic_same_family_share = _median([float(row["diagnostic_same_family_share"]) for row in family_rows])
    median_command_share = _median(
        [
            _median([float(row["baseline_command_share"]), float(row["diagnostic_command_share"])])
            for row in family_rows
        ]
    )
    median_mode_share = _median(
        [
            _median([float(row["baseline_mode_share"]), float(row["diagnostic_mode_share"])])
            for row in family_rows
        ]
    )
    top1_stability_rate = float(sum(1 for row in family_rows if bool(row["top1_stable"])) / len(family_rows)) if family_rows else math.nan
    top1_sign_match_rate = float(sum(1 for row in family_rows if bool(row["top1_sign_match"])) / len(family_rows)) if family_rows else math.nan
    median_top5_jaccard = _median([float(row["top5_jaccard"]) for row in family_rows])
    blocking_reasons: list[str] = []
    if not math.isfinite(baseline_same_family_share) or baseline_same_family_share < SAME_FAMILY_SHARE_MIN:
        blocking_reasons.append("baseline_same_family_share_below_threshold")
    if not math.isfinite(diagnostic_same_family_share) or diagnostic_same_family_share < SAME_FAMILY_SHARE_MIN:
        blocking_reasons.append("diagnostic_same_family_share_below_threshold")
    if not math.isfinite(median_command_share) or median_command_share > COMMAND_SHARE_MAX:
        blocking_reasons.append("command_share_above_threshold")
    if not math.isfinite(median_mode_share) or median_mode_share > MODE_SHARE_MAX:
        blocking_reasons.append("mode_share_above_threshold")
    if not math.isfinite(top1_stability_rate) or top1_stability_rate < TOP1_STABILITY_MIN:
        blocking_reasons.append("top1_stability_below_threshold")
    if not math.isfinite(top1_sign_match_rate) or top1_sign_match_rate < TOP1_SIGN_MATCH_MIN:
        blocking_reasons.append("top1_sign_match_below_threshold")
    if not math.isfinite(median_top5_jaccard) or median_top5_jaccard < TOP5_JACCARD_MIN:
        blocking_reasons.append("top5_overlap_below_threshold")
    return {
        "family_id": spec.family_id,
        "response_count": len(family_rows),
        "responses": [row["response_name"] for row in family_rows],
        "baseline_median_same_family_share": baseline_same_family_share,
        "diagnostic_median_same_family_share": diagnostic_same_family_share,
        "median_command_share": median_command_share,
        "median_mode_share": median_mode_share,
        "top1_stability_rate": top1_stability_rate,
        "top1_sign_match_rate": top1_sign_match_rate,
        "median_top5_jaccard": median_top5_jaccard,
        "supported": not blocking_reasons,
        "blocking_reasons": blocking_reasons,
    }


def _family_sort_key(result: dict[str, Any]) -> tuple[Any, ...]:
    avg_same_family = _median(
        [
            float(result["baseline_median_same_family_share"]),
            float(result["diagnostic_median_same_family_share"]),
        ]
    )
    return (
        bool(result["supported"]),
        avg_same_family,
        float(result["top1_stability_rate"]),
        float(result["median_top5_jaccard"]),
        -float(result["median_command_share"]),
    )


def analyze_px4_a1_target_scout(
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

    response_rows: list[dict[str, Any]] = []
    for spec in FAMILY_SPECS:
        for response_name in spec.responses:
            if response_name not in baseline_matrix.response_names or response_name not in diagnostic_matrix.response_names:
                continue
            response_rows.append(_response_row(response_name, baseline_matrix, diagnostic_matrix, spec.family_id))
    if not response_rows:
        raise ValueError("no A1 response rows were available for target scouting")
    family_results = [
        _family_result(spec, response_rows)
        for spec in FAMILY_SPECS
        if any(row["family_id"] == spec.family_id for row in response_rows)
    ]
    family_results.sort(key=_family_sort_key, reverse=True)
    best_family = family_results[0]
    combo_ready = (
        str(baseline_entry.get("generalization_status")) == "generalized_supported"
        and str(diagnostic_entry.get("generalization_status")) == "generalized_supported"
    )
    recommended_next_target = best_family["family_id"] if combo_ready and bool(best_family["supported"]) else "none"
    recommended_next_step = (
        "start_px4_a1_attitude_family_readiness"
        if recommended_next_target == "attitude_roll_pitch_continuation"
        else "iterate_a1_family_selection_only"
    )
    if recommended_next_target == "none":
        recommended_next_step = "iterate_a1_family_selection_only"
    overall_decision = {
        "recommended_next_target": recommended_next_target,
        "recommended_next_step": recommended_next_step,
        "combo_ready": combo_ready,
        "selected_family": best_family["family_id"],
    }
    study_scope = {
        "backend": "px4",
        "anchor_id": "A1",
        "combo": "full_augmented | next_raw_state | ols_affine | stratified",
        "baseline_study": str(_prefer_workspace_study_path(baseline_study)),
        "diagnostic_study": str(_prefer_workspace_study_path(diagnostic_study)),
        "target_family_scope": [result["family_id"] for result in family_results],
    }
    phase_generalization = {
        "baseline": baseline_entry,
        "diagnostic": diagnostic_entry,
    }
    blocking_reasons = [reason for result in family_results for reason in result["blocking_reasons"]]
    return {
        "study_scope": study_scope,
        "phase_generalization": phase_generalization,
        "response_rows": response_rows,
        "family_results": family_results,
        "overall_decision": overall_decision,
        "blocking_reasons": blocking_reasons,
    }


def render_px4_a1_target_scout_markdown(payload: dict[str, Any]) -> str:
    overall = payload["overall_decision"]
    lines = [
        "# PX4 A1 Target Scout",
        "",
        f"- recommended_next_target: {overall['recommended_next_target']}",
        f"- recommended_next_step: {overall['recommended_next_step']}",
        f"- selected_family: {overall['selected_family']}",
        f"- combo_ready: {'yes' if overall['combo_ready'] else 'no'}",
        "",
        "## Family Matrix",
        "",
        "| family | supported | baseline_same | diagnostic_same | command | top1_stable | top5_jaccard |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in payload["family_results"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    result["family_id"],
                    _format_metric(result["supported"]),
                    _format_metric(result["baseline_median_same_family_share"]),
                    _format_metric(result["diagnostic_median_same_family_share"]),
                    _format_metric(result["median_command_share"]),
                    _format_metric(result["top1_stability_rate"]),
                    _format_metric(result["median_top5_jaccard"]),
                ]
            )
            + " |"
        )
    lines.append("")
    for result in payload["family_results"]:
        lines.append(f"## {result['family_id']}")
        lines.append("")
        lines.append(f"- responses: {', '.join(result['responses'])}")
        lines.append(
            f"- baseline_same_family_share={_format_metric(result['baseline_median_same_family_share'])}, "
            f"diagnostic_same_family_share={_format_metric(result['diagnostic_median_same_family_share'])}, "
            f"median_command_share={_format_metric(result['median_command_share'])}, "
            f"median_mode_share={_format_metric(result['median_mode_share'])}"
        )
        lines.append(
            f"- top1_stability_rate={_format_metric(result['top1_stability_rate'])}, "
            f"top1_sign_match_rate={_format_metric(result['top1_sign_match_rate'])}, "
            f"median_top5_jaccard={_format_metric(result['median_top5_jaccard'])}"
        )
        lines.append(
            f"- blocking_reasons: {', '.join(result['blocking_reasons']) if result['blocking_reasons'] else 'none'}"
        )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run_px4_a1_target_scout(
    *,
    baseline_study: Path = DEFAULT_BASELINE_STUDY,
    diagnostic_study: Path = DEFAULT_DIAGNOSTIC_STUDY,
    output_root: Path | None = None,
) -> Path:
    payload = analyze_px4_a1_target_scout(
        baseline_study=baseline_study,
        diagnostic_study=diagnostic_study,
    )
    paths = _output_paths(output_root.expanduser().resolve() if output_root else None)
    family_rows = []
    for result in payload["family_results"]:
        family_rows.append(
            {
                "family_id": result["family_id"],
                "response_count": result["response_count"],
                "baseline_median_same_family_share": result["baseline_median_same_family_share"],
                "diagnostic_median_same_family_share": result["diagnostic_median_same_family_share"],
                "median_command_share": result["median_command_share"],
                "median_mode_share": result["median_mode_share"],
                "top1_stability_rate": result["top1_stability_rate"],
                "top1_sign_match_rate": result["top1_sign_match_rate"],
                "median_top5_jaccard": result["median_top5_jaccard"],
                "supported": result["supported"],
                "blocking_reasons": ",".join(result["blocking_reasons"]),
            }
        )
    paths["report_path"].write_text(render_px4_a1_target_scout_markdown(payload), encoding="utf-8")
    write_json(paths["summary_path"], payload)
    write_rows_csv(paths["response_table_path"], payload["response_rows"], fieldnames=RESPONSE_LEVEL_FIELDNAMES)
    write_rows_csv(paths["family_matrix_path"], family_rows, fieldnames=FAMILY_MATRIX_FIELDNAMES)
    write_yaml(
        paths["manifest_path"],
        {
            "study_name": STUDY_NAME,
            "study_id": paths["base_dir"].name,
            "baseline_study": str(_prefer_workspace_study_path(baseline_study)),
            "diagnostic_study": str(_prefer_workspace_study_path(diagnostic_study)),
            "output_files": {
                "report": _relative_workspace_path(paths["report_path"]),
                "summary": _relative_workspace_path(paths["summary_path"]),
                "response_level_target_scout": _relative_workspace_path(paths["response_table_path"]),
                "family_target_matrix": _relative_workspace_path(paths["family_matrix_path"]),
            },
            "summary": payload,
        },
    )
    return paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Analyze PX4 A1 target families from canonical fit artifacts.")
    parser.add_argument("--baseline-study", type=Path, default=DEFAULT_BASELINE_STUDY)
    parser.add_argument("--diagnostic-study", type=Path, default=DEFAULT_DIAGNOSTIC_STUDY)
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args(argv)

    study_dir = run_px4_a1_target_scout(
        baseline_study=args.baseline_study,
        diagnostic_study=args.diagnostic_study,
        output_root=args.output_root,
    )
    print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
