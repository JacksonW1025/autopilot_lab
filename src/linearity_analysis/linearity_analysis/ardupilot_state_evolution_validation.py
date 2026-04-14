from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from linearity_core.io import ensure_study_directories, write_json, write_yaml
from linearity_core.study_artifacts import (
    build_ardupilot_state_evolution_validation_payload,
    render_ardupilot_state_evolution_validation_markdown,
)


def run_ardupilot_state_evolution_validation(
    *,
    stabilize_baseline_dir: Path,
    stabilize_diagnostic_dir: Path,
    guided_nogps_baseline_dir: Path,
    guided_nogps_diagnostic_dir: Path,
    output_root: Path | None = None,
) -> Path:
    study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_ardupilot_state_evolution_validation"
    paths = ensure_study_directories(study_id, root=output_root)
    payload = build_ardupilot_state_evolution_validation_payload(
        stabilize_baseline_dir=stabilize_baseline_dir,
        stabilize_diagnostic_dir=stabilize_diagnostic_dir,
        guided_nogps_baseline_dir=guided_nogps_baseline_dir,
        guided_nogps_diagnostic_dir=guided_nogps_diagnostic_dir,
    )
    report_path = paths["reports_dir"] / "state_evolution_validation.md"
    summary_path = paths["summary_dir"] / "state_evolution_validation.json"
    report_path.write_text(render_ardupilot_state_evolution_validation_markdown(payload), encoding="utf-8")
    write_json(summary_path, payload)
    write_yaml(
        paths["manifest_path"],
        {
            "study_name": "ardupilot_state_evolution_validation",
            "study_id": study_id,
            "stabilize_baseline_dir": str(stabilize_baseline_dir),
            "stabilize_diagnostic_dir": str(stabilize_diagnostic_dir),
            "guided_nogps_baseline_dir": str(guided_nogps_baseline_dir),
            "guided_nogps_diagnostic_dir": str(guided_nogps_diagnostic_dir),
            "summary": payload,
        },
    )
    return paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build the Formal V2 ArduPilot mode-isolated state-evolution validation artifact.")
    parser.add_argument("--stabilize-baseline", type=Path, required=True)
    parser.add_argument("--stabilize-diagnostic", type=Path, required=True)
    parser.add_argument("--guided-baseline", type=Path, required=True)
    parser.add_argument("--guided-diagnostic", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args(argv)

    study_dir = run_ardupilot_state_evolution_validation(
        stabilize_baseline_dir=args.stabilize_baseline.expanduser().resolve(),
        stabilize_diagnostic_dir=args.stabilize_diagnostic.expanduser().resolve(),
        guided_nogps_baseline_dir=args.guided_baseline.expanduser().resolve(),
        guided_nogps_diagnostic_dir=args.guided_diagnostic.expanduser().resolve(),
        output_root=args.output_root.expanduser().resolve() if args.output_root else None,
    )
    print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
