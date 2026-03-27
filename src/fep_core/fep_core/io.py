from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from typing import Any

import yaml


def ensure_run_directories(root: Path, run_id: str) -> dict[str, Path]:
    base_dir = root / run_id
    telemetry_dir = base_dir / "telemetry"
    plots_dir = base_dir / "plots"
    base_dir.mkdir(parents=True, exist_ok=True)
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)
    return {
        "base_dir": base_dir,
        "telemetry_dir": telemetry_dir,
        "plots_dir": plots_dir,
        "manifest_path": base_dir / "manifest.yaml",
        "notes_path": base_dir / "notes.md",
        "metrics_path": base_dir / "metrics.csv",
        "input_trace_path": telemetry_dir / "input_profile.csv",
    }


def capture_host_snapshot() -> dict[str, str]:
    uptime = subprocess.run(["uptime"], check=True, capture_output=True, text=True).stdout.strip()
    loadavg = Path("/proc/loadavg").read_text(encoding="utf-8").strip()
    return {"uptime": uptime, "loadavg": loadavg}


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=True)


def write_single_row_csv(path: Path, row: dict[str, Any], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)


def write_rows_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
