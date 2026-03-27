from __future__ import annotations

import math
from dataclasses import dataclass

from .config import RunConfig, clamp


@dataclass(slots=True)
class CommandSample:
    publish_time_ns: int
    elapsed_s: float
    profile_value: float
    roll_body: float
    pitch_body: float
    yaw_body: float
    thrust_z: float
    phase: str

    def to_row(self) -> dict[str, float | int | str]:
        return {
            "publish_time_ns": self.publish_time_ns,
            "elapsed_s": round(self.elapsed_s, 6),
            "profile_value": self.profile_value,
            "roll_body": self.roll_body,
            "pitch_body": self.pitch_body,
            "yaw_body": self.yaw_body,
            "thrust_z": self.thrust_z,
            "phase": self.phase,
        }


class ProfileGenerator:
    def __init__(self, config: RunConfig) -> None:
        self._config = config

    @property
    def total_duration_s(self) -> float:
        return self._config.active_duration_s

    def profile_value_at(self, elapsed_s: float) -> tuple[float, str]:
        config = self._config

        if config.profile_type == "baseline":
            return config.bias, "baseline_hold"

        if elapsed_s < config.start_after_s:
            return config.bias, "stabilize"

        active_elapsed = elapsed_s - config.start_after_s
        if config.profile_type == "step":
            if active_elapsed < config.duration_s:
                return config.bias + config.amplitude, "step_active"
            return config.bias, "recover"

        if config.profile_type == "pulse":
            pulse_width_s = float(config.extras.get("pulse_width_s", min(config.duration_s, 0.2)))
            if active_elapsed < pulse_width_s:
                return config.bias + config.amplitude, "pulse_active"
            return config.bias, "recover"

        if config.profile_type == "sweep":
            if active_elapsed >= config.duration_s:
                return config.bias, "recover"
            sweep_start_hz = float(config.extras.get("sweep_start_hz", 0.2))
            sweep_end_hz = float(config.extras.get("sweep_end_hz", 2.0))
            sweep_span = sweep_end_hz - sweep_start_hz
            phase = 2.0 * math.pi * (
                sweep_start_hz * active_elapsed
                + 0.5 * sweep_span * (active_elapsed**2) / max(config.duration_s, 1e-6)
            )
            return config.bias + config.amplitude * math.sin(phase), "sweep_active"

        raise ValueError(f"不支持的 profile_type: {config.profile_type}")

    def attitude_targets_at(self, elapsed_s: float) -> tuple[float, float, float, float, float, str]:
        config = self._config
        profile_value, phase = self.profile_value_at(elapsed_s)

        roll_body = 0.0
        pitch_body = 0.0
        yaw_body = 0.0
        thrust_z = config.hover_thrust

        if config.axis == "roll":
            roll_body = profile_value
        elif config.axis == "pitch":
            pitch_body = profile_value
        elif config.axis == "yaw":
            yaw_body = profile_value
        elif config.axis == "throttle":
            thrust_z = clamp(config.hover_thrust - profile_value, -1.0, 1.0)
        elif config.axis == "composite":
            roll_body = clamp(profile_value * float(config.extras.get("roll_amplitude", 0.0)), -1.0, 1.0)
            pitch_body = clamp(profile_value * float(config.extras.get("pitch_amplitude", 0.0)), -1.0, 1.0)
            yaw_body = clamp(profile_value * float(config.extras.get("yaw_amplitude", 0.0)), -1.0, 1.0)
            thrust_delta = profile_value * float(config.extras.get("thrust_delta", 0.0))
            thrust_z = clamp(config.hover_thrust - thrust_delta, -1.0, 1.0)
        else:
            raise ValueError(f"不支持的 axis: {config.axis}")

        return profile_value, roll_body, pitch_body, yaw_body, thrust_z, phase

    def manual_targets_at(self, elapsed_s: float) -> tuple[float, float, float, float, float, str]:
        config = self._config
        profile_value, phase = self.profile_value_at(elapsed_s)

        roll = 0.0
        pitch = 0.0
        yaw = 0.0
        throttle = 0.0

        if config.axis == "roll":
            roll = clamp(profile_value, -1.0, 1.0)
        elif config.axis == "pitch":
            pitch = clamp(profile_value, -1.0, 1.0)
        elif config.axis == "yaw":
            yaw = clamp(profile_value, -1.0, 1.0)
        elif config.axis == "throttle":
            throttle = clamp(profile_value, -1.0, 1.0)
        elif config.axis == "composite":
            roll = clamp(profile_value * float(config.extras.get("roll_amplitude", 0.0)), -1.0, 1.0)
            pitch = clamp(profile_value * float(config.extras.get("pitch_amplitude", 0.0)), -1.0, 1.0)
            yaw = clamp(profile_value * float(config.extras.get("yaw_amplitude", 0.0)), -1.0, 1.0)
            throttle = clamp(profile_value * float(config.extras.get("throttle", 0.0)), -1.0, 1.0)
        else:
            raise ValueError(f"不支持的 axis: {config.axis}")

        return profile_value, roll, pitch, yaw, throttle, phase
