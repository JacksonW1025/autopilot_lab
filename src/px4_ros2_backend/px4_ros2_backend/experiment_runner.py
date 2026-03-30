from __future__ import annotations

import argparse
import math
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import rclpy
from fep_core.milestone import capability_level, milestone_id, schema_version
from fep_core.mav_params import close_mavlink, connect_mavlink, set_parameters, snapshot_parameters
from rclpy.executors import SingleThreadedExecutor

from .artifacts import (
    capture_host_snapshot,
    ensure_run_directories,
    resolve_ulog_path,
    snapshot_ulog_files,
    write_single_row_csv,
    write_rows_csv,
    write_yaml,
)
from .attitude_injector import AttitudeInjector
from .manual_input_injector import ManualInputInjector
from .rate_injector import RateInjector
from .common import (
    RECORDED_TOPICS,
    RunConfig,
    ensure_clock_bridge,
    load_run_config,
    read_clock_topic_advancing,
    read_clock_topic_available,
    stop_clock_bridge,
)
from .metrics import compute_metrics
from .telemetry_recorder import TelemetryRecorder
from .ulog_metrics import summarize_ulog

PX4_PARAM_MASTER_DEFAULT = "udp:127.0.0.1:14550"
MANUAL_MOTION_THRESHOLD_EPSILON = 1e-3


def _preflight_checks() -> tuple[list[str], bool]:
    anomalies: list[str] = []
    if not read_clock_topic_available():
        anomalies.append("clock_missing")
        return anomalies, False
    if not read_clock_topic_advancing():
        anomalies.append("clock_not_advancing")
        return anomalies, False
    return anomalies, True


def _prepare_px4_parameters(config: RunConfig) -> tuple[Any | None, dict[str, Any], dict[str, Any], list[str]]:
    parameter_names = list(dict.fromkeys(config.controlled_parameters_for_backend("px4")))
    parameter_names.extend(
        name for name in config.parameter_overrides_for_backend("px4") if name not in parameter_names
    )
    if not parameter_names:
        return None, {}, {}, []

    anomalies: list[str] = []
    master = None
    before: dict[str, Any] = {}
    after_apply: dict[str, Any] = {}
    try:
        master = connect_mavlink(str(config.extras.get("px4_param_master_uri", PX4_PARAM_MASTER_DEFAULT)), timeout_s=8.0)
        before = snapshot_parameters(master, parameter_names, timeout_s=2.0)
        overrides = config.parameter_overrides_for_backend("px4")
        if overrides:
            apply_results = set_parameters(master, overrides, timeout_s=2.0)
            failed = [name for name, ok in apply_results.items() if not ok]
            if failed:
                anomalies.append(f"parameter_apply_failed:{','.join(failed)}")
            after_apply = snapshot_parameters(master, parameter_names, timeout_s=2.0)
        else:
            after_apply = dict(before)
    except Exception as exc:
        anomalies.append(f"parameter_session_unavailable:{type(exc).__name__}")
        close_mavlink(master)
        return None, before, after_apply, anomalies

    return master, before, after_apply, anomalies


def _restore_px4_parameters(master: Any | None, snapshot_before: dict[str, Any]) -> list[str]:
    if master is None or not snapshot_before:
        return []
    restore_values = {name: value for name, value in snapshot_before.items() if value not in ("", None)}
    if not restore_values:
        return []
    try:
        results = set_parameters(master, restore_values, timeout_s=2.0)
    except Exception as exc:
        return [f"parameter_restore_failed:{type(exc).__name__}"]

    failed = [name for name, ok in results.items() if not ok]
    if failed:
        return [f"parameter_restore_failed:{','.join(failed)}"]
    return []


def _mechanism_flags(metrics: dict[str, Any], anomalies: list[str]) -> list[str]:
    flags: list[str] = []
    if metrics.get("failsafe_event") == 1:
        flags.append("failsafe")
    if metrics.get("nav_state_change") == 1:
        flags.append("mode_transition_unexpected")
    if any(item.startswith("parameter_") for item in anomalies):
        flags.append("parameter_session_issue")
    if float(metrics.get("clip_frac", 0.0) or 0.0) >= 0.015:
        flags.append("motor_clipping")
    if float(metrics.get("max_unalloc_torque", 0.0) or 0.0) >= 0.5:
        flags.append("allocator_unallocated_torque")
    if float(metrics.get("torque_achieved", 1.0) or 1.0) <= 0.85:
        flags.append("torque_achieved_low")
    if float(metrics.get("xy_displacement_peak_m", 0.0) or 0.0) >= 15.0:
        flags.append("xy_drift_high")
    if float(metrics.get("tracking_error_peak", 0.0) or 0.0) >= 0.25:
        flags.append("tracking_error_high")
    if float(metrics.get("response_delay_ms", 0.0) or 0.0) >= 250.0:
        flags.append("response_delay_high")
    return flags


def _stress_class(metrics: dict[str, Any], run_status: str, mechanism_flags: list[str]) -> str:
    if run_status != "completed" or metrics.get("failsafe_event") == 1:
        return "saturated"
    if any(flag in mechanism_flags for flag in {"motor_clipping", "allocator_unallocated_torque", "xy_drift_high"}):
        return "saturated"
    if any(flag in mechanism_flags for flag in {"tracking_error_high", "response_delay_high", "torque_achieved_low"}):
        return "stressed"
    return "nominal"


def _oracle_decision(
    config: RunConfig,
    metrics: dict[str, Any],
    anomalies: list[str],
    run_status: str,
    mechanism_flags: list[str],
) -> tuple[int, str]:
    if run_status != "completed":
        return 0, f"run_status:{run_status}"
    if metrics.get("failsafe_event") == 1:
        return 0, "failsafe_event"
    if metrics.get("nav_state_change") == 1:
        return 0, "unexpected_mode_transition"
    if any(
        item
        in {
            "ground_clearance_low",
            "profile_clearance_low",
            "takeoff_clearance_timeout",
            "manual_motion_not_observed",
            "manual_motion_window_missing",
            "manual_control_not_enabled",
            "manual_posctl_not_reached",
            "manual_echo_invalid",
            "prestart_xy_radius_excessive",
        }
        for item in anomalies
    ):
        return 0, "runtime_gate_failed"

    if config.resolved_study_layer == "attitude_explicit":
        if float(metrics.get("tracking_error_peak", 0.0) or 0.0) >= float(
            config.extras.get("oracle_attitude_tracking_error_peak_limit", 0.35)
        ):
            return 0, "attitude_tracking_error_peak_high"
        if float(metrics.get("tracking_error_rms", 0.0) or 0.0) >= float(
            config.extras.get("oracle_attitude_tracking_error_rms_limit", 0.20)
        ):
            return 0, "attitude_tracking_error_rms_high"
        if float(metrics.get("response_delay_ms", 0.0) or 0.0) >= float(
            config.extras.get("oracle_attitude_response_delay_ms_limit", 400.0)
        ):
            return 0, "attitude_response_delay_high"
    elif config.resolved_study_layer == "manual_whole_loop":
        if "xy_drift_high" in mechanism_flags and float(metrics.get("xy_displacement_peak_m", 0.0) or 0.0) >= float(
            config.extras.get("oracle_manual_xy_displacement_limit_m", 25.0)
        ):
            return 0, "manual_xy_drift_high"
    else:
        if float(metrics.get("tracking_error_peak", 0.0) or 0.0) >= float(
            config.extras.get("oracle_rate_tracking_error_peak_limit", 0.60)
        ):
            return 0, "rate_tracking_error_peak_high"
        if float(metrics.get("tracking_error_rms", 0.0) or 0.0) >= float(
            config.extras.get("oracle_rate_tracking_error_rms_limit", 0.30)
        ):
            return 0, "rate_tracking_error_rms_high"
        if float(metrics.get("response_delay_ms", 0.0) or 0.0) >= float(
            config.extras.get("oracle_rate_response_delay_ms_limit", 250.0)
        ):
            return 0, "rate_response_delay_high"

    return 1, "valid"


def _rate_layer_recommendation(
    config: RunConfig,
    oracle_valid: int,
    mechanism_flags: list[str],
) -> tuple[int, list[str]]:
    reasons = list(config.rate_layer_recommended_reasons())
    if config.resolved_study_layer == "attitude_explicit" and oracle_valid == 0 and not mechanism_flags:
        reasons.append("attitude_difference_unexplained_by_current_mechanisms")
    if config.resolved_study_layer == "attitude_explicit" and "tracking_error_high" in mechanism_flags and (
        "parameter_group_is_rate_related" in reasons
    ):
        reasons.append("attitude_tracking_difference_under_rate_parameter_factor")
    deduped = list(dict.fromkeys(reasons))
    return (1 if deduped else 0), deduped


def _recommend_next_action(config: RunConfig, status: str) -> str:
    if status != "completed":
        return "先修复本次 run 的 anomaly，再继续下一档激励。"
    if config.input_chain == "manual":
        if config.axis == "composite":
            return "若 composite 稳定，可继续拉长 duration，或提高其中一个分量后复测。"
        if config.manual_mode == "flight":
            return "若机体位移与姿态响应都正常，可继续补 pitch 或放大到 0.40。"
        if config.profile_type == "baseline":
            return "可继续执行 0.20 的 manual step，优先验证 roll 或 throttle。"
        if config.profile_type == "step" and abs(config.amplitude - 0.20) < 1e-6:
            return "若回显稳定，可继续做 0.40 或切到 throttle / pitch。"
        return "保持当前口径，继续补齐下一组 manual echo 验证。"
    if config.profile_type == "baseline":
        return "可继续执行 0.10 rad 的 roll step。"
    if config.profile_type == "step" and abs(config.amplitude - 0.10) < 1e-6:
        return "若无异常，可考虑下一档 0.20 rad。"
    return "保持当前口径，继续补齐下一组实验。"


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


def _float_value(value: Any, default: float | None = None) -> float | None:
    if value in ("", None):
        return default
    return float(value)


def _wrapped_angle_delta_rad(reference_rad: float, value_rad: float) -> float:
    delta = value_rad - reference_rad
    while delta > math.pi:
        delta -= 2.0 * math.pi
    while delta < -math.pi:
        delta += 2.0 * math.pi
    return delta


def _manual_xy_motion_anomaly(
    recorder_rows: dict[str, list[dict[str, Any]]],
    step_start_ns: int,
    step_end_ns: int,
    motion_threshold: float,
) -> str | None:
    position_rows = [
        row
        for row in recorder_rows["vehicle_local_position"]
        if int(row["received_time_ns"]) >= step_start_ns and int(row["received_time_ns"]) <= step_end_ns
    ]
    valid_rows = [row for row in position_rows if _bool_value(row.get("xy_valid", False))]
    if len(valid_rows) < 2:
        return "manual_motion_window_missing"
    x0 = _float_value(valid_rows[0]["x"], 0.0)
    y0 = _float_value(valid_rows[0]["y"], 0.0)
    max_disp = max(
        math.hypot(_float_value(row["x"], 0.0) - x0, _float_value(row["y"], 0.0) - y0) for row in valid_rows
    )
    if max_disp + MANUAL_MOTION_THRESHOLD_EPSILON < motion_threshold:
        return "manual_motion_not_observed"
    return None


def _manual_z_motion_anomaly(
    recorder_rows: dict[str, list[dict[str, Any]]],
    step_start_ns: int,
    step_end_ns: int,
    motion_threshold: float,
) -> str | None:
    position_rows = [
        row
        for row in recorder_rows["vehicle_local_position"]
        if int(row["received_time_ns"]) >= step_start_ns and int(row["received_time_ns"]) <= step_end_ns
    ]
    valid_rows = [row for row in position_rows if _bool_value(row.get("z_valid", False))]
    if len(valid_rows) < 2:
        return "manual_motion_window_missing"
    z0 = _float_value(valid_rows[0]["z"], 0.0)
    max_disp = max(abs(_float_value(row["z"], 0.0) - z0) for row in valid_rows)
    if max_disp + MANUAL_MOTION_THRESHOLD_EPSILON < motion_threshold:
        return "manual_motion_not_observed"
    return None


def _manual_yaw_motion_anomaly(
    recorder_rows: dict[str, list[dict[str, Any]]],
    step_start_ns: int,
    step_end_ns: int,
    yaw_threshold: float,
) -> str | None:
    attitude_rows = [
        row
        for row in recorder_rows["vehicle_attitude"]
        if int(row["received_time_ns"]) >= step_start_ns and int(row["received_time_ns"]) <= step_end_ns
    ]
    if len(attitude_rows) < 2:
        return "manual_motion_window_missing"
    yaw0 = _float_value(attitude_rows[0].get("yaw"), 0.0)
    max_yaw_delta = max(
        abs(_wrapped_angle_delta_rad(float(yaw0), _float_value(row.get("yaw"), 0.0) or 0.0)) for row in attitude_rows
    )
    if max_yaw_delta + MANUAL_MOTION_THRESHOLD_EPSILON < yaw_threshold:
        return "manual_motion_not_observed"
    return None


def _post_run_quality_anomalies(
    config: RunConfig,
    recorder_rows: dict[str, list[dict[str, Any]]],
    injector_report: dict[str, Any],
) -> list[str]:
    if config.input_chain != "attitude":
        return []

    anomalies: list[str] = []
    start_ns = injector_report.get("experiment_start_time_ns")
    end_ns = injector_report.get("landing_command_time_ns") or injector_report.get("completion_time_ns")
    takeoff_reference_z = injector_report.get("takeoff_reference_z")
    if start_ns is None or end_ns is None:
        return anomalies

    min_clearance_m: float | None = None
    for row in recorder_rows["vehicle_local_position"]:
        received_time_ns = int(row["received_time_ns"])
        if received_time_ns < int(start_ns) or received_time_ns > int(end_ns):
            continue
        candidates: list[float] = []
        if _bool_value(row.get("dist_bottom_valid", False)):
            dist_bottom_m = _float_value(row.get("dist_bottom"))
            if dist_bottom_m is not None and not math.isnan(dist_bottom_m):
                candidates.append(dist_bottom_m)
        if takeoff_reference_z is not None and _bool_value(row.get("z_valid", False)):
            z_m = _float_value(row.get("z"))
            if z_m is not None and not math.isnan(z_m):
                candidates.append(max(0.0, float(takeoff_reference_z) - z_m))
        if not candidates:
            continue
        clearance_m = max(candidates)
        if min_clearance_m is None or clearance_m < min_clearance_m:
            min_clearance_m = clearance_m

    if min_clearance_m is not None and min_clearance_m < config.min_profile_clearance_m:
        anomalies.append("ground_clearance_low")
    return anomalies


def _xy_motion_summary(
    recorder_rows: dict[str, list[dict[str, Any]]],
    start_ns: int | None,
    end_ns: int | None,
) -> dict[str, float] | None:
    if start_ns is None or end_ns is None:
        return None

    valid_rows = [
        row
        for row in recorder_rows["vehicle_local_position"]
        if int(row["received_time_ns"]) >= int(start_ns)
        if int(row["received_time_ns"]) <= int(end_ns)
        if _bool_value(row.get("xy_valid", False))
    ]
    if not valid_rows:
        return None

    start_x = _float_value(valid_rows[0].get("x"), 0.0) or 0.0
    start_y = _float_value(valid_rows[0].get("y"), 0.0) or 0.0
    end_x = _float_value(valid_rows[-1].get("x"), 0.0) or 0.0
    end_y = _float_value(valid_rows[-1].get("y"), 0.0) or 0.0
    start_radius = math.hypot(start_x, start_y)
    end_radius = math.hypot(end_x, end_y)
    max_radius = max(
        math.hypot(_float_value(row.get("x"), 0.0) or 0.0, _float_value(row.get("y"), 0.0) or 0.0)
        for row in valid_rows
    )
    max_displacement = max(
        math.hypot(
            (_float_value(row.get("x"), 0.0) or 0.0) - start_x,
            (_float_value(row.get("y"), 0.0) or 0.0) - start_y,
        )
        for row in valid_rows
    )
    return {
        "start_x_m": round(start_x, 3),
        "start_y_m": round(start_y, 3),
        "end_x_m": round(end_x, 3),
        "end_y_m": round(end_y, 3),
        "start_xy_radius_m": round(start_radius, 3),
        "end_xy_radius_m": round(end_radius, 3),
        "max_xy_radius_m": round(max_radius, 3),
        "max_xy_displacement_m": round(max_displacement, 3),
    }


def _xy_motion_anomalies(
    recorder_rows: dict[str, list[dict[str, Any]]],
    start_ns: int | None,
    end_ns: int | None,
    sim_world: str | None,
    config: RunConfig,
) -> tuple[list[str], dict[str, float] | None]:
    summary = _xy_motion_summary(recorder_rows, start_ns, end_ns)
    if summary is None:
        return [], None

    radius_limit = float(config.extras.get("max_xy_radius_m", 45.0))
    displacement_limit = float(config.extras.get("max_xy_displacement_m", 45.0))
    anomalies: list[str] = []
    if sim_world == "windy":
        if summary["start_xy_radius_m"] > radius_limit:
            anomalies.append("start_xy_radius_excessive")
        if summary["max_xy_radius_m"] > radius_limit:
            anomalies.append("xy_radius_excessive")
        if summary["max_xy_displacement_m"] > displacement_limit:
            anomalies.append("xy_displacement_excessive")
    return anomalies, summary


def _planned_input_peak(config: RunConfig) -> float:
    if config.axis != "composite":
        return round(abs(config.amplitude), 6)

    candidates = [
        abs(float(config.extras.get("roll_amplitude", 0.0))),
        abs(float(config.extras.get("pitch_amplitude", 0.0))),
        abs(float(config.extras.get("yaw_amplitude", 0.0))),
        abs(float(config.extras.get("throttle", 0.0))),
        abs(float(config.extras.get("thrust_delta", 0.0))),
    ]
    return round(max(candidates, default=0.0), 6)


def _placeholder_metrics(config: RunConfig, prestart_gate_summary: dict[str, Any] | None) -> dict[str, Any]:
    prestart_radius = math.nan
    displacement_peak = math.nan
    if prestart_gate_summary and _bool_value(prestart_gate_summary.get("xy_valid", False)):
        prestart_radius = _float_value(prestart_gate_summary.get("prestart_xy_radius_m"), math.nan)
        displacement_peak = 0.0

    return {
        "run_id": "",
        "input_chain": config.input_chain,
        "profile_type": config.profile_type,
        "axis": config.axis,
        "input_peak": _planned_input_peak(config),
        "input_rate_peak": math.nan,
        "tracking_error_peak": math.nan,
        "tracking_error_rms": math.nan,
        "response_delay_ms": math.nan,
        "nav_state_change": 0,
        "failsafe_event": 0,
        "start_xy_radius_m": prestart_radius,
        "end_xy_radius_m": prestart_radius,
        "xy_radius_peak_m": prestart_radius,
        "xy_displacement_peak_m": displacement_peak,
        "ulog_saturation_metric": "pending_ulog_parse",
        "ulog_parse_status": "missing_parser",
    }


def _prestart_xy_gate(
    recorder: TelemetryRecorder,
    sim_world: str | None,
    config: RunConfig,
) -> tuple[list[str], dict[str, Any], bool]:
    enabled = sim_world == "windy" and _bool_value(config.extras.get("enforce_prestart_xy_radius_gate", True))
    threshold_m = float(config.extras.get("prestart_max_xy_radius_m", 5.0))
    timeout_s = float(config.extras.get("prestart_xy_gate_timeout_s", 2.0))
    summary: dict[str, Any] = {
        "enabled": enabled,
        "sim_world": sim_world or "unspecified",
        "threshold_m": round(threshold_m, 3),
        "timeout_s": round(timeout_s, 3),
    }
    if not enabled:
        summary["passed"] = True
        return [], summary, True

    latest_row: dict[str, Any] | None = None
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        candidate = recorder.latest_row("vehicle_local_position")
        if candidate and _bool_value(candidate.get("xy_valid", False)):
            latest_row = candidate
            break
        time.sleep(0.05)

    if latest_row is None:
        summary["xy_valid"] = False
        summary["passed"] = False
        return ["prestart_xy_unavailable"], summary, False

    x_m = _float_value(latest_row.get("x"), 0.0) or 0.0
    y_m = _float_value(latest_row.get("y"), 0.0) or 0.0
    radius_m = math.hypot(x_m, y_m)
    summary.update(
        {
            "xy_valid": True,
            "sample_received_time_ns": int(latest_row["received_time_ns"]),
            "prestart_x_m": round(x_m, 3),
            "prestart_y_m": round(y_m, 3),
            "prestart_xy_radius_m": round(radius_m, 3),
            "passed": radius_m <= threshold_m,
        }
    )
    if radius_m > threshold_m:
        return ["prestart_xy_radius_excessive"], summary, False
    return [], summary, True


def _post_run_manual_anomalies(
    config: RunConfig,
    recorder_rows: dict[str, list[dict[str, Any]]],
    injector_report: dict[str, Any],
) -> list[str]:
    if config.input_chain != "manual":
        return []

    start_ns = injector_report.get("experiment_start_time_ns")
    end_ns = injector_report.get("completion_time_ns")
    if start_ns is None or end_ns is None:
        return ["manual_window_missing"]

    manual_rows = [
        row
        for row in recorder_rows["manual_control_setpoint"]
        if int(row["received_time_ns"]) >= int(start_ns) and int(row["received_time_ns"]) <= int(end_ns)
    ]
    if not manual_rows:
        return ["manual_echo_missing"]

    if not any(_bool_value(row.get("valid", False)) for row in manual_rows):
        return ["manual_echo_invalid"]

    if not any(int(row.get("data_source", -1)) == 2 for row in manual_rows):
        return ["manual_echo_source_mismatch"]

    if config.manual_mode != "flight":
        return []

    control_rows = [
        row
        for row in recorder_rows["vehicle_control_mode"]
        if int(row["received_time_ns"]) >= int(start_ns) and int(row["received_time_ns"]) <= int(end_ns)
    ]
    if not any(_bool_value(row.get("flag_control_manual_enabled", False)) for row in control_rows):
        return ["manual_control_not_enabled"]

    status_rows = [
        row
        for row in recorder_rows["vehicle_status"]
        if int(row["received_time_ns"]) >= int(start_ns) and int(row["received_time_ns"]) <= int(end_ns)
    ]
    if not any(int(row.get("nav_state", -1)) == 2 for row in status_rows):
        return ["manual_posctl_not_reached"]

    evaluation_phase_names = {
        "step": {"step_active", "recover"},
        "pulse": {"pulse_active", "recover"},
        "sweep": {"sweep_active", "recover"},
    }.get(config.profile_type, set())
    active_command_trace = [
        row for row in injector_report.get("command_trace", []) if str(row.get("phase", "")) in evaluation_phase_names
    ]
    active_command_times = [
        int(row["publish_time_ns"])
        for row in active_command_trace
    ]
    if not active_command_times:
        return ["manual_profile_window_missing"]

    step_start_ns = min(active_command_times)
    step_end_ns = max(max(active_command_times), int(end_ns))
    motion_threshold = float(config.extras.get("manual_motion_min_displacement_m", 0.20))
    z_motion_threshold = float(config.extras.get("manual_motion_min_z_displacement_m", motion_threshold))

    if config.axis in {"roll", "pitch"}:
        anomaly = _manual_xy_motion_anomaly(recorder_rows, step_start_ns, step_end_ns, motion_threshold)
        return [anomaly] if anomaly else []

    if config.axis == "throttle":
        anomaly = _manual_z_motion_anomaly(recorder_rows, step_start_ns, step_end_ns, z_motion_threshold)
        return [anomaly] if anomaly else []

    if config.axis == "yaw":
        yaw_threshold = float(config.extras.get("manual_motion_min_yaw_rad", 0.20))
        anomaly = _manual_yaw_motion_anomaly(recorder_rows, step_start_ns, step_end_ns, yaw_threshold)
        return [anomaly] if anomaly else []

    if config.axis == "composite":
        required_anomalies: list[str] = []
        if any(abs(_float_value(row.get("roll_body"), 0.0) or 0.0) > 1e-3 for row in active_command_trace) or any(
            abs(_float_value(row.get("pitch_body"), 0.0) or 0.0) > 1e-3 for row in active_command_trace
        ):
            anomaly = _manual_xy_motion_anomaly(recorder_rows, step_start_ns, step_end_ns, motion_threshold)
            if anomaly:
                required_anomalies.append("manual_composite_xy_not_observed")
                if anomaly not in required_anomalies:
                    required_anomalies.append(anomaly)
        if any(abs(_float_value(row.get("yaw_body"), 0.0) or 0.0) > 1e-3 for row in active_command_trace):
            yaw_threshold = float(config.extras.get("manual_motion_min_yaw_rad", 0.20))
            anomaly = _manual_yaw_motion_anomaly(recorder_rows, step_start_ns, step_end_ns, yaw_threshold)
            if anomaly:
                required_anomalies.append("manual_composite_yaw_not_observed")
                if anomaly not in required_anomalies:
                    required_anomalies.append(anomaly)
        if any(abs(_float_value(row.get("thrust_z"), 0.0) or 0.0) > 1e-3 for row in active_command_trace):
            anomaly = _manual_z_motion_anomaly(recorder_rows, step_start_ns, step_end_ns, z_motion_threshold)
            if anomaly:
                required_anomalies.append("manual_composite_z_not_observed")
                if anomaly not in required_anomalies:
                    required_anomalies.append(anomaly)
        return required_anomalies

    return []


def _run_purpose(config: RunConfig) -> str:
    if config.input_chain == "manual":
        if config.manual_mode == "flight":
            return f"验证 `{config.profile_type}` / `{config.axis}` 的 manual_control_input 对机体的真实控制效果。"
        return f"验证 `{config.profile_type}` / `{config.axis}` 的 manual_control_input 回显链与 artifact 落盘。"
    if config.input_chain == "rate":
        return f"验证 `{config.profile_type}` / `{config.axis}` 的 body-rate 主链闭环与 artifact 落盘。"
    return f"验证 `{config.profile_type}` / `{config.axis}` 的 attitude 主链闭环与 artifact 落盘。"


def _build_notes(
    config: RunConfig,
    run_id: str,
    status: str,
    start_time: datetime,
    end_time: datetime,
    host_start: dict[str, str],
    host_end: dict[str, str],
    timing_valid: bool,
    anomalies: list[str],
    recorder_summary: dict[str, Any],
    injector_report: dict[str, Any],
    ulog_path: str | None,
    sim_world: str | None,
    xy_motion_summary: dict[str, float] | None,
    prestart_gate_summary: dict[str, Any] | None,
    clock_bridge_summary: dict[str, Any] | None,
) -> str:
    anomaly_lines = "\n".join(f"- {item}" for item in anomalies) if anomalies else "- 无"
    prestart_lines = ["- unavailable"]
    if prestart_gate_summary is not None:
        prestart_lines = [
            f"- enabled: {'yes' if _bool_value(prestart_gate_summary.get('enabled', False)) else 'no'}",
            f"- threshold_m: {prestart_gate_summary.get('threshold_m', 'n/a')}",
            f"- timeout_s: {prestart_gate_summary.get('timeout_s', 'n/a')}",
            f"- passed: {'yes' if _bool_value(prestart_gate_summary.get('passed', False)) else 'no'}",
        ]
        if _bool_value(prestart_gate_summary.get("xy_valid", False)):
            prestart_lines.extend(
                [
                    f"- prestart_xy=({prestart_gate_summary['prestart_x_m']}, {prestart_gate_summary['prestart_y_m']}) m",
                    f"- prestart_xy_radius_m={prestart_gate_summary['prestart_xy_radius_m']}",
                ]
            )
        else:
            prestart_lines.append("- valid_xy: no")
    xy_summary_lines = (
        [
            f"- start_xy=({xy_motion_summary['start_x_m']}, {xy_motion_summary['start_y_m']}) m",
            f"- end_xy=({xy_motion_summary['end_x_m']}, {xy_motion_summary['end_y_m']}) m",
            f"- start_xy_radius_m={xy_motion_summary['start_xy_radius_m']}",
            f"- end_xy_radius_m={xy_motion_summary['end_xy_radius_m']}",
            f"- max_xy_radius_m={xy_motion_summary['max_xy_radius_m']}",
            f"- max_xy_displacement_m={xy_motion_summary['max_xy_displacement_m']}",
        ]
        if xy_motion_summary
        else ["- unavailable"]
    )
    clock_bridge_lines = ["- started: no"]
    if clock_bridge_summary is not None:
        clock_bridge_lines = [
            f"- started: {'yes' if _bool_value(clock_bridge_summary.get('started', False)) else 'no'}",
            f"- timing_ready_after_bridge: {'yes' if _bool_value(clock_bridge_summary.get('timing_ready_after_bridge', False)) else 'no'}",
            f"- gz_topic: {clock_bridge_summary.get('gz_topic', 'unavailable')}",
            f"- log_path: {clock_bridge_summary.get('log_path', 'n/a')}",
        ]
    return "\n".join(
        [
            f"# Run Notes: {run_id}",
            "",
            "## 本次 run 的目的",
            f"- {_run_purpose(config)}",
            "",
            "## 研究层信息",
            f"- study_family: {config.study_family}",
            f"- study_layer: {config.resolved_study_layer}",
            f"- study_role: {config.resolved_study_role}",
            f"- oracle_profile: {config.resolved_oracle_profile}",
            f"- parameter_group: {config.resolved_parameter_group}",
            f"- parameter_set_name: {config.parameter_set_name}",
            f"- mode_under_test(px4): {config.mode_under_test_for_backend('px4')}",
            f"- attribution_boundary: {config.resolved_attribution_boundary}",
            "",
            "## 操作人/Agent",
            f"- {config.operator}",
            "",
            "## Run 概览",
            f"- 开始时间: {start_time.isoformat()}",
            f"- 结束时间: {end_time.isoformat()}",
            f"- 结果状态: {status}",
            f"- completion_reason: {injector_report['completion_reason']}",
            f"- ULog 路径: {ulog_path or 'missing'}",
            f"- Gazebo world: {sim_world or 'unspecified'}",
            "",
            "## 起飞前位置 Gate",
            *prestart_lines,
            "",
            "## Clock Bridge",
            *clock_bridge_lines,
            "",
            "## 观察到的异常",
            anomaly_lines,
            "",
            "## Recorder 摘要",
            f"- message_counts: {recorder_summary['message_counts']}",
            f"- event_counts: {recorder_summary['event_counts']}",
            "",
            "## XY 运动摘要",
            *xy_summary_lines,
            "",
            "## 是否建议放大下一轮激励",
            f"- {_recommend_next_action(config, status)}",
            "",
            "## 主机性能快照（开始前）",
            f"- uptime: {host_start['uptime']}",
            f"- /proc/loadavg: {host_start['loadavg']}",
            "",
            "## 主机性能快照（结束后）",
            f"- uptime: {host_end['uptime']}",
            f"- /proc/loadavg: {host_end['loadavg']}",
            "",
            "## Timing 分析可用性",
            f"- {'yes' if timing_valid else 'no'}",
        ]
    )


def run_experiment(config: RunConfig) -> tuple[int, Path]:
    start_time = datetime.now(timezone.utc).astimezone()
    run_id = config.build_run_id(start_time)
    study = config.study_metadata("px4")
    paths = ensure_run_directories(run_id)
    host_start = capture_host_snapshot()

    clock_bridge_handle = None
    clock_bridge_summary: dict[str, Any] = {
        "started": False,
        "timing_ready_after_bridge": False,
        "gz_topic": "unavailable",
        "log_path": str(paths["base_dir"] / "gz_clock_bridge.log"),
    }
    if _bool_value(config.extras.get("auto_clock_bridge", True)):
        clock_bridge_handle, clock_ready = ensure_clock_bridge(log_path=paths["base_dir"] / "gz_clock_bridge.log")
        clock_bridge_summary["timing_ready_after_bridge"] = clock_ready
        if clock_bridge_handle is not None:
            clock_bridge_summary["started"] = True
            clock_bridge_summary["gz_topic"] = clock_bridge_handle.gz_topic

    ulog_before = snapshot_ulog_files()
    preflight_anomalies, clock_available = _preflight_checks()
    sim_world = os.environ.get("PX4_GZ_WORLD", "").strip() or None
    parameter_master, parameter_snapshot_before, parameter_snapshot_after, parameter_anomalies = _prepare_px4_parameters(config)

    rclpy.init()
    recorder = TelemetryRecorder()
    if config.input_chain == "manual":
        injector = ManualInputInjector(config)
    elif config.input_chain == "attitude":
        injector = AttitudeInjector(config)
    elif config.input_chain == "rate":
        injector = RateInjector(config)
    else:
        raise ValueError(f"PX4 不支持 input_chain={config.input_chain}")
    executor = SingleThreadedExecutor()
    executor.add_node(recorder)
    executor.add_node(injector)

    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()

    run_status = "completed"
    anomalies = list(preflight_anomalies) + list(parameter_anomalies)
    timing_valid = clock_available
    prestart_gate_summary: dict[str, Any] | None = None
    completion_reason_override: str | None = None
    injector_started = False

    try:
        ready_deadline = time.monotonic() + config.ready_timeout_s
        while time.monotonic() < ready_deadline and not recorder.core_topics_ready():
            time.sleep(0.1)

        if not recorder.core_topics_ready():
            anomalies.append("recorder_core_topics_not_ready")
            run_status = "invalid_runtime"
        else:
            prestart_gate_anomalies, prestart_gate_summary, prestart_gate_passed = _prestart_xy_gate(
                recorder,
                sim_world,
                config,
            )
            anomalies.extend(prestart_gate_anomalies)
            if not prestart_gate_passed:
                run_status = "invalid_runtime"
                completion_reason_override = (
                    "prestart_xy_gate_unavailable"
                    if "prestart_xy_unavailable" in prestart_gate_anomalies
                    else "prestart_xy_gate_blocked"
                )
            else:
                injector.start_run()
                injector_started = True
                deadline = time.monotonic() + config.run_timeout_s
                while time.monotonic() < deadline and not injector.is_completed():
                    time.sleep(0.1)

                if not injector.is_completed():
                    anomalies.append("run_timeout")
                    run_status = "invalid_runtime"
                time.sleep(1.0)
    finally:
        executor.shutdown()
        spin_thread.join(timeout=5.0)
        injector.destroy_node()
        recorder.destroy_node()
        rclpy.shutdown()
        stop_clock_bridge(clock_bridge_handle)
        if parameter_snapshot_after != parameter_snapshot_before:
            anomalies.extend(_restore_px4_parameters(parameter_master, parameter_snapshot_before))
        close_mavlink(parameter_master)

    host_end = capture_host_snapshot()
    ulog_after = snapshot_ulog_files()
    ulog_path = resolve_ulog_path(ulog_before, ulog_after)
    end_time = datetime.now(timezone.utc).astimezone()

    recorder.write_csvs(paths["telemetry_dir"])
    command_trace = injector.command_trace()
    write_rows_csv(
        paths["input_trace_path"],
        command_trace,
        ["publish_time_ns", "elapsed_s", "profile_value", "roll_body", "pitch_body", "yaw_body", "thrust_z", "phase"],
    )

    injector_report = injector.report()
    if completion_reason_override is not None:
        injector_report["completion_reason"] = completion_reason_override
    injector_report["command_trace"] = command_trace
    anomalies.extend(injector_report["anomalies"])
    recorder_summary = recorder.summary()
    rows = recorder.snapshot_rows()
    if injector_started:
        anomalies.extend(_post_run_quality_anomalies(config, rows, injector_report))
        anomalies.extend(_post_run_manual_anomalies(config, rows, injector_report))
    active_command_trace = command_trace
    if config.input_chain == "manual":
        active_trace_start_ns = injector_report["experiment_start_time_ns"]
    else:
        active_trace_start_ns = injector_report["offboard_command_time_ns"] or injector_report["experiment_start_time_ns"]
    if active_trace_start_ns is not None:
        active_command_trace = [
            row for row in command_trace if int(row["publish_time_ns"]) >= int(active_trace_start_ns)
        ]

    if config.input_chain == "manual":
        metrics_start_ns = injector_report["experiment_start_time_ns"]
        metrics_end_ns = injector_report["landing_command_time_ns"] or injector_report["completion_time_ns"]
    else:
        metrics_start_ns = injector_report["offboard_command_time_ns"] or injector_report["experiment_start_time_ns"]
        metrics_end_ns = injector_report["landing_command_time_ns"] or injector_report["completion_time_ns"]

    xy_anomalies, xy_motion_summary = _xy_motion_anomalies(
        rows,
        metrics_start_ns,
        metrics_end_ns,
        sim_world,
        config,
    )
    anomalies.extend(xy_anomalies)

    if injector_started:
        metrics = compute_metrics(
            config,
            active_command_trace,
            rows["vehicle_attitude"],
            rows["vehicle_angular_velocity"],
            rows["vehicle_rates_setpoint"],
            rows["manual_control_setpoint"],
            rows["vehicle_local_position"],
            rows["vehicle_status"],
            metrics_start_ns,
            metrics_end_ns,
        )
    else:
        metrics = _placeholder_metrics(config, prestart_gate_summary)
    metrics["run_id"] = run_id
    metrics["backend"] = "px4_ros2"
    metrics["study_layer"] = study["study_layer"]
    metrics["study_role"] = study["study_role"]
    metrics["mode_under_test"] = study["mode_under_test"]
    metrics["parameter_group"] = study["parameter_group"]
    metrics["parameter_set_name"] = study["parameter_set_name"]
    metrics.update(
        summarize_ulog(
            ulog_path,
            run_context={
                "input_chain": config.input_chain,
                "profile_type": config.profile_type,
                "profile_params": config.profile_params(),
            },
        )
    )

    if ulog_path is None and injector_started:
        anomalies.append("ulog_missing")
        run_status = "invalid_artifacts"

    if metrics["failsafe_event"] == 1 or metrics["nav_state_change"] == 1:
        run_status = "invalid_runtime"

    if any(
        item
        in {
            "takeoff_clearance_timeout",
            "profile_clearance_low",
            "ground_clearance_low",
            "manual_window_missing",
            "manual_echo_missing",
            "manual_echo_invalid",
            "manual_echo_source_mismatch",
            "manual_control_not_enabled",
            "manual_posctl_not_reached",
            "manual_step_window_missing",
            "manual_profile_window_missing",
            "manual_motion_window_missing",
            "manual_motion_not_observed",
            "manual_composite_xy_not_observed",
            "manual_composite_yaw_not_observed",
            "manual_composite_z_not_observed",
            "prestart_xy_unavailable",
            "prestart_xy_radius_excessive",
        }
        for item in anomalies
    ):
        run_status = "invalid_runtime"

    if config.timing_required and not timing_valid:
        run_status = "invalid_timing"

    mechanism_flags = _mechanism_flags(metrics, anomalies)
    stress_class = _stress_class(metrics, run_status, mechanism_flags)
    oracle_valid, oracle_failure_reason = _oracle_decision(config, metrics, anomalies, run_status, mechanism_flags)
    rate_layer_recommended, rate_layer_reasons = _rate_layer_recommendation(config, oracle_valid, mechanism_flags)
    metrics["oracle_valid"] = oracle_valid
    metrics["oracle_failure_reason"] = oracle_failure_reason
    metrics["stress_class"] = stress_class
    metrics["mechanism_flags"] = ",".join(mechanism_flags)
    metrics["rate_layer_recommended"] = rate_layer_recommended
    metrics["rate_layer_reasons"] = ",".join(rate_layer_reasons)
    metrics["attribution_boundary"] = config.resolved_attribution_boundary

    notes_text = _build_notes(
        config,
        run_id,
        run_status,
        start_time,
        end_time,
        host_start,
        host_end,
        timing_valid,
        anomalies,
        recorder_summary,
        injector_report,
        ulog_path,
        sim_world,
        xy_motion_summary,
        prestart_gate_summary,
        clock_bridge_summary,
    )
    paths["notes_path"].write_text(notes_text, encoding="utf-8")

    manifest = {
        "run_id": run_id,
        "backend": "px4_ros2",
        "schema_version": schema_version(),
        "milestone_id": milestone_id(),
        "capability_level": capability_level(),
        "phase": config.phase,
        "input_chain": config.input_chain,
        "input_topic": config.input_topic,
        "profile_type": config.profile_type,
        "profile_params": config.profile_params(),
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "status": run_status,
        "sim_world": sim_world or "unspecified",
        "study": study,
        "px4_log_path": ulog_path,
        "prestart_xy_gate": prestart_gate_summary,
        "clock_bridge": clock_bridge_summary,
        "xy_motion_summary": xy_motion_summary,
        "ros_topics_recorded": list(RECORDED_TOPICS),
        "parameter_snapshot_before": parameter_snapshot_before,
        "parameter_snapshot_after": parameter_snapshot_after,
        "anomaly_summary": anomalies,
    }
    write_yaml(paths["manifest_path"], manifest)

    write_single_row_csv(
        paths["metrics_path"],
        metrics,
        [
            "run_id",
            "backend",
            "study_layer",
            "study_role",
            "mode_under_test",
            "parameter_group",
            "parameter_set_name",
            "input_chain",
            "profile_type",
            "axis",
            "input_peak",
            "input_rate_peak",
            "tracking_error_peak",
            "tracking_error_rms",
            "response_delay_ms",
            "nav_state_change",
            "failsafe_event",
            "start_xy_radius_m",
            "end_xy_radius_m",
            "xy_radius_peak_m",
            "xy_displacement_peak_m",
            "ulog_saturation_metric",
            "ulog_parse_status",
            "oracle_valid",
            "oracle_failure_reason",
            "stress_class",
            "mechanism_flags",
            "rate_layer_recommended",
            "rate_layer_reasons",
            "attribution_boundary",
        ],
    )

    return (0 if run_status == "completed" else 1), paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="运行 FEP Phase 1 实验并自动落盘 artifacts。")
    parser.add_argument("--config", type=Path, required=True, help="YAML 配置路径。")
    args = parser.parse_args(argv)

    config = load_run_config(args.config)
    exit_code, artifact_dir = run_experiment(config)
    print(f"artifact_dir={artifact_dir}")
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
