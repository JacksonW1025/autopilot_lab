from __future__ import annotations

import bisect
import math
from typing import Any

from px4_msgs.msg import VehicleStatus

from .common import RunConfig


def _float_value(value: Any, default: float = 0.0) -> float:
    if value in ("", None):
        return default
    return float(value)


def _command_value(command: dict[str, Any], channel: str) -> float:
    column_map = {
        "roll": "roll_body",
        "pitch": "pitch_body",
        "yaw": "yaw_body",
        "throttle": "thrust_z",
    }
    return _float_value(command.get(column_map[channel], 0.0))


def _actual_value(actual: dict[str, Any], channel: str) -> float:
    return _float_value(actual.get(channel, 0.0))


def _nearest_actual_values(
    command_trace: list[dict[str, Any]],
    actual_rows: list[dict[str, Any]],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    if not command_trace or not actual_rows:
        return []

    actual_times = [int(row["received_time_ns"]) for row in actual_rows]
    aligned: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for command in command_trace:
        command_time = int(command["publish_time_ns"])
        index = bisect.bisect_left(actual_times, command_time)
        candidates = []
        if index < len(actual_rows):
            candidates.append(actual_rows[index])
        if index > 0:
            candidates.append(actual_rows[index - 1])
        if not candidates:
            continue
        closest = min(candidates, key=lambda row: abs(int(row["received_time_ns"]) - command_time))
        aligned.append((command, closest))
    return aligned


def _manual_nav_state_changed(
    status_rows: list[dict[str, Any]],
    start_time_ns: int | None,
    end_time_ns: int | None,
) -> int:
    if not status_rows:
        return 1

    segment = [
        row
        for row in status_rows
        if start_time_ns is None or int(row["received_time_ns"]) >= start_time_ns
        if end_time_ns is None or int(row["received_time_ns"]) <= end_time_ns
    ]
    if not segment:
        return 1

    baseline_nav_state = int(segment[0]["nav_state"])
    return 1 if any(int(row["nav_state"]) != baseline_nav_state for row in segment[1:]) else 0


def _xy_motion_metrics(
    position_rows: list[dict[str, Any]],
    start_time_ns: int | None,
    end_time_ns: int | None,
) -> dict[str, float]:
    valid_rows = [
        row
        for row in position_rows
        if row.get("xy_valid", False) in (True, "True", "true")
        if start_time_ns is None or int(row["received_time_ns"]) >= start_time_ns
        if end_time_ns is None or int(row["received_time_ns"]) <= end_time_ns
    ]
    if not valid_rows:
        return {
            "start_xy_radius_m": math.nan,
            "end_xy_radius_m": math.nan,
            "xy_radius_peak_m": math.nan,
            "xy_displacement_peak_m": math.nan,
        }

    x0 = _float_value(valid_rows[0].get("x"))
    y0 = _float_value(valid_rows[0].get("y"))
    start_radius = math.hypot(x0, y0)
    end_radius = math.hypot(_float_value(valid_rows[-1].get("x")), _float_value(valid_rows[-1].get("y")))
    radius_peak = max(math.hypot(_float_value(row.get("x")), _float_value(row.get("y"))) for row in valid_rows)
    displacement_peak = max(
        math.hypot(_float_value(row.get("x")) - x0, _float_value(row.get("y")) - y0) for row in valid_rows
    )
    return {
        "start_xy_radius_m": round(start_radius, 3),
        "end_xy_radius_m": round(end_radius, 3),
        "xy_radius_peak_m": round(radius_peak, 3),
        "xy_displacement_peak_m": round(displacement_peak, 3),
    }


def compute_metrics(
    config: RunConfig,
    command_trace: list[dict[str, Any]],
    attitude_rows: list[dict[str, Any]],
    manual_rows: list[dict[str, Any]],
    local_position_rows: list[dict[str, Any]],
    status_rows: list[dict[str, Any]],
    start_time_ns: int | None,
    end_time_ns: int | None,
) -> dict[str, Any]:
    composite_manual = config.input_chain == "manual" and config.axis == "composite"

    if config.input_chain == "manual":
        axis_column = {"roll": "roll", "pitch": "pitch", "yaw": "yaw", "throttle": "throttle"}.get(
            config.axis, "roll"
        )
        actual_rows = manual_rows
    else:
        axis_column = {"roll": "roll", "pitch": "pitch", "yaw": "yaw"}.get(config.axis, "roll")
        actual_rows = attitude_rows

    aligned = _nearest_actual_values(command_trace, actual_rows)

    if composite_manual:
        active_channels = [
            channel
            for channel in ("roll", "pitch", "yaw", "throttle")
            if any(abs(_command_value(row, channel)) > 1e-6 for row in command_trace)
        ]
        input_peak = max(
            (abs(_command_value(row, channel)) for row in command_trace for channel in active_channels),
            default=0.0,
        )
    else:
        input_values = [_float_value(row["profile_value"]) for row in command_trace]
        input_peak = max((abs(value) for value in input_values), default=0.0)

    input_rate_peak = 0.0
    for previous, current in zip(command_trace, command_trace[1:]):
        delta_t = (_float_value(current["elapsed_s"]) - _float_value(previous["elapsed_s"]))
        if delta_t <= 0.0:
            continue
        if composite_manual:
            for channel in active_channels:
                delta_value = _command_value(current, channel) - _command_value(previous, channel)
                input_rate_peak = max(input_rate_peak, abs(delta_value / delta_t))
        else:
            delta_value = _float_value(current["profile_value"]) - _float_value(previous["profile_value"])
            input_rate_peak = max(input_rate_peak, abs(delta_value / delta_t))

    errors: list[float] = []
    if composite_manual:
        for command, actual in aligned:
            for channel in active_channels:
                errors.append(_command_value(command, channel) - _actual_value(actual, channel))
    else:
        for command, actual in aligned:
            errors.append(_float_value(command["profile_value"]) - _float_value(actual[axis_column]))

    tracking_error_peak = max((abs(value) for value in errors), default=0.0)
    tracking_error_rms = math.sqrt(sum(value * value for value in errors) / len(errors)) if errors else 0.0

    response_delay_ms = math.nan
    if config.profile_type != "baseline" and input_peak > 0.0 and actual_rows:
        threshold_candidates = [input_peak * 0.1, input_peak * 0.05, 0.002]
        thresholds: list[float] = []
        for candidate in threshold_candidates:
            if candidate > 0.0 and candidate not in thresholds:
                thresholds.append(candidate)

        for threshold in thresholds:
            if composite_manual:
                delays_ms: list[float] = []
                for channel in active_channels:
                    input_cross_time_ns = None
                    for row in command_trace:
                        if abs(_command_value(row, channel)) >= threshold:
                            input_cross_time_ns = int(row["publish_time_ns"])
                            break
                    if input_cross_time_ns is None:
                        continue
                    baseline_samples = [
                        _actual_value(row, channel) for row in actual_rows if int(row["received_time_ns"]) < input_cross_time_ns
                    ]
                    baseline_actual = sum(baseline_samples) / len(baseline_samples) if baseline_samples else 0.0
                    for row in actual_rows:
                        if int(row["received_time_ns"]) < input_cross_time_ns:
                            continue
                        actual_delta = _actual_value(row, channel) - baseline_actual
                        if abs(actual_delta) >= threshold:
                            delays_ms.append((int(row["received_time_ns"]) - input_cross_time_ns) / 1_000_000.0)
                            break
                if delays_ms:
                    response_delay_ms = min(delays_ms)
                    break
            else:
                input_cross_time_ns = None
                for row in command_trace:
                    profile_value = _float_value(row["profile_value"]) - config.bias
                    if abs(profile_value) >= threshold:
                        input_cross_time_ns = int(row["publish_time_ns"])
                        break

                if input_cross_time_ns is None:
                    continue

                baseline_samples = [
                    _float_value(row[axis_column])
                    for row in actual_rows
                    if int(row["received_time_ns"]) < input_cross_time_ns
                ]
                baseline_actual = sum(baseline_samples) / len(baseline_samples) if baseline_samples else 0.0

                crossed = False
                for row in actual_rows:
                    if int(row["received_time_ns"]) < input_cross_time_ns:
                        continue
                    actual_delta = _float_value(row[axis_column]) - baseline_actual
                    if abs(actual_delta) >= threshold:
                        response_delay_ms = (int(row["received_time_ns"]) - input_cross_time_ns) / 1_000_000.0
                        crossed = True
                        break

                if crossed:
                    break

    failsafe_event = 0
    unexpected_nav_state = 0
    if status_rows:
        for row in status_rows:
            if str(row.get("failsafe", "False")).lower() == "true" or int(row.get("failure_detector_status", 0)) != 0:
                failsafe_event = 1
                break

        if config.input_chain == "manual":
            unexpected_nav_state = _manual_nav_state_changed(status_rows, start_time_ns, end_time_ns)
        elif start_time_ns is None:
            unexpected_nav_state = 1
        else:
            landing_guard_ns = end_time_ns or (start_time_ns + int(config.active_duration_s * 1e9))
            for row in status_rows:
                received_time_ns = int(row["received_time_ns"])
                if received_time_ns < start_time_ns:
                    continue
                if received_time_ns > landing_guard_ns:
                    break
                if int(row["nav_state"]) != VehicleStatus.NAVIGATION_STATE_OFFBOARD:
                    unexpected_nav_state = 1
                    break

    xy_motion = _xy_motion_metrics(local_position_rows, start_time_ns, end_time_ns)

    return {
        "run_id": "",
        "input_chain": config.input_chain,
        "profile_type": config.profile_type,
        "axis": config.axis,
        "input_peak": round(input_peak, 6),
        "input_rate_peak": round(input_rate_peak, 6),
        "tracking_error_peak": round(tracking_error_peak, 6),
        "tracking_error_rms": round(tracking_error_rms, 6),
        "response_delay_ms": response_delay_ms if math.isnan(response_delay_ms) else round(response_delay_ms, 3),
        "nav_state_change": unexpected_nav_state,
        "failsafe_event": failsafe_event,
        "start_xy_radius_m": xy_motion["start_xy_radius_m"],
        "end_xy_radius_m": xy_motion["end_xy_radius_m"],
        "xy_radius_peak_m": xy_motion["xy_radius_peak_m"],
        "xy_displacement_peak_m": xy_motion["xy_displacement_peak_m"],
        "ulog_saturation_metric": "pending_ulog_parse",
        "ulog_parse_status": "missing_parser",
    }
