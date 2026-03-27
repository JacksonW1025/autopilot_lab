from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .io import ensure_study_directories, write_rows_csv, write_yaml
from .paths import ARDUPILOT_RUNS_ROOT, PX4_RUNS_ROOT, STUDY_ARTIFACT_ROOT


def _read_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _read_metrics(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            return dict(row)
    return {}


def _discover_run_dirs(run_roots: list[Path]) -> list[Path]:
    run_dirs: list[Path] = []
    for root in run_roots:
        if not root.exists():
            continue
        run_dirs.extend(sorted(path for path in root.iterdir() if path.is_dir()))
    return run_dirs


def _row_from_run(run_dir: Path) -> dict[str, Any] | None:
    manifest_path = run_dir / "manifest.yaml"
    metrics_path = run_dir / "metrics.csv"
    if not manifest_path.exists() or not metrics_path.exists():
        return None

    manifest = _read_yaml(manifest_path)
    metrics = _read_metrics(metrics_path)
    study = manifest.get("study", {})
    if not isinstance(study, dict):
        study = {}

    return {
        "run_id": str(manifest.get("run_id", run_dir.name)),
        "backend": str(manifest.get("backend", metrics.get("backend", ""))),
        "status": str(manifest.get("status", "")),
        "study_family": str(study.get("study_family", "")),
        "study_layer": str(study.get("study_layer", "")),
        "study_role": str(study.get("study_role", "")),
        "mode_under_test": str(study.get("mode_under_test", "")),
        "parameter_group": str(study.get("parameter_group", "")),
        "parameter_set_name": str(study.get("parameter_set_name", "")),
        "oracle_profile": str(study.get("oracle_profile", "")),
        "oracle_valid": str(metrics.get("oracle_valid", "")),
        "oracle_failure_reason": str(metrics.get("oracle_failure_reason", "")),
        "stress_class": str(metrics.get("stress_class", "")),
        "input_chain": str(manifest.get("input_chain", metrics.get("input_chain", ""))),
        "profile_type": str(manifest.get("profile_type", metrics.get("profile_type", ""))),
        "axis": str(metrics.get("axis", "")),
        "input_peak": str(metrics.get("input_peak", "")),
        "tracking_error_peak": str(metrics.get("tracking_error_peak", "")),
        "tracking_error_rms": str(metrics.get("tracking_error_rms", "")),
        "response_delay_ms": str(metrics.get("response_delay_ms", "")),
        "mechanism_flags": str(metrics.get("mechanism_flags", "")),
        "rate_layer_recommended": str(metrics.get("rate_layer_recommended", "")),
        "rate_layer_reasons": str(metrics.get("rate_layer_reasons", "")),
        "run_dir": str(run_dir),
    }


def _summary_lines(rows: list[dict[str, Any]]) -> list[str]:
    if not rows:
        return ["- 当前没有可汇总的 run。"]

    lines = [f"- 总 run 数: {len(rows)}"]
    by_backend = Counter(row["backend"] for row in rows)
    backend_text = ", ".join(f"{key}={value}" for key, value in sorted(by_backend.items()))
    lines.append(f"- backend 分布: {backend_text}")

    by_layer = Counter(row["study_layer"] for row in rows)
    layer_text = ", ".join(f"{key}={value}" for key, value in sorted(by_layer.items()))
    lines.append(f"- study_layer 分布: {layer_text}")

    valid_counts = Counter((row["study_layer"], row["oracle_valid"]) for row in rows)
    layer_valid_text = []
    for layer in sorted(by_layer):
        valid = valid_counts.get((layer, "1"), 0)
        invalid = valid_counts.get((layer, "0"), 0)
        layer_valid_text.append(f"{layer}: valid={valid}, invalid={invalid}")
    lines.append(f"- oracle 汇总: {'; '.join(layer_valid_text)}")

    by_group: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_group[(row["backend"], row["study_layer"], row["parameter_set_name"])].append(row)

    lines.append("- 代表性分组:")
    for (backend, layer, parameter_set), group_rows in sorted(by_group.items())[:12]:
        status_counter = Counter(row["oracle_valid"] for row in group_rows)
        lines.append(
            f"  - {backend} | {layer} | {parameter_set}: runs={len(group_rows)}, "
            f"valid={status_counter.get('1', 0)}, invalid={status_counter.get('0', 0)}"
        )
    return lines


def run_study_analysis(run_roots: list[Path], output_root: Path = STUDY_ARTIFACT_ROOT) -> Path:
    analysis_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_layered_sensitivity"
    paths = ensure_study_directories(output_root, analysis_id)
    rows = [row for run_dir in _discover_run_dirs(run_roots) if (row := _row_from_run(run_dir)) is not None]
    rows.sort(key=lambda item: (item["study_layer"], item["backend"], item["run_id"]))

    fieldnames = list(rows[0].keys()) if rows else [
        "run_id",
        "backend",
        "status",
        "study_family",
        "study_layer",
        "study_role",
        "mode_under_test",
        "parameter_group",
        "parameter_set_name",
        "oracle_profile",
        "oracle_valid",
        "oracle_failure_reason",
        "stress_class",
        "input_chain",
        "profile_type",
        "axis",
        "input_peak",
        "tracking_error_peak",
        "tracking_error_rms",
        "response_delay_ms",
        "mechanism_flags",
        "rate_layer_recommended",
        "rate_layer_reasons",
        "run_dir",
    ]
    write_rows_csv(paths["tables_dir"] / "merged_runs.csv", rows, fieldnames)

    summary_text = "\n".join(
        [
            f"# Layered Sensitivity Study Summary: {analysis_id}",
            "",
            "## 研究口径",
            "- 本汇总按 `manual_whole_loop`、`attitude_explicit`、`rate_single_loop` 分层，不混合解释。",
            "- 主标签使用 `oracle_valid`，`stress_class` 只作为辅助归因层。",
            "",
            "## 汇总结果",
            *_summary_lines(rows),
        ]
    )
    paths["summary_path"].write_text(summary_text, encoding="utf-8")
    write_yaml(
        paths["manifest_path"],
        {
            "analysis_id": analysis_id,
            "run_roots": [str(path) for path in run_roots],
            "row_count": len(rows),
            "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        },
    )
    return paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="汇总 PX4 与 ArduPilot 的分层敏感性研究 run。")
    parser.add_argument(
        "--run-root",
        action="append",
        dest="run_roots",
        help="Run artifact 根目录；可重复。默认同时读取 PX4 与 ArduPilot。",
    )
    parser.add_argument("--output-root", type=Path, default=STUDY_ARTIFACT_ROOT)
    args = parser.parse_args(argv)

    run_roots = [Path(path).expanduser().resolve() for path in (args.run_roots or [PX4_RUNS_ROOT, ARDUPILOT_RUNS_ROOT])]
    output_dir = run_study_analysis(run_roots, output_root=args.output_root)
    print(f"study_dir={output_dir}")


if __name__ == "__main__":
    main()
