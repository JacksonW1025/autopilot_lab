from __future__ import annotations

import numpy as np

from linearity_core.config import StudyConfig
from linearity_core.fit import fit_schema_combo
from linearity_core.schemas import SchemaMatrices


def _base_config() -> StudyConfig:
    return StudyConfig.from_dict(
        {
            "study_name": "known_linear",
            "backend": "synthetic",
            "flight_mode": "POSCTL",
            "scenario": "unit",
            "config_profile": "known_linear",
            "seed": 3,
            "repeat_count": 1,
            "sampling_rate_hz": 20.0,
            "x_schema": "commands_only",
            "y_schema": "delta_state",
            "model": ["ols_affine"],
            "reporting": {"stability_repeats": 1},
            "sparsity": {"threshold": 0.02, "bootstrap_repeats": 2, "stability_selection_threshold": 0.5},
        }
    )


def test_known_linear_system_recovers_f() -> None:
    rng = np.random.default_rng(7)
    X = rng.normal(size=(160, 3))
    true_f = np.asarray([[1.2, 0.0], [-0.5, 0.8], [0.0, 1.1]], dtype=float)
    true_b = np.asarray([0.1, -0.2], dtype=float)
    Y = X @ true_f + true_b
    matrices = SchemaMatrices(
        X=X,
        Y=Y,
        feature_names=["x0", "x1", "x2"],
        response_names=["y0", "y1"],
        valid_mask=np.ones(len(X), dtype=bool),
        schema_metadata={},
    )
    run_ids = [f"run_{index // 40}" for index in range(len(X))]
    result = fit_schema_combo(
        run_ids,
        ["synthetic"] * len(X),
        ["POSCTL"] * len(X),
        ["unit"] * len(X),
        matrices,
        _base_config(),
        "ols_affine",
    )
    assert np.allclose(result.coefficient_matrix, true_f, atol=1e-6)
    assert np.allclose(result.bias_vector, true_b, atol=1e-6)
    assert result.summary["median_test_r2"] > 0.999999


def test_sparse_matrix_recovery_identifies_main_nonzero_terms() -> None:
    rng = np.random.default_rng(11)
    X = rng.normal(size=(220, 6))
    true_f = np.zeros((6, 3), dtype=float)
    true_f[0, 0] = 1.4
    true_f[3, 1] = -1.1
    true_f[5, 2] = 0.9
    Y = X @ true_f + rng.normal(0.0, 0.01, size=(220, 3))
    matrices = SchemaMatrices(
        X=X,
        Y=Y,
        feature_names=[f"x{index}" for index in range(6)],
        response_names=[f"y{index}" for index in range(3)],
        valid_mask=np.ones(len(X), dtype=bool),
        schema_metadata={},
    )
    config = StudyConfig.from_dict(
        {
            "study_name": "sparse_recovery",
            "backend": "synthetic",
            "flight_mode": "POSCTL",
            "scenario": "unit",
            "config_profile": "sparse",
            "seed": 5,
            "repeat_count": 1,
            "sampling_rate_hz": 20.0,
            "x_schema": "commands_only",
            "y_schema": "delta_state",
            "model": ["lasso_affine"],
            "reporting": {"stability_repeats": 2},
                "sparsity": {
                    "threshold": 0.02,
                    "lasso_alpha": 0.2,
                    "bootstrap_repeats": 4,
                    "stability_selection_threshold": 0.5,
                    "coef_std_tolerance": 0.25,
            },
        }
    )
    run_ids = [f"run_{index // 55}" for index in range(len(X))]
    result = fit_schema_combo(
        run_ids,
        ["synthetic"] * len(X),
        ["POSCTL"] * len(X),
        ["unit"] * len(X),
        matrices,
        config,
        "lasso_affine",
    )
    mask = result.sparsity_mask.astype(bool)
    assert mask[0, 0]
    assert mask[3, 1]
    assert mask[5, 2]
    assert result.summary["nonzero_count"] <= 8
    assert "scenario_consistency" in result.summary
    assert result.summary["scenario_subgroup_metrics"]["unit"]["sample_count"] > 0
