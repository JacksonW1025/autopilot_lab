from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class RunConfig:
    phase: int
    input_chain: str
    axis: str
    profile_type: str
    amplitude: float
    bias: float
    start_after_s: float
    duration_s: float
    sample_rate_hz: float
    hover_thrust: float
    hold_s: float
    timing_required: bool
    extras: dict[str, Any] = field(default_factory=dict)
    source_path: Path | None = None
    operator: str = "Codex"
    warmup_cycles: int = 10
    takeoff_thrust: float = -0.80
    takeoff_thrust_max: float = -0.92
    takeoff_ramp_s: float = 2.0
    takeoff_altitude_m: float = 1.5
    takeoff_position_tolerance_m: float = 0.2
    takeoff_velocity_tolerance_m: float = 0.3
    takeoff_settle_s: float = 1.5
    takeoff_timeout_s: float = 10.0
    min_takeoff_clearance_m: float = 0.35
    min_profile_clearance_m: float = 0.25
    altitude_hold_kp: float = 0.12
    altitude_hold_kd: float = 0.08
    thrust_z_min: float = -0.95
    thrust_z_max: float = -0.35
    land_timeout_s: float = 8.0
    ready_timeout_s: float = 20.0

    @classmethod
    def from_dict(cls, data: dict[str, Any], source_path: Path | None = None) -> "RunConfig":
        required = {
            "phase",
            "input_chain",
            "axis",
            "profile_type",
            "amplitude",
            "bias",
            "start_after_s",
            "duration_s",
            "sample_rate_hz",
            "hover_thrust",
            "hold_s",
            "timing_required",
        }
        missing = sorted(required - data.keys())
        if missing:
            raise ValueError(f"配置缺少字段: {', '.join(missing)}")

        optional_runtime = {
            "operator",
            "warmup_cycles",
            "takeoff_thrust",
            "takeoff_thrust_max",
            "takeoff_ramp_s",
            "takeoff_altitude_m",
            "takeoff_position_tolerance_m",
            "takeoff_velocity_tolerance_m",
            "takeoff_settle_s",
            "takeoff_timeout_s",
            "min_takeoff_clearance_m",
            "min_profile_clearance_m",
            "altitude_hold_kp",
            "altitude_hold_kd",
            "thrust_z_min",
            "thrust_z_max",
            "land_timeout_s",
            "ready_timeout_s",
        }
        extras = {key: value for key, value in data.items() if key not in required and key not in optional_runtime}
        input_chain = str(data["input_chain"])
        if input_chain not in {"attitude", "manual"}:
            raise ValueError(f"不支持的 input_chain: {input_chain}")

        profile_type = str(data["profile_type"])
        if profile_type not in {"baseline", "step", "sweep", "pulse"}:
            raise ValueError(f"不支持的 profile_type: {profile_type}")

        axis = str(data["axis"])
        if axis not in {"roll", "pitch", "yaw", "throttle", "composite"}:
            raise ValueError(f"不支持的 axis: {axis}")

        return cls(
            phase=int(data["phase"]),
            input_chain=input_chain,
            axis=axis,
            profile_type=profile_type,
            amplitude=float(data["amplitude"]),
            bias=float(data["bias"]),
            start_after_s=float(data["start_after_s"]),
            duration_s=float(data["duration_s"]),
            sample_rate_hz=float(data["sample_rate_hz"]),
            hover_thrust=float(data["hover_thrust"]),
            hold_s=float(data["hold_s"]),
            timing_required=bool(data["timing_required"]),
            extras=extras,
            source_path=source_path,
            operator=str(data.get("operator", "Codex")),
            warmup_cycles=int(data.get("warmup_cycles", 10)),
            takeoff_thrust=float(data.get("takeoff_thrust", -0.80)),
            takeoff_thrust_max=float(data.get("takeoff_thrust_max", -0.92)),
            takeoff_ramp_s=float(data.get("takeoff_ramp_s", 2.0)),
            takeoff_altitude_m=float(data.get("takeoff_altitude_m", 1.5)),
            takeoff_position_tolerance_m=float(data.get("takeoff_position_tolerance_m", 0.2)),
            takeoff_velocity_tolerance_m=float(data.get("takeoff_velocity_tolerance_m", 0.3)),
            takeoff_settle_s=float(data.get("takeoff_settle_s", 1.5)),
            takeoff_timeout_s=float(data.get("takeoff_timeout_s", 10.0)),
            min_takeoff_clearance_m=float(data.get("min_takeoff_clearance_m", 0.35)),
            min_profile_clearance_m=float(data.get("min_profile_clearance_m", 0.25)),
            altitude_hold_kp=float(data.get("altitude_hold_kp", 0.12)),
            altitude_hold_kd=float(data.get("altitude_hold_kd", 0.08)),
            thrust_z_min=float(data.get("thrust_z_min", -0.95)),
            thrust_z_max=float(data.get("thrust_z_max", -0.35)),
            land_timeout_s=float(data.get("land_timeout_s", 8.0)),
            ready_timeout_s=float(data.get("ready_timeout_s", 20.0)),
        )

    @property
    def period_s(self) -> float:
        if self.sample_rate_hz <= 0.0:
            raise ValueError("sample_rate_hz 必须大于 0")
        return 1.0 / self.sample_rate_hz

    @property
    def active_duration_s(self) -> float:
        return max(0.0, self.start_after_s) + max(0.0, self.duration_s) + max(0.0, self.hold_s)

    @property
    def input_topic(self) -> str:
        if self.input_chain == "attitude":
            return "/fmu/in/vehicle_attitude_setpoint"
        if self.input_chain == "manual":
            return "/fmu/in/manual_control_input"
        raise ValueError(f"不支持的 input_chain: {self.input_chain}")

    @property
    def manual_mode(self) -> str:
        if self.input_chain != "manual":
            return ""
        return str(self.extras.get("manual_mode", "echo"))

    @property
    def run_timeout_s(self) -> float:
        if self.input_chain == "manual" and self.manual_mode != "flight":
            return self.active_duration_s + (self.warmup_cycles * self.period_s) + 5.0
        return (
            self.active_duration_s
            + self.takeoff_timeout_s
            + self.land_timeout_s
            + (self.warmup_cycles * self.period_s)
            + 5.0
        )

    def profile_params(self) -> dict[str, Any]:
        params = {
            "axis": self.axis,
            "amplitude": self.amplitude,
            "bias": self.bias,
            "start_after_s": self.start_after_s,
            "duration_s": self.duration_s,
            "sample_rate_hz": self.sample_rate_hz,
            "hover_thrust": self.hover_thrust,
            "takeoff_thrust": self.takeoff_thrust,
            "takeoff_thrust_max": self.takeoff_thrust_max,
            "takeoff_ramp_s": self.takeoff_ramp_s,
            "takeoff_altitude_m": self.takeoff_altitude_m,
            "takeoff_position_tolerance_m": self.takeoff_position_tolerance_m,
            "takeoff_velocity_tolerance_m": self.takeoff_velocity_tolerance_m,
            "takeoff_settle_s": self.takeoff_settle_s,
            "takeoff_timeout_s": self.takeoff_timeout_s,
            "min_takeoff_clearance_m": self.min_takeoff_clearance_m,
            "min_profile_clearance_m": self.min_profile_clearance_m,
            "altitude_hold_kp": self.altitude_hold_kp,
            "altitude_hold_kd": self.altitude_hold_kd,
            "thrust_z_min": self.thrust_z_min,
            "thrust_z_max": self.thrust_z_max,
            "hold_s": self.hold_s,
            "timing_required": self.timing_required,
        }
        params.update(self.extras)
        return params

    def build_run_id(self, when: datetime | None = None) -> str:
        timestamp = when or datetime.now(timezone.utc).astimezone()
        return f"{timestamp:%Y%m%d_%H%M%S}_{self.input_chain}_{self.profile_type}_{self.axis}"


def load_run_config(path: str | Path) -> RunConfig:
    config_path = Path(path).expanduser().resolve()
    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    if not isinstance(raw, dict):
        raise ValueError("配置文件必须是 YAML object")
    return RunConfig.from_dict(raw, source_path=config_path)


def euler_to_quaternion(roll: float, pitch: float, yaw: float) -> list[float]:
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)

    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy
    return [w, x, y, z]


def quaternion_to_euler(quaternion: list[float] | tuple[float, float, float, float]) -> tuple[float, float, float]:
    if len(quaternion) != 4:
        raise ValueError("Quaternion 长度必须为 4")
    w, x, y, z = [float(value) for value in quaternion]

    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    sinp = 2.0 * (w * y - z * x)
    if abs(sinp) >= 1.0:
        pitch = math.copysign(math.pi / 2.0, sinp)
    else:
        pitch = math.asin(sinp)

    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))
