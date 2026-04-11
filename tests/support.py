from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from linearity_core.config import StudyConfig, load_study_config

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "tests" / "fixtures"


def synthetic_config_payload(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "study_name": "synthetic_linear_f",
        "backend": "synthetic",
        "flight_mode": "POSCTL",
        "scenario": "nominal",
        "config_profile": "synthetic_linear_f",
        "seed": 7,
        "repeat_count": 1,
        "sampling_rate_hz": 20.0,
        "x_schema": "commands_plus_state",
        "y_schema": "delta_state",
        "model": ["ols_affine"],
        "research_tier": "authoritative_research",
        "pooling_mode": "compare_both",
        "output_semantics": "future_state",
        "history_length": 3,
        "prediction_horizon": 2,
        "prediction_horizon_unit": "steps",
        "run_level_covariates_as_inputs": True,
        "stratify_by": ["backend", "mode"],
        "internal_signals_enabled": True,
        "reporting": {"stability_repeats": 1},
        "sparsity": {
            "threshold": 0.05,
            "ridge_alpha": 0.6,
            "lasso_alpha": 0.04,
            "bootstrap_repeats": 4,
            "stability_selection_threshold": 0.5,
        },
        "synthetic": {"sample_count": 96, "noise_std": 0.02, "sparse_matrix_density": 0.18},
    }
    payload.update(overrides)
    return payload


def write_synthetic_config(tmp_path: Path, filename: str = "synthetic_config.json", **overrides: Any) -> Path:
    path = tmp_path / filename
    path.write_text(json.dumps(synthetic_config_payload(**overrides), ensure_ascii=False), encoding="utf-8")
    return path


def load_synthetic_config(tmp_path: Path, filename: str = "synthetic_config.json", **overrides: Any) -> StudyConfig:
    return load_study_config(write_synthetic_config(tmp_path, filename=filename, **overrides))


def fixture_path(*parts: str) -> Path:
    return FIXTURE_ROOT.joinpath(*parts)
