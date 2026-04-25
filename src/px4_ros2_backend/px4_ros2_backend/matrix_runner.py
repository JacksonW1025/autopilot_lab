from __future__ import annotations

import argparse
import csv
import os
import shlex
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

from linearity_core.config import load_study_config
from linearity_core.io import read_yaml
from linearity_core.paths import CONFIG_ROOT, PX4_MATRIX_ROOT as MATRIX_ROOT, PX4_ROOT

from .common import wait_for_ros_topics
from .experiment_runner import run_capture

WORLD_ROOT = PX4_ROOT / "Tools/simulation/gz/worlds"
GZ_RESOURCE_PATH = f"{PX4_ROOT}/Tools/simulation/gz/models:{WORLD_ROOT}"
DEFAULT_PATTERNS = ("*.yaml",)
ROOTFS_STATE_FILES = ("dataman", "parameters.bson", "parameters_backup.bson")
CORE_TOPIC_SUFFIXES = ("vehicle_status", "vehicle_attitude", "vehicle_control_mode", "vehicle_local_position")
PX4_PROCESS_PATTERN = "gz sim|MicroXRCEAgent|px4_sitl_default/bin/px4|gz_clock_bridge"
RUNS_FIELDNAMES = [
    "index",
    "repeat_index",
    "config",
    "artifact_dir",
    "status",
    "exit_code",
    "session_dir",
    "research_acceptance",
    "accepted_count_for_config",
]


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


def _cleanup_residual_px4_processes() -> None:
    for signal_name in ("INT", "TERM", "KILL"):
        subprocess.run(
            ["bash", "-lc", f"pkill -{signal_name} -f '{PX4_PROCESS_PATTERN}' || true"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1.0)


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
    _cleanup_residual_px4_processes()
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
    _cleanup_residual_px4_processes()


def _write_matrix_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RUNS_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _read_matrix_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _existing_index(rows: list[dict[str, str]]) -> int:
    result = 0
    for row in rows:
        try:
            result = max(result, int(row.get("index", 0) or 0))
        except ValueError:
            continue
    return result


def _next_session_generation(matrix_dir: Path) -> int:
    session_root = matrix_dir / "_session"
    generation = 0
    if session_root.exists():
        for path in session_root.iterdir():
            if not path.is_dir():
                continue
            name = path.name
            if not name.startswith("session_"):
                continue
            try:
                generation = max(generation, int(name.split("_", 1)[1]))
            except ValueError:
                continue
    return generation


def _acceptance_state(artifact_dir: str) -> str:
    if not artifact_dir:
        return ""
    manifest_path = Path(artifact_dir) / "manifest.yaml"
    if not manifest_path.exists():
        return ""
    manifest = read_yaml(manifest_path)
    return str(manifest.get("research_acceptance", "")).strip().lower()


@lru_cache(maxsize=None)
def _artifact_manifest(artifact_dir: str) -> dict[str, object]:
    if not artifact_dir:
        return {}
    manifest_path = Path(artifact_dir) / "manifest.yaml"
    if not manifest_path.exists():
        return {}
    manifest = read_yaml(manifest_path)
    return manifest if isinstance(manifest, dict) else {}


def _acceptance_block_from_manifest(manifest: dict[str, object]) -> dict[str, object]:
    data_quality = manifest.get("data_quality", {})
    if not isinstance(data_quality, dict):
        return {}
    acceptance = data_quality.get("acceptance", {})
    return acceptance if isinstance(acceptance, dict) else {}


def _row_counts_towards_attempt_budget(row: dict[str, str]) -> bool:
    if str(row.get("status", "")).strip().lower() != "completed":
        return False
    manifest = _artifact_manifest(str(row.get("artifact_dir", "")).strip())
    if not manifest:
        return False
    if str(manifest.get("research_acceptance", "")).strip().lower() == "accepted":
        return True
    acceptance = _acceptance_block_from_manifest(manifest)
    if not bool(acceptance.get("experiment_started", False)):
        return False
    if not bool(acceptance.get("active_phase_present", False)):
        return False
    if list(acceptance.get("missing_topics_blocking", []) or []):
        return False
    return True


def _should_restart_persistent_session(row: dict[str, str]) -> bool:
    if str(row.get("status", "")).strip().lower() != "completed":
        return True
    manifest = _artifact_manifest(str(row.get("artifact_dir", "")).strip())
    if not manifest:
        return True
    acceptance = _acceptance_block_from_manifest(manifest)
    if not bool(acceptance.get("experiment_started", False)):
        return True
    if not bool(acceptance.get("active_phase_present", False)):
        return True
    if list(acceptance.get("missing_topics_blocking", []) or []):
        return True
    injector_report = manifest.get("injector_report", {})
    if isinstance(injector_report, dict):
        completion_reason = str(injector_report.get("completion_reason", "") or "").strip()
        if completion_reason in {
            "disarmed_before_experiment",
            "disarmed_before_or_during_mode_switch",
            "land_timeout_before_experiment",
        }:
            return True
        anomalies = {str(item) for item in list(injector_report.get("anomalies", []) or [])}
        if "takeoff_clearance_timeout" in anomalies:
            return True
    return False


def _config_progress(rows: list[dict[str, str]], config_path: Path) -> tuple[int, int, int]:
    config_key = str(config_path.resolve())
    total_attempts = 0
    counted_attempts = 0
    accepted = 0
    for row in rows:
        row_config = str(row.get("config", "")).strip()
        if not row_config:
            continue
        try:
            row_key = str(Path(row_config).resolve())
        except OSError:
            row_key = row_config
        if row_key != config_key:
            continue
        total_attempts += 1
        if str(row.get("research_acceptance", "")).strip().lower() == "accepted":
            accepted += 1
        if _row_counts_towards_attempt_budget(row):
            counted_attempts += 1
    return total_attempts, counted_attempts, accepted


def run_matrix(
    world: str,
    config_paths: list[Path],
    repeat: int = 1,
    *,
    accepted_target: int = 0,
    max_attempts_per_config: int | None = None,
    persistent_session: bool = False,
    resume_from: Path | None = None,
) -> tuple[Path, list[dict[str, str]]]:
    if resume_from is not None:
        matrix_dir = resume_from.expanduser().resolve()
    else:
        run_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_{world}"
        matrix_dir = MATRIX_ROOT / run_id
    matrix_dir.mkdir(parents=True, exist_ok=True)
    runs_path = matrix_dir / "runs.csv"
    results = _read_matrix_rows(runs_path)
    required_topics = tuple(f"/fmu/out/{name}" for name in CORE_TOPIC_SUFFIXES)
    accepted_target = max(0, int(accepted_target))
    default_attempt_limit = max(max(repeat, 1), accepted_target) + 5 if accepted_target > 0 else max(repeat, 1)
    attempt_limit = max_attempts_per_config if max_attempts_per_config is not None else default_attempt_limit

    index = _existing_index(results)
    active_processes: list[ManagedProcess] | None = None
    active_session_dir: Path | None = None
    session_generation = _next_session_generation(matrix_dir)

    def _stop_active_session() -> None:
        nonlocal active_processes, active_session_dir
        if active_processes is None:
            return
        _stop_session(active_processes)
        active_processes = None
        active_session_dir = None

    def _ensure_persistent_session() -> tuple[list[ManagedProcess], Path]:
        nonlocal active_processes, active_session_dir, session_generation
        if active_processes is not None and active_session_dir is not None:
            return active_processes, active_session_dir
        session_generation += 1
        active_session_dir = matrix_dir / "_session" / f"session_{session_generation:02d}"
        active_session_dir.mkdir(parents=True, exist_ok=True)
        active_processes = _start_session(world, active_session_dir)
        return active_processes, active_session_dir

    try:
        for config_path in config_paths:
            total_attempt_count, counted_attempt_count, accepted_count = _config_progress(results, config_path)
            while True:
                if accepted_target > 0:
                    if accepted_count >= accepted_target:
                        break
                    if counted_attempt_count >= max(attempt_limit, accepted_target):
                        raise RuntimeError(
                            f"{config_path.name} accepted runs不足: expected={accepted_target}, actual={accepted_count}, attempts={total_attempt_count}, counted_attempts={counted_attempt_count}"
                        )
                else:
                    if total_attempt_count >= max(repeat, 1):
                        break

                total_attempt_count += 1
                repeat_index = total_attempt_count
                index += 1
                status = "session_failed"
                exit_code = 1
                artifact_dir = ""
                if persistent_session:
                    _processes, session_dir = _ensure_persistent_session()
                    if not wait_for_ros_topics(required_topics, timeout_s=10.0):
                        _stop_active_session()
                        _processes, session_dir = _ensure_persistent_session()
                    if not wait_for_ros_topics(required_topics, timeout_s=60.0):
                        status = "topics_not_ready"
                        _stop_active_session()
                    else:
                        config = load_study_config(config_path).with_repeat_index(repeat_index)
                        exit_code, artifact_path = run_capture(config)
                        artifact_dir = str(artifact_path)
                        status = "completed" if exit_code == 0 else "failed"
                        if exit_code != 0:
                            _stop_active_session()
                else:
                    session_dir = matrix_dir / f"{index:02d}_{config_path.stem}_r{repeat_index}"
                    session_dir.mkdir(parents=True, exist_ok=True)
                    processes = _start_session(world, session_dir)
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

                research_acceptance = _acceptance_state(artifact_dir)
                if research_acceptance == "accepted":
                    accepted_count += 1
                row = {
                    "index": str(index),
                    "repeat_index": str(repeat_index),
                    "config": str(config_path.resolve()),
                    "artifact_dir": artifact_dir,
                    "status": status,
                    "exit_code": str(exit_code),
                    "session_dir": str(session_dir),
                    "research_acceptance": research_acceptance,
                    "accepted_count_for_config": str(accepted_count),
                }
                if _row_counts_towards_attempt_budget(row):
                    counted_attempt_count += 1
                results.append(row)
                if persistent_session and _should_restart_persistent_session(row):
                    _stop_active_session()
                _write_matrix_rows(runs_path, results)
    finally:
        _stop_active_session()
    return matrix_dir, results


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="批量执行 PX4 raw linearity capture。")
    parser.add_argument("--world", default="default", help="Gazebo world 名称。")
    parser.add_argument("--config", action="append", dest="configs", help="显式 study config 路径，可重复。")
    parser.add_argument("--pattern", action="append", dest="patterns", help="study config glob，可重复。")
    parser.add_argument("--repeat", type=int, default=1, help="每个 config fresh 重复次数。")
    parser.add_argument("--accepted-target", type=int, default=0, help="每个 config 需要达到的 accepted raw run 数量。")
    parser.add_argument("--max-attempts-per-config", type=int, default=None, help="accepted-target 模式下每个 config 的最大尝试次数。")
    parser.add_argument("--persistent-session", action="store_true", help="复用单个 PX4/Gazebo 会话执行多个 config。")
    parser.add_argument("--resume-from", type=Path, default=None, help="从已有 matrix 目录继续执行。")
    args = parser.parse_args(argv)

    patterns = tuple(args.patterns or (DEFAULT_PATTERNS if not args.configs else ()))
    configs = _resolve_config_paths(tuple(args.configs or ()), patterns)
    matrix_dir, rows = run_matrix(
        args.world,
        configs,
        repeat=args.repeat,
        accepted_target=args.accepted_target,
        max_attempts_per_config=args.max_attempts_per_config,
        persistent_session=args.persistent_session,
        resume_from=args.resume_from,
    )
    print(f"matrix_dir={matrix_dir}")
    print(f"jobs={len(rows)}")


if __name__ == "__main__":
    main()
