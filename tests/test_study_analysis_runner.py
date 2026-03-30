from __future__ import annotations

import csv
from pathlib import Path

import yaml

from fep_core.milestone import capability_level, milestone_id, schema_version
from fep_core.study_analysis_runner import run_study_analysis


def _write_row_csv(path: Path, row: dict[str, object]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)


def _write_run(run_dir: Path, *, include_schema: bool) -> None:
    manifest = {
        "run_id": run_dir.name,
        "backend": "px4_ros2",
        "status": "completed",
        "study": {
            "study_family": "aggressive_input_sensitivity",
            "study_layer": "manual_whole_loop",
            "study_role": "primary",
            "oracle_profile": "manual_whole_loop_v1",
            "mode_under_test": "POSCTL",
            "parameter_group": "roll_rate_pid",
            "parameter_set_name": "baseline",
            "parameter_overrides": {},
            "controlled_parameters": ["MC_ROLLRATE_P"],
            "input_contract": {"signals": ["roll"]},
            "output_contract": {"signals": ["vehicle_attitude"]},
            "attribution_boundary": "manual whole loop",
        },
        "parameter_snapshot_before": {"MC_ROLLRATE_P": 0.15},
        "parameter_snapshot_after": {"MC_ROLLRATE_P": 0.15},
    }
    if include_schema:
        manifest["schema_version"] = schema_version()
        manifest["milestone_id"] = milestone_id()
        manifest["capability_level"] = capability_level()
    (run_dir / "manifest.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    _write_row_csv(
        run_dir / "metrics.csv",
        {
            "run_id": run_dir.name,
            "backend": "px4_ros2",
            "study_layer": "manual_whole_loop",
            "study_role": "primary",
            "mode_under_test": "POSCTL",
            "parameter_group": "roll_rate_pid",
            "parameter_set_name": "baseline",
            "input_chain": "manual",
            "profile_type": "step",
            "axis": "roll",
            "input_peak": 0.2,
            "tracking_error_peak": 0.0,
            "tracking_error_rms": 0.0,
            "response_delay_ms": 5.0,
            "oracle_valid": 1,
            "oracle_failure_reason": "valid",
            "stress_class": "nominal",
            "mechanism_flags": "",
            "rate_layer_recommended": 0,
            "rate_layer_reasons": "",
            "attribution_boundary": "manual whole loop",
        },
    )


def test_run_study_analysis_filters_legacy_by_default(tmp_path: Path) -> None:
    run_root = tmp_path / "runs"
    run_root.mkdir()
    accepted_dir = run_root / "accepted"
    accepted_dir.mkdir()
    _write_run(accepted_dir, include_schema=True)

    legacy_dir = run_root / "legacy"
    legacy_dir.mkdir()
    _write_run(legacy_dir, include_schema=False)

    output_root = tmp_path / "studies"
    strict_dir = run_study_analysis([run_root], output_root=output_root, include_legacy=False)
    accepted_rows = list(csv.DictReader((strict_dir / "tables" / "accepted_runs.csv").open("r", encoding="utf-8")))
    rejected_rows = list(csv.DictReader((strict_dir / "tables" / "rejected_runs.csv").open("r", encoding="utf-8")))
    assert [row["run_id"] for row in accepted_rows] == ["accepted"]
    assert [row["classification"] for row in rejected_rows] == ["legacy"]

    include_legacy_dir = run_study_analysis([run_root], output_root=output_root, include_legacy=True)
    accepted_with_legacy = list(csv.DictReader((include_legacy_dir / "tables" / "accepted_runs.csv").open("r", encoding="utf-8")))
    assert {row["run_id"] for row in accepted_with_legacy} == {"accepted", "legacy"}
