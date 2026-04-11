from __future__ import annotations

from pathlib import Path

import pytest

from linearity_core.config import load_ablation_plan, load_study_config
from tests.support import write_synthetic_config


ROOT = Path(__file__).resolve().parents[1]


def test_study_config_parses_new_linearity_fields(tmp_path: Path) -> None:
    config = load_study_config(write_synthetic_config(tmp_path))
    assert config.x_schema == "commands_plus_state"
    assert config.y_schema == "delta_state"
    assert config.research_tier == "authoritative_research"
    assert config.pooling_mode == "compare_both"
    assert config.output_semantics == "future_state"
    assert config.history_length == 3
    assert config.prediction_horizon == 2
    assert config.prediction_horizon_unit == "steps"
    assert config.run_level_covariates_as_inputs is True
    assert "backend" in config.stratify_by
    assert config.backend_mode_covariates == ["backend", "mode", "scenario", "config_profile"]


def test_ablation_plan_parses_schema_lists() -> None:
    plan = load_ablation_plan(ROOT / "configs/ablations/default_schema_ablation.yaml")
    assert "commands_only" in plan.x_schemas
    assert "delta_state" in plan.y_schemas
    assert "pooled" in plan.pooling_modes
    assert "stratified" in plan.pooling_modes


def test_invalid_prediction_unit_raises(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text(
        "\n".join(
            [
                "study_name: bad",
                "backend: synthetic",
                "flight_mode: POSCTL",
                "scenario: nominal",
                "config_profile: bad",
                "seed: 1",
                "repeat_count: 1",
                "sampling_rate_hz: 20",
                "x_schema: commands_only",
                "prediction_horizon_unit: minutes",
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="prediction_horizon_unit"):
        load_study_config(path)


def test_invalid_output_semantics_raises(tmp_path: Path) -> None:
    path = tmp_path / "bad_output.yaml"
    path.write_text(
        "\n".join(
            [
                "study_name: bad",
                "backend: synthetic",
                "flight_mode: POSCTL",
                "scenario: nominal",
                "config_profile: bad",
                "seed: 1",
                "repeat_count: 1",
                "sampling_rate_hz: 20",
                "x_schema: commands_only",
                "output_semantics: impossible",
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="output_semantics"):
        load_study_config(path)


def test_research_tier_parses_from_px4_configs() -> None:
    authoritative = load_study_config(ROOT / "configs/studies/px4_real_nominal_posctl_capture.yaml")
    demo = load_study_config(ROOT / "configs/studies/px4_visual_demo_offboard_roll_sweep_capture.yaml")
    diagnostic = load_study_config(ROOT / "configs/studies/px4_diagnostic_posctl_axis_capture.yaml")
    throttle = load_study_config(ROOT / "configs/studies/px4_diagnostic_posctl_throttle_capture.yaml")
    assert authoritative.research_tier == "authoritative_research"
    assert demo.research_tier == "demo_only"
    assert diagnostic.research_tier == "diagnostic_research"
    assert throttle.profile_type == "pulse_train"


def test_generalization_profiles_and_backend_mode_covariates_parse(tmp_path: Path) -> None:
    multi_broad = load_study_config(
        write_synthetic_config(
            tmp_path,
            filename="generalization_multi_broad.yaml",
            profile_type="multi_broad",
            axis="composite",
            backend_mode_covariates=["backend", "mode"],
            extras={
                "multi_broad_frequencies_hz": {
                    "roll": [0.13, 0.37, 0.71],
                    "pitch": [0.17, 0.43, 0.89],
                    "yaw": [0.11, 0.29, 0.61],
                    "throttle": [0.19, 0.47, 0.97],
                },
                "multi_broad_phases_rad": {
                    "roll": [0.0, 0.9, 1.8],
                    "pitch": [0.4, 1.3, 2.2],
                    "yaw": [0.7, 1.6, 2.5],
                    "throttle": [1.1, 2.0, 2.9],
                },
            },
        )
    )
    alternating = load_study_config(
        write_synthetic_config(
            tmp_path,
            filename="generalization_alternating.yaml",
            profile_type="alternating_pulse_train",
            axis="throttle",
            extras={"pulse_count": 5, "pulse_width_s": 0.35, "pulse_gap_s": 0.65},
        )
    )
    assert multi_broad.profile_type == "multi_broad"
    assert multi_broad.backend_mode_covariates == ["backend", "mode"]
    assert alternating.profile_type == "alternating_pulse_train"


def test_invalid_backend_mode_covariates_raise(tmp_path: Path) -> None:
    path = write_synthetic_config(tmp_path, filename="invalid_backend_mode_covariates.yaml", backend_mode_covariates=["backend", "impossible"])
    with pytest.raises(ValueError, match="backend_mode_covariates"):
        load_study_config(path)


def test_invalid_research_tier_raises(tmp_path: Path) -> None:
    path = tmp_path / "bad_research_tier.yaml"
    path.write_text(
        "\n".join(
            [
                "study_name: bad",
                "backend: synthetic",
                "flight_mode: POSCTL",
                "scenario: nominal",
                "config_profile: bad",
                "seed: 1",
                "repeat_count: 1",
                "sampling_rate_hz: 20",
                "x_schema: commands_only",
                "research_tier: impossible",
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="research_tier"):
        load_study_config(path)


def test_ardupilot_attitude_defaults_to_guided_nogps() -> None:
    config = load_study_config(ROOT / "configs/studies/ardupilot_real_nominal_guided_nogps_capture.yaml")
    assert config.mode_under_test_for_backend("ardupilot") == "GUIDED_NOGPS"


def test_active_ardupilot_configs_and_scripts_no_longer_use_guided_attitude() -> None:
    active_paths = [
        ROOT / "scripts/run_ardupilot_visual_demos.sh",
        ROOT / "scripts/run_ardupilot_broad_ablation.sh",
        ROOT / "scripts/run_ardupilot_diagnostic_matrix.sh",
        ROOT / "configs/studies/ardupilot_real_nominal_guided_nogps_capture.yaml",
        ROOT / "configs/studies/ardupilot_diagnostic_guided_nogps_axis_capture.yaml",
        ROOT / "configs/studies/ardupilot_diagnostic_guided_nogps_throttle_capture.yaml",
    ]
    for path in active_paths:
        text = path.read_text(encoding="utf-8")
        assert "GUIDED_ATTITUDE" not in text
        assert "guided_attitude" not in text
