from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from pymavlink import DFReader


BIN_MESSAGES = ("ATT", "RATE", "MOTB", "RCOU", "POS", "AHR2", "BAT", "MODE", "ORGN")


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
    }


def _normalize_motb(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "received_time_ns": int(_float_value(row.get("TimeUS")) * 1000.0),
        "th_limit": _float_value(row.get("ThLimit")),
        "lift_max": _float_value(row.get("LiftMax")),
    }


def _normalize_rcou(row: dict[str, Any]) -> dict[str, Any]:
    normalized = {"received_time_ns": int(_float_value(row.get("TimeUS")) * 1000.0)}
    for index in range(1, 9):
        normalized[f"c{index}"] = _float_value(row.get(f"C{index}"))
    return normalized


def _normalize_pos(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "received_time_ns": int(_float_value(row.get("TimeUS")) * 1000.0),
        "lat_deg": _float_value(row.get("Lat")),
        "lon_deg": _float_value(row.get("Lng")),
        "alt_m": _float_value(row.get("Alt")),
        "rel_home_alt_m": _float_value(row.get("RelHomeAlt")),
        "rel_origin_alt_m": _float_value(row.get("RelOriginAlt")),
    }


def _normalize_ahr2(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "received_time_ns": int(_float_value(row.get("TimeUS")) * 1000.0),
        "roll_deg": _float_value(row.get("Roll")),
        "pitch_deg": _float_value(row.get("Pitch")),
        "yaw_deg": _float_value(row.get("Yaw")),
        "alt_m": _float_value(row.get("Alt")),
        "lat_deg": _float_value(row.get("Lat")),
        "lon_deg": _float_value(row.get("Lng")),
    }


def _normalize_bat(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "received_time_ns": int(_float_value(row.get("TimeUS")) * 1000.0),
        "instance": int(_float_value(row.get("Instance"))),
        "voltage_v": _float_value(row.get("Volt")),
        "current_a": _float_value(row.get("Curr")),
        "battery_remaining_pct": _float_value(row.get("RemPct")),
    }


def _normalize_mode(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "received_time_ns": int(_float_value(row.get("TimeUS")) * 1000.0),
        "mode": int(_float_value(row.get("Mode"))),
        "mode_num": int(_float_value(row.get("ModeNum"))),
        "reason": int(_float_value(row.get("Rsn"))),
    }


def _normalize_orgn(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "received_time_ns": int(_float_value(row.get("TimeUS")) * 1000.0),
        "type": int(_float_value(row.get("Type"))),
        "lat_deg": _float_value(row.get("Lat")),
        "lon_deg": _float_value(row.get("Lng")),
        "alt_m": _float_value(row.get("Alt")),
    }


def extract_bin_log(bin_log_path: str | Path, telemetry_dir: Path) -> dict[str, Any]:
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
        elif message_type == "MOTB":
            rows_by_type[message_type].append(_normalize_motb(raw_row))
        elif message_type == "RCOU":
            rows_by_type[message_type].append(_normalize_rcou(raw_row))
        elif message_type == "POS":
            rows_by_type[message_type].append(_normalize_pos(raw_row))
        elif message_type == "AHR2":
            rows_by_type[message_type].append(_normalize_ahr2(raw_row))
        elif message_type == "BAT":
            rows_by_type[message_type].append(_normalize_bat(raw_row))
        elif message_type == "MODE":
            rows_by_type[message_type].append(_normalize_mode(raw_row))
        elif message_type == "ORGN":
            rows_by_type[message_type].append(_normalize_orgn(raw_row))

    _write_csv(telemetry_dir / "bin_att.csv", rows_by_type["ATT"])
    _write_csv(telemetry_dir / "bin_rate.csv", rows_by_type["RATE"])
    _write_csv(telemetry_dir / "bin_motb.csv", rows_by_type["MOTB"])
    _write_csv(telemetry_dir / "bin_rcou.csv", rows_by_type["RCOU"])
    _write_csv(telemetry_dir / "bin_pos.csv", rows_by_type["POS"])
    _write_csv(telemetry_dir / "bin_ahr2.csv", rows_by_type["AHR2"])
    _write_csv(telemetry_dir / "bin_bat.csv", rows_by_type["BAT"])
    _write_csv(telemetry_dir / "bin_mode.csv", rows_by_type["MODE"])
    _write_csv(telemetry_dir / "bin_orgn.csv", rows_by_type["ORGN"])
    return {"message_counts": {name: len(rows) for name, rows in rows_by_type.items()}}
