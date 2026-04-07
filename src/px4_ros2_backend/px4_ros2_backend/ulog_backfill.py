from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from pyulog import ULog

from linearity_core.io import read_rows_csv, write_rows_csv


TOPIC_FIELDNAMES: dict[str, list[str]] = {
    "vehicle_angular_velocity": [
        "received_time_ns",
        "timestamp",
        "timestamp_sample",
        "xyz_x",
        "xyz_y",
        "xyz_z",
        "xyz_derivative_x",
        "xyz_derivative_y",
        "xyz_derivative_z",
    ],
    "vehicle_rates_setpoint": [
        "received_time_ns",
        "timestamp",
        "roll",
        "pitch",
        "yaw",
        "thrust_body_x",
        "thrust_body_y",
        "thrust_body_z",
        "reset_integral",
    ],
    "rate_ctrl_status": [
        "received_time_ns",
        "timestamp",
        "rollspeed_integ",
        "pitchspeed_integ",
        "yawspeed_integ",
        "wheel_rate_integ",
    ],
    "control_allocator_status": [
        "received_time_ns",
        "timestamp",
        "torque_setpoint_achieved",
        "thrust_setpoint_achieved",
        "unallocated_torque_x",
        "unallocated_torque_y",
        "unallocated_torque_z",
        "unallocated_thrust_x",
        "unallocated_thrust_y",
        "unallocated_thrust_z",
        "max_actuator_saturation",
        "handled_motor_failure_mask",
    ],
    "actuator_motors": [
        "received_time_ns",
        "timestamp",
        "timestamp_sample",
        "reversible_flags",
        "motor_1",
        "motor_2",
        "motor_3",
        "motor_4",
        "motor_5",
        "motor_6",
        "motor_7",
        "motor_8",
        "motor_9",
        "motor_10",
        "motor_11",
        "motor_12",
        "motors_peak",
    ],
    "vehicle_attitude_setpoint": [
        "received_time_ns",
        "timestamp",
        "roll_body",
        "pitch_body",
        "yaw_body",
        "yaw_sp_move_rate",
        "thrust_body_x",
        "thrust_body_y",
        "thrust_body_z",
        "reset_integral",
    ],
}

REFERENCE_TOPICS = (
    "vehicle_attitude",
    "vehicle_local_position",
    "vehicle_status",
)


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


def _median(values: list[int]) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    return int(ordered[len(ordered) // 2])


def _ulog_dataset_map(ulog_path: Path) -> dict[str, Any]:
    ulog = ULog(str(ulog_path), None)
    mapping: dict[str, Any] = {}
    for dataset in ulog.data_list:
        mapping.setdefault(dataset.name, []).append(dataset)
    return mapping


def _relative_index_pairs(left_count: int, right_count: int, sample_count: int) -> list[tuple[int, int]]:
    if left_count <= 0 or right_count <= 0 or sample_count <= 0:
        return []
    if sample_count == 1:
        return [(0, 0)]
    return [
        (
            int(round(index * (left_count - 1) / (sample_count - 1))),
            int(round(index * (right_count - 1) / (sample_count - 1))),
        )
        for index in range(sample_count)
    ]


def _offsets_from_reference_rows(rows: list[dict[str, Any]], dataset: Any) -> list[int]:
    ulog_timestamps = list(dataset.data.get("timestamp", []))
    if not rows or not ulog_timestamps:
        return []
    sample_count = min(256, len(rows), len(ulog_timestamps))
    offsets: list[int] = []
    for row_index, dataset_index in _relative_index_pairs(len(rows), len(ulog_timestamps), sample_count):
        received_time_ns = _int_value(rows[row_index].get("received_time_ns"), 0)
        ulog_timestamp = _int_value(ulog_timestamps[dataset_index], 0)
        if received_time_ns <= 0 or ulog_timestamp <= 0:
            continue
        offsets.append(received_time_ns - (ulog_timestamp * 1000))
    return offsets


def estimate_ulog_time_offset_ns(
    telemetry_dir: Path,
    *,
    datasets: dict[str, Any] | None = None,
) -> tuple[int | None, str | None, str | None]:
    for topic in REFERENCE_TOPICS:
        rows = read_rows_csv(telemetry_dir / f"{topic}.csv")
        topic_datasets = datasets.get(topic, []) if datasets else []
        if topic_datasets:
            offsets = _offsets_from_reference_rows(rows, topic_datasets[0])
            offset_ns = _median(offsets)
            if offset_ns is not None:
                return offset_ns, topic, None
        offsets: list[int] = []
        for row in rows:
            timestamp = _int_value(row.get("timestamp"), 0)
            received_time_ns = _int_value(row.get("received_time_ns"), 0)
            if timestamp <= 0 or received_time_ns <= 0:
                continue
            offsets.append(received_time_ns - (timestamp * 1000))
        offset_ns = _median(offsets)
        if offset_ns is not None:
            return offset_ns, topic, None
    return None, None, "timebase_unresolved"


def _has_rows(path: Path) -> bool:
    rows = read_rows_csv(path)
    return len(rows) > 0


def _backfill_vehicle_angular_velocity(dataset: Any, offset_ns: int) -> list[dict[str, Any]]:
    data = dataset.data
    timestamps = data["timestamp"]
    timestamp_samples = data["timestamp_sample"]
    xyz_x = data["xyz[0]"]
    xyz_y = data["xyz[1]"]
    xyz_z = data["xyz[2]"]
    derivative_x = data["xyz_derivative[0]"]
    derivative_y = data["xyz_derivative[1]"]
    derivative_z = data["xyz_derivative[2]"]
    return [
        {
            "received_time_ns": int(timestamp * 1000 + offset_ns),
            "timestamp": int(timestamp),
            "timestamp_sample": int(timestamp_sample),
            "xyz_x": float(x),
            "xyz_y": float(y),
            "xyz_z": float(z),
            "xyz_derivative_x": float(dx),
            "xyz_derivative_y": float(dy),
            "xyz_derivative_z": float(dz),
        }
        for timestamp, timestamp_sample, x, y, z, dx, dy, dz in zip(
            timestamps,
            timestamp_samples,
            xyz_x,
            xyz_y,
            xyz_z,
            derivative_x,
            derivative_y,
            derivative_z,
            strict=False,
        )
    ]


def _backfill_vehicle_rates_setpoint(dataset: Any, offset_ns: int) -> list[dict[str, Any]]:
    data = dataset.data
    return [
        {
            "received_time_ns": int(timestamp * 1000 + offset_ns),
            "timestamp": int(timestamp),
            "roll": float(roll),
            "pitch": float(pitch),
            "yaw": float(yaw),
            "thrust_body_x": float(tx),
            "thrust_body_y": float(ty),
            "thrust_body_z": float(tz),
            "reset_integral": bool(reset),
        }
        for timestamp, roll, pitch, yaw, tx, ty, tz, reset in zip(
            data["timestamp"],
            data["roll"],
            data["pitch"],
            data["yaw"],
            data["thrust_body[0]"],
            data["thrust_body[1]"],
            data["thrust_body[2]"],
            data["reset_integral"],
            strict=False,
        )
    ]


def _backfill_rate_ctrl_status(dataset: Any, offset_ns: int) -> list[dict[str, Any]]:
    data = dataset.data
    return [
        {
            "received_time_ns": int(timestamp * 1000 + offset_ns),
            "timestamp": int(timestamp),
            "rollspeed_integ": float(roll),
            "pitchspeed_integ": float(pitch),
            "yawspeed_integ": float(yaw),
            "wheel_rate_integ": float(wheel),
        }
        for timestamp, roll, pitch, yaw, wheel in zip(
            data["timestamp"],
            data["rollspeed_integ"],
            data["pitchspeed_integ"],
            data["yawspeed_integ"],
            data["wheel_rate_integ"],
            strict=False,
        )
    ]


def _backfill_control_allocator_status(dataset: Any, offset_ns: int) -> list[dict[str, Any]]:
    data = dataset.data
    saturation_columns = [data[f"actuator_saturation[{index}]"] for index in range(16)]
    rows: list[dict[str, Any]] = []
    for values in zip(
        data["timestamp"],
        data["torque_setpoint_achieved"],
        data["thrust_setpoint_achieved"],
        data["unallocated_torque[0]"],
        data["unallocated_torque[1]"],
        data["unallocated_torque[2]"],
        data["unallocated_thrust[0]"],
        data["unallocated_thrust[1]"],
        data["unallocated_thrust[2]"],
        data["handled_motor_failure_mask"],
        *saturation_columns,
        strict=False,
    ):
        timestamp = values[0]
        max_saturation = max(int(item) for item in values[10:26])
        rows.append(
            {
                "received_time_ns": int(timestamp * 1000 + offset_ns),
                "timestamp": int(timestamp),
                "torque_setpoint_achieved": bool(values[1]),
                "thrust_setpoint_achieved": bool(values[2]),
                "unallocated_torque_x": float(values[3]),
                "unallocated_torque_y": float(values[4]),
                "unallocated_torque_z": float(values[5]),
                "unallocated_thrust_x": float(values[6]),
                "unallocated_thrust_y": float(values[7]),
                "unallocated_thrust_z": float(values[8]),
                "max_actuator_saturation": max_saturation,
                "handled_motor_failure_mask": int(values[9]),
            }
        )
    return rows


def _backfill_actuator_motors(dataset: Any, offset_ns: int) -> list[dict[str, Any]]:
    data = dataset.data
    control_columns = [data[f"control[{index}]"] for index in range(12)]
    rows: list[dict[str, Any]] = []
    for values in zip(
        data["timestamp"],
        data["timestamp_sample"],
        data["reversible_flags"],
        *control_columns,
        strict=False,
    ):
        controls = [float(value) for value in values[3:15]]
        finite_controls = [abs(value) for value in controls if not math.isnan(value)]
        row: dict[str, Any] = {
            "received_time_ns": int(values[0] * 1000 + offset_ns),
            "timestamp": int(values[0]),
            "timestamp_sample": int(values[1]),
            "reversible_flags": int(values[2]),
            "motors_peak": max(finite_controls, default=math.nan),
        }
        for index, control in enumerate(controls, start=1):
            row[f"motor_{index}"] = control
        rows.append(row)
    return rows


def _backfill_vehicle_attitude_setpoint(dataset: Any, offset_ns: int) -> list[dict[str, Any]]:
    data = dataset.data
    return [
        {
            "received_time_ns": int(timestamp * 1000 + offset_ns),
            "timestamp": int(timestamp),
            "roll_body": float(roll),
            "pitch_body": float(pitch),
            "yaw_body": float(yaw),
            "yaw_sp_move_rate": float(yaw_rate),
            "thrust_body_x": float(tx),
            "thrust_body_y": float(ty),
            "thrust_body_z": float(tz),
            "reset_integral": bool(reset),
        }
        for timestamp, roll, pitch, yaw, yaw_rate, tx, ty, tz, reset in zip(
            data["timestamp"],
            data["roll_body"],
            data["pitch_body"],
            data["yaw_body"],
            data["yaw_sp_move_rate"],
            data["thrust_body[0]"],
            data["thrust_body[1]"],
            data["thrust_body[2]"],
            data["reset_integral"],
            strict=False,
        )
    ]


BACKFILLERS = {
    "vehicle_angular_velocity": _backfill_vehicle_angular_velocity,
    "vehicle_rates_setpoint": _backfill_vehicle_rates_setpoint,
    "rate_ctrl_status": _backfill_rate_ctrl_status,
    "control_allocator_status": _backfill_control_allocator_status,
    "actuator_motors": _backfill_actuator_motors,
    "vehicle_attitude_setpoint": _backfill_vehicle_attitude_setpoint,
}


def backfill_px4_ulog_topics(
    telemetry_dir: Path,
    *,
    ulog_path: str | Path | None,
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "ulog_path": str(ulog_path) if ulog_path else "",
        "timebase_reference_topic": "",
        "offset_ns": None,
        "topics": {},
        "failure_reasons": [],
    }
    if not ulog_path:
        summary["failure_reasons"].append("ulog_missing")
        return summary

    ulog_file = Path(str(ulog_path)).expanduser().resolve()
    if not ulog_file.exists():
        summary["failure_reasons"].append("ulog_missing")
        return summary

    datasets = _ulog_dataset_map(ulog_file)
    offset_ns, reference_topic, offset_error = estimate_ulog_time_offset_ns(telemetry_dir, datasets=datasets)
    summary["timebase_reference_topic"] = reference_topic or ""
    summary["offset_ns"] = offset_ns
    if offset_error is not None or offset_ns is None:
        summary["failure_reasons"].append(offset_error or "timebase_unresolved")
        for topic in BACKFILLERS:
            path = telemetry_dir / f"{topic}.csv"
            summary["topics"][topic] = {
                "source": "ros2" if _has_rows(path) else "missing",
                "row_count": len(read_rows_csv(path)) if path.exists() else 0,
                "failure_reason": offset_error or "timebase_unresolved",
            }
        return summary

    for topic, backfiller in BACKFILLERS.items():
        path = telemetry_dir / f"{topic}.csv"
        existing_rows = read_rows_csv(path)
        if existing_rows:
            summary["topics"][topic] = {
                "source": "ros2",
                "row_count": len(existing_rows),
            }
            continue
        topic_datasets = datasets.get(topic, [])
        if not topic_datasets:
            summary["topics"][topic] = {
                "source": "missing",
                "row_count": 0,
                "failure_reason": "ulog_missing_topic",
            }
            continue
        rows = backfiller(topic_datasets[0], offset_ns)
        write_rows_csv(path, rows, fieldnames=TOPIC_FIELDNAMES[topic])
        summary["topics"][topic] = {
            "source": "ulog_backfill",
            "row_count": len(rows),
        }
    return summary
