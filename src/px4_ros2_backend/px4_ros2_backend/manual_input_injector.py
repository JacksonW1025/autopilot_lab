from __future__ import annotations

import argparse
import math
import time
from collections import deque
from pathlib import Path
from threading import Lock
from typing import Any

import numpy as np
import rclpy
from px4_msgs.msg import (
    ActuatorMotors,
    ControlAllocatorStatus,
    ManualControlSetpoint,
    OffboardControlMode,
    TrajectorySetpoint,
    VehicleAngularVelocity,
    VehicleAttitude,
    VehicleAttitudeSetpoint,
    VehicleCommand,
    VehicleControlMode,
    VehicleLocalPosition,
    VehicleRatesSetpoint,
    VehicleStatus,
)
from rclpy.clock import Clock, ClockType
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node

from linearity_core.attack_eval import (
    apply_attack_to_command,
    build_attack_controller_from_config,
    make_attack_trace_row,
    summarize_attack_trace,
)
from linearity_core.attack_runtime import AttackContext, AttackDelta

from .common import RunConfig, clamp, load_run_config, px4_qos_profile, quaternion_to_euler
from .profiles import CommandSample, ProfileGenerator


class ManualInputInjector(Node):
    def __init__(self, config: RunConfig) -> None:
        super().__init__("linearity_manual_input_injector")
        self._config = config
        self._profile = ProfileGenerator(config)
        self._lock = Lock()

        self._active = False
        self._completed = False
        self._completion_reason = "not_started"
        self._warmup_counter = 0
        self._landing_sent = False
        self._offboard_command_time_ns: int | None = None
        self._arm_command_time_ns: int | None = None
        self._takeoff_start_time_ns: int | None = None
        self._takeoff_reference_z: float | None = None
        self._takeoff_target_x: float = 0.0
        self._takeoff_target_y: float = 0.0
        self._takeoff_target_z: float | None = None
        self._takeoff_target_yaw: float = 0.0
        self._takeoff_stable_since_ns: int | None = None
        self._manual_mode_command_time_ns: int | None = None
        self._experiment_start_time_ns: int | None = None
        self._landing_command_time_ns: int | None = None
        self._disarm_command_time_ns: int | None = None
        self._completion_time_ns: int | None = None
        self._command_trace: list[dict[str, Any]] = []
        self._attack_trace: list[dict[str, Any]] = []
        self._anomalies: list[str] = []
        self._attack_controller = build_attack_controller_from_config(config)
        self._vehicle_status = VehicleStatus()
        self._vehicle_control_mode = VehicleControlMode()
        self._vehicle_local_position = VehicleLocalPosition()
        self._vehicle_attitude = VehicleAttitude()
        self._vehicle_angular_velocity = VehicleAngularVelocity()
        self._vehicle_attitude_setpoint = VehicleAttitudeSetpoint()
        self._vehicle_rates_setpoint = VehicleRatesSetpoint()
        self._control_allocator_status = ControlAllocatorStatus()
        self._actuator_motors = ActuatorMotors()
        self._state_history_snapshots: deque[dict[str, float]] = deque(maxlen=3)
        self._timer_clock = Clock(clock_type=ClockType.SYSTEM_TIME)

        qos = px4_qos_profile()
        self._manual_input_publisher = self.create_publisher(ManualControlSetpoint, "/fmu/in/manual_control_input", qos)
        self._offboard_control_mode_publisher = self.create_publisher(
            OffboardControlMode, "/fmu/in/offboard_control_mode", qos
        )
        self._trajectory_setpoint_publisher = self.create_publisher(
            TrajectorySetpoint, "/fmu/in/trajectory_setpoint", qos
        )
        self._vehicle_command_publisher = self.create_publisher(VehicleCommand, "/fmu/in/vehicle_command", qos)
        self.create_subscription(VehicleStatus, "/fmu/out/vehicle_status", self._vehicle_status_callback, qos)
        self.create_subscription(
            VehicleControlMode,
            "/fmu/out/vehicle_control_mode",
            self._vehicle_control_mode_callback,
            qos,
        )
        self.create_subscription(
            VehicleLocalPosition,
            "/fmu/out/vehicle_local_position",
            self._vehicle_local_position_callback,
            qos,
        )
        self.create_subscription(VehicleAttitude, "/fmu/out/vehicle_attitude", self._vehicle_attitude_callback, qos)
        self.create_subscription(
            VehicleAngularVelocity,
            "/fmu/out/vehicle_angular_velocity",
            self._vehicle_angular_velocity_callback,
            qos,
        )
        self.create_subscription(
            VehicleAttitudeSetpoint,
            "/fmu/out/vehicle_attitude_setpoint",
            self._vehicle_attitude_setpoint_callback,
            qos,
        )
        self.create_subscription(
            VehicleRatesSetpoint,
            "/fmu/out/vehicle_rates_setpoint",
            self._vehicle_rates_setpoint_callback,
            qos,
        )
        self.create_subscription(
            ControlAllocatorStatus,
            "/fmu/out/control_allocator_status",
            self._control_allocator_status_callback,
            qos,
        )
        self.create_subscription(ActuatorMotors, "/fmu/out/actuator_motors", self._actuator_motors_callback, qos)

        # Drive setpoint publication from wall-clock time so simulator /clock stalls do not interrupt OFFBOARD streaming.
        self._timer = self.create_timer(self._config.period_s, self._timer_callback, clock=self._timer_clock)

    def _vehicle_status_callback(self, msg: VehicleStatus) -> None:
        with self._lock:
            self._vehicle_status = msg
            if msg.failsafe:
                self._append_anomaly("vehicle_status_failsafe")

    def _vehicle_control_mode_callback(self, msg: VehicleControlMode) -> None:
        with self._lock:
            self._vehicle_control_mode = msg

    def _vehicle_local_position_callback(self, msg: VehicleLocalPosition) -> None:
        with self._lock:
            self._vehicle_local_position = msg

    def _vehicle_attitude_callback(self, msg: VehicleAttitude) -> None:
        with self._lock:
            self._vehicle_attitude = msg

    def _vehicle_angular_velocity_callback(self, msg: VehicleAngularVelocity) -> None:
        with self._lock:
            self._vehicle_angular_velocity = msg

    def _vehicle_attitude_setpoint_callback(self, msg: VehicleAttitudeSetpoint) -> None:
        with self._lock:
            self._vehicle_attitude_setpoint = msg

    def _vehicle_rates_setpoint_callback(self, msg: VehicleRatesSetpoint) -> None:
        with self._lock:
            self._vehicle_rates_setpoint = msg

    def _control_allocator_status_callback(self, msg: ControlAllocatorStatus) -> None:
        with self._lock:
            self._control_allocator_status = msg

    def _actuator_motors_callback(self, msg: ActuatorMotors) -> None:
        with self._lock:
            self._actuator_motors = msg

    def _append_anomaly(self, text: str) -> None:
        if text not in self._anomalies:
            self._anomalies.append(text)

    def start_run(self) -> None:
        with self._lock:
            self._active = True
            self._completed = False
            self._completion_reason = "running"
            self._warmup_counter = 0
            self._landing_sent = False
            self._offboard_command_time_ns = None
            self._arm_command_time_ns = None
            self._takeoff_start_time_ns = None
            self._takeoff_reference_z = None
            self._takeoff_target_x = 0.0
            self._takeoff_target_y = 0.0
            self._takeoff_target_z = None
            self._takeoff_target_yaw = 0.0
            self._takeoff_stable_since_ns = None
            self._manual_mode_command_time_ns = None
            self._experiment_start_time_ns = None
            self._landing_command_time_ns = None
            self._disarm_command_time_ns = None
            self._completion_time_ns = None
            self._command_trace.clear()
            self._attack_trace.clear()
            self._anomalies.clear()
            self._state_history_snapshots.clear()
            if self._attack_controller is not None:
                self._attack_controller.reset()

    def is_completed(self) -> bool:
        with self._lock:
            return self._completed

    def command_trace(self) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._command_trace)

    def attack_trace(self) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._attack_trace)

    def report(self) -> dict[str, Any]:
        with self._lock:
            attack_summary = {}
            if self._attack_controller is not None:
                trace_summary = summarize_attack_trace(self._attack_trace)
                attack_summary = {
                    "enabled": True,
                    "method_name": self._attack_controller.method_spec.method_name,
                    "line_code": self._attack_controller.method_spec.line_code,
                    "candidate_id": self._attack_controller.method_spec.candidate_id,
                    **trace_summary,
                }
            return {
                "offboard_command_time_ns": self._offboard_command_time_ns,
                "arm_command_time_ns": self._arm_command_time_ns,
                "takeoff_start_time_ns": self._takeoff_start_time_ns,
                "takeoff_reference_z": self._takeoff_reference_z,
                "takeoff_target_z": self._takeoff_target_z,
                "experiment_start_time_ns": self._experiment_start_time_ns,
                "landing_command_time_ns": self._landing_command_time_ns,
                "disarm_command_time_ns": self._disarm_command_time_ns,
                "completion_time_ns": self._completion_time_ns,
                "completion_reason": self._completion_reason,
                "anomalies": list(self._anomalies),
                "attack_summary": attack_summary,
            }

    def _is_flight_mode(self) -> bool:
        return self._config.manual_mode == "flight"

    def _mode_switch_timeout_s(self) -> float:
        return float(self._config.extras.get("mode_switch_timeout_s", 5.0))

    def _current_heading(self) -> float:
        heading = float(self._vehicle_local_position.heading)
        if math.isnan(heading):
            return 0.0
        return heading

    def _initialize_takeoff_target(self) -> None:
        if bool(self._vehicle_local_position.xy_valid):
            self._takeoff_target_x = float(self._vehicle_local_position.x)
            self._takeoff_target_y = float(self._vehicle_local_position.y)
        if bool(self._vehicle_local_position.z_valid):
            current_z = float(self._vehicle_local_position.z)
            self._takeoff_reference_z = current_z
            self._takeoff_target_z = current_z - self._config.takeoff_altitude_m
        elif self._takeoff_target_z is None:
            self._takeoff_reference_z = 0.0
            self._takeoff_target_z = -self._config.takeoff_altitude_m
            self._append_anomaly("takeoff_reference_unavailable")
        self._takeoff_target_yaw = self._current_heading()

    def _estimated_clearance_m(self) -> float | None:
        candidates: list[float] = []
        if bool(self._vehicle_local_position.dist_bottom_valid):
            candidates.append(float(self._vehicle_local_position.dist_bottom))
        if self._takeoff_reference_z is not None and bool(self._vehicle_local_position.z_valid):
            candidates.append(max(0.0, self._takeoff_reference_z - float(self._vehicle_local_position.z)))
        if not candidates:
            return None
        return max(candidates)

    def _has_valid_clearance(self, min_clearance_m: float) -> bool:
        clearance_m = self._estimated_clearance_m()
        return clearance_m is not None and clearance_m >= min_clearance_m

    def _clearance_is_low(self, min_clearance_m: float) -> bool:
        clearance_m = self._estimated_clearance_m()
        return clearance_m is not None and clearance_m < min_clearance_m

    def _takeoff_target_reached(self) -> bool:
        position_ok = False
        if self._takeoff_target_z is not None and bool(self._vehicle_local_position.z_valid):
            position_ok = abs(float(self._vehicle_local_position.z) - self._takeoff_target_z) <= (
                self._config.takeoff_position_tolerance_m
            )
        velocity_ok = True
        if bool(self._vehicle_local_position.v_z_valid):
            velocity_ok = abs(float(self._vehicle_local_position.vz)) <= self._config.takeoff_velocity_tolerance_m
        clearance_m = self._estimated_clearance_m()
        clearance_ok = clearance_m is not None and clearance_m >= self._config.min_takeoff_clearance_m
        target_clearance_ok = (
            clearance_m is not None
            and clearance_m >= max(self._config.min_takeoff_clearance_m, self._config.takeoff_altitude_m - self._config.takeoff_position_tolerance_m)
        )
        return velocity_ok and (position_ok or (clearance_ok and target_clearance_ok))

    def _record_command(
        self,
        publish_time_ns: int,
        elapsed_s: float,
        profile_value: float,
        roll: float,
        pitch: float,
        yaw: float,
        throttle: float,
        phase: str,
        *,
        command_roll: float | None = None,
        command_pitch: float | None = None,
        command_yaw: float | None = None,
        command_throttle: float | None = None,
    ) -> None:
        sample = CommandSample(
            publish_time_ns=publish_time_ns,
            elapsed_s=elapsed_s,
            profile_value=profile_value,
            roll_body=command_roll if command_roll is not None else roll,
            pitch_body=command_pitch if command_pitch is not None else pitch,
            yaw_body=command_yaw if command_yaw is not None else yaw,
            thrust_z=command_throttle if command_throttle is not None else throttle,
            phase=phase,
        )
        self._command_trace.append(sample.to_row())

    def _current_state_snapshot(self) -> dict[str, float]:
        roll, pitch, yaw = quaternion_to_euler(list(self._vehicle_attitude.q))
        heading = float(self._vehicle_local_position.heading)
        if math.isnan(heading):
            heading = yaw
        altitude = -float(self._vehicle_local_position.z) if bool(self._vehicle_local_position.z_valid) else 0.0
        vertical_speed = -float(self._vehicle_local_position.vz) if bool(self._vehicle_local_position.v_z_valid) else 0.0
        return {
            "roll": float(roll),
            "pitch": float(pitch),
            "yaw": float(yaw),
            "roll_rate": float(self._vehicle_angular_velocity.xyz[0]),
            "pitch_rate": float(self._vehicle_angular_velocity.xyz[1]),
            "yaw_rate": float(self._vehicle_angular_velocity.xyz[2]),
            "position_x": float(self._vehicle_local_position.x) if bool(self._vehicle_local_position.xy_valid) else 0.0,
            "position_y": float(self._vehicle_local_position.y) if bool(self._vehicle_local_position.xy_valid) else 0.0,
            "position_z": float(self._vehicle_local_position.z) if bool(self._vehicle_local_position.z_valid) else 0.0,
            "velocity_x": float(self._vehicle_local_position.vx) if bool(self._vehicle_local_position.v_xy_valid) else 0.0,
            "velocity_y": float(self._vehicle_local_position.vy) if bool(self._vehicle_local_position.v_xy_valid) else 0.0,
            "velocity_z": float(self._vehicle_local_position.vz) if bool(self._vehicle_local_position.v_z_valid) else 0.0,
            "altitude": altitude,
            "vertical_speed": vertical_speed,
            "heading": float(heading),
        }

    def _state_delta_snapshot(self, current_state: dict[str, float]) -> dict[str, float]:
        previous_state = self._state_history_snapshots[0] if self._state_history_snapshots else {}
        return {
            name: float(current_state.get(name, 0.0)) - float(previous_state.get(name, 0.0))
            for name in current_state
        }

    def _tracking_error_snapshot(self, current_state: dict[str, float]) -> dict[str, float]:
        return {
            "roll": float(self._vehicle_attitude_setpoint.roll_body) - float(current_state.get("roll", 0.0)),
            "pitch": float(self._vehicle_attitude_setpoint.pitch_body) - float(current_state.get("pitch", 0.0)),
            "yaw": float(self._vehicle_attitude_setpoint.yaw_body) - float(current_state.get("yaw", 0.0)),
            "roll_rate": float(self._vehicle_rates_setpoint.roll) - float(current_state.get("roll_rate", 0.0)),
            "pitch_rate": float(self._vehicle_rates_setpoint.pitch) - float(current_state.get("pitch_rate", 0.0)),
            "yaw_rate": float(self._vehicle_rates_setpoint.yaw) - float(current_state.get("yaw_rate", 0.0)),
        }

    def _attitude_error_snapshot(self, current_state: dict[str, float]) -> dict[str, float]:
        tracking = self._tracking_error_snapshot(current_state)
        return {
            "roll": float(tracking["roll"]),
            "pitch": float(tracking["pitch"]),
            "yaw": float(tracking["yaw"]),
        }

    def _boundary_stress_value(self) -> float:
        allocator_stress = getattr(self._control_allocator_status, "max_actuator_saturation", None)
        if allocator_stress is not None:
            allocator_stress_value = float(allocator_stress)
            if math.isfinite(allocator_stress_value):
                normalized = allocator_stress_value / 2.0 if abs(allocator_stress_value) > 1.0 else allocator_stress_value
                return max(0.0, min(1.0, abs(normalized)))
        saturation_states = getattr(self._control_allocator_status, "actuator_saturation", None)
        if saturation_states is not None:
            finite_states = [abs(float(value)) for value in list(saturation_states) if math.isfinite(float(value))]
            if finite_states:
                return max(0.0, min(1.0, max(finite_states) / 2.0))
        finite_controls = [abs(float(value)) for value in list(getattr(self._actuator_motors, "control", [])) if math.isfinite(float(value))]
        return max(finite_controls, default=0.0)

    def _recovery_cost_value(self, state_delta: dict[str, float]) -> float:
        values = [abs(float(state_delta.get(name, 0.0))) for name in ("roll", "pitch", "yaw", "roll_rate", "pitch_rate", "yaw_rate")]
        baseline = float(np.mean(values)) if values else 0.0
        return max(0.0, min(1.0, baseline + (0.25 * self._boundary_stress_value())))

    def _current_mode_name(self) -> str:
        if self._vehicle_status.nav_state == VehicleStatus.NAVIGATION_STATE_POSCTL:
            return "POSCTL"
        return self._config.mode_under_test_for_backend("px4")

    def _record_attack_placeholder(
        self,
        *,
        publish_time_ns: int,
        elapsed_s: float,
        phase: str,
        nominal_command: tuple[float, float, float, float],
        attacked_command: tuple[float, float, float, float],
        note: str,
    ) -> None:
        if self._attack_controller is None:
            return
        delta = AttackDelta(
            line_code=self._attack_controller.method_spec.line_code,
            family_name=self._attack_controller.method_spec.method_name,
            active=False,
            delta_command=(0.0, 0.0, 0.0, 0.0),
            pre_projection_command=(0.0, 0.0, 0.0, 0.0),
            objective_terms={
                "bundle_gain": 0.0,
                "tracking_deviation": 0.0,
                "attitude_deviation": 0.0,
                "boundary_stress": 0.0,
                "recovery_cost": 0.0,
                "off_target_leakage": 0.0,
                "conditioning": 0.0,
                "budget": 0.0,
            },
            objective_score=0.0,
            budget_terms={"cumulative_energy": 0.0, "energy_limit": 0.0, "budget_usage": 0.0},
            context_features={},
            notes=(note,),
        )
        self._attack_trace.append(
            make_attack_trace_row(
                publish_time_ns=publish_time_ns,
                elapsed_s=elapsed_s,
                phase=phase,
                nominal_command=nominal_command,
                attacked_command=attacked_command,
                delta=delta,
                method_spec=self._attack_controller.method_spec,
            )
        )

    def _apply_attack(
        self,
        *,
        publish_time_ns: int,
        elapsed_s: float,
        phase: str,
        nominal_command: tuple[float, float, float, float],
        attack_enabled: bool,
    ) -> tuple[float, float, float, float]:
        if self._attack_controller is None:
            return nominal_command
        if not attack_enabled:
            self._record_attack_placeholder(
                publish_time_ns=publish_time_ns,
                elapsed_s=elapsed_s,
                phase=phase,
                nominal_command=nominal_command,
                attacked_command=nominal_command,
                note="inactive_phase",
            )
            return nominal_command
        current_state = self._current_state_snapshot()
        state_delta = self._state_delta_snapshot(current_state)
        tracking_error = self._tracking_error_snapshot(current_state)
        attitude_error = self._attitude_error_snapshot(current_state)
        context = AttackContext(
            backend="PX4",
            mode=self._current_mode_name(),
            current_state=current_state,
            state_delta=state_delta,
            state_history=list(self._state_history_snapshots),
            current_command=nominal_command,
            tracking_error=tracking_error,
            attitude_error=attitude_error,
            boundary_stress=self._boundary_stress_value(),
            recovery_cost=self._recovery_cost_value(state_delta),
            elapsed_fraction=max(0.0, min(1.0, elapsed_s / max(self._profile.total_duration_s, 1e-6))),
        )
        delta = self._attack_controller.generate(context)
        attacked_command = apply_attack_to_command(nominal_command, delta)
        self._attack_trace.append(
            make_attack_trace_row(
                publish_time_ns=publish_time_ns,
                elapsed_s=elapsed_s,
                phase=phase,
                nominal_command=nominal_command,
                attacked_command=attacked_command,
                delta=delta,
                method_spec=self._attack_controller.method_spec,
            )
        )
        self._state_history_snapshots.appendleft(current_state)
        return attacked_command

    def _publish_manual_input(
        self,
        timestamp_us: int,
        timestamp_sample_us: int,
        roll: float,
        pitch: float,
        yaw: float,
        throttle: float,
    ) -> None:
        msg = ManualControlSetpoint()
        msg.timestamp = timestamp_us
        msg.timestamp_sample = timestamp_sample_us
        msg.valid = True
        msg.data_source = ManualControlSetpoint.SOURCE_MAVLINK_0
        msg.roll = clamp(float(roll), -1.0, 1.0)
        msg.pitch = clamp(float(pitch), -1.0, 1.0)
        msg.yaw = clamp(float(yaw), -1.0, 1.0)
        msg.throttle = clamp(float(throttle), -1.0, 1.0)
        msg.flaps = 0.0
        msg.aux1 = 0.0
        msg.aux2 = 0.0
        msg.aux3 = 0.0
        msg.aux4 = 0.0
        msg.aux5 = 0.0
        msg.aux6 = 0.0
        msg.sticks_moving = any(abs(value) > 1e-3 for value in (msg.roll, msg.pitch, msg.yaw, msg.throttle))
        msg.buttons = 0
        self._manual_input_publisher.publish(msg)

    def _publish_position_offboard_control_mode(self, timestamp_us: int) -> None:
        msg = OffboardControlMode()
        msg.position = True
        msg.velocity = False
        msg.acceleration = False
        msg.attitude = False
        msg.body_rate = False
        msg.thrust_and_torque = False
        msg.direct_actuator = False
        msg.timestamp = timestamp_us
        self._offboard_control_mode_publisher.publish(msg)

    def _publish_trajectory_setpoint(self, timestamp_us: int, x: float, y: float, z: float, yaw: float) -> None:
        msg = TrajectorySetpoint()
        msg.timestamp = timestamp_us
        msg.position = [float(x), float(y), float(z)]
        msg.yaw = float(yaw)
        self._trajectory_setpoint_publisher.publish(msg)

    def _publish_vehicle_command(self, command: int, timestamp_us: int, **params: float) -> None:
        msg = VehicleCommand()
        msg.timestamp = timestamp_us
        msg.command = command
        msg.param1 = params.get("param1", 0.0)
        msg.param2 = params.get("param2", 0.0)
        msg.param3 = params.get("param3", 0.0)
        msg.param4 = params.get("param4", 0.0)
        msg.param5 = params.get("param5", 0.0)
        msg.param6 = params.get("param6", 0.0)
        msg.param7 = params.get("param7", 0.0)
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        self._vehicle_command_publisher.publish(msg)

    def _publish_manual_zero(self, timestamp_us: int) -> None:
        self._publish_manual_input(timestamp_us, timestamp_us, 0.0, 0.0, 0.0, 0.0)

    def _manual_mode_engaged(self) -> bool:
        return (
            self._vehicle_status.nav_state == VehicleStatus.NAVIGATION_STATE_POSCTL
            and bool(self._vehicle_control_mode.flag_control_manual_enabled)
        )

    def _echo_timer_callback(self, now_ns: int, now_us: int) -> None:
        if self._warmup_counter < self._config.warmup_cycles:
            self._publish_manual_zero(now_us)
            self._record_command(now_ns, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "warmup_manual")
            self._record_attack_placeholder(
                publish_time_ns=now_ns,
                elapsed_s=0.0,
                phase="warmup_manual",
                nominal_command=(0.0, 0.0, 0.0, 0.0),
                attacked_command=(0.0, 0.0, 0.0, 0.0),
                note="inactive_phase",
            )
            self._warmup_counter += 1
            if self._warmup_counter == self._config.warmup_cycles:
                self._experiment_start_time_ns = now_ns
            return

        if self._experiment_start_time_ns is None:
            self._experiment_start_time_ns = now_ns

        elapsed_s = (now_ns - self._experiment_start_time_ns) / 1e9
        profile_value, nominal_roll, nominal_pitch, nominal_yaw, nominal_throttle, phase = self._profile.manual_targets_at(elapsed_s)
        attacked_command = self._apply_attack(
            publish_time_ns=now_ns,
            elapsed_s=elapsed_s,
            phase=phase,
            nominal_command=(nominal_roll, nominal_pitch, nominal_yaw, nominal_throttle),
            attack_enabled=True,
        )
        self._publish_manual_input(now_us, now_us, *attacked_command)
        self._record_command(
            now_ns,
            elapsed_s,
            profile_value,
            nominal_roll,
            nominal_pitch,
            nominal_yaw,
            nominal_throttle,
            phase,
            command_roll=attacked_command[0],
            command_pitch=attacked_command[1],
            command_yaw=attacked_command[2],
            command_throttle=attacked_command[3],
        )

        if elapsed_s >= self._profile.total_duration_s:
            self._completed = True
            self._completion_time_ns = now_ns
            self._completion_reason = "profile_completed"

    def _flight_timer_callback(self, now_ns: int, now_us: int) -> None:
        if self._warmup_counter < self._config.warmup_cycles:
            if self._takeoff_target_z is None:
                self._initialize_takeoff_target()
            self._publish_position_offboard_control_mode(now_us)
            self._publish_trajectory_setpoint(
                now_us,
                self._takeoff_target_x,
                self._takeoff_target_y,
                self._takeoff_target_z if self._takeoff_target_z is not None else 0.0,
                self._takeoff_target_yaw,
            )
            self._publish_manual_zero(now_us)
            self._record_command(now_ns, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "warmup_position")
            self._record_attack_placeholder(
                publish_time_ns=now_ns,
                elapsed_s=0.0,
                phase="warmup_position",
                nominal_command=(0.0, 0.0, 0.0, 0.0),
                attacked_command=(0.0, 0.0, 0.0, 0.0),
                note="inactive_phase",
            )
            self._warmup_counter += 1
            if self._warmup_counter == self._config.warmup_cycles:
                self._initialize_takeoff_target()
                self._publish_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, now_us, param1=1.0, param2=6.0)
                self._publish_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, now_us, param1=1.0)
                self._offboard_command_time_ns = now_ns
                self._arm_command_time_ns = now_ns
                self._takeoff_start_time_ns = now_ns
            return

        if self._experiment_start_time_ns is None and not self._landing_sent:
            takeoff_elapsed_s = 0.0
            if self._takeoff_start_time_ns is not None:
                takeoff_elapsed_s = (now_ns - self._takeoff_start_time_ns) / 1e9
            if self._takeoff_target_z is None:
                self._initialize_takeoff_target()

            if not self._manual_mode_engaged():
                self._publish_position_offboard_control_mode(now_us)
                self._publish_trajectory_setpoint(
                    now_us,
                    self._takeoff_target_x,
                    self._takeoff_target_y,
                    self._takeoff_target_z if self._takeoff_target_z is not None else 0.0,
                    self._takeoff_target_yaw,
                )

            self._publish_manual_zero(now_us)
            self._record_command(now_ns, takeoff_elapsed_s, 0.0, 0.0, 0.0, 0.0, 0.0, "takeoff_position_hold")
            self._record_attack_placeholder(
                publish_time_ns=now_ns,
                elapsed_s=takeoff_elapsed_s,
                phase="takeoff_position_hold",
                nominal_command=(0.0, 0.0, 0.0, 0.0),
                attacked_command=(0.0, 0.0, 0.0, 0.0),
                note="inactive_phase",
            )

            if self._manual_mode_engaged():
                self._experiment_start_time_ns = now_ns
                return

            if self._takeoff_target_reached():
                if self._takeoff_stable_since_ns is None:
                    self._takeoff_stable_since_ns = now_ns
                stable_elapsed_s = (now_ns - self._takeoff_stable_since_ns) / 1e9
                if stable_elapsed_s >= self._config.takeoff_settle_s:
                    if self._manual_mode_command_time_ns is None:
                        self._publish_vehicle_command(
                            VehicleCommand.VEHICLE_CMD_SET_NAV_STATE,
                            now_us,
                            param1=float(VehicleStatus.NAVIGATION_STATE_POSCTL),
                        )
                        self._manual_mode_command_time_ns = now_ns
            else:
                self._takeoff_stable_since_ns = None

            if (
                self._manual_mode_command_time_ns is not None
                and (now_ns - self._manual_mode_command_time_ns) / 1e9 >= self._mode_switch_timeout_s()
            ):
                self._append_anomaly("manual_mode_switch_timeout")
                self._publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND, now_us)
                self._landing_sent = True
                self._landing_command_time_ns = now_ns
                return

            if takeoff_elapsed_s >= self._config.takeoff_timeout_s:
                self._append_anomaly("takeoff_clearance_timeout")
                self._publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND, now_us)
                self._landing_sent = True
                self._landing_command_time_ns = now_ns
            return

        if self._experiment_start_time_ns is None:
            if self._vehicle_status.arming_state == VehicleStatus.ARMING_STATE_DISARMED:
                self._completed = True
                self._completion_time_ns = now_ns
                self._completion_reason = "disarmed_before_or_during_mode_switch"
                return
            if self._landing_command_time_ns is not None:
                land_elapsed_s = (now_ns - self._landing_command_time_ns) / 1e9
                if land_elapsed_s >= self._config.land_timeout_s:
                    if self._vehicle_status.arming_state == VehicleStatus.ARMING_STATE_ARMED:
                        self._publish_vehicle_command(
                            VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM,
                            now_us,
                            param1=0.0,
                        )
                        self._disarm_command_time_ns = now_ns
                        self._append_anomaly("land_timeout_force_disarm")
                    self._completed = True
                    self._completion_time_ns = now_ns
                    self._completion_reason = "land_timeout_before_experiment"
            return

        elapsed_s = (now_ns - self._experiment_start_time_ns) / 1e9
        if not self._landing_sent:
            profile_value, nominal_roll, nominal_pitch, nominal_yaw, nominal_throttle, phase = self._profile.manual_targets_at(elapsed_s)
            attacked_command = self._apply_attack(
                publish_time_ns=now_ns,
                elapsed_s=elapsed_s,
                phase=phase,
                nominal_command=(nominal_roll, nominal_pitch, nominal_yaw, nominal_throttle),
                attack_enabled=True,
            )
            self._publish_manual_input(now_us, now_us, *attacked_command)
            self._record_command(
                now_ns,
                elapsed_s,
                profile_value,
                nominal_roll,
                nominal_pitch,
                nominal_yaw,
                nominal_throttle,
                phase,
                command_roll=attacked_command[0],
                command_pitch=attacked_command[1],
                command_yaw=attacked_command[2],
                command_throttle=attacked_command[3],
            )

            if not self._manual_mode_engaged() and elapsed_s > 1.0:
                self._append_anomaly("manual_mode_not_held")

            if self._clearance_is_low(self._config.min_profile_clearance_m):
                self._append_anomaly("profile_clearance_low")
                self._publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND, now_us)
                self._landing_sent = True
                self._landing_command_time_ns = now_ns
                return

        if not self._landing_sent and elapsed_s >= self._profile.total_duration_s:
            self._publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND, now_us)
            self._landing_sent = True
            self._landing_command_time_ns = now_ns
            return

        if self._landing_sent:
            self._publish_manual_zero(now_us)
            self._record_attack_placeholder(
                publish_time_ns=now_ns,
                elapsed_s=elapsed_s,
                phase="landing_hold",
                nominal_command=(0.0, 0.0, 0.0, 0.0),
                attacked_command=(0.0, 0.0, 0.0, 0.0),
                note="inactive_phase",
            )
            if self._vehicle_status.arming_state == VehicleStatus.ARMING_STATE_DISARMED:
                self._completed = True
                self._completion_time_ns = now_ns
                self._completion_reason = "disarmed_after_land"
                return

            if self._landing_command_time_ns is not None:
                land_elapsed_s = (now_ns - self._landing_command_time_ns) / 1e9
                if land_elapsed_s >= self._config.land_timeout_s:
                    if self._vehicle_status.arming_state == VehicleStatus.ARMING_STATE_ARMED:
                        self._publish_vehicle_command(
                            VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM,
                            now_us,
                            param1=0.0,
                        )
                        self._disarm_command_time_ns = now_ns
                        self._append_anomaly("land_timeout_force_disarm")
                    self._completed = True
                    self._completion_time_ns = now_ns
                    self._completion_reason = "land_timeout"

    def _timer_callback(self) -> None:
        with self._lock:
            if not self._active or self._completed:
                return

            now_ns = time.time_ns()
            now_us = int(now_ns / 1000)
            if self._is_flight_mode():
                self._flight_timer_callback(now_ns, now_us)
            else:
                self._echo_timer_callback(now_ns, now_us)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="独立运行 manual input injector 调试入口。")
    parser.add_argument("--config", type=Path, required=True, help="YAML 配置路径。")
    args = parser.parse_args(argv)

    config = load_run_config(args.config)
    rclpy.init()
    injector = ManualInputInjector(config)
    executor = SingleThreadedExecutor()
    executor.add_node(injector)
    injector.start_run()

    deadline = time.monotonic() + config.run_timeout_s
    try:
        while time.monotonic() < deadline and not injector.is_completed():
            executor.spin_once(timeout_sec=0.1)
    finally:
        executor.shutdown()
        injector.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
