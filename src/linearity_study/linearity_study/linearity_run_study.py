from __future__ import annotations

import argparse
import os
from pathlib import Path

from linearity_analysis.linearity_analyze import run_analysis
from linearity_core.config import load_ablation_plan, load_study_config
from linearity_core.synthetic import generate_synthetic_raw_runs


def run_study(config_path: Path, *, output_root: Path | None = None, skip_analysis: bool = False) -> tuple[list[Path], Path | None]:
    config = load_study_config(config_path)
    raw_dirs: list[Path] = []
    if config.backend == "synthetic":
        raw_root = output_root.parent / "raw" if output_root is not None else None
        raw_dirs = generate_synthetic_raw_runs(config, output_root=raw_root)
    elif config.backend == "px4":
        from px4_ros2_backend.linearity_matrix import run_matrix

        world = str(config.extras.get("world", os.environ.get("PX4_GZ_WORLD", "default"))).strip() or "default"
        if config.source_path is None:
            raise ValueError("PX4 study config 必须来自文件路径，才能自动启动可视化会话。")
        _, rows = run_matrix(world, [config.source_path.resolve()], repeat=config.repeat_count)
        raw_dirs = [Path(row["artifact_dir"]) for row in rows if row.get("artifact_dir")]
        failed_rows = [row for row in rows if row.get("status") != "completed"]
        if failed_rows:
            details = ", ".join(
                f"{Path(row['config']).name}: status={row['status']} session={row['session_dir']}"
                for row in failed_rows
            )
            raise RuntimeError(f"PX4 study capture 未全部完成: {details}")
    elif config.backend == "ardupilot":
        from ardupilot_mavlink_backend.linearity_capture import run_capture

        for repeat_index in range(1, config.repeat_count + 1):
            _, raw_dir = run_capture(config.with_repeat_index(repeat_index))
            raw_dirs.append(raw_dir)
    else:
        raise ValueError(f"不支持的 backend: {config.backend}")

    if skip_analysis:
        return raw_dirs, None

    plan = None
    if isinstance(config.ablation_plan, str) and config.ablation_plan:
        plan_path = Path(config.ablation_plan).expanduser()
        if not plan_path.is_absolute() and config.source_path is not None:
            plan_path = (config.source_path.parent / plan_path).resolve()
        plan = load_ablation_plan(plan_path)
    study_dir = run_analysis(raw_dirs, config, ablation_plan=plan, output_root=output_root)
    return raw_dirs, study_dir


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="执行一个全局线性 study：采集 raw run，构造 X/Y，拟合并输出报告。")
    parser.add_argument("--config", type=Path, required=True, help="study config YAML 路径。")
    parser.add_argument("--output-root", type=Path, default=None)
    parser.add_argument("--skip-analysis", action="store_true")
    args = parser.parse_args(argv)

    raw_dirs, study_dir = run_study(args.config, output_root=args.output_root, skip_analysis=args.skip_analysis)
    print("raw_runs=" + ",".join(str(path) for path in raw_dirs))
    if study_dir is not None:
        print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
