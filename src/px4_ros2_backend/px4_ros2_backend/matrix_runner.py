from __future__ import annotations

import argparse
import csv
import os
import shlex
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from linearity_core.config import load_study_config
from linearity_core.paths import CONFIG_ROOT, PX4_MATRIX_ROOT as MATRIX_ROOT, PX4_ROOT

from .common import wait_for_ros_topics
from .experiment_runner import run_capture

WORLD_ROOT = PX4_ROOT / "Tools/simulation/gz/worlds"
GZ_RESOURCE_PATH = f"{PX4_ROOT}/Tools/simulation/gz/models:{WORLD_ROOT}"
DEFAULT_PATTERNS = ("*.yaml",)
ROOTFS_STATE_FILES = ("dataman", "parameters.bson", "parameters_backup.bson")
CORE_TOPIC_SUFFIXES = ("vehicle_status", "vehicle_attitude", "vehicle_control_mode", "vehicle_local_position")


@dataclass(slots=True)
class ManagedProcess:
    name: str
    process: subprocess.Popen[str]
    log_path: Path

    def stop(self) -> None:
        if self.process.poll() is not None:
            return
        self.process.terminate()
        try:
            self.process.wait(timeout=10.0)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=5.0)


def _discover_configs(patterns: tuple[str, ...]) -> list[Path]:
    configs: list[Path] = []
    seen: set[Path] = set()
    for pattern in patterns:
        for path in sorted(CONFIG_ROOT.glob(pattern)):
            resolved = path.resolve()
            if resolved not in seen:
                configs.append(resolved)
                seen.add(resolved)
    return configs


def _resolve_config_paths(explicit_configs: tuple[str, ...], patterns: tuple[str, ...]) -> list[Path]:
    configs: list[Path] = []
    seen: set[Path] = set()
    for value in explicit_configs:
        resolved = Path(value).expanduser().resolve()
        if resolved not in seen:
            configs.append(resolved)
            seen.add(resolved)
    for resolved in _discover_configs(patterns):
        if resolved not in seen:
            configs.append(resolved)
            seen.add(resolved)
    return configs


def _start_process(name: str, command: str, log_path: Path, env: dict[str, str], cwd: Path | None = None) -> ManagedProcess:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8") as handle:
        handle.write(f"$ {command}\n")
    log_file = log_path.open("a", encoding="utf-8")
    process = subprocess.Popen(
        ["bash", "-lc", command],
        cwd=str(cwd) if cwd else None,
        env=env,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return ManagedProcess(name=name, process=process, log_path=log_path)


def _headless_enabled() -> bool:
    if os.environ.get("AUTOPILOT_LAB_HEADLESS", "").strip() == "1":
        return True
    if os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"):
        return False
    return True


def _session_env(world: str) -> dict[str, str]:
    env = os.environ.copy()
    env["PX4_GZ_WORLD"] = world
    env["PX4_GZ_STANDALONE"] = "1"
    env["HEADLESS"] = "1" if _headless_enabled() else "0"
    env["GZ_SIM_RESOURCE_PATH"] = GZ_RESOURCE_PATH
    env.setdefault("GZ_VERSION", "harmonic")
    env.setdefault("ROS_DOMAIN_ID", "0")
    return env


def _reset_px4_rootfs_state() -> None:
    rootfs_dir = PX4_ROOT / "build/px4_sitl_default/rootfs"
    for filename in ROOTFS_STATE_FILES:
        path = rootfs_dir / filename
        try:
            path.unlink()
        except FileNotFoundError:
            continue


def _start_session(world: str, session_dir: Path) -> list[ManagedProcess]:
    env = _session_env(world)
    headless = env.get("HEADLESS") == "1"
    _reset_px4_rootfs_state()
    processes = [
        _start_process(
            "gazebo",
            f"exec gz sim -r {'-s ' if headless else ''}{shlex.quote(str(WORLD_ROOT / f'{world}.sdf'))}",
            session_dir / "gazebo.log",
            env,
        ),
        _start_process(
            "microxrce",
            "exec MicroXRCEAgent udp4 -p 8888",
            session_dir / "microxrce.log",
            env,
        ),
    ]
    time.sleep(2.0)
    processes.append(
        _start_process(
            "px4",
            f"cd {shlex.quote(str(PX4_ROOT))} && exec make px4_sitl gz_x500",
            session_dir / "px4.log",
            env,
        )
    )
    return processes


def _stop_session(processes: list[ManagedProcess]) -> None:
    for process in reversed(processes):
        process.stop()
    subprocess.run(
        ["bash", "-lc", "pkill -INT -f 'gz sim|MicroXRCEAgent|px4_sitl_default/bin/px4|gz_clock_bridge' || true"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2.0)


def _write_matrix_rows(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = ["index", "repeat_index", "config", "artifact_dir", "status", "exit_code", "session_dir"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def run_matrix(world: str, config_paths: list[Path], repeat: int = 1) -> tuple[Path, list[dict[str, str]]]:
    run_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_{world}"
    matrix_dir = MATRIX_ROOT / run_id
    matrix_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, str]] = []
    required_topics = tuple(f"/fmu/out/{name}" for name in CORE_TOPIC_SUFFIXES)
    jobs = [(config_path, repeat_index) for repeat_index in range(1, max(repeat, 1) + 1) for config_path in config_paths]
    for index, (config_path, repeat_index) in enumerate(jobs, start=1):
        session_dir = matrix_dir / f"{index:02d}_{config_path.stem}_r{repeat_index}"
        session_dir.mkdir(parents=True, exist_ok=True)
        processes = _start_session(world, session_dir)
        status = "session_failed"
        exit_code = 1
        artifact_dir = ""
        try:
            if not wait_for_ros_topics(required_topics, timeout_s=60.0):
                status = "topics_not_ready"
            else:
                config = load_study_config(config_path).with_repeat_index(repeat_index)
                exit_code, artifact_path = run_capture(config)
                artifact_dir = str(artifact_path)
                status = "completed" if exit_code == 0 else "failed"
        finally:
            _stop_session(processes)

        results.append(
            {
                "index": str(index),
                "repeat_index": str(repeat_index),
                "config": str(config_path),
                "artifact_dir": artifact_dir,
                "status": status,
                "exit_code": str(exit_code),
                "session_dir": str(session_dir),
            }
        )
        _write_matrix_rows(matrix_dir / "runs.csv", results)
    return matrix_dir, results


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="批量执行 PX4 raw linearity capture。")
    parser.add_argument("--world", default="default", help="Gazebo world 名称。")
    parser.add_argument("--config", action="append", dest="configs", help="显式 study config 路径，可重复。")
    parser.add_argument("--pattern", action="append", dest="patterns", help="study config glob，可重复。")
    parser.add_argument("--repeat", type=int, default=1, help="每个 config fresh 重复次数。")
    args = parser.parse_args(argv)

    patterns = tuple(args.patterns or DEFAULT_PATTERNS)
    configs = _resolve_config_paths(tuple(args.configs or ()), patterns)
    matrix_dir, rows = run_matrix(args.world, configs, repeat=args.repeat)
    print(f"matrix_dir={matrix_dir}")
    print(f"jobs={len(rows)}")


if __name__ == "__main__":
    main()
