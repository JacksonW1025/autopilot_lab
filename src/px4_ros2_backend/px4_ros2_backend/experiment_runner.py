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
from linearity_core.io import capture_host_snapshot, read_rows_csv, write_rows_csv, write_yaml
from linearity_core.mav_params import close_mavlink, connect_mavlink, set_parameters, snapshot_parameters
from rclpy.executors import SingleThreadedExecutor

from .artifacts import ensure_run_directories, resolve_ulog_path, snapshot_ulog_files
from .attitude_injector import AttitudeInjector
from .common import (
    RECORDED_TOPICS,
    RunConfig,
    ensure_clock_bridge,
    read_clock_topic_advancing,
    read_clock_topic_available,
    stop_clock_bridge,
)
from .manual_input_injector import ManualInputInjector
from .rate_injector import RateInjector
from .telemetry_recorder import TelemetryRecorder
from .ulog_backfill import backfill_px4_ulog_topics

PX4_PARAM_MASTER_DEFAULT = "udp:127.0.0.1:14550"
INPUT_TRACE_FIELDS = [
    "publish_time_ns",
    "elapsed_s",
    "profile_value",
    "roll_body",
    "pitch_body",
    "yaw_body",
    "thrust_z",
    "command_roll",
    "command_pitch",
    "command_yaw",
    "command_throttle",
    "phase",
]


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
    parameter_names.extend(name for name in config.parameter_overrides_for_backend("px4") if name not in parameter_names)
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


def _select_injector(config: RunConfig):
    if config.input_chain == "manual":
        return ManualInputInjector(config)
    if config.input_chain == "attitude":
        return AttitudeInjector(config)
    if config.input_chain == "rate":
        return RateInjector(config)
    raise ValueError(f"PX4 不支持 input_type={config.input_chain}")


def _notes_text(
    run_id: str,
    config: RunConfig,
    status: str,
    anomalies: list[str],
    ulog_path: str | None,
    recorder_summary: dict[str, Any],
    injector_report: dict[str, Any],
) -> str:
    return "\n".join(
        [
            f"# {run_id}",
            "- px4 raw linearity capture",
            f"- status: {status}",
            f"- backend: px4",
            f"- input_type: {config.input_type}",
            f"- flight_mode: {config.mode_under_test_for_backend('px4')}",
            f"- x_schema: {config.x_schema}",
            f"- y_schema: {config.y_schema}",
            f"- ulog_path: {ulog_path or 'missing'}",
            f"- anomalies: {', '.join(anomalies) if anomalies else 'none'}",
            f"- recorder_counts: {recorder_summary.get('message_counts', {})}",
            f"- injector_completion: {injector_report.get('completion_reason', 'unknown')}",
        ]
    )


def _int_value(value: Any, default: int = 0) -> int:
    if value in ("", None):
        return default
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _sorted_csv_rows(path: Path, time_key: str) -> list[dict[str, Any]]:
    rows = read_rows_csv(path)
    rows.sort(key=lambda row: _int_value(row.get(time_key), 0))
    return rows


def _timestamp_monotonic(rows: list[dict[str, Any]], time_key: str) -> bool:
    previous = None
    for row in rows:
        current = _int_value(row.get(time_key), 0)
        if previous is not None and current < previous:
            return False
        previous = current
    return True


def _nearest_gap_metrics(reference_rows: list[dict[str, Any]], target_rows: list[dict[str, Any]], reference_key: str, target_key: str) -> dict[str, float]:
    if not reference_rows or not target_rows:
        return {"count": 0.0, "median_ns": math.nan, "p95_ns": math.nan, "max_ns": math.nan}
    target_times = [_int_value(row.get(target_key), 0) for row in target_rows]
    gaps: list[int] = []
    for row in reference_rows:
        target_ns = _int_value(row.get(reference_key), 0)
        nearest = min(target_times, key=lambda value: abs(value - target_ns))
        gaps.append(abs(nearest - target_ns))
    if not gaps:
        return {"count": 0.0, "median_ns": math.nan, "p95_ns": math.nan, "max_ns": math.nan}
    return {
        "count": float(len(gaps)),
        "median_ns": float(sorted(gaps)[len(gaps) // 2]),
        "p95_ns": float(sorted(gaps)[min(len(gaps) - 1, int(0.95 * (len(gaps) - 1)))]),
        "max_ns": float(max(gaps)),
    }


def _prediction_constructibility_metrics(command_trace: list[dict[str, Any]], topic_counts: dict[str, int], config: RunConfig) -> dict[str, float]:
    total_samples = float(len(command_trace))
    future_samples = max(0.0, total_samples - float(config.prediction_horizon))
    actuator_samples = float(topic_counts.get("actuator_motors", 0))
    return {
        "total_input_samples": total_samples,
        "prediction_horizon": float(config.prediction_horizon),
        "future_state_ratio_estimate": (future_samples / total_samples) if total_samples > 0 else 0.0,
        "delta_state_ratio_estimate": (future_samples / total_samples) if total_samples > 0 else 0.0,
        "window_summary_ratio_estimate": (future_samples / total_samples) if total_samples > 0 else 0.0,
        "actuator_response_ratio_estimate": min(1.0, actuator_samples / total_samples) if total_samples > 0 else 0.0,
    }


def _px4_data_quality(paths: dict[str, Path], recorder_summary: dict[str, Any], command_trace: list[dict[str, Any]], config: RunConfig) -> dict[str, Any]:
    required_topics = (
        "vehicle_attitude",
        "vehicle_angular_velocity",
        "vehicle_local_position",
        "vehicle_status",
        "vehicle_control_mode",
        "actuator_motors",
    )
    input_rows = _sorted_csv_rows(paths["input_trace_path"], "publish_time_ns")
    telemetry_rows = {
        "vehicle_attitude": _sorted_csv_rows(paths["telemetry_dir"] / "vehicle_attitude.csv", "received_time_ns"),
        "vehicle_angular_velocity": _sorted_csv_rows(paths["telemetry_dir"] / "vehicle_angular_velocity.csv", "received_time_ns"),
        "vehicle_local_position": _sorted_csv_rows(paths["telemetry_dir"] / "vehicle_local_position.csv", "received_time_ns"),
        "vehicle_status": _sorted_csv_rows(paths["telemetry_dir"] / "vehicle_status.csv", "received_time_ns"),
        "vehicle_control_mode": _sorted_csv_rows(paths["telemetry_dir"] / "vehicle_control_mode.csv", "received_time_ns"),
        "actuator_motors": _sorted_csv_rows(paths["telemetry_dir"] / "actuator_motors.csv", "received_time_ns"),
    }
    topic_counts = {topic: len(telemetry_rows[topic]) for topic in required_topics}
    missing_topics = sorted([topic for topic, count in topic_counts.items() if count <= 0])
    timestamp_monotonicity = {
        "input_trace": _timestamp_monotonic(input_rows, "publish_time_ns"),
        **{name: _timestamp_monotonic(rows, "received_time_ns") for name, rows in telemetry_rows.items()},
    }
    input_alignment_ns = {
        name: _nearest_gap_metrics(input_rows, rows, "publish_time_ns", "received_time_ns")
        for name, rows in telemetry_rows.items()
    }
    max_alignment_error_ms = float(config.reporting.get("max_alignment_error_ms", 150.0))
    p95_alignment_failures = sorted(
        name
        for name, metrics in input_alignment_ns.items()
        if not math.isnan(metrics["p95_ns"]) and metrics["p95_ns"] > max_alignment_error_ms * 1_000_000.0
    )
    return {
        "topic_presence": {
            "required_topic_counts": topic_counts,
            "missing_topics": missing_topics,
            "ros_message_counts": {
                topic: int(recorder_summary.get("message_counts", {}).get(topic, 0))
                for topic in required_topics
            },
        },
        "timestamp_monotonicity": timestamp_monotonicity,
        "input_alignment_ns": input_alignment_ns,
        "prediction_constructibility": _prediction_constructibility_metrics(command_trace, topic_counts, config),
        "thresholds": {
            "max_alignment_error_ms": max_alignment_error_ms,
        },
        "quality_flags": {
            "non_monotonic_streams": sorted(name for name, ok in timestamp_monotonicity.items() if not ok),
            "alignment_p95_exceeded_streams": p95_alignment_failures,
        },
    }


def run_capture(config: RunConfig) -> tuple[int, Path]:
    start_time = datetime.now(timezone.utc).astimezone()
    run_id = config.build_run_id(start_time, repeat_index=config.repeat_index)
    paths = ensure_run_directories(run_id)
    host_start = capture_host_snapshot()

    clock_bridge_handle = None
    clock_bridge_summary: dict[str, Any] = {
        "started": False,
        "timing_ready_after_bridge": False,
        "gz_topic": "unavailable",
        "log_path": str(paths["logs_dir"] / "gz_clock_bridge.log"),
    }
    if bool(config.extras.get("auto_clock_bridge", True)):
        clock_bridge_handle, clock_ready = ensure_clock_bridge(log_path=paths["logs_dir"] / "gz_clock_bridge.log")
        clock_bridge_summary["timing_ready_after_bridge"] = clock_ready
        if clock_bridge_handle is not None:
            clock_bridge_summary["started"] = True
            clock_bridge_summary["gz_topic"] = clock_bridge_handle.gz_topic

    anomalies, timing_valid = _preflight_checks()
    parameter_master, parameter_snapshot_before, parameter_snapshot_after, parameter_anomalies = _prepare_px4_parameters(config)
    anomalies.extend(parameter_anomalies)
    ulog_before = snapshot_ulog_files()
    sim_world = os.environ.get("PX4_GZ_WORLD", "").strip() or "default"

    rclpy.init()
    recorder = TelemetryRecorder()
    injector = _select_injector(config)
    executor = SingleThreadedExecutor()
    executor.add_node(recorder)
    executor.add_node(injector)
    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()

    status = "completed"
    failure_reason = ""
    try:
        ready_deadline = time.monotonic() + config.ready_timeout_s
        while time.monotonic() < ready_deadline and not recorder.core_topics_ready():
            time.sleep(0.1)
        if not recorder.core_topics_ready():
            status = "failed"
            failure_reason = "recorder_core_topics_not_ready"
            anomalies.append(failure_reason)
        else:
            injector.start_run()
            deadline = time.monotonic() + config.run_timeout_s
            while time.monotonic() < deadline and not injector.is_completed():
                time.sleep(0.1)
            if not injector.is_completed():
                status = "failed"
                failure_reason = "run_timeout"
                anomalies.append(failure_reason)
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
    write_rows_csv(paths["input_trace_path"], command_trace, INPUT_TRACE_FIELDS)
    recorder_summary = recorder.summary()
    injector_report = injector.report()
    anomalies.extend(injector_report.get("anomalies", []))
    telemetry_backfill = backfill_px4_ulog_topics(paths["telemetry_dir"], ulog_path=ulog_path)
    if telemetry_backfill.get("failure_reasons"):
        anomalies.extend(f"telemetry_backfill:{reason}" for reason in telemetry_backfill["failure_reasons"])
    for topic, payload in telemetry_backfill.get("topics", {}).items():
        if payload.get("source") == "missing" and payload.get("failure_reason"):
            anomalies.append(f"{topic}:{payload['failure_reason']}")
    data_quality = _px4_data_quality(paths, recorder_summary, command_trace, config)
    if data_quality["topic_presence"]["missing_topics"]:
        anomalies.append("quality_missing_topics")
    if data_quality["quality_flags"]["non_monotonic_streams"]:
        anomalies.append("quality_non_monotonic_streams")
    if data_quality["quality_flags"]["alignment_p95_exceeded_streams"]:
        anomalies.append("quality_alignment_p95_exceeded")

    if config.timing_required and not timing_valid:
        status = "failed"
        failure_reason = failure_reason or "timing_invalid"

    manifest = {
        "kind": "linearity_raw_run",
        "raw_schema_version": 1,
        "run_id": run_id,
        "backend": "px4",
        "status": status,
        "failure_reason": failure_reason,
        "study_name": config.study_name,
        "study_config": config.to_dict(),
        "flight_mode": config.mode_under_test_for_backend("px4"),
        "scenario": config.scenario,
        "config_profile": config.config_profile,
        "seed": config.seed,
        "repeat_index": config.repeat_index,
        "input_type": config.input_type,
        "profile_type": config.profile_type,
        "axis": config.axis,
        "sim_world": sim_world,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "px4_log_path": ulog_path,
        "clock_bridge": clock_bridge_summary,
        "ros_topics_recorded": list(RECORDED_TOPICS),
        "parameter_snapshot_before": parameter_snapshot_before,
        "parameter_snapshot_after": parameter_snapshot_after,
        "host_snapshot_start": host_start,
        "host_snapshot_end": host_end,
        "recorder_summary": recorder_summary,
        "telemetry_backfill": telemetry_backfill,
        "injector_report": injector_report,
        "data_quality": data_quality,
        "anomaly_summary": sorted(dict.fromkeys(anomalies)),
        "telemetry_files": sorted(path.name for path in paths["telemetry_dir"].glob("*.csv")),
    }
    write_yaml(paths["manifest_path"], manifest)
    paths["notes_path"].write_text(
        _notes_text(run_id, config, status, sorted(dict.fromkeys(anomalies)), ulog_path, recorder_summary, injector_report),
        encoding="utf-8",
    )
    return (0 if status == "completed" else 1), paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="运行 PX4 raw linearity capture，并写出新的 raw artifact。")
    parser.add_argument("--config", type=Path, required=True, help="study config YAML 路径。")
    args = parser.parse_args(argv)

    from linearity_core.config import load_study_config

    config = load_study_config(args.config)
    exit_code, artifact_dir = run_capture(config)
    print(f"artifact_dir={artifact_dir}")
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
