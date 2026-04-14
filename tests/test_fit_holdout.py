from __future__ import annotations

import numpy as np

from linearity_analysis.linearity_analyze import _run_stratified_holdout_fit
from linearity_core.dataset import PreparedSampleTable
from linearity_core.fit import fit_schema_combo_holdout
from linearity_core.schemas import SchemaMatrices
from tests.support import load_synthetic_config


def test_fit_schema_combo_holdout_recovers_linear_mapping(tmp_path) -> None:
    config = load_synthetic_config(
        tmp_path,
        reporting={"stability_repeats": 1},
        sparsity={
            "threshold": 0.01,
            "ridge_alpha": 0.1,
            "lasso_alpha": 0.01,
            "bootstrap_repeats": 2,
            "stability_selection_threshold": 0.5,
        },
    )
    scenarios = ["nominal"] * 6 + ["dynamic"] * 6 + ["throttle_biased"] * 6
    x1 = np.linspace(-1.0, 1.0, len(scenarios))
    x2 = np.linspace(0.5, 2.3, len(scenarios))
    X = np.column_stack([x1, x2])
    Y = (2.0 * x1 - 0.5 * x2).reshape(-1, 1)
    matrices = SchemaMatrices(
        X=X,
        Y=Y,
        feature_names=["command_roll", "roll"],
        response_names=["future_state_roll"],
        valid_mask=np.ones(len(scenarios), dtype=bool),
        schema_metadata={},
    )
    run_ids = [f"run_{index:02d}" for index in range(len(scenarios))]
    backends = ["synthetic"] * len(scenarios)
    modes = ["POSCTL"] * len(scenarios)
    train_valid_indices = np.asarray([index for index, scenario in enumerate(scenarios) if scenario != "throttle_biased"], dtype=int)
    test_valid_indices = np.asarray([index for index, scenario in enumerate(scenarios) if scenario == "throttle_biased"], dtype=int)

    result = fit_schema_combo_holdout(
        run_ids,
        backends,
        modes,
        scenarios,
        matrices,
        config,
        "ols_affine",
        train_valid_indices=train_valid_indices,
        test_valid_indices=test_valid_indices,
    )

    assert result.summary["holdout_test_r2"] > 0.99
    assert result.summary["holdout_sample_count"] == len(test_valid_indices)
    assert result.coefficient_matrix.shape == (2, 1)
    assert result.residual_rows


def test_run_stratified_holdout_fit_respects_group_specific_models(tmp_path) -> None:
    config = load_synthetic_config(
        tmp_path,
        reporting={"stability_repeats": 1},
        sparsity={
            "threshold": 0.01,
            "ridge_alpha": 0.1,
            "lasso_alpha": 0.01,
            "bootstrap_repeats": 2,
            "stability_selection_threshold": 0.5,
        },
    )
    rows = []
    features: list[list[float]] = []
    responses: list[list[float]] = []
    run_index = 0
    for mode_name, scale in (("MODE_A", 2.0), ("MODE_B", -3.0)):
        for scenario_name in ("nominal", "dynamic", "throttle_biased"):
            for step in range(4):
                x = float(step + 1)
                rows.append(
                    {
                        "run_id": f"run_{run_index:02d}",
                        "backend": "synthetic",
                        "mode": mode_name,
                        "scenario": scenario_name,
                    }
                )
                features.append([x])
                responses.append([scale * x])
                run_index += 1
    table = PreparedSampleTable(rows=rows, numeric_columns=[])
    matrices = SchemaMatrices(
        X=np.asarray(features, dtype=float),
        Y=np.asarray(responses, dtype=float),
        feature_names=["command_roll"],
        response_names=["future_state_roll"],
        valid_mask=np.ones(len(rows), dtype=bool),
        schema_metadata={},
    )

    fitted = _run_stratified_holdout_fit(
        table,
        matrices,
        config,
        "ols_affine",
        ["mode"],
        holdout_scenario="throttle_biased",
    )

    assert fitted["summary"]["holdout_test_r2"] > 0.99
    assert fitted["summary"]["holdout_sample_count"] == 8
    assert fitted["summary"]["group_results"]
