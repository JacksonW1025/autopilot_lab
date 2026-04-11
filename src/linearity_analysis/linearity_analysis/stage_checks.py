from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

from linearity_core.io import read_yaml
from linearity_core.paths import STUDY_ARTIFACT_ROOT
from linearity_core.study_artifacts import NONZERO_GATE_REASON, _load_diagnostic_gate

BASELINE_REQUIRED_PATHS = [
    "prepared/sample_table.csv",
    "reports/summary.md",
    "reports/baseline_stability.md",
    "reports/matrix_gallery.md",
    "summary/study_summary.json",
    "summary/matrix_gallery.json",
]
DIAGNOSTIC_REQUIRED_PATHS = [
    "prepared/sample_table.csv",
    "reports/summary.md",
    "reports/diagnostic_gate.md",
    "reports/matrix_gallery.md",
    "summary/study_summary.json",
    "summary/diagnostic_gate.json",
    "summary/matrix_gallery.json",
]
PARTIAL_BASELINE_STUDY_NAME = "ardupilot_stabilize_partial_baseline"
PARTIAL_THROTTLE_DIAGNOSTIC_STUDY_NAME = "ardupilot_diagnostic_stabilize_throttle"
ARDUPILOT_FULL_BASELINE_STUDY_NAME = "ardupilot_real_broad_ablation"
ARDUPILOT_FULL_DIAGNOSTIC_STUDY_NAME = "ardupilot_diagnostic_axis_matrix_balanced"
PX4_FULL_BASELINE_STUDY_NAME = "px4_real_broad_ablation"
PX4_FULL_DIAGNOSTIC_STUDY_NAME = "px4_diagnostic_axis_matrix_balanced"


def _read_runs_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _accepted_count_for_config(rows: list[dict[str, str]], config_name: str) -> int:
    matching = [row for row in rows if Path(row.get("config", "")).name == config_name]
    if not matching:
        return 0
    return max(int(row.get("accepted_count_for_config", "0") or 0) for row in matching)


def _attempt_count_for_config(rows: list[dict[str, str]], config_name: str) -> int:
    return sum(1 for row in rows if Path(row.get("config", "")).name == config_name)


def _missing_paths(base_dir: Path, required_paths: list[str]) -> list[str]:
    return [relative_path for relative_path in required_paths if not (base_dir / relative_path).exists()]


def _study_acceptance_count(study_dir: Path) -> int:
    inventory_path = study_dir / "prepared" / "schema_inventory.yaml"
    if not inventory_path.exists():
        return 0
    inventory = read_yaml(inventory_path)
    return int(inventory.get("data_quality", {}).get("accepted_run_count", inventory.get("run_count", 0)) or 0)


def latest_study_dir_by_name(study_name: str) -> Path | None:
    candidates: list[Path] = []
    for candidate in sorted(STUDY_ARTIFACT_ROOT.glob(f"*_{study_name}")):
        manifest_path = candidate / "manifest.yaml"
        if not manifest_path.exists():
            continue
        manifest = read_yaml(manifest_path)
        if str(manifest.get("study_name", "")).strip() != study_name:
            continue
        candidates.append(candidate)
    return candidates[-1] if candidates else None


def validate_matrix_targets(matrix_dir: Path, expected_targets: dict[str, int]) -> dict[str, Any]:
    runs_path = matrix_dir / "runs.csv"
    if not runs_path.exists():
        return {
            "ok": False,
            "reason": "runs_csv_missing",
            "missing_configs": sorted(expected_targets.keys()),
        }
    rows = _read_runs_csv(runs_path)
    configs: list[dict[str, Any]] = []
    failures: list[str] = []
    for config_name, target in sorted(expected_targets.items()):
        accepted = _accepted_count_for_config(rows, config_name)
        attempts = _attempt_count_for_config(rows, config_name)
        configs.append(
            {
                "config_name": config_name,
                "accepted_count": accepted,
                "attempt_count": attempts,
                "target": target,
            }
        )
        if accepted < target:
            failures.append(f"{config_name}:accepted={accepted},target={target},attempts={attempts}")
    return {
        "ok": not failures,
        "reason": "" if not failures else "accepted_target_not_met",
        "configs": configs,
        "failures": failures,
    }


def validate_study_artifact(study_dir: Path, required_paths: list[str]) -> dict[str, Any]:
    missing = _missing_paths(study_dir, required_paths)
    return {
        "ok": not missing,
        "study_dir": str(study_dir),
        "missing_paths": missing,
    }


def validate_diagnostic_gate_clear(
    study_dir: Path,
    *,
    blocking_reason: str = NONZERO_GATE_REASON,
) -> dict[str, Any]:
    payload = _load_diagnostic_gate(study_dir)
    diagnostic_status = str(payload.get("status", "diagnostic_unavailable"))
    throttle_sections = list(payload.get("throttle", []) or [])
    blocked_sections = [
        {
            "mode": section.get("mode", ""),
            "axis": section.get("axis", ""),
            "first_problem_tier": section.get("first_problem_tier", "none"),
            "dominant_rejection_reasons": list(section.get("dominant_rejection_reasons", []) or []),
        }
        for section in throttle_sections
        if blocking_reason in list(section.get("dominant_rejection_reasons", []) or [])
    ]
    if diagnostic_status != "diagnostic_available":
        conclusion = "diagnostic gate artifact is unavailable, so throttle gate cannot be cleared."
    elif blocked_sections:
        conclusion = "当前 dedicated pulse_train 仍不足以解锁 ArduPilot throttle 研究。"
    else:
        conclusion = "当前 dedicated pulse_train 已经摆脱 insufficient_active_nonzero_command_samples gate。"
    return {
        "ok": diagnostic_status == "diagnostic_available" and not blocked_sections,
        "study_dir": str(study_dir),
        "diagnostic_status": diagnostic_status,
        "blocked_sections": blocked_sections,
        "conclusion": conclusion,
    }


def validate_full_matrix_prerequisites() -> dict[str, Any]:
    partial_baseline_dir = latest_study_dir_by_name(PARTIAL_BASELINE_STUDY_NAME)
    throttle_dir = latest_study_dir_by_name(PARTIAL_THROTTLE_DIAGNOSTIC_STUDY_NAME)
    failures: list[str] = []

    partial_baseline = {
        "study_dir": str(partial_baseline_dir) if partial_baseline_dir else "",
        "accepted_run_count": 0,
        "required_paths_ok": False,
    }
    if partial_baseline_dir is None:
        failures.append("partial_baseline_missing")
    else:
        partial_baseline["accepted_run_count"] = _study_acceptance_count(partial_baseline_dir)
        partial_artifact = validate_study_artifact(partial_baseline_dir, BASELINE_REQUIRED_PATHS)
        partial_baseline["required_paths_ok"] = partial_artifact["ok"]
        partial_baseline["missing_paths"] = partial_artifact["missing_paths"]
        if partial_baseline["accepted_run_count"] < 5:
            failures.append("partial_baseline_accepted_target_not_met")
        if not partial_artifact["ok"]:
            failures.append("partial_baseline_artifact_incomplete")

    throttle = {
        "study_dir": str(throttle_dir) if throttle_dir else "",
        "required_paths_ok": False,
        "gate_clear": False,
    }
    if throttle_dir is None:
        failures.append("stabilize_throttle_diagnostic_missing")
    else:
        diagnostic_artifact = validate_study_artifact(throttle_dir, DIAGNOSTIC_REQUIRED_PATHS)
        throttle["required_paths_ok"] = diagnostic_artifact["ok"]
        throttle["missing_paths"] = diagnostic_artifact["missing_paths"]
        gate_check = validate_diagnostic_gate_clear(throttle_dir)
        throttle["gate_clear"] = gate_check["ok"]
        throttle["blocked_sections"] = gate_check["blocked_sections"]
        throttle["conclusion"] = gate_check["conclusion"]
        if not diagnostic_artifact["ok"]:
            failures.append("stabilize_throttle_diagnostic_artifact_incomplete")
        if not gate_check["ok"]:
            failures.append("stabilize_throttle_nonzero_gate_still_blocked")

    return {
        "ok": not failures,
        "failures": failures,
        "partial_baseline": partial_baseline,
        "throttle": throttle,
    }


def validate_final_compare_inputs() -> dict[str, Any]:
    px4_baseline_dir = latest_study_dir_by_name(PX4_FULL_BASELINE_STUDY_NAME)
    ardupilot_baseline_dir = latest_study_dir_by_name(ARDUPILOT_FULL_BASELINE_STUDY_NAME)
    px4_diagnostic_dir = latest_study_dir_by_name(PX4_FULL_DIAGNOSTIC_STUDY_NAME)
    ardupilot_diagnostic_dir = latest_study_dir_by_name(ARDUPILOT_FULL_DIAGNOSTIC_STUDY_NAME)

    failures: list[str] = []
    result = {
        "px4_baseline_dir": str(px4_baseline_dir) if px4_baseline_dir else "",
        "ardupilot_baseline_dir": str(ardupilot_baseline_dir) if ardupilot_baseline_dir else "",
        "px4_diagnostic_dir": str(px4_diagnostic_dir) if px4_diagnostic_dir else "",
        "ardupilot_diagnostic_dir": str(ardupilot_diagnostic_dir) if ardupilot_diagnostic_dir else "",
    }
    if px4_baseline_dir is None:
        failures.append("px4_baseline_missing")
    if ardupilot_baseline_dir is None:
        failures.append("ardupilot_baseline_missing")
    if px4_diagnostic_dir is None:
        failures.append("px4_diagnostic_missing")
    if ardupilot_diagnostic_dir is None:
        failures.append("ardupilot_diagnostic_missing")
    if px4_baseline_dir is not None:
        baseline_check = validate_study_artifact(px4_baseline_dir, BASELINE_REQUIRED_PATHS)
        if not baseline_check["ok"]:
            failures.append("px4_baseline_artifact_incomplete")
    if ardupilot_baseline_dir is not None:
        baseline_check = validate_study_artifact(ardupilot_baseline_dir, BASELINE_REQUIRED_PATHS)
        if not baseline_check["ok"]:
            failures.append("ardupilot_baseline_artifact_incomplete")
    if px4_diagnostic_dir is not None:
        diagnostic_check = validate_study_artifact(px4_diagnostic_dir, DIAGNOSTIC_REQUIRED_PATHS)
        if not diagnostic_check["ok"]:
            failures.append("px4_diagnostic_artifact_incomplete")
    if ardupilot_diagnostic_dir is not None:
        diagnostic_check = validate_study_artifact(ardupilot_diagnostic_dir, DIAGNOSTIC_REQUIRED_PATHS)
        if not diagnostic_check["ok"]:
            failures.append("ardupilot_diagnostic_artifact_incomplete")
    return {
        "ok": not failures,
        "failures": failures,
        **result,
    }


def _main_partial_baseline(args: argparse.Namespace) -> int:
    matrix_check = validate_matrix_targets(args.matrix_dir, {args.config_name: args.accepted_target})
    study_check = validate_study_artifact(args.study_dir, BASELINE_REQUIRED_PATHS)
    ok = matrix_check["ok"] and study_check["ok"]
    if not ok:
        print(f"stage_check=failed")
        for failure in matrix_check.get("failures", []):
            print(f"failure={failure}")
        for missing in study_check.get("missing_paths", []):
            print(f"missing_path={missing}")
        return 1
    print("stage_check=ok")
    print(f"study_dir={args.study_dir}")
    return 0


def _main_diagnostic(args: argparse.Namespace) -> int:
    study_check = validate_study_artifact(args.study_dir, DIAGNOSTIC_REQUIRED_PATHS)
    gate_check = validate_diagnostic_gate_clear(args.study_dir)
    ok = study_check["ok"] and gate_check["ok"]
    if not ok:
        print("stage_check=failed")
        for missing in study_check.get("missing_paths", []):
            print(f"missing_path={missing}")
        for section in gate_check.get("blocked_sections", []):
            print(
                "blocked_section="
                f"{section['mode']}:{section['axis']}:{section['first_problem_tier']}:{','.join(section['dominant_rejection_reasons'])}"
            )
        print(f"conclusion={gate_check['conclusion']}")
        return 1
    print("stage_check=ok")
    print(f"conclusion={gate_check['conclusion']}")
    return 0


def _main_diagnostic_artifact(args: argparse.Namespace) -> int:
    study_check = validate_study_artifact(args.study_dir, DIAGNOSTIC_REQUIRED_PATHS)
    if not study_check["ok"]:
        print("stage_check=failed")
        for missing in study_check.get("missing_paths", []):
            print(f"missing_path={missing}")
        return 1
    print("stage_check=ok")
    return 0


def _main_matrix_targets(args: argparse.Namespace) -> int:
    target_map = {config_name: args.accepted_target for config_name in args.config_names}
    matrix_check = validate_matrix_targets(args.matrix_dir, target_map)
    if not matrix_check["ok"]:
        print("stage_check=failed")
        for failure in matrix_check.get("failures", []):
            print(f"failure={failure}")
        return 1
    print("stage_check=ok")
    return 0


def _main_artifact_paths(args: argparse.Namespace) -> int:
    required_paths = list(args.required_paths or [])
    study_check = validate_study_artifact(args.study_dir, required_paths)
    if not study_check["ok"]:
        print("stage_check=failed")
        for missing in study_check.get("missing_paths", []):
            print(f"missing_path={missing}")
        return 1
    print("stage_check=ok")
    return 0


def _main_full_prereq(_args: argparse.Namespace) -> int:
    payload = validate_full_matrix_prerequisites()
    if not payload["ok"]:
        print("stage_check=failed")
        for failure in payload["failures"]:
            print(f"failure={failure}")
        if payload["throttle"].get("conclusion"):
            print(f"conclusion={payload['throttle']['conclusion']}")
        return 1
    print("stage_check=ok")
    return 0


def _main_full_baseline(args: argparse.Namespace) -> int:
    target_map = {config_name: args.accepted_target for config_name in args.config_names}
    matrix_check = validate_matrix_targets(args.matrix_dir, target_map)
    required_paths = [*BASELINE_REQUIRED_PATHS, *(args.required_paths or [])]
    study_check = validate_study_artifact(args.study_dir, required_paths)
    if not matrix_check["ok"] or not study_check["ok"]:
        print("stage_check=failed")
        for failure in matrix_check.get("failures", []):
            print(f"failure={failure}")
        for missing in study_check.get("missing_paths", []):
            print(f"missing_path={missing}")
        return 1
    print("stage_check=ok")
    return 0


def _main_compare_inputs(_args: argparse.Namespace) -> int:
    payload = validate_final_compare_inputs()
    if not payload["ok"]:
        print("stage_check=failed")
        for failure in payload["failures"]:
            print(f"failure={failure}")
        return 1
    print("stage_check=ok")
    print(f"px4_baseline_dir={payload['px4_baseline_dir']}")
    print(f"ardupilot_baseline_dir={payload['ardupilot_baseline_dir']}")
    print(f"px4_diagnostic_dir={payload['px4_diagnostic_dir']}")
    print(f"ardupilot_diagnostic_dir={payload['ardupilot_diagnostic_dir']}")
    return 0


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Stage gate validators for the ArduPilot/PX4 experiment workflow.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    partial = subparsers.add_parser("partial-baseline")
    partial.add_argument("--matrix-dir", type=Path, required=True)
    partial.add_argument("--study-dir", type=Path, required=True)
    partial.add_argument("--config-name", required=True)
    partial.add_argument("--accepted-target", type=int, required=True)
    partial.set_defaults(handler=_main_partial_baseline)

    diagnostic = subparsers.add_parser("diagnostic")
    diagnostic.add_argument("--study-dir", type=Path, required=True)
    diagnostic.set_defaults(handler=_main_diagnostic)

    diagnostic_artifact = subparsers.add_parser("diagnostic-artifact")
    diagnostic_artifact.add_argument("--study-dir", type=Path, required=True)
    diagnostic_artifact.set_defaults(handler=_main_diagnostic_artifact)

    matrix_targets = subparsers.add_parser("matrix-targets")
    matrix_targets.add_argument("--matrix-dir", type=Path, required=True)
    matrix_targets.add_argument("--config-name", action="append", dest="config_names", required=True)
    matrix_targets.add_argument("--accepted-target", type=int, required=True)
    matrix_targets.set_defaults(handler=_main_matrix_targets)

    artifact_paths = subparsers.add_parser("artifact-paths")
    artifact_paths.add_argument("--study-dir", type=Path, required=True)
    artifact_paths.add_argument("--required-path", action="append", dest="required_paths", required=True)
    artifact_paths.set_defaults(handler=_main_artifact_paths)

    full_prereq = subparsers.add_parser("full-prereq")
    full_prereq.set_defaults(handler=_main_full_prereq)

    full_baseline = subparsers.add_parser("full-baseline")
    full_baseline.add_argument("--matrix-dir", type=Path, required=True)
    full_baseline.add_argument("--study-dir", type=Path, required=True)
    full_baseline.add_argument("--config-name", action="append", dest="config_names", required=True)
    full_baseline.add_argument("--accepted-target", type=int, required=True)
    full_baseline.add_argument("--required-path", action="append", dest="required_paths")
    full_baseline.set_defaults(handler=_main_full_baseline)

    compare_inputs = subparsers.add_parser("compare-inputs")
    compare_inputs.set_defaults(handler=_main_compare_inputs)

    args = parser.parse_args(argv)
    exit_code = args.handler(args)
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
