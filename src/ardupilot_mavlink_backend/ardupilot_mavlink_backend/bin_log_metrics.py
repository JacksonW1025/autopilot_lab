from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any

from fep_core.config import RunConfig
from pymavlink import DFReader


BIN_MESSAGES = ("ATT", "RATE", "CTUN", "MOTB", "RCOU", "PIDR", "PIDP", "PIDY")


def _float_value(value: Any, default: float = 0.0) -> float:
    if value in ("", None):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _normalize_att(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "received_time_ns": int(_float_value(row.get("TimeUS")) * 1000.0),
        "des_roll": _float_value(row.get("DesRoll")),
        "roll": _float_value(row.get("Roll")),
        "des_pitch": _float_value(row.get("DesPitch")),
        "pitch": _float_value(row.get("Pitch")),
        "des_yaw": _float_value(row.get("DesYaw")),
        "yaw": _float_value(row.get("Yaw")),
        "err_rp": _float_value(row.get("ErrRP")),
        "err_yaw": _float_value(row.get("ErrYaw")),
        "aekf": _float_value(row.get("AEKF")),
    }


def _normalize_rate(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "received_time_ns": int(_float_value(row.get("TimeUS")) * 1000.0),
        "des_roll_rate": _float_value(row.get("RDes")),
        "roll_rate": _float_value(row.get("R")),
        "roll_out": _float_value(row.get("ROut")),
        "des_pitch_rate": _float_value(row.get("PDes")),
        "pitch_rate": _float_value(row.get("P")),
        "pitch_out": _float_value(row.get("POut")),
        "des_yaw_rate": _float_value(row.get("YDes")),
        "yaw_rate": _float_value(row.get("Y")),
        "yaw_out": _float_value(row.get("YOut")),
        "des_accel": _float_value(row.get("ADes")),
        "accel": _float_value(row.get("A")),
        "accel_out": _float_value(row.get("AOut")),
    }


def _normalize_ctun(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "received_time_ns": int(_float_value(row.get("TimeUS")) * 1000.0),
        "th_i": _float_value(row.get("ThI")),
        "abst": _float_value(row.get("ABst")),
        "th_o": _float_value(row.get("ThO")),
        "th_h": _float_value(row.get("ThH")),
        "d_alt": _float_value(row.get("DAlt")),
        "alt": _float_value(row.get("Alt")),
        "b_alt": _float_value(row.get("BAlt")),
        "ds_alt": _float_value(row.get("DSAlt")),
        "s_alt": _float_value(row.get("SAlt")),
        "t_alt": _float_value(row.get("TAlt")),
        "d_crt": _float_value(row.get("DCRt")),
        "crt": _float_value(row.get("CRt")),
    }


def _normalize_motb(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "received_time_ns": int(_float_value(row.get("TimeUS")) * 1000.0),
        "lift_max": _float_value(row.get("LiftMax")),
        "bat_volt": _float_value(row.get("BatVolt")),
        "bat_res": _float_value(row.get("BatRes")),
        "th_limit": _float_value(row.get("ThLimit")),
    }


def _normalize_rcou(row: dict[str, Any]) -> dict[str, Any]:
    normalized = {"received_time_ns": int(_float_value(row.get("TimeUS")) * 1000.0)}
    channel_values: list[float] = []
    active_channel_values: list[float] = []
    for index in range(1, 15):
        key = f"C{index}"
        value = _float_value(row.get(key))
        normalized[f"c{index}"] = value
        channel_values.append(value)
        if value > 900.0:
            active_channel_values.append(value)
    normalized["max_channel"] = max(channel_values, default=0.0)
    normalized["min_channel"] = min(channel_values, default=0.0)
    normalized["active_max_channel"] = max(active_channel_values, default=0.0)
    normalized["active_min_channel"] = min(active_channel_values, default=0.0)
    return normalized


def _normalize_pid(row: dict[str, Any]) -> dict[str, Any]:
    normalized = {"received_time_ns": int(_float_value(row.get("TimeUS")) * 1000.0)}
    for key, value in row.items():
        if key in {"mavpackettype", "TimeUS"}:
            continue
        normalized[str(key).lower()] = value
    return normalized


def _axis_series(config: RunConfig, att_rows: list[dict[str, Any]], rate_rows: list[dict[str, Any]]) -> tuple[list[float], list[float]]:
    if config.resolved_study_layer == "rate_single_loop":
        if config.axis == "roll":
            return [row["des_roll_rate"] for row in rate_rows], [row["roll_rate"] for row in rate_rows]
        if config.axis == "pitch":
            return [row["des_pitch_rate"] for row in rate_rows], [row["pitch_rate"] for row in rate_rows]
        if config.axis == "yaw":
            return [row["des_yaw_rate"] for row in rate_rows], [row["yaw_rate"] for row in rate_rows]
        if config.axis == "composite":
            desired = [
                max(abs(row["des_roll_rate"]), abs(row["des_pitch_rate"]), abs(row["des_yaw_rate"])) for row in rate_rows
            ]
            actual = [max(abs(row["roll_rate"]), abs(row["pitch_rate"]), abs(row["yaw_rate"])) for row in rate_rows]
            return desired, actual
        return [], []

    if config.axis == "roll":
        return [row["des_roll"] for row in att_rows], [row["roll"] for row in att_rows]
    if config.axis == "pitch":
        return [row["des_pitch"] for row in att_rows], [row["pitch"] for row in att_rows]
    if config.axis == "yaw":
        return [row["des_yaw"] for row in att_rows], [row["yaw"] for row in att_rows]
    if config.axis == "composite":
        desired = [max(abs(row["des_roll"]), abs(row["des_pitch"]), abs(row["des_yaw"])) for row in att_rows]
        actual = [max(abs(row["roll"]), abs(row["pitch"]), abs(row["yaw"])) for row in att_rows]
        return desired, actual
    return [], []


def _tracking_metrics(desired: list[float], actual: list[float]) -> tuple[float, float]:
    if not desired or not actual:
        return math.nan, math.nan
    count = min(len(desired), len(actual))
    errors = [float(desired[index]) - float(actual[index]) for index in range(count)]
    if not errors:
        return math.nan, math.nan
    peak = max(abs(value) for value in errors)
    rms = math.sqrt(sum(value * value for value in errors) / len(errors))
    return round(peak, 6), round(rms, 6)


def _response_delay_ms(
    desired: list[float],
    actual: list[float],
    time_ns: list[int],
) -> float:
    if not desired or not actual or not time_ns:
        return math.nan
    count = min(len(desired), len(actual), len(time_ns))
    desired = desired[:count]
    actual = actual[:count]
    time_ns = time_ns[:count]
    input_peak = max((abs(value) for value in desired), default=0.0)
    if input_peak <= 0.0:
        return math.nan
    threshold = max(input_peak * 0.1, input_peak * 0.05, 0.002)
    input_cross_ns = None
    for timestamp_ns, value in zip(time_ns, desired):
        if abs(value) >= threshold:
            input_cross_ns = timestamp_ns
            break
    if input_cross_ns is None:
        return math.nan
    baseline = desired[0] * 0.0
    for timestamp_ns, value in zip(time_ns, actual):
        if timestamp_ns < input_cross_ns:
            baseline = value
            continue
        if abs(value - baseline) >= threshold:
            return round((timestamp_ns - input_cross_ns) / 1_000_000.0, 3)
    return math.nan


def summarize_bin_log(
    config: RunConfig,
    bin_log_path: str | Path,
    telemetry_dir: Path | None = None,
) -> dict[str, Any]:
    path = Path(bin_log_path).expanduser().resolve()
    rows_by_type: dict[str, list[dict[str, Any]]] = {message_type: [] for message_type in BIN_MESSAGES}
    reader = DFReader.DFReader_binary(str(path))
    while True:
        message = reader.recv_msg()
        if message is None:
            break
        message_type = message.get_type()
        if message_type not in rows_by_type:
            continue
        raw_row = message.to_dict()
        if message_type == "ATT":
            rows_by_type[message_type].append(_normalize_att(raw_row))
        elif message_type == "RATE":
            rows_by_type[message_type].append(_normalize_rate(raw_row))
        elif message_type == "CTUN":
            rows_by_type[message_type].append(_normalize_ctun(raw_row))
        elif message_type == "MOTB":
            rows_by_type[message_type].append(_normalize_motb(raw_row))
        elif message_type == "RCOU":
            rows_by_type[message_type].append(_normalize_rcou(raw_row))
        else:
            rows_by_type[message_type].append(_normalize_pid(raw_row))

    if telemetry_dir is not None:
        _write_csv(telemetry_dir / "bin_att.csv", rows_by_type["ATT"])
        _write_csv(telemetry_dir / "bin_rate.csv", rows_by_type["RATE"])
        _write_csv(telemetry_dir / "bin_ctun.csv", rows_by_type["CTUN"])
        _write_csv(telemetry_dir / "bin_motb.csv", rows_by_type["MOTB"])
        _write_csv(telemetry_dir / "bin_rcou.csv", rows_by_type["RCOU"])
        _write_csv(telemetry_dir / "bin_pidr.csv", rows_by_type["PIDR"])
        _write_csv(telemetry_dir / "bin_pidp.csv", rows_by_type["PIDP"])
        _write_csv(telemetry_dir / "bin_pidy.csv", rows_by_type["PIDY"])

    desired_series, actual_series = _axis_series(config, rows_by_type["ATT"], rows_by_type["RATE"])
    reference_rows = rows_by_type["RATE"] if config.resolved_study_layer == "rate_single_loop" else rows_by_type["ATT"]
    time_ns = [int(row["received_time_ns"]) for row in reference_rows]
    tracking_peak, tracking_rms = _tracking_metrics(desired_series, actual_series)

    rate_peak, rate_rms = _tracking_metrics(
        [row["des_roll_rate"] for row in rows_by_type["RATE"]],
        [row["roll_rate"] for row in rows_by_type["RATE"]],
    )
    if config.axis == "pitch":
        rate_peak, rate_rms = _tracking_metrics(
            [row["des_pitch_rate"] for row in rows_by_type["RATE"]],
            [row["pitch_rate"] for row in rows_by_type["RATE"]],
        )
    elif config.axis == "yaw":
        rate_peak, rate_rms = _tracking_metrics(
            [row["des_yaw_rate"] for row in rows_by_type["RATE"]],
            [row["yaw_rate"] for row in rows_by_type["RATE"]],
        )

    max_motor_output = max((row["max_channel"] for row in rows_by_type["RCOU"]), default=math.nan)
    rcou_high_frac = 0.0
    if rows_by_type["RCOU"]:
        saturated = [
            row
            for row in rows_by_type["RCOU"]
            if row["active_max_channel"] >= 1950.0 or (row["active_min_channel"] > 0.0 and row["active_min_channel"] <= 1050.0)
        ]
        rcou_high_frac = len(saturated) / len(rows_by_type["RCOU"])
    thlimit_peak = max((row["th_limit"] for row in rows_by_type["MOTB"]), default=math.nan)

    return {
        "bin_parse_status": "parsed",
        "bin_message_counts": {key: len(value) for key, value in rows_by_type.items() if value},
        "tracking_error_peak": tracking_peak,
        "tracking_error_rms": tracking_rms,
        "response_delay_ms": _response_delay_ms(desired_series, actual_series, time_ns),
        "rate_tracking_error_peak": rate_peak,
        "rate_tracking_error_rms": rate_rms,
        "max_motor_output": "" if math.isnan(max_motor_output) else round(max_motor_output, 3),
        "clip_frac": round(rcou_high_frac, 6),
        "thlimit_peak": "" if math.isnan(thlimit_peak) else round(thlimit_peak, 6),
    }
