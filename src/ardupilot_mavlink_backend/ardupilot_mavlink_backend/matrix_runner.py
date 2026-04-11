from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

from linearity_core.config import load_study_config
from linearity_core.io import read_yaml
from linearity_core.paths import ARDUPILOT_MATRIX_ROOT, CONFIG_ROOT

from .experiment_runner import run_capture


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
    fieldnames = [
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
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _acceptance_state(artifact_dir: str) -> str:
    if not artifact_dir:
        return ""
    manifest_path = Path(artifact_dir) / "manifest.yaml"
    if not manifest_path.exists():
        return ""
    manifest = read_yaml(manifest_path)
    return str(manifest.get("research_acceptance", "")).strip().lower()


def run_matrix(
    config_paths: list[Path],
    vehicle: str,
    frame: str,
    skip_sitl: bool,
    repeat: int = 1,
    *,
    accepted_target: int = 0,
    max_attempts_per_config: int | None = None,
) -> tuple[Path, list[dict[str, str]]]:
    run_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_ardupilot"
    matrix_dir = ARDUPILOT_MATRIX_ROOT / run_id
    matrix_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    accepted_target = max(0, int(accepted_target))
    default_attempt_limit = max(max(repeat, 1), accepted_target) + 5 if accepted_target > 0 else max(repeat, 1)
    attempt_limit = max_attempts_per_config if max_attempts_per_config is not None else default_attempt_limit

    index = 0
    for config_path in config_paths:
        accepted_count = 0
        attempt_count = 0
        while True:
            if accepted_target > 0:
                if accepted_count >= accepted_target:
                    break
                if attempt_count >= max(attempt_limit, accepted_target):
                    raise RuntimeError(
                        f"{config_path.name} accepted runs不足: expected={accepted_target}, actual={accepted_count}, attempts={attempt_count}"
                    )
            else:
                if attempt_count >= max(repeat, 1):
                    break

            attempt_count += 1
            repeat_index = attempt_count
            index += 1
            config = load_study_config(config_path).with_repeat_index(repeat_index)
            session_dir = matrix_dir / f"{index:02d}_{config_path.stem}_r{repeat_index}"
            session_dir.mkdir(parents=True, exist_ok=True)
            exit_code, artifact_dir = run_capture(
                config,
                vehicle=vehicle,
                frame=frame,
                start_sitl=not skip_sitl,
                sitl_log_path=session_dir / "ardupilot_sitl.log",
            )
            research_acceptance = _acceptance_state(str(artifact_dir))
            if research_acceptance == "accepted":
                accepted_count += 1
            rows.append(
                {
                    "index": str(index),
                    "repeat_index": str(repeat_index),
                    "config": str(config_path),
                    "artifact_dir": str(artifact_dir),
                    "status": "completed" if exit_code == 0 else "failed",
                    "exit_code": str(exit_code),
                    "session_dir": str(session_dir),
                    "research_acceptance": research_acceptance,
                    "accepted_count_for_config": str(accepted_count),
                }
            )
            _write_runs_csv(matrix_dir / "runs.csv", rows)
    return matrix_dir, rows


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="批量执行 ArduPilot raw linearity capture。")
    parser.add_argument("--config", action="append", dest="configs", help="显式 study config 路径，可重复。")
    parser.add_argument("--pattern", action="append", dest="patterns", help="study config glob，可重复。")
    parser.add_argument("--vehicle", default="ArduCopter")
    parser.add_argument("--frame", default="quad")
    parser.add_argument("--skip-sitl", action="store_true")
    parser.add_argument("--repeat", type=int, default=1, help="每个 config fresh 重复次数。")
    parser.add_argument("--accepted-target", type=int, default=0, help="每个 config 需要达到的 accepted raw run 数量。")
    parser.add_argument("--max-attempts-per-config", type=int, default=None, help="accepted-target 模式下每个 config 的最大尝试次数。")
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
    )
    print(f"matrix_dir={matrix_dir}")
    print(f"jobs={len(rows)}")


if __name__ == "__main__":
    main()
