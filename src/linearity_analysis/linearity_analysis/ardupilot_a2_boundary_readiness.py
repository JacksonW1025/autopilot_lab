from __future__ import annotations

import argparse
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from linearity_core.io import ensure_study_directories, read_rows_csv, write_json, write_rows_csv, write_yaml
from linearity_core.research_contract import manifest_acceptance_state

from .ardupilot_a2_readiness import (
    _bool_as_rate,
    _build_aligned_samples,
    _format_metric,
    _median,
    _read_manifest,
    _relative_workspace_path,
    _safe_float,
    _safe_int,
    _safe_str_list,
)

STUDY_NAME = "ardupilot_a2_stabilize_boundary_readiness"
SCENARIOS = ("nominal", "throttle_biased")
TIERS = ("micro", "probe", "confirm")
BASELINE_PHASES = frozenset({"stabilize", "pulse_gap", "recover"})
ACTIVE_PHASES = frozenset({"pulse_active", "alternating_pulse_active_pos", "alternating_pulse_active_neg"})
FLOOR_THRESHOLD = 0.02
RECOVERY_TOLERANCE = 0.02
ACCEPTED_TARGET = 5
GATE_RATE_MAX = 0.20
FAILSAFE_RATE_MAX = 0.0
MICRO_TRIGGER_RATE_MAX = 0.20
MICRO_FLOOR_HIT_RATE_MAX = 0.10
BASELINE_FALSE_TRIGGER_RATE_MAX = 0.05
PROBE_TRIGGER_RATE_MIN = 0.80
PROBE_FLOOR_HIT_RATE_MIN = 0.30
PROBE_HIT_LATENCY_MAX_MS = 200.0
RECOVERY_RATE_MIN = 0.80
HIT_PATTERN_CONSISTENCY_MIN = 0.70

RUN_LEVEL_FIELDNAMES = [
    "scenario",
    "amplitude_tier",
    "flight_mode",
    "config_key",
    "config_name",
    "run_id",
    "study_name",
    "config_profile",
    "artifact_dir",
    "analysis_status",
    "baseline_command_throttle",
    "baseline_min_actuator",
    "baseline_sample_count",
    "active_sample_count",
    "aligned_sample_count",
    "pulse_count_seen",
    "triggered_pulse_count",
    "pulse_trigger_rate",
    "floor_hit_rate",
    "baseline_false_trigger_rate",
    "median_hit_latency_ms",
    "recovery_rate",
    "hit_pattern_consistency",
    "accepted",
    "failsafe_during_experiment",
    "completion_reason",
    "rejection_reasons",
    "anomaly_summary",
    "status",
    "exit_code",
    "research_acceptance",
]

CONFIG_MATRIX_FIELDNAMES = [
    "scenario",
    "accepted_count",
    "attempt_count",
    "gate_rate",
    "failsafe_rate",
    "threshold_window_present",
    "ready",
    "blocking_reasons",
    "micro_attempt_count",
    "micro_accepted_count",
    "micro_gate_rate",
    "micro_failsafe_rate",
    "micro_median_pulse_trigger_rate",
    "micro_median_floor_hit_rate",
    "micro_median_baseline_false_trigger_rate",
    "micro_median_hit_latency_ms",
    "micro_median_recovery_rate",
    "micro_median_hit_pattern_consistency",
    "probe_attempt_count",
    "probe_accepted_count",
    "probe_gate_rate",
    "probe_failsafe_rate",
    "probe_median_pulse_trigger_rate",
    "probe_median_floor_hit_rate",
    "probe_median_baseline_false_trigger_rate",
    "probe_median_hit_latency_ms",
    "probe_median_recovery_rate",
    "probe_median_hit_pattern_consistency",
    "confirm_attempt_count",
    "confirm_accepted_count",
    "confirm_gate_rate",
    "confirm_failsafe_rate",
    "confirm_median_pulse_trigger_rate",
    "confirm_median_floor_hit_rate",
    "confirm_median_baseline_false_trigger_rate",
    "confirm_median_hit_latency_ms",
    "confirm_median_recovery_rate",
    "confirm_median_hit_pattern_consistency",
]


def _output_paths(output_root: Path | None) -> dict[str, Path]:
    study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_{STUDY_NAME}"
    paths = ensure_study_directories(study_id, root=output_root)
    tables_dir = paths["base_dir"] / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    return {
        **paths,
        "tables_dir": tables_dir,
        "manifest_path": paths["base_dir"] / "manifest.yaml",
        "report_path": paths["reports_dir"] / "a2_boundary_readiness.md",
        "summary_path": paths["summary_dir"] / "a2_boundary_readiness.json",
        "run_level_table_path": tables_dir / "run_level_boundary_effects.csv",
        "config_matrix_path": tables_dir / "config_threshold_matrix.csv",
    }


def _scenario_tier_from_text(text: str) -> tuple[str, str] | None:
    normalized = str(text).strip().lower().replace(".yaml", "")
    for scenario in SCENARIOS:
        for tier in TIERS:
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
    if str(manifest.get("scenario", "")) in SCENARIOS and str(extras.get("amplitude_tier", "")) in TIERS:
        return str(manifest.get("scenario", "")), str(extras.get("amplitude_tier", ""))
    raise ValueError(f"unable to infer boundary readiness scenario/tier from row={row.get('config', '')!r}")


def _flight_mode_from_manifest(manifest: dict[str, Any]) -> str:
    study_config = manifest.get("study_config", {}) or {}
    if isinstance(study_config, dict):
        candidate = str(study_config.get("flight_mode", "")).strip().upper()
        if candidate:
            return candidate
    candidate = str(manifest.get("flight_mode", "")).strip().upper()
    return candidate or "UNKNOWN"


def _segment_active_pulses(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    current_phase = ""
    current_start = -1
    current_rows: list[dict[str, Any]] = []
    for index, row in enumerate(samples):
        phase = str(row.get("phase", ""))
        if phase not in ACTIVE_PHASES:
            if current_rows:
                segments.append(
                    {
                        "phase": current_phase,
                        "rows": list(current_rows),
                        "start_index": current_start,
                        "end_index": index - 1,
                    }
                )
                current_rows = []
                current_phase = ""
                current_start = -1
            continue
        if current_rows and phase != current_phase:
            segments.append(
                {
                    "phase": current_phase,
                    "rows": list(current_rows),
                    "start_index": current_start,
                    "end_index": index - 1,
                }
            )
            current_rows = []
            current_start = -1
        if current_start < 0:
            current_start = index
        current_phase = phase
        current_rows.append(row)
    if current_rows:
        segments.append(
            {
                "phase": current_phase,
                "rows": list(current_rows),
                "start_index": current_start,
                "end_index": len(samples) - 1,
            }
        )
    return segments


def _pulse_recovery_rows(samples: list[dict[str, Any]], segment: dict[str, Any], next_start: int | None) -> list[dict[str, Any]]:
    start_index = int(segment["end_index"]) + 1
    end_index = next_start if next_start is not None else len(samples)
    rows: list[dict[str, Any]] = []
    for row in samples[start_index:end_index]:
        if str(row.get("phase", "")) not in BASELINE_PHASES:
            continue
        if math.isfinite(_safe_float(row.get("a_min"))):
            rows.append(row)
    return rows


def _floor_pattern(rows: list[dict[str, Any]]) -> tuple[int, int, int, int]:
    pattern: list[int] = []
    for actuator_index in range(1, 5):
        hit = any(_safe_float(row.get(f"actuator_{actuator_index}")) <= FLOOR_THRESHOLD for row in rows)
        pattern.append(1 if hit else 0)
    return tuple(pattern)  # type: ignore[return-value]


def _compute_run_boundary_metrics(samples: list[dict[str, Any]]) -> dict[str, Any]:
    baseline_rows = [
        row
        for row in samples
        if str(row.get("phase", "")) in BASELINE_PHASES
        and all(math.isfinite(_safe_float(row.get(f"actuator_{index}"))) for index in range(1, 5))
    ]
    if not baseline_rows:
        return {
            "analysis_status": "baseline_unavailable",
            "baseline_command_throttle": math.nan,
            "baseline_min_actuator": math.nan,
            "baseline_sample_count": 0,
            "active_sample_count": 0,
            "aligned_sample_count": 0,
            "pulse_count_seen": 0,
            "triggered_pulse_count": 0,
            "pulse_trigger_rate": math.nan,
            "floor_hit_rate": math.nan,
            "baseline_false_trigger_rate": math.nan,
            "median_hit_latency_ms": math.nan,
            "recovery_rate": math.nan,
            "hit_pattern_consistency": math.nan,
        }

    baseline_command = _median([_safe_float(row.get("command_throttle")) for row in baseline_rows])
    baseline_min_actuator = _median(
        [min(_safe_float(row.get(f"actuator_{index}")) for index in range(1, 5)) for row in baseline_rows]
    )

    aligned_sample_count = 0
    active_sample_count = 0
    for row in samples:
        actuator_values = [_safe_float(row.get(f"actuator_{index}")) for index in range(1, 5)]
        if all(math.isfinite(value) for value in actuator_values):
            a_min = min(actuator_values)
            aligned_sample_count += 1
        else:
            a_min = math.nan
        row["a_min"] = a_min
        row["delta_u"] = _safe_float(row.get("command_throttle")) - baseline_command if math.isfinite(baseline_command) else math.nan
        row["floor_hit"] = bool(math.isfinite(a_min) and a_min <= FLOOR_THRESHOLD)
        row["near_baseline"] = bool(math.isfinite(a_min) and math.isfinite(baseline_min_actuator) and abs(a_min - baseline_min_actuator) <= RECOVERY_TOLERANCE)
        if str(row.get("phase", "")) in ACTIVE_PHASES and math.isfinite(a_min):
            active_sample_count += 1

    baseline_false_trigger_rate = _bool_as_rate(
        sum(1 for row in baseline_rows if bool(row.get("floor_hit"))),
        len(baseline_rows),
    )
    active_rows = [row for row in samples if str(row.get("phase", "")) in ACTIVE_PHASES and math.isfinite(_safe_float(row.get("a_min")))]
    floor_hit_rate = _bool_as_rate(sum(1 for row in active_rows if bool(row.get("floor_hit"))), len(active_rows))

    segments = _segment_active_pulses(samples)
    hit_latencies_ms: list[float] = []
    recovery_rates: list[float] = []
    triggered_patterns: list[tuple[int, int, int, int]] = []
    triggered_pulse_count = 0
    for index, segment in enumerate(segments):
        rows = segment["rows"]
        pulse_trigger = any(bool(row.get("floor_hit")) for row in rows)
        segment["pulse_trigger"] = pulse_trigger
        if pulse_trigger:
            triggered_pulse_count += 1
            first_trigger = next(row for row in rows if bool(row.get("floor_hit")))
            hit_latency_ms = (
                _safe_int(first_trigger.get("publish_time_ns")) - _safe_int(rows[0].get("publish_time_ns"))
            ) / 1_000_000.0
            hit_latencies_ms.append(float(hit_latency_ms))
            triggered_patterns.append(_floor_pattern(rows))
        next_start = int(segments[index + 1]["start_index"]) if index + 1 < len(segments) else None
        recovery_rows = _pulse_recovery_rows(samples, segment, next_start)
        if recovery_rows:
            recovery_rates.append(
                float(
                    sum(1 for row in recovery_rows if bool(row.get("near_baseline")))
                    / max(len(recovery_rows), 1)
                )
            )

    pattern_consistency = math.nan
    if triggered_patterns:
        most_common_count = Counter(triggered_patterns).most_common(1)[0][1]
        pattern_consistency = float(most_common_count / len(triggered_patterns))

    return {
        "analysis_status": "ok" if segments else "active_pulses_unavailable",
        "baseline_command_throttle": baseline_command,
        "baseline_min_actuator": baseline_min_actuator,
        "baseline_sample_count": len(baseline_rows),
        "active_sample_count": active_sample_count,
        "aligned_sample_count": aligned_sample_count,
        "pulse_count_seen": len(segments),
        "triggered_pulse_count": triggered_pulse_count,
        "pulse_trigger_rate": _bool_as_rate(triggered_pulse_count, len(segments)),
        "floor_hit_rate": floor_hit_rate,
        "baseline_false_trigger_rate": baseline_false_trigger_rate,
        "median_hit_latency_ms": _median(hit_latencies_ms),
        "recovery_rate": _median(recovery_rates),
        "hit_pattern_consistency": pattern_consistency,
    }


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
        "scenario": scenario,
        "amplitude_tier": tier,
        "flight_mode": _flight_mode_from_manifest(manifest) if manifest else "UNKNOWN",
        "config_key": f"{scenario}-{tier}" if scenario in SCENARIOS and tier in TIERS else "unknown",
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
        "baseline_command_throttle": math.nan,
        "baseline_min_actuator": math.nan,
        "baseline_sample_count": 0,
        "active_sample_count": 0,
        "aligned_sample_count": 0,
        "pulse_count_seen": 0,
        "triggered_pulse_count": 0,
        "pulse_trigger_rate": math.nan,
        "floor_hit_rate": math.nan,
        "baseline_false_trigger_rate": math.nan,
        "median_hit_latency_ms": math.nan,
        "recovery_rate": math.nan,
        "hit_pattern_consistency": math.nan,
    }
    if artifact_dir is None or not artifact_dir.exists() or not manifest:
        return attempt
    samples = _build_aligned_samples(artifact_dir, manifest)
    if not samples:
        attempt["analysis_status"] = "telemetry_unavailable"
        return attempt
    attempt.update(_compute_run_boundary_metrics(samples))
    return attempt


def _tier_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    attempt_count = len(rows)
    accepted_rows = [row for row in rows if bool(row.get("accepted"))]
    gate_count = sum(1 for row in rows if not bool(row.get("accepted")) and not bool(row.get("failsafe_during_experiment")))
    failsafe_count = sum(1 for row in rows if bool(row.get("failsafe_during_experiment")))
    return {
        "attempt_count": attempt_count,
        "accepted_count": len(accepted_rows),
        "gate_rate": _bool_as_rate(gate_count, attempt_count),
        "failsafe_rate": _bool_as_rate(failsafe_count, attempt_count),
        "median_pulse_trigger_rate": _median([_safe_float(row.get("pulse_trigger_rate")) for row in accepted_rows]),
        "median_floor_hit_rate": _median([_safe_float(row.get("floor_hit_rate")) for row in accepted_rows]),
        "median_baseline_false_trigger_rate": _median([_safe_float(row.get("baseline_false_trigger_rate")) for row in accepted_rows]),
        "median_hit_latency_ms": _median([_safe_float(row.get("median_hit_latency_ms")) for row in accepted_rows]),
        "median_recovery_rate": _median([_safe_float(row.get("recovery_rate")) for row in accepted_rows]),
        "median_hit_pattern_consistency": _median([_safe_float(row.get("hit_pattern_consistency")) for row in accepted_rows]),
    }


def _append_tier_blockers(scenario: str, tier: str, tier_result: dict[str, Any], blocking_reasons: list[str]) -> None:
    accepted_count = int(tier_result["accepted_count"])
    gate_rate = _safe_float(tier_result["gate_rate"])
    failsafe_rate = _safe_float(tier_result["failsafe_rate"])
    if accepted_count < ACCEPTED_TARGET:
        blocking_reasons.append(f"{scenario}_{tier}_accepted_target_not_met")
    if not math.isfinite(gate_rate) or gate_rate > GATE_RATE_MAX:
        blocking_reasons.append(f"{scenario}_{tier}_gate_rate_above_threshold")
    if not math.isfinite(failsafe_rate) or failsafe_rate > FAILSAFE_RATE_MAX:
        blocking_reasons.append(f"{scenario}_{tier}_failsafe_rate_above_threshold")


def _scenario_summary(scenario: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    tier_rows = {tier: [row for row in rows if str(row.get("amplitude_tier", "")) == tier] for tier in TIERS}
    tier_results = {tier: _tier_summary(tier_rows[tier]) for tier in TIERS}
    attempt_count = len(rows)
    gate_count = sum(1 for row in rows if not bool(row.get("accepted")) and not bool(row.get("failsafe_during_experiment")))
    failsafe_count = sum(1 for row in rows if bool(row.get("failsafe_during_experiment")))

    blocking_reasons: list[str] = []
    for tier in TIERS:
        _append_tier_blockers(scenario, tier, tier_results[tier], blocking_reasons)

    micro = tier_results["micro"]
    probe = tier_results["probe"]
    confirm = tier_results["confirm"]

    micro_trigger = _safe_float(micro["median_pulse_trigger_rate"])
    micro_floor = _safe_float(micro["median_floor_hit_rate"])
    micro_false = _safe_float(micro["median_baseline_false_trigger_rate"])
    probe_trigger = _safe_float(probe["median_pulse_trigger_rate"])
    probe_floor = _safe_float(probe["median_floor_hit_rate"])
    probe_latency = _safe_float(probe["median_hit_latency_ms"])
    probe_recovery = _safe_float(probe["median_recovery_rate"])
    probe_consistency = _safe_float(probe["median_hit_pattern_consistency"])
    confirm_trigger = _safe_float(confirm["median_pulse_trigger_rate"])
    confirm_floor = _safe_float(confirm["median_floor_hit_rate"])
    confirm_recovery = _safe_float(confirm["median_recovery_rate"])
    confirm_consistency = _safe_float(confirm["median_hit_pattern_consistency"])

    micro_nontrigger = (
        math.isfinite(micro_trigger)
        and micro_trigger <= MICRO_TRIGGER_RATE_MAX
        and math.isfinite(micro_floor)
        and micro_floor <= MICRO_FLOOR_HIT_RATE_MAX
        and math.isfinite(micro_false)
        and micro_false <= BASELINE_FALSE_TRIGGER_RATE_MAX
    )
    probe_trigger_ready = (
        math.isfinite(probe_trigger)
        and probe_trigger >= PROBE_TRIGGER_RATE_MIN
        and math.isfinite(probe_floor)
        and probe_floor >= PROBE_FLOOR_HIT_RATE_MIN
        and math.isfinite(probe_latency)
        and probe_latency <= PROBE_HIT_LATENCY_MAX_MS
        and math.isfinite(probe_recovery)
        and probe_recovery >= RECOVERY_RATE_MIN
        and math.isfinite(probe_consistency)
        and probe_consistency >= HIT_PATTERN_CONSISTENCY_MIN
    )
    confirm_ready = (
        math.isfinite(confirm_trigger)
        and math.isfinite(probe_trigger)
        and confirm_trigger >= probe_trigger
        and math.isfinite(confirm_floor)
        and math.isfinite(probe_floor)
        and confirm_floor >= probe_floor
        and math.isfinite(confirm_recovery)
        and confirm_recovery >= RECOVERY_RATE_MIN
        and math.isfinite(confirm_consistency)
        and confirm_consistency >= HIT_PATTERN_CONSISTENCY_MIN
    )
    threshold_window_present = micro_nontrigger and probe_trigger_ready

    if not math.isfinite(micro_trigger) or micro_trigger > MICRO_TRIGGER_RATE_MAX:
        blocking_reasons.append(f"{scenario}_micro_trigger_rate_above_ceiling")
    if not math.isfinite(micro_floor) or micro_floor > MICRO_FLOOR_HIT_RATE_MAX:
        blocking_reasons.append(f"{scenario}_micro_floor_hit_rate_above_ceiling")
    if not math.isfinite(micro_false) or micro_false > BASELINE_FALSE_TRIGGER_RATE_MAX:
        blocking_reasons.append(f"{scenario}_micro_baseline_false_trigger_rate_above_ceiling")
    if not math.isfinite(probe_trigger) or probe_trigger < PROBE_TRIGGER_RATE_MIN:
        blocking_reasons.append(f"{scenario}_probe_trigger_rate_below_floor")
    if not math.isfinite(probe_floor) or probe_floor < PROBE_FLOOR_HIT_RATE_MIN:
        blocking_reasons.append(f"{scenario}_probe_floor_hit_rate_below_floor")
    if not math.isfinite(probe_latency) or probe_latency > PROBE_HIT_LATENCY_MAX_MS:
        blocking_reasons.append(f"{scenario}_probe_hit_latency_above_ceiling")
    if not math.isfinite(probe_recovery) or probe_recovery < RECOVERY_RATE_MIN:
        blocking_reasons.append(f"{scenario}_probe_recovery_rate_below_floor")
    if not math.isfinite(probe_consistency) or probe_consistency < HIT_PATTERN_CONSISTENCY_MIN:
        blocking_reasons.append(f"{scenario}_probe_hit_pattern_consistency_below_floor")
    if not math.isfinite(confirm_trigger) or not math.isfinite(probe_trigger) or confirm_trigger < probe_trigger:
        blocking_reasons.append(f"{scenario}_confirm_trigger_rate_regressed")
    if not math.isfinite(confirm_floor) or not math.isfinite(probe_floor) or confirm_floor < probe_floor:
        blocking_reasons.append(f"{scenario}_confirm_floor_hit_rate_regressed")
    if not math.isfinite(confirm_recovery) or confirm_recovery < RECOVERY_RATE_MIN:
        blocking_reasons.append(f"{scenario}_confirm_recovery_rate_below_floor")
    if not math.isfinite(confirm_consistency) or confirm_consistency < HIT_PATTERN_CONSISTENCY_MIN:
        blocking_reasons.append(f"{scenario}_confirm_hit_pattern_consistency_below_floor")

    accepted_count = min(int(tier_results[tier]["accepted_count"]) for tier in TIERS)
    return {
        "scenario": scenario,
        "accepted_count": accepted_count,
        "attempt_count": attempt_count,
        "gate_rate": _bool_as_rate(gate_count, attempt_count),
        "failsafe_rate": _bool_as_rate(failsafe_count, attempt_count),
        "threshold_window_present": threshold_window_present,
        "ready": not blocking_reasons,
        "blocking_reasons": blocking_reasons,
        "tiers": tier_results,
    }


def _flatten_config_row(result: dict[str, Any]) -> dict[str, Any]:
    row = {
        "scenario": result["scenario"],
        "accepted_count": result["accepted_count"],
        "attempt_count": result["attempt_count"],
        "gate_rate": result["gate_rate"],
        "failsafe_rate": result["failsafe_rate"],
        "threshold_window_present": result["threshold_window_present"],
        "ready": result["ready"],
        "blocking_reasons": ",".join(result["blocking_reasons"]),
    }
    for tier in TIERS:
        tier_result = result["tiers"][tier]
        row[f"{tier}_attempt_count"] = tier_result["attempt_count"]
        row[f"{tier}_accepted_count"] = tier_result["accepted_count"]
        row[f"{tier}_gate_rate"] = tier_result["gate_rate"]
        row[f"{tier}_failsafe_rate"] = tier_result["failsafe_rate"]
        row[f"{tier}_median_pulse_trigger_rate"] = tier_result["median_pulse_trigger_rate"]
        row[f"{tier}_median_floor_hit_rate"] = tier_result["median_floor_hit_rate"]
        row[f"{tier}_median_baseline_false_trigger_rate"] = tier_result["median_baseline_false_trigger_rate"]
        row[f"{tier}_median_hit_latency_ms"] = tier_result["median_hit_latency_ms"]
        row[f"{tier}_median_recovery_rate"] = tier_result["median_recovery_rate"]
        row[f"{tier}_median_hit_pattern_consistency"] = tier_result["median_hit_pattern_consistency"]
    return row


def render_ardupilot_a2_boundary_readiness_markdown(payload: dict[str, Any]) -> str:
    overall = payload["overall_decision"]
    mode_scope = payload.get("study_scope", {}).get("mode_scope", [])
    mode_label = ", ".join(mode_scope) if mode_scope else "UNKNOWN"
    lines = [
        f"# ArduPilot A2 Boundary Readiness ({mode_label})",
        "",
        f"- ready_for_binary_attack_v1: {'yes' if overall['ready_for_binary_attack_v1'] else 'no'}",
        f"- recommended_path: {overall['recommended_path']}",
        f"- blocking_reasons: {', '.join(payload['blocking_reasons']) if payload['blocking_reasons'] else 'none'}",
        "",
        "## Scenario Matrix",
        "",
        "| scenario | ready | threshold_window_present | accepted_count | attempt_count | failsafe_rate | gate_rate |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in payload["config_results"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    result["scenario"],
                    _format_metric(result["ready"]),
                    _format_metric(result["threshold_window_present"]),
                    str(result["accepted_count"]),
                    str(result["attempt_count"]),
                    _format_metric(result["failsafe_rate"]),
                    _format_metric(result["gate_rate"]),
                ]
            )
            + " |"
        )
    lines.append("")
    for result in payload["config_results"]:
        lines.append(f"## {result['scenario']}")
        lines.append("")
        lines.append(f"- ready: {'yes' if result['ready'] else 'no'}")
        lines.append(f"- threshold_window_present: {'yes' if result['threshold_window_present'] else 'no'}")
        lines.append(f"- blocking_reasons: {', '.join(result['blocking_reasons']) if result['blocking_reasons'] else 'none'}")
        for tier in TIERS:
            tier_result = result["tiers"][tier]
            lines.append(
                f"- {tier}: accepted={tier_result['accepted_count']}, "
                f"trigger_rate={_format_metric(tier_result['median_pulse_trigger_rate'])}, "
                f"floor_hit_rate={_format_metric(tier_result['median_floor_hit_rate'])}, "
                f"baseline_false_trigger_rate={_format_metric(tier_result['median_baseline_false_trigger_rate'])}, "
                f"hit_latency_ms={_format_metric(tier_result['median_hit_latency_ms'])}, "
                f"recovery_rate={_format_metric(tier_result['median_recovery_rate'])}, "
                f"pattern_consistency={_format_metric(tier_result['median_hit_pattern_consistency'])}"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run_ardupilot_a2_boundary_readiness(
    *,
    runs_manifest: Path,
    output_root: Path | None = None,
) -> Path:
    manifest_path = runs_manifest.expanduser().resolve()
    if not manifest_path.exists():
        raise FileNotFoundError(f"runs_manifest not found: {manifest_path}")
    rows = read_rows_csv(manifest_path)
    attempts = [_analyze_attempt(row) for row in rows]
    scenarios_evaluated = [scenario for scenario in SCENARIOS if any(str(row.get("scenario", "")) == scenario for row in attempts)]
    if not scenarios_evaluated:
        raise ValueError("no boundary readiness scenarios were found in runs_manifest")
    mode_scope = sorted({str(row.get("flight_mode", "UNKNOWN")).strip().upper() or "UNKNOWN" for row in attempts})
    config_results = [_scenario_summary(scenario, [row for row in attempts if row.get("scenario") == scenario]) for scenario in scenarios_evaluated]
    blocking_reasons = [reason for result in config_results for reason in result["blocking_reasons"]]
    ready_for_binary_attack_v1 = all(result["ready"] for result in config_results)
    boundary_pinned = [
        result["scenario"]
        for result in config_results
        if (
            math.isfinite(_safe_float(result["tiers"]["micro"]["median_pulse_trigger_rate"]))
            and _safe_float(result["tiers"]["micro"]["median_pulse_trigger_rate"]) > MICRO_TRIGGER_RATE_MAX
        )
        or (
            math.isfinite(_safe_float(result["tiers"]["micro"]["median_floor_hit_rate"]))
            and _safe_float(result["tiers"]["micro"]["median_floor_hit_rate"]) > MICRO_FLOOR_HIT_RATE_MAX
        )
        or (
            math.isfinite(_safe_float(result["tiers"]["micro"]["median_baseline_false_trigger_rate"]))
            and _safe_float(result["tiers"]["micro"]["median_baseline_false_trigger_rate"]) > BASELINE_FALSE_TRIGGER_RATE_MAX
        )
    ]
    recommended_path = "start_ardupilot_a2_binary_attack_v1" if ready_for_binary_attack_v1 else "iterate_boundary_protocol_only"
    if boundary_pinned and all(not bool(result["threshold_window_present"]) for result in config_results) and not ready_for_binary_attack_v1:
        recommended_path = "change_target_or_regime"
    overall_decision = {
        "ready_for_binary_attack_v1": ready_for_binary_attack_v1,
        "recommended_path": recommended_path,
        "scenario_status": {result["scenario"]: result["ready"] for result in config_results},
    }
    study_scope = {
        "backend": "ardupilot",
        "mode_scope": mode_scope,
        "x_schema": "commands_only",
        "y_schema": "actuator_response",
        "input_source": "telemetry/input_trace.csv",
        "response_source": "telemetry/bin_rcou.csv",
        "response_focus": "min(actuator_1..4)",
        "profile_type": "pulse_train",
        "scenario_scope": scenarios_evaluated,
        "tier_scope": list(TIERS),
        "accepted_target_per_config": ACCEPTED_TARGET,
        "max_attempts_per_config": 10,
    }
    floor_definition = {
        "normalized_pwm": "clamp((pwm - 1000) / 1000, 0, 1)",
        "floor_signal": "a_min = min(actuator_1..4)",
        "floor_threshold": FLOOR_THRESHOLD,
        "floor_hit_definition": f"a_min <= {FLOOR_THRESHOLD:.2f}",
        "recovery_tolerance": RECOVERY_TOLERANCE,
        "recovery_definition": f"abs(a_min - baseline_min_actuator) <= {RECOVERY_TOLERANCE:.2f}",
    }
    payload = {
        "study_scope": study_scope,
        "floor_definition": floor_definition,
        "config_results": config_results,
        "overall_decision": overall_decision,
        "blocking_reasons": blocking_reasons,
    }

    paths = _output_paths(output_root.expanduser().resolve() if output_root else None)
    report_text = render_ardupilot_a2_boundary_readiness_markdown(payload)
    run_level_rows = []
    for row in attempts:
        normalized = {key: row.get(key, "") for key in RUN_LEVEL_FIELDNAMES}
        normalized["rejection_reasons"] = ",".join(_safe_str_list(normalized.get("rejection_reasons")))
        normalized["anomaly_summary"] = ",".join(_safe_str_list(normalized.get("anomaly_summary")))
        run_level_rows.append(normalized)
    config_matrix_rows = [_flatten_config_row(result) for result in config_results]

    paths["report_path"].write_text(report_text, encoding="utf-8")
    write_json(paths["summary_path"], payload)
    write_rows_csv(paths["run_level_table_path"], run_level_rows, fieldnames=RUN_LEVEL_FIELDNAMES)
    write_rows_csv(paths["config_matrix_path"], config_matrix_rows, fieldnames=CONFIG_MATRIX_FIELDNAMES)
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
                "run_level_boundary_effects": _relative_workspace_path(paths["run_level_table_path"]),
                "config_threshold_matrix": _relative_workspace_path(paths["config_matrix_path"]),
            },
            "summary": payload,
        },
    )
    return paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Analyze narrow ArduPilot A2 boundary readiness runs.")
    parser.add_argument("--runs-manifest", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args(argv)

    study_dir = run_ardupilot_a2_boundary_readiness(
        runs_manifest=args.runs_manifest,
        output_root=args.output_root,
    )
    print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
