from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import pytest

from linearity_analysis.ardupilot_a2_readiness import (
    _build_aligned_samples,
    _compute_run_effect_metrics,
    main,
    run_ardupilot_a2_readiness,
)
from linearity_core.io import read_yaml, write_yaml


def _write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _write_baseline_study(study_dir: Path, *, sign: float = -0.4) -> None:
    matrix_dir = study_dir / "fits" / "commands_only__actuator_response__pooled" / "ridge_affine"
    matrix_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        matrix_dir / "matrix_f.csv",
        [
            {
                "feature": "command_roll",
                "actuator_1": 0.0,
                "actuator_2": 0.0,
                "actuator_3": 0.0,
                "actuator_4": 0.0,
            },
            {
                "feature": "command_throttle",
                "actuator_1": sign,
                "actuator_2": sign,
                "actuator_3": sign,
                "actuator_4": sign,
            },
        ],
        fieldnames=["feature", "actuator_1", "actuator_2", "actuator_3", "actuator_4"],
    )


def _write_readiness_run(
    run_dir: Path,
    *,
    run_id: str,
    scenario: str,
    tier: str,
    accepted: bool = True,
    completion_reason: str = "profile_completed",
    failsafe: bool = False,
    profile_type: str = "alternating_pulse_train",
    pos_pwm: int = 1300,
    neg_pwm: int = 1500,
) -> None:
    telemetry_dir = run_dir / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    if profile_type == "pulse_train":
        input_rows = [
            {"publish_time_ns": 1_000_000_000, "command_throttle": 0.65, "phase": "stabilize"},
            {"publish_time_ns": 1_100_000_000, "command_throttle": 0.65, "phase": "stabilize"},
            {"publish_time_ns": 1_200_000_000, "command_throttle": 0.65, "phase": "stabilize"},
            {"publish_time_ns": 1_300_000_000, "command_throttle": 0.68, "phase": "pulse_active"},
            {"publish_time_ns": 1_400_000_000, "command_throttle": 0.68, "phase": "pulse_active"},
            {"publish_time_ns": 1_500_000_000, "command_throttle": 0.65, "phase": "pulse_gap"},
            {"publish_time_ns": 1_600_000_000, "command_throttle": 0.65, "phase": "pulse_gap"},
            {"publish_time_ns": 1_700_000_000, "command_throttle": 0.68, "phase": "pulse_active"},
            {"publish_time_ns": 1_800_000_000, "command_throttle": 0.68, "phase": "pulse_active"},
            {"publish_time_ns": 1_900_000_000, "command_throttle": 0.65, "phase": "recover"},
            {"publish_time_ns": 2_000_000_000, "command_throttle": 0.65, "phase": "recover"},
        ]
    else:
        input_rows = [
            {"publish_time_ns": 1_000_000_000, "command_throttle": 0.65, "phase": "stabilize"},
            {"publish_time_ns": 1_100_000_000, "command_throttle": 0.65, "phase": "stabilize"},
            {"publish_time_ns": 1_200_000_000, "command_throttle": 0.65, "phase": "stabilize"},
            {"publish_time_ns": 1_300_000_000, "command_throttle": 0.68, "phase": "alternating_pulse_active_pos"},
            {"publish_time_ns": 1_400_000_000, "command_throttle": 0.68, "phase": "alternating_pulse_active_pos"},
            {"publish_time_ns": 1_500_000_000, "command_throttle": 0.65, "phase": "pulse_gap"},
            {"publish_time_ns": 1_600_000_000, "command_throttle": 0.65, "phase": "pulse_gap"},
            {"publish_time_ns": 1_700_000_000, "command_throttle": 0.62, "phase": "alternating_pulse_active_neg"},
            {"publish_time_ns": 1_800_000_000, "command_throttle": 0.62, "phase": "alternating_pulse_active_neg"},
            {"publish_time_ns": 1_900_000_000, "command_throttle": 0.65, "phase": "recover"},
            {"publish_time_ns": 2_000_000_000, "command_throttle": 0.65, "phase": "recover"},
        ]
    _write_csv(
        telemetry_dir / "input_trace.csv",
        [
            {
                "publish_time_ns": row["publish_time_ns"],
                "elapsed_s": (row["publish_time_ns"] - input_rows[0]["publish_time_ns"]) / 1_000_000_000.0,
                "profile_value": 0.0,
                "roll_body": 0.0,
                "pitch_body": 0.0,
                "yaw_body": 0.0,
                "thrust_z": row["command_throttle"],
                "command_roll": 0.0,
                "command_pitch": 0.0,
                "command_yaw": 0.0,
                "command_throttle": row["command_throttle"],
                "phase": row["phase"],
            }
            for row in input_rows
        ],
        fieldnames=[
            "publish_time_ns",
            "elapsed_s",
            "profile_value",
            "roll_body",
            "pitch_body",
            "yaw_body",
            "thrust_z",
            "command_roll",
            "command_pitch",
            "command_yaw",
            "command_throttle",
            "phase",
        ],
    )
    rcou_rows = []
    relative_times = [
        4_000_000_000,
        4_100_000_000,
        4_200_000_000,
        4_300_000_000,
        4_400_000_000,
        4_500_000_000,
        4_600_000_000,
        4_700_000_000,
        4_800_000_000,
        4_900_000_000,
        5_000_000_000,
    ]
    if profile_type == "pulse_train":
        pwm_values = [
            1400,
            1400,
            1405,
            pos_pwm,
            pos_pwm,
            1400,
            1400,
            pos_pwm,
            pos_pwm,
            1400,
            1400,
        ]
    else:
        pwm_values = [
            1400,
            1400,
            1405,
            pos_pwm,
            pos_pwm,
            1400,
            1400,
            neg_pwm,
            neg_pwm,
            1400,
            1400,
        ]
    for received_time_ns, pwm in zip(relative_times, pwm_values, strict=True):
        rcou_rows.append(
            {
                "received_time_ns": received_time_ns,
                "c1": pwm,
                "c2": pwm,
                "c3": pwm,
                "c4": pwm,
                "c5": 0,
                "c6": 0,
                "c7": 0,
                "c8": 0,
            }
        )
    _write_csv(
        telemetry_dir / "bin_rcou.csv",
        rcou_rows,
        fieldnames=["received_time_ns", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"],
    )
    _write_csv(
        telemetry_dir / "bin_att.csv",
        [{"received_time_ns": 4_000_000_000, "roll": 0.0}],
        fieldnames=["received_time_ns", "roll"],
    )
    _write_csv(
        telemetry_dir / "bin_rate.csv",
        [{"received_time_ns": 4_000_000_000, "roll_rate": 0.0}],
        fieldnames=["received_time_ns", "roll_rate"],
    )
    write_yaml(
        run_dir / "manifest.yaml",
        {
            "run_id": run_id,
            "study_name": f"ardupilot_a2_stabilize_readiness_{scenario}_{tier}",
            "scenario": scenario,
            "config_profile": f"ardupilot_a2_stabilize_readiness_{scenario}_{tier}",
            "status": "completed",
            "research_acceptance": "accepted" if accepted else "rejected",
            "research_rejection_reasons": [] if accepted else ["insufficient_active_nonzero_command_samples"],
            "anomaly_summary": [],
            "study_config": {
                "scenario": scenario,
                "reporting": {"max_alignment_error_ms": 150.0},
                "extras": {
                    "amplitude_tier": tier,
                    "readiness_scenario": scenario,
                    "profile_family": profile_type,
                },
            },
            "runtime_report": {
                "completion_reason": completion_reason,
            },
            "data_quality": {
                "acceptance": {
                    "failsafe_during_experiment": failsafe,
                    "accepted": accepted,
                    "rejection_reasons": [] if accepted else ["insufficient_active_nonzero_command_samples"],
                }
            },
            "raw_schema_version": 2,
        },
    )


def test_aligns_relative_bin_timestamps_to_input_trace(tmp_path: Path) -> None:
    run_dir = tmp_path / "raw" / "run_align"
    _write_readiness_run(run_dir, run_id="run_align", scenario="nominal", tier="small")
    manifest = {"study_config": {"reporting": {"max_alignment_error_ms": 150.0}}}

    samples = _build_aligned_samples(run_dir, manifest)

    assert len(samples) == 11
    assert samples[0]["publish_time_ns"] == 1_000_000_000
    assert samples[0]["quality_alignment_actuator_ns"] == pytest.approx(0.0)
    assert samples[0]["actuator_1"] == pytest.approx(0.4)
    assert samples[3]["actuator_1"] == pytest.approx(0.3)


def test_phase_slicing_and_delta_metrics_are_stable(tmp_path: Path) -> None:
    run_dir = tmp_path / "raw" / "run_metrics"
    _write_readiness_run(run_dir, run_id="run_metrics", scenario="nominal", tier="small")
    samples = _build_aligned_samples(run_dir, read_yaml(run_dir / "manifest.yaml"))

    metrics = _compute_run_effect_metrics(samples)

    assert metrics["analysis_status"] == "ok"
    assert metrics["pulse_count_seen"] == 2
    assert metrics["baseline_command_throttle"] == pytest.approx(0.65)
    assert metrics["mean_delta_actuator_pos"] < 0.0
    assert metrics["mean_delta_actuator_neg"] > 0.0
    assert metrics["effect_abs_median"] > 0.0
    assert metrics["slope_median"] < 0.0
    assert metrics["snr"] >= 3.0


def test_pulse_train_single_polarity_uses_delta_u_sign_for_effect_direction(tmp_path: Path) -> None:
    run_dir = tmp_path / "raw" / "run_pulse_train"
    _write_readiness_run(
        run_dir,
        run_id="run_pulse_train",
        scenario="nominal",
        tier="small",
        profile_type="pulse_train",
        pos_pwm=1320,
    )
    samples = _build_aligned_samples(run_dir, read_yaml(run_dir / "manifest.yaml"))

    metrics = _compute_run_effect_metrics(samples)

    assert metrics["analysis_status"] == "ok"
    assert metrics["pulse_count_seen"] == 2
    assert metrics["mean_delta_actuator_pos"] < 0.0
    assert math.isnan(metrics["mean_delta_actuator_neg"])
    assert metrics["effect_abs_median"] > 0.0
    assert metrics["slope_median"] < 0.0


def test_real_nominal_throttle_run_recovers_nonzero_actuator_delta(tmp_path: Path) -> None:
    real_run = Path("/mnt/nvme/autopilot_lab/artifacts/raw/ardupilot/20260413_090727_ardupilot_manual_alternating_pulse_train_throttle_r1")
    if not (real_run / "manifest.yaml").exists():
        pytest.skip("real throttle diagnostic run is not available")

    baseline_dir = tmp_path / "baseline"
    _write_baseline_study(baseline_dir)
    runs_manifest = tmp_path / "runs.csv"
    _write_csv(
        runs_manifest,
        [
            {
                "index": 1,
                "repeat_index": 1,
                "config": "ardupilot_a2_stabilize_readiness_nominal_small.yaml",
                "artifact_dir": str(real_run),
                "status": "completed",
                "exit_code": 0,
                "session_dir": str(tmp_path / "session"),
                "research_acceptance": "accepted",
                "accepted_count_for_config": 1,
            }
        ],
        fieldnames=[
            "index",
            "repeat_index",
            "config",
            "artifact_dir",
            "status",
            "exit_code",
            "session_dir",
            "research_acceptance",
            "accepted_count_for_config",
        ],
    )

    study_dir = run_ardupilot_a2_readiness(
        runs_manifest=runs_manifest,
        baseline_study_dir=baseline_dir,
        output_root=tmp_path / "studies",
    )

    rows = list(csv.DictReader((study_dir / "tables" / "run_level_effects.csv").open("r", encoding="utf-8")))
    assert len(rows) == 1
    assert rows[0]["run_id"] == "20260413_090727_ardupilot_manual_alternating_pulse_train_throttle_r1"
    assert abs(float(rows[0]["mean_delta_actuator_pos"])) > 0.0 or abs(float(rows[0]["mean_delta_actuator_neg"])) > 0.0


def test_readiness_cli_smoke_writes_expected_outputs(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    baseline_dir = tmp_path / "baseline"
    _write_baseline_study(baseline_dir)
    raw_root = tmp_path / "raw"
    run_specs = [
        ("nominal", "small", True, "profile_completed", False, "pulse_train", 1360, 1500),
        ("nominal", "medium", True, "profile_completed", False, "pulse_train", 1320, 1500),
        ("proxy_dynamic", "small", True, "profile_completed", False, "alternating_pulse_train", 1310, 1490),
        ("proxy_dynamic", "medium", True, "profile_completed", False, "alternating_pulse_train", 1270, 1530),
        ("throttle_biased", "small", True, "profile_completed", False, "pulse_train", 1350, 1500),
        ("throttle_biased", "medium", False, "profile_interrupted", False, "pulse_train", 1310, 1500),
    ]
    rows = []
    for index, (scenario, tier, accepted, completion_reason, failsafe, profile_type, pos_pwm, neg_pwm) in enumerate(run_specs, start=1):
        run_dir = raw_root / f"{scenario}_{tier}"
        _write_readiness_run(
            run_dir,
            run_id=f"{scenario}_{tier}",
            scenario=scenario,
            tier=tier,
            accepted=accepted,
            completion_reason=completion_reason,
            failsafe=failsafe,
            profile_type=profile_type,
            pos_pwm=pos_pwm,
            neg_pwm=neg_pwm,
        )
        rows.append(
            {
                "index": index,
                "repeat_index": 1,
                "config": f"ardupilot_a2_stabilize_readiness_{scenario}_{tier}.yaml",
                "artifact_dir": str(run_dir),
                "status": "completed",
                "exit_code": 0,
                "session_dir": str(tmp_path / f"session_{index}"),
                "research_acceptance": "accepted" if accepted else "rejected",
                "accepted_count_for_config": 1 if accepted else 0,
            }
        )
    runs_manifest = tmp_path / "runs.csv"
    _write_csv(
        runs_manifest,
        rows,
        fieldnames=[
            "index",
            "repeat_index",
            "config",
            "artifact_dir",
            "status",
            "exit_code",
            "session_dir",
            "research_acceptance",
            "accepted_count_for_config",
        ],
    )

    main(
        [
            "--runs-manifest",
            str(runs_manifest),
            "--baseline-study-dir",
            str(baseline_dir),
            "--output-root",
            str(tmp_path / "studies"),
        ]
    )
    captured = capsys.readouterr()
    study_dir = Path(captured.out.strip().split("=", 1)[1])

    assert (study_dir / "summary" / "a2_readiness.json").exists()
    assert (study_dir / "reports" / "a2_readiness.md").exists()
    assert (study_dir / "tables" / "run_level_effects.csv").exists()
    assert (study_dir / "tables" / "config_readiness_matrix.csv").exists()

    summary = json.loads((study_dir / "summary" / "a2_readiness.json").read_text(encoding="utf-8"))
    assert "overall_decision" in summary
    assert summary["overall_decision"]["ready_for_attack_v1"] is False


def test_readiness_scopes_summary_to_present_scenarios(tmp_path: Path) -> None:
    baseline_dir = tmp_path / "baseline"
    _write_baseline_study(baseline_dir)
    raw_root = tmp_path / "raw"
    rows = []
    for index, tier in enumerate(("small", "medium"), start=1):
        run_dir = raw_root / f"nominal_{tier}"
        _write_readiness_run(
            run_dir,
            run_id=f"nominal_{tier}",
            scenario="nominal",
            tier=tier,
            profile_type="pulse_train",
            pos_pwm=1360 if tier == "small" else 1320,
        )
        rows.append(
            {
                "index": index,
                "repeat_index": 1,
                "config": f"ardupilot_a2_stabilize_readiness_nominal_{tier}.yaml",
                "artifact_dir": str(run_dir),
                "status": "completed",
                "exit_code": 0,
                "session_dir": str(tmp_path / f"session_{index}"),
                "research_acceptance": "accepted",
                "accepted_count_for_config": 1,
            }
        )
    runs_manifest = tmp_path / "runs.csv"
    _write_csv(
        runs_manifest,
        rows,
        fieldnames=[
            "index",
            "repeat_index",
            "config",
            "artifact_dir",
            "status",
            "exit_code",
            "session_dir",
            "research_acceptance",
            "accepted_count_for_config",
        ],
    )

    study_dir = run_ardupilot_a2_readiness(
        runs_manifest=runs_manifest,
        baseline_study_dir=baseline_dir,
        output_root=tmp_path / "studies",
    )
    summary = json.loads((study_dir / "summary" / "a2_readiness.json").read_text(encoding="utf-8"))

    assert summary["study_scope"]["scenario_scope"] == ["nominal"]
    assert [item["scenario"] for item in summary["config_results"]] == ["nominal"]
