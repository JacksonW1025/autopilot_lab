from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

from linearity_core.config import load_study_config
from linearity_core.io import read_yaml
from linearity_core.paths import ARDUPILOT_MATRIX_ROOT, CONFIG_ROOT

from .experiment_runner import run_capture
from .session import cleanup_residual_processes, start_sitl as start_sitl_process, start_visualizer, stop_process


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


def _write_runs_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RUNS_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _read_runs_csv(path: Path) -> list[dict[str, str]]:
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
    return False


def run_matrix(
    config_paths: list[Path],
    vehicle: str,
    frame: str,
    skip_sitl: bool,
    repeat: int = 1,
    *,
    accepted_target: int = 0,
    max_attempts_per_config: int | None = None,
    enable_visualization: bool | None = None,
    persistent_session: bool = False,
    resume_from: Path | None = None,
) -> tuple[Path, list[dict[str, str]]]:
    if resume_from is not None:
        matrix_dir = resume_from.expanduser().resolve()
    else:
        run_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_ardupilot"
        matrix_dir = ARDUPILOT_MATRIX_ROOT / run_id
    matrix_dir.mkdir(parents=True, exist_ok=True)
    runs_path = matrix_dir / "runs.csv"
    rows = _read_runs_csv(runs_path)
    accepted_target = max(0, int(accepted_target))
    default_attempt_limit = max(max(repeat, 1), accepted_target) + 5 if accepted_target > 0 else max(repeat, 1)
    attempt_limit = max_attempts_per_config if max_attempts_per_config is not None else default_attempt_limit

    index = _existing_index(rows)
    active_session = None
    active_session_dir: Path | None = None
    session_generation = _next_session_generation(matrix_dir)

    def _stop_active_session() -> None:
        nonlocal active_session, active_session_dir
        if active_session is None:
            return
        stop_process(active_session)
        cleanup_residual_processes()
        active_session = None
        active_session_dir = None

    def _ensure_persistent_session():
        nonlocal active_session, active_session_dir, session_generation
        if active_session is not None and active_session_dir is not None:
            return active_session, active_session_dir
        session_generation += 1
        active_session_dir = matrix_dir / "_session" / f"session_{session_generation:02d}"
        active_session_dir.mkdir(parents=True, exist_ok=True)
        cleanup_residual_processes()
        active_session = start_sitl_process(
            active_session_dir.name,
            vehicle,
            frame,
            active_session_dir / "ardupilot_sitl.log",
            enable_visualization=enable_visualization,
        )
        if bool(getattr(getattr(active_session, "visualization", None), "requested", False)):
            active_session = start_visualizer(active_session, "tcp:127.0.0.1:5760")
        return active_session, active_session_dir

    try:
        for config_path in config_paths:
            total_attempt_count, counted_attempt_count, accepted_count = _config_progress(rows, config_path)
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
                config = load_study_config(config_path).with_repeat_index(repeat_index)
                if persistent_session and not skip_sitl:
                    _session, session_dir = _ensure_persistent_session()
                    exit_code, artifact_dir = run_capture(
                        config,
                        vehicle=vehicle,
                        frame=frame,
                        master_uri=str(getattr(_session, "control_master_uri", "tcp:127.0.0.1:5760")),
                        start_sitl=False,
                        owns_session=False,
                        sitl_log_path=session_dir / "ardupilot_sitl.log",
                        enable_visualization=enable_visualization,
                    )
                    if exit_code != 0:
                        _stop_active_session()
                else:
                    session_dir = matrix_dir / f"{index:02d}_{config_path.stem}_r{repeat_index}"
                    session_dir.mkdir(parents=True, exist_ok=True)
                    exit_code, artifact_dir = run_capture(
                        config,
                        vehicle=vehicle,
                        frame=frame,
                        start_sitl=not skip_sitl,
                        owns_session=not skip_sitl,
                        sitl_log_path=session_dir / "ardupilot_sitl.log",
                        enable_visualization=enable_visualization,
                    )
                research_acceptance = _acceptance_state(str(artifact_dir))
                if research_acceptance == "accepted":
                    accepted_count += 1
                row = {
                    "index": str(index),
                    "repeat_index": str(repeat_index),
                    "config": str(config_path.resolve()),
                    "artifact_dir": str(artifact_dir),
                    "status": "completed" if exit_code == 0 else "failed",
                    "exit_code": str(exit_code),
                    "session_dir": str(session_dir),
                    "research_acceptance": research_acceptance,
                    "accepted_count_for_config": str(accepted_count),
                }
                if _row_counts_towards_attempt_budget(row):
                    counted_attempt_count += 1
                rows.append(row)
                if persistent_session and not skip_sitl and _should_restart_persistent_session(row):
                    _stop_active_session()
                _write_runs_csv(runs_path, rows)
    finally:
        _stop_active_session()
    return matrix_dir, rows


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="批量执行 ArduPilot raw linearity capture。")
    parser.add_argument("--config", action="append", dest="configs", help="显式 study config 路径，可重复。")
    parser.add_argument("--pattern", action="append", dest="patterns", help="study config glob，可重复。")
    parser.add_argument("--vehicle", default="ArduCopter")
    parser.add_argument("--frame", default="quad")
    parser.add_argument("--skip-sitl", action="store_true")
    parser.add_argument(
        "--enable-visualization",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="控制 MAVProxy/map 可视化。ArduPilot 默认启用，可用 --no-enable-visualization 显式关闭。",
    )
    parser.add_argument("--repeat", type=int, default=1, help="每个 config fresh 重复次数。")
    parser.add_argument("--accepted-target", type=int, default=0, help="每个 config 需要达到的 accepted raw run 数量。")
    parser.add_argument("--max-attempts-per-config", type=int, default=None, help="accepted-target 模式下每个 config 的最大尝试次数。")
    parser.add_argument("--persistent-session", action="store_true", help="复用单个 ArduPilot SITL 会话执行多个 config。")
    parser.add_argument("--resume-from", type=Path, default=None, help="从已有 matrix 目录继续执行。")
    args = parser.parse_args(argv)

    patterns = tuple(args.patterns or (["*.yaml"] if not args.configs else []))
    configs = _resolve_config_paths(tuple(args.configs or ()), patterns)
    matrix_dir, rows = run_matrix(
        configs,
        vehicle=args.vehicle,
        frame=args.frame,
        skip_sitl=args.skip_sitl,
        repeat=args.repeat,
        accepted_target=args.accepted_target,
        max_attempts_per_config=args.max_attempts_per_config,
        enable_visualization=args.enable_visualization,
        persistent_session=args.persistent_session,
        resume_from=args.resume_from,
    )
    print(f"matrix_dir={matrix_dir}")
    print(f"jobs={len(rows)}")


if __name__ == "__main__":
    main()
