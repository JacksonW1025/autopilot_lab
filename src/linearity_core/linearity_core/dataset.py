from __future__ import annotations

import bisect
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from .canonical import (
    ACTUATOR_COLUMNS,
    BACKEND_PREFIX,
    COMMAND_COLUMNS,
    CONFIG_PROFILE_PREFIX,
    CONTROLLER_PARAM_PREFIX,
    INTERNAL_COLUMNS,
    MODE_PREFIX,
    SCENARIO_PREFIX,
    STATE_COLUMNS,
    TRACKING_ERROR_COLUMNS,
)
from .config import StudyConfig
from .io import read_rows_csv, read_yaml

PREPARED_SAMPLE_IDENTITY_COLUMNS = [
    "sample_id",
    "run_id",
    "backend",
    "mode",
    "scenario",
    "config_profile",
    "research_tier",
    "research_acceptance",
    "seed",
    "timestamp",
    "logical_step",
]


def _float_value(value: Any, default: float = math.nan) -> float:
    if value in ("", None):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _int_value(value: Any, default: int = 0) -> int:
    if value in ("", None):
        return default
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _nearest_row(rows: list[dict[str, Any]], time_key: str, target_ns: int) -> dict[str, Any] | None:
    if not rows:
        return None
    times = [_int_value(row.get(time_key), 0) for row in rows]
    index = bisect.bisect_left(times, target_ns)
    candidates: list[dict[str, Any]] = []
    if index < len(rows):
        candidates.append(rows[index])
    if index > 0:
        candidates.append(rows[index - 1])
    if not candidates:
        return None
    return min(candidates, key=lambda row: abs(_int_value(row.get(time_key), 0) - target_ns))


def _nearest_row_with_delta(rows: list[dict[str, Any]], time_key: str, target_ns: int) -> tuple[dict[str, Any] | None, int | None]:
    row = _nearest_row(rows, time_key, target_ns)
    if row is None:
        return None, None
    return row, abs(_int_value(row.get(time_key), 0) - target_ns)


def _sorted_rows(path: Path, time_key: str) -> list[dict[str, Any]]:
    rows = read_rows_csv(path)
    rows.sort(key=lambda row: _int_value(row.get(time_key), 0))
    return rows


def _safe_heading(row: dict[str, Any] | None) -> float:
    if row is None:
        return math.nan
    return _float_value(row.get("heading"))


def _safe_nanmedian_ms(values: list[float]) -> float:
    array = np.asarray(values, dtype=float)
    finite = array[np.isfinite(array)]
    if finite.size == 0:
        return math.nan
    return float(np.median(finite) / 1_000_000.0)


def _normalize_actuator(value: float, *, backend: str) -> float:
    if math.isnan(value):
        return value
    if backend == "ardupilot":
        return max(0.0, min(1.0, (value - 1000.0) / 1000.0))
    return value


def _px4_rows_from_manifest(run_dir: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    telemetry_dir = run_dir / "telemetry"
    input_rows = _sorted_rows(telemetry_dir / "input_trace.csv", "publish_time_ns")
    attitude_rows = _sorted_rows(telemetry_dir / "vehicle_attitude.csv", "received_time_ns")
    angular_velocity_rows = _sorted_rows(telemetry_dir / "vehicle_angular_velocity.csv", "received_time_ns")
    local_position_rows = _sorted_rows(telemetry_dir / "vehicle_local_position.csv", "received_time_ns")
    attitude_setpoint_rows = _sorted_rows(telemetry_dir / "vehicle_attitude_setpoint.csv", "received_time_ns")
    rates_setpoint_rows = _sorted_rows(telemetry_dir / "vehicle_rates_setpoint.csv", "received_time_ns")
    rate_ctrl_rows = _sorted_rows(telemetry_dir / "rate_ctrl_status.csv", "received_time_ns")
    allocator_rows = _sorted_rows(telemetry_dir / "control_allocator_status.csv", "received_time_ns")
    actuator_rows = _sorted_rows(telemetry_dir / "actuator_motors.csv", "received_time_ns")
    status_rows = _sorted_rows(telemetry_dir / "vehicle_status.csv", "received_time_ns")

    parameter_snapshot = manifest.get("parameter_snapshot_after", {}) or {}
    study_config = manifest.get("study_config", {}) or {}
    reporting = study_config.get("reporting", {}) if isinstance(study_config, dict) else {}
    max_alignment_error_ns = int(float(reporting.get("max_alignment_error_ms", 150.0)) * 1_000_000.0)
    base_rows: list[dict[str, Any]] = []
    for index, input_row in enumerate(input_rows):
        timestamp_ns = _int_value(input_row.get("publish_time_ns"), 0)
        attitude, attitude_delta = _nearest_row_with_delta(attitude_rows, "received_time_ns", timestamp_ns)
        rates, rates_delta = _nearest_row_with_delta(angular_velocity_rows, "received_time_ns", timestamp_ns)
        position, position_delta = _nearest_row_with_delta(local_position_rows, "received_time_ns", timestamp_ns)
        attitude_sp, attitude_sp_delta = _nearest_row_with_delta(attitude_setpoint_rows, "received_time_ns", timestamp_ns)
        rates_sp, rates_sp_delta = _nearest_row_with_delta(rates_setpoint_rows, "received_time_ns", timestamp_ns)
        integrators, integrators_delta = _nearest_row_with_delta(rate_ctrl_rows, "received_time_ns", timestamp_ns)
        allocator, allocator_delta = _nearest_row_with_delta(allocator_rows, "received_time_ns", timestamp_ns)
        actuators, actuators_delta = _nearest_row_with_delta(actuator_rows, "received_time_ns", timestamp_ns)
        status, status_delta = _nearest_row_with_delta(status_rows, "received_time_ns", timestamp_ns)
        alignment_deltas = [value for value in (attitude_delta, rates_delta, position_delta) if value is not None]
        max_core_alignment_ns = max(alignment_deltas) if alignment_deltas else math.nan
        alignment_failed = bool(alignment_deltas) and max_core_alignment_ns > max_alignment_error_ns

        row: dict[str, Any] = {
            "sample_id": f"{manifest['run_id']}:{index:06d}",
            "run_id": str(manifest["run_id"]),
            "backend": "px4",
            "mode": str(manifest.get("flight_mode", "")),
            "scenario": str(manifest.get("scenario", "")),
            "config_profile": str(manifest.get("config_profile", "")),
            "research_tier": str(manifest.get("research_tier", "")),
            "research_acceptance": str(manifest.get("research_acceptance", "")),
            "seed": int(manifest.get("seed", 0)),
            "timestamp": timestamp_ns,
            "logical_step": index,
            "command_roll": _float_value(input_row.get("command_roll", input_row.get("roll_body"))),
            "command_pitch": _float_value(input_row.get("command_pitch", input_row.get("pitch_body"))),
            "command_yaw": _float_value(input_row.get("command_yaw", input_row.get("yaw_body"))),
            "command_throttle": _float_value(input_row.get("command_throttle", input_row.get("thrust_z"))),
            "roll": _float_value(attitude.get("roll") if attitude else None),
            "pitch": _float_value(attitude.get("pitch") if attitude else None),
            "yaw": _float_value(attitude.get("yaw") if attitude else None),
            "roll_rate": _float_value(rates.get("xyz_x") if rates else None),
            "pitch_rate": _float_value(rates.get("xyz_y") if rates else None),
            "yaw_rate": _float_value(rates.get("xyz_z") if rates else None),
            "position_x": _float_value(position.get("x") if position else None),
            "position_y": _float_value(position.get("y") if position else None),
            "position_z": _float_value(position.get("z") if position else None),
            "velocity_x": _float_value(position.get("vx") if position else None),
            "velocity_y": _float_value(position.get("vy") if position else None),
            "velocity_z": _float_value(position.get("vz") if position else None),
            "altitude": -_float_value(position.get("z") if position else None),
            "vertical_speed": -_float_value(position.get("vz") if position else None),
            "heading": _safe_heading(position),
            "integrator_roll": _float_value(integrators.get("rollspeed_integ") if integrators else None),
            "integrator_pitch": _float_value(integrators.get("pitchspeed_integ") if integrators else None),
            "integrator_yaw": _float_value(integrators.get("yawspeed_integ") if integrators else None),
            "control_output_roll": _float_value(rates_sp.get("roll") if rates_sp else None),
            "control_output_pitch": _float_value(rates_sp.get("pitch") if rates_sp else None),
            "control_output_yaw": _float_value(rates_sp.get("yaw") if rates_sp else None),
            "torque_achieved": _float_value(allocator.get("torque_setpoint_achieved") if allocator else None),
            "thrust_achieved": _float_value(allocator.get("thrust_setpoint_achieved") if allocator else None),
            "saturation_ratio": _float_value(allocator.get("max_actuator_saturation") if allocator else None),
            "tracking_error_roll": _float_value(attitude_sp.get("roll_body") if attitude_sp else None)
            - _float_value(attitude.get("roll") if attitude else None),
            "tracking_error_pitch": _float_value(attitude_sp.get("pitch_body") if attitude_sp else None)
            - _float_value(attitude.get("pitch") if attitude else None),
            "tracking_error_yaw": _float_value(attitude_sp.get("yaw_body") if attitude_sp else None)
            - _float_value(attitude.get("yaw") if attitude else None),
            "tracking_error_rate_roll": _float_value(rates_sp.get("roll") if rates_sp else None)
            - _float_value(rates.get("xyz_x") if rates else None),
            "tracking_error_rate_pitch": _float_value(rates_sp.get("pitch") if rates_sp else None)
            - _float_value(rates.get("xyz_y") if rates else None),
            "tracking_error_rate_yaw": _float_value(rates_sp.get("yaw") if rates_sp else None)
            - _float_value(rates.get("xyz_z") if rates else None),
            "run_status": str(manifest.get("status", "")),
            "runtime_failsafe": _int_value(status.get("failsafe") if status else 0),
            "quality_alignment_attitude_ns": float(attitude_delta) if attitude_delta is not None else math.nan,
            "quality_alignment_rates_ns": float(rates_delta) if rates_delta is not None else math.nan,
            "quality_alignment_position_ns": float(position_delta) if position_delta is not None else math.nan,
            "quality_alignment_attitude_setpoint_ns": float(attitude_sp_delta) if attitude_sp_delta is not None else math.nan,
            "quality_alignment_rates_setpoint_ns": float(rates_sp_delta) if rates_sp_delta is not None else math.nan,
            "quality_alignment_integrator_ns": float(integrators_delta) if integrators_delta is not None else math.nan,
            "quality_alignment_allocator_ns": float(allocator_delta) if allocator_delta is not None else math.nan,
            "quality_alignment_actuator_ns": float(actuators_delta) if actuators_delta is not None else math.nan,
            "quality_alignment_status_ns": float(status_delta) if status_delta is not None else math.nan,
            "quality_missing_attitude": 1.0 if attitude is None else 0.0,
            "quality_missing_rates": 1.0 if rates is None else 0.0,
            "quality_missing_local_position": 1.0 if position is None else 0.0,
            "quality_missing_attitude_setpoint": 1.0 if attitude_sp is None else 0.0,
            "quality_missing_rates_setpoint": 1.0 if rates_sp is None else 0.0,
            "quality_missing_integrator": 1.0 if integrators is None else 0.0,
            "quality_missing_allocator": 1.0 if allocator is None else 0.0,
            "quality_missing_actuator": 1.0 if actuators is None else 0.0,
            "quality_missing_status": 1.0 if status is None else 0.0,
            "quality_alignment_failed": 1.0 if alignment_failed else 0.0,
        }
        for actuator_index, column in enumerate(ACTUATOR_COLUMNS, start=1):
            row[column] = _normalize_actuator(_float_value(actuators.get(f"motor_{actuator_index}") if actuators else None), backend="px4")
        for name, value in parameter_snapshot.items():
            row[f"{CONTROLLER_PARAM_PREFIX}{name}"] = _float_value(value)
        base_rows.append(row)
    return base_rows


def _ardupilot_rows_from_manifest(run_dir: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    telemetry_dir = run_dir / "telemetry"
    input_rows = _sorted_rows(telemetry_dir / "input_trace.csv", "publish_time_ns")
    attitude_rows = _sorted_rows(telemetry_dir / "attitude.csv", "received_time_ns")
    position_rows = _sorted_rows(telemetry_dir / "local_position.csv", "received_time_ns")
    heartbeat_rows = _sorted_rows(telemetry_dir / "heartbeat.csv", "received_time_ns")
    sys_status_rows = _sorted_rows(telemetry_dir / "sys_status.csv", "received_time_ns")
    bin_att_rows = _sorted_rows(telemetry_dir / "bin_att.csv", "received_time_ns")
    bin_rate_rows = _sorted_rows(telemetry_dir / "bin_rate.csv", "received_time_ns")
    bin_motb_rows = _sorted_rows(telemetry_dir / "bin_motb.csv", "received_time_ns")
    bin_rcou_rows = _sorted_rows(telemetry_dir / "bin_rcou.csv", "received_time_ns")

    parameter_snapshot = manifest.get("parameter_snapshot_after", {}) or {}
    study_config = manifest.get("study_config", {}) or {}
    reporting = study_config.get("reporting", {}) if isinstance(study_config, dict) else {}
    max_alignment_error_ns = int(float(reporting.get("max_alignment_error_ms", 150.0)) * 1_000_000.0)
    base_rows: list[dict[str, Any]] = []
    for index, input_row in enumerate(input_rows):
        timestamp_ns = _int_value(input_row.get("publish_time_ns"), 0)
        attitude, attitude_delta = _nearest_row_with_delta(attitude_rows, "received_time_ns", timestamp_ns)
        position, position_delta = _nearest_row_with_delta(position_rows, "received_time_ns", timestamp_ns)
        heartbeat, heartbeat_delta = _nearest_row_with_delta(heartbeat_rows, "received_time_ns", timestamp_ns)
        sys_status, sys_status_delta = _nearest_row_with_delta(sys_status_rows, "received_time_ns", timestamp_ns)
        bin_att, bin_att_delta = _nearest_row_with_delta(bin_att_rows, "received_time_ns", timestamp_ns)
        bin_rate, bin_rate_delta = _nearest_row_with_delta(bin_rate_rows, "received_time_ns", timestamp_ns)
        bin_motb, bin_motb_delta = _nearest_row_with_delta(bin_motb_rows, "received_time_ns", timestamp_ns)
        bin_rcou, bin_rcou_delta = _nearest_row_with_delta(bin_rcou_rows, "received_time_ns", timestamp_ns)
        alignment_deltas = [value for value in (attitude_delta, position_delta) if value is not None]
        max_core_alignment_ns = max(alignment_deltas) if alignment_deltas else math.nan
        alignment_failed = bool(alignment_deltas) and max_core_alignment_ns > max_alignment_error_ns

        roll = _float_value(bin_att.get("roll") if bin_att else attitude.get("roll") if attitude else None)
        pitch = _float_value(bin_att.get("pitch") if bin_att else attitude.get("pitch") if attitude else None)
        yaw = _float_value(bin_att.get("yaw") if bin_att else attitude.get("yaw") if attitude else None)
        roll_rate = _float_value(bin_rate.get("roll_rate") if bin_rate else attitude.get("rollspeed") if attitude else None)
        pitch_rate = _float_value(bin_rate.get("pitch_rate") if bin_rate else attitude.get("pitchspeed") if attitude else None)
        yaw_rate = _float_value(bin_rate.get("yaw_rate") if bin_rate else attitude.get("yawspeed") if attitude else None)

        row: dict[str, Any] = {
            "sample_id": f"{manifest['run_id']}:{index:06d}",
            "run_id": str(manifest["run_id"]),
            "backend": "ardupilot",
            "mode": str(manifest.get("flight_mode", "")),
            "scenario": str(manifest.get("scenario", "")),
            "config_profile": str(manifest.get("config_profile", "")),
            "research_tier": str(manifest.get("research_tier", "")),
            "research_acceptance": str(manifest.get("research_acceptance", "")),
            "seed": int(manifest.get("seed", 0)),
            "timestamp": timestamp_ns,
            "logical_step": index,
            "command_roll": _float_value(input_row.get("command_roll", input_row.get("roll_body"))),
            "command_pitch": _float_value(input_row.get("command_pitch", input_row.get("pitch_body"))),
            "command_yaw": _float_value(input_row.get("command_yaw", input_row.get("yaw_body"))),
            "command_throttle": _float_value(input_row.get("command_throttle", input_row.get("thrust_z"))),
            "roll": roll,
            "pitch": pitch,
            "yaw": yaw,
            "roll_rate": roll_rate,
            "pitch_rate": pitch_rate,
            "yaw_rate": yaw_rate,
            "position_x": _float_value(position.get("x") if position else None),
            "position_y": _float_value(position.get("y") if position else None),
            "position_z": _float_value(position.get("z") if position else None),
            "velocity_x": _float_value(position.get("vx") if position else None),
            "velocity_y": _float_value(position.get("vy") if position else None),
            "velocity_z": _float_value(position.get("vz") if position else None),
            "altitude": -_float_value(position.get("z") if position else None),
            "vertical_speed": -_float_value(position.get("vz") if position else None),
            "heading": yaw,
            "integrator_roll": _float_value(bin_att.get("err_rp") if bin_att else None),
            "integrator_pitch": _float_value(bin_att.get("err_rp") if bin_att else None),
            "integrator_yaw": _float_value(bin_att.get("err_yaw") if bin_att else None),
            "control_output_roll": _float_value(bin_rate.get("roll_out") if bin_rate else None),
            "control_output_pitch": _float_value(bin_rate.get("pitch_out") if bin_rate else None),
            "control_output_yaw": _float_value(bin_rate.get("yaw_out") if bin_rate else None),
            "torque_achieved": math.nan,
            "thrust_achieved": math.nan,
            "saturation_ratio": _float_value(bin_motb.get("th_limit") if bin_motb else None),
            "tracking_error_roll": _float_value(bin_att.get("des_roll") if bin_att else None) - roll,
            "tracking_error_pitch": _float_value(bin_att.get("des_pitch") if bin_att else None) - pitch,
            "tracking_error_yaw": _float_value(bin_att.get("des_yaw") if bin_att else None) - yaw,
            "tracking_error_rate_roll": _float_value(bin_rate.get("des_roll_rate") if bin_rate else None) - roll_rate,
            "tracking_error_rate_pitch": _float_value(bin_rate.get("des_pitch_rate") if bin_rate else None) - pitch_rate,
            "tracking_error_rate_yaw": _float_value(bin_rate.get("des_yaw_rate") if bin_rate else None) - yaw_rate,
            "run_status": str(manifest.get("status", "")),
            "runtime_failsafe": 0,
            "quality_alignment_attitude_ns": float(attitude_delta) if attitude_delta is not None else math.nan,
            "quality_alignment_rates_ns": float(bin_rate_delta) if bin_rate_delta is not None else math.nan,
            "quality_alignment_position_ns": float(position_delta) if position_delta is not None else math.nan,
            "quality_alignment_attitude_setpoint_ns": math.nan,
            "quality_alignment_rates_setpoint_ns": math.nan,
            "quality_alignment_integrator_ns": float(bin_att_delta) if bin_att_delta is not None else math.nan,
            "quality_alignment_allocator_ns": float(bin_motb_delta) if bin_motb_delta is not None else math.nan,
            "quality_alignment_actuator_ns": float(bin_rcou_delta) if bin_rcou_delta is not None else math.nan,
            "quality_alignment_status_ns": float(heartbeat_delta if heartbeat_delta is not None else sys_status_delta if sys_status_delta is not None else math.nan),
            "quality_missing_attitude": 1.0 if attitude is None and bin_att is None else 0.0,
            "quality_missing_rates": 1.0 if bin_rate is None and attitude is None else 0.0,
            "quality_missing_local_position": 1.0 if position is None else 0.0,
            "quality_missing_attitude_setpoint": 1.0,
            "quality_missing_rates_setpoint": 1.0,
            "quality_missing_integrator": 1.0 if bin_att is None else 0.0,
            "quality_missing_allocator": 1.0 if bin_motb is None else 0.0,
            "quality_missing_actuator": 1.0 if bin_rcou is None else 0.0,
            "quality_missing_status": 1.0 if heartbeat is None and sys_status is None else 0.0,
            "quality_alignment_failed": 1.0 if alignment_failed else 0.0,
        }
        for actuator_index, column in enumerate(ACTUATOR_COLUMNS, start=1):
            row[column] = _normalize_actuator(_float_value(bin_rcou.get(f"c{actuator_index}") if bin_rcou else None), backend="ardupilot")
        for name, value in parameter_snapshot.items():
            row[f"{CONTROLLER_PARAM_PREFIX}{name}"] = _float_value(value)
        base_rows.append(row)
    return base_rows


def _synthetic_rows_from_manifest(run_dir: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    rows = read_rows_csv(run_dir / "analysis_inputs" / "canonical_samples.csv")
    normalized: list[dict[str, Any]] = []
    for row in rows:
        normalized_row: dict[str, Any] = {
            key: (_float_value(value) if key not in {"sample_id", "run_id", "backend", "mode", "scenario", "config_profile"} else value)
            for key, value in row.items()
        }
        normalized_row["seed"] = _int_value(row.get("seed"), 0)
        normalized_row["logical_step"] = _int_value(row.get("logical_step"), 0)
        normalized_row["timestamp"] = _int_value(row.get("timestamp"), 0)
        normalized_row["run_status"] = str(manifest.get("status", "completed"))
        normalized_row["research_tier"] = str(manifest.get("research_tier", ""))
        normalized_row["research_acceptance"] = str(manifest.get("research_acceptance", ""))
        normalized.append(normalized_row)
    return normalized


def _categorical_one_hot(rows: list[dict[str, Any]], key: str, prefix: str) -> None:
    categories = sorted({str(row.get(key, "")) for row in rows if str(row.get(key, ""))})
    for row in rows:
        current = str(row.get(key, ""))
        for category in categories:
            row[f"{prefix}{category.lower()}"] = 1.0 if current == category else 0.0


def _add_default_future_columns(rows: list[dict[str, Any]], config: StudyConfig) -> None:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row["run_id"]), []).append(row)
    for run_rows in grouped.values():
        run_rows.sort(key=lambda item: int(item["logical_step"]))
        for index, row in enumerate(run_rows):
            future_index = index + config.prediction_horizon
            future_row = run_rows[future_index] if future_index < len(run_rows) else None
            row["quality_future_horizon_available"] = 1.0 if future_row is not None else 0.0
            row["quality_delta_state_available"] = 1.0 if future_row is not None else 0.0
            for column in STATE_COLUMNS:
                row[f"baseline_state_{column}"] = row.get(column, math.nan)
                row[f"future_state_{column}"] = future_row.get(column, math.nan) if future_row else math.nan
                row[f"delta_state_{column}"] = (
                    (future_row.get(column, math.nan) if future_row else math.nan) - _float_value(row.get(column))
                    if future_row is not None
                    else math.nan
                )
            if future_row is None:
                row["quality_window_summary_available"] = 0.0
                continue
            window_rows = run_rows[index + 1 : future_index + 1]
            row["quality_window_summary_available"] = 1.0 if window_rows else 0.0
            for column in ("roll", "pitch", "yaw", "roll_rate", "pitch_rate", "yaw_rate", "altitude", "vertical_speed"):
                values = [_float_value(item.get(column)) for item in window_rows if not math.isnan(_float_value(item.get(column)))]
                if not values:
                    row[f"window_mean_{column}"] = math.nan
                    row[f"window_peak_{column}"] = math.nan
                    row[f"window_rms_{column}"] = math.nan
                    continue
                row[f"window_mean_{column}"] = float(np.mean(values))
                row[f"window_peak_{column}"] = float(np.max(np.abs(values)))
                row[f"window_rms_{column}"] = float(np.sqrt(np.mean(np.square(values))))


@dataclass(slots=True)
class PreparedSampleTable:
    rows: list[dict[str, Any]]
    numeric_columns: list[str]

    def column(self, name: str) -> np.ndarray:
        return np.asarray([_float_value(row.get(name)) for row in self.rows], dtype=float)

    def string_column(self, name: str) -> list[str]:
        return [str(row.get(name, "")) for row in self.rows]

    def to_csv_rows(self) -> list[dict[str, Any]]:
        return self.rows


def prepared_sample_table_fieldnames(rows: list[dict[str, Any]]) -> list[str]:
    ordered_keys: list[str] = []
    seen: set[str] = set()
    for key in PREPARED_SAMPLE_IDENTITY_COLUMNS:
        if key not in seen:
            ordered_keys.append(key)
            seen.add(key)
    for row in rows:
        for key in row.keys():
            if key not in seen:
                ordered_keys.append(key)
                seen.add(key)
    return ordered_keys


def build_prepared_sample_table(run_dirs: list[Path], config: StudyConfig) -> tuple[PreparedSampleTable, dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    inventory_runs: list[dict[str, Any]] = []
    for run_dir in run_dirs:
        manifest = read_yaml(run_dir / "manifest.yaml")
        backend = str(manifest.get("backend", "")).strip().lower()
        if backend == "px4":
            run_rows = _px4_rows_from_manifest(run_dir, manifest)
        elif backend == "ardupilot":
            run_rows = _ardupilot_rows_from_manifest(run_dir, manifest)
        elif backend == "synthetic":
            run_rows = _synthetic_rows_from_manifest(run_dir, manifest)
        else:
            raise ValueError(f"不支持的 raw backend: {backend}")
        rows.extend(run_rows)
        inventory_runs.append(
            {
                "run_id": manifest.get("run_id", run_dir.name),
                "backend": backend,
                "row_count": len(run_rows),
                "flight_mode": manifest.get("flight_mode", ""),
                "scenario": manifest.get("scenario", ""),
                "config_profile": manifest.get("config_profile", ""),
                "research_tier": manifest.get("research_tier", ""),
                "research_acceptance": manifest.get("research_acceptance", ""),
                "research_rejection_reasons": list(manifest.get("research_rejection_reasons", []) or []),
                "raw_data_quality": manifest.get("data_quality", {}),
            }
        )

    rows.sort(key=lambda row: (str(row["run_id"]), int(row["logical_step"])))
    _categorical_one_hot(rows, "backend", BACKEND_PREFIX)
    _categorical_one_hot(rows, "mode", MODE_PREFIX)
    _categorical_one_hot(rows, "scenario", SCENARIO_PREFIX)
    _categorical_one_hot(rows, "config_profile", CONFIG_PROFILE_PREFIX)

    for row in rows:
        tracking_terms = [_float_value(row.get(name)) for name in TRACKING_ERROR_COLUMNS]
        tracking_terms = [value for value in tracking_terms if not math.isnan(value)]
        row["tracking_error_magnitude"] = float(np.linalg.norm(tracking_terms)) if tracking_terms else math.nan
        actuator_terms = [_float_value(row.get(name)) for name in ACTUATOR_COLUMNS]
        actuator_terms = [value for value in actuator_terms if not math.isnan(value)]
        row["control_effort_magnitude"] = float(np.mean(np.abs(actuator_terms))) if actuator_terms else math.nan

    _add_default_future_columns(rows, config)
    for row in rows:
        row["quality_actuator_response_available"] = 1.0 if all(not math.isnan(_float_value(row.get(name))) for name in ACTUATOR_COLUMNS) else 0.0
        row["quality_tracking_error_available"] = 1.0 if all(not math.isnan(_float_value(row.get(name))) for name in TRACKING_ERROR_COLUMNS) else 0.0

    numeric_columns: list[str] = []
    if rows:
        sample = rows[0]
        for key in sample:
            if key in {"sample_id", "run_id", "backend", "mode", "scenario", "config_profile", "run_status"}:
                continue
            if isinstance(rows[0].get(key), (int, float)) or key.startswith((CONTROLLER_PARAM_PREFIX, BACKEND_PREFIX, MODE_PREFIX, SCENARIO_PREFIX, CONFIG_PROFILE_PREFIX)):
                numeric_columns.append(key)

    inventory = {
        "row_count": len(rows),
        "run_count": len(inventory_runs),
        "runs": inventory_runs,
        "numeric_columns": numeric_columns,
        "controller_param_columns": sorted([name for name in numeric_columns if name.startswith(CONTROLLER_PARAM_PREFIX)]),
        "categorical_covariate_columns": sorted(
            [
                name
                for name in numeric_columns
                if name.startswith((BACKEND_PREFIX, MODE_PREFIX, SCENARIO_PREFIX, CONFIG_PROFILE_PREFIX))
            ]
        ),
        "internal_columns": sorted([name for name in numeric_columns if name in INTERNAL_COLUMNS]),
        "data_quality": {
            "alignment_failure_ratio": float(np.mean([_float_value(row.get("quality_alignment_failed"), 0.0) for row in rows])) if rows else 0.0,
            "missing_attitude_ratio": float(np.mean([_float_value(row.get("quality_missing_attitude"), 0.0) for row in rows])) if rows else 0.0,
            "missing_local_position_ratio": float(np.mean([_float_value(row.get("quality_missing_local_position"), 0.0) for row in rows])) if rows else 0.0,
            "missing_actuator_ratio": float(np.mean([_float_value(row.get("quality_missing_actuator"), 0.0) for row in rows])) if rows else 0.0,
            "future_horizon_available_ratio": float(np.mean([_float_value(row.get("quality_future_horizon_available"), 0.0) for row in rows])) if rows else 0.0,
            "delta_state_available_ratio": float(np.mean([_float_value(row.get("quality_delta_state_available"), 0.0) for row in rows])) if rows else 0.0,
            "window_summary_available_ratio": float(np.mean([_float_value(row.get("quality_window_summary_available"), 0.0) for row in rows])) if rows else 0.0,
            "actuator_response_available_ratio": float(np.mean([_float_value(row.get("quality_actuator_response_available"), 0.0) for row in rows])) if rows else 0.0,
            "tracking_error_available_ratio": float(np.mean([_float_value(row.get("quality_tracking_error_available"), 0.0) for row in rows])) if rows else 0.0,
            "median_alignment_attitude_ms": _safe_nanmedian_ms([_float_value(row.get("quality_alignment_attitude_ns")) for row in rows]) if rows else math.nan,
            "median_alignment_position_ms": _safe_nanmedian_ms([_float_value(row.get("quality_alignment_position_ns")) for row in rows]) if rows else math.nan,
            "accepted_row_ratio": float(np.mean([1.0 if str(row.get("research_acceptance", "")).strip().lower() == "accepted" else 0.0 for row in rows]))
            if rows
            else 0.0,
            "accepted_run_count": int(
                sum(1 for item in inventory_runs if str(item.get("research_acceptance", "")).strip().lower() == "accepted")
            ),
            "rejected_run_count": int(
                sum(1 for item in inventory_runs if str(item.get("research_acceptance", "")).strip().lower() == "rejected")
            ),
            "research_tiers": sorted({str(item.get("research_tier", "")) for item in inventory_runs if str(item.get("research_tier", ""))}),
        },
    }
    return PreparedSampleTable(rows=rows, numeric_columns=numeric_columns), inventory
