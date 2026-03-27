from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from pyulog import ULog

from .analysis_runner import (
    RunRecord,
    XY_CONTAMINATION_ANOMALIES,
    filter_records_by_world,
    load_run_records,
    select_nominal_records,
)
from .artifacts import write_rows_csv, write_yaml
from .common import ARTIFACT_ROOT, quaternion_to_euler
from .ulog_metrics import ACTIVE_PHASES, ULogWindowContext, build_window_context_from_aligned_events


IDENTIFICATION_ROOT = ARTIFACT_ROOT.parent / "identification"
DEFAULT_INPUT_CHAIN = "attitude"
DEFAULT_WORLD_FILTER = "nominal"
DEFAULT_EXCLUDED_PHASES = {"warmup_position"}
DEFAULT_MOTOR_COUNT = 4
NEXT_STATE_FIELDS = (
    "state_roll",
    "state_pitch",
    "state_yaw",
    "state_roll_rate",
    "state_pitch_rate",
    "state_yaw_rate",
)


@dataclass(slots=True)
class SampleSeries:
    timestamps_us: np.ndarray
    values: np.ndarray
    angle: bool = False
    discrete: bool = False


def _float_value(value: Any, default: float = math.nan) -> float:
    if value in ("", None):
        return default
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"true", "yes"}:
            return 1.0
        if text in {"false", "no"}:
            return 0.0
    return float(value)


def _int_value(value: Any, default: int = 0) -> int:
    if value in ("", None):
        return default
    return int(float(value))


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"1", "true", "yes"}:
        return True
    if text in {"0", "false", "no", ""}:
        return False
    return bool(value)


def _csv_value(value: Any) -> Any:
    if isinstance(value, (np.floating, float)) and math.isnan(float(value)):
        return ""
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def _load_manifest(run_dir: Path) -> dict[str, Any]:
    payload = yaml.safe_load((run_dir / "manifest.yaml").read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _load_csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _matrix_run_ids(matrix_dir: Path) -> list[str]:
    rows = _load_csv_rows(matrix_dir / "runs.csv")
    run_ids: list[str] = []
    for row in rows:
        artifact_dir = str(row.get("artifact_dir", "")).strip()
        if not artifact_dir:
            continue
        manifest_path = Path(artifact_dir).expanduser().resolve() / "manifest.yaml"
        if not manifest_path.exists():
            continue
        payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            continue
        run_id = str(payload.get("run_id", "")).strip()
        if run_id:
            run_ids.append(run_id)
    return run_ids


def _prepare_series(timestamps: np.ndarray, values: np.ndarray) -> SampleSeries | None:
    if timestamps.size == 0 or values.size == 0 or timestamps.size != values.size:
        return None
    finite_mask = np.isfinite(timestamps) & np.isfinite(values)
    if not np.any(finite_mask):
        return None
    timestamps = timestamps[finite_mask]
    values = values[finite_mask]
    order = np.argsort(timestamps, kind="stable")
    timestamps = timestamps[order]
    values = values[order]
    unique_index = np.concatenate(([0], np.nonzero(np.diff(timestamps))[0] + 1))
    timestamps = timestamps[unique_index]
    values = values[unique_index]
    if timestamps.size == 0:
        return None
    return SampleSeries(timestamps_us=timestamps, values=values)


def _build_series_from_rows(
    rows: list[dict[str, Any]],
    timestamp_key: str,
    value_key: str,
    *,
    angle: bool = False,
    discrete: bool = False,
) -> SampleSeries | None:
    timestamps = np.asarray([_float_value(row.get(timestamp_key)) for row in rows], dtype=float)
    values = np.asarray([_float_value(row.get(value_key)) for row in rows], dtype=float)
    series = _prepare_series(timestamps, values)
    if series is None:
        return None
    series.angle = angle
    series.discrete = discrete
    return series


def _build_series_from_ulog(
    ulog: ULog,
    dataset_name: str,
    value_key: str,
    *,
    angle: bool = False,
    discrete: bool = False,
) -> SampleSeries | None:
    dataset = next((item for item in ulog.data_list if item.name == dataset_name), None)
    if dataset is None or "timestamp" not in dataset.data or value_key not in dataset.data:
        return None
    timestamps = np.asarray(dataset.data["timestamp"], dtype=float)
    values = np.asarray(dataset.data[value_key], dtype=float)
    series = _prepare_series(timestamps, values)
    if series is None:
        return None
    series.angle = angle
    series.discrete = discrete
    return series


def _sample_series(series: SampleSeries | None, query_timestamps_us: np.ndarray) -> np.ndarray:
    if series is None or query_timestamps_us.size == 0:
        return np.full(query_timestamps_us.shape, np.nan, dtype=float)
    if series.timestamps_us.size == 1:
        return np.full(query_timestamps_us.shape, float(series.values[0]), dtype=float)
    if series.discrete:
        indices = np.searchsorted(series.timestamps_us, query_timestamps_us, side="left")
        indices = np.clip(indices, 0, series.timestamps_us.size - 1)
        previous = np.clip(indices - 1, 0, series.timestamps_us.size - 1)
        choose_previous = np.abs(query_timestamps_us - series.timestamps_us[previous]) <= np.abs(
            query_timestamps_us - series.timestamps_us[indices]
        )
        nearest = np.where(choose_previous, previous, indices)
        return series.values[nearest].astype(float)
    values = np.unwrap(series.values) if series.angle else series.values
    sampled = np.interp(
        query_timestamps_us,
        series.timestamps_us,
        values,
        left=np.nan,
        right=np.nan,
    )
    if series.angle:
        sampled = ((sampled + math.pi) % (2.0 * math.pi)) - math.pi
    return sampled.astype(float)


def _command_columns(input_rows: list[dict[str, Any]]) -> dict[str, np.ndarray]:
    return {
        "command_profile_value": np.asarray([_float_value(row.get("profile_value"), 0.0) for row in input_rows], dtype=float),
        "command_roll_body": np.asarray([_float_value(row.get("roll_body"), 0.0) for row in input_rows], dtype=float),
        "command_pitch_body": np.asarray([_float_value(row.get("pitch_body"), 0.0) for row in input_rows], dtype=float),
        "command_yaw_body": np.asarray([_float_value(row.get("yaw_body"), 0.0) for row in input_rows], dtype=float),
        "command_thrust_z": np.asarray([_float_value(row.get("thrust_z"), 0.0) for row in input_rows], dtype=float),
    }


def _phase_flags(
    profile_type: str,
    phases: list[str],
    timestamps_us: np.ndarray,
    window_context: ULogWindowContext,
) -> dict[str, np.ndarray]:
    active_phases = ACTIVE_PHASES.get(profile_type, set())
    active_mask = np.asarray([1 if phase in active_phases else 0 for phase in phases], dtype=int)
    recover_mask = np.asarray([1 if phase == "recover" else 0 for phase in phases], dtype=int)
    stabilize_mask = np.asarray([1 if phase == "stabilize" else 0 for phase in phases], dtype=int)
    prefailsafe_mask = np.zeros(timestamps_us.shape, dtype=int)
    if window_context.prefailsafe_start_us is not None and window_context.prefailsafe_end_us is not None:
        prefailsafe_mask = (
            (timestamps_us >= float(window_context.prefailsafe_start_us))
            & (timestamps_us <= float(window_context.prefailsafe_end_us))
        ).astype(int)
    return {
        "active_window": active_mask,
        "recover_window": recover_mask,
        "stabilize_window": stabilize_mask,
        "prefailsafe_window": prefailsafe_mask,
    }


def _estimate_offset_and_context(
    ulog: ULog,
    manifest: dict[str, Any],
    input_rows: list[dict[str, Any]],
    status_rows: list[dict[str, Any]],
) -> tuple[float | None, ULogWindowContext]:
    context = build_window_context_from_aligned_events(ulog, manifest, input_rows, status_rows)
    active_rows = [row for row in input_rows if str(row.get("phase", "")) in ACTIVE_PHASES.get(str(manifest.get("profile_type", "")), set())]
    if not active_rows or context.active_start_us is None:
        return None, context
    active_start_ns = min(_int_value(row.get("publish_time_ns")) for row in active_rows)
    return float(context.active_start_us) - (active_start_ns / 1000.0), context


def _build_attitude_state_series_from_ulog(ulog: ULog) -> dict[str, SampleSeries | None]:
    dataset = next((item for item in ulog.data_list if item.name == "vehicle_attitude"), None)
    if dataset is None or "timestamp" not in dataset.data:
        return {"state_roll": None, "state_pitch": None, "state_yaw": None}
    timestamps = np.asarray(dataset.data["timestamp"], dtype=float)
    q_w = np.asarray(dataset.data.get("q[0]"), dtype=float)
    q_x = np.asarray(dataset.data.get("q[1]"), dtype=float)
    q_y = np.asarray(dataset.data.get("q[2]"), dtype=float)
    q_z = np.asarray(dataset.data.get("q[3]"), dtype=float)
    if not all(array.size == timestamps.size for array in (q_w, q_x, q_y, q_z)):
        return {"state_roll": None, "state_pitch": None, "state_yaw": None}
    euler = np.asarray(
        [quaternion_to_euler([float(w), float(x), float(y), float(z)]) for w, x, y, z in zip(q_w, q_x, q_y, q_z)],
        dtype=float,
    )
    roll_series = _prepare_series(timestamps, euler[:, 0])
    pitch_series = _prepare_series(timestamps, euler[:, 1])
    yaw_series = _prepare_series(timestamps, euler[:, 2])
    if yaw_series is not None:
        yaw_series.angle = True
    return {
        "state_roll": roll_series,
        "state_pitch": pitch_series,
        "state_yaw": yaw_series,
    }


def _build_local_position_series_from_ulog(ulog: ULog) -> dict[str, SampleSeries | None]:
    field_map = {
        "state_x": "x",
        "state_y": "y",
        "state_z": "z",
        "state_vx": "vx",
        "state_vy": "vy",
        "state_vz": "vz",
    }
    return {
        output_name: _build_series_from_ulog(ulog, "vehicle_local_position", value_key)
        for output_name, value_key in field_map.items()
    }


def _build_status_series_from_ulog(ulog: ULog) -> dict[str, SampleSeries | None]:
    return {
        "status_nav_state": _build_series_from_ulog(ulog, "vehicle_status", "nav_state", discrete=True),
        "status_arming_state": _build_series_from_ulog(ulog, "vehicle_status", "arming_state", discrete=True),
        "status_failsafe": _build_series_from_ulog(ulog, "vehicle_status", "failsafe", discrete=True),
        "status_failure_detector": _build_series_from_ulog(
            ulog,
            "vehicle_status",
            "failure_detector_status",
            discrete=True,
        ),
    }


def _build_manual_echo_series_from_ulog(ulog: ULog) -> dict[str, SampleSeries | None]:
    field_map = {
        "manual_echo_roll": "roll",
        "manual_echo_pitch": "pitch",
        "manual_echo_yaw": "yaw",
        "manual_echo_throttle": "throttle",
    }
    return {
        output_name: _build_series_from_ulog(ulog, "manual_control_setpoint", value_key)
        for output_name, value_key in field_map.items()
    }


def _build_ulog_series(ulog: ULog) -> dict[str, SampleSeries | None]:
    field_map = {
        "attitude_sp_roll": ("vehicle_attitude_setpoint", "roll_body", False, False),
        "attitude_sp_pitch": ("vehicle_attitude_setpoint", "pitch_body", False, False),
        "attitude_sp_yaw": ("vehicle_attitude_setpoint", "yaw_body", True, False),
        "attitude_sp_thrust_z": ("vehicle_attitude_setpoint", "thrust_body[2]", False, False),
        "rates_sp_roll": ("vehicle_rates_setpoint", "roll", False, False),
        "rates_sp_pitch": ("vehicle_rates_setpoint", "pitch", False, False),
        "rates_sp_yaw": ("vehicle_rates_setpoint", "yaw", False, False),
        "rates_sp_thrust_z": ("vehicle_rates_setpoint", "thrust_body[2]", False, False),
        "state_roll_rate": ("vehicle_angular_velocity", "xyz[0]", False, False),
        "state_pitch_rate": ("vehicle_angular_velocity", "xyz[1]", False, False),
        "state_yaw_rate": ("vehicle_angular_velocity", "xyz[2]", False, False),
        "torque_sp_x": ("vehicle_torque_setpoint", "xyz[0]", False, False),
        "torque_sp_y": ("vehicle_torque_setpoint", "xyz[1]", False, False),
        "torque_sp_z": ("vehicle_torque_setpoint", "xyz[2]", False, False),
        "thrust_sp_x": ("vehicle_thrust_setpoint", "xyz[0]", False, False),
        "thrust_sp_y": ("vehicle_thrust_setpoint", "xyz[1]", False, False),
        "thrust_sp_z": ("vehicle_thrust_setpoint", "xyz[2]", False, False),
        "allocator_unallocated_torque_x": ("control_allocator_status", "unallocated_torque[0]", False, False),
        "allocator_unallocated_torque_y": ("control_allocator_status", "unallocated_torque[1]", False, False),
        "allocator_unallocated_torque_z": ("control_allocator_status", "unallocated_torque[2]", False, False),
        "allocator_torque_setpoint_achieved": ("control_allocator_status", "torque_setpoint_achieved", False, False),
        "allocator_thrust_setpoint_achieved": ("control_allocator_status", "thrust_setpoint_achieved", False, False),
    }
    signals: dict[str, SampleSeries | None] = {}
    for output_name, (dataset_name, value_key, angle, discrete) in field_map.items():
        signals[output_name] = _build_series_from_ulog(ulog, dataset_name, value_key, angle=angle, discrete=discrete)
    for motor_index in range(DEFAULT_MOTOR_COUNT):
        signals[f"motor_{motor_index}"] = _build_series_from_ulog(
            ulog,
            "actuator_motors",
            f"control[{motor_index}]",
        )
    return signals


def _shift_next(values: np.ndarray) -> np.ndarray:
    shifted = np.full(values.shape, np.nan, dtype=float)
    if values.size > 1:
        shifted[:-1] = values[1:]
    return shifted


def _run_row_values(
    record: RunRecord,
    manifest: dict[str, Any],
    input_rows: list[dict[str, Any]],
    window_context: ULogWindowContext,
    offset_us: float,
) -> dict[str, np.ndarray | list[str] | list[int]]:
    filtered_rows = [row for row in input_rows if str(row.get("phase", "")) not in DEFAULT_EXCLUDED_PHASES]
    if not filtered_rows:
        filtered_rows = list(input_rows)
    filtered_rows.sort(key=lambda row: _int_value(row.get("publish_time_ns")))

    publish_times_ns = np.asarray([_int_value(row.get("publish_time_ns")) for row in filtered_rows], dtype=float)
    timestamps_us = (publish_times_ns / 1000.0) + offset_us
    elapsed_s = np.asarray([_float_value(row.get("elapsed_s"), 0.0) for row in filtered_rows], dtype=float)
    phases = [str(row.get("phase", "")) for row in filtered_rows]
    command_columns = _command_columns(filtered_rows)
    phase_columns = _phase_flags(record.profile_type, phases, timestamps_us, window_context)

    return {
        "sample_index": np.arange(len(filtered_rows), dtype=int),
        "timestamp_us": timestamps_us,
        "elapsed_s": elapsed_s,
        "phase": phases,
        **command_columns,
        **phase_columns,
    }


def build_identification_rows(record: RunRecord) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = _load_manifest(record.run_dir)
    telemetry_dir = record.run_dir / "telemetry"
    input_rows = _load_csv_rows(telemetry_dir / "input_profile.csv")
    status_rows = _load_csv_rows(telemetry_dir / "vehicle_status.csv")
    px4_log_path = Path(str(manifest.get("px4_log_path", ""))).expanduser()
    if not px4_log_path.exists():
        raise FileNotFoundError(f"缺少 px4 log: {px4_log_path}")

    ulog = ULog(str(px4_log_path))
    offset_us, window_context = _estimate_offset_and_context(ulog, manifest, input_rows, status_rows)
    if offset_us is None:
        raise RuntimeError(f"无法为 run {record.run_id} 估计 telemetry -> ULog 时间偏移")

    base_columns = _run_row_values(record, manifest, input_rows, window_context, offset_us)
    timestamps_us = np.asarray(base_columns["timestamp_us"], dtype=float)

    sampled_columns: dict[str, np.ndarray | list[str] | list[int]] = dict(base_columns)
    for name, series in {
        **_build_attitude_state_series_from_ulog(ulog),
        **_build_local_position_series_from_ulog(ulog),
        **_build_status_series_from_ulog(ulog),
        **_build_manual_echo_series_from_ulog(ulog),
        **_build_ulog_series(ulog),
    }.items():
        sampled_columns[name] = _sample_series(series, timestamps_us)

    motor_stack = np.vstack(
        [
            np.asarray(sampled_columns[f"motor_{motor_index}"], dtype=float)
            for motor_index in range(DEFAULT_MOTOR_COUNT)
        ]
    )
    sampled_columns["motor_max_abs"] = np.nanmax(np.abs(motor_stack), axis=0)
    sampled_columns["motor_clip_any"] = (sampled_columns["motor_max_abs"] >= 0.98).astype(int)
    sampled_columns["run_timing_valid"] = np.full(timestamps_us.shape, 1 if record.timing_valid else 0, dtype=int)
    sampled_columns["run_xy_contaminated"] = np.full(
        timestamps_us.shape,
        1 if any(item in XY_CONTAMINATION_ANOMALIES for item in record.anomalies) else 0,
        dtype=int,
    )
    sampled_columns["run_failsafe_event"] = np.full(timestamps_us.shape, int(record.failsafe_event), dtype=int)
    sampled_columns["run_nav_state_change"] = np.full(timestamps_us.shape, int(record.nav_state_change), dtype=int)

    for field in NEXT_STATE_FIELDS:
        sampled_columns[f"next_{field}"] = _shift_next(np.asarray(sampled_columns[field], dtype=float))
    sampled_columns["dt_next_s"] = _shift_next(timestamps_us) - timestamps_us
    sampled_columns["dt_next_s"] = np.asarray(sampled_columns["dt_next_s"], dtype=float) / 1_000_000.0

    rows: list[dict[str, Any]] = []
    row_count = len(base_columns["phase"])
    for index in range(row_count):
        row = {
            "run_id": record.run_id,
            "sim_world": record.sim_world,
            "input_chain": record.input_chain,
            "profile_type": record.profile_type,
            "axis": record.axis,
            "manual_mode": record.manual_mode,
            "run_input_peak": round(record.input_peak, 6),
            "status": record.status,
            "selection_reason": record.selection_reason,
            "config_signature": record.config_signature,
            "scenario_signature": record.scenario_signature,
            "timing_valid": 1 if record.timing_valid else 0,
            "sample_index": int(np.asarray(sampled_columns["sample_index"])[index]),
            "timestamp_us": int(round(float(timestamps_us[index]))),
            "elapsed_s": float(np.asarray(sampled_columns["elapsed_s"], dtype=float)[index]),
            "phase": str(base_columns["phase"][index]),
        }
        for key, values in sampled_columns.items():
            if key in {"sample_index", "timestamp_us", "elapsed_s", "phase"}:
                continue
            if isinstance(values, list):
                row[key] = values[index]
            else:
                row[key] = _csv_value(np.asarray(values)[index])
        rows.append(row)

    summary = {
        "run_id": record.run_id,
        "row_count": len(rows),
        "px4_log_path": str(px4_log_path),
        "offset_us": round(offset_us, 3),
        "active_start_us": window_context.active_start_us,
        "active_end_us": window_context.active_end_us,
        "prefailsafe_start_us": window_context.prefailsafe_start_us,
        "prefailsafe_end_us": window_context.prefailsafe_end_us,
    }
    return rows, summary


def _fieldnames(rows: list[dict[str, Any]]) -> list[str]:
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    return ordered


def _select_records(args: argparse.Namespace) -> list[RunRecord]:
    records = load_run_records(Path(args.artifact_root))
    matrix_run_ids: list[str] = []
    if args.matrix_dir:
        matrix_run_ids = _matrix_run_ids(Path(args.matrix_dir).expanduser().resolve())
    wanted = set(args.run_id) | set(matrix_run_ids)
    if wanted:
        records = [record for record in records if record.run_id in wanted]
    else:
        records = filter_records_by_world(records, args.world_filter)
        if args.input_chain != "all":
            records = [record for record in records if record.input_chain == args.input_chain]
        if args.profile_type != "all":
            records = [record for record in records if record.profile_type == args.profile_type]
        if args.axis != "all":
            records = [record for record in records if record.axis == args.axis]
    if not args.include_non_timing:
        records = [record for record in records if record.timing_valid]
    if not args.include_non_completed:
        records = [record for record in records if record.status == "completed"]
    if args.dedupe_by_scenario:
        records = select_nominal_records(records)
    records.sort(key=lambda item: item.start_time)
    if args.max_runs is not None:
        records = records[: max(args.max_runs, 0)]
    return records


def _default_output_dir(args: argparse.Namespace) -> Path:
    stamp = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d_%H%M%S")
    world = args.world_filter
    chain = args.input_chain
    return IDENTIFICATION_ROOT / f"{stamp}_{world}_{chain}"


def _write_summary(
    output_dir: Path,
    args: argparse.Namespace,
    records: list[RunRecord],
    per_run_summaries: list[dict[str, Any]],
    sample_count: int,
) -> None:
    summary_lines = [
        "# Identification Dataset Summary",
        "",
        f"- output_dir: {output_dir}",
        f"- runs: {len(records)}",
        f"- samples: {sample_count}",
        f"- world_filter: {args.world_filter}",
        f"- input_chain: {args.input_chain}",
        f"- profile_type: {args.profile_type}",
        f"- axis: {args.axis}",
        f"- include_non_timing: {args.include_non_timing}",
        f"- include_non_completed: {args.include_non_completed}",
        f"- dedupe_by_scenario: {args.dedupe_by_scenario}",
        "",
        "## Notes",
        "- sample grid uses `telemetry/input_profile.csv` publish times aligned into PX4 boot-time via event-based offset estimation.",
        "- state, setpoint, allocator and actuator columns all come from ULog; telemetry currently only participates in event-based time alignment.",
        "- `next_state_*` columns are one-step-ahead targets for first-stage `a/b` identification.",
        "- current default selection is intended for nominal, timing-valid, hover-local identification rather than windy disturbed fitting.",
        "",
        "## Included Runs",
    ]
    for summary in per_run_summaries:
        summary_lines.append(
            f"- {summary['run_id']}: rows={summary['row_count']}, offset_us={summary['offset_us']}"
        )
    (output_dir / "summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


def run_builder(args: argparse.Namespace) -> Path:
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else _default_output_dir(args)
    output_dir.mkdir(parents=True, exist_ok=True)
    per_run_dir = output_dir / "per_run"
    per_run_dir.mkdir(parents=True, exist_ok=True)

    records = _select_records(args)
    if not records:
        raise RuntimeError("没有匹配到可导出的 runs")

    manifest_payload = {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "artifact_root": str(Path(args.artifact_root).expanduser().resolve()),
        "world_filter": args.world_filter,
        "matrix_dir": str(Path(args.matrix_dir).expanduser().resolve()) if args.matrix_dir else "",
        "input_chain": args.input_chain,
        "profile_type": args.profile_type,
        "axis": args.axis,
        "include_non_timing": bool(args.include_non_timing),
        "include_non_completed": bool(args.include_non_completed),
        "dedupe_by_scenario": bool(args.dedupe_by_scenario),
        "runs": [record.run_id for record in records],
    }
    write_yaml(output_dir / "manifest.yaml", manifest_payload)

    selected_rows = [record.to_row() for record in records]
    write_rows_csv(output_dir / "selected_runs.csv", selected_rows, _fieldnames(selected_rows))

    merged_rows: list[dict[str, Any]] = []
    per_run_summaries: list[dict[str, Any]] = []
    for record in records:
        rows, summary = build_identification_rows(record)
        write_rows_csv(per_run_dir / f"{record.run_id}.csv", rows, _fieldnames(rows))
        merged_rows.extend(rows)
        per_run_summaries.append(summary)

    write_rows_csv(output_dir / "samples.csv", merged_rows, _fieldnames(merged_rows))
    write_rows_csv(output_dir / "run_windows.csv", per_run_summaries, _fieldnames(per_run_summaries))
    _write_summary(output_dir, args, records, per_run_summaries, len(merged_rows))
    return output_dir


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="导出 a/b 参数辨识用的 sample-level identification dataset。")
    parser.add_argument("--artifact-root", default=str(ARTIFACT_ROOT), help="runs artifact 根目录。")
    parser.add_argument("--world-filter", choices=("nominal", "windy", "all"), default=DEFAULT_WORLD_FILTER)
    parser.add_argument("--input-chain", choices=("attitude", "manual", "all"), default=DEFAULT_INPUT_CHAIN)
    parser.add_argument("--profile-type", choices=("baseline", "step", "pulse", "sweep", "all"), default="all")
    parser.add_argument("--axis", choices=("roll", "pitch", "yaw", "throttle", "composite", "all"), default="all")
    parser.add_argument("--matrix-dir", default="", help="matrix 目录；若提供，则按 runs.csv 中的 run_id 选取。")
    parser.add_argument("--run-id", action="append", default=[], help="显式指定 run_id，可重复传入。")
    parser.add_argument("--include-non-timing", action="store_true", help="包含 non-timing run。")
    parser.add_argument("--include-non-completed", action="store_true", help="包含非 completed run。")
    parser.add_argument(
        "--no-dedupe-by-scenario",
        dest="dedupe_by_scenario",
        action="store_false",
        help="不要按 scenario 去重；默认保留每个 scenario 的最新 completed run。",
    )
    parser.set_defaults(dedupe_by_scenario=True)
    parser.add_argument("--max-runs", type=int, default=None, help="最多导出多少个 runs。")
    parser.add_argument("--output-dir", default="", help="输出目录；默认写到 artifacts/identification/<timestamp>_*。")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    output_dir = run_builder(args)
    print(f"identification_dir={output_dir}")


if __name__ == "__main__":
    main()
