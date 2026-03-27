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


def fetch_parameter(master: mavutil.mavfile, name: str, timeout_s: float = 5.0) -> float | None:
    master.mav.param_request_read_send(master.target_system, master.target_component, name.encode("ascii"), -1)
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        message = master.recv_match(type="PARAM_VALUE", blocking=True, timeout=0.5)
        if message is None:
            continue
        message_name = message.param_id.decode("ascii", errors="ignore").rstrip("\x00")
        if message_name == name:
            return float(message.param_value)
    return None


def set_parameter(master: mavutil.mavfile, name: str, value: float, timeout_s: float = 5.0) -> bool:
    master.mav.param_set_send(
        master.target_system,
        master.target_component,
        name.encode("ascii"),
        float(value),
        mavutil.mavlink.MAV_PARAM_TYPE_REAL32,
    )
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        message = master.recv_match(type="PARAM_VALUE", blocking=True, timeout=0.5)
        if message is None:
            continue
        message_name = message.param_id.decode("ascii", errors="ignore").rstrip("\x00")
        if message_name != name:
            continue
        return abs(float(message.param_value) - float(value)) < 1e-4
    return False


def snapshot_parameters(master: mavutil.mavfile, names: list[str], timeout_s: float = 5.0) -> dict[str, float | None]:
    return {name: fetch_parameter(master, name, timeout_s=timeout_s) for name in names}


def set_parameters(master: mavutil.mavfile, values: dict[str, Any], timeout_s: float = 5.0) -> dict[str, bool]:
    return {name: set_parameter(master, name, float(value), timeout_s=timeout_s) for name, value in values.items()}
