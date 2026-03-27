from __future__ import annotations

import argparse
import math
import time
from pathlib import Path
from threading import Lock
from typing import Any

import rclpy
from px4_msgs.msg import (
    ActuatorMotors,
    ControlAllocatorStatus,
    ManualControlSetpoint,
    RateCtrlStatus,
    VehicleAngularVelocity,
    VehicleAttitude,
    VehicleAttitudeSetpoint,
    VehicleControlMode,
    VehicleLocalPosition,
    VehicleRatesSetpoint,
    VehicleStatus,
)
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node

from .artifacts import write_rows_csv
from .common import CORE_READY_TOPICS, px4_qos_profile, quaternion_to_euler


class TelemetryRecorder(Node):
    FIELDNAMES = {
        "vehicle_attitude": [
            "received_time_ns",
            "timestamp",
            "timestamp_sample",
            "q_w",
            "q_x",
            "q_y",
            "q_z",
            "roll",
            "pitch",
            "yaw",
        ],
        "vehicle_local_position": [
            "received_time_ns",
            "timestamp",
            "timestamp_sample",
            "x",
            "y",
            "z",
            "vx",
            "vy",
            "vz",
            "heading",
            "dist_bottom",
            "dist_bottom_valid",
            "xy_valid",
            "z_valid",
            "v_xy_valid",
            "v_z_valid",
        ],
        "vehicle_attitude_setpoint": [
            "received_time_ns",
            "timestamp",
            "roll_body",
            "pitch_body",
            "yaw_body",
            "yaw_sp_move_rate",
            "thrust_body_x",
            "thrust_body_y",
            "thrust_body_z",
            "reset_integral",
        ],
        "vehicle_angular_velocity": [
            "received_time_ns",
            "timestamp",
            "timestamp_sample",
            "xyz_x",
            "xyz_y",
            "xyz_z",
            "xyz_derivative_x",
            "xyz_derivative_y",
            "xyz_derivative_z",
        ],
        "vehicle_rates_setpoint": [
            "received_time_ns",
            "timestamp",
            "roll",
            "pitch",
            "yaw",
            "thrust_body_x",
            "thrust_body_y",
            "thrust_body_z",
            "reset_integral",
        ],
        "rate_ctrl_status": [
            "received_time_ns",
            "timestamp",
            "rollspeed_integ",
            "pitchspeed_integ",
            "yawspeed_integ",
            "wheel_rate_integ",
        ],
        "control_allocator_status": [
            "received_time_ns",
            "timestamp",
            "torque_setpoint_achieved",
            "thrust_setpoint_achieved",
            "unallocated_torque_x",
            "unallocated_torque_y",
            "unallocated_torque_z",
            "unallocated_thrust_x",
            "unallocated_thrust_y",
            "unallocated_thrust_z",
            "max_actuator_saturation",
            "handled_motor_failure_mask",
        ],
        "actuator_motors": [
            "received_time_ns",
            "timestamp",
            "timestamp_sample",
            "reversible_flags",
            "motor_1",
            "motor_2",
            "motor_3",
            "motor_4",
            "motor_5",
            "motor_6",
            "motor_7",
            "motor_8",
            "motor_9",
            "motor_10",
            "motor_11",
            "motor_12",
            "motors_peak",
        ],
        "vehicle_status": [
            "received_time_ns",
            "timestamp",
            "arming_state",
            "nav_state",
            "nav_state_user_intention",
            "failsafe",
            "failsafe_defer_state",
            "failure_detector_status",
            "pre_flight_checks_pass",
            "gcs_connection_lost",
            "latest_arming_reason",
            "latest_disarming_reason",
            "vehicle_type",
        ],
        "manual_control_setpoint": [
            "received_time_ns",
            "timestamp",
            "timestamp_sample",
            "valid",
            "data_source",
            "roll",
            "pitch",
            "yaw",
            "throttle",
            "sticks_moving",
            "buttons",
        ],
        "vehicle_control_mode": [
            "received_time_ns",
            "timestamp",
            "flag_armed",
            "flag_control_manual_enabled",
            "flag_control_auto_enabled",
            "flag_control_offboard_enabled",
            "flag_control_position_enabled",
            "flag_control_velocity_enabled",
            "flag_control_altitude_enabled",
            "flag_control_acceleration_enabled",
            "flag_control_attitude_enabled",
            "flag_control_rates_enabled",
            "source_id",
        ],
        "vehicle_status_events": [
            "received_time_ns",
            "event_type",
            "field_name",
            "previous_value",
            "current_value",
        ],
        "vehicle_control_mode_events": [
            "received_time_ns",
            "event_type",
            "field_name",
            "previous_value",
            "current_value",
        ],
    }

    def __init__(self) -> None:
        super().__init__("fep_telemetry_recorder")
        self._lock = Lock()
        self._rows: dict[str, list[dict[str, Any]]] = {
            "vehicle_attitude": [],
            "vehicle_attitude_setpoint": [],
            "vehicle_angular_velocity": [],
            "vehicle_rates_setpoint": [],
            "vehicle_local_position": [],
            "rate_ctrl_status": [],
            "control_allocator_status": [],
            "actuator_motors": [],
            "vehicle_status": [],
            "manual_control_setpoint": [],
            "vehicle_control_mode": [],
            "vehicle_status_events": [],
            "vehicle_control_mode_events": [],
        }
        self._counts = {key: 0 for key in self._rows}
        self._previous_status: dict[str, Any] | None = None
        self._previous_control_mode: dict[str, Any] | None = None

        qos = px4_qos_profile()
        self.create_subscription(VehicleAttitude, "/fmu/out/vehicle_attitude", self._vehicle_attitude_callback, qos)
        self.create_subscription(
            VehicleAttitudeSetpoint,
            "/fmu/out/vehicle_attitude_setpoint",
            self._vehicle_attitude_setpoint_callback,
            qos,
        )
        self.create_subscription(
            VehicleAngularVelocity,
            "/fmu/out/vehicle_angular_velocity",
            self._vehicle_angular_velocity_callback,
            qos,
        )
        self.create_subscription(
            VehicleRatesSetpoint,
            "/fmu/out/vehicle_rates_setpoint",
            self._vehicle_rates_setpoint_callback,
            qos,
        )
        self.create_subscription(
            VehicleLocalPosition,
            "/fmu/out/vehicle_local_position",
            self._vehicle_local_position_callback,
            qos,
        )
        self.create_subscription(RateCtrlStatus, "/fmu/out/rate_ctrl_status", self._rate_ctrl_status_callback, qos)
        self.create_subscription(
            ControlAllocatorStatus,
            "/fmu/out/control_allocator_status",
            self._control_allocator_status_callback,
            qos,
        )
        self.create_subscription(ActuatorMotors, "/fmu/out/actuator_motors", self._actuator_motors_callback, qos)
        self.create_subscription(VehicleStatus, "/fmu/out/vehicle_status", self._vehicle_status_callback, qos)
        self.create_subscription(
            ManualControlSetpoint,
            "/fmu/out/manual_control_setpoint",
            self._manual_control_setpoint_callback,
            qos,
        )
        self.create_subscription(
            VehicleControlMode,
            "/fmu/out/vehicle_control_mode",
            self._vehicle_control_mode_callback,
            qos,
        )

    def _append_row(self, key: str, row: dict[str, Any]) -> None:
        with self._lock:
            self._rows[key].append(row)
            self._counts[key] += 1

    def _append_events(
        self,
        key: str,
        received_time_ns: int,
        previous: dict[str, Any] | None,
        current: dict[str, Any],
        fields: tuple[str, ...],
    ) -> dict[str, Any]:
        if previous is None:
            return current
        events = []
        for field in fields:
            previous_value = previous[field]
            current_value = current[field]
            if previous_value != current_value:
                events.append(
                    {
                        "received_time_ns": received_time_ns,
                        "event_type": key,
                        "field_name": field,
                        "previous_value": previous_value,
                        "current_value": current_value,
                    }
                )
        if events:
            with self._lock:
                self._rows[key].extend(events)
                self._counts[key] += len(events)
        return current

    def _vehicle_attitude_callback(self, msg: VehicleAttitude) -> None:
        received_time_ns = time.time_ns()
        roll, pitch, yaw = quaternion_to_euler(list(msg.q))
        self._append_row(
            "vehicle_attitude",
            {
                "received_time_ns": received_time_ns,
                "timestamp": msg.timestamp,
                "timestamp_sample": msg.timestamp_sample,
                "q_w": msg.q[0],
                "q_x": msg.q[1],
                "q_y": msg.q[2],
                "q_z": msg.q[3],
                "roll": roll,
                "pitch": pitch,
                "yaw": yaw,
            },
        )

    def _vehicle_attitude_setpoint_callback(self, msg: VehicleAttitudeSetpoint) -> None:
        received_time_ns = time.time_ns()
        self._append_row(
            "vehicle_attitude_setpoint",
            {
                "received_time_ns": received_time_ns,
                "timestamp": msg.timestamp,
                "roll_body": msg.roll_body,
                "pitch_body": msg.pitch_body,
                "yaw_body": msg.yaw_body,
                "yaw_sp_move_rate": msg.yaw_sp_move_rate,
                "thrust_body_x": msg.thrust_body[0],
                "thrust_body_y": msg.thrust_body[1],
                "thrust_body_z": msg.thrust_body[2],
                "reset_integral": msg.reset_integral,
            },
        )

    def _vehicle_angular_velocity_callback(self, msg: VehicleAngularVelocity) -> None:
        received_time_ns = time.time_ns()
        self._append_row(
            "vehicle_angular_velocity",
            {
                "received_time_ns": received_time_ns,
                "timestamp": msg.timestamp,
                "timestamp_sample": msg.timestamp_sample,
                "xyz_x": msg.xyz[0],
                "xyz_y": msg.xyz[1],
                "xyz_z": msg.xyz[2],
                "xyz_derivative_x": msg.xyz_derivative[0],
                "xyz_derivative_y": msg.xyz_derivative[1],
                "xyz_derivative_z": msg.xyz_derivative[2],
            },
        )

    def _vehicle_rates_setpoint_callback(self, msg: VehicleRatesSetpoint) -> None:
        received_time_ns = time.time_ns()
        self._append_row(
            "vehicle_rates_setpoint",
            {
                "received_time_ns": received_time_ns,
                "timestamp": msg.timestamp,
                "roll": msg.roll,
                "pitch": msg.pitch,
                "yaw": msg.yaw,
                "thrust_body_x": msg.thrust_body[0],
                "thrust_body_y": msg.thrust_body[1],
                "thrust_body_z": msg.thrust_body[2],
                "reset_integral": msg.reset_integral,
            },
        )

    def _vehicle_local_position_callback(self, msg: VehicleLocalPosition) -> None:
        received_time_ns = time.time_ns()
        self._append_row(
            "vehicle_local_position",
            {
                "received_time_ns": received_time_ns,
                "timestamp": msg.timestamp,
                "timestamp_sample": msg.timestamp_sample,
                "x": msg.x,
                "y": msg.y,
                "z": msg.z,
                "vx": msg.vx,
                "vy": msg.vy,
                "vz": msg.vz,
                "heading": msg.heading,
                "dist_bottom": msg.dist_bottom,
                "dist_bottom_valid": msg.dist_bottom_valid,
                "xy_valid": msg.xy_valid,
                "z_valid": msg.z_valid,
                "v_xy_valid": msg.v_xy_valid,
                "v_z_valid": msg.v_z_valid,
            },
        )

    def _vehicle_status_callback(self, msg: VehicleStatus) -> None:
        received_time_ns = time.time_ns()
        current = {
            "received_time_ns": received_time_ns,
            "timestamp": msg.timestamp,
            "arming_state": msg.arming_state,
            "nav_state": msg.nav_state,
            "nav_state_user_intention": msg.nav_state_user_intention,
            "failsafe": msg.failsafe,
            "failsafe_defer_state": msg.failsafe_defer_state,
            "failure_detector_status": msg.failure_detector_status,
            "pre_flight_checks_pass": msg.pre_flight_checks_pass,
            "gcs_connection_lost": msg.gcs_connection_lost,
            "latest_arming_reason": msg.latest_arming_reason,
            "latest_disarming_reason": msg.latest_disarming_reason,
            "vehicle_type": msg.vehicle_type,
        }
        self._append_row("vehicle_status", current)
        self._previous_status = self._append_events(
            "vehicle_status_events",
            received_time_ns,
            self._previous_status,
            current,
            (
                "arming_state",
                "nav_state",
                "failsafe",
                "failure_detector_status",
                "pre_flight_checks_pass",
                "gcs_connection_lost",
            ),
        )

    def _rate_ctrl_status_callback(self, msg: RateCtrlStatus) -> None:
        received_time_ns = time.time_ns()
        self._append_row(
            "rate_ctrl_status",
            {
                "received_time_ns": received_time_ns,
                "timestamp": msg.timestamp,
                "rollspeed_integ": msg.rollspeed_integ,
                "pitchspeed_integ": msg.pitchspeed_integ,
                "yawspeed_integ": msg.yawspeed_integ,
                "wheel_rate_integ": msg.wheel_rate_integ,
            },
        )

    def _control_allocator_status_callback(self, msg: ControlAllocatorStatus) -> None:
        received_time_ns = time.time_ns()
        max_saturation = max(int(value) for value in msg.actuator_saturation)
        self._append_row(
            "control_allocator_status",
            {
                "received_time_ns": received_time_ns,
                "timestamp": msg.timestamp,
                "torque_setpoint_achieved": msg.torque_setpoint_achieved,
                "thrust_setpoint_achieved": msg.thrust_setpoint_achieved,
                "unallocated_torque_x": msg.unallocated_torque[0],
                "unallocated_torque_y": msg.unallocated_torque[1],
                "unallocated_torque_z": msg.unallocated_torque[2],
                "unallocated_thrust_x": msg.unallocated_thrust[0],
                "unallocated_thrust_y": msg.unallocated_thrust[1],
                "unallocated_thrust_z": msg.unallocated_thrust[2],
                "max_actuator_saturation": max_saturation,
                "handled_motor_failure_mask": msg.handled_motor_failure_mask,
            },
        )

    def _actuator_motors_callback(self, msg: ActuatorMotors) -> None:
        received_time_ns = time.time_ns()
        controls = list(msg.control)
        finite_controls = [abs(float(value)) for value in controls if not math.isnan(float(value))]
        row = {
            "received_time_ns": received_time_ns,
            "timestamp": msg.timestamp,
            "timestamp_sample": msg.timestamp_sample,
            "reversible_flags": msg.reversible_flags,
            "motors_peak": max(finite_controls, default=math.nan),
        }
        for index, value in enumerate(controls, start=1):
            row[f"motor_{index}"] = value
        self._append_row("actuator_motors", row)

    def _manual_control_setpoint_callback(self, msg: ManualControlSetpoint) -> None:
        received_time_ns = time.time_ns()
        self._append_row(
            "manual_control_setpoint",
            {
                "received_time_ns": received_time_ns,
                "timestamp": msg.timestamp,
                "timestamp_sample": msg.timestamp_sample,
                "valid": msg.valid,
                "data_source": msg.data_source,
                "roll": msg.roll,
                "pitch": msg.pitch,
                "yaw": msg.yaw,
                "throttle": msg.throttle,
                "sticks_moving": msg.sticks_moving,
                "buttons": msg.buttons,
            },
        )

    def _vehicle_control_mode_callback(self, msg: VehicleControlMode) -> None:
        received_time_ns = time.time_ns()
        current = {
            "received_time_ns": received_time_ns,
            "timestamp": msg.timestamp,
            "flag_armed": msg.flag_armed,
            "flag_control_manual_enabled": msg.flag_control_manual_enabled,
            "flag_control_auto_enabled": msg.flag_control_auto_enabled,
            "flag_control_offboard_enabled": msg.flag_control_offboard_enabled,
            "flag_control_position_enabled": msg.flag_control_position_enabled,
            "flag_control_velocity_enabled": msg.flag_control_velocity_enabled,
            "flag_control_altitude_enabled": msg.flag_control_altitude_enabled,
            "flag_control_acceleration_enabled": msg.flag_control_acceleration_enabled,
            "flag_control_attitude_enabled": msg.flag_control_attitude_enabled,
            "flag_control_rates_enabled": msg.flag_control_rates_enabled,
            "source_id": msg.source_id,
        }
        self._append_row("vehicle_control_mode", current)
        self._previous_control_mode = self._append_events(
            "vehicle_control_mode_events",
            received_time_ns,
            self._previous_control_mode,
            current,
            (
                "flag_armed",
                "flag_control_manual_enabled",
                "flag_control_auto_enabled",
                "flag_control_offboard_enabled",
                "flag_control_attitude_enabled",
                "flag_control_rates_enabled",
                "source_id",
            ),
        )

    def core_topics_ready(self) -> bool:
        with self._lock:
            return all(self._counts[key] > 0 for key in CORE_READY_TOPICS)

    def snapshot_rows(self) -> dict[str, list[dict[str, Any]]]:
        with self._lock:
            return {key: list(rows) for key, rows in self._rows.items()}

    def latest_row(self, key: str) -> dict[str, Any] | None:
        with self._lock:
            if key not in self._rows or not self._rows[key]:
                return None
            return dict(self._rows[key][-1])

    def summary(self) -> dict[str, Any]:
        with self._lock:
            return {
                "message_counts": {
                    "vehicle_attitude": self._counts["vehicle_attitude"],
                    "vehicle_attitude_setpoint": self._counts["vehicle_attitude_setpoint"],
                    "vehicle_angular_velocity": self._counts["vehicle_angular_velocity"],
                    "vehicle_rates_setpoint": self._counts["vehicle_rates_setpoint"],
                    "vehicle_local_position": self._counts["vehicle_local_position"],
                    "rate_ctrl_status": self._counts["rate_ctrl_status"],
                    "control_allocator_status": self._counts["control_allocator_status"],
                    "actuator_motors": self._counts["actuator_motors"],
                    "vehicle_status": self._counts["vehicle_status"],
                    "manual_control_setpoint": self._counts["manual_control_setpoint"],
                    "vehicle_control_mode": self._counts["vehicle_control_mode"],
                },
                "event_counts": {
                    "vehicle_status_events": self._counts["vehicle_status_events"],
                    "vehicle_control_mode_events": self._counts["vehicle_control_mode_events"],
                },
            }

    def write_csvs(self, telemetry_dir: Path) -> None:
        snapshot = self.snapshot_rows()
        write_rows_csv(
            telemetry_dir / "vehicle_attitude.csv",
            snapshot["vehicle_attitude"],
            self.FIELDNAMES["vehicle_attitude"],
        )
        write_rows_csv(
            telemetry_dir / "vehicle_local_position.csv",
            snapshot["vehicle_local_position"],
            self.FIELDNAMES["vehicle_local_position"],
        )
        write_rows_csv(
            telemetry_dir / "vehicle_attitude_setpoint.csv",
            snapshot["vehicle_attitude_setpoint"],
            self.FIELDNAMES["vehicle_attitude_setpoint"],
        )
        write_rows_csv(
            telemetry_dir / "vehicle_angular_velocity.csv",
            snapshot["vehicle_angular_velocity"],
            self.FIELDNAMES["vehicle_angular_velocity"],
        )
        write_rows_csv(
            telemetry_dir / "vehicle_rates_setpoint.csv",
            snapshot["vehicle_rates_setpoint"],
            self.FIELDNAMES["vehicle_rates_setpoint"],
        )
        write_rows_csv(
            telemetry_dir / "rate_ctrl_status.csv",
            snapshot["rate_ctrl_status"],
            self.FIELDNAMES["rate_ctrl_status"],
        )
        write_rows_csv(
            telemetry_dir / "control_allocator_status.csv",
            snapshot["control_allocator_status"],
            self.FIELDNAMES["control_allocator_status"],
        )
        write_rows_csv(
            telemetry_dir / "actuator_motors.csv",
            snapshot["actuator_motors"],
            self.FIELDNAMES["actuator_motors"],
        )
        write_rows_csv(
            telemetry_dir / "vehicle_status.csv",
            snapshot["vehicle_status"],
            self.FIELDNAMES["vehicle_status"],
        )
        write_rows_csv(
            telemetry_dir / "manual_control_setpoint.csv",
            snapshot["manual_control_setpoint"],
            self.FIELDNAMES["manual_control_setpoint"],
        )
        write_rows_csv(
            telemetry_dir / "vehicle_control_mode.csv",
            snapshot["vehicle_control_mode"],
            self.FIELDNAMES["vehicle_control_mode"],
        )
        write_rows_csv(
            telemetry_dir / "vehicle_status_events.csv",
            snapshot["vehicle_status_events"],
            self.FIELDNAMES["vehicle_status_events"],
        )
        write_rows_csv(
            telemetry_dir / "vehicle_control_mode_events.csv",
            snapshot["vehicle_control_mode_events"],
            self.FIELDNAMES["vehicle_control_mode_events"],
        )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="独立运行 telemetry recorder 调试入口。")
    parser.add_argument("--output-dir", type=Path, required=True, help="CSV 输出目录。")
    parser.add_argument("--duration-s", type=float, default=10.0, help="录制时长。")
    args = parser.parse_args(argv)

    rclpy.init()
    recorder = TelemetryRecorder()
    executor = SingleThreadedExecutor()
    executor.add_node(recorder)
    deadline = time.monotonic() + args.duration_s
    try:
        while time.monotonic() < deadline:
            executor.spin_once(timeout_sec=0.1)
    finally:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        recorder.write_csvs(args.output_dir)
        executor.shutdown()
        recorder.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
