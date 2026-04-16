from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from linearity_core.io import ensure_study_directories, read_rows_csv, write_json, write_rows_csv, write_yaml

from .ardupilot_a2_readiness import _format_metric, _median, _relative_workspace_path, _safe_float, _safe_str_list
from .ardupilot_a2_target_scout import _analyze_attempt, _tier_range

STUDY_NAME = "ardupilot_a2_pair_target_readiness"
TARGET_MODE = "GUIDED_NOGPS"
TARGET_SCENARIOS = ("nominal", "throttle_biased")
ACCEPTED_TARGET = 5
PAIR_ACTIVE_RATE_MIN = 0.15
PAIR_BASELINE_RATE_MAX = 0.05
PAIR_SPECIFICITY_MIN = 0.12
PAIR_SIGN_CONSISTENCY_MIN = 0.90
PAIR_TO_COLLECTIVE_RATIO_MIN = 0.70
PAIR_TIER_RANGE_MAX = 0.08

RUN_LEVEL_FIELDNAMES = [
    "flight_mode",
    "scenario",
    "amplitude_tier",
    "config_key",
    "config_name",
    "run_id",
    "study_name",
    "config_profile",
    "artifact_dir",
    "analysis_status",
    "baseline_pair_split_rate",
    "active_pair_split_rate",
    "pair_split_specificity",
    "pair_split_sign_consistency",
    "pair_split_direction",
    "baseline_collective_floor_rate",
    "active_collective_floor_rate",
    "collective_floor_specificity",
    "accepted",
    "failsafe_during_experiment",
    "completion_reason",
    "rejection_reasons",
    "anomaly_summary",
    "status",
    "exit_code",
    "research_acceptance",
]

SCENARIO_MATRIX_FIELDNAMES = [
    "scenario",
    "accepted_count",
    "attempt_count",
    "ready",
    "median_active_pair_rate",
    "median_baseline_pair_rate",
    "median_pair_specificity",
    "median_pair_sign_consistency",
    "median_pair_to_collective_ratio",
    "pair_tier_range_specificity",
    "dominant_direction",
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
        "report_path": paths["reports_dir"] / "a2_pair_target_readiness.md",
        "summary_path": paths["summary_dir"] / "a2_pair_target_readiness.json",
        "run_level_table_path": tables_dir / "run_level_pair_target.csv",
        "scenario_matrix_path": tables_dir / "scenario_pair_target_matrix.csv",
    }


def _scenario_summary(scenario: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    attempt_count = len(rows)
    accepted_rows = [row for row in rows if bool(row.get("accepted"))]
    accepted_count = len(accepted_rows)
    blocking_reasons: list[str] = []
    if accepted_count < ACCEPTED_TARGET:
        blocking_reasons.append("accepted_target_not_met")

    median_active_pair_rate = _median([_safe_float(row.get("active_pair_split_rate")) for row in accepted_rows])
    median_baseline_pair_rate = _median([_safe_float(row.get("baseline_pair_split_rate")) for row in accepted_rows])
    median_pair_specificity = _median([_safe_float(row.get("pair_split_specificity")) for row in accepted_rows])
    median_pair_sign_consistency = _median([_safe_float(row.get("pair_split_sign_consistency")) for row in accepted_rows])
    median_collective_specificity = _median([_safe_float(row.get("collective_floor_specificity")) for row in accepted_rows])
    pair_tier_range_specificity = _tier_range(accepted_rows, "pair_split_specificity")
    pair_to_collective_ratios = []
    for row in accepted_rows:
        pair_specificity = _safe_float(row.get("pair_split_specificity"))
        collective_specificity = _safe_float(row.get("collective_floor_specificity"))
        if not math.isfinite(pair_specificity):
            continue
        if math.isfinite(collective_specificity) and collective_specificity > 0.0:
            pair_to_collective_ratios.append(pair_specificity / collective_specificity)
        elif pair_specificity > 0.0:
            pair_to_collective_ratios.append(999.0)
    median_pair_to_collective_ratio = _median(pair_to_collective_ratios)
    directions = [
        str(row.get("pair_split_direction", ""))
        for row in accepted_rows
        if str(row.get("pair_split_direction", "")) not in ("", "none")
    ]
    dominant_direction = Counter(directions).most_common(1)[0][0] if directions else "none"

    if not math.isfinite(median_active_pair_rate) or median_active_pair_rate < PAIR_ACTIVE_RATE_MIN:
        blocking_reasons.append("pair_active_rate_below_threshold")
    if not math.isfinite(median_baseline_pair_rate) or median_baseline_pair_rate > PAIR_BASELINE_RATE_MAX:
        blocking_reasons.append("pair_baseline_rate_above_threshold")
    if not math.isfinite(median_pair_specificity) or median_pair_specificity < PAIR_SPECIFICITY_MIN:
        blocking_reasons.append("pair_specificity_below_threshold")
    if not math.isfinite(median_pair_sign_consistency) or median_pair_sign_consistency < PAIR_SIGN_CONSISTENCY_MIN:
        blocking_reasons.append("pair_sign_consistency_below_threshold")
    if not math.isfinite(median_pair_to_collective_ratio) or median_pair_to_collective_ratio < PAIR_TO_COLLECTIVE_RATIO_MIN:
        blocking_reasons.append("pair_to_collective_ratio_below_threshold")
    if not math.isfinite(pair_tier_range_specificity) or pair_tier_range_specificity > PAIR_TIER_RANGE_MAX:
        blocking_reasons.append("pair_tier_range_above_threshold")
    if dominant_direction == "none":
        blocking_reasons.append("pair_direction_unavailable")

    return {
        "scenario": scenario,
        "accepted_count": accepted_count,
        "attempt_count": attempt_count,
        "ready": not blocking_reasons,
        "median_active_pair_rate": median_active_pair_rate,
        "median_baseline_pair_rate": median_baseline_pair_rate,
        "median_pair_specificity": median_pair_specificity,
        "median_pair_sign_consistency": median_pair_sign_consistency,
        "median_pair_to_collective_ratio": median_pair_to_collective_ratio,
        "pair_tier_range_specificity": pair_tier_range_specificity,
        "dominant_direction": dominant_direction,
        "blocking_reasons": blocking_reasons,
    }


def _flatten_scenario_row(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "scenario": result["scenario"],
        "accepted_count": result["accepted_count"],
        "attempt_count": result["attempt_count"],
        "ready": result["ready"],
        "median_active_pair_rate": result["median_active_pair_rate"],
        "median_baseline_pair_rate": result["median_baseline_pair_rate"],
        "median_pair_specificity": result["median_pair_specificity"],
        "median_pair_sign_consistency": result["median_pair_sign_consistency"],
        "median_pair_to_collective_ratio": result["median_pair_to_collective_ratio"],
        "pair_tier_range_specificity": result["pair_tier_range_specificity"],
        "dominant_direction": result["dominant_direction"],
        "blocking_reasons": ",".join(result["blocking_reasons"]),
    }


def render_ardupilot_a2_pair_target_readiness_markdown(payload: dict[str, Any]) -> str:
    overall = payload["overall_decision"]
    lines = [
        "# ArduPilot A2 Pair-Target Readiness",
        "",
        f"- ready_for_pair_attack_v1: {'yes' if overall['ready_for_pair_attack_v1'] else 'no'}",
        f"- recommended_path: {overall['recommended_path']}",
        f"- dominant_direction: {overall['dominant_direction']}",
        f"- blocking_reasons: {', '.join(payload['blocking_reasons']) if payload['blocking_reasons'] else 'none'}",
        "",
        "## Scenario Matrix",
        "",
        "| scenario | ready | accepted_count | active_pair_rate | baseline_pair_rate | specificity | sign_consistency | ratio | direction |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in payload["scenario_results"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    result["scenario"],
                    _format_metric(result["ready"]),
                    str(result["accepted_count"]),
                    _format_metric(result["median_active_pair_rate"]),
                    _format_metric(result["median_baseline_pair_rate"]),
                    _format_metric(result["median_pair_specificity"]),
                    _format_metric(result["median_pair_sign_consistency"]),
                    _format_metric(result["median_pair_to_collective_ratio"]),
                    result["dominant_direction"],
                ]
            )
            + " |"
        )
    lines.append("")
    for result in payload["scenario_results"]:
        lines.append(f"## {result['scenario']}")
        lines.append("")
        lines.append(f"- ready: {'yes' if result['ready'] else 'no'}")
        lines.append(
            f"- pair metrics: active_rate={_format_metric(result['median_active_pair_rate'])}, "
            f"baseline_rate={_format_metric(result['median_baseline_pair_rate'])}, "
            f"specificity={_format_metric(result['median_pair_specificity'])}, "
            f"sign_consistency={_format_metric(result['median_pair_sign_consistency'])}, "
            f"pair_to_collective_ratio={_format_metric(result['median_pair_to_collective_ratio'])}, "
            f"tier_range={_format_metric(result['pair_tier_range_specificity'])}, "
            f"direction={result['dominant_direction']}"
        )
        lines.append(
            f"- blocking_reasons: {', '.join(result['blocking_reasons']) if result['blocking_reasons'] else 'none'}"
        )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run_ardupilot_a2_pair_target_readiness(
    *,
    runs_manifest: Path,
    output_root: Path | None = None,
) -> Path:
    manifest_path = runs_manifest.expanduser().resolve()
    if not manifest_path.exists():
        raise FileNotFoundError(f"runs_manifest not found: {manifest_path}")
    rows = read_rows_csv(manifest_path)
    attempts = [_analyze_attempt(row) for row in rows]
    filtered_attempts = [
        row
        for row in attempts
        if str(row.get("flight_mode", "")).strip().upper() == TARGET_MODE and str(row.get("scenario", "")) in TARGET_SCENARIOS
    ]
    if not filtered_attempts:
        raise ValueError("no GUIDED_NOGPS pair-target scenarios were found in runs_manifest")

    scenario_results = [
        _scenario_summary(scenario, [row for row in filtered_attempts if row.get("scenario") == scenario])
        for scenario in TARGET_SCENARIOS
        if any(str(row.get("scenario", "")) == scenario for row in filtered_attempts)
    ]
    blocking_reasons = [reason for result in scenario_results for reason in result["blocking_reasons"]]
    directions = {result["dominant_direction"] for result in scenario_results if result["dominant_direction"] != "none"}
    dominant_direction = next(iter(directions)) if len(directions) == 1 else "mixed"
    ready_for_pair_attack_v1 = all(result["ready"] for result in scenario_results) and dominant_direction not in {"none", "mixed"}
    overall_decision = {
        "ready_for_pair_attack_v1": ready_for_pair_attack_v1,
        "recommended_path": "start_guided_nogps_pair_attack_v1" if ready_for_pair_attack_v1 else "iterate_pair_target_protocol_only",
        "dominant_direction": dominant_direction,
        "scenario_status": {result["scenario"]: result["ready"] for result in scenario_results},
    }
    study_scope = {
        "backend": "ardupilot",
        "mode_scope": [TARGET_MODE],
        "x_schema": "commands_only",
        "y_schema": "actuator_response",
        "target_signal": "pair_imbalance_12_vs_34",
        "input_source": "telemetry/input_trace.csv",
        "response_source": "telemetry/bin_rcou.csv",
        "scenario_scope": [result["scenario"] for result in scenario_results],
    }
    payload = {
        "study_scope": study_scope,
        "scenario_results": scenario_results,
        "overall_decision": overall_decision,
        "blocking_reasons": blocking_reasons,
    }

    paths = _output_paths(output_root.expanduser().resolve() if output_root else None)
    report_text = render_ardupilot_a2_pair_target_readiness_markdown(payload)
    run_level_rows = []
    for row in filtered_attempts:
        normalized = {key: row.get(key, "") for key in RUN_LEVEL_FIELDNAMES}
        normalized["rejection_reasons"] = ",".join(_safe_str_list(normalized.get("rejection_reasons")))
        normalized["anomaly_summary"] = ",".join(_safe_str_list(normalized.get("anomaly_summary")))
        run_level_rows.append(normalized)
    scenario_matrix_rows = [_flatten_scenario_row(result) for result in scenario_results]

    paths["report_path"].write_text(report_text, encoding="utf-8")
    write_json(paths["summary_path"], payload)
    write_rows_csv(paths["run_level_table_path"], run_level_rows, fieldnames=RUN_LEVEL_FIELDNAMES)
    write_rows_csv(paths["scenario_matrix_path"], scenario_matrix_rows, fieldnames=SCENARIO_MATRIX_FIELDNAMES)
    write_yaml(
        paths["manifest_path"],
        {
            "study_name": STUDY_NAME,
            "study_id": paths["base_dir"].name,
            "runs_manifest": str(manifest_path),
            "source_run_dirs": sorted({row["artifact_dir"] for row in run_level_rows if row.get("artifact_dir")}),
            "output_files": {
                "report": _relative_workspace_path(paths["report_path"]),
                "summary": _relative_workspace_path(paths["summary_path"]),
                "run_level_pair_target": _relative_workspace_path(paths["run_level_table_path"]),
                "scenario_pair_target_matrix": _relative_workspace_path(paths["scenario_matrix_path"]),
            },
            "summary": payload,
        },
    )
    return paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Assess GUIDED_NOGPS pair-target readiness from existing A2 runs.")
    parser.add_argument("--runs-manifest", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args(argv)

    study_dir = run_ardupilot_a2_pair_target_readiness(
        runs_manifest=args.runs_manifest,
        output_root=args.output_root,
    )
    print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
