#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
for pkg_src in (
    ROOT_DIR / "src" / "linearity_core",
    ROOT_DIR / "src" / "linearity_analysis",
):
    pkg_text = str(pkg_src)
    if pkg_text not in sys.path:
        sys.path.insert(0, pkg_text)

from linearity_analysis.anchor_deep_dive import DEFAULT_RAW_TOP_K, run_formal_v2_anchor_deep_dive


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Formal V2 anchor deep-dive artifact from canonical studies.")
    parser.add_argument("--px4-baseline", type=Path, default=None)
    parser.add_argument("--px4-diagnostic", type=Path, default=None)
    parser.add_argument("--ardupilot-baseline", type=Path, default=None)
    parser.add_argument("--ardupilot-diagnostic", type=Path, default=None)
    parser.add_argument("--targeted-validation", type=Path, default=None)
    parser.add_argument("--stabilize-baseline", type=Path, default=None)
    parser.add_argument("--stabilize-diagnostic", type=Path, default=None)
    parser.add_argument("--guided-nogps-baseline", type=Path, default=None)
    parser.add_argument("--guided-nogps-diagnostic", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--raw-top-k", type=int, default=DEFAULT_RAW_TOP_K)
    args = parser.parse_args(argv)

    study_dir = run_formal_v2_anchor_deep_dive(
        px4_baseline_dir=args.px4_baseline.expanduser().absolute() if args.px4_baseline else None,
        px4_diagnostic_dir=args.px4_diagnostic.expanduser().absolute() if args.px4_diagnostic else None,
        ardupilot_baseline_dir=args.ardupilot_baseline.expanduser().absolute() if args.ardupilot_baseline else None,
        ardupilot_diagnostic_dir=args.ardupilot_diagnostic.expanduser().absolute() if args.ardupilot_diagnostic else None,
        targeted_validation_dir=args.targeted_validation.expanduser().absolute() if args.targeted_validation else None,
        stabilize_baseline_dir=args.stabilize_baseline.expanduser().absolute() if args.stabilize_baseline else None,
        stabilize_diagnostic_dir=args.stabilize_diagnostic.expanduser().absolute() if args.stabilize_diagnostic else None,
        guided_nogps_baseline_dir=args.guided_nogps_baseline.expanduser().absolute() if args.guided_nogps_baseline else None,
        guided_nogps_diagnostic_dir=args.guided_nogps_diagnostic.expanduser().absolute() if args.guided_nogps_diagnostic else None,
        output_dir=args.output_dir.expanduser().absolute() if args.output_dir else None,
        raw_top_k=args.raw_top_k,
    )
    print(f"study_dir={study_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
