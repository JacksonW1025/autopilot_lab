from __future__ import annotations

import time
from typing import Any

from pymavlink import mavutil


def connect_mavlink(master_uri: str, timeout_s: float = 10.0, source_system: int = 250) -> mavutil.mavfile:
    master = mavutil.mavlink_connection(master_uri, source_system=source_system, autoreconnect=True)
    master.wait_heartbeat(timeout=timeout_s)
    return master


def close_mavlink(master: mavutil.mavfile | None) -> None:
    if master is None:
        return
    try:
        master.close()
    except Exception:
        pass


def _param_id_text(param_id: Any) -> str:
    if isinstance(param_id, bytes):
        return param_id.decode("ascii", errors="ignore").rstrip("\x00")
    if isinstance(param_id, str):
        return param_id.rstrip("\x00")
    return str(param_id).rstrip("\x00")


def _param_value_float(value: Any) -> float | None:
    if value in ("", None):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fetch_parameter(master: mavutil.mavfile, name: str, timeout_s: float = 5.0) -> float | None:
    master.mav.param_request_read_send(master.target_system, master.target_component, name.encode("ascii"), -1)
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        message = master.recv_match(type="PARAM_VALUE", blocking=True, timeout=0.5)
        if message is None:
            continue
        if _param_id_text(message.param_id) != name:
            continue
        value = _param_value_float(message.param_value)
        if value is not None:
            return value
    return None


def set_parameter(master: mavutil.mavfile, name: str, value: float, timeout_s: float = 5.0) -> bool:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        master.mav.param_set_send(
            master.target_system,
            master.target_component,
            name.encode("ascii"),
            float(value),
            mavutil.mavlink.MAV_PARAM_TYPE_REAL32,
        )
        remaining_s = max(0.1, min(1.0, deadline - time.monotonic()))
        current = fetch_parameter(master, name, timeout_s=remaining_s)
        if current is not None and abs(float(current) - float(value)) < 1e-4:
            return True
    return False


def snapshot_parameters(master: mavutil.mavfile, names: list[str], timeout_s: float = 5.0) -> dict[str, float | None]:
    return {name: fetch_parameter(master, name, timeout_s=timeout_s) for name in names}


def set_parameters(master: mavutil.mavfile, values: dict[str, Any], timeout_s: float = 5.0) -> dict[str, bool]:
    return {name: set_parameter(master, name, float(value), timeout_s=timeout_s) for name, value in values.items()}
