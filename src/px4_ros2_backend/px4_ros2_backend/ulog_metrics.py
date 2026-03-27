from __future__ import annotations

import bisect
import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

try:
    from pyulog import ULog
except ImportError:  # pragma: no cover - runtime dependency
    ULog = None


SIGNIFICANT_UNALLOC_TORQUE_THRESHOLD = 0.5
PREFAILSAFE_LOOKBACK_US = 2_000_000
ACTIVE_PHASES = {
    "baseline": {"baseline_hold"},
    "step": {"step_active"},
    "pulse": {"pulse_active"},
    "sweep": {"sweep_active"},
}


@dataclass(slots=True)
class ULogWindowContext:
    active_start_us: int | None = None
    active_end_us: int | None = None
    failure_time_us: int | None = None
    prefailsafe_start_us: int | None = None
    prefailsafe_end_us: int | None = None


def summarize_ulog(
    ulog_path: str | None,
    window_context: ULogWindowContext | None = None,
    run_context: dict[str, Any] | None = None,
) -> dict[str, str]:
    if not ulog_path:
        return {
            "ulog_saturation_metric": "ulog_missing",
            "ulog_parse_status": "missing_log",
        }
    if ULog is None:
        return {
            "ulog_saturation_metric": "pending_ulog_parse",
            "ulog_parse_status": "missing_parser",
        }

    path = Path(ulog_path).expanduser()
    if not path.exists():
        return {
            "ulog_saturation_metric": "ulog_missing",
            "ulog_parse_status": "missing_log",
        }

    try:
        ulog = ULog(str(path))
    except Exception as exc:  # pragma: no cover - parser failure path
        return {
            "ulog_saturation_metric": f"parse_error:{type(exc).__name__}",
            "ulog_parse_status": "parse_error",
        }

    if window_context is None and run_context is not None:
        window_context = build_window_context_from_ulog(ulog, run_context)

    metric_parts: list[str] = []

    motor_peak, clip_fraction = _actuator_motor_metrics(ulog)
    if not math.isnan(motor_peak):
        metric_parts.append(f"motors_peak={motor_peak:.3f}")
    if not math.isnan(clip_fraction):
        metric_parts.append(f"clip_frac={clip_fraction:.3f}")

    thrust_achieved, torque_achieved, max_unallocated_torque = _allocator_metrics(ulog)
    if not math.isnan(thrust_achieved):
        metric_parts.append(f"thrust_achieved={thrust_achieved:.3f}")
    if not math.isnan(torque_achieved):
        metric_parts.append(f"torque_achieved={torque_achieved:.3f}")
    if not math.isnan(max_unallocated_torque):
        metric_parts.append(f"max_unalloc_torque={max_unallocated_torque:.3f}")

    if window_context is not None:
        active_metrics = _active_window_metrics(ulog, window_context.active_start_us, window_context.active_end_us)
        for key, value in active_metrics.items():
            if not math.isnan(value):
                metric_parts.append(f"{key}={value:.3f}")

        prefailsafe_metrics = _prefailsafe_metrics(
            ulog,
            window_context.prefailsafe_start_us,
            window_context.prefailsafe_end_us,
        )
        for key, value in prefailsafe_metrics.items():
            if not math.isnan(value):
                metric_parts.append(f"{key}={value:.3f}")

    if not metric_parts:
        return {
            "ulog_saturation_metric": "ulog_topics_missing",
            "ulog_parse_status": "no_relevant_topics",
        }

    return {
        "ulog_saturation_metric": ";".join(metric_parts),
        "ulog_parse_status": "parsed",
    }


def summarize_run_ulog(run_dir: Path, manifest: dict[str, Any]) -> dict[str, str]:
    px4_log_path = manifest.get("px4_log_path")
    return summarize_ulog(
        str(px4_log_path) if px4_log_path else None,
        window_context=build_window_context_from_artifact(run_dir, manifest),
        run_context=manifest,
    )


def _dataset(ulog: ULog, name: str) -> Any | None:
    for item in ulog.data_list:
        if item.name == name:
            return item
    return None


def _active_numeric_columns(data: dict[str, Any], prefix: str) -> list[np.ndarray]:
    columns: list[np.ndarray] = []
    for key in sorted(data):
        if not key.startswith(prefix):
            continue
        series = np.asarray(data[key], dtype=float)
        if series.size == 0 or np.all(np.isnan(series)):
            continue
        columns.append(series)
    return columns


def _window_mask(timestamps: np.ndarray, start_us: int | None, end_us: int | None) -> np.ndarray:
    mask = np.ones(timestamps.shape, dtype=bool)
    if start_us is not None:
        mask &= timestamps >= start_us
    if end_us is not None:
        mask &= timestamps <= end_us
    return mask


def _windowed_stack(columns: list[np.ndarray], mask: np.ndarray) -> np.ndarray | None:
    if not columns:
        return None
    stacked = np.vstack(columns)
    if stacked.shape[1] != mask.shape[0]:
        return None
    return stacked[:, mask]


def _first_rel_time_s(timestamps: np.ndarray, start_us: int | None, mask: np.ndarray) -> float:
    if start_us is None:
        return math.nan
    if not np.any(mask):
        return math.nan
    first_timestamp = float(timestamps[np.argmax(mask)])
    return (first_timestamp - float(start_us)) / 1_000_000.0


def _actuator_motor_metrics(ulog: ULog) -> tuple[float, float]:
    motors = _dataset(ulog, "actuator_motors")
    if motors is None:
        return math.nan, math.nan

    controls = _active_numeric_columns(motors.data, "control[")
    if not controls:
        return math.nan, math.nan

    stacked = np.vstack(controls)
    motor_peak = float(np.nanmax(np.abs(stacked)))
    clip_fraction = float(np.mean(np.any(np.abs(stacked) >= 0.98, axis=0)))
    return motor_peak, clip_fraction


def _allocator_metrics(ulog: ULog) -> tuple[float, float, float]:
    allocator = _dataset(ulog, "control_allocator_status")
    if allocator is None:
        return math.nan, math.nan, math.nan

    data = allocator.data
    thrust_achieved = _mean_if_present(data.get("thrust_setpoint_achieved"))
    torque_achieved = _mean_if_present(data.get("torque_setpoint_achieved"))

    unallocated_axes = []
    for key in sorted(data):
        if key.startswith("unallocated_torque["):
            unallocated_axes.append(np.asarray(data[key], dtype=float))
    if unallocated_axes:
        max_unallocated_torque = float(np.nanmax(np.abs(np.vstack(unallocated_axes))))
    else:
        max_unallocated_torque = math.nan

    return thrust_achieved, torque_achieved, max_unallocated_torque


def _mean_if_present(value: Any) -> float:
    if value is None:
        return math.nan
    array = np.asarray(value, dtype=float)
    if array.size == 0 or np.all(np.isnan(array)):
        return math.nan
    return float(np.nanmean(array))


def _min_if_present(value: Any) -> float:
    if value is None:
        return math.nan
    array = np.asarray(value, dtype=float)
    if array.size == 0 or np.all(np.isnan(array)):
        return math.nan
    return float(np.nanmin(array))


def _active_window_metrics(ulog: ULog, start_us: int | None, end_us: int | None) -> dict[str, float]:
    metrics = {
        "active_clip_frac": math.nan,
        "active_max_unalloc_torque": math.nan,
        "active_torque_achieved": math.nan,
        "active_torque_achieved_min": math.nan,
        "active_thrust_achieved": math.nan,
        "active_thrust_achieved_min": math.nan,
        "first_clip_rel_s": math.nan,
        "first_unalloc_rel_s": math.nan,
    }
    if start_us is None or end_us is None or end_us < start_us:
        return metrics

    motors = _dataset(ulog, "actuator_motors")
    if motors is not None:
        timestamps = np.asarray(motors.data.get("timestamp"), dtype=float)
        controls = _active_numeric_columns(motors.data, "control[")
        if timestamps.size > 0 and controls:
            window = _window_mask(timestamps, start_us, end_us)
            stacked = _windowed_stack(controls, window)
            if stacked is not None and stacked.size > 0:
                clip_mask = np.any(np.abs(stacked) >= 0.98, axis=0)
                metrics["active_clip_frac"] = float(np.mean(clip_mask))
                metrics["first_clip_rel_s"] = _first_rel_time_s(timestamps[window], start_us, clip_mask)

    allocator = _dataset(ulog, "control_allocator_status")
    if allocator is not None:
        timestamps = np.asarray(allocator.data.get("timestamp"), dtype=float)
        if timestamps.size > 0:
            window = _window_mask(timestamps, start_us, end_us)
            if np.any(window):
                torque = np.asarray(allocator.data.get("torque_setpoint_achieved"), dtype=float)
                thrust = np.asarray(allocator.data.get("thrust_setpoint_achieved"), dtype=float)
                if torque.size == timestamps.size:
                    metrics["active_torque_achieved"] = _mean_if_present(torque[window])
                    metrics["active_torque_achieved_min"] = _min_if_present(torque[window])
                if thrust.size == timestamps.size:
                    metrics["active_thrust_achieved"] = _mean_if_present(thrust[window])
                    metrics["active_thrust_achieved_min"] = _min_if_present(thrust[window])

                unallocated_axes = []
                for key in sorted(allocator.data):
                    if key.startswith("unallocated_torque["):
                        series = np.asarray(allocator.data[key], dtype=float)
                        if series.size == timestamps.size:
                            unallocated_axes.append(series[window])
                if unallocated_axes:
                    stacked = np.vstack(unallocated_axes)
                    max_abs = np.max(np.abs(stacked), axis=0)
                    metrics["active_max_unalloc_torque"] = float(np.nanmax(max_abs))
                    significant = max_abs >= SIGNIFICANT_UNALLOC_TORQUE_THRESHOLD
                    metrics["first_unalloc_rel_s"] = _first_rel_time_s(timestamps[window], start_us, significant)

    return metrics


def _prefailsafe_metrics(ulog: ULog, start_us: int | None, end_us: int | None) -> dict[str, float]:
    metrics = {
        "prefailsafe_max_unalloc_torque": math.nan,
        "prefailsafe_clip_frac": math.nan,
    }
    if start_us is None or end_us is None or end_us < start_us:
        return metrics

    allocator = _dataset(ulog, "control_allocator_status")
    if allocator is not None:
        timestamps = np.asarray(allocator.data.get("timestamp"), dtype=float)
        if timestamps.size > 0:
            window = _window_mask(timestamps, start_us, end_us)
            if np.any(window):
                unallocated_axes = []
                for key in sorted(allocator.data):
                    if key.startswith("unallocated_torque["):
                        series = np.asarray(allocator.data[key], dtype=float)
                        if series.size == timestamps.size:
                            unallocated_axes.append(series[window])
                if unallocated_axes:
                    metrics["prefailsafe_max_unalloc_torque"] = float(np.nanmax(np.abs(np.vstack(unallocated_axes))))

    motors = _dataset(ulog, "actuator_motors")
    if motors is not None:
        timestamps = np.asarray(motors.data.get("timestamp"), dtype=float)
        controls = _active_numeric_columns(motors.data, "control[")
        if timestamps.size > 0 and controls:
            window = _window_mask(timestamps, start_us, end_us)
            stacked = _windowed_stack(controls, window)
            if stacked is not None and stacked.size > 0:
                metrics["prefailsafe_clip_frac"] = float(np.mean(np.any(np.abs(stacked) >= 0.98, axis=0)))

    return metrics


def build_window_context_from_ulog(ulog: ULog, run_context: dict[str, Any]) -> ULogWindowContext:
    input_chain = str(run_context.get("input_chain", ""))
    profile_type = str(run_context.get("profile_type", ""))
    profile_params = run_context.get("profile_params", {}) or {}
    if not isinstance(profile_params, dict):
        profile_params = {}

    active_start_us, active_end_us = _active_window_from_ulog(ulog, input_chain, profile_type, profile_params)
    failure_time_us = _failure_time_from_ulog(ulog, active_start_us)
    prefailsafe_start_us = None
    prefailsafe_end_us = None
    if failure_time_us is not None:
        prefailsafe_end_us = failure_time_us
        prefailsafe_start_us = max(active_start_us or failure_time_us, failure_time_us - PREFAILSAFE_LOOKBACK_US)

    return ULogWindowContext(
        active_start_us=active_start_us,
        active_end_us=active_end_us,
        failure_time_us=failure_time_us,
        prefailsafe_start_us=prefailsafe_start_us,
        prefailsafe_end_us=prefailsafe_end_us,
    )


def _active_window_from_ulog(
    ulog: ULog,
    input_chain: str,
    profile_type: str,
    profile_params: dict[str, Any],
) -> tuple[int | None, int | None]:
    signal_timestamps, signal_values, expected_peak = _command_signal_from_ulog(ulog, input_chain, profile_params)
    if signal_timestamps.size == 0 or signal_values.size == 0 or expected_peak <= 0.0:
        return None, None

    threshold = max(0.01, expected_peak * 0.2)
    active_indices = np.flatnonzero(signal_values >= threshold)
    if active_indices.size == 0:
        return None, None

    if profile_type == "baseline":
        return int(signal_timestamps[0]), int(signal_timestamps[-1])
    return int(signal_timestamps[active_indices[0]]), int(signal_timestamps[active_indices[-1]])


def _command_signal_from_ulog(
    ulog: ULog,
    input_chain: str,
    profile_params: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray, float]:
    axis = str(profile_params.get("axis", ""))
    amplitude = abs(float(profile_params.get("amplitude", 0.0) or 0.0))

    if input_chain == "manual":
        dataset = _dataset(ulog, "manual_control_setpoint")
        if dataset is None:
            return np.array([], dtype=float), np.array([], dtype=float), 0.0
        field_map = {
            "roll": ("roll", amplitude),
            "pitch": ("pitch", amplitude),
            "yaw": ("yaw", amplitude),
            "throttle": ("throttle", amplitude),
        }
        timestamps = np.asarray(dataset.data.get("timestamp"), dtype=float)
        if axis == "composite":
            components = [
                ("roll", abs(float(profile_params.get("roll_amplitude", 0.0) or 0.0))),
                ("pitch", abs(float(profile_params.get("pitch_amplitude", 0.0) or 0.0))),
                ("yaw", abs(float(profile_params.get("yaw_amplitude", 0.0) or 0.0))),
                ("throttle", abs(float(profile_params.get("throttle", 0.0) or 0.0))),
            ]
            signals = [
                np.abs(np.asarray(dataset.data.get(field), dtype=float))
                for field, scale in components
                if scale > 0.0 and field in dataset.data
            ]
            expected_peak = max((scale for _, scale in components), default=0.0)
        else:
            field, expected_peak = field_map.get(axis, ("roll", amplitude))
            signals = [np.abs(np.asarray(dataset.data.get(field), dtype=float))]
        if not signals or timestamps.size == 0:
            return np.array([], dtype=float), np.array([], dtype=float), 0.0
        stacked = np.vstack(signals)
        return timestamps, np.nanmax(stacked, axis=0), expected_peak

    dataset = _dataset(ulog, "vehicle_attitude_setpoint")
    if dataset is None:
        return np.array([], dtype=float), np.array([], dtype=float), 0.0
    timestamps = np.asarray(dataset.data.get("timestamp"), dtype=float)
    field_map = {
        "roll": ("roll_body", amplitude),
        "pitch": ("pitch_body", amplitude),
        "yaw": ("yaw_body", amplitude),
    }
    if axis == "composite":
        components = [
            ("roll_body", abs(float(profile_params.get("roll_amplitude", 0.0) or 0.0))),
            ("pitch_body", abs(float(profile_params.get("pitch_amplitude", 0.0) or 0.0))),
            ("yaw_body", abs(float(profile_params.get("yaw_amplitude", 0.0) or 0.0))),
        ]
        signals = [
            np.abs(np.asarray(dataset.data.get(field), dtype=float))
            for field, scale in components
            if scale > 0.0 and field in dataset.data
        ]
        expected_peak = max((scale for _, scale in components), default=0.0)
    else:
        field, expected_peak = field_map.get(axis, ("roll_body", amplitude))
        if field not in dataset.data:
            return np.array([], dtype=float), np.array([], dtype=float), 0.0
        signals = [np.abs(np.asarray(dataset.data.get(field), dtype=float))]
    if not signals or timestamps.size == 0:
        return np.array([], dtype=float), np.array([], dtype=float), 0.0
    stacked = np.vstack(signals)
    return timestamps, np.nanmax(stacked, axis=0), expected_peak


def _failure_time_from_ulog(ulog: ULog, active_start_us: int | None) -> int | None:
    status = _dataset(ulog, "vehicle_status")
    if status is None:
        return None
    timestamps = np.asarray(status.data.get("timestamp"), dtype=float)
    if timestamps.size == 0:
        return None
    failsafe = np.asarray(status.data.get("failsafe"), dtype=float) if "failsafe" in status.data else None
    failure_detector = (
        np.asarray(status.data.get("failure_detector_status"), dtype=float)
        if "failure_detector_status" in status.data
        else None
    )
    for index, timestamp in enumerate(timestamps):
        if active_start_us is not None and timestamp < active_start_us:
            continue
        failsafe_hit = failsafe is not None and index < failsafe.size and failsafe[index] > 0.5
        detector_hit = failure_detector is not None and index < failure_detector.size and failure_detector[index] > 0.0
        if failsafe_hit or detector_hit:
            return int(timestamp)
    return None


def build_window_context_from_artifact(run_dir: Path, manifest: dict[str, Any]) -> ULogWindowContext:
    px4_log_path = manifest.get("px4_log_path")
    if not px4_log_path or ULog is None:
        return ULogWindowContext()
    path = Path(str(px4_log_path)).expanduser()
    if not path.exists():
        return ULogWindowContext()
    telemetry_dir = run_dir / "telemetry"
    input_profile_path = telemetry_dir / "input_profile.csv"
    status_path = telemetry_dir / "vehicle_status.csv"
    if not input_profile_path.exists() or not status_path.exists():
        return ULogWindowContext()
    input_rows = _read_csv_rows(input_profile_path)
    status_rows = _read_csv_rows(status_path)
    try:
        ulog = ULog(str(path))
    except Exception:
        return ULogWindowContext()
    return build_window_context_from_aligned_events(ulog, manifest, input_rows, status_rows)


def build_window_context_from_rows(
    input_rows: list[dict[str, Any]],
    profile_type: str,
    reference_rows: list[dict[str, int]],
    status_rows: list[dict[str, Any]],
) -> ULogWindowContext:
    if not input_rows or not reference_rows:
        return ULogWindowContext()

    active_phases = ACTIVE_PHASES.get(profile_type, set())
    active_rows = [row for row in input_rows if str(row.get("phase", "")) in active_phases]
    if not active_rows:
        return ULogWindowContext()

    active_start_ns = min(int(row["publish_time_ns"]) for row in active_rows)
    active_end_ns = max(int(row["publish_time_ns"]) for row in active_rows)
    active_start_us = _nearest_px4_timestamp_us(reference_rows, active_start_ns)
    active_end_us = _nearest_px4_timestamp_us(reference_rows, active_end_ns)
    failure_time_us = _first_failure_timestamp_us(status_rows, active_start_us)
    prefailsafe_start_us = None
    prefailsafe_end_us = None
    if failure_time_us is not None:
        prefailsafe_end_us = failure_time_us
        prefailsafe_start_us = max(active_start_us or failure_time_us, failure_time_us - PREFAILSAFE_LOOKBACK_US)

    return ULogWindowContext(
        active_start_us=active_start_us,
        active_end_us=active_end_us,
        failure_time_us=failure_time_us,
        prefailsafe_start_us=prefailsafe_start_us,
        prefailsafe_end_us=prefailsafe_end_us,
    )


def build_window_context_from_aligned_events(
    ulog: ULog,
    run_context: dict[str, Any],
    input_rows: list[dict[str, Any]],
    status_rows: list[dict[str, Any]],
) -> ULogWindowContext:
    profile_type = str(run_context.get("profile_type", ""))
    active_phases = ACTIVE_PHASES.get(profile_type, set())
    active_rows = [row for row in input_rows if str(row.get("phase", "")) in active_phases]
    if not active_rows:
        return build_window_context_from_ulog(ulog, run_context)

    offset_us = _estimate_ulog_offset_us(ulog, run_context, status_rows)
    if offset_us is None:
        return build_window_context_from_ulog(ulog, run_context)

    active_start_ns = min(int(row["publish_time_ns"]) for row in active_rows)
    active_end_ns = max(int(row["publish_time_ns"]) for row in active_rows)
    active_start_us = int((active_start_ns / 1000.0) + offset_us)
    active_end_us = int((active_end_ns / 1000.0) + offset_us)
    failure_time_us = _failure_time_from_ulog(ulog, active_start_us)
    prefailsafe_start_us = None
    prefailsafe_end_us = None
    if failure_time_us is not None:
        prefailsafe_end_us = failure_time_us
        prefailsafe_start_us = max(active_start_us, failure_time_us - PREFAILSAFE_LOOKBACK_US)

    return ULogWindowContext(
        active_start_us=active_start_us,
        active_end_us=active_end_us,
        failure_time_us=failure_time_us,
        prefailsafe_start_us=prefailsafe_start_us,
        prefailsafe_end_us=prefailsafe_end_us,
    )


def _read_csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _load_reference_rows(telemetry_dir: Path) -> list[dict[str, int]]:
    candidates = []
    for name in ("vehicle_attitude.csv", "vehicle_local_position.csv", "manual_control_setpoint.csv", "vehicle_status.csv"):
        path = telemetry_dir / name
        if path.exists():
            candidates = _read_csv_rows(path)
            if candidates:
                break
    reference_rows: list[dict[str, int]] = []
    for row in candidates:
        try:
            reference_rows.append(
                {
                    "received_time_ns": int(row["received_time_ns"]),
                    "timestamp_us": int(row["timestamp"]),
                }
            )
        except (KeyError, TypeError, ValueError):
            continue
    reference_rows.sort(key=lambda item: item["received_time_ns"])
    return reference_rows


def _nearest_px4_timestamp_us(reference_rows: list[dict[str, int]], received_time_ns: int) -> int | None:
    if not reference_rows:
        return None
    times = [row["received_time_ns"] for row in reference_rows]
    index = bisect.bisect_left(times, received_time_ns)
    candidates: list[dict[str, int]] = []
    if index < len(reference_rows):
        candidates.append(reference_rows[index])
    if index > 0:
        candidates.append(reference_rows[index - 1])
    if not candidates:
        return None
    closest = min(candidates, key=lambda row: abs(row["received_time_ns"] - received_time_ns))
    return closest["timestamp_us"]


def _first_failure_timestamp_us(status_rows: list[dict[str, Any]], active_start_us: int | None) -> int | None:
    for row in status_rows:
        try:
            timestamp_us = int(row["timestamp"])
        except (KeyError, TypeError, ValueError):
            continue
        if active_start_us is not None and timestamp_us < active_start_us:
            continue
        failsafe = str(row.get("failsafe", "False")).lower() == "true"
        try:
            failure_detector = int(row.get("failure_detector_status", 0)) != 0
        except ValueError:
            failure_detector = False
        if failsafe or failure_detector:
            return timestamp_us
    return None


def _estimate_ulog_offset_us(ulog: ULog, run_context: dict[str, Any], status_rows: list[dict[str, Any]]) -> float | None:
    telemetry_anchor_ns = _telemetry_anchor_received_ns(status_rows, run_context)
    ulog_anchor_us = _ulog_anchor_timestamp_us(ulog, run_context)
    if telemetry_anchor_ns is None or ulog_anchor_us is None:
        return None
    return float(ulog_anchor_us) - (float(telemetry_anchor_ns) / 1000.0)


def _target_nav_state(run_context: dict[str, Any]) -> int | None:
    input_chain = str(run_context.get("input_chain", ""))
    profile_params = run_context.get("profile_params", {}) or {}
    if not isinstance(profile_params, dict):
        profile_params = {}
    manual_mode = str(profile_params.get("manual_mode", "echo"))
    if input_chain == "attitude":
        return 14
    if input_chain == "manual" and manual_mode == "flight":
        return 2
    return None


def _telemetry_anchor_received_ns(status_rows: list[dict[str, Any]], run_context: dict[str, Any]) -> int | None:
    target_nav_state = _target_nav_state(run_context)
    for row in status_rows:
        try:
            arming_state = int(row.get("arming_state", 0))
            nav_state = int(row.get("nav_state", -1))
            received_time_ns = int(row["received_time_ns"])
        except (KeyError, TypeError, ValueError):
            continue
        if target_nav_state is not None and nav_state == target_nav_state and arming_state == 2:
            return received_time_ns
    for row in status_rows:
        try:
            arming_state = int(row.get("arming_state", 0))
            received_time_ns = int(row["received_time_ns"])
        except (KeyError, TypeError, ValueError):
            continue
        if arming_state == 2:
            return received_time_ns
    return None


def _ulog_anchor_timestamp_us(ulog: ULog, run_context: dict[str, Any]) -> int | None:
    status = _dataset(ulog, "vehicle_status")
    if status is None:
        return None
    timestamps = np.asarray(status.data.get("timestamp"), dtype=float)
    if timestamps.size == 0:
        return None
    arming_state = np.asarray(status.data.get("arming_state"), dtype=float)
    nav_state = np.asarray(status.data.get("nav_state"), dtype=float)
    target_nav_state = _target_nav_state(run_context)
    for index, timestamp in enumerate(timestamps):
        armed = index < arming_state.size and arming_state[index] >= 2
        nav_match = target_nav_state is None or (index < nav_state.size and int(nav_state[index]) == target_nav_state)
        if armed and nav_match:
            return int(timestamp)
    for index, timestamp in enumerate(timestamps):
        if index < arming_state.size and arming_state[index] >= 2:
            return int(timestamp)
    return None
