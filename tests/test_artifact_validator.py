from __future__ import annotations

import csv
from pathlib import Path

import yaml

from fep_core.artifact_validator import validate_run_dir
from fep_core.milestone import capability_level, milestone_id, schema_version


def _write_row_csv(path: Path, row: dict[str, object]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)


def _accepted_manifest(run_id: str) -> dict[str, object]:
    return {
        "run_id": run_id,
        "backend": "px4_ros2",
        "schema_version": schema_version(),
        "milestone_id": milestone_id(),
        "capability_level": capability_level(),
        "status": "completed",
        "study": {
            "study_family": "aggressive_input_sensitivity",
            "study_layer": "rate_single_loop",
            "study_role": "primary",
            "oracle_profile": "rate_tracking_v1",
            "mode_under_test": "OFFBOARD_RATE",
            "parameter_group": "roll_rate_pid",
            "parameter_set_name": "baseline",
            "parameter_overrides": {},
            "controlled_parameters": ["MC_ROLLRATE_P"],
            "input_contract": {"signals": ["roll_rate"]},
            "output_contract": {"signals": ["vehicle_rates_setpoint", "vehicle_angular_velocity"]},
            "attribution_boundary": "rate inner-loop",
        },
        "parameter_snapshot_before": {"MC_ROLLRATE_P": 0.15},
        "parameter_snapshot_after": {"MC_ROLLRATE_P": 0.15},
    }


def _accepted_metrics(run_id: str) -> dict[str, object]:
    return {
        "run_id": run_id,
        "backend": "px4_ros2",
        "study_layer": "rate_single_loop",
        "study_role": "primary",
        "mode_under_test": "OFFBOARD_RATE",
        "parameter_group": "roll_rate_pid",
        "parameter_set_name": "baseline",
        "input_chain": "rate",
        "profile_type": "step",
        "axis": "roll",
        "input_peak": 0.1,
        "tracking_error_peak": 0.1,
        "tracking_error_rms": 0.05,
        "response_delay_ms": 10.0,
        "oracle_valid": 1,
        "oracle_failure_reason": "valid",
        "stress_class": "nominal",
        "mechanism_flags": "",
        "rate_layer_recommended": 1,
        "rate_layer_reasons": "study_layer_is_rate_single_loop",
        "attribution_boundary": "rate inner-loop",
    }


def test_validate_run_dir_classifies_accepted_legacy_and_rejected(tmp_path: Path) -> None:
    accepted_dir = tmp_path / "accepted"
    accepted_dir.mkdir()
    (accepted_dir / "manifest.yaml").write_text(yaml.safe_dump(_accepted_manifest("accepted")), encoding="utf-8")
    _write_row_csv(accepted_dir / "metrics.csv", _accepted_metrics("accepted"))

    legacy_dir = tmp_path / "legacy"
    legacy_dir.mkdir()
    legacy_manifest = _accepted_manifest("legacy")
    legacy_manifest.pop("schema_version")
    legacy_manifest.pop("milestone_id")
    (legacy_dir / "manifest.yaml").write_text(yaml.safe_dump(legacy_manifest), encoding="utf-8")
    _write_row_csv(legacy_dir / "metrics.csv", _accepted_metrics("legacy"))

    rejected_dir = tmp_path / "rejected"
    rejected_dir.mkdir()
    (rejected_dir / "manifest.yaml").write_text(yaml.safe_dump(_accepted_manifest("rejected")), encoding="utf-8")
    rejected_metrics = _accepted_metrics("rejected")
    rejected_metrics.pop("oracle_valid")
    _write_row_csv(rejected_dir / "metrics.csv", rejected_metrics)

    accepted = validate_run_dir(accepted_dir, expected_milestone_id=milestone_id(), expected_schema_version=schema_version(), expected_capability_level=capability_level())
    legacy = validate_run_dir(legacy_dir, expected_milestone_id=milestone_id(), expected_schema_version=schema_version(), expected_capability_level=capability_level())
    rejected = validate_run_dir(rejected_dir, expected_milestone_id=milestone_id(), expected_schema_version=schema_version(), expected_capability_level=capability_level())

    assert accepted["classification"] == "accepted"
    assert legacy["classification"] == "legacy"
    assert legacy["reason"] == "missing_schema_or_milestone"
    assert rejected["classification"] == "rejected"
    assert rejected["reason"].startswith("missing_metrics_keys:")


def test_validate_run_dir_rejects_non_completed_status(tmp_path: Path) -> None:
    run_dir = tmp_path / "invalid_runtime"
    run_dir.mkdir()

    manifest = _accepted_manifest("invalid_runtime")
    manifest["status"] = "invalid_runtime"
    (run_dir / "manifest.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    _write_row_csv(run_dir / "metrics.csv", _accepted_metrics("invalid_runtime"))

    result = validate_run_dir(
        run_dir,
        expected_milestone_id=milestone_id(),
        expected_schema_version=schema_version(),
        expected_capability_level=capability_level(),
    )

    assert result["classification"] == "rejected"
    assert result["reason"] == "run_status:invalid_runtime"
