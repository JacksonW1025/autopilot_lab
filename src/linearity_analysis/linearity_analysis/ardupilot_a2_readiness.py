from __future__ import annotations

import argparse
import bisect
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from linearity_core.io import ensure_study_directories, read_rows_csv, read_yaml, write_json, write_rows_csv, write_yaml
from linearity_core.paths import STUDY_ARTIFACT_ROOT, WORKSPACE_ROOT
from linearity_core.research_contract import manifest_acceptance_state

from .matrix_gallery import load_matrix_csv

STUDY_NAME = "ardupilot_a2_stabilize_readiness"
DEFAULT_A2_BASELINE_STUDY = STUDY_ARTIFACT_ROOT / "20260413_070802_ardupilot_real_generalization_ablation"
BASELINE_COMBO_PATH = Path("fits/commands_only__actuator_response__pooled/ridge_affine/matrix_f.csv")
SCENARIOS = ("nominal", "proxy_dynamic", "throttle_biased")
TIERS = ("small", "medium")
BASELINE_PHASES = frozenset({"stabilize", "pulse_gap", "recover"})
ACTIVE_PHASES = frozenset({"pulse_active", "alternating_pulse_active_pos", "alternating_pulse_active_neg"})
BIN_TIME_FILES = (
    "bin_att.csv",
    "bin_rate.csv",
    "bin_motb.csv",
    "bin_rcou.csv",
    "bin_pos.csv",
    "bin_ahr2.csv",
    "bin_bat.csv",
    "bin_mode.csv",
    "bin_orgn.csv",
)
RUN_LEVEL_FIELDNAMES = [
    "scenario",
    "amplitude_tier",
    "config_key",
    "config_name",
    "run_id",
    "study_name",
    "config_profile",
    "artifact_dir",
    "analysis_status",
    "baseline_command_throttle",
    "baseline_actuator_1",
    "baseline_actuator_2",
    "baseline_actuator_3",
    "baseline_actuator_4",
    "baseline_sample_count",
    "active_sample_count",
    "aligned_sample_count",
    "pulse_count_seen",
    "mean_delta_actuator_pos",
    "mean_delta_actuator_neg",
    "effect_abs_median",
    "slope_median",
    "slope_abs_median",
    "baseline_noise_mad",
    "snr",
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
    "direction_consistency",
    "predictability_cv",
    "small_tier_above_noise",
    "monotonicity",
    "profile_not_completed_rate",
    "ready",
    "blocking_reasons",
    "small_attempt_count",
    "small_accepted_count",
    "small_gate_rate",
    "small_failsafe_rate",
    "small_direction_consistency",
    "small_predictability_cv",
    "small_median_snr",
    "small_median_effect_abs",
    "small_median_slope_abs",
    "medium_attempt_count",
    "medium_accepted_count",
    "medium_gate_rate",
    "medium_failsafe_rate",
    "medium_direction_consistency",
    "medium_predictability_cv",
    "medium_median_snr",
    "medium_median_effect_abs",
    "medium_median_slope_abs",
]


def _safe_float(value: Any, default: float = math.nan) -> float:
    if value in ("", None):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    if value in ("", None):
        return default
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _safe_str_list(value: Any) -> list[str]:
    if value in ("", None):
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    return [str(value)]


def _normalize_pwm(value: float) -> float:
    if math.isnan(value):
        return value
    return max(0.0, min(1.0, (value - 1000.0) / 1000.0))


def _finite_values(values: list[float]) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    return array[np.isfinite(array)]


def _median(values: list[float]) -> float:
    finite = _finite_values(values)
    if finite.size == 0:
        return math.nan
    return float(np.median(finite))


def _mad(values: list[float]) -> float:
    finite = _finite_values(values)
    if finite.size == 0:
        return math.nan
    center = float(np.median(finite))
    return float(np.median(np.abs(finite - center)))


def _bool_as_rate(count: int, total: int) -> float:
    if total <= 0:
        return math.nan
    return float(count / total)


def _sign(value: float) -> int:
    if not math.isfinite(value) or abs(value) <= 1e-12:
        return 0
    return -1 if value < 0.0 else 1


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
    study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_{STUDY_NAME}"
    paths = ensure_study_directories(study_id, root=output_root)
    tables_dir = paths["base_dir"] / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    return {
        **paths,
        "tables_dir": tables_dir,
        "manifest_path": paths["base_dir"] / "manifest.yaml",
        "report_path": paths["reports_dir"] / "a2_readiness.md",
        "summary_path": paths["summary_dir"] / "a2_readiness.json",
        "run_level_table_path": tables_dir / "run_level_effects.csv",
        "config_matrix_path": tables_dir / "config_readiness_matrix.csv",
    }


def _scenario_tier_from_text(text: str) -> tuple[str, str] | None:
    normalized = str(text).strip().lower().replace(".yaml", "")
    for scenario in SCENARIOS:
        for tier in TIERS:
            token = f"{scenario}_{tier}"
            if token in normalized:
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
    raise ValueError(f"unable to infer readiness scenario/tier from row={row.get('config', '')!r}")


def _load_baseline_sign_reference(study_dir: Path) -> dict[str, Any]:
    resolved_dir = _prefer_workspace_study_path(study_dir)
    matrix_path = resolved_dir / BASELINE_COMBO_PATH
    matrix = load_matrix_csv(matrix_path)
    try:
        feature_index = matrix.feature_names.index("command_throttle")
    except ValueError as exc:
        raise ValueError(f"command_throttle row missing in {matrix_path}") from exc
    actuator_columns = [matrix.response_names.index(f"actuator_{index}") for index in range(1, 5)]
    weight_values = [float(matrix.values[feature_index, column_index]) for column_index in actuator_columns]
    mean_weight = float(np.mean(weight_values))
    sign_value = _sign(mean_weight)
    if sign_value == 0:
        raise ValueError(f"sign_ref is zero in {matrix_path}")
    return {
        "sign": sign_value,
        "mean_weight": mean_weight,
        "weights": {f"actuator_{index}": value for index, value in enumerate(weight_values, start=1)},
        "source_study_dir": str(resolved_dir),
        "source_matrix_path": str(matrix_path),
        "combo": "commands_only | actuator_response | ridge_affine | pooled",
    }


def _read_manifest(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    return read_yaml(path)


def _bin_global_start_ns(telemetry_dir: Path) -> int | None:
    candidates: list[int] = []
    for filename in BIN_TIME_FILES:
        rows = read_rows_csv(telemetry_dir / filename)
        if not rows:
            continue
        times = [_safe_int(row.get("received_time_ns"), 0) for row in rows]
        positive = [value for value in times if value > 0]
        if positive:
            candidates.append(min(positive))
    if not candidates:
        return None
    return min(candidates)


def _nearest_aligned_row(
    rows: list[dict[str, Any]],
    times: list[int],
    target_ns: int,
) -> tuple[dict[str, Any] | None, int | None]:
    if not rows:
        return None, None
    index = bisect.bisect_left(times, target_ns)
    candidates: list[dict[str, Any]] = []
    if index < len(rows):
        candidates.append(rows[index])
    if index > 0:
        candidates.append(rows[index - 1])
    if not candidates:
        return None, None
    selected = min(candidates, key=lambda row: abs(_safe_int(row.get("aligned_time_ns"), 0) - target_ns))
    delta_ns = abs(_safe_int(selected.get("aligned_time_ns"), 0) - target_ns)
    return selected, delta_ns


def _build_aligned_samples(run_dir: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    telemetry_dir = run_dir / "telemetry"
    input_rows = read_rows_csv(telemetry_dir / "input_trace.csv")
    if not input_rows:
        return []
    input_rows.sort(key=lambda row: _safe_int(row.get("publish_time_ns"), 0))
    bin_start_ns = _bin_global_start_ns(telemetry_dir)
    if bin_start_ns is None:
        return []
    anchor_time_ns = _safe_int(input_rows[0].get("publish_time_ns"), 0)
    if anchor_time_ns <= 0:
        return []
    actuator_rows = read_rows_csv(telemetry_dir / "bin_rcou.csv")
    actuator_rows.sort(key=lambda row: _safe_int(row.get("received_time_ns"), 0))
    aligned_rows: list[dict[str, Any]] = []
    for row in actuator_rows:
        received_time_ns = _safe_int(row.get("received_time_ns"), 0)
        aligned_rows.append(
            {
                **row,
                "aligned_time_ns": anchor_time_ns + max(0, received_time_ns - bin_start_ns),
            }
        )
    aligned_times = [_safe_int(row.get("aligned_time_ns"), 0) for row in aligned_rows]
    study_config = manifest.get("study_config", {}) or {}
    reporting = study_config.get("reporting", {}) if isinstance(study_config, dict) else {}
    max_alignment_error_ns = int(float(reporting.get("max_alignment_error_ms", 150.0)) * 1_000_000.0)

    samples: list[dict[str, Any]] = []
    for row in input_rows:
        timestamp_ns = _safe_int(row.get("publish_time_ns"), 0)
        actuator_row, alignment_ns = _nearest_aligned_row(aligned_rows, aligned_times, timestamp_ns)
        within_window = actuator_row is not None and alignment_ns is not None and alignment_ns <= max_alignment_error_ns
        sample = {
            "publish_time_ns": timestamp_ns,
            "phase": str(row.get("phase", "")),
            "command_throttle": _safe_float(row.get("command_throttle")),
            "quality_alignment_actuator_ns": float(alignment_ns) if alignment_ns is not None else math.nan,
        }
        for actuator_index in range(1, 5):
            value = _safe_float(actuator_row.get(f"c{actuator_index}") if within_window else None)
            sample[f"actuator_{actuator_index}"] = _normalize_pwm(value)
        samples.append(sample)
    return samples


def _segment_active_pulses(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    current_phase = ""
    current_rows: list[dict[str, Any]] = []
    for row in samples:
        phase = str(row.get("phase", ""))
        if phase not in ACTIVE_PHASES:
            if current_rows:
                segments.append({"phase": current_phase, "rows": list(current_rows)})
                current_rows = []
                current_phase = ""
            continue
        if current_rows and phase != current_phase:
            segments.append({"phase": current_phase, "rows": list(current_rows)})
            current_rows = []
        current_phase = phase
        current_rows.append(row)
    if current_rows:
        segments.append({"phase": current_phase, "rows": list(current_rows)})
    return segments


def _compute_run_effect_metrics(samples: list[dict[str, Any]]) -> dict[str, Any]:
    baseline_rows = [
        row
        for row in samples
        if str(row.get("phase", "")) in BASELINE_PHASES and all(math.isfinite(_safe_float(row.get(f"actuator_{index}"))) for index in range(1, 5))
    ]
    if not baseline_rows:
        return {
            "analysis_status": "baseline_unavailable",
            "baseline_command_throttle": math.nan,
            "baseline_actuator_1": math.nan,
            "baseline_actuator_2": math.nan,
            "baseline_actuator_3": math.nan,
            "baseline_actuator_4": math.nan,
            "baseline_sample_count": 0,
            "active_sample_count": 0,
            "aligned_sample_count": 0,
            "pulse_count_seen": 0,
            "mean_delta_actuator_pos": math.nan,
            "mean_delta_actuator_neg": math.nan,
            "effect_abs_median": math.nan,
            "slope_median": math.nan,
            "slope_abs_median": math.nan,
            "baseline_noise_mad": math.nan,
            "snr": math.nan,
        }

    baseline_command = _median([_safe_float(row.get("command_throttle")) for row in baseline_rows])
    baseline_actuators = {
        f"baseline_actuator_{index}": _median([_safe_float(row.get(f"actuator_{index}")) for row in baseline_rows])
        for index in range(1, 5)
    }

    aligned_sample_count = 0
    active_sample_count = 0
    for row in samples:
        delta_values: list[float] = []
        for actuator_index in range(1, 5):
            actuator_value = _safe_float(row.get(f"actuator_{actuator_index}"))
            baseline_value = baseline_actuators[f"baseline_actuator_{actuator_index}"]
            delta = actuator_value - baseline_value if math.isfinite(actuator_value) and math.isfinite(baseline_value) else math.nan
            row[f"delta_actuator_{actuator_index}"] = delta
            if math.isfinite(delta):
                delta_values.append(delta)
        row["delta_u"] = _safe_float(row.get("command_throttle")) - baseline_command if math.isfinite(baseline_command) else math.nan
        row["delta_a_mean"] = float(np.mean(delta_values)) if len(delta_values) == 4 else math.nan
        if math.isfinite(_safe_float(row.get("delta_a_mean"))):
            aligned_sample_count += 1
            if str(row.get("phase", "")) in ACTIVE_PHASES:
                active_sample_count += 1

    baseline_noise_mad = _mad([_safe_float(row.get("delta_a_mean")) for row in baseline_rows])
    segments = _segment_active_pulses(samples)
    segment_rows: list[dict[str, Any]] = []
    for segment in segments:
        segment_delta_u = _median([_safe_float(row.get("delta_u")) for row in segment["rows"]])
        segment_delta_a = _median([_safe_float(row.get("delta_a_mean")) for row in segment["rows"]])
        slope = math.nan
        if math.isfinite(segment_delta_u) and abs(segment_delta_u) > 1e-12 and math.isfinite(segment_delta_a):
            slope = float(segment_delta_a / segment_delta_u)
        segment_rows.append(
            {
                "phase": segment["phase"],
                "delta_u_median": segment_delta_u,
                "delta_a_mean_median": segment_delta_a,
                "direction_sign": _sign(segment_delta_u),
                "slope": slope,
                "sample_count": len(segment["rows"]),
            }
        )

    slope_values = [float(item["slope"]) for item in segment_rows if math.isfinite(_safe_float(item.get("slope")))]
    signal_values = [abs(float(item["delta_a_mean_median"])) for item in segment_rows if math.isfinite(_safe_float(item.get("delta_a_mean_median")))]
    baseline_noise_floor = max(baseline_noise_mad, 1e-6) if math.isfinite(baseline_noise_mad) else math.nan
    snr = _median(signal_values) / baseline_noise_floor if signal_values and math.isfinite(baseline_noise_floor) else math.nan

    return {
        "analysis_status": "ok" if segment_rows else "active_pulses_unavailable",
        "baseline_command_throttle": baseline_command,
        **baseline_actuators,
        "baseline_sample_count": len(baseline_rows),
        "active_sample_count": active_sample_count,
        "aligned_sample_count": aligned_sample_count,
        "pulse_count_seen": len(segments),
        "mean_delta_actuator_pos": _median(
            [float(item["delta_a_mean_median"]) for item in segment_rows if int(item["direction_sign"]) > 0]
        ),
        "mean_delta_actuator_neg": _median(
            [float(item["delta_a_mean_median"]) for item in segment_rows if int(item["direction_sign"]) < 0]
        ),
        "effect_abs_median": _median(signal_values),
        "slope_median": _median(slope_values),
        "slope_abs_median": _median([abs(value) for value in slope_values]),
        "baseline_noise_mad": baseline_noise_mad,
        "snr": snr,
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
        "baseline_actuator_1": math.nan,
        "baseline_actuator_2": math.nan,
        "baseline_actuator_3": math.nan,
        "baseline_actuator_4": math.nan,
        "baseline_sample_count": 0,
        "active_sample_count": 0,
        "aligned_sample_count": 0,
        "pulse_count_seen": 0,
        "mean_delta_actuator_pos": math.nan,
        "mean_delta_actuator_neg": math.nan,
        "effect_abs_median": math.nan,
        "slope_median": math.nan,
        "slope_abs_median": math.nan,
        "baseline_noise_mad": math.nan,
        "snr": math.nan,
    }
    if artifact_dir is None or not artifact_dir.exists() or not manifest:
        return attempt
    samples = _build_aligned_samples(artifact_dir, manifest)
    if not samples:
        attempt["analysis_status"] = "telemetry_unavailable"
        return attempt
    attempt.update(_compute_run_effect_metrics(samples))
    return attempt


def _tier_summary(rows: list[dict[str, Any]], sign_ref: int) -> dict[str, Any]:
    attempt_count = len(rows)
    accepted_rows = [row for row in rows if bool(row.get("accepted"))]
    gate_count = sum(1 for row in rows if not bool(row.get("accepted")) and not bool(row.get("failsafe_during_experiment")))
    failsafe_count = sum(1 for row in rows if bool(row.get("failsafe_during_experiment")))
    finite_slope_rows = [row for row in accepted_rows if math.isfinite(_safe_float(row.get("slope_median")))]
    slope_abs_values = [_safe_float(row.get("slope_abs_median")) for row in accepted_rows if math.isfinite(_safe_float(row.get("slope_abs_median")))]
    direction_matches = sum(1 for row in finite_slope_rows if _sign(_safe_float(row.get("slope_median"))) == sign_ref)
    predictability_cv = math.nan
    finite_abs = _finite_values(slope_abs_values)
    if finite_abs.size > 0:
        mean_value = float(np.mean(finite_abs))
        predictability_cv = float(np.std(finite_abs) / mean_value) if mean_value > 0.0 else math.nan
    return {
        "attempt_count": attempt_count,
        "accepted_count": len(accepted_rows),
        "gate_rate": _bool_as_rate(gate_count, attempt_count),
        "failsafe_rate": _bool_as_rate(failsafe_count, attempt_count),
        "direction_consistency": _bool_as_rate(direction_matches, len(finite_slope_rows)),
        "predictability_cv": predictability_cv,
        "median_snr": _median([_safe_float(row.get("snr")) for row in accepted_rows]),
        "median_effect_abs": _median([_safe_float(row.get("effect_abs_median")) for row in accepted_rows]),
        "median_slope_abs": _median([_safe_float(row.get("slope_abs_median")) for row in accepted_rows]),
    }


def _scenario_thresholds(scenario: str) -> dict[str, Any]:
    if scenario == "proxy_dynamic":
        return {
            "direction_consistency_min": 0.60,
            "predictability_cv_max": 0.55,
            "failsafe_rate_max": 0.20,
            "gate_rate_max": None,
            "small_tier_above_noise_required": False,
            "monotonicity_required": False,
            "profile_not_completed_majority_forbidden": True,
        }
    return {
        "direction_consistency_min": 0.80,
        "predictability_cv_max": 0.40,
        "failsafe_rate_max": 0.0,
        "gate_rate_max": 0.20,
        "small_tier_above_noise_required": True,
        "monotonicity_required": True,
        "profile_not_completed_majority_forbidden": False,
    }


def _scenario_summary(scenario: str, rows: list[dict[str, Any]], sign_ref: int) -> dict[str, Any]:
    tier_rows = {
        tier: [row for row in rows if str(row.get("amplitude_tier", "")) == tier]
        for tier in TIERS
    }
    tier_results = {tier: _tier_summary(tier_rows[tier], sign_ref) for tier in TIERS}
    accepted_rows = [row for row in rows if bool(row.get("accepted"))]
    finite_slope_rows = [row for row in accepted_rows if math.isfinite(_safe_float(row.get("slope_median")))]
    direction_matches = sum(1 for row in finite_slope_rows if _sign(_safe_float(row.get("slope_median"))) == sign_ref)
    overall_abs = [_safe_float(row.get("slope_abs_median")) for row in accepted_rows if math.isfinite(_safe_float(row.get("slope_abs_median")))]
    overall_cv = math.nan
    finite_abs = _finite_values(overall_abs)
    if finite_abs.size > 0:
        mean_value = float(np.mean(finite_abs))
        overall_cv = float(np.std(finite_abs) / mean_value) if mean_value > 0.0 else math.nan
    attempt_count = len(rows)
    gate_count = sum(1 for row in rows if not bool(row.get("accepted")) and not bool(row.get("failsafe_during_experiment")))
    failsafe_count = sum(1 for row in rows if bool(row.get("failsafe_during_experiment")))
    profile_not_completed_count = sum(
        1
        for row in rows
        if str(row.get("completion_reason", "")).strip().lower() != "profile_completed" or str(row.get("status", "")).strip().lower() != "completed"
    )

    thresholds = _scenario_thresholds(scenario)
    small_result = tier_results["small"]
    medium_result = tier_results["medium"]
    small_tier_above_noise = math.isfinite(_safe_float(small_result["median_snr"])) and float(small_result["median_snr"]) >= 3.0
    medium_effect = _safe_float(medium_result["median_effect_abs"])
    small_effect = _safe_float(small_result["median_effect_abs"])
    monotonicity = math.isfinite(medium_effect) and math.isfinite(small_effect) and medium_effect > small_effect
    accepted_count = min(int(small_result["accepted_count"]), int(medium_result["accepted_count"]))

    blocking_reasons: list[str] = []
    if accepted_count < 5:
        blocking_reasons.append(f"{scenario}_accepted_target_not_met")
    if not math.isfinite(_safe_float(_bool_as_rate(direction_matches, len(finite_slope_rows)))) or float(_bool_as_rate(direction_matches, len(finite_slope_rows))) < float(thresholds["direction_consistency_min"]):
        blocking_reasons.append(f"{scenario}_direction_consistency_below_threshold")
    if not math.isfinite(overall_cv) or overall_cv > float(thresholds["predictability_cv_max"]):
        blocking_reasons.append(f"{scenario}_predictability_cv_above_threshold")
    if thresholds["small_tier_above_noise_required"] and not small_tier_above_noise:
        blocking_reasons.append(f"{scenario}_small_tier_below_snr_gate")
    if thresholds["monotonicity_required"] and not monotonicity:
        blocking_reasons.append(f"{scenario}_monotonicity_failed")
    failsafe_rate = _bool_as_rate(failsafe_count, attempt_count)
    if not math.isfinite(_safe_float(failsafe_rate)) or float(failsafe_rate) > float(thresholds["failsafe_rate_max"]):
        blocking_reasons.append(f"{scenario}_failsafe_rate_above_threshold")
    gate_rate = _bool_as_rate(gate_count, attempt_count)
    gate_rate_max = thresholds["gate_rate_max"]
    if gate_rate_max is not None and (not math.isfinite(_safe_float(gate_rate)) or float(gate_rate) > float(gate_rate_max)):
        blocking_reasons.append(f"{scenario}_gate_rate_above_threshold")
    profile_not_completed_rate = _bool_as_rate(profile_not_completed_count, attempt_count)
    if thresholds["profile_not_completed_majority_forbidden"] and math.isfinite(_safe_float(profile_not_completed_rate)) and float(profile_not_completed_rate) > 0.5:
        blocking_reasons.append(f"{scenario}_profile_completion_majority_failed")

    return {
        "scenario": scenario,
        "accepted_count": accepted_count,
        "attempt_count": attempt_count,
        "gate_rate": gate_rate,
        "failsafe_rate": failsafe_rate,
        "direction_consistency": _bool_as_rate(direction_matches, len(finite_slope_rows)),
        "predictability_cv": overall_cv,
        "small_tier_above_noise": small_tier_above_noise,
        "monotonicity": monotonicity,
        "profile_not_completed_rate": profile_not_completed_rate,
        "ready": not blocking_reasons,
        "blocking_reasons": blocking_reasons,
        "tiers": tier_results,
    }


def _flatten_config_row(result: dict[str, Any]) -> dict[str, Any]:
    small = result["tiers"]["small"]
    medium = result["tiers"]["medium"]
    return {
        "scenario": result["scenario"],
        "accepted_count": result["accepted_count"],
        "attempt_count": result["attempt_count"],
        "gate_rate": result["gate_rate"],
        "failsafe_rate": result["failsafe_rate"],
        "direction_consistency": result["direction_consistency"],
        "predictability_cv": result["predictability_cv"],
        "small_tier_above_noise": result["small_tier_above_noise"],
        "monotonicity": result["monotonicity"],
        "profile_not_completed_rate": result["profile_not_completed_rate"],
        "ready": result["ready"],
        "blocking_reasons": ",".join(result["blocking_reasons"]),
        "small_attempt_count": small["attempt_count"],
        "small_accepted_count": small["accepted_count"],
        "small_gate_rate": small["gate_rate"],
        "small_failsafe_rate": small["failsafe_rate"],
        "small_direction_consistency": small["direction_consistency"],
        "small_predictability_cv": small["predictability_cv"],
        "small_median_snr": small["median_snr"],
        "small_median_effect_abs": small["median_effect_abs"],
        "small_median_slope_abs": small["median_slope_abs"],
        "medium_attempt_count": medium["attempt_count"],
        "medium_accepted_count": medium["accepted_count"],
        "medium_gate_rate": medium["gate_rate"],
        "medium_failsafe_rate": medium["failsafe_rate"],
        "medium_direction_consistency": medium["direction_consistency"],
        "medium_predictability_cv": medium["predictability_cv"],
        "medium_median_snr": medium["median_snr"],
        "medium_median_effect_abs": medium["median_effect_abs"],
        "medium_median_slope_abs": medium["median_slope_abs"],
    }


def render_ardupilot_a2_readiness_markdown(payload: dict[str, Any]) -> str:
    overall = payload["overall_decision"]
    lines = [
        "# ArduPilot A2 STABILIZE Readiness",
        "",
        f"- ready_for_attack_v1: {'yes' if overall['ready_for_attack_v1'] else 'no'}",
        f"- next_step: {overall['next_step']}",
        f"- sign_ref: {payload['sign_ref']['sign']} ({_format_metric(payload['sign_ref']['mean_weight'])})",
        f"- blocking_reasons: {', '.join(payload['blocking_reasons']) if payload['blocking_reasons'] else 'none'}",
        "",
        "## Scenario Matrix",
        "",
        "| scenario | ready | accepted_count | attempt_count | dir_consistency | predictability_cv | small_snr_gate | monotonicity | failsafe_rate | gate_rate |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in payload["config_results"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    result["scenario"],
                    _format_metric(result["ready"]),
                    str(result["accepted_count"]),
                    str(result["attempt_count"]),
                    _format_metric(result["direction_consistency"]),
                    _format_metric(result["predictability_cv"]),
                    _format_metric(result["small_tier_above_noise"]),
                    _format_metric(result["monotonicity"]),
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
        lines.append(f"- blocking_reasons: {', '.join(result['blocking_reasons']) if result['blocking_reasons'] else 'none'}")
        lines.append(
            f"- small: accepted={result['tiers']['small']['accepted_count']}, "
            f"snr={_format_metric(result['tiers']['small']['median_snr'])}, "
            f"effect_abs={_format_metric(result['tiers']['small']['median_effect_abs'])}, "
            f"slope_abs={_format_metric(result['tiers']['small']['median_slope_abs'])}"
        )
        lines.append(
            f"- medium: accepted={result['tiers']['medium']['accepted_count']}, "
            f"snr={_format_metric(result['tiers']['medium']['median_snr'])}, "
            f"effect_abs={_format_metric(result['tiers']['medium']['median_effect_abs'])}, "
            f"slope_abs={_format_metric(result['tiers']['medium']['median_slope_abs'])}"
        )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run_ardupilot_a2_readiness(
    *,
    runs_manifest: Path,
    output_root: Path | None = None,
    baseline_study_dir: Path | None = None,
) -> Path:
    manifest_path = runs_manifest.expanduser().resolve()
    if not manifest_path.exists():
        raise FileNotFoundError(f"runs_manifest not found: {manifest_path}")
    rows = read_rows_csv(manifest_path)
    attempts = [_analyze_attempt(row) for row in rows]
    scenarios_evaluated = [scenario for scenario in SCENARIOS if any(str(row.get("scenario", "")) == scenario for row in attempts)]
    if not scenarios_evaluated:
        scenarios_evaluated = list(SCENARIOS)
    sign_ref = _load_baseline_sign_reference(baseline_study_dir or DEFAULT_A2_BASELINE_STUDY)
    config_results = [
        _scenario_summary(scenario, [row for row in attempts if row.get("scenario") == scenario], sign_ref["sign"])
        for scenario in scenarios_evaluated
    ]
    blocking_reasons = [reason for result in config_results for reason in result["blocking_reasons"]]
    ready_for_attack_v1 = all(result["ready"] for result in config_results)
    overall_decision = {
        "ready_for_attack_v1": ready_for_attack_v1,
        "next_step": "start_ardupilot_a2_stabilize_attack_v1" if ready_for_attack_v1 else "iterate_capture_profile_only",
        "scenario_status": {result["scenario"]: result["ready"] for result in config_results},
    }
    study_scope = {
        "backend": "ardupilot",
        "mode": "STABILIZE",
        "x_schema": "commands_only",
        "y_schema": "actuator_response",
        "input_source": "telemetry/input_trace.csv",
        "response_source": "telemetry/bin_rcou.csv",
        "scenario_scope": scenarios_evaluated,
        "tier_scope": list(TIERS),
        "accepted_target_per_config": 5,
        "max_attempts_per_config": 10,
        "accepted_count_definition": "min(accepted_count_small, accepted_count_medium)",
        "proxy_dynamic_note": "proxy_dynamic is a throttle-only, higher-cadence proxy and not the Formal V2 dynamic scenario.",
    }
    payload = {
        "study_scope": study_scope,
        "sign_ref": sign_ref,
        "config_results": config_results,
        "overall_decision": overall_decision,
        "blocking_reasons": blocking_reasons,
    }

    paths = _output_paths(output_root.expanduser().resolve() if output_root else None)
    report_text = render_ardupilot_a2_readiness_markdown(payload)
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
            "baseline_study_dir": str(_prefer_workspace_study_path(baseline_study_dir or DEFAULT_A2_BASELINE_STUDY)),
            "source_run_dirs": sorted({row["artifact_dir"] for row in run_level_rows if row.get("artifact_dir")}),
            "output_files": {
                "report": _relative_workspace_path(paths["report_path"]),
                "summary": _relative_workspace_path(paths["summary_path"]),
                "run_level_effects": _relative_workspace_path(paths["run_level_table_path"]),
                "config_readiness_matrix": _relative_workspace_path(paths["config_matrix_path"]),
            },
            "summary": payload,
        },
    )
    return paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Analyze narrow ArduPilot A2 STABILIZE readiness runs.")
    parser.add_argument("--runs-manifest", type=Path, required=True)
    parser.add_argument("--baseline-study-dir", type=Path, default=None)
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args(argv)

    study_dir = run_ardupilot_a2_readiness(
        runs_manifest=args.runs_manifest,
        baseline_study_dir=args.baseline_study_dir,
        output_root=args.output_root,
    )
    print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
