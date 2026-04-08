from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "visualize_fit_matrices.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("visualize_fit_matrices", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_matrix_csv(path: Path, features: list[str], responses: list[str], rows: list[list[float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["feature", *responses])
        for feature, values in zip(features, rows, strict=True):
            writer.writerow([feature, *values])


def _build_study_dir(tmp_path: Path) -> Path:
    study_dir = tmp_path / "study"
    (study_dir / "summary").mkdir(parents=True)
    (study_dir / "fits").mkdir(parents=True)
    manifest = {
        "report_matrix": {
            "appendix_x_schemas": ["feature_mapped_linear", "pooled_backend_mode_augmented"],
        }
    }
    (study_dir / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    responses = ["future_state_roll", "future_state_pitch"]
    features = ["command_roll", "roll", "yaw", "command_roll__lag_1"]
    _write_matrix_csv(
        study_dir / "fits/full_augmented__next_raw_state__pooled/ols_affine/matrix_f.csv",
        features,
        responses,
        [[1.0, -2.0], [0.2, 0.4], [0.0, 0.0], [0.1, -0.1]],
    )
    _write_matrix_csv(
        study_dir / "fits/commands_plus_state_history__next_raw_state__pooled/ols_affine/matrix_f.csv",
        features,
        responses,
        [[0.8, -1.6], [0.1, 0.3], [0.0, 0.0], [0.05, -0.05]],
    )
    _write_matrix_csv(
        study_dir / "fits/commands_plus_state_history__delta_state__stratified/ridge_affine/matrix_f.csv",
        features,
        responses,
        [[0.5, -0.5], [0.0, 0.2], [0.1, 0.1], [0.02, -0.02]],
    )
    _write_matrix_csv(
        study_dir / "fits/feature_mapped_linear__next_raw_state__pooled/ridge_affine/matrix_f.csv",
        features,
        responses,
        [[0.7, -0.4], [0.2, 0.1], [0.0, 0.0], [0.01, -0.01]],
    )

    summary = {
        "study_name": "fake_study",
        "best_result": {
            "x_schema": "full_augmented",
            "y_schema": "next_raw_state",
            "pooling_mode": "pooled",
            "model_name": "ols_affine",
            "appendix": False,
        },
        "best_sparse_result": {
            "x_schema": "commands_plus_state_history",
            "y_schema": "delta_state",
            "pooling_mode": "stratified",
            "model_name": "ridge_affine",
            "appendix": False,
        },
        "ranking": [
            {
                "x_schema": "full_augmented",
                "y_schema": "next_raw_state",
                "pooling_mode": "pooled",
                "model_name": "ols_affine",
                "support": "partial",
                "median_test_r2": 0.99,
                "median_test_mse": 0.01,
                "median_test_mae": 0.01,
            },
            {
                "x_schema": "commands_plus_state_history",
                "y_schema": "next_raw_state",
                "pooling_mode": "pooled",
                "model_name": "ols_affine",
                "support": "supported",
                "median_test_r2": 0.98,
                "median_test_mse": 0.01,
                "median_test_mae": 0.01,
            },
            {
                "x_schema": "feature_mapped_linear",
                "y_schema": "next_raw_state",
                "pooling_mode": "pooled",
                "model_name": "ridge_affine",
                "support": "supported",
                "median_test_r2": 0.97,
                "median_test_mse": 0.01,
                "median_test_mae": 0.01,
            },
        ],
    }
    (study_dir / "summary" / "study_summary.json").write_text(json.dumps(summary), encoding="utf-8")
    return study_dir


def test_select_default_matrix_specs_prefers_best_and_supported_next_raw_state(tmp_path: Path) -> None:
    module = _load_module()
    study_dir = _build_study_dir(tmp_path)

    selected = module.select_default_matrix_specs(study_dir)

    assert [item.path for item in selected] == [
        study_dir / "fits/full_augmented__next_raw_state__pooled/ols_affine/matrix_f.csv",
        study_dir / "fits/commands_plus_state_history__next_raw_state__pooled/ols_affine/matrix_f.csv",
    ]


def test_select_default_matrix_specs_falls_back_to_best_sparse_result(tmp_path: Path) -> None:
    module = _load_module()
    study_dir = _build_study_dir(tmp_path)
    summary_path = study_dir / "summary" / "study_summary.json"
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    payload["ranking"] = [
        {
            "x_schema": "full_augmented",
            "y_schema": "next_raw_state",
            "pooling_mode": "pooled",
            "model_name": "ols_affine",
            "support": "partial",
            "median_test_r2": 0.99,
            "median_test_mse": 0.01,
            "median_test_mae": 0.01,
        }
    ]
    summary_path.write_text(json.dumps(payload), encoding="utf-8")

    selected = module.select_default_matrix_specs(study_dir)

    assert selected[1].path == study_dir / "fits/commands_plus_state_history__delta_state__stratified/ridge_affine/matrix_f.csv"


def test_main_generates_heatmaps_for_study_dir(tmp_path: Path) -> None:
    module = _load_module()
    study_dir = _build_study_dir(tmp_path)

    exit_code = module.main(["--study-dir", str(study_dir)])

    assert exit_code == 0
    for path in (
        study_dir / "fits/full_augmented__next_raw_state__pooled/ols_affine/matrix_heatmap_abs.png",
        study_dir / "fits/full_augmented__next_raw_state__pooled/ols_affine/matrix_heatmap_signed.png",
        study_dir / "fits/commands_plus_state_history__next_raw_state__pooled/ols_affine/matrix_heatmap_abs.png",
        study_dir / "fits/commands_plus_state_history__next_raw_state__pooled/ols_affine/matrix_heatmap_signed.png",
    ):
        assert path.exists()
        assert path.stat().st_size > 0


def test_main_generates_heatmaps_for_explicit_paths_only(tmp_path: Path) -> None:
    module = _load_module()
    first = tmp_path / "fits/commands_only__next_raw_state__pooled/ols_affine/matrix_f.csv"
    second = tmp_path / "fits/commands_plus_state__next_raw_state__pooled/ols_affine/matrix_f.csv"
    _write_matrix_csv(first, ["f1", "f2"], ["y1", "y2"], [[1.0, -2.0], [0.0, 0.5]])
    _write_matrix_csv(second, ["f1", "f2"], ["y1", "y2"], [[0.5, -0.8], [0.1, 0.2]])

    exit_code = module.main(["--matrix-csv", str(first), "--matrix-csv", str(second)])

    assert exit_code == 0
    assert (first.parent / "matrix_heatmap_abs.png").exists()
    assert (first.parent / "matrix_heatmap_signed.png").exists()
    assert (second.parent / "matrix_heatmap_abs.png").exists()
    assert (second.parent / "matrix_heatmap_signed.png").exists()


def test_render_heatmap_figure_omits_cell_numbers_and_numeric_colorbar_ticks(tmp_path: Path) -> None:
    module = _load_module()
    matrix_csv = tmp_path / "fits/full_augmented__next_raw_state__pooled/ols_affine/matrix_f.csv"
    features = [f"feature_{index}" for index in range(40)]
    responses = ["y1", "y2", "y3"]
    rows = [[float(index), -float(index), float(index) / 2.0] for index in range(40)]
    _write_matrix_csv(matrix_csv, features, responses, rows)
    matrix_data = module.load_matrix_csv(matrix_csv)

    fig, ax, colorbar = module.render_heatmap_figure(matrix_data, signed=True, limit=10.0, max_row_labels=10)
    try:
        assert len(ax.texts) == 0
        assert list(colorbar.get_ticks()) == []
        assert len(ax.get_xticklabels()) == len(responses)
        assert len(ax.get_yticklabels()) <= 10
        assert "full_augmented -> next_raw_state" in ax.get_title()
    finally:
        module.plt.close(fig)


def test_main_errors_for_missing_study_summary(tmp_path: Path) -> None:
    module = _load_module()
    missing_study_dir = tmp_path / "missing_summary"
    missing_study_dir.mkdir()

    try:
        module.main(["--study-dir", str(missing_study_dir)])
    except FileNotFoundError as exc:
        assert "study_summary.json" in str(exc)
    else:
        raise AssertionError("expected FileNotFoundError")
