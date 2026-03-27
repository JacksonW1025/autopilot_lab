from __future__ import annotations

import argparse
import csv
from pathlib import Path

from fep_core.paths import PX4_RUNS_ROOT as ARTIFACT_ROOT
import yaml

from .ulog_metrics import summarize_run_ulog


def backfill_runs(artifact_root: Path) -> tuple[int, int]:
    updated = 0
    skipped = 0
    for run_dir in sorted(path for path in artifact_root.iterdir() if path.is_dir()):
        manifest_path = run_dir / "manifest.yaml"
        metrics_path = run_dir / "metrics.csv"
        if not manifest_path.exists() or not metrics_path.exists():
            skipped += 1
            continue

        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            skipped += 1
            continue
        with metrics_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            fieldnames = list(reader.fieldnames or [])
        if not rows:
            skipped += 1
            continue

        ulog_summary = summarize_run_ulog(run_dir, manifest)
        changed = False
        for row in rows:
            for key, value in ulog_summary.items():
                if row.get(key) != value:
                    row[key] = value
                    changed = True

        for field in ("ulog_saturation_metric", "ulog_parse_status"):
            if field not in fieldnames:
                fieldnames.append(field)
                changed = True

        if not changed:
            skipped += 1
            continue

        with metrics_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        updated += 1

    return updated, skipped


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="回填所有历史 run 的 ULog 饱和指标。")
    parser.add_argument("--artifact-root", type=Path, default=ARTIFACT_ROOT)
    args = parser.parse_args(argv)

    updated, skipped = backfill_runs(args.artifact_root)
    print(f"updated={updated}")
    print(f"skipped={skipped}")


if __name__ == "__main__":
    main()
