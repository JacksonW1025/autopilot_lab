from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml
from fep_core.paths import PX4_ANALYSIS_ROOT as ANALYSIS_ROOT
from fep_core.paths import PX4_RUNS_ROOT as ARTIFACT_ROOT

TOLERATED_ANOMALIES = {"clock_missing"}
PROFILE_MARKERS = {
    "baseline": "o",
    "step": "s",
    "pulse": "^",
    "sweep": "D",
}
AXIS_COLORS = {
    "roll": "#c0392b",
    "pitch": "#2471a3",
    "yaw": "#138d75",
    "throttle": "#b9770e",
    "composite": "#7d3c98",
}
XY_CONTAMINATION_ANOMALIES = {
    "xy_radius_excessive",
    "xy_displacement_excessive",
    "start_xy_radius_excessive",
    "prestart_xy_radius_excessive",
}
TIMING_ANOMALIES = {"clock_missing", "clock_not_advancing"}
RUNTIME_GUARD_ANOMALIES = {
    "ground_clearance_low",
    "land_timeout_force_disarm",
    "manual_control_not_enabled",
    "manual_echo_invalid",
    "manual_echo_missing",
    "manual_echo_source_mismatch",
    "manual_motion_not_observed",
    "manual_motion_window_missing",
    "manual_posctl_not_reached",
    "manual_profile_window_missing",
    "manual_step_window_missing",
    "manual_window_missing",
    "prestart_xy_radius_excessive",
    "prestart_xy_unavailable",
    "profile_clearance_low",
    "run_timeout",
    "takeoff_clearance_timeout",
}
MOTOR_PEAK_SAT_THRESHOLD = 0.98
FALLBACK_CLIP_THRESHOLD = 0.015
FALLBACK_UNALLOC_THRESHOLD = 0.5
TORQUE_ACHIEVED_LOW_THRESHOLD = 0.85
THRUST_ACHIEVED_LOW_THRESHOLD = 0.95


@dataclass(slots=True)
class RunRecord:
    run_id: str
    run_dir: Path
    start_time: datetime
    end_time: datetime | None
    phase: int
    input_chain: str
    profile_type: str
    axis: str
    manual_mode: str
    sim_world: str
    status: str
    anomalies: list[str]
    px4_log_path: str | None
    profile_params: dict[str, Any]
    input_peak: float
    input_rate_peak: float
    tracking_error_peak: float
    tracking_error_rms: float
    response_delay_ms: float
    nav_state_change: int
    failsafe_event: int
    ulog_saturation_metric: str
    ulog_parse_status: str
    motors_peak: float = math.nan
    clip_frac: float = math.nan
    thrust_achieved: float = math.nan
    torque_achieved: float = math.nan
    max_unalloc_torque: float = math.nan
    active_clip_frac: float = math.nan
    active_thrust_achieved: float = math.nan
    active_thrust_achieved_min: float = math.nan
    active_torque_achieved: float = math.nan
    active_torque_achieved_min: float = math.nan
    active_max_unalloc_torque: float = math.nan
    first_clip_rel_s: float = math.nan
    first_unalloc_rel_s: float = math.nan
    prefailsafe_max_unalloc_torque: float = math.nan
    prefailsafe_clip_frac: float = math.nan
    config_signature: str = ""
    scenario_signature: str = ""
    operational_group: str = ""
    boundary_class: str = "pending"
    selected: bool = False
    selection_reason: str = ""
    superseded_invalid: bool = False
    rank_status: int = 0
    critical_anomaly_count: int = 0

    @property
    def timing_valid(self) -> bool:
        return self.status != "invalid_timing" and "clock_missing" not in self.anomalies and "clock_not_advancing" not in self.anomalies

    @property
    def has_fatal_state(self) -> bool:
        return self.status != "completed" or self.nav_state_change == 1 or self.failsafe_event == 1

    @property
    def amplitude(self) -> float:
        return _float_value(self.profile_params.get("amplitude", self.input_peak))

    @property
    def duration_s(self) -> float:
        return _float_value(self.profile_params.get("duration_s", 0.0))

    def to_row(self) -> dict[str, Any]:
        delay_value = _csv_float(self.response_delay_ms, digits=3)
        return {
            "run_id": self.run_id,
            "run_dir": str(self.run_dir),
            "start_time": self.start_time.isoformat(),
            "input_chain": self.input_chain,
            "profile_type": self.profile_type,
            "axis": self.axis,
            "manual_mode": self.manual_mode,
            "sim_world": self.sim_world,
            "status": self.status,
            "boundary_class": self.boundary_class,
            "superseded_invalid": self.superseded_invalid,
            "input_peak": round(self.input_peak, 6),
            "input_rate_peak": round(self.input_rate_peak, 6),
            "tracking_error_peak": round(self.tracking_error_peak, 6),
            "tracking_error_rms": round(self.tracking_error_rms, 6),
            "response_delay_ms": delay_value,
            "nav_state_change": self.nav_state_change,
            "failsafe_event": self.failsafe_event,
            "timing_valid": self.timing_valid,
            "anomalies": ",".join(self.anomalies),
            "selection_reason": self.selection_reason,
            "config_signature": self.config_signature,
            "scenario_signature": self.scenario_signature,
            "px4_log_path": self.px4_log_path or "",
            "ulog_parse_status": self.ulog_parse_status,
            "ulog_saturation_metric": self.ulog_saturation_metric,
            "motors_peak": _csv_float(self.motors_peak),
            "clip_frac": _csv_float(self.clip_frac),
            "thrust_achieved": _csv_float(self.thrust_achieved),
            "torque_achieved": _csv_float(self.torque_achieved),
            "max_unalloc_torque": _csv_float(self.max_unalloc_torque),
            "active_clip_frac": _csv_float(self.active_clip_frac),
            "active_thrust_achieved": _csv_float(self.active_thrust_achieved),
            "active_thrust_achieved_min": _csv_float(self.active_thrust_achieved_min),
            "active_torque_achieved": _csv_float(self.active_torque_achieved),
            "active_torque_achieved_min": _csv_float(self.active_torque_achieved_min),
            "active_max_unalloc_torque": _csv_float(self.active_max_unalloc_torque),
            "first_clip_rel_s": _csv_float(self.first_clip_rel_s),
            "first_unalloc_rel_s": _csv_float(self.first_unalloc_rel_s),
            "prefailsafe_max_unalloc_torque": _csv_float(self.prefailsafe_max_unalloc_torque),
            "prefailsafe_clip_frac": _csv_float(self.prefailsafe_clip_frac),
        }


@dataclass(slots=True)
class AxisLayer:
    input_chain: str
    profile_type: str
    axis: str
    manual_mode: str
    safe_upper_bound_input_peak: float | None
    degraded_input_peaks: list[float] = field(default_factory=list)
    frontier_invalid_input_peak: float | None = None
    safe_run_ids: list[str] = field(default_factory=list)
    degraded_run_ids: list[str] = field(default_factory=list)
    invalid_run_ids: list[str] = field(default_factory=list)
    superseded_invalid_run_ids: list[str] = field(default_factory=list)

    def to_row(self) -> dict[str, Any]:
        return {
            "input_chain": self.input_chain,
            "profile_type": self.profile_type,
            "axis": self.axis,
            "manual_mode": self.manual_mode,
            "safe_upper_bound_input_peak": "" if self.safe_upper_bound_input_peak is None else round(self.safe_upper_bound_input_peak, 6),
            "degraded_input_peaks": ",".join(f"{value:.6f}" for value in self.degraded_input_peaks),
            "frontier_invalid_input_peak": "" if self.frontier_invalid_input_peak is None else round(self.frontier_invalid_input_peak, 6),
            "safe_run_ids": ",".join(self.safe_run_ids),
            "degraded_run_ids": ",".join(self.degraded_run_ids),
            "invalid_run_ids": ",".join(self.invalid_run_ids),
            "superseded_invalid_run_ids": ",".join(self.superseded_invalid_run_ids),
        }


def _float_value(value: Any, default: float = math.nan) -> float:
    if value in ("", None):
        return default
    return float(value)


def _csv_float(value: float, digits: int = 6) -> float | str:
    return "" if math.isnan(value) else round(value, digits)


def _parse_datetime(value: Any) -> datetime:
    if value in ("", None):
        return datetime.now(timezone.utc).astimezone()
    return datetime.fromisoformat(str(value))


def _parse_ulog_metric_string(metric_text: str) -> dict[str, float]:
    parsed: dict[str, float] = {}
    for part in metric_text.split(";"):
        if "=" not in part:
            continue
        key, raw_value = part.split("=", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not key or not raw_value:
            continue
        try:
            parsed[key] = float(raw_value)
        except ValueError:
            continue
    return parsed


def _normalize_for_signature(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 6)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {key: _normalize_for_signature(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_normalize_for_signature(item) for item in value]
    return value


def _status_rank(status: str) -> int:
    return {
        "completed": 4,
        "invalid_timing": 3,
        "invalid_runtime": 2,
        "invalid_artifacts": 1,
    }.get(status, 0)


def _critical_anomaly_count(anomalies: Iterable[str]) -> int:
    return sum(1 for item in anomalies if item not in TOLERATED_ANOMALIES)


def _manual_mode(input_chain: str, profile_params: dict[str, Any]) -> str:
    if input_chain != "manual":
        return "n/a"
    value = str(profile_params.get("manual_mode", "echo")).strip()
    return value or "echo"


def _scenario_profile_params(
    input_chain: str,
    profile_type: str,
    axis: str,
    profile_params: dict[str, Any],
    manual_mode: str,
) -> dict[str, Any]:
    relevant: dict[str, Any] = {}

    if input_chain == "manual":
        relevant["manual_mode"] = manual_mode

    if profile_type != "baseline" and "amplitude" in profile_params:
        relevant["amplitude"] = profile_params["amplitude"]

    if profile_type in {"step", "pulse", "sweep"} and "duration_s" in profile_params:
        relevant["duration_s"] = profile_params["duration_s"]

    if profile_type == "pulse" and "pulse_width_s" in profile_params:
        relevant["pulse_width_s"] = profile_params["pulse_width_s"]

    if profile_type == "sweep":
        if "sweep_start_hz" in profile_params:
            relevant["sweep_start_hz"] = profile_params["sweep_start_hz"]
        if "sweep_end_hz" in profile_params:
            relevant["sweep_end_hz"] = profile_params["sweep_end_hz"]

    if axis == "composite":
        for key in ("roll_amplitude", "pitch_amplitude", "yaw_amplitude", "throttle", "thrust_delta"):
            if key in profile_params:
                relevant[key] = profile_params[key]

    return relevant


def _load_metrics_csv(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        row = next(reader, None)
    if row is None:
        raise ValueError(f"空 metrics.csv: {path}")
    return row


def load_run_records(artifacts_root: Path) -> list[RunRecord]:
    records: list[RunRecord] = []
    for run_dir in sorted(path for path in artifacts_root.iterdir() if path.is_dir()):
        manifest_path = run_dir / "manifest.yaml"
        metrics_path = run_dir / "metrics.csv"
        if not manifest_path.exists() or not metrics_path.exists():
            continue

        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        metrics = _load_metrics_csv(metrics_path)
        if not isinstance(manifest, dict):
            continue

        profile_params = manifest.get("profile_params", {})
        if not isinstance(profile_params, dict):
            profile_params = {}

        ulog_metrics = _parse_ulog_metric_string(str(metrics.get("ulog_saturation_metric", "")))

        record = RunRecord(
            run_id=str(manifest["run_id"]),
            run_dir=run_dir.resolve(),
            start_time=_parse_datetime(manifest.get("start_time")),
            end_time=_parse_datetime(manifest.get("end_time")) if manifest.get("end_time") else None,
            phase=int(manifest.get("phase", 0)),
            input_chain=str(manifest.get("input_chain", "")),
            profile_type=str(manifest.get("profile_type", "")),
            axis=str(profile_params.get("axis", metrics.get("axis", ""))),
            manual_mode=_manual_mode(str(manifest.get("input_chain", "")), profile_params),
            sim_world=str(manifest.get("sim_world", "unspecified") or "unspecified"),
            status=str(manifest.get("status", "missing")),
            anomalies=[str(item) for item in manifest.get("anomaly_summary", [])],
            px4_log_path=str(manifest.get("px4_log_path")) if manifest.get("px4_log_path") else None,
            profile_params=profile_params,
            input_peak=_float_value(metrics.get("input_peak"), 0.0),
            input_rate_peak=_float_value(metrics.get("input_rate_peak"), 0.0),
            tracking_error_peak=_float_value(metrics.get("tracking_error_peak"), 0.0),
            tracking_error_rms=_float_value(metrics.get("tracking_error_rms"), 0.0),
            response_delay_ms=_float_value(metrics.get("response_delay_ms"), math.nan),
            nav_state_change=int(metrics.get("nav_state_change", 0)),
            failsafe_event=int(metrics.get("failsafe_event", 0)),
            ulog_saturation_metric=str(metrics.get("ulog_saturation_metric", "")),
            ulog_parse_status=str(metrics.get("ulog_parse_status", "")),
            motors_peak=ulog_metrics.get("motors_peak", math.nan),
            clip_frac=ulog_metrics.get("clip_frac", math.nan),
            thrust_achieved=ulog_metrics.get("thrust_achieved", math.nan),
            torque_achieved=ulog_metrics.get("torque_achieved", math.nan),
            max_unalloc_torque=ulog_metrics.get("max_unalloc_torque", math.nan),
            active_clip_frac=ulog_metrics.get("active_clip_frac", math.nan),
            active_thrust_achieved=ulog_metrics.get("active_thrust_achieved", math.nan),
            active_thrust_achieved_min=ulog_metrics.get("active_thrust_achieved_min", math.nan),
            active_torque_achieved=ulog_metrics.get("active_torque_achieved", math.nan),
            active_torque_achieved_min=ulog_metrics.get("active_torque_achieved_min", math.nan),
            active_max_unalloc_torque=ulog_metrics.get("active_max_unalloc_torque", math.nan),
            first_clip_rel_s=ulog_metrics.get("first_clip_rel_s", math.nan),
            first_unalloc_rel_s=ulog_metrics.get("first_unalloc_rel_s", math.nan),
            prefailsafe_max_unalloc_torque=ulog_metrics.get("prefailsafe_max_unalloc_torque", math.nan),
            prefailsafe_clip_frac=ulog_metrics.get("prefailsafe_clip_frac", math.nan),
        )
        record.rank_status = _status_rank(record.status)
        record.critical_anomaly_count = _critical_anomaly_count(record.anomalies)
        record.config_signature = json.dumps(
            {
                "phase": record.phase,
                "input_chain": record.input_chain,
                "profile_type": record.profile_type,
                "axis": record.axis,
                "profile_params": _normalize_for_signature(record.profile_params),
            },
            sort_keys=True,
            ensure_ascii=False,
        )
        record.scenario_signature = json.dumps(
            {
                "phase": record.phase,
                "input_chain": record.input_chain,
                "profile_type": record.profile_type,
                "axis": record.axis,
                "scenario_profile_params": _normalize_for_signature(
                    _scenario_profile_params(
                        record.input_chain,
                        record.profile_type,
                        record.axis,
                        record.profile_params,
                        record.manual_mode,
                    )
                ),
            },
            sort_keys=True,
            ensure_ascii=False,
        )
        record.operational_group = "|".join([record.input_chain, record.profile_type, record.axis, record.manual_mode])
        records.append(record)

    return records


def filter_records_by_world(records: list[RunRecord], world_filter: str) -> list[RunRecord]:
    if world_filter == "all":
        return list(records)
    if world_filter == "windy":
        return [item for item in records if item.sim_world == "windy"]
    return [item for item in records if item.sim_world in {"unspecified", "default"}]


def select_nominal_records(records: list[RunRecord]) -> list[RunRecord]:
    grouped: dict[str, list[RunRecord]] = {}
    for record in records:
        grouped.setdefault(record.scenario_signature, []).append(record)

    selected: list[RunRecord] = []
    for candidates in grouped.values():
        candidates.sort(
            key=lambda item: (
                item.rank_status,
                item.start_time.timestamp(),
                -item.critical_anomaly_count,
            )
        )
        chosen = candidates[-1]
        chosen.selected = True
        if chosen.status == "completed":
            chosen.selection_reason = "preferred_latest_completed"
        elif chosen.rank_status == 0:
            chosen.selection_reason = "fallback_unknown_status"
        else:
            chosen.selection_reason = "fallback_latest_non_completed"
        selected.append(chosen)

    selected.sort(key=lambda item: item.start_time)
    return selected


def _median(values: list[float]) -> float | None:
    cleaned = [value for value in values if not math.isnan(value)]
    if not cleaned:
        return None
    return float(statistics.median(cleaned))


def _is_metric_stressed(record: RunRecord, lower_completed: list[RunRecord]) -> bool:
    if any(item not in TOLERATED_ANOMALIES for item in record.anomalies):
        return True

    lower_delays = [item.response_delay_ms for item in lower_completed if not math.isnan(item.response_delay_ms)]
    delay_baseline = _median(lower_delays)
    if delay_baseline is not None and not math.isnan(record.response_delay_ms):
        if record.response_delay_ms > max(delay_baseline * 1.5, delay_baseline + 15.0):
            return True

    if record.input_chain == "attitude" and record.input_peak > 0.0:
        lower_ratios = [
            item.tracking_error_rms / item.input_peak
            for item in lower_completed
            if item.input_peak > 0.0 and not math.isnan(item.tracking_error_rms)
        ]
        ratio_baseline = _median(lower_ratios)
        current_ratio = record.tracking_error_rms / record.input_peak if record.input_peak > 0.0 else 0.0
        if ratio_baseline is not None and current_ratio > max(ratio_baseline * 1.5, ratio_baseline + 0.05):
            return True

    return False


def classify_records(records: list[RunRecord]) -> list[AxisLayer]:
    grouped: dict[str, list[RunRecord]] = {}
    for record in records:
        grouped.setdefault(record.operational_group, []).append(record)

    layers: list[AxisLayer] = []
    for group_key, group_records in sorted(grouped.items()):
        group_records.sort(key=lambda item: (item.input_peak, item.start_time.timestamp()))
        completed_records = [item for item in group_records if not item.has_fatal_state]
        completed_frontier = max((item.input_peak for item in completed_records), default=None)
        lower_completed: list[RunRecord] = []

        for record in group_records:
            record.superseded_invalid = record.has_fatal_state and any(
                item.input_peak > record.input_peak for item in completed_records
            )
            if record.has_fatal_state:
                record.boundary_class = "invalid"
                continue
            if record.profile_type == "baseline":
                record.boundary_class = "safe"
                lower_completed.append(record)
                continue

            stressed = _is_metric_stressed(record, lower_completed)
            is_frontier = (
                completed_frontier is not None
                and len(completed_records) > 1
                and math.isclose(record.input_peak, completed_frontier, abs_tol=1e-9)
                and bool(lower_completed)
            )
            record.boundary_class = "degraded" if stressed or is_frontier else "safe"
            lower_completed.append(record)

        input_chain, profile_type, axis, manual_mode = group_key.split("|")
        safe_records = [item for item in group_records if item.boundary_class == "safe"]
        degraded_records = [item for item in group_records if item.boundary_class == "degraded"]
        invalid_records = [item for item in group_records if item.boundary_class == "invalid"]
        frontier_invalids = [
            item
            for item in invalid_records
            if not item.superseded_invalid and (completed_frontier is None or item.input_peak >= completed_frontier)
        ]
        layer = AxisLayer(
            input_chain=input_chain,
            profile_type=profile_type,
            axis=axis,
            manual_mode=manual_mode,
            safe_upper_bound_input_peak=max((item.input_peak for item in safe_records), default=None),
            degraded_input_peaks=[item.input_peak for item in degraded_records],
            frontier_invalid_input_peak=min((item.input_peak for item in frontier_invalids), default=None),
            safe_run_ids=[item.run_id for item in safe_records],
            degraded_run_ids=[item.run_id for item in degraded_records],
            invalid_run_ids=[item.run_id for item in invalid_records],
            superseded_invalid_run_ids=[item.run_id for item in invalid_records if item.superseded_invalid],
        )
        layers.append(layer)

    return layers


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _write_markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "_无数据_"
    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([head, sep, *body])


def _format_delay(value: float) -> str:
    return "nan" if math.isnan(value) else f"{value:.3f}"


def _format_metric(value: float) -> str:
    return "nan" if math.isnan(value) else f"{value:.3f}"


def _metric_median(records: list[RunRecord], metric_name: str) -> float:
    values = [getattr(item, metric_name) for item in records if not math.isnan(getattr(item, metric_name))]
    if not values:
        return math.nan
    return float(statistics.median(values))


def _metric_count(records: list[RunRecord], metric_name: str, threshold: float) -> int:
    return sum(1 for item in records if not math.isnan(getattr(item, metric_name)) and getattr(item, metric_name) >= threshold)


def _preferred_metric_value(record: RunRecord, *metric_names: str) -> float:
    for metric_name in metric_names:
        value = getattr(record, metric_name)
        if not math.isnan(value):
            return value
    return math.nan


def _metric_median_preferred(records: list[RunRecord], *metric_names: str) -> float:
    values = [_preferred_metric_value(item, *metric_names) for item in records]
    cleaned = [value for value in values if not math.isnan(value)]
    if not cleaned:
        return math.nan
    return float(statistics.median(cleaned))


def _max_metric_value(record: RunRecord, *metric_names: str) -> float:
    values = [getattr(record, metric_name) for metric_name in metric_names if not math.isnan(getattr(record, metric_name))]
    if not values:
        return math.nan
    return max(values)


def _min_metric_value(record: RunRecord, *metric_names: str) -> float:
    values = [getattr(record, metric_name) for metric_name in metric_names if not math.isnan(getattr(record, metric_name))]
    if not values:
        return math.nan
    return min(values)


def _has_xy_contamination(record: RunRecord) -> bool:
    return any(item in XY_CONTAMINATION_ANOMALIES for item in record.anomalies)


def _clip_threshold(safe_clip: float) -> float:
    if math.isnan(safe_clip):
        return FALLBACK_CLIP_THRESHOLD
    return max(FALLBACK_CLIP_THRESHOLD, safe_clip + 0.005)


def _unalloc_threshold(safe_unalloc: float) -> float:
    if math.isnan(safe_unalloc):
        return FALLBACK_UNALLOC_THRESHOLD
    return max(FALLBACK_UNALLOC_THRESHOLD, safe_unalloc + 0.2, safe_unalloc * 2.0)


def _dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def build_failure_attribution_rows(selected_records: list[RunRecord]) -> list[dict[str, Any]]:
    safe_by_chain = {
        chain: [item for item in selected_records if item.input_chain == chain and item.boundary_class == "safe"]
        for chain in ("attitude", "manual")
    }
    rows: list[dict[str, Any]] = []

    for record in selected_records:
        if record.boundary_class not in {"degraded", "invalid"} or record.superseded_invalid:
            continue

        safe_records = safe_by_chain.get(record.input_chain, [])
        safe_clip = _metric_median_preferred(safe_records, "active_clip_frac", "clip_frac")
        safe_unalloc = _metric_median_preferred(safe_records, "active_max_unalloc_torque", "max_unalloc_torque")
        clip_threshold = _clip_threshold(safe_clip)
        unalloc_threshold = _unalloc_threshold(safe_unalloc)

        clip_value = _max_metric_value(record, "active_clip_frac", "prefailsafe_clip_frac", "clip_frac")
        unalloc_value = _max_metric_value(record, "active_max_unalloc_torque", "prefailsafe_max_unalloc_torque", "max_unalloc_torque")
        torque_value = _min_metric_value(record, "active_torque_achieved", "torque_achieved")
        thrust_value = _min_metric_value(record, "active_thrust_achieved", "thrust_achieved")
        torque_min_value = _preferred_metric_value(record, "active_torque_achieved_min")
        thrust_min_value = _preferred_metric_value(record, "active_thrust_achieved_min")

        torque_limited = not math.isnan(torque_value) and torque_value <= TORQUE_ACHIEVED_LOW_THRESHOLD
        thrust_limited = not math.isnan(thrust_value) and thrust_value <= THRUST_ACHIEVED_LOW_THRESHOLD
        clip_stressed = (
            (not math.isnan(record.motors_peak) and record.motors_peak >= MOTOR_PEAK_SAT_THRESHOLD)
            or (not math.isnan(clip_value) and clip_value >= clip_threshold)
        )
        allocation_stressed = not math.isnan(unalloc_value) and unalloc_value >= unalloc_threshold
        xy_contaminated = _has_xy_contamination(record)
        timing_invalid = any(item in TIMING_ANOMALIES for item in record.anomalies)
        runtime_guard_failure = any(
            item in RUNTIME_GUARD_ANOMALIES or item.startswith("manual_")
            for item in record.anomalies
        )

        factors: list[str] = []
        reasons: list[str] = []

        if timing_invalid:
            factors.append("timing_invalid")
            reasons.append("clock anomalies present")
        if xy_contaminated:
            factors.append("xy_drift_contamination")
            reasons.append("xy radius/displacement exceeded artifact guardrails")
        if clip_stressed and torque_limited:
            factors.append("motor_clipping")
            reasons.append(
                f"clip_frac={_format_metric(clip_value)} or motors_peak={_format_metric(record.motors_peak)} with torque_achieved={_format_metric(torque_value)}"
            )
        if allocation_stressed and torque_limited:
            factors.append("torque_allocation_limit")
            reasons.append(
                f"max_unalloc_torque={_format_metric(unalloc_value)} with torque_achieved={_format_metric(torque_value)}"
            )
        if thrust_limited:
            factors.append("thrust_tracking_limit")
            reasons.append(f"thrust_achieved={_format_metric(thrust_value)}")
        if torque_limited and not clip_stressed and not allocation_stressed:
            factors.append("torque_tracking_limit")
            reasons.append(f"torque_achieved={_format_metric(torque_value)} without clear clip/unalloc dominance")
        if runtime_guard_failure:
            factors.append("runtime_guard_failure")
            guard_anomalies = ",".join(item for item in record.anomalies if item in RUNTIME_GUARD_ANOMALIES or item.startswith("manual_"))
            reasons.append(f"runtime anomalies: {guard_anomalies}")
        if not math.isnan(record.first_clip_rel_s):
            reasons.append(f"first_clip_rel_s={_format_metric(record.first_clip_rel_s)}")
        if not math.isnan(record.first_unalloc_rel_s):
            reasons.append(f"first_unalloc_rel_s={_format_metric(record.first_unalloc_rel_s)}")
        if not math.isnan(record.prefailsafe_max_unalloc_torque):
            reasons.append(f"prefailsafe_max_unalloc_torque={_format_metric(record.prefailsafe_max_unalloc_torque)}")
        if not math.isnan(record.prefailsafe_clip_frac):
            reasons.append(f"prefailsafe_clip_frac={_format_metric(record.prefailsafe_clip_frac)}")
        if not math.isnan(torque_min_value):
            reasons.append(f"active_torque_achieved_min={_format_metric(torque_min_value)}")
        if not math.isnan(thrust_min_value):
            reasons.append(f"active_thrust_achieved_min={_format_metric(thrust_min_value)}")

        factors = _dedupe_preserve_order(factors)
        reasons = _dedupe_preserve_order(reasons)
        core_factors = [item for item in factors if item not in {"timing_invalid", "xy_drift_contamination"}]

        if xy_contaminated and core_factors:
            primary_mode = "mixed_failure_factors"
        elif "motor_clipping" in factors and "torque_allocation_limit" not in factors and len(core_factors) == 1:
            primary_mode = "motor_clipping_dominant"
        elif "torque_allocation_limit" in factors and "motor_clipping" not in factors and len(core_factors) == 1:
            primary_mode = "torque_allocation_limit_dominant"
        elif "thrust_tracking_limit" in factors and len(core_factors) == 1:
            primary_mode = "thrust_tracking_limit_dominant"
        elif "torque_tracking_limit" in factors and len(core_factors) == 1:
            primary_mode = "torque_tracking_limit_dominant"
        elif xy_contaminated and not core_factors:
            primary_mode = "xy_drift_contamination"
        elif "runtime_guard_failure" in factors and len(core_factors) == 1:
            primary_mode = "runtime_guard_failure"
        elif "timing_invalid" in factors and not core_factors:
            primary_mode = "timing_invalid"
        elif factors:
            primary_mode = "mixed_failure_factors"
        else:
            primary_mode = "unclassified_degradation"
            reasons.append("frontier/degraded classification without a dominant mechanism signal")

        rows.append(
            {
                "run_id": record.run_id,
                "input_chain": record.input_chain,
                "profile_type": record.profile_type,
                "axis": record.axis,
                "manual_mode": record.manual_mode,
                "status": record.status,
                "boundary_class": record.boundary_class,
                "input_peak": round(record.input_peak, 6),
                "primary_failure_mode": primary_mode,
                "contributing_factors": ",".join(factors) or "none",
                "reason_summary": "; ".join(reasons),
                "xy_contamination": xy_contaminated,
                "clip_frac": _csv_float(clip_value),
                "clip_threshold": round(clip_threshold, 6),
                "motors_peak": _csv_float(record.motors_peak),
                "torque_achieved": _csv_float(torque_value),
                "thrust_achieved": _csv_float(thrust_value),
                "max_unalloc_torque": _csv_float(unalloc_value),
                "unalloc_threshold": round(unalloc_threshold, 6),
                "active_torque_achieved_min": _csv_float(torque_min_value),
                "active_thrust_achieved_min": _csv_float(thrust_min_value),
                "first_clip_rel_s": _csv_float(record.first_clip_rel_s),
                "first_unalloc_rel_s": _csv_float(record.first_unalloc_rel_s),
                "prefailsafe_max_unalloc_torque": _csv_float(record.prefailsafe_max_unalloc_torque),
                "prefailsafe_clip_frac": _csv_float(record.prefailsafe_clip_frac),
                "timing_valid": record.timing_valid,
                "anomalies": ",".join(record.anomalies),
            }
        )

    return rows


def build_mechanism_rows(selected_records: list[RunRecord]) -> list[dict[str, Any]]:
    scopes = [
        ("attitude:selected", [item for item in selected_records if item.input_chain == "attitude"]),
        (
            "attitude:safe",
            [item for item in selected_records if item.input_chain == "attitude" and item.boundary_class == "safe"],
        ),
        (
            "attitude:frontier",
            [
                item
                for item in selected_records
                if item.input_chain == "attitude" and item.boundary_class in {"degraded", "invalid"} and not item.superseded_invalid
            ],
        ),
        ("manual:selected", [item for item in selected_records if item.input_chain == "manual"]),
        (
            "manual:safe",
            [item for item in selected_records if item.input_chain == "manual" and item.boundary_class == "safe"],
        ),
        (
            "manual:frontier",
            [
                item
                for item in selected_records
                if item.input_chain == "manual" and item.boundary_class in {"degraded", "invalid"} and not item.superseded_invalid
            ],
        ),
    ]

    rows: list[dict[str, Any]] = []
    for scope, records in scopes:
        if not records:
            continue
        rows.append(
            {
                "scope": scope,
                "runs": len(records),
                "parsed_runs": sum(1 for item in records if item.ulog_parse_status == "parsed"),
                "motor_sat_runs": _metric_count(records, "motors_peak", 0.98),
                "clip_runs": _metric_count(records, "clip_frac", 0.01),
                "median_motors_peak": _csv_float(_metric_median(records, "motors_peak")),
                "median_clip_frac": _csv_float(_metric_median(records, "clip_frac")),
                "median_thrust_achieved": _csv_float(_metric_median(records, "thrust_achieved")),
                "median_torque_achieved": _csv_float(_metric_median(records, "torque_achieved")),
                "median_max_unalloc_torque": _csv_float(_metric_median(records, "max_unalloc_torque")),
            }
        )
    return rows


def build_summary_markdown(
    all_records: list[RunRecord],
    selected_records: list[RunRecord],
    layers: list[AxisLayer],
    output_dir: Path,
    world_filter: str,
) -> str:
    completed_records = [item for item in selected_records if item.status == "completed"]
    attitude_rows = [item for item in selected_records if item.input_chain == "attitude"]
    manual_rows = [item for item in selected_records if item.input_chain == "manual"]
    attitude_safe = [item for item in attitude_rows if item.boundary_class == "safe"]
    attitude_frontier = [item for item in attitude_rows if item.boundary_class in {"degraded", "invalid"} and not item.superseded_invalid]
    timing_valid_completed = [item for item in completed_records if item.timing_valid]
    non_timing_completed = [item for item in completed_records if not item.timing_valid]
    invalid_timing_count = sum(1 for item in selected_records if item.status == "invalid_timing")
    mechanism_rows = build_mechanism_rows(selected_records)
    failure_attribution_rows = build_failure_attribution_rows(selected_records)

    missing_profiles: list[str] = []
    for chain in ("attitude", "manual"):
        for profile in ("pulse", "sweep"):
            if not any(item.input_chain == chain and item.profile_type == profile for item in selected_records):
                missing_profiles.append(f"{chain}:{profile}")

    attitude_table = _write_markdown_table(
        ["run_id", "profile", "axis", "status", "layer", "input_peak", "err_peak", "delay_ms"],
        [
            [
                item.run_id,
                item.profile_type,
                item.axis,
                item.status,
                item.boundary_class,
                f"{item.input_peak:.3f}",
                f"{item.tracking_error_peak:.6f}",
                _format_delay(item.response_delay_ms),
            ]
            for item in attitude_rows
        ],
    )
    manual_table = _write_markdown_table(
        ["run_id", "profile", "axis", "mode", "status", "layer", "input_peak", "delay_ms", "superseded_invalid"],
        [
            [
                item.run_id,
                item.profile_type,
                item.axis,
                item.manual_mode,
                item.status,
                item.boundary_class,
                f"{item.input_peak:.3f}",
                _format_delay(item.response_delay_ms),
                "yes" if item.superseded_invalid else "no",
            ]
            for item in manual_rows
        ],
    )
    layer_table = _write_markdown_table(
        ["chain", "profile", "axis", "mode", "safe<= ", "degraded", "frontier_invalid", "superseded_invalids"],
        [
            [
                layer.input_chain,
                layer.profile_type,
                layer.axis,
                layer.manual_mode,
                "" if layer.safe_upper_bound_input_peak is None else f"{layer.safe_upper_bound_input_peak:.3f}",
                ",".join(f"{value:.3f}" for value in layer.degraded_input_peaks) or "-",
                "" if layer.frontier_invalid_input_peak is None else f"{layer.frontier_invalid_input_peak:.3f}",
                ",".join(layer.superseded_invalid_run_ids) or "-",
            ]
            for layer in layers
        ],
    )
    mechanism_table = _write_markdown_table(
        [
            "scope",
            "runs",
            "parsed",
            "motor_sat>=0.98",
            "clip>=0.01",
            "median_clip",
            "median_torque",
            "median_thrust",
            "median_unalloc",
        ],
        [
            [
                str(row["scope"]),
                str(row["runs"]),
                str(row["parsed_runs"]),
                str(row["motor_sat_runs"]),
                str(row["clip_runs"]),
                str(row["median_clip_frac"]),
                str(row["median_torque_achieved"]),
                str(row["median_thrust_achieved"]),
                str(row["median_max_unalloc_torque"]),
            ]
            for row in mechanism_rows
        ],
    )
    attribution_table = _write_markdown_table(
        ["run_id", "profile", "axis", "mode", "layer", "primary_mode", "factors"],
        [
            [
                str(row["run_id"]),
                str(row["profile_type"]),
                str(row["axis"]),
                str(row["manual_mode"]),
                str(row["boundary_class"]),
                str(row["primary_failure_mode"]),
                str(row["contributing_factors"]),
            ]
            for row in failure_attribution_rows
        ],
    )

    findings: list[str] = []
    findings.append(
        f"- 在 world_filter={world_filter} 下选中的 run 共 {len(selected_records)} 组，其中 completed={len(completed_records)}，non-timing={len(non_timing_completed)}。"
    )
    if completed_records:
        if not non_timing_completed:
            findings.append("- 当前已完成 run 均满足 timing 条件，可用于 sim-time / timing 对照。")
        elif not timing_valid_completed:
            findings.append("- 当前全部已完成 run 仍为 non-timing，因此只能用于 functional / non-timing 结论。")
        else:
            findings.append(
                f"- 当前已完成 run 中有 {len(timing_valid_completed)} 组 timing-valid，{len(non_timing_completed)} 组仍为 non-timing；涉 `clock_missing/clock_not_advancing` 的 run 只能用于 functional 结论。"
            )
    if invalid_timing_count:
        findings.append(f"- 当前仍有 {invalid_timing_count} 组 run 被标为 `invalid_timing`，需要与 timing-valid run 分开解释。")
    if missing_profiles:
        findings.append(f"- 当前数据集中仍缺 profile：{', '.join(missing_profiles)}。")

    attitude_degraded = [item for item in attitude_rows if item.boundary_class == "degraded"]
    attitude_invalid = [item for item in attitude_rows if item.boundary_class == "invalid" and not item.superseded_invalid]
    if attitude_degraded:
        degraded_text = ", ".join(f"{item.profile_type}/{item.axis}@{item.input_peak:.2f}" for item in attitude_degraded)
        findings.append(f"- attitude 当前已探到的 frontier 点被标为 degraded：{degraded_text}。")
    if attitude_invalid:
        invalid_text = ", ".join(f"{item.profile_type}/{item.axis}@{item.input_peak:.2f}" for item in attitude_invalid)
        findings.append(f"- attitude 当前已出现 invalid frontier：{invalid_text}。")

    manual_degraded = [item for item in manual_rows if item.boundary_class == "degraded"]
    if manual_degraded:
        degraded_text = ", ".join(f"{item.profile_type}/{item.axis}@{item.input_peak:.2f}" for item in manual_degraded)
        findings.append(f"- manual frontier completed 点被标为 degraded：{degraded_text}；表示已到当前探索前沿，不代表已证明失稳。")

    superseded_invalids = [item for item in manual_rows if item.superseded_invalid]
    if superseded_invalids:
        findings.append(
            "- 低幅值 invalid 若已被更高幅值 completed run 覆盖，会标记为 superseded_invalid，表示它更像门禁/配置伪失败，而不是当前边界。"
        )

    xy_boundary_risk = [
        item
        for item in all_records
        if "xy_radius_excessive" in item.anomalies
        or "xy_displacement_excessive" in item.anomalies
        or "start_xy_radius_excessive" in item.anomalies
        or "prestart_xy_radius_excessive" in item.anomalies
    ]
    if xy_boundary_risk:
        risk_text = ", ".join(item.run_id for item in xy_boundary_risk[:4])
        suffix = " 等" if len(xy_boundary_risk) > 4 else ""
        findings.append(
            f"- 当前有 {len(xy_boundary_risk)} 组 run 带 `xy_radius/xy_displacement_excessive` 或 `prestart_xy_radius_excessive`，例如 {risk_text}{suffix}；这些 run 可能受风场下的位置漂移、地图边界污染，或被起飞前位置 gate 直接拦截。"
        )

    if attitude_rows:
        attitude_motor_sat = _metric_count(attitude_rows, "motors_peak", 0.98)
        attitude_clip = _metric_count(attitude_rows, "clip_frac", 0.01)
        findings.append(
            f"- ULog 侧显示，attitude 已选 run 中有 {attitude_motor_sat}/{len(attitude_rows)} 组触到 `motors_peak>=0.98`，{attitude_clip}/{len(attitude_rows)} 组出现 `clip_frac>=0.01`。"
        )

    if attitude_frontier and attitude_safe:
        safe_clip = _metric_median_preferred(attitude_safe, "active_clip_frac", "clip_frac")
        frontier_clip = _metric_median_preferred(attitude_frontier, "active_clip_frac", "clip_frac")
        safe_unalloc = _metric_median_preferred(attitude_safe, "active_max_unalloc_torque", "max_unalloc_torque")
        frontier_unalloc = _metric_median_preferred(attitude_frontier, "active_max_unalloc_torque", "max_unalloc_torque")
        if not math.isnan(frontier_clip) and not math.isnan(safe_clip) and frontier_clip > safe_clip + 0.005:
            findings.append(
                f"- 与 attitude safe 点相比，frontier 点的 `clip_frac` 中位数从 {_format_metric(safe_clip)} 抬升到 {_format_metric(frontier_clip)}。"
            )
        if not math.isnan(frontier_unalloc) and not math.isnan(safe_unalloc) and frontier_unalloc > safe_unalloc + 0.5:
            findings.append(
                f"- 与 attitude safe 点相比，frontier 点的 `max_unalloc_torque` 中位数从 {_format_metric(safe_unalloc)} 抬升到 {_format_metric(frontier_unalloc)}，更像控制分配开始受限。"
            )
        frontier_thrust = _metric_median_preferred(attitude_frontier, "active_thrust_achieved", "thrust_achieved")
        frontier_torque = _metric_median_preferred(attitude_frontier, "active_torque_achieved", "torque_achieved")
        if (
            not math.isnan(frontier_thrust)
            and not math.isnan(frontier_torque)
            and frontier_thrust >= 0.95
            and frontier_torque <= 0.80
            and (
                (not math.isnan(frontier_unalloc) and frontier_unalloc >= 1.0)
                or (not math.isnan(frontier_clip) and frontier_clip >= 0.015)
            )
        ):
            findings.append(
                f"- attitude frontier 点的 `thrust_achieved` 中位数仍约 {_format_metric(frontier_thrust)}，但 `torque_achieved` 中位数只有 {_format_metric(frontier_torque)}；这更像姿态力矩裕度先被吃掉，而不是总推力先耗尽。"
            )

    if attitude_rows and manual_rows:
        attitude_unalloc = _metric_median_preferred(attitude_rows, "active_max_unalloc_torque", "max_unalloc_torque")
        manual_unalloc = _metric_median_preferred(manual_rows, "active_max_unalloc_torque", "max_unalloc_torque")
        attitude_clip = _metric_median_preferred(attitude_rows, "active_clip_frac", "clip_frac")
        manual_clip = _metric_median_preferred(manual_rows, "active_clip_frac", "clip_frac")
        if (
            not math.isnan(attitude_unalloc)
            and not math.isnan(manual_unalloc)
            and not math.isnan(attitude_clip)
            and not math.isnan(manual_clip)
            and (attitude_unalloc > manual_unalloc + 0.5 or attitude_clip > manual_clip + 0.005)
        ):
            findings.append(
                f"- 相比 manual 链，attitude 链的 `clip_frac` / `max_unalloc_torque` 更高（中位数分别为 {_format_metric(attitude_clip)} / {_format_metric(attitude_unalloc)}，manual 为 {_format_metric(manual_clip)} / {_format_metric(manual_unalloc)}），说明其更早触到执行器或控制分配约束。"
            )

    if failure_attribution_rows:
        mode_counts: dict[str, int] = {}
        for row in failure_attribution_rows:
            mode_counts[str(row["primary_failure_mode"])] = mode_counts.get(str(row["primary_failure_mode"]), 0) + 1
        mode_text = ", ".join(f"{mode} x{count}" for mode, count in sorted(mode_counts.items(), key=lambda item: (-item[1], item[0])))
        findings.append(f"- failure attribution 已按 frontier/degraded run 落到更具体机理标签：{mode_text}。")
        sample_rows = failure_attribution_rows[:3]
        sample_text = ", ".join(
            f"{row['profile_type']}/{row['axis']}@{float(row['input_peak']):.2f}->{row['primary_failure_mode']}"
            for row in sample_rows
        )
        findings.append(f"- 例如：{sample_text}。")

    findings.append("- `safe` / `degraded` / `invalid` 是第一版 operational layering：`degraded` 表示前沿或指标明显抬升，后续仍需 sweep/pulse 与 windy rerun 复核。")

    if missing_profiles:
        gap_lines = [f"- 当前 world_filter={world_filter} 下仍缺 profile：{', '.join(missing_profiles)}。"]
    else:
        gap_lines = ["- 当前 world_filter 下的已选 run 已覆盖 baseline / step / pulse / sweep 首轮 profile，后续可补更多轴和更激进组合。"]
    if world_filter == "nominal":
        gap_lines.append("- nominal 结果已可与最新 windy fresh matrix 对照，但两类结论仍需分环境解释，不能直接混成单一边界。")
    elif world_filter == "windy":
        gap_lines.append("- 当前 windy 数据已不再局限于少量 anchor；后续若继续收敛边界，更合理的是补更细分幅值或转向机制解释。")
    else:
        gap_lines.append("- nominal 与 windy 数据当前都存在，但 wind/no-wind 仍需分开解释，不能直接混成单一边界。")

    return "\n".join(
        [
            "# Phase 3 Summary",
            "",
            "## 输出目录",
            f"- {output_dir}",
            f"- world_filter: {world_filter}",
            "",
            "## 核心发现",
            *findings,
            "",
            "## Attitude Run Summary",
            attitude_table,
            "",
            "## Manual Run Summary",
            manual_table,
            "",
            "## Axis Layers",
            layer_table,
            "",
            "## ULog Mechanism Summary",
            mechanism_table,
            "",
            "## Failure Attribution",
            attribution_table,
            "",
            "## 当前缺口",
            *gap_lines,
        ]
    )


def _svg_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _metric_range(records: list[RunRecord], attr_name: str) -> tuple[float, float]:
    values = [getattr(item, attr_name) for item in records if not math.isnan(getattr(item, attr_name))]
    if not values:
        return 0.0, 1.0
    min_value = min(values)
    max_value = max(values)
    if math.isclose(min_value, max_value):
        padding = 1.0 if math.isclose(max_value, 0.0) else abs(max_value) * 0.2
        return min_value - padding, max_value + padding
    padding = (max_value - min_value) * 0.15
    return min(0.0, min_value - padding), max_value + padding


def _map_value(value: float, input_min: float, input_max: float, output_min: float, output_max: float) -> float:
    if math.isclose(input_min, input_max):
        return (output_min + output_max) / 2.0
    ratio = (value - input_min) / (input_max - input_min)
    return output_min + ratio * (output_max - output_min)


def _svg_marker(record: RunRecord, x: float, y: float) -> str:
    fill = AXIS_COLORS.get(record.axis, "#555555")
    stroke = "#000000" if record.boundary_class == "safe" else "#f39c12"
    stroke_width = 1.5 if record.boundary_class == "safe" else 2.5
    marker = PROFILE_MARKERS.get(record.profile_type, "o")
    size = 5.5

    if record.boundary_class == "invalid":
        return (
            f'<line x1="{x - size:.1f}" y1="{y - size:.1f}" x2="{x + size:.1f}" y2="{y + size:.1f}" '
            f'stroke="{fill}" stroke-width="2.0"/>'
            f'<line x1="{x - size:.1f}" y1="{y + size:.1f}" x2="{x + size:.1f}" y2="{y - size:.1f}" '
            f'stroke="{fill}" stroke-width="2.0"/>'
        )

    if marker == "o":
        return (
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size:.1f}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{stroke_width:.1f}"/>'
        )
    if marker == "s":
        return (
            f'<rect x="{x - size:.1f}" y="{y - size:.1f}" width="{size * 2:.1f}" height="{size * 2:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"/>'
        )
    if marker == "^":
        points = f"{x:.1f},{y - size:.1f} {x - size:.1f},{y + size:.1f} {x + size:.1f},{y + size:.1f}"
        return f'<polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"/>'
    points = f"{x:.1f},{y - size:.1f} {x - size:.1f},{y:.1f} {x:.1f},{y + size:.1f} {x + size:.1f},{y:.1f}"
    return f'<polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"/>'


def _build_svg_panel(
    records: list[RunRecord],
    attr_name: str,
    title: str,
    x0: float,
    y0: float,
    panel_width: float,
    panel_height: float,
) -> str:
    plot_left = x0 + 70.0
    plot_top = y0 + 45.0
    plot_width = panel_width - 110.0
    plot_height = panel_height - 105.0
    x_min = 0.0
    x_max = max((item.input_peak for item in records), default=1.0)
    if math.isclose(x_max, 0.0):
        x_max = 1.0
    x_max *= 1.1
    y_min, y_max = _metric_range(records, attr_name)

    parts = [
        f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{panel_width:.1f}" height="{panel_height:.1f}" fill="#ffffff" stroke="#d0d7de"/>',
        f'<text x="{x0 + 20:.1f}" y="{y0 + 26:.1f}" font-size="16" font-family="monospace">{_svg_escape(title)}</text>',
        f'<line x1="{plot_left:.1f}" y1="{plot_top + plot_height:.1f}" x2="{plot_left + plot_width:.1f}" y2="{plot_top + plot_height:.1f}" stroke="#444"/>',
        f'<line x1="{plot_left:.1f}" y1="{plot_top:.1f}" x2="{plot_left:.1f}" y2="{plot_top + plot_height:.1f}" stroke="#444"/>',
        f'<text x="{plot_left + plot_width / 2.0 - 30:.1f}" y="{y0 + panel_height - 18:.1f}" font-size="12" font-family="monospace">input_peak</text>',
        f'<text x="{x0 + 10:.1f}" y="{y0 + 24:.1f}" font-size="12" font-family="monospace">{_svg_escape(attr_name)}</text>',
    ]

    for index in range(5):
        x_value = x_min + (x_max - x_min) * index / 4.0
        x_pixel = _map_value(x_value, x_min, x_max, plot_left, plot_left + plot_width)
        parts.append(
            f'<line x1="{x_pixel:.1f}" y1="{plot_top:.1f}" x2="{x_pixel:.1f}" y2="{plot_top + plot_height:.1f}" stroke="#ebeff2"/>'
        )
        parts.append(
            f'<text x="{x_pixel - 12:.1f}" y="{plot_top + plot_height + 20:.1f}" font-size="11" font-family="monospace">{x_value:.2f}</text>'
        )

    for index in range(5):
        y_value = y_min + (y_max - y_min) * index / 4.0
        y_pixel = _map_value(y_value, y_min, y_max, plot_top + plot_height, plot_top)
        parts.append(
            f'<line x1="{plot_left:.1f}" y1="{y_pixel:.1f}" x2="{plot_left + plot_width:.1f}" y2="{y_pixel:.1f}" stroke="#ebeff2"/>'
        )
        parts.append(
            f'<text x="{x0 + 8:.1f}" y="{y_pixel + 4:.1f}" font-size="11" font-family="monospace">{y_value:.2f}</text>'
        )

    for record in records:
        y_value = getattr(record, attr_name)
        if math.isnan(y_value):
            continue
        x_pixel = _map_value(record.input_peak, x_min, x_max, plot_left, plot_left + plot_width)
        y_pixel = _map_value(y_value, y_min, y_max, plot_top + plot_height, plot_top)
        parts.append(_svg_marker(record, x_pixel, y_pixel))
        if record.boundary_class in {"degraded", "invalid"}:
            label = _svg_escape(f"{record.axis}@{record.input_peak:.2f}")
            parts.append(
                f'<text x="{x_pixel + 8:.1f}" y="{y_pixel - 6:.1f}" font-size="11" font-family="monospace" fill="#333">{label}</text>'
            )

    return "\n".join(parts)


def write_chain_plot(records: list[RunRecord], chain: str, plots_dir: Path, world_filter: str) -> Path | None:
    chain_records = [item for item in records if item.input_chain == chain]
    if not chain_records:
        return None

    width = 1240.0
    height = 560.0
    left_panel = _build_svg_panel(chain_records, "tracking_error_peak", f"{chain}: input_peak -> tracking_error_peak", 20.0, 70.0, 580.0, 430.0)
    right_panel = _build_svg_panel(chain_records, "response_delay_ms", f"{chain}: input_peak -> response_delay_ms", 640.0, 70.0, 580.0, 430.0)

    legend_parts = [
        f'<text x="20" y="28" font-size="18" font-family="monospace">Phase 3 {world_filter} Summary</text>',
        '<text x="20" y="48" font-size="12" font-family="monospace">axis color: roll/pitch/yaw/throttle/composite | outline: safe=black degraded=orange invalid=x</text>',
    ]
    legend_x = 760
    legend_y = 28
    for index, (axis, color) in enumerate(AXIS_COLORS.items()):
        y = legend_y + index * 18
        legend_parts.append(f'<circle cx="{legend_x}" cy="{y}" r="5" fill="{color}" stroke="{color}"/>')
        legend_parts.append(f'<text x="{legend_x + 12}" y="{y + 4}" font-size="11" font-family="monospace">{axis}</text>')

    svg_text = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">',
            '<rect width="100%" height="100%" fill="#f8fafc"/>',
            *legend_parts,
            left_panel,
            right_panel,
            "</svg>",
        ]
    )
    output_path = plots_dir / f"{chain}_overview.svg"
    output_path.write_text(svg_text, encoding="utf-8")
    return output_path


def build_output_directory(output_dir: Path | None, world_filter: str) -> Path:
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir.resolve()

    timestamp = datetime.now(timezone.utc).astimezone()
    path = ANALYSIS_ROOT / f"{timestamp:%Y%m%d_%H%M%S}_phase3_{world_filter}"
    path.mkdir(parents=True, exist_ok=True)
    return path.resolve()


def run_analysis(artifacts_root: Path, output_dir: Path | None, skip_plots: bool, world_filter: str) -> Path:
    records = filter_records_by_world(load_run_records(artifacts_root), world_filter)
    if not records:
        raise ValueError(f"未在 {artifacts_root} 找到满足 world_filter={world_filter} 的 run artifacts。")

    selected_records = select_nominal_records(records)
    layers = classify_records(selected_records)
    analysis_dir = build_output_directory(output_dir, world_filter)
    plots_dir = analysis_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    all_rows = [item.to_row() for item in records]
    selected_rows = [item.to_row() for item in selected_records]
    nominal_rows = [item.to_row() for item in selected_records if item.status == "completed"]
    layer_rows = [item.to_row() for item in layers]
    mechanism_rows = build_mechanism_rows(selected_records)
    failure_attribution_rows = build_failure_attribution_rows(selected_records)

    _write_csv(analysis_dir / "all_runs_inventory.csv", all_rows, list(all_rows[0].keys()))
    _write_csv(analysis_dir / "selected_runs.csv", selected_rows, list(selected_rows[0].keys()))
    _write_csv(
        analysis_dir / "nominal_completed_runs.csv",
        nominal_rows,
        list((nominal_rows[0] if nominal_rows else selected_rows[0]).keys()),
    )
    _write_csv(analysis_dir / "axis_layers.csv", layer_rows, list(layer_rows[0].keys()))
    if mechanism_rows:
        _write_csv(analysis_dir / "ulog_mechanism_summary.csv", mechanism_rows, list(mechanism_rows[0].keys()))
    if failure_attribution_rows:
        _write_csv(analysis_dir / "failure_attribution.csv", failure_attribution_rows, list(failure_attribution_rows[0].keys()))

    if not skip_plots:
        write_chain_plot(selected_records, "attitude", plots_dir, world_filter)
        write_chain_plot(selected_records, "manual", plots_dir, world_filter)

    summary_text = build_summary_markdown(records, selected_records, layers, analysis_dir, world_filter)
    (analysis_dir / "summary.md").write_text(summary_text, encoding="utf-8")

    return analysis_dir


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="汇总 artifacts/runs，生成 Phase 3 第一版 nominal 分析表与图。")
    parser.add_argument(
        "--artifacts-root",
        type=Path,
        default=ARTIFACT_ROOT,
        help=f"run artifacts 根目录，默认使用 {ARTIFACT_ROOT}。",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="分析输出目录；不传时自动落到 artifacts/analysis/<timestamp>_phase3_nominal。",
    )
    parser.add_argument(
        "--world-filter",
        choices=("nominal", "windy", "all"),
        default="nominal",
        help="按 sim_world 过滤 run。默认 nominal，只纳入 sim_world=unspecified/default。",
    )
    parser.add_argument("--skip-plots", action="store_true", help="只写 CSV / Markdown，不生成 SVG 图。")
    args = parser.parse_args(argv)

    analysis_dir = run_analysis(
        args.artifacts_root.expanduser().resolve(),
        args.output_dir,
        args.skip_plots,
        args.world_filter,
    )
    print(f"analysis_dir={analysis_dir}")


if __name__ == "__main__":
    main()
