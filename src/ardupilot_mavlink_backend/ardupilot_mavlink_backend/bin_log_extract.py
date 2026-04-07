from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from pymavlink import DFReader


BIN_MESSAGES = ("ATT", "RATE", "MOTB", "RCOU")


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

    _write_csv(telemetry_dir / "bin_att.csv", rows_by_type["ATT"])
    _write_csv(telemetry_dir / "bin_rate.csv", rows_by_type["RATE"])
    _write_csv(telemetry_dir / "bin_motb.csv", rows_by_type["MOTB"])
    _write_csv(telemetry_dir / "bin_rcou.csv", rows_by_type["RCOU"])
    return {"message_counts": {name: len(rows) for name, rows in rows_by_type.items()}}
