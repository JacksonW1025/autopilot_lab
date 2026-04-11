from __future__ import annotations

import json
from pathlib import Path

import linearity_analysis.stage_checks as stage_checks
from linearity_core.io import write_yaml


def _touch(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_baseline_study(root: Path, dirname: str, study_name: str, *, accepted_run_count: int, complete: bool = True) -> Path:
    study_dir = root / dirname
    write_yaml(study_dir / "manifest.yaml", {"study_name": study_name})
    if complete:
        write_yaml(
            study_dir / "prepared" / "schema_inventory.yaml",
            {
                "run_count": accepted_run_count,
                "data_quality": {"accepted_run_count": accepted_run_count},
            },
        )
        _touch(study_dir / "prepared" / "sample_table.csv", "sample_id\n")
        _touch(study_dir / "reports" / "summary.md", "# Summary\n")
        _touch(study_dir / "reports" / "baseline_stability.md", "# Baseline Stability\n")
        _touch(study_dir / "reports" / "matrix_gallery.md", "# Matrix Gallery\n")
        _touch(study_dir / "reports" / "state_evolution_audit.md", "# State-Evolution Audit\n")
        _touch(study_dir / "summary" / "study_summary.json", json.dumps({"best_result": {}, "ranking": []}))
        _touch(study_dir / "summary" / "matrix_gallery.json", json.dumps({"status": "no_supported_results", "entries": []}))
        _touch(study_dir / "summary" / "state_evolution_audit.json", json.dumps({"status": "audit_available", "entries": []}))
    return study_dir


def _write_diagnostic_study(
    root: Path,
    dirname: str,
    study_name: str,
    *,
    diagnostic_payload: dict,
    complete: bool = True,
) -> Path:
    study_dir = root / dirname
    write_yaml(study_dir / "manifest.yaml", {"study_name": study_name})
    if complete:
        _touch(study_dir / "prepared" / "sample_table.csv", "sample_id\n")
        _touch(study_dir / "reports" / "summary.md", "# Summary\n")
        _touch(study_dir / "reports" / "diagnostic_gate.md", "# Diagnostic Gate\n")
        _touch(study_dir / "reports" / "matrix_gallery.md", "# Matrix Gallery\n")
        _touch(study_dir / "summary" / "study_summary.json", json.dumps({"best_result": {}, "ranking": []}))
        _touch(study_dir / "summary" / "diagnostic_gate.json", json.dumps(diagnostic_payload))
        _touch(study_dir / "summary" / "matrix_gallery.json", json.dumps({"status": "no_supported_results", "entries": []}))
    return study_dir


def test_validate_full_matrix_prerequisites_pass(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(stage_checks, "STUDY_ARTIFACT_ROOT", tmp_path)
    _write_baseline_study(
        tmp_path,
        "20260409_100000_ardupilot_stabilize_partial_baseline",
        stage_checks.PARTIAL_BASELINE_STUDY_NAME,
        accepted_run_count=5,
    )
    _write_diagnostic_study(
        tmp_path,
        "20260409_110000_ardupilot_diagnostic_stabilize_throttle",
        stage_checks.PARTIAL_THROTTLE_DIAGNOSTIC_STUDY_NAME,
        diagnostic_payload={
            "status": "diagnostic_available",
            "throttle": [
                {
                    "mode": "STABILIZE",
                    "axis": "throttle",
                    "first_problem_tier": "none",
                    "dominant_rejection_reasons": [],
                }
            ],
        },
    )

    payload = stage_checks.validate_full_matrix_prerequisites()
    assert payload["ok"] is True
    assert payload["partial_baseline"]["accepted_run_count"] == 5
    assert payload["throttle"]["gate_clear"] is True


def test_validate_full_matrix_prerequisites_fails_when_nonzero_gate_remains(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(stage_checks, "STUDY_ARTIFACT_ROOT", tmp_path)
    _write_baseline_study(
        tmp_path,
        "20260409_100000_ardupilot_stabilize_partial_baseline",
        stage_checks.PARTIAL_BASELINE_STUDY_NAME,
        accepted_run_count=5,
    )
    _write_diagnostic_study(
        tmp_path,
        "20260409_110000_ardupilot_diagnostic_stabilize_throttle",
        stage_checks.PARTIAL_THROTTLE_DIAGNOSTIC_STUDY_NAME,
        diagnostic_payload={
            "status": "diagnostic_available",
            "throttle": [
                {
                    "mode": "STABILIZE",
                    "axis": "throttle",
                    "first_problem_tier": "small",
                    "dominant_rejection_reasons": ["insufficient_active_nonzero_command_samples"],
                }
            ],
        },
    )

    payload = stage_checks.validate_full_matrix_prerequisites()
    assert payload["ok"] is False
    assert "stabilize_throttle_nonzero_gate_still_blocked" in payload["failures"]
    assert payload["throttle"]["conclusion"] == "当前 dedicated pulse_train 仍不足以解锁 ArduPilot throttle 研究。"


def test_validate_final_compare_inputs_requires_complete_artifacts(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(stage_checks, "STUDY_ARTIFACT_ROOT", tmp_path)
    _write_baseline_study(
        tmp_path,
        "20260409_120000_px4_real_broad_ablation",
        stage_checks.PX4_FULL_BASELINE_STUDY_NAME,
        accepted_run_count=10,
    )
    _write_baseline_study(
        tmp_path,
        "20260409_130000_ardupilot_real_broad_ablation",
        stage_checks.ARDUPILOT_FULL_BASELINE_STUDY_NAME,
        accepted_run_count=10,
        complete=False,
    )
    _write_diagnostic_study(
        tmp_path,
        "20260409_140000_px4_diagnostic_axis_matrix_balanced",
        stage_checks.PX4_FULL_DIAGNOSTIC_STUDY_NAME,
        diagnostic_payload={"status": "diagnostic_available", "throttle": []},
    )
    _write_diagnostic_study(
        tmp_path,
        "20260409_150000_ardupilot_diagnostic_axis_matrix_balanced",
        stage_checks.ARDUPILOT_FULL_DIAGNOSTIC_STUDY_NAME,
        diagnostic_payload={"status": "diagnostic_available", "throttle": []},
    )

    payload = stage_checks.validate_final_compare_inputs()
    assert payload["ok"] is False
    assert "ardupilot_baseline_artifact_incomplete" in payload["failures"]


def test_full_baseline_stage_check_accepts_extra_required_paths(tmp_path: Path) -> None:
    matrix_dir = tmp_path / "matrix"
    runs_path = matrix_dir / "runs.csv"
    runs_path.parent.mkdir(parents=True, exist_ok=True)
    runs_path.write_text(
        "config,accepted_count_for_config\n"
        "configs/studies/ardupilot_real_nominal_stabilize_capture.yaml,8\n"
        "configs/studies/ardupilot_real_nominal_guided_nogps_capture.yaml,8\n",
        encoding="utf-8",
    )
    study_dir = _write_baseline_study(
        tmp_path,
        "20260409_180000_ardupilot_real_broad_ablation",
        stage_checks.ARDUPILOT_FULL_BASELINE_STUDY_NAME,
        accepted_run_count=16,
    )

    args = type(
        "Args",
        (),
        {
            "matrix_dir": matrix_dir,
            "study_dir": study_dir,
            "config_names": [
                "ardupilot_real_nominal_stabilize_capture.yaml",
                "ardupilot_real_nominal_guided_nogps_capture.yaml",
            ],
            "accepted_target": 8,
            "required_paths": ["reports/state_evolution_audit.md", "summary/state_evolution_audit.json"],
        },
    )()
    assert stage_checks._main_full_baseline(args) == 0


def test_matrix_targets_stage_check_validates_uniform_target(tmp_path: Path) -> None:
    matrix_dir = tmp_path / "matrix"
    runs_path = matrix_dir / "runs.csv"
    runs_path.parent.mkdir(parents=True, exist_ok=True)
    runs_path.write_text(
        "config,accepted_count_for_config\n"
        "configs/studies/px4_real_generalization_posctl_nominal_capture.yaml,3\n"
        "configs/studies/px4_real_generalization_offboard_dynamic_capture.yaml,3\n",
        encoding="utf-8",
    )
    args = type(
        "Args",
        (),
        {
            "matrix_dir": matrix_dir,
            "config_names": [
                "px4_real_generalization_posctl_nominal_capture.yaml",
                "px4_real_generalization_offboard_dynamic_capture.yaml",
            ],
            "accepted_target": 3,
        },
    )()
    assert stage_checks._main_matrix_targets(args) == 0


def test_artifact_paths_stage_check_requires_all_paths(tmp_path: Path) -> None:
    study_dir = tmp_path / "study"
    _touch(study_dir / "reports" / "scenario_generalization.md", "# Scenario Generalization\n")
    _touch(study_dir / "summary" / "scenario_generalization.json", "{}")
    args = type(
        "Args",
        (),
        {
            "study_dir": study_dir,
            "required_paths": [
                "reports/scenario_generalization.md",
                "summary/scenario_generalization.json",
            ],
        },
    )()
    assert stage_checks._main_artifact_paths(args) == 0
