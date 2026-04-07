from __future__ import annotations

from pathlib import Path

import numpy as np

from linearity_core.config import load_study_config
from linearity_core.dataset import build_prepared_sample_table
from linearity_core.schemas import available_x_schemas, build_schema_matrices
from linearity_core.synthetic import generate_synthetic_raw_runs


ROOT = Path(__file__).resolve().parents[1]


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
    config = load_study_config(ROOT / "configs/studies/global_linear_history_augmented__future_state_horizon.yaml")
    run_dirs = generate_synthetic_raw_runs(config, output_root=tmp_path)
    table, _ = build_prepared_sample_table(run_dirs, config)
    matrices = build_schema_matrices(table, config, "commands_plus_state_history", "future_state_horizon")
    assert matrices.X.shape[1] > 0
    assert any("__lag_" in name for name in matrices.feature_names)
    assert np.sum(matrices.valid_mask) > 10


def test_feature_mapped_linear_is_marked_non_strict(tmp_path: Path) -> None:
    config = load_study_config(ROOT / "configs/studies/global_linear_pooled_backend_augmented__selected_state_subset.yaml")
    run_dirs = generate_synthetic_raw_runs(config, output_root=tmp_path)
    table, _ = build_prepared_sample_table(run_dirs, config)
    matrices = build_schema_matrices(table, config, "feature_mapped_linear", "selected_state_subset")
    assert matrices.schema_metadata["strict_raw_linear"] is False
    assert any(name.startswith("sq__") or "__command_" in name for name in matrices.feature_names)


def test_missing_state_columns_are_pruned_instead_of_invalidating_schema(tmp_path: Path) -> None:
    config = load_study_config(ROOT / "configs/studies/global_linear_commands_plus_state__delta_state.yaml")
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
