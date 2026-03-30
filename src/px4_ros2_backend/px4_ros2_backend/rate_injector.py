from __future__ import annotations

import argparse
import time
from pathlib import Path

import rclpy
from px4_msgs.msg import OffboardControlMode, VehicleCommand, VehicleRatesSetpoint, VehicleStatus
from rclpy.executors import SingleThreadedExecutor

from .attitude_injector import AttitudeInjector
from .common import load_run_config, px4_qos_profile


class RateInjector(AttitudeInjector):
    def __init__(self, config) -> None:
        super().__init__(config)
        qos = px4_qos_profile()
        self._vehicle_rates_setpoint_publisher = self.create_publisher(
            VehicleRatesSetpoint,
            "/fmu/in/vehicle_rates_setpoint",
            qos,
        )

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
                profile_value, roll_rate, pitch_rate, yaw_rate, thrust_z, phase = self._profile.rate_targets_at(elapsed_s)
                thrust_z = self._apply_altitude_hold(thrust_z)
                self._publish_attitude_setpoint(now_us, roll_rate, pitch_rate, yaw_rate, thrust_z)
                self._record_command(now_ns, elapsed_s, profile_value, roll_rate, pitch_rate, yaw_rate, thrust_z, phase)

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

    def _publish_attitude_offboard_control_mode(self, timestamp_us: int) -> None:
        msg = OffboardControlMode()
        msg.position = False
        msg.velocity = False
        msg.acceleration = False
        msg.attitude = False
        msg.body_rate = True
        msg.thrust_and_torque = False
        msg.direct_actuator = False
        msg.timestamp = timestamp_us
        self._offboard_control_mode_publisher.publish(msg)

    def _publish_attitude_setpoint(
        self,
        timestamp_us: int,
        roll_body: float,
        pitch_body: float,
        yaw_body: float,
        thrust_z: float,
    ) -> None:
        msg = VehicleRatesSetpoint()
        msg.timestamp = timestamp_us
        msg.roll = float(roll_body)
        msg.pitch = float(pitch_body)
        msg.yaw = float(yaw_body)
        msg.thrust_body = [0.0, 0.0, float(thrust_z)]
        msg.reset_integral = False
        self._vehicle_rates_setpoint_publisher.publish(msg)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="独立运行 rate injector 调试入口。")
    parser.add_argument("--config", type=Path, required=True, help="YAML 配置路径。")
    args = parser.parse_args(argv)

    config = load_run_config(args.config)
    rclpy.init()
    injector = RateInjector(config)
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
