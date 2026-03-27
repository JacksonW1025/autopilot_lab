from __future__ import annotations

import argparse
import csv
from pathlib import Path

import yaml
from fep_core.paths import ARDUPILOT_RUNS_ROOT


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

        changed = False
        if manifest.get("backend") != "ardupilot_mavlink":
            manifest["backend"] = "ardupilot_mavlink"
            changed = True
        manifest.setdefault("ardupilot_tlog_path", str(run_dir / "telemetry" / "ardupilot.tlog"))
        manifest.setdefault("ardupilot_bin_log_path", manifest.get("ardupilot_bin_log_path"))
        if changed:
            manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")

        if "backend" not in fieldnames:
            fieldnames.insert(1, "backend")
            for row in rows:
                row["backend"] = "ardupilot_mavlink"
            with metrics_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            changed = True

        if changed:
            updated += 1
        else:
            skipped += 1
    return updated, skipped


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Backfill ArduPilot backend metadata into run artifacts.")
    parser.add_argument("--artifact-root", type=Path, default=ARDUPILOT_RUNS_ROOT)
    args = parser.parse_args(argv)
    updated, skipped = backfill_runs(args.artifact_root)
    print(f"updated={updated}")
    print(f"skipped={skipped}")


if __name__ == "__main__":
    main()
