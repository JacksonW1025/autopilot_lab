from __future__ import annotations

import argparse
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from linearity_core.io import ensure_study_directories, write_json, write_rows_csv, write_yaml

from .px4_a1_target_scout import (
    DEFAULT_BASELINE_STUDY,
    DEFAULT_DIAGNOSTIC_STUDY,
    RESPONSE_LEVEL_FIELDNAMES,
    _format_metric,
    _median,
    _relative_workspace_path,
    analyze_px4_a1_target_scout,
)

STUDY_NAME = "px4_a1_family_readiness"
TARGET_FAMILY_ID = "attitude_roll_pitch_continuation"
SCENARIO_CONSISTENCY_MIN = 0.95
SCENARIO_R2_MIN = 0.95
BASELINE_SAME_FAMILY_SHARE_MIN = 0.55
DIAGNOSTIC_SAME_FAMILY_SHARE_MIN = 0.60
COMMAND_SHARE_MAX = 0.12
MODE_SHARE_MAX = 0.01
TOP1_STABILITY_MIN = 1.0
TOP1_SIGN_MATCH_MIN = 1.0
TOP5_JACCARD_MIN = 0.50

FAMILY_READINESS_FIELDNAMES = [
    "family_id",
    "response_count",
    "baseline_scenario_consistency",
    "diagnostic_scenario_consistency",
    "baseline_min_scenario_r2",
    "diagnostic_min_scenario_r2",
    "baseline_median_same_family_share",
    "diagnostic_median_same_family_share",
    "median_command_share",
    "median_mode_share",
    "top1_stability_rate",
    "top1_sign_match_rate",
    "median_top5_jaccard",
    "ready",
    "blocking_reasons",
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
        "report_path": paths["reports_dir"] / "a1_family_readiness.md",
        "summary_path": paths["summary_dir"] / "a1_family_readiness.json",
        "response_table_path": tables_dir / "response_level_family_readiness.csv",
        "family_table_path": tables_dir / "family_readiness.csv",
    }


def _phase_metrics(entry: dict[str, Any]) -> dict[str, float]:
    subgroup = dict(entry.get("scenario_subgroup_r2", {}) or {})
    subgroup_values = [float(value) for value in subgroup.values()]
    finite_values = [value for value in subgroup_values if math.isfinite(value)]
    return {
        "scenario_consistency": float(entry.get("scenario_consistency", math.nan)),
        "min_scenario_r2": float(min(finite_values)) if finite_values else math.nan,
    }


def render_px4_a1_family_readiness_markdown(payload: dict[str, Any]) -> str:
    overall = payload["overall_decision"]
    family = payload["family_result"]
    lines = [
        "# PX4 A1 Family Readiness",
        "",
        f"- selected_family: {family['family_id']}",
        f"- ready_for_reproduction_v1: {'yes' if overall['ready_for_reproduction_v1'] else 'no'}",
        f"- recommended_path: {overall['recommended_path']}",
        f"- blocking_reasons: {', '.join(payload['blocking_reasons']) if payload['blocking_reasons'] else 'none'}",
        "",
        "## Readiness",
        "",
        f"- baseline_scenario_consistency={_format_metric(family['baseline_scenario_consistency'])}, "
        f"diagnostic_scenario_consistency={_format_metric(family['diagnostic_scenario_consistency'])}",
        f"- baseline_min_scenario_r2={_format_metric(family['baseline_min_scenario_r2'])}, "
        f"diagnostic_min_scenario_r2={_format_metric(family['diagnostic_min_scenario_r2'])}",
        f"- baseline_same_family_share={_format_metric(family['baseline_median_same_family_share'])}, "
        f"diagnostic_same_family_share={_format_metric(family['diagnostic_median_same_family_share'])}",
        f"- median_command_share={_format_metric(family['median_command_share'])}, "
        f"median_mode_share={_format_metric(family['median_mode_share'])}",
        f"- top1_stability_rate={_format_metric(family['top1_stability_rate'])}, "
        f"top1_sign_match_rate={_format_metric(family['top1_sign_match_rate'])}, "
        f"median_top5_jaccard={_format_metric(family['median_top5_jaccard'])}",
        "",
        "## Responses",
        "",
    ]
    for row in payload["response_rows"]:
        lines.append(
            f"- {row['response_name']}: "
            f"baseline_top1={row['baseline_top1_feature']} ({_format_metric(row['baseline_top1_value'])}), "
            f"diagnostic_top1={row['diagnostic_top1_feature']} ({_format_metric(row['diagnostic_top1_value'])}), "
            f"same_family={_format_metric(row['baseline_same_family_share'])}/{_format_metric(row['diagnostic_same_family_share'])}, "
            f"top5_jaccard={_format_metric(row['top5_jaccard'])}"
        )
    return "\n".join(lines).rstrip() + "\n"


def run_px4_a1_family_readiness(
    *,
    baseline_study: Path = DEFAULT_BASELINE_STUDY,
    diagnostic_study: Path = DEFAULT_DIAGNOSTIC_STUDY,
    family_id: str = TARGET_FAMILY_ID,
    output_root: Path | None = None,
) -> Path:
    scout_payload = analyze_px4_a1_target_scout(
        baseline_study=baseline_study,
        diagnostic_study=diagnostic_study,
    )
    family_result = next((row for row in scout_payload["family_results"] if row["family_id"] == family_id), None)
    if family_result is None:
        raise ValueError(f"family not found in A1 target scout: {family_id}")
    response_rows = [row for row in scout_payload["response_rows"] if row["family_id"] == family_id]
    baseline_phase = _phase_metrics(scout_payload["phase_generalization"]["baseline"])
    diagnostic_phase = _phase_metrics(scout_payload["phase_generalization"]["diagnostic"])
    blocking_reasons: list[str] = []
    if not math.isfinite(baseline_phase["scenario_consistency"]) or baseline_phase["scenario_consistency"] < SCENARIO_CONSISTENCY_MIN:
        blocking_reasons.append("baseline_scenario_consistency_below_threshold")
    if not math.isfinite(diagnostic_phase["scenario_consistency"]) or diagnostic_phase["scenario_consistency"] < SCENARIO_CONSISTENCY_MIN:
        blocking_reasons.append("diagnostic_scenario_consistency_below_threshold")
    if not math.isfinite(baseline_phase["min_scenario_r2"]) or baseline_phase["min_scenario_r2"] < SCENARIO_R2_MIN:
        blocking_reasons.append("baseline_min_scenario_r2_below_threshold")
    if not math.isfinite(diagnostic_phase["min_scenario_r2"]) or diagnostic_phase["min_scenario_r2"] < SCENARIO_R2_MIN:
        blocking_reasons.append("diagnostic_min_scenario_r2_below_threshold")
    if not math.isfinite(family_result["baseline_median_same_family_share"]) or family_result["baseline_median_same_family_share"] < BASELINE_SAME_FAMILY_SHARE_MIN:
        blocking_reasons.append("baseline_same_family_share_below_threshold")
    if not math.isfinite(family_result["diagnostic_median_same_family_share"]) or family_result["diagnostic_median_same_family_share"] < DIAGNOSTIC_SAME_FAMILY_SHARE_MIN:
        blocking_reasons.append("diagnostic_same_family_share_below_threshold")
    if not math.isfinite(family_result["median_command_share"]) or family_result["median_command_share"] > COMMAND_SHARE_MAX:
        blocking_reasons.append("command_share_above_threshold")
    if not math.isfinite(family_result["median_mode_share"]) or family_result["median_mode_share"] > MODE_SHARE_MAX:
        blocking_reasons.append("mode_share_above_threshold")
    if not math.isfinite(family_result["top1_stability_rate"]) or family_result["top1_stability_rate"] < TOP1_STABILITY_MIN:
        blocking_reasons.append("top1_stability_below_threshold")
    if not math.isfinite(family_result["top1_sign_match_rate"]) or family_result["top1_sign_match_rate"] < TOP1_SIGN_MATCH_MIN:
        blocking_reasons.append("top1_sign_match_below_threshold")
    if not math.isfinite(family_result["median_top5_jaccard"]) or family_result["median_top5_jaccard"] < TOP5_JACCARD_MIN:
        blocking_reasons.append("top5_overlap_below_threshold")

    readiness_result = {
        "family_id": family_id,
        "response_count": family_result["response_count"],
        "baseline_scenario_consistency": baseline_phase["scenario_consistency"],
        "diagnostic_scenario_consistency": diagnostic_phase["scenario_consistency"],
        "baseline_min_scenario_r2": baseline_phase["min_scenario_r2"],
        "diagnostic_min_scenario_r2": diagnostic_phase["min_scenario_r2"],
        "baseline_median_same_family_share": family_result["baseline_median_same_family_share"],
        "diagnostic_median_same_family_share": family_result["diagnostic_median_same_family_share"],
        "median_command_share": family_result["median_command_share"],
        "median_mode_share": family_result["median_mode_share"],
        "top1_stability_rate": family_result["top1_stability_rate"],
        "top1_sign_match_rate": family_result["top1_sign_match_rate"],
        "median_top5_jaccard": family_result["median_top5_jaccard"],
        "ready": not blocking_reasons,
        "blocking_reasons": blocking_reasons,
    }
    overall_decision = {
        "selected_family": family_id,
        "ready_for_reproduction_v1": not blocking_reasons,
        "recommended_path": "continue_px4_a1_attitude_reproduction" if not blocking_reasons else "iterate_a1_family_selection_only",
    }
    payload = {
        "study_scope": scout_payload["study_scope"],
        "selected_family": family_id,
        "phase_generalization": scout_payload["phase_generalization"],
        "family_result": readiness_result,
        "response_rows": response_rows,
        "overall_decision": overall_decision,
        "blocking_reasons": blocking_reasons,
    }

    paths = _output_paths(output_root.expanduser().resolve() if output_root else None)
    paths["report_path"].write_text(render_px4_a1_family_readiness_markdown(payload), encoding="utf-8")
    write_json(paths["summary_path"], payload)
    write_rows_csv(paths["response_table_path"], response_rows, fieldnames=RESPONSE_LEVEL_FIELDNAMES)
    write_rows_csv(paths["family_table_path"], [readiness_result], fieldnames=FAMILY_READINESS_FIELDNAMES)
    write_yaml(
        paths["manifest_path"],
        {
            "study_name": STUDY_NAME,
            "study_id": paths["base_dir"].name,
            "baseline_study": scout_payload["study_scope"]["baseline_study"],
            "diagnostic_study": scout_payload["study_scope"]["diagnostic_study"],
            "selected_family": family_id,
            "output_files": {
                "report": _relative_workspace_path(paths["report_path"]),
                "summary": _relative_workspace_path(paths["summary_path"]),
                "response_level_family_readiness": _relative_workspace_path(paths["response_table_path"]),
                "family_readiness": _relative_workspace_path(paths["family_table_path"]),
            },
            "summary": payload,
        },
    )
    return paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Assess PX4 A1 family readiness from canonical fit artifacts.")
    parser.add_argument("--baseline-study", type=Path, default=DEFAULT_BASELINE_STUDY)
    parser.add_argument("--diagnostic-study", type=Path, default=DEFAULT_DIAGNOSTIC_STUDY)
    parser.add_argument("--family", type=str, default=TARGET_FAMILY_ID)
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args(argv)

    study_dir = run_px4_a1_family_readiness(
        baseline_study=args.baseline_study,
        diagnostic_study=args.diagnostic_study,
        family_id=args.family,
        output_root=args.output_root,
    )
    print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
