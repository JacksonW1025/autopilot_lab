from __future__ import annotations

from pathlib import Path

import pytest

from linearity_core.config import load_ablation_plan, load_study_config


ROOT = Path(__file__).resolve().parents[1]


def test_study_config_parses_new_linearity_fields() -> None:
    config = load_study_config(ROOT / "configs/studies/global_linear_commands_plus_state__delta_state.yaml")
    assert config.x_schema == "commands_plus_state"
    assert config.y_schema == "delta_state"
    assert config.research_tier == "authoritative_research"
    assert config.pooling_mode == "compare_both"
    assert config.output_semantics == "future_state"
    assert config.history_length == 2
    assert config.prediction_horizon == 2
    assert config.prediction_horizon_unit == "steps"
    assert config.run_level_covariates_as_inputs is True
    assert "backend" in config.stratify_by


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
    assert authoritative.research_tier == "authoritative_research"
    assert demo.research_tier == "demo_only"
    assert diagnostic.research_tier == "diagnostic_research"


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
