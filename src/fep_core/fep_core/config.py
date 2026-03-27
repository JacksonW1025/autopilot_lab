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
    study_family: str = "aggressive_input_sensitivity"
    study_layer: str = ""
    study_role: str = ""
    oracle_profile: str = ""
    mode_under_test: str | dict[str, Any] = field(default_factory=dict)
    parameter_group: str = ""
    parameter_set_name: str = "baseline"
    parameter_overrides: dict[str, Any] = field(default_factory=dict)
    controlled_parameters: list[str] | dict[str, Any] = field(default_factory=dict)
    input_contract: dict[str, Any] = field(default_factory=dict)
    output_contract: dict[str, Any] = field(default_factory=dict)
    attribution_boundary: str = ""

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
            "study_family",
            "study_layer",
            "study_role",
            "oracle_profile",
            "mode_under_test",
            "parameter_group",
            "parameter_set_name",
            "parameter_overrides",
            "controlled_parameters",
            "input_contract",
            "output_contract",
            "attribution_boundary",
        }
        extras = {key: value for key, value in data.items() if key not in required and key not in optional_runtime}
        input_chain = str(data["input_chain"])
        if input_chain not in {"attitude", "manual", "rate"}:
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
            study_family=str(data.get("study_family", "aggressive_input_sensitivity")),
            study_layer=str(data.get("study_layer", "")),
            study_role=str(data.get("study_role", "")),
            oracle_profile=str(data.get("oracle_profile", "")),
            mode_under_test=data.get("mode_under_test", {}),
            parameter_group=str(data.get("parameter_group", "")),
            parameter_set_name=str(data.get("parameter_set_name", "baseline")),
            parameter_overrides=dict(data.get("parameter_overrides", {})),
            controlled_parameters=data.get("controlled_parameters", {}),
            input_contract=dict(data.get("input_contract", {})),
            output_contract=dict(data.get("output_contract", {})),
            attribution_boundary=str(data.get("attribution_boundary", "")),
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
        if self.input_chain == "rate":
            return "/fmu/in/vehicle_rates_setpoint"
        raise ValueError(f"不支持的 input_chain: {self.input_chain}")

    @property
    def manual_mode(self) -> str:
        if self.input_chain != "manual":
            return ""
        return str(self.extras.get("manual_mode", "echo"))

    @property
    def resolved_study_layer(self) -> str:
        if self.study_layer:
            return self.study_layer
        if self.input_chain == "manual":
            return "manual_whole_loop"
        if self.input_chain == "attitude":
            return "attitude_explicit"
        return "rate_single_loop"

    @property
    def resolved_study_role(self) -> str:
        if self.study_role:
            return self.study_role
        if self.resolved_study_layer == "rate_single_loop":
            return "conditional"
        return "primary"

    @property
    def resolved_oracle_profile(self) -> str:
        if self.oracle_profile:
            return self.oracle_profile
        if self.resolved_study_layer == "manual_whole_loop":
            return "manual_whole_loop_v1"
        if self.resolved_study_layer == "attitude_explicit":
            return "attitude_tracking_v1"
        return "rate_tracking_v1"

    @property
    def resolved_parameter_group(self) -> str:
        if self.parameter_group:
            return self.parameter_group
        if self.resolved_study_layer == "manual_whole_loop":
            return "manual_whole_loop_nominal"
        if self.axis == "roll":
            return "roll_rate_pid"
        if self.axis == "pitch":
            return "pitch_rate_pid"
        if self.axis == "yaw":
            return "yaw_rate_pid"
        return "nominal_baseline"

    @property
    def resolved_attribution_boundary(self) -> str:
        if self.attribution_boundary:
            return self.attribution_boundary
        if self.resolved_study_layer == "manual_whole_loop":
            return "整机闭环 pilot-input sensitivity；不直接归因到 attitude/rate 单层参数。"
        if self.resolved_study_layer == "attitude_explicit":
            return "attitude 输入层及其以下控制链；不混入 manual mapping。"
        return "rate inner-loop 及其以下执行器约束，用于加强参数归因。"

    def _backend_key(self, backend: str) -> str:
        backend_key = backend.strip().lower()
        if backend_key in {"px4", "px4_ros2"}:
            return "px4"
        if backend_key in {"ardupilot", "ardupilot_mavlink"}:
            return "ardupilot"
        return backend_key

    def _resolve_mapping_value(self, value: Any, backend: str) -> Any:
        if not isinstance(value, dict):
            return value
        backend_key = self._backend_key(backend)
        if backend_key in value:
            return value[backend_key]
        for alias in ("default", "all", "common", "shared"):
            if alias in value:
                return value[alias]
        return value

    def mode_under_test_for_backend(self, backend: str) -> str:
        resolved = self._resolve_mapping_value(self.mode_under_test, backend)
        if isinstance(resolved, str) and resolved.strip():
            return resolved.strip()
        backend_key = self._backend_key(backend)
        if backend_key == "px4":
            if self.resolved_study_layer == "manual_whole_loop":
                return "POSCTL" if self.manual_mode == "flight" else "manual_echo"
            if self.resolved_study_layer == "attitude_explicit":
                return "OFFBOARD_ATTITUDE"
            return "OFFBOARD_RATE"
        if self.resolved_study_layer == "manual_whole_loop":
            return str(self.extras.get("ardupilot_manual_mode", "STABILIZE"))
        if self.resolved_study_layer == "attitude_explicit":
            return "GUIDED_ATTITUDE"
        return "GUIDED_RATE"

    def parameter_overrides_for_backend(self, backend: str) -> dict[str, Any]:
        resolved = self._resolve_mapping_value(self.parameter_overrides, backend)
        return dict(resolved) if isinstance(resolved, dict) else {}

    def controlled_parameters_for_backend(self, backend: str) -> list[str]:
        resolved = self._resolve_mapping_value(self.controlled_parameters, backend)
        if isinstance(resolved, list):
            return [str(item) for item in resolved]
        if isinstance(resolved, tuple):
            return [str(item) for item in resolved]
        if isinstance(resolved, dict):
            return [str(key) for key in resolved]

        backend_key = self._backend_key(backend)
        if backend_key == "px4":
            if self.resolved_study_layer == "manual_whole_loop":
                return [
                    "MC_ROLLRATE_P",
                    "MC_ROLLRATE_I",
                    "MC_ROLLRATE_D",
                    "MC_PITCHRATE_P",
                    "MC_PITCHRATE_I",
                    "MC_PITCHRATE_D",
                    "MPC_POS_MODE",
                    "MPC_ACC_HOR",
                    "MPC_JERK_MAX",
                ]
            return [
                "MC_ROLLRATE_P",
                "MC_ROLLRATE_I",
                "MC_ROLLRATE_D",
                "MC_PITCHRATE_P",
                "MC_PITCHRATE_I",
                "MC_PITCHRATE_D",
            ]
        if self.resolved_study_layer == "manual_whole_loop":
            return [
                "ATC_RAT_RLL_P",
                "ATC_RAT_RLL_I",
                "ATC_RAT_RLL_D",
                "ATC_RAT_PIT_P",
                "ATC_RAT_PIT_I",
                "ATC_RAT_PIT_D",
                "PSC_VELXY_P",
                "LOIT_ACC_MAX",
                "LOIT_SPEED",
            ]
        return [
            "ATC_RAT_RLL_P",
            "ATC_RAT_RLL_I",
            "ATC_RAT_RLL_D",
            "ATC_RAT_PIT_P",
            "ATC_RAT_PIT_I",
            "ATC_RAT_PIT_D",
        ]

    def input_contract_for_backend(self, backend: str) -> dict[str, Any]:
        resolved = self._resolve_mapping_value(self.input_contract, backend)
        if isinstance(resolved, dict) and resolved:
            return dict(resolved)

        if self.resolved_study_layer == "manual_whole_loop":
            return {
                "signals": ["roll", "pitch", "yaw", "throttle"],
                "profile_source": "pilot-equivalent manual profile",
                "notes": "整机飞手等价输入，经飞控内部映射进入闭环。",
            }
        if self.resolved_study_layer == "attitude_explicit":
            return {
                "signals": ["roll_body", "pitch_body", "yaw_body", "thrust_z"],
                "profile_source": "explicit attitude setpoint",
                "notes": "显式姿态设定点输入，不混入 manual stick mapping。",
            }
        return {
            "signals": ["roll_rate", "pitch_rate", "yaw_rate", "thrust_z"],
            "profile_source": "explicit body-rate setpoint",
            "notes": "用于单层 rate inner-loop 分析。",
        }

    def output_contract_for_backend(self, backend: str) -> dict[str, Any]:
        resolved = self._resolve_mapping_value(self.output_contract, backend)
        if isinstance(resolved, dict) and resolved:
            return dict(resolved)

        backend_key = self._backend_key(backend)
        if backend_key == "px4":
            if self.resolved_study_layer == "manual_whole_loop":
                return {
                    "signals": [
                        "vehicle_attitude",
                        "vehicle_local_position",
                        "vehicle_status",
                        "vehicle_control_mode",
                        "control_allocator_status",
                        "actuator_motors",
                    ]
                }
            if self.resolved_study_layer == "attitude_explicit":
                return {
                    "signals": [
                        "vehicle_attitude",
                        "vehicle_attitude_setpoint",
                        "vehicle_rates_setpoint",
                        "vehicle_angular_velocity",
                        "rate_ctrl_status",
                        "control_allocator_status",
                        "actuator_motors",
                    ]
                }
            return {
                "signals": [
                    "vehicle_angular_velocity",
                    "vehicle_rates_setpoint",
                    "rate_ctrl_status",
                    "control_allocator_status",
                    "actuator_motors",
                ]
            }
        if self.resolved_study_layer == "manual_whole_loop":
            return {"signals": ["ATT", "RATE", "CTUN", "MOTB", "RCOU", "LOCAL_POSITION_NED", "HEARTBEAT"]}
        if self.resolved_study_layer == "attitude_explicit":
            return {"signals": ["ATT", "RATE", "CTUN", "MOTB", "RCOU", "PIDR", "PIDP", "PIDY"]}
        return {"signals": ["RATE", "MOTB", "RCOU", "PIDR", "PIDP", "PIDY"]}

    def rate_layer_trigger_conditions(self) -> list[str]:
        return [
            "姿态层已经观察到显著差异，但这些差异无法由输入映射、altitude hold 或 manual shaping 解释。",
            "当前研究因素本身属于 rate 相关参数，例如 MC_ROLLRATE_*、MC_PITCHRATE_*、ATC_RAT_RLL_*、ATC_RAT_PIT_*。",
            "论文归因需要更强证据，需要明确拆开 attitude outer loop 与 rate inner loop。",
        ]

    def rate_layer_recommended_reasons(self) -> list[str]:
        reasons: list[str] = []
        if self.resolved_study_layer == "rate_single_loop":
            reasons.append("study_layer_is_rate_single_loop")
        if "rate" in self.resolved_parameter_group:
            reasons.append("parameter_group_is_rate_related")
        if bool(self.extras.get("require_rate_layer_evidence", False)):
            reasons.append("config_requires_rate_layer_evidence")
        return reasons

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

    def study_metadata(self, backend: str) -> dict[str, Any]:
        return {
            "study_family": self.study_family,
            "study_layer": self.resolved_study_layer,
            "study_role": self.resolved_study_role,
            "oracle_profile": self.resolved_oracle_profile,
            "mode_under_test": self.mode_under_test_for_backend(backend),
            "parameter_group": self.resolved_parameter_group,
            "parameter_set_name": self.parameter_set_name,
            "parameter_overrides": self.parameter_overrides_for_backend(backend),
            "controlled_parameters": self.controlled_parameters_for_backend(backend),
            "input_contract": self.input_contract_for_backend(backend),
            "output_contract": self.output_contract_for_backend(backend),
            "attribution_boundary": self.resolved_attribution_boundary,
            "rate_layer_trigger_conditions": self.rate_layer_trigger_conditions(),
            "rate_layer_recommended_reasons": self.rate_layer_recommended_reasons(),
        }

    def build_run_id(self, when: datetime | None = None) -> str:
        timestamp = when or datetime.now(timezone.utc).astimezone()
        layer_token = {
            "manual_whole_loop": "manual",
            "attitude_explicit": "attitude",
            "rate_single_loop": "rate",
        }.get(self.resolved_study_layer, self.input_chain)
        return f"{timestamp:%Y%m%d_%H%M%S}_{layer_token}_{self.profile_type}_{self.axis}"


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
