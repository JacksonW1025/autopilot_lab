from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

from fep_core.config import load_run_config
from fep_core.paths import ARDUPILOT_MATRIX_ROOT, CONFIG_ROOT, ARDUPILOT_RUNS_ROOT, PX4_RUNS_ROOT
from fep_core.study_analysis_runner import run_study_analysis

from .experiment_runner import run_experiment


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


def _write_runs_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = ["index", "repeat_index", "config", "artifact_dir", "status", "exit_code", "session_dir"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def run_matrix(
    config_paths: list[Path],
    vehicle: str,
    frame: str,
    skip_sitl: bool,
    repeat: int = 1,
) -> tuple[Path, list[dict[str, str]]]:
    run_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_ardupilot"
    matrix_dir = ARDUPILOT_MATRIX_ROOT / run_id
    matrix_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    jobs = [(config_path, repeat_index) for repeat_index in range(1, max(repeat, 1) + 1) for config_path in config_paths]
    for index, (config_path, repeat_index) in enumerate(jobs, start=1):
        config = load_run_config(config_path)
        suffix = f"_r{repeat_index}" if repeat > 1 else ""
        session_dir = matrix_dir / f"{index:02d}_{config_path.stem}{suffix}"
        session_dir.mkdir(parents=True, exist_ok=True)
        exit_code, artifact_dir = run_experiment(
            config,
            vehicle=vehicle,
            frame=frame,
            start_sitl=not skip_sitl,
            sitl_log_path=session_dir / "ardupilot_sitl.log",
        )
        rows.append(
            {
                "index": str(index),
                "repeat_index": str(repeat_index),
                "config": str(config_path),
                "artifact_dir": str(artifact_dir),
                "status": "completed" if exit_code == 0 else "failed",
                "exit_code": str(exit_code),
                "session_dir": str(session_dir),
            }
        )
        _write_runs_csv(matrix_dir / "runs.csv", rows)
    run_study_analysis([PX4_RUNS_ROOT, ARDUPILOT_RUNS_ROOT])
    return matrix_dir, rows


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="按 fresh/headless 口径批量执行 ArduPilot matrix，并在结束后生成新的分层 study 汇总。")
    parser.add_argument("--pattern", action="append", dest="patterns", help="Config glob, repeatable.")
    parser.add_argument("--vehicle", default="ArduCopter")
    parser.add_argument("--frame", default="quad")
    parser.add_argument("--skip-sitl", action="store_true")
    parser.add_argument("--repeat", type=int, default=1, help="每个 config fresh 重复次数，默认 1。")
    args = parser.parse_args(argv)

    patterns = tuple(args.patterns or ["*.yaml"])
    configs = _discover_configs(patterns)
    matrix_dir, rows = run_matrix(
        configs,
        vehicle=args.vehicle,
        frame=args.frame,
        skip_sitl=args.skip_sitl,
        repeat=args.repeat,
    )
    print(f"matrix_dir={matrix_dir}")
    print(f"jobs={len(rows)}")


if __name__ == "__main__":
    main()
