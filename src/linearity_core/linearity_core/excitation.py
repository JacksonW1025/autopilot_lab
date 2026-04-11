from __future__ import annotations

import math
import random
from dataclasses import dataclass

from .config import StudyConfig, clamp


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
            "profile_value": round(self.profile_value, 6),
            "roll_body": round(self.roll_body, 6),
            "pitch_body": round(self.pitch_body, 6),
            "yaw_body": round(self.yaw_body, 6),
            "thrust_z": round(self.thrust_z, 6),
            "command_roll": round(self.roll_body, 6),
            "command_pitch": round(self.pitch_body, 6),
            "command_yaw": round(self.yaw_body, 6),
            "command_throttle": round(self.thrust_z, 6),
            "phase": self.phase,
        }


class ExcitationGenerator:
    def __init__(self, config: StudyConfig) -> None:
        self._config = config

    @property
    def total_duration_s(self) -> float:
        return self._config.active_duration_s

    def _random_interval_value(self, interval_index: int) -> float:
        seed = (self._config.seed * 1315423911) ^ interval_index
        generator = random.Random(seed)
        return generator.uniform(-self._config.amplitude, self._config.amplitude)

    def _multi_broad_axis_signal(self, axis: str, active_elapsed_s: float) -> float:
        config = self._config
        frequency_map = config.extras.get("multi_broad_frequencies_hz", {}) or {}
        phase_map = config.extras.get("multi_broad_phases_rad", {}) or {}
        axis_key = str(axis).strip().lower()
        frequencies = frequency_map.get(axis_key, config.extras.get("broad_frequencies_hz", [0.2, 0.7, 1.3]))
        phases = phase_map.get(axis_key, [])
        value = 0.0
        frequencies = [float(item) for item in frequencies] if frequencies else [0.2, 0.7, 1.3]
        for index, freq in enumerate(frequencies):
            phase = float(phases[index]) if index < len(phases) else 0.25 * (index + 1)
            value += math.sin(2.0 * math.pi * freq * active_elapsed_s + phase)
        value /= max(len(frequencies), 1)
        return config.amplitude * value

    def _multi_broad_values(self, elapsed_s: float) -> tuple[dict[str, float], float, str]:
        config = self._config
        zero_map = {"roll": 0.0, "pitch": 0.0, "yaw": 0.0, "throttle": 0.0}
        if elapsed_s < config.start_after_s:
            return zero_map, 0.0, "stabilize"
        active_elapsed = elapsed_s - config.start_after_s
        if active_elapsed >= config.duration_s:
            return zero_map, 0.0, "recover"
        values = {
            axis: self._multi_broad_axis_signal(axis, active_elapsed)
            for axis in zero_map
        }
        aggregate = float(sum(values.values()) / max(len(values), 1))
        return values, aggregate, "multi_broad_active"

    def _multi_broad_axis_bias(self, axis: str) -> float:
        axis_bias = self._config.extras.get("multi_broad_axis_bias", {}) or {}
        return float(axis_bias.get(str(axis).strip().lower(), 0.0))

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

        if config.profile_type == "pulse_train":
            pulse_width_s = max(1e-6, float(config.extras.get("pulse_width_s", min(config.duration_s, 0.2))))
            pulse_gap_s = max(0.0, float(config.extras.get("pulse_gap_s", pulse_width_s)))
            pulse_count = max(1, int(config.extras.get("pulse_count", 3)))
            cycle_s = pulse_width_s + pulse_gap_s
            train_duration_s = pulse_count * pulse_width_s + max(0, pulse_count - 1) * pulse_gap_s
            if active_elapsed >= min(config.duration_s, train_duration_s):
                return config.bias, "recover"
            if cycle_s <= 0.0:
                return config.bias + config.amplitude, "pulse_active"
            cycle_index = int(active_elapsed / cycle_s)
            if cycle_index >= pulse_count:
                return config.bias, "recover"
            pulse_elapsed_s = active_elapsed - (cycle_index * cycle_s)
            if pulse_elapsed_s < pulse_width_s:
                return config.bias + config.amplitude, "pulse_active"
            return config.bias, "pulse_gap"

        if config.profile_type == "alternating_pulse_train":
            pulse_width_s = max(1e-6, float(config.extras.get("pulse_width_s", min(config.duration_s, 0.2))))
            pulse_gap_s = max(0.0, float(config.extras.get("pulse_gap_s", pulse_width_s)))
            pulse_count = max(1, int(config.extras.get("pulse_count", 3)))
            cycle_s = pulse_width_s + pulse_gap_s
            train_duration_s = pulse_count * pulse_width_s + max(0, pulse_count - 1) * pulse_gap_s
            if active_elapsed >= min(config.duration_s, train_duration_s):
                return config.bias, "recover"
            if cycle_s <= 0.0:
                return config.bias + config.amplitude, "alternating_pulse_active_pos"
            cycle_index = int(active_elapsed / cycle_s)
            if cycle_index >= pulse_count:
                return config.bias, "recover"
            pulse_elapsed_s = active_elapsed - (cycle_index * cycle_s)
            if pulse_elapsed_s < pulse_width_s:
                sign = 1.0 if (cycle_index % 2 == 0) else -1.0
                phase = "alternating_pulse_active_pos" if sign > 0 else "alternating_pulse_active_neg"
                return config.bias + (sign * config.amplitude), phase
            return config.bias, "pulse_gap"

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

        if config.profile_type == "random":
            if active_elapsed >= config.duration_s:
                return config.bias, "recover"
            interval_s = float(config.extras.get("random_interval_s", 0.25))
            interval_index = int(active_elapsed / max(interval_s, 1e-6))
            return config.bias + self._random_interval_value(interval_index), "random_active"

        if config.profile_type == "broad":
            if active_elapsed >= config.duration_s:
                return config.bias, "recover"
            freqs = config.extras.get("broad_frequencies_hz", [0.2, 0.7, 1.3])
            value = 0.0
            for index, freq in enumerate(freqs, start=1):
                value += math.sin(2.0 * math.pi * float(freq) * active_elapsed + 0.25 * index)
            value /= max(len(freqs), 1)
            return config.bias + config.amplitude * value, "broad_active"

        if config.profile_type == "multi_broad":
            if config.axis == "composite":
                _values, aggregate, phase = self._multi_broad_values(elapsed_s)
                return aggregate, phase
            if elapsed_s < config.start_after_s:
                return config.bias, "stabilize"
            active_elapsed = elapsed_s - config.start_after_s
            if active_elapsed >= config.duration_s:
                return config.bias, "recover"
            value = self._multi_broad_axis_signal(config.axis, active_elapsed) + self._multi_broad_axis_bias(config.axis)
            return value, "multi_broad_active"

        raise ValueError(f"不支持的 profile_type: {config.profile_type}")

    def attitude_targets_at(self, elapsed_s: float) -> tuple[float, float, float, float, float, str]:
        config = self._config
        if config.profile_type == "multi_broad" and config.axis == "composite":
            values, aggregate, phase = self._multi_broad_values(elapsed_s)
            roll_body = clamp(
                values["roll"] * float(config.extras.get("roll_amplitude", 1.0)) + self._multi_broad_axis_bias("roll"),
                -1.0,
                1.0,
            )
            pitch_body = clamp(
                values["pitch"] * float(config.extras.get("pitch_amplitude", 0.7)) + self._multi_broad_axis_bias("pitch"),
                -1.0,
                1.0,
            )
            yaw_body = clamp(
                values["yaw"] * float(config.extras.get("yaw_amplitude", 0.5)) + self._multi_broad_axis_bias("yaw"),
                -1.0,
                1.0,
            )
            thrust_delta = (
                values["throttle"] * float(config.extras.get("thrust_delta", 0.3))
                + self._multi_broad_axis_bias("throttle")
            )
            thrust_z = clamp(config.hover_thrust - thrust_delta, -1.0, 1.0)
            return aggregate, roll_body, pitch_body, yaw_body, thrust_z, phase

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
            roll_body = clamp(profile_value * float(config.extras.get("roll_amplitude", 1.0)), -1.0, 1.0)
            pitch_body = clamp(profile_value * float(config.extras.get("pitch_amplitude", 0.7)), -1.0, 1.0)
            yaw_body = clamp(profile_value * float(config.extras.get("yaw_amplitude", 0.5)), -1.0, 1.0)
            thrust_delta = profile_value * float(config.extras.get("thrust_delta", 0.3))
            thrust_z = clamp(config.hover_thrust - thrust_delta, -1.0, 1.0)
        return profile_value, roll_body, pitch_body, yaw_body, thrust_z, phase

    def manual_targets_at(self, elapsed_s: float) -> tuple[float, float, float, float, float, str]:
        config = self._config
        if config.profile_type == "multi_broad" and config.axis == "composite":
            values, aggregate, phase = self._multi_broad_values(elapsed_s)
            roll = clamp(
                values["roll"] * float(config.extras.get("roll_amplitude", 1.0)) + self._multi_broad_axis_bias("roll"),
                -1.0,
                1.0,
            )
            pitch = clamp(
                values["pitch"] * float(config.extras.get("pitch_amplitude", 0.7)) + self._multi_broad_axis_bias("pitch"),
                -1.0,
                1.0,
            )
            yaw = clamp(
                values["yaw"] * float(config.extras.get("yaw_amplitude", 0.5)) + self._multi_broad_axis_bias("yaw"),
                -1.0,
                1.0,
            )
            throttle = clamp(
                values["throttle"] * float(config.extras.get("throttle_amplitude", 0.4)) + self._multi_broad_axis_bias("throttle"),
                -1.0,
                1.0,
            )
            return aggregate, roll, pitch, yaw, throttle, phase

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
            roll = clamp(profile_value * float(config.extras.get("roll_amplitude", 1.0)), -1.0, 1.0)
            pitch = clamp(profile_value * float(config.extras.get("pitch_amplitude", 0.7)), -1.0, 1.0)
            yaw = clamp(profile_value * float(config.extras.get("yaw_amplitude", 0.5)), -1.0, 1.0)
            throttle = clamp(profile_value * float(config.extras.get("throttle_amplitude", 0.4)), -1.0, 1.0)
        return profile_value, roll, pitch, yaw, throttle, phase

    def rate_targets_at(self, elapsed_s: float) -> tuple[float, float, float, float, float, str]:
        config = self._config
        if config.profile_type == "multi_broad" and config.axis == "composite":
            values, aggregate, phase = self._multi_broad_values(elapsed_s)
            roll_rate = clamp(
                values["roll"] * float(config.extras.get("roll_rate_amplitude", 1.5)) + self._multi_broad_axis_bias("roll"),
                -4.0,
                4.0,
            )
            pitch_rate = clamp(
                values["pitch"] * float(config.extras.get("pitch_rate_amplitude", 1.2)) + self._multi_broad_axis_bias("pitch"),
                -4.0,
                4.0,
            )
            yaw_rate = clamp(
                values["yaw"] * float(config.extras.get("yaw_rate_amplitude", 0.8)) + self._multi_broad_axis_bias("yaw"),
                -4.0,
                4.0,
            )
            thrust_delta = (
                values["throttle"] * float(config.extras.get("thrust_delta", 0.3))
                + self._multi_broad_axis_bias("throttle")
            )
            thrust_z = clamp(config.hover_thrust - thrust_delta, -1.0, 1.0)
            return aggregate, roll_rate, pitch_rate, yaw_rate, thrust_z, phase

        profile_value, phase = self.profile_value_at(elapsed_s)
        roll_rate = 0.0
        pitch_rate = 0.0
        yaw_rate = 0.0
        thrust_z = config.hover_thrust
        if config.axis == "roll":
            roll_rate = profile_value
        elif config.axis == "pitch":
            pitch_rate = profile_value
        elif config.axis == "yaw":
            yaw_rate = profile_value
        elif config.axis == "throttle":
            thrust_z = clamp(config.hover_thrust - profile_value, -1.0, 1.0)
        elif config.axis == "composite":
            roll_rate = clamp(profile_value * float(config.extras.get("roll_rate_amplitude", 1.5)), -4.0, 4.0)
            pitch_rate = clamp(profile_value * float(config.extras.get("pitch_rate_amplitude", 1.2)), -4.0, 4.0)
            yaw_rate = clamp(profile_value * float(config.extras.get("yaw_rate_amplitude", 0.8)), -4.0, 4.0)
            thrust_delta = profile_value * float(config.extras.get("thrust_delta", 0.3))
            thrust_z = clamp(config.hover_thrust - thrust_delta, -1.0, 1.0)
        return profile_value, roll_rate, pitch_rate, yaw_rate, thrust_z, phase
