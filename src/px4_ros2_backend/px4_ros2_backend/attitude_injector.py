from __future__ import annotations

import argparse
import math
import time
from pathlib import Path
from threading import Lock
from typing import Any

import rclpy
from px4_msgs.msg import (
    OffboardControlMode,
    TrajectorySetpoint,
    VehicleAttitudeSetpoint,
    VehicleCommand,
    VehicleLocalPosition,
    VehicleStatus,
)
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node

from .common import RunConfig, clamp, euler_to_quaternion, load_run_config, px4_qos_profile
from .profiles import CommandSample, ProfileGenerator


class AttitudeInjector(Node):
    def __init__(self, config: RunConfig) -> None:
        super().__init__("fep_attitude_injector")
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
        self._attitude_target_z: float | None = None
        self._experiment_start_time_ns: int | None = None
        self._landing_command_time_ns: int | None = None
        self._disarm_command_time_ns: int | None = None
        self._completion_time_ns: int | None = None
        self._command_trace: list[dict[str, Any]] = []
        self._anomalies: list[str] = []
        self._vehicle_status = VehicleStatus()
        self._vehicle_local_position = VehicleLocalPosition()

        qos = px4_qos_profile()
        self._offboard_control_mode_publisher = self.create_publisher(
            OffboardControlMode, "/fmu/in/offboard_control_mode", qos
        )
        self._vehicle_attitude_setpoint_publisher = self.create_publisher(
            VehicleAttitudeSetpoint, "/fmu/in/vehicle_attitude_setpoint", qos
        )
        self._trajectory_setpoint_publisher = self.create_publisher(
            TrajectorySetpoint, "/fmu/in/trajectory_setpoint", qos
        )
        self._vehicle_command_publisher = self.create_publisher(VehicleCommand, "/fmu/in/vehicle_command", qos)

        self.create_subscription(VehicleStatus, "/fmu/out/vehicle_status", self._vehicle_status_callback, qos)
        self.create_subscription(
            VehicleLocalPosition,
            "/fmu/out/vehicle_local_position",
            self._vehicle_local_position_callback,
            qos,
        )

        self._timer = self.create_timer(self._config.period_s, self._timer_callback)

    def _vehicle_status_callback(self, msg: VehicleStatus) -> None:
        with self._lock:
            self._vehicle_status = msg
            if msg.failsafe:
                self._append_anomaly("vehicle_status_failsafe")

    def _vehicle_local_position_callback(self, msg: VehicleLocalPosition) -> None:
        with self._lock:
            self._vehicle_local_position = msg

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
            self._command_trace.clear()
            self._anomalies.clear()
            self._offboard_command_time_ns = None
            self._arm_command_time_ns = None
            self._takeoff_start_time_ns = None
            self._takeoff_reference_z = None
            self._takeoff_target_x = 0.0
            self._takeoff_target_y = 0.0
            self._takeoff_target_z = None
            self._takeoff_target_yaw = 0.0
            self._takeoff_stable_since_ns = None
            self._attitude_target_z = None
            self._experiment_start_time_ns = None
            self._landing_command_time_ns = None
            self._disarm_command_time_ns = None
            self._completion_time_ns = None

    def is_completed(self) -> bool:
        with self._lock:
            return self._completed

    def completion_reason(self) -> str:
        with self._lock:
            return self._completion_reason

    def command_trace(self) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._command_trace)

    def anomalies(self) -> list[str]:
        with self._lock:
            return list(self._anomalies)

    def report(self) -> dict[str, Any]:
        with self._lock:
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
            }

    def _estimated_clearance_m(self) -> float | None:
        candidates: list[float] = []
        if bool(self._vehicle_local_position.dist_bottom_valid):
            candidates.append(float(self._vehicle_local_position.dist_bottom))
        if self._takeoff_reference_z is not None and bool(self._vehicle_local_position.z_valid):
            relative_ascent_m = max(0.0, self._takeoff_reference_z - float(self._vehicle_local_position.z))
            candidates.append(relative_ascent_m)
        if not candidates:
            return None
        return max(candidates)

    def _has_valid_clearance(self, min_clearance_m: float) -> bool:
        clearance_m = self._estimated_clearance_m()
        return clearance_m is not None and clearance_m >= min_clearance_m

    def _clearance_is_low(self, min_clearance_m: float) -> bool:
        clearance_m = self._estimated_clearance_m()
        return clearance_m is not None and clearance_m < min_clearance_m

    def _current_takeoff_thrust(self, takeoff_elapsed_s: float) -> float:
        ramp_s = max(self._config.takeoff_ramp_s, 1e-6)
        progress = min(max(takeoff_elapsed_s / ramp_s, 0.0), 1.0)
        return self._config.takeoff_thrust + (
            self._config.takeoff_thrust_max - self._config.takeoff_thrust
        ) * progress

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

    def _takeoff_target_reached(self) -> bool:
        if self._takeoff_target_z is None or not bool(self._vehicle_local_position.z_valid):
            return False
        position_ok = abs(float(self._vehicle_local_position.z) - self._takeoff_target_z) <= (
            self._config.takeoff_position_tolerance_m
        )
        velocity_ok = True
        if bool(self._vehicle_local_position.v_z_valid):
            velocity_ok = abs(float(self._vehicle_local_position.vz)) <= self._config.takeoff_velocity_tolerance_m
        clearance_ok = self._has_valid_clearance(self._config.min_takeoff_clearance_m)
        return position_ok and velocity_ok and clearance_ok

    def _apply_altitude_hold(self, base_thrust_z: float) -> float:
        thrust_z = float(base_thrust_z)
        if self._attitude_target_z is not None and bool(self._vehicle_local_position.z_valid):
            z_error = self._attitude_target_z - float(self._vehicle_local_position.z)
            vz = float(self._vehicle_local_position.vz) if bool(self._vehicle_local_position.v_z_valid) else 0.0
            thrust_z += self._config.altitude_hold_kp * z_error
            thrust_z -= self._config.altitude_hold_kd * vz
        return clamp(thrust_z, self._config.thrust_z_min, self._config.thrust_z_max)

    def _timer_callback(self) -> None:
        with self._lock:
            if not self._active or self._completed:
                return

            now_ns = time.time_ns()
            now_us = int(now_ns / 1000)

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
                self._record_command(now_ns, 0.0, 0.0, 0.0, 0.0, 0.0, self._config.hover_thrust, "warmup_position")
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
                self._publish_position_offboard_control_mode(now_us)
                self._publish_trajectory_setpoint(
                    now_us,
                    self._takeoff_target_x,
                    self._takeoff_target_y,
                    self._takeoff_target_z if self._takeoff_target_z is not None else 0.0,
                    self._takeoff_target_yaw,
                )
                self._record_command(
                    now_ns,
                    takeoff_elapsed_s,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    self._config.hover_thrust,
                    "takeoff_position_hold",
                )
                if self._takeoff_target_reached():
                    if self._takeoff_stable_since_ns is None:
                        self._takeoff_stable_since_ns = now_ns
                    stable_elapsed_s = (now_ns - self._takeoff_stable_since_ns) / 1e9
                    if stable_elapsed_s >= self._config.takeoff_settle_s:
                        self._attitude_target_z = self._takeoff_target_z
                        self._experiment_start_time_ns = now_ns
                        return
                else:
                    self._takeoff_stable_since_ns = None
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
                    self._completion_reason = "disarmed_before_experiment"
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
                self._publish_attitude_offboard_control_mode(now_us)
                profile_value, roll_body, pitch_body, yaw_body, thrust_z, phase = self._profile.attitude_targets_at(
                    elapsed_s
                )
                thrust_z = self._apply_altitude_hold(thrust_z)
                self._publish_attitude_setpoint(now_us, roll_body, pitch_body, yaw_body, thrust_z)
                self._record_command(now_ns, elapsed_s, profile_value, roll_body, pitch_body, yaw_body, thrust_z, phase)

                if self._clearance_is_low(self._config.min_profile_clearance_m):
                    self._append_anomaly("profile_clearance_low")
                    self._publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND, now_us)
                    self._landing_sent = True
                    self._landing_command_time_ns = now_ns
                    return

                if (
                    self._offboard_command_time_ns is not None
                    and elapsed_s > 2.0
                    and self._vehicle_status.nav_state != VehicleStatus.NAVIGATION_STATE_OFFBOARD
                ):
                    self._append_anomaly("offboard_not_held")

            if not self._landing_sent and elapsed_s >= self._profile.total_duration_s:
                self._publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND, now_us)
                self._landing_sent = True
                self._landing_command_time_ns = now_ns
                return

            if self._landing_sent:
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

    def _record_command(
        self,
        publish_time_ns: int,
        elapsed_s: float,
        profile_value: float,
        roll_body: float,
        pitch_body: float,
        yaw_body: float,
        thrust_z: float,
        phase: str,
    ) -> None:
        sample = CommandSample(
            publish_time_ns=publish_time_ns,
            elapsed_s=elapsed_s,
            profile_value=profile_value,
            roll_body=roll_body,
            pitch_body=pitch_body,
            yaw_body=yaw_body,
            thrust_z=thrust_z,
            phase=phase,
        )
        self._command_trace.append(sample.to_row())

    def _publish_offboard_control_mode(self, timestamp_us: int) -> None:
        self._publish_attitude_offboard_control_mode(timestamp_us)

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

    def _publish_attitude_offboard_control_mode(self, timestamp_us: int) -> None:
        msg = OffboardControlMode()
        msg.position = False
        msg.velocity = False
        msg.acceleration = False
        msg.attitude = True
        msg.body_rate = False
        msg.thrust_and_torque = False
        msg.direct_actuator = False
        msg.timestamp = timestamp_us
        self._offboard_control_mode_publisher.publish(msg)

    def _publish_trajectory_setpoint(
        self,
        timestamp_us: int,
        x: float,
        y: float,
        z: float,
        yaw: float,
    ) -> None:
        msg = TrajectorySetpoint()
        msg.timestamp = timestamp_us
        msg.position = [float(x), float(y), float(z)]
        msg.yaw = float(yaw)
        self._trajectory_setpoint_publisher.publish(msg)

    def _publish_attitude_setpoint(
        self,
        timestamp_us: int,
        roll_body: float,
        pitch_body: float,
        yaw_body: float,
        thrust_z: float,
    ) -> None:
        msg = VehicleAttitudeSetpoint()
        msg.timestamp = timestamp_us
        msg.roll_body = float(roll_body)
        msg.pitch_body = float(pitch_body)
        msg.yaw_body = float(yaw_body)
        msg.q_d = euler_to_quaternion(float(roll_body), float(pitch_body), float(yaw_body))
        msg.thrust_body = [0.0, 0.0, float(thrust_z)]
        msg.reset_integral = False
        msg.fw_control_yaw_wheel = False
        self._vehicle_attitude_setpoint_publisher.publish(msg)

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


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="独立运行 attitude injector 调试入口。")
    parser.add_argument("--config", type=Path, required=True, help="YAML 配置路径。")
    args = parser.parse_args(argv)

    config = load_run_config(args.config)
    rclpy.init()
    injector = AttitudeInjector(config)
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
