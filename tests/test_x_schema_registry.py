from __future__ import annotations

from pathlib import Path

import numpy as np

from linearity_core.dataset import build_prepared_sample_table
from linearity_core.schemas import available_x_schemas, build_schema_matrices
from linearity_core.synthetic import generate_synthetic_raw_runs
from tests.support import load_synthetic_config


def test_x_schema_registry_contains_required_entries() -> None:
    schemas = set(available_x_schemas())
    assert {
        "commands_only",
        "commands_plus_state",
        "commands_plus_state_history",
        "commands_plus_controller_params",
        "commands_plus_state_plus_params",
        "pooled_backend_mode_augmented",
        "full_augmented",
        "feature_mapped_linear",
    }.issubset(schemas)


def test_history_schema_adds_lagged_features(tmp_path: Path) -> None:
    config = load_synthetic_config(
        tmp_path,
        filename="history_config.json",
        x_schema="commands_plus_state_history",
        y_schema="future_state_horizon",
    )
    run_dirs = generate_synthetic_raw_runs(config, output_root=tmp_path)
    table, _ = build_prepared_sample_table(run_dirs, config)
    matrices = build_schema_matrices(table, config, "commands_plus_state_history", "future_state_horizon")
    assert matrices.X.shape[1] > 0
    assert any("__lag_" in name for name in matrices.feature_names)
    assert np.sum(matrices.valid_mask) > 10


def test_feature_mapped_linear_is_marked_non_strict(tmp_path: Path) -> None:
    config = load_synthetic_config(
        tmp_path,
        filename="feature_map_config.json",
        x_schema="pooled_backend_mode_augmented",
        y_schema="selected_state_subset",
    )
    run_dirs = generate_synthetic_raw_runs(config, output_root=tmp_path)
    table, _ = build_prepared_sample_table(run_dirs, config)
    matrices = build_schema_matrices(table, config, "feature_mapped_linear", "selected_state_subset")
    assert matrices.schema_metadata["strict_raw_linear"] is False
    assert any(name.startswith("sq__") or "__command_" in name for name in matrices.feature_names)


def test_missing_state_columns_are_pruned_instead_of_invalidating_schema(tmp_path: Path) -> None:
    config = load_synthetic_config(tmp_path, filename="state_delta_config.json")
    run_dirs = generate_synthetic_raw_runs(config, output_root=tmp_path)
    table, _ = build_prepared_sample_table(run_dirs, config)
    for row in table.rows:
        row["roll_rate"] = np.nan
        row["pitch_rate"] = np.nan
        row["yaw_rate"] = np.nan
        row["future_state_roll_rate"] = np.nan
        row["future_state_pitch_rate"] = np.nan
        row["future_state_yaw_rate"] = np.nan
        row["delta_state_roll_rate"] = np.nan
        row["delta_state_pitch_rate"] = np.nan
        row["delta_state_yaw_rate"] = np.nan
    matrices = build_schema_matrices(table, config, "commands_plus_state", "delta_state")
    assert np.sum(matrices.valid_mask) > 10
    assert "roll_rate" not in matrices.feature_names
    assert "delta_state_roll_rate" not in matrices.response_names
    assert "roll_rate" in matrices.schema_metadata["dropped_unavailable_features"]
    assert "delta_state_roll_rate" in matrices.schema_metadata["dropped_unavailable_responses"]


def test_backend_mode_covariates_can_exclude_scenario_and_config_profile(tmp_path: Path) -> None:
    config = load_synthetic_config(
        tmp_path,
        filename="generalization_covariates_config.json",
        x_schema="pooled_backend_mode_augmented",
        y_schema="delta_state",
        backend_mode_covariates=["backend", "mode"],
    )
    run_dirs = generate_synthetic_raw_runs(config, output_root=tmp_path)
    table, _ = build_prepared_sample_table(run_dirs, config)
    for row in table.rows:
        row["scenario_dynamic"] = 1.0 if row["logical_step"] % 2 == 0 else 0.0
        row["scenario_nominal"] = 1.0 - row["scenario_dynamic"]
        row["config_profile_dynamic"] = row["scenario_dynamic"]
        row["config_profile_nominal"] = row["scenario_nominal"]
    matrices = build_schema_matrices(table, config, "pooled_backend_mode_augmented", "delta_state")
    assert not any(name.startswith("scenario_") for name in matrices.feature_names)
    assert not any(name.startswith("config_profile_") for name in matrices.feature_names)
    assert any(name.startswith("backend_") for name in matrices.feature_names)
    assert any(name.startswith("mode_") for name in matrices.feature_names)
