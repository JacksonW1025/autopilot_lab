from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from linearity_core.io import ensure_study_directories, read_rows_csv, read_yaml, write_json, write_rows_csv, write_yaml

import linearity_analysis.ardupilot_a2_pair_target_readiness as pair_readiness
import linearity_analysis.ardupilot_a2_target_scout as target_scout

STUDY_NAME = "ardupilot_a2_pair_target_algorithm_evaluation"
TARGET_MODE = "GUIDED_NOGPS"
TARGET_SIGNAL = "pair_imbalance_12_vs_34"
TARGET_READY_STEP = "guided_nogps_pair_target_readiness"
PAIR_READY_PATH = "start_guided_nogps_pair_attack_v1"
STRATEGY_NAME = "reference_pulse_train_v1"
EVALUATION_MODE = "offline_replay"
TARGET_SCENARIOS = ("nominal", "throttle_biased")
REFERENCE_TIERS = ("micro", "probe", "confirm")
CANONICAL_DIRECTION = "12_gt_34"
CANONICAL_PULSE_COUNT = 5
CANONICAL_PULSE_WIDTH_S = 0.35
CANONICAL_PULSE_GAP_S = 0.95
TIER_DEFAULTS = {
    "micro": {"pulse_amplitude": 0.02, "bias_nominal": 0.0, "bias_throttle_biased": 0.04},
    "probe": {"pulse_amplitude": 0.05, "bias_nominal": 0.0, "bias_throttle_biased": 0.04},
    "confirm": {"pulse_amplitude": 0.10, "bias_nominal": 0.0, "bias_throttle_biased": 0.04},
}
SAFE_ENVELOPE = {
    "pulse_amplitude_min": 0.02,
    "pulse_amplitude_max": 0.10,
    "bias_min": 0.0,
    "bias_max": 0.04,
    "pulse_count_min": 1,
    "pulse_count_max": 5,
    "pulse_width_s_min": 0.20,
    "pulse_width_s_max": 0.50,
    "pulse_gap_s_min": 0.50,
    "pulse_gap_s_max": 1.20,
}

RUN_LEVEL_FIELDNAMES = [
    "run_id",
    "flight_mode",
    "scenario",
    "amplitude_tier",
    "config_key",
    "config_name",
    "accepted",
    "analysis_status",
    "reference_tier_match",
    "selected_scenario",
    "direction_match",
    "pair_split_direction",
    "active_pair_split_rate",
    "baseline_pair_split_rate",
    "pair_split_specificity",
    "pair_split_sign_consistency",
    "collective_floor_specificity",
    "pair_to_collective_ratio",
    "artifact_dir",
    "blocking_reasons",
]

SCENARIO_MATRIX_FIELDNAMES = [
    "scenario",
    "reference_tier",
    "accepted_count",
    "attempt_count",
    "accepted_reference_tier_count",
    "reference_ready",
    "dominant_direction",
    "median_active_pair_rate",
    "median_baseline_pair_rate",
    "median_pair_specificity",
    "median_pair_sign_consistency",
    "median_pair_to_collective_ratio",
    "pair_tier_range_specificity",
    "hard_regression",
    "soft_regression",
    "blocking_reasons",
]

GENERATED_SCHEDULE_FIELDNAMES = [
    "schedule_index",
    "strategy",
    "mode",
    "scenario",
    "reference_tier",
    "direction",
    "pulse_amplitude",
    "bias",
    "pulse_count",
    "pulse_width_s",
    "pulse_gap_s",
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
        "report_path": paths["reports_dir"] / "a2_pair_target_algorithm_evaluation.md",
        "summary_path": paths["summary_dir"] / "a2_pair_target_algorithm_evaluation.json",
        "scenario_matrix_path": tables_dir / "scenario_evaluation_matrix.csv",
        "run_level_alignment_path": tables_dir / "run_level_reference_alignment.csv",
        "generated_schedule_path": tables_dir / "generated_schedule.csv",
    }


def _relative_workspace_path(path: Path) -> str:
    return pair_readiness._relative_workspace_path(path)


def _safe_float(value: Any, default: float = math.nan) -> float:
    return pair_readiness._safe_float(value, default)


def _safe_str_list(value: Any) -> list[str]:
    return pair_readiness._safe_str_list(value)


def _format_metric(value: Any, *, digits: int = 3) -> str:
    return pair_readiness._format_metric(value, digits=digits)


def _read_summary_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _load_artifact_bundle(study_dir: Path, summary_filename: str) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    resolved_dir = study_dir.expanduser().resolve()
    if not resolved_dir.exists():
        raise FileNotFoundError(f"study_dir not found: {resolved_dir}")
    manifest_path = resolved_dir / "manifest.yaml"
    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest missing: {manifest_path}")
    summary_path = resolved_dir / "summary" / summary_filename
    if not summary_path.exists():
        raise FileNotFoundError(f"summary missing: {summary_path}")
    return resolved_dir, read_yaml(manifest_path), _read_summary_json(summary_path)


def _selected_scenarios(scope: str) -> tuple[str, ...]:
    if scope == "both":
        return TARGET_SCENARIOS
    if scope not in TARGET_SCENARIOS:
        raise ValueError(f"unsupported scenario scope: {scope}")
    return (scope,)


def _resolve_runs_manifest(
    *,
    runs_manifest: Path | None,
    pair_target_manifest: dict[str, Any],
    target_scout_manifest: dict[str, Any],
) -> Path:
    candidates = [
        runs_manifest,
        Path(str(pair_target_manifest.get("runs_manifest", ""))) if pair_target_manifest.get("runs_manifest") else None,
        Path(str(target_scout_manifest.get("runs_manifest", ""))) if target_scout_manifest.get("runs_manifest") else None,
    ]
    for candidate in candidates:
        if candidate is None:
            continue
        resolved = candidate.expanduser().resolve()
        if resolved.exists():
            return resolved
    raise FileNotFoundError("runs_manifest not found in CLI args or source artifacts")


def _default_bias_for_scenario(scenario: str, reference_tier: str) -> float:
    defaults = TIER_DEFAULTS[reference_tier]
    return float(defaults["bias_throttle_biased"] if scenario == "throttle_biased" else defaults["bias_nominal"])


def _validate_algorithm_spec(algorithm_spec: dict[str, Any], canonical_direction: str) -> list[str]:
    reasons: list[str] = []
    direction = str(algorithm_spec.get("direction", ""))
    pulse_amplitude = float(algorithm_spec.get("pulse_amplitude"))
    bias = algorithm_spec.get("bias")
    pulse_count = int(algorithm_spec.get("pulse_count"))
    pulse_width_s = float(algorithm_spec.get("pulse_width_s"))
    pulse_gap_s = float(algorithm_spec.get("pulse_gap_s"))
    if str(algorithm_spec.get("mode", "")) != EVALUATION_MODE:
        reasons.append("unsupported_evaluation_mode")
    if str(algorithm_spec.get("strategy", "")) != STRATEGY_NAME:
        reasons.append("unsupported_strategy")
    if str(algorithm_spec.get("target_signal", "")) != TARGET_SIGNAL:
        reasons.append("target_signal_mismatch")
    if str(algorithm_spec.get("flight_mode", "")) != TARGET_MODE:
        reasons.append("flight_mode_mismatch")
    if direction != canonical_direction:
        reasons.append("algorithm_direction_mismatch")
    if pulse_amplitude < SAFE_ENVELOPE["pulse_amplitude_min"] or pulse_amplitude > SAFE_ENVELOPE["pulse_amplitude_max"]:
        reasons.append("pulse_amplitude_out_of_envelope")
    if bias is not None:
        bias_value = float(bias)
        if bias_value < SAFE_ENVELOPE["bias_min"] or bias_value > SAFE_ENVELOPE["bias_max"]:
            reasons.append("bias_out_of_envelope")
    if pulse_count < SAFE_ENVELOPE["pulse_count_min"] or pulse_count > SAFE_ENVELOPE["pulse_count_max"]:
        reasons.append("pulse_count_out_of_envelope")
    if pulse_width_s < SAFE_ENVELOPE["pulse_width_s_min"] or pulse_width_s > SAFE_ENVELOPE["pulse_width_s_max"]:
        reasons.append("pulse_width_out_of_envelope")
    if pulse_gap_s < SAFE_ENVELOPE["pulse_gap_s_min"] or pulse_gap_s > SAFE_ENVELOPE["pulse_gap_s_max"]:
        reasons.append("pulse_gap_s_out_of_envelope")
    return reasons


def _validate_target_scout_summary(summary: dict[str, Any], selected_scenarios: tuple[str, ...]) -> list[str]:
    overall = dict(summary.get("overall_decision", {}) or {})
    reasons: list[str] = []
    if overall.get("recommended_mode") != TARGET_MODE:
        reasons.append("target_scout_recommended_mode_mismatch")
    if overall.get("recommended_next_target") != TARGET_SIGNAL:
        reasons.append("target_scout_recommended_target_mismatch")
    if overall.get("recommended_next_step") != TARGET_READY_STEP:
        reasons.append("target_scout_recommended_step_mismatch")
    scenario_targets = {
        str(result.get("scenario", "")): str(result.get("recommended_target", ""))
        for result in list(summary.get("scenario_results", []) or [])
        if str(result.get("flight_mode", "")).upper() == TARGET_MODE
    }
    for scenario in selected_scenarios:
        if scenario_targets.get(scenario) != TARGET_SIGNAL:
            reasons.append(f"target_scout_scenario_target_mismatch:{scenario}")
    return reasons


def _validate_pair_readiness_summary(summary: dict[str, Any], selected_scenarios: tuple[str, ...], direction: str) -> list[str]:
    overall = dict(summary.get("overall_decision", {}) or {})
    scenario_status = dict(overall.get("scenario_status", {}) or {})
    reasons: list[str] = []
    if bool(overall.get("ready_for_pair_attack_v1")) is not True:
        reasons.append("pair_readiness_not_ready")
    if overall.get("recommended_path") != PAIR_READY_PATH:
        reasons.append("pair_readiness_recommended_path_mismatch")
    if overall.get("dominant_direction") != direction:
        reasons.append("pair_readiness_direction_mismatch")
    for scenario in selected_scenarios:
        if scenario_status.get(scenario) is not True:
            reasons.append(f"pair_readiness_scenario_not_ready:{scenario}")
    return reasons


def _pair_to_collective_ratio(row: dict[str, Any]) -> float:
    pair_specificity = _safe_float(row.get("pair_split_specificity"))
    collective_specificity = _safe_float(row.get("collective_floor_specificity"))
    if not math.isfinite(pair_specificity):
        return math.nan
    if math.isfinite(collective_specificity) and collective_specificity > 0.0:
        return float(pair_specificity / collective_specificity)
    if pair_specificity > 0.0:
        return 999.0
    return math.nan


def _reference_thresholds(pair_summary: dict[str, Any]) -> dict[str, Any]:
    scenario_reference = {
        str(result.get("scenario", "")): {
            "median_active_pair_rate": _safe_float(result.get("median_active_pair_rate")),
            "median_baseline_pair_rate": _safe_float(result.get("median_baseline_pair_rate")),
            "median_pair_specificity": _safe_float(result.get("median_pair_specificity")),
            "median_pair_sign_consistency": _safe_float(result.get("median_pair_sign_consistency")),
            "median_pair_to_collective_ratio": _safe_float(result.get("median_pair_to_collective_ratio")),
            "pair_tier_range_specificity": _safe_float(result.get("pair_tier_range_specificity")),
            "dominant_direction": str(result.get("dominant_direction", "")),
        }
        for result in list(pair_summary.get("scenario_results", []) or [])
        if str(result.get("scenario", ""))
    }
    return {
        "accepted_target": pair_readiness.ACCEPTED_TARGET,
        "pair_active_rate_min": pair_readiness.PAIR_ACTIVE_RATE_MIN,
        "pair_baseline_rate_max": pair_readiness.PAIR_BASELINE_RATE_MAX,
        "pair_specificity_min": pair_readiness.PAIR_SPECIFICITY_MIN,
        "pair_sign_consistency_min": pair_readiness.PAIR_SIGN_CONSISTENCY_MIN,
        "pair_to_collective_ratio_min": pair_readiness.PAIR_TO_COLLECTIVE_RATIO_MIN,
        "pair_tier_range_max": pair_readiness.PAIR_TIER_RANGE_MAX,
        "canonical_reference_metrics": scenario_reference,
        "safe_envelope": SAFE_ENVELOPE,
    }


def _soft_regression_reasons(
    *,
    scenario: str,
    observed: dict[str, Any],
    reference: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    relative_fields = (
        ("median_active_pair_rate", "active_pair_rate"),
        ("median_pair_specificity", "pair_specificity"),
        ("median_pair_to_collective_ratio", "pair_to_collective_ratio"),
    )
    for observed_key, label in relative_fields:
        observed_value = _safe_float(observed.get(observed_key))
        reference_value = _safe_float(reference.get(observed_key))
        if not math.isfinite(observed_value) or not math.isfinite(reference_value) or reference_value <= 0.0:
            continue
        if observed_value < reference_value * 0.90:
            reasons.append(f"soft_regression_{label}:{scenario}")
    observed_range = _safe_float(observed.get("pair_tier_range_specificity"))
    reference_range = _safe_float(reference.get("pair_tier_range_specificity"))
    if (
        math.isfinite(observed_range)
        and math.isfinite(reference_range)
        and observed_range > reference_range + 0.02
    ):
        reasons.append(f"soft_regression_tier_range_specificity:{scenario}")
    return reasons


def _flatten_run_alignment_row(
    row: dict[str, Any],
    *,
    selected_scenarios: tuple[str, ...],
    reference_tier: str,
    direction: str,
) -> dict[str, Any]:
    reasons: list[str] = []
    if str(row.get("flight_mode", "")) != TARGET_MODE:
        reasons.append("flight_mode_mismatch")
    if str(row.get("scenario", "")) not in selected_scenarios:
        reasons.append("scenario_out_of_scope")
    if bool(row.get("accepted")) is not True:
        reasons.append("run_not_accepted")
    if str(row.get("pair_split_direction", "none")) != direction:
        reasons.append("direction_mismatch")
    return {
        "run_id": row.get("run_id", ""),
        "flight_mode": row.get("flight_mode", ""),
        "scenario": row.get("scenario", ""),
        "amplitude_tier": row.get("amplitude_tier", ""),
        "config_key": row.get("config_key", ""),
        "config_name": row.get("config_name", ""),
        "accepted": row.get("accepted", False),
        "analysis_status": row.get("analysis_status", ""),
        "reference_tier_match": str(row.get("amplitude_tier", "")) == reference_tier,
        "selected_scenario": str(row.get("scenario", "")) in selected_scenarios,
        "direction_match": str(row.get("pair_split_direction", "none")) == direction,
        "pair_split_direction": row.get("pair_split_direction", "none"),
        "active_pair_split_rate": row.get("active_pair_split_rate", math.nan),
        "baseline_pair_split_rate": row.get("baseline_pair_split_rate", math.nan),
        "pair_split_specificity": row.get("pair_split_specificity", math.nan),
        "pair_split_sign_consistency": row.get("pair_split_sign_consistency", math.nan),
        "collective_floor_specificity": row.get("collective_floor_specificity", math.nan),
        "pair_to_collective_ratio": _pair_to_collective_ratio(row),
        "artifact_dir": row.get("artifact_dir", ""),
        "blocking_reasons": ",".join(reasons),
    }


def _flatten_scenario_result(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "scenario": result["scenario"],
        "reference_tier": result["reference_tier"],
        "accepted_count": result["accepted_count"],
        "attempt_count": result["attempt_count"],
        "accepted_reference_tier_count": result["accepted_reference_tier_count"],
        "reference_ready": result["reference_ready"],
        "dominant_direction": result["dominant_direction"],
        "median_active_pair_rate": result["median_active_pair_rate"],
        "median_baseline_pair_rate": result["median_baseline_pair_rate"],
        "median_pair_specificity": result["median_pair_specificity"],
        "median_pair_sign_consistency": result["median_pair_sign_consistency"],
        "median_pair_to_collective_ratio": result["median_pair_to_collective_ratio"],
        "pair_tier_range_specificity": result["pair_tier_range_specificity"],
        "hard_regression": result["hard_regression"],
        "soft_regression": result["soft_regression"],
        "blocking_reasons": ",".join(result["blocking_reasons"]),
    }


def _generated_schedule_rows(
    *,
    selected_scenarios: tuple[str, ...],
    algorithm_spec: dict[str, Any],
    reference_tier: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, scenario in enumerate(selected_scenarios, start=1):
        bias = algorithm_spec["bias_by_scenario"][scenario]
        rows.append(
            {
                "schedule_index": index,
                "strategy": algorithm_spec["strategy"],
                "mode": algorithm_spec["mode"],
                "scenario": scenario,
                "reference_tier": reference_tier,
                "direction": algorithm_spec["direction"],
                "pulse_amplitude": algorithm_spec["pulse_amplitude"],
                "bias": bias,
                "pulse_count": algorithm_spec["pulse_count"],
                "pulse_width_s": algorithm_spec["pulse_width_s"],
                "pulse_gap_s": algorithm_spec["pulse_gap_s"],
            }
        )
    return rows


def render_ardupilot_a2_pair_target_algorithm_evaluation_markdown(payload: dict[str, Any]) -> str:
    overall = payload["overall_decision"]
    algorithm_spec = payload["algorithm_spec"]
    lines = [
        "# ArduPilot A2 Pair-Target Algorithm Evaluation",
        "",
        f"- offline_ready_for_live_eval_v1: {'yes' if overall['offline_ready_for_live_eval_v1'] else 'no'}",
        f"- live_eval_required: {'yes' if overall['live_eval_required'] else 'no'}",
        f"- hard_regression_detected: {'yes' if overall['hard_regression_detected'] else 'no'}",
        f"- soft_regression_detected: {'yes' if overall['soft_regression_detected'] else 'no'}",
        f"- recommended_next_step: {overall['recommended_next_step']}",
        f"- blocking_reasons: {', '.join(payload['blocking_reasons']) if payload['blocking_reasons'] else 'none'}",
        "",
        "## Algorithm Spec",
        "",
        f"- strategy: {algorithm_spec['strategy']}",
        f"- mode: {algorithm_spec['mode']}",
        f"- flight_mode: {algorithm_spec['flight_mode']}",
        f"- target_signal: {algorithm_spec['target_signal']}",
        f"- scenario_scope: {', '.join(algorithm_spec['scenario_scope'])}",
        f"- reference_tier: {algorithm_spec['reference_tier']}",
        f"- direction: {algorithm_spec['direction']}",
        f"- pulse parameters: amplitude={_format_metric(algorithm_spec['pulse_amplitude'])}, "
        f"pulse_count={algorithm_spec['pulse_count']}, pulse_width_s={_format_metric(algorithm_spec['pulse_width_s'])}, "
        f"pulse_gap_s={_format_metric(algorithm_spec['pulse_gap_s'])}",
        f"- bias_by_scenario: "
        + ", ".join(f"{scenario}={_format_metric(value)}" for scenario, value in algorithm_spec["bias_by_scenario"].items()),
        "",
        "## Scenario Matrix",
        "",
        "| scenario | ready | hard_regression | soft_regression | active_pair_rate | specificity | ratio | direction |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in payload["scenario_results"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    result["scenario"],
                    _format_metric(result["reference_ready"]),
                    _format_metric(result["hard_regression"]),
                    _format_metric(result["soft_regression"]),
                    _format_metric(result["median_active_pair_rate"]),
                    _format_metric(result["median_pair_specificity"]),
                    _format_metric(result["median_pair_to_collective_ratio"]),
                    result["dominant_direction"],
                ]
            )
            + " |"
        )
    lines.append("")
    for result in payload["scenario_results"]:
        reference = payload["reference_thresholds"]["canonical_reference_metrics"].get(result["scenario"], {})
        lines.append(f"## {result['scenario']}")
        lines.append("")
        lines.append(f"- reference_ready: {'yes' if result['reference_ready'] else 'no'}")
        lines.append(
            f"- observed metrics: active_rate={_format_metric(result['median_active_pair_rate'])}, "
            f"baseline_rate={_format_metric(result['median_baseline_pair_rate'])}, "
            f"specificity={_format_metric(result['median_pair_specificity'])}, "
            f"sign_consistency={_format_metric(result['median_pair_sign_consistency'])}, "
            f"pair_to_collective_ratio={_format_metric(result['median_pair_to_collective_ratio'])}, "
            f"tier_range={_format_metric(result['pair_tier_range_specificity'])}, "
            f"direction={result['dominant_direction']}"
        )
        lines.append(
            f"- reference metrics: active_rate={_format_metric(reference.get('median_active_pair_rate'))}, "
            f"specificity={_format_metric(reference.get('median_pair_specificity'))}, "
            f"ratio={_format_metric(reference.get('median_pair_to_collective_ratio'))}, "
            f"tier_range={_format_metric(reference.get('pair_tier_range_specificity'))}, "
            f"direction={reference.get('dominant_direction', 'n/a')}"
        )
        lines.append(
            f"- blocking_reasons: {', '.join(result['blocking_reasons']) if result['blocking_reasons'] else 'none'}"
        )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run_ardupilot_a2_pair_target_algorithm_evaluation(
    *,
    a2_target_scout_dir: Path,
    a2_pair_target_dir: Path,
    runs_manifest: Path | None = None,
    output_root: Path | None = None,
    mode: str = EVALUATION_MODE,
    strategy: str = STRATEGY_NAME,
    scenario: str = "both",
    reference_tier: str = "probe",
    direction: str = CANONICAL_DIRECTION,
    pulse_amplitude: float | None = None,
    bias: float | None = None,
    pulse_count: int = CANONICAL_PULSE_COUNT,
    pulse_width_s: float = CANONICAL_PULSE_WIDTH_S,
    pulse_gap_s: float = CANONICAL_PULSE_GAP_S,
) -> Path:
    if mode != EVALUATION_MODE:
        raise ValueError(f"unsupported mode: {mode}")
    if strategy != STRATEGY_NAME:
        raise ValueError(f"unsupported strategy: {strategy}")
    if reference_tier not in REFERENCE_TIERS:
        raise ValueError(f"unsupported reference tier: {reference_tier}")

    selected_scenarios = _selected_scenarios(scenario)
    tier_defaults = TIER_DEFAULTS[reference_tier]
    pulse_amplitude = float(tier_defaults["pulse_amplitude"] if pulse_amplitude is None else pulse_amplitude)
    bias_by_scenario = {
        scenario_name: float(_default_bias_for_scenario(scenario_name, reference_tier) if bias is None else bias)
        for scenario_name in selected_scenarios
    }
    algorithm_spec = {
        "mode": mode,
        "strategy": strategy,
        "flight_mode": TARGET_MODE,
        "target_signal": TARGET_SIGNAL,
        "scenario_scope": list(selected_scenarios),
        "reference_tier": reference_tier,
        "direction": direction,
        "pulse_amplitude": pulse_amplitude,
        "bias": None if bias is None else float(bias),
        "bias_by_scenario": bias_by_scenario,
        "pulse_count": int(pulse_count),
        "pulse_width_s": float(pulse_width_s),
        "pulse_gap_s": float(pulse_gap_s),
    }

    target_scout_dir, target_scout_manifest, target_scout_summary = _load_artifact_bundle(
        a2_target_scout_dir, "a2_target_scout.json"
    )
    pair_target_dir, pair_target_manifest, pair_target_summary = _load_artifact_bundle(
        a2_pair_target_dir, "a2_pair_target_readiness.json"
    )
    resolved_runs_manifest = _resolve_runs_manifest(
        runs_manifest=runs_manifest,
        pair_target_manifest=pair_target_manifest,
        target_scout_manifest=target_scout_manifest,
    )

    blocking_reasons = []
    blocking_reasons.extend(_validate_target_scout_summary(target_scout_summary, selected_scenarios))
    blocking_reasons.extend(_validate_pair_readiness_summary(pair_target_summary, selected_scenarios, direction))
    blocking_reasons.extend(_validate_algorithm_spec(algorithm_spec, str(pair_target_summary["overall_decision"]["dominant_direction"])))

    attempts = [target_scout._analyze_attempt(row) for row in read_rows_csv(resolved_runs_manifest)]
    relevant_attempts = [
        row
        for row in attempts
        if str(row.get("flight_mode", "")).upper() == TARGET_MODE and str(row.get("scenario", "")) in selected_scenarios
    ]
    if not relevant_attempts:
        blocking_reasons.append("selected_scenarios_not_found_in_runs_manifest")

    scenario_results: list[dict[str, Any]] = []
    run_level_rows: list[dict[str, Any]] = []
    for row in relevant_attempts:
        run_level_rows.append(
            _flatten_run_alignment_row(
                row,
                selected_scenarios=selected_scenarios,
                reference_tier=reference_tier,
                direction=direction,
            )
        )

    reference_metrics = _reference_thresholds(pair_target_summary)
    canonical_reference_metrics = reference_metrics["canonical_reference_metrics"]
    for scenario_name in selected_scenarios:
        scenario_rows = [row for row in relevant_attempts if str(row.get("scenario", "")) == scenario_name]
        accepted_reference_tier_count = sum(
            1
            for row in scenario_rows
            if bool(row.get("accepted")) and str(row.get("amplitude_tier", "")) == reference_tier
        )
        scenario_result = pair_readiness._scenario_summary(scenario_name, scenario_rows)
        scenario_blocking_reasons = list(scenario_result["blocking_reasons"])
        if accepted_reference_tier_count <= 0:
            scenario_blocking_reasons.append("reference_tier_coverage_missing")
        if scenario_result["dominant_direction"] != direction:
            scenario_blocking_reasons.append("scenario_direction_mismatch")
        hard_regression = bool(scenario_blocking_reasons)
        soft_reasons = _soft_regression_reasons(
            scenario=scenario_name,
            observed=scenario_result,
            reference=canonical_reference_metrics.get(scenario_name, {}),
        )
        soft_regression = bool(soft_reasons)
        blocking_reasons.extend(f"{reason}:{scenario_name}" if ":" not in reason else reason for reason in scenario_blocking_reasons)
        blocking_reasons.extend(soft_reasons)
        scenario_results.append(
            {
                **scenario_result,
                "reference_tier": reference_tier,
                "accepted_reference_tier_count": accepted_reference_tier_count,
                "reference_ready": scenario_result["ready"],
                "hard_regression": hard_regression,
                "soft_regression": soft_regression,
                "blocking_reasons": sorted(set(scenario_blocking_reasons + soft_reasons)),
            }
        )

    hard_regression_detected = bool(
        blocking_reasons
        and any(
            not reason.startswith("soft_regression_")
            for reason in blocking_reasons
        )
    )
    soft_regression_detected = any(reason.startswith("soft_regression_") for reason in blocking_reasons)
    offline_ready_for_live_eval_v1 = not hard_regression_detected
    live_eval_required = offline_ready_for_live_eval_v1
    if hard_regression_detected:
        recommended_next_step = "fix_artifact_or_protocol_mismatch"
    elif soft_regression_detected:
        recommended_next_step = "tighten_algorithm_spec"
    else:
        recommended_next_step = "hold_for_live_eval"

    generated_schedule_rows = _generated_schedule_rows(
        selected_scenarios=selected_scenarios,
        algorithm_spec=algorithm_spec,
        reference_tier=reference_tier,
    )
    payload = {
        "study_scope": {
            "backend": "ardupilot",
            "flight_mode": TARGET_MODE,
            "mode": EVALUATION_MODE,
            "strategy": STRATEGY_NAME,
            "scenario_scope": list(selected_scenarios),
            "reference_tier": reference_tier,
            "canonical_target_signal": TARGET_SIGNAL,
            "canonical_direction": direction,
        },
        "source_artifacts": {
            "a2_target_scout_dir": str(target_scout_dir),
            "a2_pair_target_dir": str(pair_target_dir),
            "runs_manifest": str(resolved_runs_manifest),
            "source_run_dirs": sorted(
                {
                    *[str(path) for path in _safe_str_list(target_scout_manifest.get("source_run_dirs", []))],
                    *[str(path) for path in _safe_str_list(pair_target_manifest.get("source_run_dirs", []))],
                }
            ),
        },
        "algorithm_spec": algorithm_spec,
        "reference_thresholds": reference_metrics,
        "scenario_results": scenario_results,
        "overall_decision": {
            "offline_ready_for_live_eval_v1": offline_ready_for_live_eval_v1,
            "live_eval_required": live_eval_required,
            "hard_regression_detected": hard_regression_detected,
            "soft_regression_detected": soft_regression_detected,
            "recommended_next_step": recommended_next_step,
        },
        "blocking_reasons": sorted(set(blocking_reasons)),
    }

    paths = _output_paths(output_root.expanduser().resolve() if output_root else None)
    paths["report_path"].write_text(
        render_ardupilot_a2_pair_target_algorithm_evaluation_markdown(payload),
        encoding="utf-8",
    )
    write_json(paths["summary_path"], payload)
    write_rows_csv(
        paths["scenario_matrix_path"],
        [_flatten_scenario_result(result) for result in scenario_results],
        fieldnames=SCENARIO_MATRIX_FIELDNAMES,
    )
    write_rows_csv(paths["run_level_alignment_path"], run_level_rows, fieldnames=RUN_LEVEL_FIELDNAMES)
    write_rows_csv(paths["generated_schedule_path"], generated_schedule_rows, fieldnames=GENERATED_SCHEDULE_FIELDNAMES)
    write_yaml(
        paths["manifest_path"],
        {
            "study_name": STUDY_NAME,
            "study_id": paths["base_dir"].name,
            "source_artifacts": payload["source_artifacts"],
            "output_files": {
                "report": _relative_workspace_path(paths["report_path"]),
                "summary": _relative_workspace_path(paths["summary_path"]),
                "scenario_evaluation_matrix": _relative_workspace_path(paths["scenario_matrix_path"]),
                "run_level_reference_alignment": _relative_workspace_path(paths["run_level_alignment_path"]),
                "generated_schedule": _relative_workspace_path(paths["generated_schedule_path"]),
            },
            "summary": payload,
        },
    )
    return paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run offline A2 pair-target algorithm evaluation against canonical artifacts.")
    parser.add_argument("--a2-target-scout-dir", type=Path, required=True)
    parser.add_argument("--a2-pair-target-dir", type=Path, required=True)
    parser.add_argument("--runs-manifest", type=Path, default=None)
    parser.add_argument("--output-root", type=Path, default=None)
    parser.add_argument("--mode", default=EVALUATION_MODE)
    parser.add_argument("--strategy", default=STRATEGY_NAME)
    parser.add_argument("--scenario", choices=("nominal", "throttle_biased", "both"), default="both")
    parser.add_argument("--reference-tier", choices=REFERENCE_TIERS, default="probe")
    parser.add_argument("--direction", choices=("12_gt_34", "34_gt_12"), default=CANONICAL_DIRECTION)
    parser.add_argument("--pulse-amplitude", type=float, default=None)
    parser.add_argument("--bias", type=float, default=None)
    parser.add_argument("--pulse-count", type=int, default=CANONICAL_PULSE_COUNT)
    parser.add_argument("--pulse-width-s", type=float, default=CANONICAL_PULSE_WIDTH_S)
    parser.add_argument("--pulse-gap-s", type=float, default=CANONICAL_PULSE_GAP_S)
    args = parser.parse_args(argv)

    study_dir = run_ardupilot_a2_pair_target_algorithm_evaluation(
        a2_target_scout_dir=args.a2_target_scout_dir,
        a2_pair_target_dir=args.a2_pair_target_dir,
        runs_manifest=args.runs_manifest,
        output_root=args.output_root,
        mode=args.mode,
        strategy=args.strategy,
        scenario=args.scenario,
        reference_tier=args.reference_tier,
        direction=args.direction,
        pulse_amplitude=args.pulse_amplitude,
        bias=args.bias,
        pulse_count=args.pulse_count,
        pulse_width_s=args.pulse_width_s,
        pulse_gap_s=args.pulse_gap_s,
    )
    print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
