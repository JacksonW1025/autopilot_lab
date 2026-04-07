from __future__ import annotations

import os
import shlex
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

import rclpy
from linearity_core.config import RunConfig, clamp, euler_to_quaternion, load_run_config, quaternion_to_euler
from linearity_core.paths import PX4_LOG_ROOT, PX4_RAW_ROOT as PX4_RUNS_ROOT, WORKSPACE_ROOT
from rclpy.context import Context
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from rosgraph_msgs.msg import Clock


ARTIFACT_ROOT = PX4_RUNS_ROOT

RECORDED_TOPICS = (
    "/fmu/out/vehicle_attitude",
    "/fmu/out/vehicle_attitude_setpoint",
    "/fmu/out/vehicle_angular_velocity",
    "/fmu/out/vehicle_rates_setpoint",
    "/fmu/out/vehicle_local_position",
    "/fmu/out/rate_ctrl_status",
    "/fmu/out/control_allocator_status",
    "/fmu/out/actuator_motors",
    "/fmu/out/vehicle_status",
    "/fmu/out/manual_control_setpoint",
    "/fmu/out/vehicle_control_mode",
)

CORE_READY_TOPICS = (
    "vehicle_attitude",
    "vehicle_local_position",
    "vehicle_status",
    "vehicle_control_mode",
)

CLOCK_TOPIC_CANDIDATES = ("/clock", "/world/default/clock")


@dataclass(slots=True)
class ClockBridgeHandle:
    process: subprocess.Popen[str]
    gz_topic: str
    log_path: Path | None = None


def px4_qos_profile() -> QoSProfile:
    return QoSProfile(
        reliability=ReliabilityPolicy.BEST_EFFORT,
        durability=DurabilityPolicy.TRANSIENT_LOCAL,
        history=HistoryPolicy.KEEP_LAST,
        depth=1,
    )


def run_capture(command: list[str]) -> str:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def read_clock_topic_available() -> bool:
    return read_clock_sample() is not None


def read_clock_sample(timeout_s: float = 3.0) -> tuple[int, int] | None:
    context = Context()
    rclpy.init(args=None, context=context)
    node = Node("linearity_clock_probe", context=context)
    executor = SingleThreadedExecutor(context=context)
    executor.add_node(node)
    qos = QoSProfile(
        reliability=ReliabilityPolicy.BEST_EFFORT,
        durability=DurabilityPolicy.VOLATILE,
        history=HistoryPolicy.KEEP_LAST,
        depth=1,
    )
    sample: tuple[int, int] | None = None

    def callback(message: Clock) -> None:
        nonlocal sample
        sample = (int(message.clock.sec), int(message.clock.nanosec))

    subscription = node.create_subscription(Clock, "/clock", callback, qos)
    deadline = time.monotonic() + timeout_s
    try:
        while time.monotonic() < deadline and sample is None and context.ok():
            executor.spin_once(timeout_sec=0.1)
    finally:
        executor.remove_node(node)
        executor.shutdown()
        node.destroy_subscription(subscription)
        node.destroy_node()
        context.shutdown()
    return sample


def read_clock_topic_advancing(sample_gap_s: float = 1.0) -> bool:
    first = read_clock_sample()
    if first is None:
        return False
    time.sleep(sample_gap_s)
    second = read_clock_sample()
    if second is None:
        return False
    return second > first


def wait_for_ros_topics(topic_names: tuple[str, ...], timeout_s: float = 30.0) -> bool:
    context = Context()
    rclpy.init(args=None, context=context)
    node = Node("linearity_topic_probe", context=context)
    executor = SingleThreadedExecutor(context=context)
    executor.add_node(node)
    deadline = time.monotonic() + timeout_s
    try:
        while time.monotonic() < deadline and context.ok():
            available = {name for name, _types in node.get_topic_names_and_types()}
            if all(topic in available for topic in topic_names):
                return True
            executor.spin_once(timeout_sec=0.1)
    finally:
        executor.remove_node(node)
        executor.shutdown()
        node.destroy_node()
        context.shutdown()
    return False


def select_gz_clock_topic() -> str | None:
    try:
        result = subprocess.run(["gz", "topic", "-l"], check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    topics = set(result.stdout.splitlines())
    for topic in CLOCK_TOPIC_CANDIDATES:
        if topic in topics:
            return topic
    return None


def start_clock_bridge(log_path: Path | None = None) -> ClockBridgeHandle | None:
    gz_topic = select_gz_clock_topic()
    if gz_topic is None:
        return None

    command = (
        "source /opt/ros/humble/setup.bash && "
        f"source {shlex.quote(str(WORKSPACE_ROOT / 'install/setup.bash'))} && "
        f"exec ros2 run px4_ros2_backend gz_clock_bridge --gz-topic {shlex.quote(gz_topic)} --ros-topic /clock"
    )
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        command = f"{command} > {shlex.quote(str(log_path))} 2>&1"

    process = subprocess.Popen(
        ["bash", "-lc", command],
        env=os.environ.copy(),
        stdout=subprocess.DEVNULL if log_path is None else None,
        stderr=subprocess.DEVNULL if log_path is None else None,
        text=True,
    )
    return ClockBridgeHandle(process=process, gz_topic=gz_topic, log_path=log_path)


def stop_clock_bridge(handle: ClockBridgeHandle | None) -> None:
    if handle is None or handle.process.poll() is not None:
        return
    handle.process.terminate()
    try:
        handle.process.wait(timeout=5.0)
    except subprocess.TimeoutExpired:
        handle.process.kill()
        handle.process.wait(timeout=3.0)


def ensure_clock_bridge(timeout_s: float = 8.0, log_path: Path | None = None) -> tuple[ClockBridgeHandle | None, bool]:
    if read_clock_topic_available() and read_clock_topic_advancing(sample_gap_s=0.2):
        return None, True

    handle = start_clock_bridge(log_path)
    if handle is None:
        return None, False

    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if handle.process.poll() is not None:
            break
        if read_clock_topic_available() and read_clock_topic_advancing(sample_gap_s=0.2):
            return handle, True
        time.sleep(0.2)

    return handle, False
