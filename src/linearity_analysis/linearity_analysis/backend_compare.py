from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from linearity_core.io import ensure_study_directories, write_json, write_yaml
from linearity_core.study_artifacts import build_backend_compare_payload, render_backend_compare_markdown


def run_backend_compare(
    px4_baseline_dir: Path,
    ardupilot_baseline_dir: Path,
    px4_diagnostic_dir: Path,
    ardupilot_diagnostic_dir: Path,
    *,
    output_root: Path | None = None,
) -> Path:
    study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_px4_vs_ardupilot_compare"
    paths = ensure_study_directories(study_id, root=output_root)
    payload = build_backend_compare_payload(
        px4_baseline_dir=px4_baseline_dir,
        ardupilot_baseline_dir=ardupilot_baseline_dir,
        px4_diagnostic_dir=px4_diagnostic_dir,
        ardupilot_diagnostic_dir=ardupilot_diagnostic_dir,
    )
    paths["backend_compare_report_path"].write_text(render_backend_compare_markdown(payload), encoding="utf-8")
    write_json(paths["backend_compare_json_path"], payload)
    write_yaml(
        paths["manifest_path"],
        {
            "study_name": "px4_vs_ardupilot_compare",
            "study_id": study_id,
            "px4_baseline_dir": str(px4_baseline_dir),
            "ardupilot_baseline_dir": str(ardupilot_baseline_dir),
            "px4_diagnostic_dir": str(px4_diagnostic_dir),
            "ardupilot_diagnostic_dir": str(ardupilot_diagnostic_dir),
            "summary": payload,
        },
    )
    return paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build a final PX4 vs ArduPilot comparison artifact from authoritative baseline and diagnostic studies.")
    parser.add_argument("--px4-baseline", type=Path, required=True)
    parser.add_argument("--ardupilot-baseline", type=Path, required=True)
    parser.add_argument("--px4-diagnostic", type=Path, required=True)
    parser.add_argument("--ardupilot-diagnostic", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args(argv)

    study_dir = run_backend_compare(
        px4_baseline_dir=args.px4_baseline.expanduser().resolve(),
        ardupilot_baseline_dir=args.ardupilot_baseline.expanduser().resolve(),
        px4_diagnostic_dir=args.px4_diagnostic.expanduser().resolve(),
        ardupilot_diagnostic_dir=args.ardupilot_diagnostic.expanduser().resolve(),
        output_root=args.output_root.expanduser().resolve() if args.output_root else None,
    )
    print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
