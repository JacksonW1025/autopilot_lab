from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

import yaml

from .milestone import capability_level, milestone_id, schema_version
from .paths import ARDUPILOT_RUNS_ROOT, PX4_RUNS_ROOT

REQUIRED_MANIFEST_KEYS = (
    "schema_version",
    "milestone_id",
    "capability_level",
    "status",
    "study",
    "parameter_snapshot_before",
    "parameter_snapshot_after",
)
REQUIRED_STUDY_KEYS = (
    "study_family",
    "study_layer",
    "study_role",
    "oracle_profile",
    "mode_under_test",
    "parameter_group",
    "parameter_set_name",
    "parameter_overrides",
    "controlled_parameters",
    "input_contract",
    "output_contract",
    "attribution_boundary",
)
NONEMPTY_STUDY_KEYS = (
    "study_family",
    "study_layer",
    "study_role",
    "oracle_profile",
    "mode_under_test",
    "parameter_group",
    "parameter_set_name",
    "controlled_parameters",
    "input_contract",
    "output_contract",
    "attribution_boundary",
)
REQUIRED_METRIC_KEYS = (
    "study_layer",
    "study_role",
    "mode_under_test",
    "parameter_group",
    "parameter_set_name",
    "oracle_valid",
    "oracle_failure_reason",
    "stress_class",
    "mechanism_flags",
    "rate_layer_recommended",
    "rate_layer_reasons",
    "attribution_boundary",
)
NONEMPTY_METRIC_KEYS = (
    "study_layer",
    "study_role",
    "mode_under_test",
    "parameter_group",
    "parameter_set_name",
    "oracle_valid",
    "oracle_failure_reason",
    "stress_class",
    "rate_layer_recommended",
    "attribution_boundary",
)


def _read_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _read_metrics(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            return dict(row)
    return {}


def validate_run_dir(
    run_dir: Path,
    *,
    expected_milestone_id: str | None = None,
    expected_schema_version: int | None = None,
    expected_capability_level: str | None = None,
) -> dict[str, Any]:
    manifest_path = run_dir / "manifest.yaml"
    metrics_path = run_dir / "metrics.csv"
    result: dict[str, Any] = {
        "run_dir": str(run_dir),
        "run_id": run_dir.name,
        "backend": "",
        "classification": "rejected",
        "reason": "",
    }
    if not manifest_path.exists() or not metrics_path.exists():
        result["reason"] = "missing_manifest_or_metrics"
        return result

    manifest = _read_yaml(manifest_path)
    metrics = _read_metrics(metrics_path)
    result["run_id"] = str(manifest.get("run_id", run_dir.name))
    result["backend"] = str(manifest.get("backend", metrics.get("backend", "")))

    milestone_value = manifest.get("milestone_id")
    schema_value = manifest.get("schema_version")
    capability_value = manifest.get("capability_level")
    if milestone_value in ("", None) or schema_value in ("", None):
        result["classification"] = "legacy"
        result["reason"] = "missing_schema_or_milestone"
        return result

    if expected_milestone_id is not None and str(milestone_value) != expected_milestone_id:
        result["reason"] = f"milestone_mismatch:{milestone_value}"
        return result
    if expected_schema_version is not None and int(schema_value) != int(expected_schema_version):
        result["reason"] = f"schema_version_mismatch:{schema_value}"
        return result
    if expected_capability_level is not None and str(capability_value) != expected_capability_level:
        result["reason"] = f"capability_level_mismatch:{capability_value}"
        return result

    missing_manifest = [key for key in REQUIRED_MANIFEST_KEYS if key not in manifest]
    if missing_manifest:
        result["reason"] = f"missing_manifest_keys:{','.join(missing_manifest)}"
        return result

    run_status = str(manifest.get("status", "")).strip()
    if run_status != "completed":
        result["reason"] = f"run_status:{run_status or 'missing'}"
        return result

    study = manifest.get("study", {})
    if not isinstance(study, dict):
        result["reason"] = "study_not_dict"
        return result

    missing_study = [key for key in REQUIRED_STUDY_KEYS if key not in study]
    if missing_study:
        result["reason"] = f"missing_study_keys:{','.join(missing_study)}"
        return result

    empty_study = [key for key in NONEMPTY_STUDY_KEYS if study.get(key, "") in ("", None, {}, [])]
    if empty_study:
        result["reason"] = f"empty_study_keys:{','.join(empty_study)}"
        return result

    missing_metrics = [key for key in REQUIRED_METRIC_KEYS if key not in metrics]
    if missing_metrics:
        result["reason"] = f"missing_metrics_keys:{','.join(missing_metrics)}"
        return result

    empty_metrics = [key for key in NONEMPTY_METRIC_KEYS if metrics.get(key, "") in ("", None)]
    if empty_metrics:
        result["reason"] = f"empty_metrics_keys:{','.join(empty_metrics)}"
        return result

    result["classification"] = "accepted"
    result["reason"] = "accepted"
    return result


def discover_run_dirs(run_roots: list[Path]) -> list[Path]:
    run_dirs: list[Path] = []
    for root in run_roots:
        if not root.exists():
            continue
        run_dirs.extend(sorted(path for path in root.iterdir() if path.is_dir()))
    return run_dirs


def validate_run_roots(
    run_roots: list[Path],
    *,
    expected_milestone_id: str | None = None,
    expected_schema_version: int | None = None,
    expected_capability_level: str | None = None,
) -> list[dict[str, Any]]:
    return [
        validate_run_dir(
            run_dir,
            expected_milestone_id=expected_milestone_id,
            expected_schema_version=expected_schema_version,
            expected_capability_level=expected_capability_level,
        )
        for run_dir in discover_run_dirs(run_roots)
    ]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="校验实验 run 是否满足当前里程碑 schema。")
    parser.add_argument(
        "--run-root",
        action="append",
        dest="run_roots",
        help="Run artifact 根目录；可重复。默认同时读取 PX4 与 ArduPilot。",
    )
    args = parser.parse_args(argv)

    run_roots = [Path(path).expanduser().resolve() for path in (args.run_roots or [PX4_RUNS_ROOT, ARDUPILOT_RUNS_ROOT])]
    rows = validate_run_roots(
        run_roots,
        expected_milestone_id=milestone_id(),
        expected_schema_version=schema_version(),
        expected_capability_level=capability_level(),
    )
    counts: dict[str, int] = {"accepted": 0, "legacy": 0, "rejected": 0}
    for row in rows:
        counts[row["classification"]] = counts.get(row["classification"], 0) + 1
    print(f"accepted={counts.get('accepted', 0)}")
    print(f"legacy={counts.get('legacy', 0)}")
    print(f"rejected={counts.get('rejected', 0)}")
