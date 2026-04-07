from __future__ import annotations

import argparse
from pathlib import Path

from linearity_core.config import load_ablation_plan, load_study_config

from .linearity_analyze import _load_run_dirs, run_analysis


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="按 ablation plan 比较多个 X-schema 与 Y-schema。")
    parser.add_argument("--config", type=Path, required=True, help="study config YAML 路径。")
    parser.add_argument("--plan", type=Path, required=True, help="ablation plan YAML 路径。")
    parser.add_argument("--run-dir", action="append", dest="run_dirs", help="raw run 目录，可重复。")
    parser.add_argument("--study-dir", type=Path, help="包含多个 raw run 子目录的目录。")
    parser.add_argument("--runs-manifest", type=Path, help="CSV manifest；至少包含 run_dir 列。")
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args(argv)

    config = load_study_config(args.config)
    plan = load_ablation_plan(args.plan)
    run_dirs = _load_run_dirs(args)
    if not run_dirs and plan.run_dirs:
        run_dirs = [Path(item).expanduser().resolve() for item in plan.run_dirs]
    study_dir = run_analysis(run_dirs, config, ablation_plan=plan, output_root=args.output_root)
    print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
