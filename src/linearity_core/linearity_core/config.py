from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


SUPPORTED_BACKENDS = {"synthetic", "px4", "ardupilot"}
SUPPORTED_INPUT_TYPES = {"manual", "attitude", "rate"}
SUPPORTED_PROFILE_TYPES = {"baseline", "step", "pulse", "sweep", "random", "broad"}
SUPPORTED_AXIS = {"roll", "pitch", "yaw", "throttle", "composite"}
SUPPORTED_POOLING_MODES = {"pooled", "stratified", "compare_both"}
SUPPORTED_PREDICTION_UNITS = {"steps", "seconds"}
SUPPORTED_OUTPUT_SEMANTICS = {"future_state", "delta_state", "current_raw_state", "raw_state", "delayed_state", "horizon_summary"}
DEFAULT_MODELS = ["ols_affine", "ridge_affine", "lasso_affine", "thresholded_ols_affine"]
DEFAULT_X_SCHEMAS = [
    "commands_only",
    "commands_plus_state",
    "commands_plus_state_history",
    "commands_plus_controller_params",
    "commands_plus_state_plus_params",
    "pooled_backend_mode_augmented",
    "full_augmented",
    "feature_mapped_linear",
]
DEFAULT_Y_SCHEMAS = [
    "next_raw_state",
    "delta_state",
    "selected_state_subset",
    "future_state_horizon",
    "actuator_response",
    "tracking_error_response",
    "window_summary_response",
    "stability_proxy_response",
]


def _as_str_list(value: Any) -> list[str]:
    if value in ("", None):
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value]
    raise ValueError(f"无法解析为字符串列表: {value!r}")


def _as_dict(value: Any) -> dict[str, Any]:
    if value in ("", None):
        return {}
    if isinstance(value, dict):
        return dict(value)
    raise ValueError(f"无法解析为字典: {value!r}")


def _resolve_backend_mapping(value: Any, backend: str) -> Any:
    if not isinstance(value, dict):
        return value
    backend_key = backend.strip().lower()
    aliases = {
        "px4_ros2": "px4",
        "ardupilot_mavlink": "ardupilot",
    }
    backend_key = aliases.get(backend_key, backend_key)
    if backend_key in value:
        return value[backend_key]
    for alias in ("default", "all", "shared", "common"):
        if alias in value:
            return value[alias]
    return value


@dataclass(slots=True)
class StudyConfig:
    study_name: str
    backend: str
    flight_mode: str | dict[str, Any]
    scenario: str
    config_profile: str
    seed: int
    repeat_count: int
    sampling_rate_hz: float
    x_schema: str
    x_include_groups: list[str] = field(default_factory=list)
    x_exclude_groups: list[str] = field(default_factory=list)
    y_schema: str = "next_raw_state"
    y_include_groups: list[str] = field(default_factory=list)
    y_exclude_groups: list[str] = field(default_factory=list)
    feature_map: str | dict[str, Any] = "identity"
    run_level_covariates_as_inputs: list[str] | bool = field(default_factory=list)
    stratify_by: list[str] = field(default_factory=list)
    pooling_mode: str = "pooled"
    output_semantics: str = "future_state"
    history_length: int = 0
    prediction_horizon: int = 1
    prediction_horizon_unit: str = "steps"
    parameter_sweep: dict[str, Any] = field(default_factory=dict)
    internal_signals_enabled: bool = False
    perturbation_strategy: str = "single_variable_sweep"
    ablation_plan: str | dict[str, Any] | None = None
    model: str | list[str] = field(default_factory=lambda: list(DEFAULT_MODELS))
    sparsity: dict[str, Any] = field(default_factory=dict)
    reporting: dict[str, Any] = field(default_factory=dict)
    input_type: str = "manual"
    axis: str = "roll"
    profile_type: str = "step"
    amplitude: float = 0.2
    bias: float = 0.0
    start_after_s: float = 1.0
    duration_s: float = 2.0
    hold_s: float = 2.0
    hover_thrust: float = -0.69
    timing_required: bool = False
    operator: str = "Codex"
    warmup_cycles: int = 10
    manual_mode: str = "flight"
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
    parameter_overrides: dict[str, Any] = field(default_factory=dict)
    controlled_parameters: list[str] | dict[str, Any] = field(default_factory=list)
    synthetic: dict[str, Any] = field(default_factory=dict)
    extras: dict[str, Any] = field(default_factory=dict)
    source_path: Path | None = None
    repeat_index: int = 1

    @classmethod
    def from_dict(cls, data: dict[str, Any], source_path: Path | None = None) -> "StudyConfig":
        required = {
            "study_name",
            "backend",
            "flight_mode",
            "scenario",
            "config_profile",
            "seed",
            "repeat_count",
            "sampling_rate_hz",
            "x_schema",
        }
        missing = sorted(required - data.keys())
        if missing:
            raise ValueError(f"配置缺少字段: {', '.join(missing)}")

        optional_keys = {
            "x_include_groups",
            "x_exclude_groups",
            "y_schema",
            "y_include_groups",
            "y_exclude_groups",
            "feature_map",
            "run_level_covariates_as_inputs",
            "stratify_by",
            "pooling_mode",
            "output_semantics",
            "history_length",
            "prediction_horizon",
            "prediction_horizon_unit",
            "parameter_sweep",
            "internal_signals_enabled",
            "perturbation_strategy",
            "ablation_plan",
            "model",
            "sparsity",
            "reporting",
            "input_type",
            "axis",
            "profile_type",
            "amplitude",
            "bias",
            "start_after_s",
            "duration_s",
            "hold_s",
            "hover_thrust",
            "timing_required",
            "operator",
            "warmup_cycles",
            "manual_mode",
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
            "parameter_overrides",
            "controlled_parameters",
            "synthetic",
            "extras",
        }
        extras = {key: value for key, value in data.items() if key not in required and key not in optional_keys}

        backend = str(data["backend"]).strip().lower()
        if backend not in SUPPORTED_BACKENDS:
            raise ValueError(f"不支持的 backend: {backend}")

        input_type = str(data.get("input_type", "manual")).strip().lower()
        if input_type not in SUPPORTED_INPUT_TYPES:
            raise ValueError(f"不支持的 input_type: {input_type}")

        axis = str(data.get("axis", "roll")).strip().lower()
        if axis not in SUPPORTED_AXIS:
            raise ValueError(f"不支持的 axis: {axis}")

        profile_type = str(data.get("profile_type", "step")).strip().lower()
        if profile_type not in SUPPORTED_PROFILE_TYPES:
            raise ValueError(f"不支持的 profile_type: {profile_type}")

        pooling_mode = str(data.get("pooling_mode", "pooled")).strip().lower()
        if pooling_mode not in SUPPORTED_POOLING_MODES:
            raise ValueError(f"不支持的 pooling_mode: {pooling_mode}")

        prediction_horizon_unit = str(data.get("prediction_horizon_unit", "steps")).strip().lower()
        if prediction_horizon_unit not in SUPPORTED_PREDICTION_UNITS:
            raise ValueError(f"不支持的 prediction_horizon_unit: {prediction_horizon_unit}")

        output_semantics = str(data.get("output_semantics", "future_state")).strip().lower()
        if output_semantics not in SUPPORTED_OUTPUT_SEMANTICS:
            raise ValueError(f"不支持的 output_semantics: {output_semantics}")

        model = data.get("model", list(DEFAULT_MODELS))
        normalized_model: str | list[str]
        if isinstance(model, str):
            normalized_model = model
        elif isinstance(model, (list, tuple)):
            normalized_model = [str(item) for item in model]
        else:
            raise ValueError(f"不支持的 model 配置: {model!r}")

        run_level_inputs = data.get("run_level_covariates_as_inputs", [])
        if isinstance(run_level_inputs, bool):
            normalized_run_level_inputs: list[str] | bool = run_level_inputs
        else:
            normalized_run_level_inputs = _as_str_list(run_level_inputs)

        return cls(
            study_name=str(data["study_name"]),
            backend=backend,
            flight_mode=data["flight_mode"],
            scenario=str(data["scenario"]),
            config_profile=str(data["config_profile"]),
            seed=int(data["seed"]),
            repeat_count=max(1, int(data["repeat_count"])),
            sampling_rate_hz=float(data["sampling_rate_hz"]),
            x_schema=str(data["x_schema"]),
            x_include_groups=_as_str_list(data.get("x_include_groups", [])),
            x_exclude_groups=_as_str_list(data.get("x_exclude_groups", [])),
            y_schema=str(data.get("y_schema", "next_raw_state")),
            y_include_groups=_as_str_list(data.get("y_include_groups", [])),
            y_exclude_groups=_as_str_list(data.get("y_exclude_groups", [])),
            feature_map=data.get("feature_map", "identity"),
            run_level_covariates_as_inputs=normalized_run_level_inputs,
            stratify_by=_as_str_list(data.get("stratify_by", [])),
            pooling_mode=pooling_mode,
            output_semantics=output_semantics,
            history_length=max(0, int(data.get("history_length", 0))),
            prediction_horizon=max(1, int(data.get("prediction_horizon", 1))),
            prediction_horizon_unit=prediction_horizon_unit,
            parameter_sweep=_as_dict(data.get("parameter_sweep", {})),
            internal_signals_enabled=bool(data.get("internal_signals_enabled", False)),
            perturbation_strategy=str(data.get("perturbation_strategy", "single_variable_sweep")),
            ablation_plan=data.get("ablation_plan"),
            model=normalized_model,
            sparsity=_as_dict(data.get("sparsity", {})),
            reporting=_as_dict(data.get("reporting", {})),
            input_type=input_type,
            axis=axis,
            profile_type=profile_type,
            amplitude=float(data.get("amplitude", 0.2)),
            bias=float(data.get("bias", 0.0)),
            start_after_s=float(data.get("start_after_s", 1.0)),
            duration_s=float(data.get("duration_s", 2.0)),
            hold_s=float(data.get("hold_s", 2.0)),
            hover_thrust=float(data.get("hover_thrust", -0.69)),
            timing_required=bool(data.get("timing_required", False)),
            operator=str(data.get("operator", "Codex")),
            warmup_cycles=max(0, int(data.get("warmup_cycles", 10))),
            manual_mode=str(data.get("manual_mode", "flight")),
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
            parameter_overrides=_as_dict(data.get("parameter_overrides", {})),
            controlled_parameters=data.get("controlled_parameters", []),
            synthetic=_as_dict(data.get("synthetic", {})),
            extras={**_as_dict(data.get("extras", {})), **extras},
            source_path=source_path,
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if self.source_path is not None:
            payload["source_path"] = str(self.source_path)
        return payload

    @property
    def period_s(self) -> float:
        if self.sampling_rate_hz <= 0.0:
            raise ValueError("sampling_rate_hz 必须大于 0")
        return 1.0 / self.sampling_rate_hz

    @property
    def active_duration_s(self) -> float:
        return max(0.0, self.start_after_s) + max(0.0, self.duration_s) + max(0.0, self.hold_s)

    @property
    def run_timeout_s(self) -> float:
        base = self.active_duration_s + max(self.land_timeout_s, 0.0) + max(self.takeoff_timeout_s, 0.0)
        return base + (self.warmup_cycles * self.period_s) + 5.0

    @property
    def input_chain(self) -> str:
        return self.input_type

    def mode_under_test_for_backend(self, backend: str) -> str:
        resolved = _resolve_backend_mapping(self.flight_mode, backend)
        if isinstance(resolved, str) and resolved.strip():
            return resolved.strip()
        backend_key = backend.strip().lower()
        if backend_key == "px4":
            if self.input_type == "manual":
                return "POSCTL" if self.manual_mode == "flight" else "MANUAL"
            if self.input_type == "attitude":
                return "OFFBOARD_ATTITUDE"
            return "OFFBOARD_RATE"
        if self.input_type == "manual":
            return "STABILIZE"
        if self.input_type == "attitude":
            return "GUIDED_ATTITUDE"
        return "GUIDED_NOGPS"

    def parameter_overrides_for_backend(self, backend: str) -> dict[str, Any]:
        resolved = _resolve_backend_mapping(self.parameter_overrides, backend)
        return dict(resolved) if isinstance(resolved, dict) else {}

    def controlled_parameters_for_backend(self, backend: str) -> list[str]:
        resolved = _resolve_backend_mapping(self.controlled_parameters, backend)
        if isinstance(resolved, (list, tuple, set)):
            return [str(item) for item in resolved]
        if isinstance(resolved, dict):
            return [str(key) for key in resolved]
        if isinstance(resolved, str) and resolved.strip():
            return [resolved.strip()]
        return [str(name) for name in self.parameter_overrides_for_backend(backend)]

    def resolved_models(self) -> list[str]:
        if isinstance(self.model, str):
            return [self.model]
        return [str(item) for item in self.model]

    def build_run_id(self, when: datetime | None = None, repeat_index: int | None = None) -> str:
        timestamp = when or datetime.now(timezone.utc).astimezone()
        backend_token = self.backend
        repeat_token = repeat_index if repeat_index is not None else self.repeat_index
        return (
            f"{timestamp:%Y%m%d_%H%M%S}_{backend_token}_{self.input_type}_{self.profile_type}_{self.axis}"
            f"_r{max(1, int(repeat_token))}"
        )

    def with_repeat_index(self, repeat_index: int) -> "StudyConfig":
        clone = StudyConfig.from_dict(self.to_dict(), source_path=self.source_path)
        clone.repeat_index = repeat_index
        return clone


RunConfig = StudyConfig


@dataclass(slots=True)
class AblationPlan:
    plan_name: str
    run_dirs: list[str] = field(default_factory=list)
    x_schemas: list[str] = field(default_factory=list)
    y_schemas: list[str] = field(default_factory=list)
    models: list[str] = field(default_factory=lambda: list(DEFAULT_MODELS))
    pooling_modes: list[str] = field(default_factory=lambda: ["pooled"])
    stratify_by: list[str] = field(default_factory=list)
    output_study_name: str = ""
    reporting: dict[str, Any] = field(default_factory=dict)
    source_path: Path | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any], source_path: Path | None = None) -> "AblationPlan":
        if "plan_name" not in data:
            raise ValueError("ablation plan 缺少字段: plan_name")
        return cls(
            plan_name=str(data["plan_name"]),
            run_dirs=_as_str_list(data.get("run_dirs", [])),
            x_schemas=_as_str_list(data.get("x_schemas", DEFAULT_X_SCHEMAS)),
            y_schemas=_as_str_list(data.get("y_schemas", DEFAULT_Y_SCHEMAS)),
            models=_as_str_list(data.get("models", DEFAULT_MODELS)),
            pooling_modes=_as_str_list(data.get("pooling_modes", ["pooled"])),
            stratify_by=_as_str_list(data.get("stratify_by", [])),
            output_study_name=str(data.get("output_study_name", "")),
            reporting=_as_dict(data.get("reporting", {})),
            source_path=source_path,
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if self.source_path is not None:
            payload["source_path"] = str(self.source_path)
        return payload


def load_study_config(path: str | Path) -> StudyConfig:
    config_path = Path(path).expanduser().resolve()
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("配置文件必须是 YAML object")
    return StudyConfig.from_dict(raw, source_path=config_path)


def load_run_config(path: str | Path) -> StudyConfig:
    return load_study_config(path)


def load_ablation_plan(path: str | Path) -> AblationPlan:
    plan_path = Path(path).expanduser().resolve()
    raw = yaml.safe_load(plan_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("ablation plan 必须是 YAML object")
    return AblationPlan.from_dict(raw, source_path=plan_path)


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
