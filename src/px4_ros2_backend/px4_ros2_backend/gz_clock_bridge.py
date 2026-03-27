from __future__ import annotations

import argparse
import json
import subprocess
import threading
from typing import Any

import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from rosgraph_msgs.msg import Clock


class GzClockBridge(Node):
    def __init__(self, gz_topic: str, ros_topic: str) -> None:
        super().__init__("gz_clock_bridge")
        self._gz_topic = gz_topic
        self._ros_topic = ros_topic
        self._process: subprocess.Popen[str] | None = None
        self._reader_thread: threading.Thread | None = None
        self._stderr_thread: threading.Thread | None = None
        self._active = True
        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        self._publisher = self.create_publisher(Clock, ros_topic, qos)
        self._published_count = 0
        self._launch_bridge_process()

    def _launch_bridge_process(self) -> None:
        self._process = subprocess.Popen(
            [
                "gz",
                "topic",
                "-e",
                "-t",
                self._gz_topic,
                "--json-output",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._reader_thread = threading.Thread(target=self._pump_stdout, daemon=True)
        self._stderr_thread = threading.Thread(target=self._pump_stderr, daemon=True)
        self._reader_thread.start()
        self._stderr_thread.start()
        self.get_logger().info(f"bridging Gazebo clock {self._gz_topic} -> ROS {self._ros_topic}")

    def _pump_stdout(self) -> None:
        assert self._process is not None
        assert self._process.stdout is not None
        for raw_line in self._process.stdout:
            if not self._active:
                break
            line = raw_line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                self.get_logger().warning(f"ignored malformed gz clock line: {line}")
                continue

            sim_clock = payload.get("sim", payload)
            sec = _coerce_int(sim_clock.get("sec"))
            nanosec = _coerce_int(sim_clock.get("nsec", sim_clock.get("nanosec")))
            if sec is None or nanosec is None:
                continue

            message = Clock()
            message.clock.sec = sec
            message.clock.nanosec = nanosec
            self._publisher.publish(message)
            self._published_count += 1

        if self._active:
            self.get_logger().warning("gz clock stream ended")
            rclpy.shutdown()

    def _pump_stderr(self) -> None:
        assert self._process is not None
        assert self._process.stderr is not None
        for raw_line in self._process.stderr:
            if not self._active:
                break
            line = raw_line.strip()
            if line:
                self.get_logger().warning(f"gz topic stderr: {line}")

    def destroy_node(self) -> bool:
        self._active = False
        if self._process is not None and self._process.poll() is None:
            self._process.terminate()
            try:
                self._process.wait(timeout=3.0)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait(timeout=3.0)
        return super().destroy_node()


def _coerce_int(value: Any) -> int | None:
    if value in ("", None):
        return None
    return int(value)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="将 Gazebo Transport 的 Clock 转成 ROS /clock。")
    parser.add_argument("--gz-topic", default="/clock", help="Gazebo 侧时钟 topic。")
    parser.add_argument("--ros-topic", default="/clock", help="ROS 侧输出 topic。")
    args = parser.parse_args(argv)

    rclpy.init()
    node = GzClockBridge(args.gz_topic, args.ros_topic)
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
