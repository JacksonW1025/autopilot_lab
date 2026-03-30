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

from fep_core.study_analysis_runner import run_study_analysis
from fep_core.paths import CONFIG_ROOT
from fep_core.paths import PX4_MATRIX_ROOT as MATRIX_ROOT
from fep_core.paths import PX4_ROOT
from fep_core.paths import PX4_RUNS_ROOT

from .common import load_run_config, wait_for_ros_topics
from .experiment_runner import run_experiment

WORLD_ROOT = PX4_ROOT / "Tools/simulation/gz/worlds"
GZ_RESOURCE_PATH = f"{PX4_ROOT}/Tools/simulation/gz/models:{WORLD_ROOT}"

DEFAULT_PATTERNS = ("*.yaml",)
ANALYSIS_WORLD_FILTERS = {"windy": "windy", "default": "nominal"}
ROOTFS_STATE_FILES = ("dataman", "parameters.bson", "parameters_backup.bson")


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
            if path not in seen:
                configs.append(path.resolve())
                seen.add(path)
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


def _session_env(world: str) -> dict[str, str]:
    env = os.environ.copy()
    env["PX4_GZ_WORLD"] = world
    env["PX4_GZ_STANDALONE"] = "1"
    env["HEADLESS"] = "1"
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
    _reset_px4_rootfs_state()
    processes = [
        _start_process(
            "gazebo",
            f"exec gz sim -r -s {shlex.quote(str(WORLD_ROOT / f'{world}.sdf'))}",
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
        [
            "bash",
            "-lc",
            "pkill -INT -f 'gz sim|MicroXRCEAgent|px4_sitl_default/bin/px4|gz_clock_bridge' || true",
        ],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2.0)


def _write_matrix_rows(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "index",
        "repeat_index",
        "config",
        "artifact_dir",
        "status",
        "exit_code",
        "session_dir",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _analysis_world_filter(world: str, override: str | None = None) -> str:
    if override:
        return override
    return ANALYSIS_WORLD_FILTERS.get(world, "nominal")


def run_matrix(
    world: str,
    config_paths: list[Path],
    force_timing_required: bool,
    analysis_world_filter: str | None = None,
    repeat: int = 1,
) -> tuple[Path, list[dict[str, str]]]:
    run_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_{world}"
    matrix_dir = MATRIX_ROOT / run_id
    matrix_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, str]] = []
    os.environ["PX4_GZ_WORLD"] = world

    required_topics = tuple(f"/fmu/out/{name}" for name in CORE_TOPIC_SUFFIXES)
    jobs = [(config_path, repeat_index) for repeat_index in range(1, max(repeat, 1) + 1) for config_path in config_paths]
    for index, (config_path, repeat_index) in enumerate(jobs, start=1):
        suffix = f"_r{repeat_index}" if repeat > 1 else ""
        session_dir = matrix_dir / f"{index:02d}_{config_path.stem}{suffix}"
        processes = _start_session(world, session_dir)
        status = "session_failed"
        artifact_dir = ""
        exit_code = 1
        try:
            if not wait_for_ros_topics(required_topics, timeout_s=60.0):
                status = "topics_not_ready"
            else:
                config = load_run_config(config_path)
                if force_timing_required:
                    config.timing_required = True
                exit_code, artifact_path = run_experiment(config)
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

    run_study_analysis([PX4_RUNS_ROOT])
    return matrix_dir, results


CORE_TOPIC_SUFFIXES = ("vehicle_status", "vehicle_attitude", "vehicle_control_mode", "vehicle_local_position")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="按 fresh/headless 口径批量执行 PX4 matrix，并在结束后生成新的分层 study 汇总。")
    parser.add_argument("--world", default="windy", help="Gazebo world 名称，默认 windy；nominal 请传 default。")
    parser.add_argument(
        "--pattern",
        action="append",
        dest="patterns",
        help="配置 glob；默认纳入 config 目录下全部 YAML。",
    )
    parser.add_argument(
        "--force-timing-required",
        action="store_true",
        help="把所有 config 临时提升为 timing_required=true。",
    )
    parser.add_argument(
        "--analysis-world-filter",
        choices=("nominal", "windy", "all"),
        default=None,
        help="兼容旧接口；当前新的分层 study 汇总不再按 world_filter 切分。",
    )
    parser.add_argument("--repeat", type=int, default=1, help="每个 config fresh 重复次数，默认 1。")
    args = parser.parse_args(argv)

    patterns = tuple(args.patterns) if args.patterns else DEFAULT_PATTERNS
    config_paths = _discover_configs(patterns)
    if not config_paths:
        raise SystemExit("未找到任何匹配的配置文件。")

    matrix_dir, results = run_matrix(
        args.world,
        config_paths,
        args.force_timing_required,
        args.analysis_world_filter,
        args.repeat,
    )
    print(f"matrix_dir={matrix_dir}")
    print(f"runs={len(results)}")


if __name__ == "__main__":
    main()
