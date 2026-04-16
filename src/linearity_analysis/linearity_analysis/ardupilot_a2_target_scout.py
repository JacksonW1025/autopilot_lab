from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from linearity_core.io import ensure_study_directories, read_rows_csv, write_json, write_rows_csv, write_yaml
from linearity_core.research_contract import manifest_acceptance_state

from .ardupilot_a2_readiness import (
    _build_aligned_samples,
    _format_metric,
    _median,
    _read_manifest,
    _relative_workspace_path,
    _safe_float,
    _safe_int,
    _safe_str_list,
)

STUDY_NAME = "ardupilot_a2_target_scout"
KNOWN_SCENARIOS = ("nominal", "proxy_dynamic", "throttle_biased")
KNOWN_TIERS = ("micro", "probe", "confirm", "small", "medium")
BASELINE_PHASES = frozenset({"stabilize", "pulse_gap", "recover"})
ACTIVE_PHASES = frozenset({"pulse_active", "alternating_pulse_active_pos", "alternating_pulse_active_neg"})
FLOOR_THRESHOLD = 0.02
PAIR_SPLIT_THRESHOLD = 0.10
ACCEPTED_TARGET = 5
COLLECTIVE_SPECIFICITY_MIN = 0.15
PAIR_SPECIFICITY_MIN = 0.12
PAIR_ACTIVE_RATE_MIN = 0.15
PAIR_SIGN_CONSISTENCY_MIN = 0.90
SINGLE_SPECIFICITY_MIN = 0.15
SPECIFICITY_TIER_RANGE_MAX = 0.08
ACTUATOR_SPREAD_MIN = 0.03

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
    "baseline_sample_count",
    "active_sample_count",
    "baseline_collective_floor_rate",
    "active_collective_floor_rate",
    "collective_floor_specificity",
    "baseline_pair_split_rate",
    "active_pair_split_rate",
    "pair_split_specificity",
    "pair_split_sign_consistency",
    "pair_split_direction",
    "baseline_actuator_1_floor_rate",
    "baseline_actuator_2_floor_rate",
    "baseline_actuator_3_floor_rate",
    "baseline_actuator_4_floor_rate",
    "active_actuator_1_floor_rate",
    "active_actuator_2_floor_rate",
    "active_actuator_3_floor_rate",
    "active_actuator_4_floor_rate",
    "actuator_1_floor_specificity",
    "actuator_2_floor_specificity",
    "actuator_3_floor_specificity",
    "actuator_4_floor_specificity",
    "actuator_specificity_spread",
    "active_dominant_vector_state",
    "active_dominant_vector_purity",
    "baseline_dominant_vector_state",
    "baseline_dominant_vector_purity",
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
    "flight_mode",
    "scenario",
    "accepted_count",
    "attempt_count",
    "recommended_target",
    "recommended_path",
    "collective_median_specificity",
    "collective_tier_range_specificity",
    "pair_median_specificity",
    "pair_median_active_rate",
    "pair_median_sign_consistency",
    "pair_tier_range_specificity",
    "pair_dominant_direction",
    "best_single_actuator",
    "best_single_median_specificity",
    "best_single_tier_range_specificity",
    "actuator_specificity_spread",
    "active_dominant_vector_state",
    "active_dominant_vector_purity",
    "baseline_dominant_vector_state",
    "baseline_dominant_vector_purity",
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
        "report_path": paths["reports_dir"] / "a2_target_scout.md",
        "summary_path": paths["summary_dir"] / "a2_target_scout.json",
        "run_level_table_path": tables_dir / "run_level_target_scout.csv",
        "scenario_matrix_path": tables_dir / "scenario_target_matrix.csv",
    }


def _scenario_tier_from_text(text: str) -> tuple[str, str] | None:
    normalized = str(text).strip().lower().replace(".yaml", "")
    for scenario in KNOWN_SCENARIOS:
        for tier in KNOWN_TIERS:
            if f"{scenario}_{tier}" in normalized:
                return scenario, tier
    return None


def _scenario_tier_from_sources(row: dict[str, str], manifest: dict[str, Any]) -> tuple[str, str]:
    study_config = manifest.get("study_config", {}) or {}
    extras = study_config.get("extras", {}) if isinstance(study_config, dict) else {}
    candidates = [
        f"{manifest.get('scenario', '')}_{extras.get('amplitude_tier', '')}",
        f"{study_config.get('scenario', '')}_{extras.get('amplitude_tier', '')}" if isinstance(study_config, dict) else "",
        str(extras.get("readiness_scenario", "")),
        str(manifest.get("study_name", "")),
        str(manifest.get("config_profile", "")),
        Path(str(row.get("config", ""))).stem,
    ]
    for candidate in candidates:
        result = _scenario_tier_from_text(candidate)
        if result is not None:
            return result
    scenario = str(manifest.get("scenario", "")).strip().lower()
    tier = str(extras.get("amplitude_tier", "")).strip().lower()
    if scenario and tier:
        return scenario, tier
    raise ValueError(f"unable to infer target-scout scenario/tier from row={row.get('config', '')!r}")


def _flight_mode_from_manifest(manifest: dict[str, Any]) -> str:
    study_config = manifest.get("study_config", {}) or {}
    if isinstance(study_config, dict):
        candidate = str(study_config.get("flight_mode", "")).strip().upper()
        if candidate:
            return candidate
    candidate = str(manifest.get("flight_mode", "")).strip().upper()
    return candidate or "UNKNOWN"


def _bool_as_rate(count: int, total: int) -> float:
    if total <= 0:
        return math.nan
    return float(count / total)


def _vector_state(values: list[float], *, digits: int = 3) -> str:
    return "|".join(f"{value:.{digits}f}" for value in values)


def _rate(rows: list[dict[str, Any]], predicate: Any) -> float:
    if not rows:
        return math.nan
    return float(sum(1 for row in rows if predicate(row)) / len(rows))


def _dominant_state(rows: list[dict[str, Any]], field: str) -> tuple[str, float]:
    labels = [str(row.get(field, "")) for row in rows if str(row.get(field, ""))]
    if not labels:
        return "", math.nan
    counter = Counter(labels)
    label, count = counter.most_common(1)[0]
    return label, float(count / len(labels))


def _most_common_rate(labels: list[str]) -> tuple[str, float]:
    if not labels:
        return "none", math.nan
    counter = Counter(labels)
    label, count = counter.most_common(1)[0]
    return label, float(count / len(labels))


def _tier_range(rows: list[dict[str, Any]], field: str) -> float:
    values_by_tier: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        tier = str(row.get("amplitude_tier", ""))
        value = _safe_float(row.get(field))
        if tier and math.isfinite(value):
            values_by_tier[tier].append(value)
    if not values_by_tier:
        return math.nan
    tier_medians = [_median(values) for values in values_by_tier.values()]
    finite = [value for value in tier_medians if math.isfinite(value)]
    if not finite:
        return math.nan
    return float(max(finite) - min(finite))


def _pair_direction_label(value: float) -> str:
    if not math.isfinite(value) or abs(value) < 1e-12:
        return "none"
    return "12_gt_34" if value > 0.0 else "34_gt_12"


def _compute_run_target_metrics(samples: list[dict[str, Any]]) -> dict[str, Any]:
    baseline_rows = [
        row
        for row in samples
        if str(row.get("phase", "")) in BASELINE_PHASES
        and all(math.isfinite(_safe_float(row.get(f"actuator_{index}"))) for index in range(1, 5))
    ]
    active_rows = [
        row
        for row in samples
        if str(row.get("phase", "")) in ACTIVE_PHASES
        and all(math.isfinite(_safe_float(row.get(f"actuator_{index}"))) for index in range(1, 5))
    ]
    if not baseline_rows:
        return {
            "analysis_status": "baseline_unavailable",
            "baseline_sample_count": 0,
            "active_sample_count": len(active_rows),
        }
    if not active_rows:
        return {
            "analysis_status": "active_unavailable",
            "baseline_sample_count": len(baseline_rows),
            "active_sample_count": 0,
        }

    for row in baseline_rows + active_rows:
        vector = [_safe_float(row.get(f"actuator_{index}")) for index in range(1, 5)]
        row["collective_floor"] = all(value <= FLOOR_THRESHOLD for value in vector)
        pair_imbalance = ((vector[0] + vector[1]) / 2.0) - ((vector[2] + vector[3]) / 2.0)
        row["pair_imbalance"] = pair_imbalance
        row["pair_split"] = bool(abs(pair_imbalance) >= PAIR_SPLIT_THRESHOLD and not row["collective_floor"])
        row["pair_direction"] = _pair_direction_label(pair_imbalance) if row["pair_split"] else "none"
        row["vector_state"] = _vector_state(vector)
        for actuator_index, value in enumerate(vector, start=1):
            row[f"actuator_{actuator_index}_floor"] = bool(value <= FLOOR_THRESHOLD)

    baseline_collective_floor_rate = _rate(baseline_rows, lambda row: bool(row.get("collective_floor")))
    active_collective_floor_rate = _rate(active_rows, lambda row: bool(row.get("collective_floor")))
    baseline_pair_split_rate = _rate(baseline_rows, lambda row: bool(row.get("pair_split")))
    active_pair_split_rate = _rate(active_rows, lambda row: bool(row.get("pair_split")))

    active_pair_directions = [str(row.get("pair_direction", "")) for row in active_rows if bool(row.get("pair_split"))]
    dominant_pair_direction, pair_sign_consistency = _most_common_rate(active_pair_directions)
    active_dominant_vector_state, active_dominant_vector_purity = _dominant_state(active_rows, "vector_state")
    baseline_dominant_vector_state, baseline_dominant_vector_purity = _dominant_state(baseline_rows, "vector_state")

    metrics: dict[str, Any] = {
        "analysis_status": "ok",
        "baseline_sample_count": len(baseline_rows),
        "active_sample_count": len(active_rows),
        "baseline_collective_floor_rate": baseline_collective_floor_rate,
        "active_collective_floor_rate": active_collective_floor_rate,
        "collective_floor_specificity": active_collective_floor_rate - baseline_collective_floor_rate,
        "baseline_pair_split_rate": baseline_pair_split_rate,
        "active_pair_split_rate": active_pair_split_rate,
        "pair_split_specificity": active_pair_split_rate - baseline_pair_split_rate,
        "pair_split_sign_consistency": pair_sign_consistency,
        "pair_split_direction": dominant_pair_direction,
        "active_dominant_vector_state": active_dominant_vector_state,
        "active_dominant_vector_purity": active_dominant_vector_purity,
        "baseline_dominant_vector_state": baseline_dominant_vector_state,
        "baseline_dominant_vector_purity": baseline_dominant_vector_purity,
    }
    actuator_specificities: list[float] = []
    for actuator_index in range(1, 5):
        baseline_rate = _rate(baseline_rows, lambda row, idx=actuator_index: bool(row.get(f"actuator_{idx}_floor")))
        active_rate = _rate(active_rows, lambda row, idx=actuator_index: bool(row.get(f"actuator_{idx}_floor")))
        specificity = active_rate - baseline_rate
        metrics[f"baseline_actuator_{actuator_index}_floor_rate"] = baseline_rate
        metrics[f"active_actuator_{actuator_index}_floor_rate"] = active_rate
        metrics[f"actuator_{actuator_index}_floor_specificity"] = specificity
        actuator_specificities.append(specificity)
    finite_specificities = [value for value in actuator_specificities if math.isfinite(value)]
    metrics["actuator_specificity_spread"] = (
        float(max(finite_specificities) - min(finite_specificities)) if finite_specificities else math.nan
    )
    return metrics


def _analyze_attempt(row: dict[str, str]) -> dict[str, Any]:
    artifact_value = str(row.get("artifact_dir", "")).strip()
    artifact_dir = Path(artifact_value).expanduser().resolve() if artifact_value else None
    manifest = _read_manifest(artifact_dir / "manifest.yaml" if artifact_dir else None)
    scenario = ""
    tier = ""
    try:
        scenario, tier = _scenario_tier_from_sources(row, manifest)
    except ValueError:
        scenario = "unknown"
        tier = "unknown"
    manifest_state = manifest_acceptance_state(manifest) if manifest else str(row.get("research_acceptance", "")).strip().lower()
    acceptance_block = manifest.get("data_quality", {}).get("acceptance", {}) if manifest else {}
    if not isinstance(acceptance_block, dict):
        acceptance_block = {}
    run_id = str(manifest.get("run_id", artifact_dir.name if artifact_dir else f"attempt_{row.get('index', '0')}"))
    completion_reason = str(manifest.get("runtime_report", {}).get("completion_reason", "")) if manifest else ""
    research_rejection_reasons = manifest.get("research_rejection_reasons", []) if manifest else []
    rejection_reasons = _safe_str_list(research_rejection_reasons or acceptance_block.get("rejection_reasons", []))
    anomaly_summary = _safe_str_list(manifest.get("anomaly_summary", []) if manifest else [])
    attempt: dict[str, Any] = {
        "flight_mode": _flight_mode_from_manifest(manifest) if manifest else "UNKNOWN",
        "scenario": scenario,
        "amplitude_tier": tier,
        "config_key": f"{scenario}-{tier}",
        "config_name": Path(str(row.get("config", ""))).name,
        "run_id": run_id,
        "study_name": str(manifest.get("study_name", "")),
        "config_profile": str(manifest.get("config_profile", "")),
        "artifact_dir": str(artifact_dir) if artifact_dir else "",
        "analysis_status": "artifact_missing",
        "accepted": manifest_state == "accepted",
        "failsafe_during_experiment": bool(acceptance_block.get("failsafe_during_experiment")) if acceptance_block else False,
        "completion_reason": completion_reason,
        "rejection_reasons": rejection_reasons,
        "anomaly_summary": anomaly_summary,
        "status": str(row.get("status", "")),
        "exit_code": _safe_int(row.get("exit_code"), 0),
        "research_acceptance": manifest_state,
        "baseline_sample_count": 0,
        "active_sample_count": 0,
        "baseline_collective_floor_rate": math.nan,
        "active_collective_floor_rate": math.nan,
        "collective_floor_specificity": math.nan,
        "baseline_pair_split_rate": math.nan,
        "active_pair_split_rate": math.nan,
        "pair_split_specificity": math.nan,
        "pair_split_sign_consistency": math.nan,
        "pair_split_direction": "none",
        "active_dominant_vector_state": "",
        "active_dominant_vector_purity": math.nan,
        "baseline_dominant_vector_state": "",
        "baseline_dominant_vector_purity": math.nan,
        "actuator_specificity_spread": math.nan,
    }
    for actuator_index in range(1, 5):
        attempt[f"baseline_actuator_{actuator_index}_floor_rate"] = math.nan
        attempt[f"active_actuator_{actuator_index}_floor_rate"] = math.nan
        attempt[f"actuator_{actuator_index}_floor_specificity"] = math.nan
    if artifact_dir is None or not artifact_dir.exists() or not manifest:
        return attempt
    samples = _build_aligned_samples(artifact_dir, manifest)
    if not samples:
        attempt["analysis_status"] = "telemetry_unavailable"
        return attempt
    attempt.update(_compute_run_target_metrics(samples))
    return attempt


def _scenario_result(flight_mode: str, scenario: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    attempt_count = len(rows)
    accepted_rows = [row for row in rows if bool(row.get("accepted"))]
    accepted_count = len(accepted_rows)
    blocking_reasons: list[str] = []
    if accepted_count < ACCEPTED_TARGET:
        blocking_reasons.append("accepted_target_not_met")

    collective_specificity = _median([_safe_float(row.get("collective_floor_specificity")) for row in accepted_rows])
    collective_tier_range = _tier_range(accepted_rows, "collective_floor_specificity")
    pair_specificity = _median([_safe_float(row.get("pair_split_specificity")) for row in accepted_rows])
    pair_active_rate = _median([_safe_float(row.get("active_pair_split_rate")) for row in accepted_rows])
    pair_sign_consistency = _median([_safe_float(row.get("pair_split_sign_consistency")) for row in accepted_rows])
    pair_tier_range = _tier_range(accepted_rows, "pair_split_specificity")
    pair_dominant_direction, _ = _most_common_rate(
        [str(row.get("pair_split_direction", "")) for row in accepted_rows if str(row.get("pair_split_direction", "")) not in ("", "none")]
    )
    actuator_specificities = {
        f"actuator_{index}": _median([_safe_float(row.get(f"actuator_{index}_floor_specificity")) for row in accepted_rows])
        for index in range(1, 5)
    }
    best_single_actuator = max(actuator_specificities, key=lambda key: _safe_float(actuator_specificities[key], -math.inf))
    best_single_specificity = _safe_float(actuator_specificities[best_single_actuator])
    best_single_tier_range = _tier_range(
        [
            {
                **row,
                "single_specificity": row.get(f"{best_single_actuator}_floor_specificity"),
            }
            for row in accepted_rows
        ],
        "single_specificity",
    )
    actuator_spread = _safe_float(_median([_safe_float(row.get("actuator_specificity_spread")) for row in accepted_rows]))
    active_state, active_purity = _most_common_rate(
        [str(row.get("active_dominant_vector_state", "")) for row in accepted_rows if str(row.get("active_dominant_vector_state", ""))]
    )
    baseline_state, baseline_purity = _most_common_rate(
        [str(row.get("baseline_dominant_vector_state", "")) for row in accepted_rows if str(row.get("baseline_dominant_vector_state", ""))]
    )

    pair_supported = (
        accepted_count >= ACCEPTED_TARGET
        and math.isfinite(pair_specificity)
        and pair_specificity >= PAIR_SPECIFICITY_MIN
        and math.isfinite(pair_active_rate)
        and pair_active_rate >= PAIR_ACTIVE_RATE_MIN
        and math.isfinite(pair_sign_consistency)
        and pair_sign_consistency >= PAIR_SIGN_CONSISTENCY_MIN
        and math.isfinite(pair_tier_range)
        and pair_tier_range <= SPECIFICITY_TIER_RANGE_MAX
    )
    single_supported = (
        accepted_count >= ACCEPTED_TARGET
        and math.isfinite(best_single_specificity)
        and best_single_specificity >= SINGLE_SPECIFICITY_MIN
        and math.isfinite(best_single_tier_range)
        and best_single_tier_range <= SPECIFICITY_TIER_RANGE_MAX
        and math.isfinite(actuator_spread)
        and actuator_spread >= ACTUATOR_SPREAD_MIN
    )
    collective_supported = (
        accepted_count >= ACCEPTED_TARGET
        and math.isfinite(collective_specificity)
        and collective_specificity >= COLLECTIVE_SPECIFICITY_MIN
        and math.isfinite(collective_tier_range)
        and collective_tier_range <= SPECIFICITY_TIER_RANGE_MAX
    )

    if not pair_supported:
        if not math.isfinite(pair_specificity) or pair_specificity < PAIR_SPECIFICITY_MIN:
            blocking_reasons.append("pair_specificity_below_threshold")
        if not math.isfinite(pair_active_rate) or pair_active_rate < PAIR_ACTIVE_RATE_MIN:
            blocking_reasons.append("pair_active_rate_below_threshold")
        if not math.isfinite(pair_sign_consistency) or pair_sign_consistency < PAIR_SIGN_CONSISTENCY_MIN:
            blocking_reasons.append("pair_sign_consistency_below_threshold")
        if not math.isfinite(pair_tier_range) or pair_tier_range > SPECIFICITY_TIER_RANGE_MAX:
            blocking_reasons.append("pair_tier_range_above_threshold")
    if not single_supported:
        if not math.isfinite(actuator_spread) or actuator_spread < ACTUATOR_SPREAD_MIN:
            blocking_reasons.append("single_actuator_symmetry_collapse")
        if not math.isfinite(best_single_specificity) or best_single_specificity < SINGLE_SPECIFICITY_MIN:
            blocking_reasons.append("single_actuator_specificity_below_threshold")
    if not collective_supported:
        if not math.isfinite(collective_specificity) or collective_specificity < COLLECTIVE_SPECIFICITY_MIN:
            blocking_reasons.append("collective_specificity_below_threshold")
        if not math.isfinite(collective_tier_range) or collective_tier_range > SPECIFICITY_TIER_RANGE_MAX:
            blocking_reasons.append("collective_tier_range_above_threshold")

    if pair_supported:
        recommended_target = "pair_imbalance_12_vs_34"
        recommended_path = f"{flight_mode.lower()}_pair_target_readiness"
    elif single_supported:
        recommended_target = best_single_actuator
        recommended_path = "run_single_actuator_target_readiness"
    elif collective_supported:
        recommended_target = "collective_floor_state"
        recommended_path = "collective_only_no_new_target_gain"
    else:
        recommended_target = "none"
        recommended_path = "no_target_signal_identified"

    return {
        "flight_mode": flight_mode,
        "scenario": scenario,
        "accepted_count": accepted_count,
        "attempt_count": attempt_count,
        "recommended_target": recommended_target,
        "recommended_path": recommended_path,
        "collective_floor": {
            "median_active_rate": _median([_safe_float(row.get("active_collective_floor_rate")) for row in accepted_rows]),
            "median_baseline_rate": _median([_safe_float(row.get("baseline_collective_floor_rate")) for row in accepted_rows]),
            "median_specificity": collective_specificity,
            "tier_range_specificity": collective_tier_range,
        },
        "pair_imbalance": {
            "median_active_rate": pair_active_rate,
            "median_baseline_rate": _median([_safe_float(row.get("baseline_pair_split_rate")) for row in accepted_rows]),
            "median_specificity": pair_specificity,
            "median_sign_consistency": pair_sign_consistency,
            "tier_range_specificity": pair_tier_range,
            "dominant_direction": pair_dominant_direction,
        },
        "best_single_actuator": {
            "actuator": best_single_actuator,
            "median_active_rate": _median([_safe_float(row.get(f"active_{best_single_actuator}_floor_rate")) for row in accepted_rows]),
            "median_baseline_rate": _median([_safe_float(row.get(f"baseline_{best_single_actuator}_floor_rate")) for row in accepted_rows]),
            "median_specificity": best_single_specificity,
            "tier_range_specificity": best_single_tier_range,
        },
        "actuator_specificity_spread": actuator_spread,
        "active_dominant_vector_state": active_state,
        "active_dominant_vector_purity": active_purity,
        "baseline_dominant_vector_state": baseline_state,
        "baseline_dominant_vector_purity": baseline_purity,
        "blocking_reasons": sorted(set(blocking_reasons)),
    }


def _flatten_scenario_row(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "flight_mode": result["flight_mode"],
        "scenario": result["scenario"],
        "accepted_count": result["accepted_count"],
        "attempt_count": result["attempt_count"],
        "recommended_target": result["recommended_target"],
        "recommended_path": result["recommended_path"],
        "collective_median_specificity": result["collective_floor"]["median_specificity"],
        "collective_tier_range_specificity": result["collective_floor"]["tier_range_specificity"],
        "pair_median_specificity": result["pair_imbalance"]["median_specificity"],
        "pair_median_active_rate": result["pair_imbalance"]["median_active_rate"],
        "pair_median_sign_consistency": result["pair_imbalance"]["median_sign_consistency"],
        "pair_tier_range_specificity": result["pair_imbalance"]["tier_range_specificity"],
        "pair_dominant_direction": result["pair_imbalance"]["dominant_direction"],
        "best_single_actuator": result["best_single_actuator"]["actuator"],
        "best_single_median_specificity": result["best_single_actuator"]["median_specificity"],
        "best_single_tier_range_specificity": result["best_single_actuator"]["tier_range_specificity"],
        "actuator_specificity_spread": result["actuator_specificity_spread"],
        "active_dominant_vector_state": result["active_dominant_vector_state"],
        "active_dominant_vector_purity": result["active_dominant_vector_purity"],
        "baseline_dominant_vector_state": result["baseline_dominant_vector_state"],
        "baseline_dominant_vector_purity": result["baseline_dominant_vector_purity"],
        "blocking_reasons": ",".join(result["blocking_reasons"]),
    }


def render_ardupilot_a2_target_scout_markdown(payload: dict[str, Any]) -> str:
    overall = payload["overall_decision"]
    lines = [
        "# ArduPilot A2 Target Scout",
        "",
        f"- recommended_next_target: {overall['recommended_next_target']}",
        f"- recommended_next_step: {overall['recommended_next_step']}",
        f"- recommended_mode: {overall['recommended_mode']}",
        f"- blocking_reasons: {', '.join(payload['blocking_reasons']) if payload['blocking_reasons'] else 'none'}",
        "",
        "## Scenario Matrix",
        "",
        "| mode | scenario | recommended_target | accepted_count | collective_specificity | pair_specificity | best_single | spread |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in payload["scenario_results"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    result["flight_mode"],
                    result["scenario"],
                    result["recommended_target"],
                    str(result["accepted_count"]),
                    _format_metric(result["collective_floor"]["median_specificity"]),
                    _format_metric(result["pair_imbalance"]["median_specificity"]),
                    result["best_single_actuator"]["actuator"],
                    _format_metric(result["actuator_specificity_spread"]),
                ]
            )
            + " |"
        )
    lines.append("")
    for result in payload["scenario_results"]:
        lines.append(f"## {result['flight_mode']} / {result['scenario']}")
        lines.append("")
        lines.append(f"- recommended_target: {result['recommended_target']}")
        lines.append(f"- recommended_path: {result['recommended_path']}")
        lines.append(
            f"- collective_floor: specificity={_format_metric(result['collective_floor']['median_specificity'])}, "
            f"tier_range={_format_metric(result['collective_floor']['tier_range_specificity'])}"
        )
        lines.append(
            f"- pair_imbalance: specificity={_format_metric(result['pair_imbalance']['median_specificity'])}, "
            f"active_rate={_format_metric(result['pair_imbalance']['median_active_rate'])}, "
            f"sign_consistency={_format_metric(result['pair_imbalance']['median_sign_consistency'])}, "
            f"direction={result['pair_imbalance']['dominant_direction']}"
        )
        lines.append(
            f"- best_single_actuator: {result['best_single_actuator']['actuator']} "
            f"(specificity={_format_metric(result['best_single_actuator']['median_specificity'])}, "
            f"tier_range={_format_metric(result['best_single_actuator']['tier_range_specificity'])})"
        )
        lines.append(
            f"- dominant_states: active={result['active_dominant_vector_state'] or 'n/a'} "
            f"({_format_metric(result['active_dominant_vector_purity'])}), baseline={result['baseline_dominant_vector_state'] or 'n/a'} "
            f"({_format_metric(result['baseline_dominant_vector_purity'])})"
        )
        lines.append(
            f"- blocking_reasons: {', '.join(result['blocking_reasons']) if result['blocking_reasons'] else 'none'}"
        )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run_ardupilot_a2_target_scout(
    *,
    runs_manifest: Path,
    output_root: Path | None = None,
) -> Path:
    manifest_path = runs_manifest.expanduser().resolve()
    if not manifest_path.exists():
        raise FileNotFoundError(f"runs_manifest not found: {manifest_path}")
    rows = read_rows_csv(manifest_path)
    attempts = [_analyze_attempt(row) for row in rows]
    scenario_keys = sorted(
        {
            (str(row.get("flight_mode", "UNKNOWN")).strip().upper() or "UNKNOWN", str(row.get("scenario", "")).strip())
            for row in attempts
            if str(row.get("scenario", "")).strip() and str(row.get("scenario", "")).strip() != "unknown"
        }
    )
    if not scenario_keys:
        raise ValueError("no target-scout scenarios were found in runs_manifest")
    scenario_results = [
        _scenario_result(mode, scenario, [row for row in attempts if row.get("flight_mode") == mode and row.get("scenario") == scenario])
        for mode, scenario in scenario_keys
    ]
    blocking_reasons = [reason for result in scenario_results for reason in result["blocking_reasons"]]
    mode_status = defaultdict(dict)
    for result in scenario_results:
        mode_status[result["flight_mode"]][result["scenario"]] = result["recommended_target"]

    recommended_next_target = "none"
    recommended_next_step = "no_target_signal_identified"
    recommended_mode = "none"
    grouped_by_mode: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for result in scenario_results:
        grouped_by_mode[result["flight_mode"]].append(result)

    for mode, results in grouped_by_mode.items():
        if results and all(result["recommended_target"] == "pair_imbalance_12_vs_34" for result in results):
            recommended_next_target = "pair_imbalance_12_vs_34"
            recommended_next_step = f"{mode.lower()}_pair_target_readiness"
            recommended_mode = mode
            break
    if recommended_next_target == "none":
        for mode, results in grouped_by_mode.items():
            if results and all(result["recommended_target"].startswith("actuator_") for result in results):
                actuator_names = {result["recommended_target"] for result in results}
                if len(actuator_names) == 1:
                    recommended_next_target = next(iter(actuator_names))
                    recommended_next_step = "run_single_actuator_target_readiness"
                    recommended_mode = mode
                    break

    overall_decision = {
        "recommended_next_target": recommended_next_target,
        "recommended_next_step": recommended_next_step,
        "recommended_mode": recommended_mode,
        "mode_status": dict(mode_status),
    }
    study_scope = {
        "backend": "ardupilot",
        "mode_scope": sorted(grouped_by_mode.keys()),
        "x_schema": "commands_only",
        "y_schema": "actuator_response",
        "input_source": "telemetry/input_trace.csv",
        "response_source": "telemetry/bin_rcou.csv",
        "response_focus": [
            "collective_floor_state",
            "pair_imbalance_12_vs_34",
            "single_actuator_floor_state",
        ],
        "floor_threshold": FLOOR_THRESHOLD,
        "pair_split_threshold": PAIR_SPLIT_THRESHOLD,
    }
    payload = {
        "study_scope": study_scope,
        "scenario_results": scenario_results,
        "overall_decision": overall_decision,
        "blocking_reasons": blocking_reasons,
    }

    paths = _output_paths(output_root.expanduser().resolve() if output_root else None)
    report_text = render_ardupilot_a2_target_scout_markdown(payload)
    run_level_rows = []
    for row in attempts:
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
                "run_level_target_scout": _relative_workspace_path(paths["run_level_table_path"]),
                "scenario_target_matrix": _relative_workspace_path(paths["scenario_matrix_path"]),
            },
            "summary": payload,
        },
    )
    return paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Analyze ArduPilot A2 actuator target candidates from existing runs.")
    parser.add_argument("--runs-manifest", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args(argv)

    study_dir = run_ardupilot_a2_target_scout(
        runs_manifest=args.runs_manifest,
        output_root=args.output_root,
    )
    print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
