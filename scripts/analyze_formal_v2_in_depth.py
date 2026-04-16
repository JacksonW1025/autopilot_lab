#!/usr/bin/env python3
from __future__ import annotations

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

import argparse

from linearity_analysis.in_depth_analysis import DEFAULT_TOP_K, run_formal_v2_in_depth_analysis


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Formal V2 reusable in-depth analysis artifact from canonical studies.")
    parser.add_argument("--px4-baseline", type=Path, default=None)
    parser.add_argument("--px4-diagnostic", type=Path, default=None)
    parser.add_argument("--ardupilot-baseline", type=Path, default=None)
    parser.add_argument("--ardupilot-diagnostic", type=Path, default=None)
    parser.add_argument("--targeted-validation", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    args = parser.parse_args(argv)

    study_dir = run_formal_v2_in_depth_analysis(
        px4_baseline_dir=args.px4_baseline.expanduser().resolve() if args.px4_baseline else None,
        px4_diagnostic_dir=args.px4_diagnostic.expanduser().resolve() if args.px4_diagnostic else None,
        ardupilot_baseline_dir=args.ardupilot_baseline.expanduser().resolve() if args.ardupilot_baseline else None,
        ardupilot_diagnostic_dir=args.ardupilot_diagnostic.expanduser().resolve() if args.ardupilot_diagnostic else None,
        targeted_validation_dir=args.targeted_validation.expanduser().resolve() if args.targeted_validation else None,
        output_dir=args.output_dir.expanduser().resolve() if args.output_dir else None,
        top_k=args.top_k,
    )
    print(f"study_dir={study_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
