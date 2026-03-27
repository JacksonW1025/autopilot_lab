from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

from fep_core.config import load_run_config
from fep_core.paths import ARDUPILOT_MATRIX_ROOT, CONFIG_ROOT

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
    fieldnames = ["index", "config", "artifact_dir", "status", "exit_code"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def run_matrix(config_paths: list[Path], vehicle: str, frame: str, skip_sitl: bool) -> tuple[Path, list[dict[str, str]]]:
    run_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_ardupilot"
    matrix_dir = ARDUPILOT_MATRIX_ROOT / run_id
    matrix_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    for index, config_path in enumerate(config_paths, start=1):
        config = load_run_config(config_path)
        exit_code, artifact_dir = run_experiment(config, vehicle=vehicle, frame=frame, start_sitl=not skip_sitl)
        rows.append(
            {
                "index": str(index),
                "config": str(config_path),
                "artifact_dir": str(artifact_dir),
                "status": "completed" if exit_code == 0 else "failed",
                "exit_code": str(exit_code),
            }
        )
        _write_runs_csv(matrix_dir / "runs.csv", rows)
    return matrix_dir, rows


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run a simple ArduPilot config matrix.")
    parser.add_argument("--pattern", action="append", dest="patterns", help="Config glob, repeatable.")
    parser.add_argument("--vehicle", default="ArduCopter")
    parser.add_argument("--frame", default="quad")
    parser.add_argument("--skip-sitl", action="store_true")
    args = parser.parse_args(argv)

    patterns = tuple(args.patterns or ["*.yaml"])
    configs = _discover_configs(patterns)
    matrix_dir, rows = run_matrix(configs, vehicle=args.vehicle, frame=args.frame, skip_sitl=args.skip_sitl)
    print(f"matrix_dir={matrix_dir}")
    print(f"jobs={len(rows)}")


if __name__ == "__main__":
    main()
