from __future__ import annotations

from linearity_core.dataset import build_prepared_sample_table
from linearity_core.schemas import available_y_schemas, build_schema_matrices
from linearity_core.synthetic import generate_synthetic_raw_runs
from tests.support import load_synthetic_config


def test_y_schema_registry_contains_required_entries() -> None:
    schemas = set(available_y_schemas())
    assert {
        "next_raw_state",
        "delta_state",
        "selected_state_subset",
        "future_state_horizon",
        "actuator_response",
        "tracking_error_response",
        "window_summary_response",
        "stability_proxy_response",
    }.issubset(schemas)


def test_future_and_window_response_shapes(tmp_path: Path) -> None:
    config = load_synthetic_config(
        tmp_path,
        filename="window_config.json",
        x_schema="full_augmented",
        y_schema="window_summary_response",
    )
    run_dirs = generate_synthetic_raw_runs(config, output_root=tmp_path)
    table, _ = build_prepared_sample_table(run_dirs, config)

    future_matrices = build_schema_matrices(table, config, "commands_plus_state", "future_state_horizon")
    assert future_matrices.Y.shape[1] == config.prediction_horizon * 6
    assert any(name.endswith("__h1") for name in future_matrices.response_names)

    window_matrices = build_schema_matrices(table, config, "full_augmented", "window_summary_response")
    assert window_matrices.Y.shape[1] > 0
    assert any(name.startswith("window_mean_") for name in window_matrices.response_names)
