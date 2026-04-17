from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import pytest

import linearity_analysis.ardupilot_a2_pair_target_live_campaign as campaign
import linearity_analysis.ardupilot_a2_pair_target_readiness as pair_readiness
import linearity_analysis.ardupilot_a2_target_scout as target_scout
from linearity_core.io import write_yaml
from tests.support import build_runs_manifest_row, write_a2_target_run, write_runs_manifest


def _parse_key_values(output: str) -> dict[str, str]:
    payload: dict[str, str] = {}
    for line in output.strip().splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", maxsplit=1)
        payload[key.strip()] = value.strip()
    return payload


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _build_ready_artifacts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[Path, Path]:
    monkeypatch.setattr(target_scout, "ACCEPTED_TARGET", 1)
    monkeypatch.setattr(pair_readiness, "ACCEPTED_TARGET", 1)
    rows: list[dict[str, object]] = []
    run_index = 0
    for scenario in ("nominal", "throttle_biased"):
        for tier in ("micro", "probe", "confirm"):
            run_dir = tmp_path / "raw" / f"source_{scenario}_{tier}"
            write_a2_target_run(
                run_dir,
                run_id=f"{scenario}_{tier}",
                scenario=scenario,
                tier=tier,
                baseline_pwm=(1588, 1588, 1588, 1588),
                active_pwm=(1550, 1550, 1350, 1350),
            )
            rows.append(
                build_runs_manifest_row(
                    run_index,
                    artifact_dir=run_dir,
                    config_name=f"ardupilot_a2_target_scout_{scenario}_{tier}.yaml",
                )
            )
            run_index += 1
    runs_manifest = tmp_path / "source_runs.csv"
    write_runs_manifest(runs_manifest, rows)
    studies_root = tmp_path / "studies"
    target_dir = target_scout.run_ardupilot_a2_target_scout(runs_manifest=runs_manifest, output_root=studies_root)
    pair_dir = pair_readiness.run_ardupilot_a2_pair_target_readiness(runs_manifest=runs_manifest, output_root=studies_root)
    return target_dir, pair_dir


def _build_live_matrix_dir(
    base_dir: Path,
    *,
    tier: str,
    baseline_pwm: tuple[int, int, int, int] = (1588, 1588, 1588, 1588),
    active_pwm: tuple[int, int, int, int] = (1550, 1550, 1350, 1350),
    repeats_per_scenario: int = 5,
) -> Path:
    matrix_dir = base_dir / "matrix"
    rows: list[dict[str, object]] = []
    run_index = 0
    for scenario in ("nominal", "throttle_biased"):
        for repeat_index in range(1, repeats_per_scenario + 1):
            run_dir = base_dir / "raw" / f"{scenario}_{repeat_index}"
            write_a2_target_run(
                run_dir,
                run_id=f"{scenario}_{repeat_index}",
                scenario=scenario,
                tier=tier,
                baseline_pwm=baseline_pwm,
                active_pwm=active_pwm,
                study_name_prefix="ardupilot_a2_pair_target_live_campaign",
                config_profile_prefix="ardupilot_a2_pair_target_live_campaign",
            )
            rows.append(
                build_runs_manifest_row(
                    run_index,
                    artifact_dir=run_dir,
                    config_name=f"ardupilot_a2_pair_target_live_campaign_{scenario}_{tier}.yaml",
                    accepted_count_for_config=repeat_index,
                )
            )
            run_index += 1
    write_runs_manifest(matrix_dir / "runs.csv", rows)
    return matrix_dir


def _write_campaign_spec(
    tmp_path: Path,
    *,
    a2_target_scout_dir: Path,
    a2_pair_target_dir: Path,
    matrix_dirs: dict[str, Path] | None = None,
) -> Path:
    phases = [
        {
            "phase_id": "probe_stability_r1",
            "reference_tier": "probe",
            "scenario_scope": "both",
            "direction": "12_gt_34",
            "pulse_amplitude": 0.05,
            "use_canonical_bias_by_scenario": True,
            "pulse_count": 5,
            "pulse_width_s": 0.35,
            "pulse_gap_s": 0.95,
            "accepted_target": 5,
            "max_attempts_per_config": 10,
        },
        {
            "phase_id": "probe_stability_r2",
            "reference_tier": "probe",
            "scenario_scope": "both",
            "direction": "12_gt_34",
            "pulse_amplitude": 0.05,
            "use_canonical_bias_by_scenario": True,
            "pulse_count": 5,
            "pulse_width_s": 0.35,
            "pulse_gap_s": 0.95,
            "accepted_target": 5,
            "max_attempts_per_config": 10,
        },
        {
            "phase_id": "micro_robustness_r1",
            "reference_tier": "micro",
            "scenario_scope": "both",
            "direction": "12_gt_34",
            "pulse_amplitude": 0.02,
            "use_canonical_bias_by_scenario": True,
            "pulse_count": 5,
            "pulse_width_s": 0.35,
            "pulse_gap_s": 0.95,
            "accepted_target": 5,
            "max_attempts_per_config": 10,
        },
        {
            "phase_id": "confirm_robustness_r1",
            "reference_tier": "confirm",
            "scenario_scope": "both",
            "direction": "12_gt_34",
            "pulse_amplitude": 0.10,
            "use_canonical_bias_by_scenario": True,
            "pulse_count": 5,
            "pulse_width_s": 0.35,
            "pulse_gap_s": 0.95,
            "accepted_target": 5,
            "max_attempts_per_config": 10,
        },
    ]
    for phase in phases:
        matrix_dir = None if matrix_dirs is None else matrix_dirs.get(str(phase["phase_id"]))
        if matrix_dir is not None:
            phase["matrix_dir"] = str(matrix_dir)
    spec_path = tmp_path / "campaign.yaml"
    write_yaml(
        spec_path,
        {
            "campaign_name": "test_a2_live_campaign",
            "campaign_version": "v1",
            "a2_target_scout_dir": str(a2_target_scout_dir),
            "a2_pair_target_dir": str(a2_pair_target_dir),
            "phase_order": list(campaign.EXPECTED_PHASE_IDS),
            "phases": phases,
        },
    )
    return spec_path


def _default_algorithm_scenario_results() -> list[dict[str, Any]]:
    return [
        {
            "scenario": "nominal",
            "reference_ready": True,
            "hard_regression": False,
            "soft_regression": False,
            "dominant_direction": "12_gt_34",
            "median_active_pair_rate": 0.20,
            "median_baseline_pair_rate": 0.01,
            "median_pair_specificity": 0.19,
            "median_pair_sign_consistency": 1.0,
            "median_pair_to_collective_ratio": 0.92,
            "pair_tier_range_specificity": 0.00,
            "blocking_reasons": [],
        },
        {
            "scenario": "throttle_biased",
            "reference_ready": True,
            "hard_regression": False,
            "soft_regression": False,
            "dominant_direction": "12_gt_34",
            "median_active_pair_rate": 0.20,
            "median_baseline_pair_rate": 0.01,
            "median_pair_specificity": 0.19,
            "median_pair_sign_consistency": 1.0,
            "median_pair_to_collective_ratio": 0.92,
            "pair_tier_range_specificity": 0.00,
            "blocking_reasons": [],
        },
    ]


def _default_live_scenario_results() -> list[dict[str, Any]]:
    return [
        {
            "scenario": "nominal",
            "live_ready": True,
            "hard_regression": False,
            "soft_regression": False,
            "dominant_direction": "12_gt_34",
            "median_active_pair_rate": 0.20,
            "median_baseline_pair_rate": 0.01,
            "median_pair_specificity": 0.19,
            "median_pair_sign_consistency": 1.0,
            "median_pair_to_collective_ratio": 0.92,
            "pair_tier_range_specificity": 0.00,
            "blocking_reasons": [],
        },
        {
            "scenario": "throttle_biased",
            "live_ready": True,
            "hard_regression": False,
            "soft_regression": False,
            "dominant_direction": "12_gt_34",
            "median_active_pair_rate": 0.20,
            "median_baseline_pair_rate": 0.01,
            "median_pair_specificity": 0.19,
            "median_pair_sign_consistency": 1.0,
            "median_pair_to_collective_ratio": 0.92,
            "pair_tier_range_specificity": 0.00,
            "blocking_reasons": [],
        },
    ]


def _write_algorithm_eval_summary(
    base_dir: Path,
    phase_id: str,
    *,
    offline_ready: bool = True,
    hard: bool = False,
    soft: bool = False,
    recommended_next_step: str = "hold_for_live_eval",
    blocking_reasons: list[str] | None = None,
) -> Path:
    study_dir = base_dir / f"{phase_id}_algorithm_eval"
    summary_dir = study_dir / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "overall_decision": {
            "offline_ready_for_live_eval_v1": offline_ready,
            "live_eval_required": offline_ready,
            "hard_regression_detected": hard,
            "soft_regression_detected": soft,
            "recommended_next_step": recommended_next_step,
        },
        "scenario_results": _default_algorithm_scenario_results(),
        "blocking_reasons": list(blocking_reasons or []),
    }
    (summary_dir / "a2_pair_target_algorithm_evaluation.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return study_dir


def _write_live_eval_summary(
    base_dir: Path,
    phase_id: str,
    *,
    success: bool = True,
    direction: str = "12_gt_34",
    hard: bool = False,
    soft: bool = False,
    blocking_reasons: list[str] | None = None,
) -> Path:
    study_dir = base_dir / f"{phase_id}_live_eval"
    summary_dir = study_dir / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "overall_decision": {
            "live_pair_target_success_v1": success,
            "dominant_direction": direction,
            "hard_regression_detected": hard,
            "soft_regression_detected": soft,
        },
        "scenario_results": _default_live_scenario_results(),
        "blocking_reasons": list(blocking_reasons or []),
    }
    (summary_dir / "a2_pair_target_live_evaluation.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return study_dir


def test_load_campaign_spec_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target_dir, pair_dir = _build_ready_artifacts(tmp_path, monkeypatch)
    matrix_dirs = {
        "probe_stability_r1": _build_live_matrix_dir(tmp_path / "probe_r1", tier="probe"),
        "probe_stability_r2": _build_live_matrix_dir(tmp_path / "probe_r2", tier="probe"),
        "micro_robustness_r1": _build_live_matrix_dir(tmp_path / "micro_r1", tier="micro"),
        "confirm_robustness_r1": _build_live_matrix_dir(tmp_path / "confirm_r1", tier="confirm"),
    }
    spec_path = _write_campaign_spec(
        tmp_path,
        a2_target_scout_dir=target_dir,
        a2_pair_target_dir=pair_dir,
        matrix_dirs=matrix_dirs,
    )

    payload = campaign._load_campaign_spec(spec_path, skip_capture=True)

    assert payload["phase_order"] == list(campaign.EXPECTED_PHASE_IDS)
    assert payload["phases"]["probe_stability_r1"]["matrix_dir"] == matrix_dirs["probe_stability_r1"].resolve()
    assert payload["phases"]["confirm_robustness_r1"]["reference_tier"] == "confirm"


def test_live_campaign_skip_capture_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    target_dir, pair_dir = _build_ready_artifacts(tmp_path, monkeypatch)
    matrix_dirs = {
        "probe_stability_r1": _build_live_matrix_dir(tmp_path / "probe_r1", tier="probe"),
        "probe_stability_r2": _build_live_matrix_dir(tmp_path / "probe_r2", tier="probe"),
        "micro_robustness_r1": _build_live_matrix_dir(tmp_path / "micro_r1", tier="micro"),
        "confirm_robustness_r1": _build_live_matrix_dir(tmp_path / "confirm_r1", tier="confirm"),
    }
    spec_path = _write_campaign_spec(
        tmp_path,
        a2_target_scout_dir=target_dir,
        a2_pair_target_dir=pair_dir,
        matrix_dirs=matrix_dirs,
    )

    campaign.main(
        [
            "--campaign-spec",
            str(spec_path),
            "--skip-smoke",
            "--skip-capture",
            "--output-root",
            str(tmp_path / "campaign"),
        ]
    )
    payload = _parse_key_values(capsys.readouterr().out)
    campaign_dir = Path(payload["campaign_dir"])
    summary = json.loads(
        (campaign_dir / "summary" / "a2_pair_target_live_campaign.json").read_text(encoding="utf-8")
    )

    assert payload["guided_nogps_smoke_passed"] == "skipped"
    assert payload["probe_stability_passed"] == "true"
    assert payload["tier_robustness_passed"] == "true"
    assert payload["ready_for_live_evidence_review_v1"] == "true"
    assert payload["recommended_next_step"] == "publish_live_evidence_review"
    assert [item["phase_id"] for item in summary["phase_results"]] == list(campaign.EXPECTED_PHASE_IDS)
    assert summary["overall_decision"]["dominant_direction_consistent"] is True
    assert summary["overall_decision"]["hard_regression_detected"] is False
    assert (campaign_dir / "reports" / "a2_pair_target_live_campaign.md").exists()
    assert (campaign_dir / "tables" / "campaign_phase_board.csv").exists()
    assert (campaign_dir / "tables" / "campaign_scenario_board.csv").exists()
    assert (campaign_dir / "tables" / "failure_taxonomy.csv").exists()
    assert len(_read_csv_rows(campaign_dir / "tables" / "campaign_phase_board.csv")) == 4
    assert len(_read_csv_rows(campaign_dir / "tables" / "campaign_scenario_board.csv")) == 8


def test_live_campaign_smoke_runs_once_and_phase_order_is_respected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_dir, pair_dir = _build_ready_artifacts(tmp_path, monkeypatch)
    spec_path = _write_campaign_spec(tmp_path, a2_target_scout_dir=target_dir, a2_pair_target_dir=pair_dir)
    smoke_calls: list[str] = []
    algorithm_calls: list[str] = []
    live_calls: list[str] = []

    def _fake_smoke(**kwargs: Any) -> dict[str, Any]:
        smoke_calls.append("smoke")
        return {
            "matrix_dir": tmp_path / "smoke_matrix",
            "payload": {"passed": True},
        }

    def _fake_algorithm_eval(**kwargs: Any) -> Path:
        phase_id = Path(kwargs["output_root"]).parents[0].name
        algorithm_calls.append(phase_id)
        return _write_algorithm_eval_summary(tmp_path / "fake_algo", phase_id)

    def _fake_live_eval(**kwargs: Any) -> dict[str, Any]:
        phase_id = Path(kwargs["output_root"]).parents[0].name
        assert kwargs["skip_smoke"] is True
        live_calls.append(phase_id)
        study_dir = _write_live_eval_summary(tmp_path / "fake_live", phase_id)
        return {"live_evaluation_dir": study_dir}

    monkeypatch.setattr(campaign.live_eval, "_run_guided_mode_smoke", _fake_smoke)
    monkeypatch.setattr(campaign.algorithm_eval, "run_ardupilot_a2_pair_target_algorithm_evaluation", _fake_algorithm_eval)
    monkeypatch.setattr(campaign.live_eval, "run_ardupilot_a2_pair_target_live_evaluation", _fake_live_eval)

    result = campaign.run_ardupilot_a2_pair_target_live_campaign(
        campaign_spec=spec_path,
        output_root=tmp_path / "campaign",
    )

    assert smoke_calls == ["smoke"]
    assert algorithm_calls == list(campaign.EXPECTED_PHASE_IDS)
    assert live_calls == list(campaign.EXPECTED_PHASE_IDS)
    assert result["probe_stability_passed"] is True
    assert result["tier_robustness_passed"] is True


def test_live_campaign_algorithm_eval_failure_blocks_phase_live_eval(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_dir, pair_dir = _build_ready_artifacts(tmp_path, monkeypatch)
    spec_path = _write_campaign_spec(tmp_path, a2_target_scout_dir=target_dir, a2_pair_target_dir=pair_dir)
    live_calls: list[str] = []

    def _fake_algorithm_eval(**kwargs: Any) -> Path:
        phase_id = Path(kwargs["output_root"]).parents[0].name
        if phase_id == "probe_stability_r1":
            return _write_algorithm_eval_summary(
                tmp_path / "fake_algo",
                phase_id,
                offline_ready=True,
                soft=True,
                recommended_next_step="tighten_algorithm_spec",
                blocking_reasons=["soft_regression_specificity_drop"],
            )
        return _write_algorithm_eval_summary(tmp_path / "fake_algo", phase_id)

    def _fake_live_eval(**kwargs: Any) -> dict[str, Any]:
        phase_id = Path(kwargs["output_root"]).parents[0].name
        live_calls.append(phase_id)
        study_dir = _write_live_eval_summary(tmp_path / "fake_live", phase_id)
        return {"live_evaluation_dir": study_dir}

    monkeypatch.setattr(campaign.algorithm_eval, "run_ardupilot_a2_pair_target_algorithm_evaluation", _fake_algorithm_eval)
    monkeypatch.setattr(campaign.live_eval, "run_ardupilot_a2_pair_target_live_evaluation", _fake_live_eval)

    result = campaign.run_ardupilot_a2_pair_target_live_campaign(
        campaign_spec=spec_path,
        skip_smoke=True,
        output_root=tmp_path / "campaign",
    )
    summary = json.loads(
        (Path(result["campaign_dir"]) / "summary" / "a2_pair_target_live_campaign.json").read_text(encoding="utf-8")
    )
    failure_rows = _read_csv_rows(Path(result["campaign_dir"]) / "tables" / "failure_taxonomy.csv")

    assert live_calls == ["probe_stability_r2", "micro_robustness_r1", "confirm_robustness_r1"]
    first_phase = summary["phase_results"][0]
    assert first_phase["algorithm_eval_ready"] is False
    assert first_phase["live_evaluation_dir"] == ""
    assert first_phase["stage_source"] == "algorithm_evaluation"
    assert "algorithm_eval_soft_regression" in first_phase["failure_categories"]
    assert any(row["failure_category"] == "algorithm_eval_soft_regression" for row in failure_rows)


def test_live_campaign_probe_hard_regression_stops_early(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_dir, pair_dir = _build_ready_artifacts(tmp_path, monkeypatch)
    spec_path = _write_campaign_spec(tmp_path, a2_target_scout_dir=target_dir, a2_pair_target_dir=pair_dir)
    algorithm_calls: list[str] = []
    live_calls: list[str] = []

    def _fake_algorithm_eval(**kwargs: Any) -> Path:
        phase_id = Path(kwargs["output_root"]).parents[0].name
        algorithm_calls.append(phase_id)
        if phase_id == "probe_stability_r1":
            return _write_algorithm_eval_summary(
                tmp_path / "fake_algo",
                phase_id,
                offline_ready=False,
                hard=True,
                recommended_next_step="fix_artifact_or_protocol_mismatch",
                blocking_reasons=["pair_readiness_direction_mismatch"],
            )
        return _write_algorithm_eval_summary(tmp_path / "fake_algo", phase_id)

    def _fake_live_eval(**kwargs: Any) -> dict[str, Any]:
        phase_id = Path(kwargs["output_root"]).parents[0].name
        live_calls.append(phase_id)
        study_dir = _write_live_eval_summary(tmp_path / "fake_live", phase_id)
        return {"live_evaluation_dir": study_dir}

    monkeypatch.setattr(campaign.algorithm_eval, "run_ardupilot_a2_pair_target_algorithm_evaluation", _fake_algorithm_eval)
    monkeypatch.setattr(campaign.live_eval, "run_ardupilot_a2_pair_target_live_evaluation", _fake_live_eval)

    result = campaign.run_ardupilot_a2_pair_target_live_campaign(
        campaign_spec=spec_path,
        skip_smoke=True,
        output_root=tmp_path / "campaign",
    )
    summary = json.loads(
        (Path(result["campaign_dir"]) / "summary" / "a2_pair_target_live_campaign.json").read_text(encoding="utf-8")
    )
    failure_rows = _read_csv_rows(Path(result["campaign_dir"]) / "tables" / "failure_taxonomy.csv")

    assert algorithm_calls == ["probe_stability_r1"]
    assert live_calls == []
    assert summary["overall_decision"]["stopped_early"] is True
    assert summary["overall_decision"]["stop_reason"] == "probe_hard_regression"
    assert summary["overall_decision"]["recommended_next_step"] == "rerun_probe_stability"
    assert any(row["stopped_campaign"] == "True" for row in failure_rows)


def test_live_campaign_micro_hard_regression_allows_confirm(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_dir, pair_dir = _build_ready_artifacts(tmp_path, monkeypatch)
    spec_path = _write_campaign_spec(tmp_path, a2_target_scout_dir=target_dir, a2_pair_target_dir=pair_dir)
    live_calls: list[str] = []

    def _fake_algorithm_eval(**kwargs: Any) -> Path:
        phase_id = Path(kwargs["output_root"]).parents[0].name
        return _write_algorithm_eval_summary(tmp_path / "fake_algo", phase_id)

    def _fake_live_eval(**kwargs: Any) -> dict[str, Any]:
        phase_id = Path(kwargs["output_root"]).parents[0].name
        live_calls.append(phase_id)
        if phase_id == "micro_robustness_r1":
            study_dir = _write_live_eval_summary(
                tmp_path / "fake_live",
                phase_id,
                success=False,
                hard=True,
                blocking_reasons=["scenario_threshold_regression:nominal"],
            )
        else:
            study_dir = _write_live_eval_summary(tmp_path / "fake_live", phase_id)
        return {"live_evaluation_dir": study_dir}

    monkeypatch.setattr(campaign.algorithm_eval, "run_ardupilot_a2_pair_target_algorithm_evaluation", _fake_algorithm_eval)
    monkeypatch.setattr(campaign.live_eval, "run_ardupilot_a2_pair_target_live_evaluation", _fake_live_eval)

    result = campaign.run_ardupilot_a2_pair_target_live_campaign(
        campaign_spec=spec_path,
        skip_smoke=True,
        output_root=tmp_path / "campaign",
    )
    summary = json.loads(
        (Path(result["campaign_dir"]) / "summary" / "a2_pair_target_live_campaign.json").read_text(encoding="utf-8")
    )
    failure_rows = _read_csv_rows(Path(result["campaign_dir"]) / "tables" / "failure_taxonomy.csv")

    assert live_calls == list(campaign.EXPECTED_PHASE_IDS)
    assert summary["overall_decision"]["stopped_early"] is False
    assert summary["overall_decision"]["tier_robustness_passed"] is False
    assert summary["overall_decision"]["recommended_next_step"] == "investigate_tier_regression"
    assert any(row["phase_id"] == "micro_robustness_r1" and row["failure_category"] == "live_threshold_regression" for row in failure_rows)


def test_live_campaign_direction_mismatch_stops_immediately(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_dir, pair_dir = _build_ready_artifacts(tmp_path, monkeypatch)
    spec_path = _write_campaign_spec(tmp_path, a2_target_scout_dir=target_dir, a2_pair_target_dir=pair_dir)
    algorithm_calls: list[str] = []
    live_calls: list[str] = []

    def _fake_algorithm_eval(**kwargs: Any) -> Path:
        phase_id = Path(kwargs["output_root"]).parents[0].name
        algorithm_calls.append(phase_id)
        return _write_algorithm_eval_summary(tmp_path / "fake_algo", phase_id)

    def _fake_live_eval(**kwargs: Any) -> dict[str, Any]:
        phase_id = Path(kwargs["output_root"]).parents[0].name
        live_calls.append(phase_id)
        if phase_id == "probe_stability_r1":
            study_dir = _write_live_eval_summary(
                tmp_path / "fake_live",
                phase_id,
                success=False,
                direction="34_gt_12",
                hard=True,
                blocking_reasons=["scenario_direction_mismatch:nominal"],
            )
        else:
            study_dir = _write_live_eval_summary(tmp_path / "fake_live", phase_id)
        return {"live_evaluation_dir": study_dir}

    monkeypatch.setattr(campaign.algorithm_eval, "run_ardupilot_a2_pair_target_algorithm_evaluation", _fake_algorithm_eval)
    monkeypatch.setattr(campaign.live_eval, "run_ardupilot_a2_pair_target_live_evaluation", _fake_live_eval)

    result = campaign.run_ardupilot_a2_pair_target_live_campaign(
        campaign_spec=spec_path,
        skip_smoke=True,
        output_root=tmp_path / "campaign",
    )
    summary = json.loads(
        (Path(result["campaign_dir"]) / "summary" / "a2_pair_target_live_campaign.json").read_text(encoding="utf-8")
    )
    failure_rows = _read_csv_rows(Path(result["campaign_dir"]) / "tables" / "failure_taxonomy.csv")

    assert algorithm_calls == ["probe_stability_r1"]
    assert live_calls == ["probe_stability_r1"]
    assert summary["overall_decision"]["stopped_early"] is True
    assert summary["overall_decision"]["stop_reason"] == "direction_mismatch"
    assert summary["overall_decision"]["recommended_next_step"] == "rerun_probe_stability"
    assert any(row["failure_category"] == "live_direction_mismatch" for row in failure_rows)
