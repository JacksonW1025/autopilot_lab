from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np

from .config import StudyConfig
from .schemas import SchemaMatrices

CONDITIONING_ALIAS_KEEP = {
    "altitude": "position_z",
    "vertical_speed": "velocity_z",
}
CONDITIONING_ONE_HOT_PREFIXES = (
    "backend_",
    "mode_",
    "scenario_",
    "config_profile_",
)


def _safe_median(values: list[float]) -> float:
    clean = [float(value) for value in values if not math.isnan(float(value))]
    if not clean:
        return math.nan
    return float(np.median(np.asarray(clean, dtype=float)))


def _standardize(X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = np.nanmean(X, axis=0)
    std = np.nanstd(X, axis=0)
    std[std == 0.0] = 1.0
    standardized = (X - mean) / std
    return standardized, mean, std


def _singular_values(X: np.ndarray) -> np.ndarray:
    if X.size == 0:
        return np.asarray([], dtype=float)
    return np.linalg.svd(X, compute_uv=False)


def _condition_number_from_singular_values(singular_values: np.ndarray) -> float:
    if singular_values.size == 0:
        return math.nan
    smallest = float(singular_values[-1])
    largest = float(singular_values[0])
    if not math.isfinite(largest) or largest <= 0.0:
        return math.nan
    tolerance = np.finfo(float).eps * max(1, singular_values.size) * largest
    if smallest <= tolerance or not math.isfinite(smallest):
        return math.inf
    return largest / smallest


def _independent_column_indices(X: np.ndarray) -> list[int]:
    if X.size == 0 or X.shape[1] == 0:
        return []
    keep: list[int] = []
    previous_rank = 0
    for column_index in range(X.shape[1]):
        candidate_indices = keep + [column_index]
        candidate_rank = int(np.linalg.matrix_rank(X[:, candidate_indices]))
        if candidate_rank > previous_rank:
            keep.append(column_index)
            previous_rank = candidate_rank
    return keep


def _conditioning_view(X: np.ndarray, feature_names: list[str]) -> dict[str, Any]:
    if X.size == 0 or not feature_names:
        return {
            "X": X[:, :0],
            "feature_names": [],
            "conditioning_pruned_features": [],
            "conditioning_baseline_drops": [],
            "conditioning_extra_pruned_features": [],
        }

    keep_mask = np.ones(len(feature_names), dtype=bool)
    alias_drops: list[str] = []
    for drop_name, keep_name in CONDITIONING_ALIAS_KEEP.items():
        if drop_name in feature_names and keep_name in feature_names:
            keep_mask[feature_names.index(drop_name)] = False
            alias_drops.append(drop_name)

    baseline_drops: list[str] = []
    for prefix in CONDITIONING_ONE_HOT_PREFIXES:
        family = [index for index, name in enumerate(feature_names) if keep_mask[index] and name.startswith(prefix)]
        if len(family) <= 1:
            continue
        baseline_name, baseline_index = sorted((feature_names[index], index) for index in family)[0]
        keep_mask[baseline_index] = False
        baseline_drops.append(baseline_name)

    candidate_indices = [index for index, keep in enumerate(keep_mask) if keep]
    candidate_names = [feature_names[index] for index in candidate_indices]
    candidate_X = X[:, candidate_indices] if candidate_indices else X[:, :0]
    independent_relative = _independent_column_indices(candidate_X)
    effective_names = [candidate_names[index] for index in independent_relative]
    effective_X = candidate_X[:, independent_relative] if independent_relative else candidate_X[:, :0]
    independent_set = set(independent_relative)
    extra_drops = [candidate_names[index] for index in range(len(candidate_names)) if index not in independent_set]
    return {
        "X": effective_X,
        "feature_names": effective_names,
        "conditioning_pruned_features": alias_drops + baseline_drops + extra_drops,
        "conditioning_baseline_drops": baseline_drops,
        "conditioning_extra_pruned_features": extra_drops,
    }


def _split_indices(run_ids: list[str], seed: int, size: int) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    unique_run_ids = np.asarray(sorted(set(run_ids)), dtype=object)
    if len(unique_run_ids) >= 3:
        shuffled = unique_run_ids.copy()
        rng.shuffle(shuffled)
        train_cut = max(1, int(round(len(shuffled) * 0.6)))
        val_cut = max(train_cut + 1, int(round(len(shuffled) * 0.8)))
        train_ids = set(shuffled[:train_cut])
        val_ids = set(shuffled[train_cut:val_cut])
        test_ids = set(shuffled[val_cut:]) or set(shuffled[-1:])
        return {
            "train": np.asarray([index for index, run_id in enumerate(run_ids) if run_id in train_ids], dtype=int),
            "val": np.asarray([index for index, run_id in enumerate(run_ids) if run_id in val_ids], dtype=int),
            "test": np.asarray([index for index, run_id in enumerate(run_ids) if run_id in test_ids], dtype=int),
        }

    indices = np.arange(size, dtype=int)
    train_cut = max(1, int(round(size * 0.6)))
    val_cut = max(train_cut + 1, int(round(size * 0.8)))
    return {
        "train": indices[:train_cut],
        "val": indices[train_cut:val_cut] if val_cut > train_cut else indices[:0],
        "test": indices[val_cut:] if val_cut < size else indices[-1:],
    }


def _mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(np.square(y_true - y_pred)))


def _mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(np.abs(y_true - y_pred)))


def _r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    numerator = float(np.sum(np.square(y_true - y_pred)))
    denominator = float(np.sum(np.square(y_true - np.mean(y_true, axis=0))))
    if denominator <= 0.0:
        return math.nan
    return 1.0 - numerator / denominator


def _residual_statistics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    residual = y_true - y_pred
    return {
        "residual_mean_abs": float(np.mean(np.abs(residual))),
        "residual_std": float(np.std(residual)),
        "residual_max_abs": float(np.max(np.abs(residual))),
    }


def _solve_ols(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    return np.linalg.lstsq(X, Y, rcond=None)[0]


def _solve_ridge(X: np.ndarray, Y: np.ndarray, alpha: float) -> np.ndarray:
    eye = np.eye(X.shape[1], dtype=float)
    return np.linalg.solve(X.T @ X + alpha * eye, X.T @ Y)


def _soft_threshold(value: float, threshold: float) -> float:
    if value > threshold:
        return value - threshold
    if value < -threshold:
        return value + threshold
    return 0.0


def _solve_lasso(X: np.ndarray, Y: np.ndarray, alpha: float, max_iter: int = 200, tolerance: float = 1e-6) -> np.ndarray:
    feature_count = X.shape[1]
    target_count = Y.shape[1]
    beta = np.zeros((feature_count, target_count), dtype=float)
    gram_diag = np.sum(np.square(X), axis=0)
    gram_diag[gram_diag == 0.0] = 1.0
    for target_index in range(target_count):
        y = Y[:, target_index]
        weights = np.zeros(feature_count, dtype=float)
        residual = y.copy()
        for _ in range(max_iter):
            max_delta = 0.0
            for feature_index in range(feature_count):
                column = X[:, feature_index]
                old_weight = weights[feature_index]
                if old_weight != 0.0:
                    residual += column * old_weight
                rho = float(np.dot(column, residual))
                new_weight = _soft_threshold(rho, alpha) / gram_diag[feature_index]
                if new_weight != 0.0:
                    residual -= column * new_weight
                weights[feature_index] = new_weight
                max_delta = max(max_delta, abs(new_weight - old_weight))
            if max_delta <= tolerance:
                break
        beta[:, target_index] = weights
    return beta


def _fit_single_model(
    model_name: str,
    X_train: np.ndarray,
    Y_train: np.ndarray,
    config: StudyConfig,
    feature_names: list[str],
) -> dict[str, Any]:
    Xs, X_mean, X_std = _standardize(X_train)
    y_mean = np.mean(Y_train, axis=0)
    Y_centered = Y_train - y_mean
    raw_singular_values = _singular_values(Xs)
    raw_condition_number = _condition_number_from_singular_values(raw_singular_values)

    if model_name == "ols_affine":
        beta = _solve_ols(Xs, Y_centered)
        standardized_beta = beta
    elif model_name == "ridge_affine":
        alpha = float(config.sparsity.get("ridge_alpha", 1.0))
        beta = _solve_ridge(Xs, Y_centered, alpha=alpha)
        standardized_beta = beta
    elif model_name == "lasso_affine":
        alpha = float(config.sparsity.get("lasso_alpha", 0.05))
        beta = _solve_lasso(
            Xs,
            Y_centered,
            alpha=alpha,
            max_iter=int(config.sparsity.get("lasso_max_iter", 200)),
            tolerance=float(config.sparsity.get("lasso_tolerance", 1e-6)),
        )
        standardized_beta = beta
    elif model_name == "thresholded_ols_affine":
        beta = _solve_ols(Xs, Y_centered)
        threshold = float(config.sparsity.get("threshold", 0.05))
        standardized_beta = np.where(np.abs(beta) >= threshold, beta, 0.0)
    else:
        raise ValueError(f"不支持的 model: {model_name}")

    coef = standardized_beta / X_std.reshape(-1, 1)
    bias = y_mean - X_mean @ coef
    threshold = float(config.sparsity.get("threshold", 0.05))
    mask = np.abs(standardized_beta) > (threshold if model_name != "lasso_affine" else 1e-9)
    conditioning = _conditioning_view(Xs, feature_names)
    effective_singular_values = _singular_values(conditioning["X"])
    effective_condition_number = _condition_number_from_singular_values(effective_singular_values)
    return {
        "coef": coef,
        "bias": bias,
        "mask": mask.astype(float),
        "standardized_coef": standardized_beta,
        "raw_condition_number": raw_condition_number,
        "effective_condition_number": effective_condition_number,
        "condition_number": effective_condition_number,
        "raw_singular_values": [float(value) for value in raw_singular_values[: min(10, len(raw_singular_values))]],
        "effective_singular_values": [float(value) for value in effective_singular_values[: min(10, len(effective_singular_values))]],
        "conditioning_pruned_features": conditioning["conditioning_pruned_features"],
        "conditioning_baseline_drops": conditioning["conditioning_baseline_drops"],
        "conditioning_extra_pruned_features": conditioning["conditioning_extra_pruned_features"],
    }


def _predict(X: np.ndarray, coef: np.ndarray, bias: np.ndarray) -> np.ndarray:
    return X @ coef + bias


def _metrics_bundle(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    bundle = {
        "r2": _r2(y_true, y_pred),
        "mse": _mse(y_true, y_pred),
        "mae": _mae(y_true, y_pred),
    }
    bundle.update(_residual_statistics(y_true, y_pred))
    return bundle


def _bootstrap_selection_frequency(
    model_name: str,
    X_train: np.ndarray,
    Y_train: np.ndarray,
    config: StudyConfig,
    feature_names: list[str],
) -> np.ndarray:
    repeats = int(config.sparsity.get("bootstrap_repeats", 8))
    threshold = float(config.sparsity.get("stability_selection_threshold", 0.60))
    if repeats <= 0:
        return np.zeros((X_train.shape[1], Y_train.shape[1]), dtype=float)
    rng = np.random.default_rng(config.seed)
    selections: list[np.ndarray] = []
    for _ in range(repeats):
        indices = rng.integers(0, X_train.shape[0], size=X_train.shape[0])
        fit = _fit_single_model(model_name, X_train[indices], Y_train[indices], config, feature_names)
        selections.append(fit["mask"])
    freq = np.mean(np.stack(selections, axis=0), axis=0)
    return np.where(freq >= threshold, freq, freq)


def _group_consistency(
    group_name: str,
    group_values: list[str],
    indices: np.ndarray,
    Y: np.ndarray,
    coef: np.ndarray,
    bias: np.ndarray,
    X: np.ndarray,
) -> dict[str, dict[str, float]]:
    metrics: dict[str, dict[str, float]] = {}
    for value in sorted({group_values[index] for index in indices if group_values[index]}):
        value_indices = np.asarray([index for index in indices if group_values[index] == value], dtype=int)
        if len(value_indices) == 0:
            continue
        predictions = _predict(X[value_indices], coef, bias)
        metrics[value] = {
            **_metrics_bundle(Y[value_indices], predictions),
            "sample_count": float(len(value_indices)),
        }
    return metrics


def _consistency_score(metrics: dict[str, dict[str, float]]) -> float:
    r2_values = [
        float(item.get("r2", math.nan))
        for item in metrics.values()
        if math.isfinite(float(item.get("r2", math.nan)))
    ]
    if not r2_values:
        return math.nan
    if len(r2_values) == 1:
        return 1.0
    best = max(r2_values)
    worst = min(r2_values)
    if best <= 0.0:
        return 0.0
    return max(0.0, min(1.0, worst / best))


@dataclass(slots=True)
class ModelResult:
    summary: dict[str, Any]
    coefficient_matrix: np.ndarray
    bias_vector: np.ndarray
    sparsity_mask: np.ndarray
    residual_rows: list[dict[str, Any]]


def _valid_subset(
    table_run_ids: list[str],
    backends: list[str],
    modes: list[str],
    scenarios: list[str],
    matrices: SchemaMatrices,
) -> dict[str, Any]:
    valid_indices = np.flatnonzero(matrices.valid_mask)
    return {
        "valid_indices": valid_indices,
        "X": matrices.X[valid_indices],
        "Y": matrices.Y[valid_indices],
        "run_ids": [table_run_ids[index] for index in valid_indices],
        "backends": [backends[index] for index in valid_indices],
        "modes": [modes[index] for index in valid_indices],
        "scenarios": [scenarios[index] for index in valid_indices],
    }


def fit_schema_combo(
    table_run_ids: list[str],
    backends: list[str],
    modes: list[str],
    scenarios: list[str],
    matrices: SchemaMatrices,
    config: StudyConfig,
    model_name: str,
) -> ModelResult:
    valid_indices = np.flatnonzero(matrices.valid_mask)
    X = matrices.X[valid_indices]
    Y = matrices.Y[valid_indices]
    run_ids = [table_run_ids[index] for index in valid_indices]
    backends_valid = [backends[index] for index in valid_indices]
    modes_valid = [modes[index] for index in valid_indices]
    scenarios_valid = [scenarios[index] for index in valid_indices]

    stability_repeats = int(config.reporting.get("stability_repeats", 3))
    summaries: list[dict[str, Any]] = []
    coefficients: list[np.ndarray] = []
    biases: list[np.ndarray] = []
    masks: list[np.ndarray] = []
    residual_rows: list[dict[str, Any]] = []
    split_records: list[dict[str, Any]] = []
    bootstrap_frequency: np.ndarray | None = None

    for repeat_index in range(stability_repeats):
        split = _split_indices(run_ids, config.seed + repeat_index, len(run_ids))
        X_train = X[split["train"]]
        Y_train = Y[split["train"]]
        fit = _fit_single_model(model_name, X_train, Y_train, config, matrices.feature_names)
        coef = fit["coef"]
        bias = fit["bias"]
        mask = fit["mask"]
        coefficients.append(coef)
        biases.append(bias)
        masks.append(mask)
        if bootstrap_frequency is None:
            bootstrap_frequency = _bootstrap_selection_frequency(model_name, X_train, Y_train, config, matrices.feature_names)

        split_summary: dict[str, Any] = {
            "repeat_index": repeat_index + 1,
            "train": _metrics_bundle(Y_train, _predict(X_train, coef, bias)),
            "val": _metrics_bundle(Y[split["val"]], _predict(X[split["val"]], coef, bias)) if len(split["val"]) else {},
            "test": _metrics_bundle(Y[split["test"]], _predict(X[split["test"]], coef, bias)) if len(split["test"]) else {},
            "condition_number": fit["condition_number"],
            "raw_condition_number": fit["raw_condition_number"],
            "raw_singular_values": fit["raw_singular_values"],
            "effective_condition_number": fit["effective_condition_number"],
            "singular_values": fit["effective_singular_values"],
            "effective_singular_values": fit["effective_singular_values"],
            "conditioning_pruned_features": fit["conditioning_pruned_features"],
            "conditioning_baseline_drops": fit["conditioning_baseline_drops"],
            "conditioning_extra_pruned_features": fit["conditioning_extra_pruned_features"],
        }
        summaries.append(split_summary)
        split_records.append(
            {
                "repeat_index": repeat_index + 1,
                "train_count": int(len(split["train"])),
                "val_count": int(len(split["val"])),
                "test_count": int(len(split["test"])),
            }
        )
        if repeat_index == 0:
            test_indices = split["test"] if len(split["test"]) else split["train"]
            predictions = _predict(X[test_indices], coef, bias)
            for row_offset, sample_index in enumerate(test_indices):
                residual_rows.append(
                    {
                        "sample_index": int(valid_indices[sample_index]),
                        "backend": backends_valid[sample_index],
                        "mode": modes_valid[sample_index],
                        "run_id": run_ids[sample_index],
                        "target_norm": float(np.linalg.norm(Y[test_indices][row_offset])),
                        "prediction_norm": float(np.linalg.norm(predictions[row_offset])),
                        "residual_norm": float(np.linalg.norm(Y[test_indices][row_offset] - predictions[row_offset])),
                    }
                )

    mean_coef = np.mean(np.stack(coefficients, axis=0), axis=0)
    mean_bias = np.mean(np.stack(biases, axis=0), axis=0)
    mean_mask = np.mean(np.stack(masks, axis=0), axis=0)
    stable_mask_threshold = float(config.sparsity.get("stability_selection_threshold", 0.60))
    stable_mask = mean_mask >= stable_mask_threshold
    frequency = bootstrap_frequency if bootstrap_frequency is not None else mean_mask

    test_r2_values = [float(summary["test"].get("r2", math.nan)) for summary in summaries]
    test_mse_values = [float(summary["test"].get("mse", math.nan)) for summary in summaries]
    test_mae_values = [float(summary["test"].get("mae", math.nan)) for summary in summaries]
    raw_condition_values = [float(summary.get("raw_condition_number", math.nan)) for summary in summaries]
    effective_condition_values = [float(summary.get("effective_condition_number", math.nan)) for summary in summaries]
    coefficient_stability = float(np.mean(np.std(np.stack(coefficients, axis=0), axis=0) <= float(config.sparsity.get("coef_std_tolerance", 0.15))))
    conditioning_pruned_features = sorted({name for summary in summaries for name in summary.get("conditioning_pruned_features", [])})
    conditioning_baseline_drops = sorted({name for summary in summaries for name in summary.get("conditioning_baseline_drops", [])})
    conditioning_extra_pruned_features = sorted({name for summary in summaries for name in summary.get("conditioning_extra_pruned_features", [])})

    top_influential: dict[str, list[dict[str, float | str]]] = {}
    for response_index, response_name in enumerate(matrices.response_names):
        response_weights = np.abs(mean_coef[:, response_index])
        order = np.argsort(response_weights)[::-1][:5]
        top_influential[response_name] = [
            {
                "feature": matrices.feature_names[index],
                "weight": float(mean_coef[index, response_index]),
                "selection_frequency": float(frequency[index, response_index]),
            }
            for index in order
            if response_weights[index] > 0.0
        ]

    all_indices = np.arange(X.shape[0], dtype=int)
    backend_consistency = _group_consistency("backend", backends_valid, all_indices, Y, mean_coef, mean_bias, X)
    mode_consistency = _group_consistency("mode", modes_valid, all_indices, Y, mean_coef, mean_bias, X)
    scenario_subgroup_metrics = _group_consistency("scenario", scenarios_valid, all_indices, Y, mean_coef, mean_bias, X)
    nonzero_count = int(np.sum(stable_mask))
    sparsity_ratio = 1.0 - (nonzero_count / max(1, stable_mask.size))

    summary = {
        "model_name": model_name,
        "repeat_metrics": summaries,
        "split_records": split_records,
        "median_test_r2": _safe_median(test_r2_values),
        "median_test_mse": _safe_median(test_mse_values),
        "median_test_mae": _safe_median(test_mae_values),
        "coefficient_stability": coefficient_stability,
        "nonzero_count": nonzero_count,
        "sparsity_ratio": sparsity_ratio,
        "block_sparsity_summary": {
            "feature_blocks": {
                "commands": int(sum(1 for name in matrices.feature_names if name.startswith("command_"))),
                "state": int(sum(1 for name in matrices.feature_names if name in {"roll", "pitch", "yaw", "roll_rate", "pitch_rate", "yaw_rate"})),
                "history": int(sum(1 for name in matrices.feature_names if "__lag_" in name)),
                "controller_params": int(sum(1 for name in matrices.feature_names if name.startswith("param_"))),
            },
        },
        "raw_condition_number": _safe_median(raw_condition_values),
        "effective_condition_number": _safe_median(effective_condition_values),
        "condition_number": _safe_median(effective_condition_values),
        "raw_singular_values": summaries[0]["raw_singular_values"] if summaries else [],
        "singular_values": summaries[0]["effective_singular_values"] if summaries else [],
        "effective_singular_values": summaries[0]["effective_singular_values"] if summaries else [],
        "conditioning_pruned_features": conditioning_pruned_features,
        "conditioning_baseline_drops": conditioning_baseline_drops,
        "conditioning_extra_pruned_features": conditioning_extra_pruned_features,
        "selection_frequency": frequency.tolist(),
        "backend_consistency": backend_consistency,
        "mode_consistency": mode_consistency,
        "scenario_consistency": _consistency_score(scenario_subgroup_metrics),
        "scenario_subgroup_metrics": scenario_subgroup_metrics,
        "top_influential": top_influential,
    }
    return ModelResult(
        summary=summary,
        coefficient_matrix=mean_coef,
        bias_vector=mean_bias,
        sparsity_mask=stable_mask.astype(float),
        residual_rows=residual_rows,
    )


def fit_schema_combo_holdout(
    table_run_ids: list[str],
    backends: list[str],
    modes: list[str],
    scenarios: list[str],
    matrices: SchemaMatrices,
    config: StudyConfig,
    model_name: str,
    *,
    train_valid_indices: np.ndarray,
    test_valid_indices: np.ndarray,
    split_name: str = "holdout",
) -> ModelResult:
    valid = _valid_subset(table_run_ids, backends, modes, scenarios, matrices)
    X = valid["X"]
    Y = valid["Y"]
    valid_indices = valid["valid_indices"]
    run_ids_valid = valid["run_ids"]
    backends_valid = valid["backends"]
    modes_valid = valid["modes"]
    scenarios_valid = valid["scenarios"]

    train_indices = np.asarray(train_valid_indices, dtype=int)
    test_indices = np.asarray(test_valid_indices, dtype=int)
    if train_indices.ndim != 1 or test_indices.ndim != 1:
        raise ValueError("train_valid_indices/test_valid_indices 必须是一维索引。")
    if len(train_indices) == 0:
        raise ValueError("显式 holdout split 至少需要一个 train 样本。")
    if len(test_indices) == 0:
        raise ValueError("显式 holdout split 至少需要一个 test 样本。")

    train_matrices = type(matrices)(
        X=X[train_indices],
        Y=Y[train_indices],
        feature_names=matrices.feature_names,
        response_names=matrices.response_names,
        valid_mask=np.ones(len(train_indices), dtype=bool),
        schema_metadata=dict(matrices.schema_metadata),
    )
    trained = fit_schema_combo(
        [run_ids_valid[index] for index in train_indices],
        [backends_valid[index] for index in train_indices],
        [modes_valid[index] for index in train_indices],
        [scenarios_valid[index] for index in train_indices],
        train_matrices,
        config,
        model_name,
    )

    predictions = _predict(X[test_indices], trained.coefficient_matrix, trained.bias_vector)
    holdout_metrics = _metrics_bundle(Y[test_indices], predictions)
    summary = dict(trained.summary)
    summary.update(
        {
            f"{split_name}_test_r2": holdout_metrics["r2"],
            f"{split_name}_test_mse": holdout_metrics["mse"],
            f"{split_name}_test_mae": holdout_metrics["mae"],
            f"{split_name}_sample_count": int(len(test_indices)),
            f"{split_name}_scenarios": sorted({scenarios_valid[index] for index in test_indices if scenarios_valid[index]}),
            f"{split_name}_modes": sorted({modes_valid[index] for index in test_indices if modes_valid[index]}),
        }
    )

    residual_rows: list[dict[str, Any]] = []
    for row_offset, sample_index in enumerate(test_indices):
        residual_rows.append(
            {
                "sample_index": int(valid_indices[sample_index]),
                "backend": backends_valid[sample_index],
                "mode": modes_valid[sample_index],
                "scenario": scenarios_valid[sample_index],
                "run_id": run_ids_valid[sample_index],
                "target_norm": float(np.linalg.norm(Y[test_indices][row_offset])),
                "prediction_norm": float(np.linalg.norm(predictions[row_offset])),
                "residual_norm": float(np.linalg.norm(Y[test_indices][row_offset] - predictions[row_offset])),
            }
        )

    return ModelResult(
        summary=summary,
        coefficient_matrix=trained.coefficient_matrix,
        bias_vector=trained.bias_vector,
        sparsity_mask=trained.sparsity_mask,
        residual_rows=residual_rows,
    )
