from __future__ import annotations

from pathlib import Path

from linearity_core.io import (
    capture_host_snapshot,
    ensure_raw_run_directories as ensure_backend_run_directories,
    write_rows_csv,
    write_single_row_csv,
    write_yaml,
)
from linearity_core.paths import PX4_LOG_ROOT, PX4_RAW_ROOT as PX4_RUNS_ROOT


def ensure_run_directories(run_id: str) -> dict[str, Path]:
    return ensure_backend_run_directories("px4", run_id, root=PX4_RUNS_ROOT)


def snapshot_ulog_files(log_root: Path = PX4_LOG_ROOT) -> dict[str, float]:
    if not log_root.exists():
        return {}

    files: dict[str, float] = {}
    for path in log_root.rglob("*.ulg"):
        files[str(path)] = path.stat().st_mtime
    return files


def resolve_ulog_path(before: dict[str, float], after: dict[str, float]) -> str | None:
    candidates = [path for path in after if path not in before]
    if not candidates:
        candidates = list(after.keys())
    if not candidates:
        return None
    candidates.sort(key=lambda item: after[item], reverse=True)
    return candidates[0]
