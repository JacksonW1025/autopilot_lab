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

from linearity_analysis.next_phase_decision_layer import run_formal_v2_next_phase_decision_layer


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Formal V2 next-phase decision layer from latest derived artifacts.")
    parser.add_argument("--anchor-deep-dive", type=Path, default=None)
    parser.add_argument("--in-depth-analysis", type=Path, default=None)
    parser.add_argument("--a2-pair-target", type=Path, default=None)
    parser.add_argument("--a1-targeted-reproduction", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args(argv)

    study_dir = run_formal_v2_next_phase_decision_layer(
        anchor_deep_dive_dir=args.anchor_deep_dive.expanduser().resolve() if args.anchor_deep_dive else None,
        in_depth_analysis_dir=args.in_depth_analysis.expanduser().resolve() if args.in_depth_analysis else None,
        a2_pair_target_dir=args.a2_pair_target.expanduser().resolve() if args.a2_pair_target else None,
        a1_targeted_reproduction_dir=(
            args.a1_targeted_reproduction.expanduser().resolve() if args.a1_targeted_reproduction else None
        ),
        output_dir=args.output_dir.expanduser().resolve() if args.output_dir else None,
    )
    print(f"study_dir={study_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
