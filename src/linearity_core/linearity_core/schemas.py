from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np

from .canonical import (
    ACTUATOR_COLUMNS,
    BACKEND_PREFIX,
    COMMAND_COLUMNS,
    CONFIG_PROFILE_PREFIX,
    CONTROLLER_PARAM_PREFIX,
    INTERNAL_COLUMNS,
    MODE_PREFIX,
    SCENARIO_PREFIX,
    STATE_COLUMNS,
    STATE_SUBSET_COLUMNS,
    STRICT_RAW_X_SCHEMAS,
    TRACKING_ERROR_COLUMNS,
)
from .config import StudyConfig
from .dataset import PreparedSampleTable


def _unique_in_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            ordered.append(item)
            seen.add(item)
    return ordered


def _dynamic_group_columns(table: PreparedSampleTable, prefix: str) -> list[str]:
    return [name for name in table.numeric_columns if name.startswith(prefix)]


def _filter_available_table_columns(
    table: PreparedSampleTable,
    columns: list[str],
) -> tuple[list[str], list[str], dict[str, float]]:
    available: list[str] = []
    dropped: list[str] = []
    partial: dict[str, float] = {}
    total_rows = max(1, len(table.rows))
    for name in _unique_in_order(columns):
        if name not in table.numeric_columns:
            dropped.append(name)
            continue
        values = table.column(name)
        finite_count = int(np.sum(np.isfinite(values)))
        if finite_count <= 0:
            dropped.append(name)
            continue
        available.append(name)
        if finite_count < total_rows:
            partial[name] = float(finite_count / total_rows)
    return available, dropped, partial


def _filter_available_matrix_columns(
    matrix: np.ndarray,
    names: list[str],
) -> tuple[np.ndarray, list[str], list[str], dict[str, float]]:
    if matrix.size == 0 or not names:
        return matrix[:, :0], [], list(names), {}
    finite_mask = np.isfinite(matrix)
    finite_counts = np.sum(finite_mask, axis=0)
    keep_mask = finite_counts > 0
    available_names = [name for name, keep in zip(names, keep_mask) if keep]
    dropped_names = [name for name, keep in zip(names, keep_mask) if not keep]
    partial: dict[str, float] = {}
    total_rows = max(1, matrix.shape[0])
    for name, count, keep in zip(names, finite_counts, keep_mask):
        if keep and count < total_rows:
            partial[name] = float(count / total_rows)
    if not np.any(keep_mask):
        return matrix[:, :0], [], dropped_names, partial
    return matrix[:, keep_mask], available_names, dropped_names, partial


def _controller_param_columns(table: PreparedSampleTable) -> list[str]:
    return _dynamic_group_columns(table, CONTROLLER_PARAM_PREFIX)


def _backend_mode_columns(table: PreparedSampleTable) -> list[str]:
    prefixes = (BACKEND_PREFIX, MODE_PREFIX, SCENARIO_PREFIX, CONFIG_PROFILE_PREFIX)
    return [name for name in table.numeric_columns if name.startswith(prefixes)]


def _history_columns(table: PreparedSampleTable, base_columns: list[str], run_ids: list[str], history_length: int) -> tuple[np.ndarray, list[str]]:
    if history_length <= 0:
        return np.empty((len(table.rows), 0)), []
    values = np.column_stack([table.column(name) for name in base_columns]) if base_columns else np.empty((len(table.rows), 0))
    if values.size == 0:
        return np.empty((len(table.rows), 0)), []
    history_blocks: list[np.ndarray] = []
    history_names: list[str] = []
    run_ids_array = np.asarray(run_ids, dtype=object)
    for lag in range(1, history_length + 1):
        shifted = np.full_like(values, fill_value=np.nan, dtype=float)
        same_run = run_ids_array[lag:] == run_ids_array[:-lag]
        shifted[lag:][same_run] = values[:-lag][same_run]
        history_blocks.append(shifted)
        history_names.extend([f"{name}__lag_{lag}" for name in base_columns])
    return np.hstack(history_blocks), history_names


def _apply_feature_map(
    X: np.ndarray,
    feature_names: list[str],
    table: PreparedSampleTable,
    config: StudyConfig,
    x_schema: str,
) -> tuple[np.ndarray, list[str], dict[str, Any]]:
    if x_schema != "feature_mapped_linear":
        return X, feature_names, {"strict_raw_linear": x_schema in STRICT_RAW_X_SCHEMAS}

    mapped_blocks = [X]
    mapped_names = list(feature_names)
    for index, name in enumerate(feature_names):
        if name.startswith("command_"):
            clipped = np.clip(X[:, index], -0.5, 0.5)
            mapped_blocks.append(clipped.reshape(-1, 1))
            mapped_names.append(f"clip__{name}")
            squared = np.square(X[:, index])
            mapped_blocks.append(squared.reshape(-1, 1))
            mapped_names.append(f"sq__{name}")
        if name in {"roll", "pitch", "yaw", "roll_rate", "pitch_rate", "yaw_rate"}:
            squared = np.square(X[:, index])
            mapped_blocks.append(squared.reshape(-1, 1))
            mapped_names.append(f"sq__{name}")

    backend_columns = [name for name in table.numeric_columns if name.startswith(BACKEND_PREFIX)]
    for backend_name in backend_columns:
        backend_vector = table.column(backend_name)
        for index, name in enumerate(feature_names):
            if name.startswith("command_"):
                gated = backend_vector * X[:, index]
                mapped_blocks.append(gated.reshape(-1, 1))
                mapped_names.append(f"{backend_name}__{name}")

    return np.hstack(mapped_blocks), mapped_names, {"strict_raw_linear": False}


def _drop_invalid_rows(X: np.ndarray, Y: np.ndarray, run_ids: list[str]) -> np.ndarray:
    if X.size == 0 or Y.size == 0:
        return np.zeros(len(run_ids), dtype=bool)
    return np.all(np.isfinite(X), axis=1) & np.all(np.isfinite(Y), axis=1)


@dataclass(slots=True)
class SchemaMatrices:
    X: np.ndarray
    Y: np.ndarray
    feature_names: list[str]
    response_names: list[str]
    valid_mask: np.ndarray
    schema_metadata: dict[str, Any]


def available_x_schemas() -> list[str]:
    return [
        "commands_only",
        "commands_plus_state",
        "commands_plus_state_history",
        "commands_plus_controller_params",
        "commands_plus_state_plus_params",
        "pooled_backend_mode_augmented",
        "full_augmented",
        "feature_mapped_linear",
    ]


def available_y_schemas() -> list[str]:
    return [
        "next_raw_state",
        "delta_state",
        "selected_state_subset",
        "future_state_horizon",
        "actuator_response",
        "tracking_error_response",
        "window_summary_response",
        "stability_proxy_response",
    ]


def _resolve_feature_columns(table: PreparedSampleTable, config: StudyConfig, x_schema: str) -> list[str]:
    groups: list[str] = []
    if x_schema == "commands_only":
        groups = ["commands"]
    elif x_schema == "commands_plus_state":
        groups = ["commands", "state"]
    elif x_schema == "commands_plus_state_history":
        groups = ["commands", "state"]
    elif x_schema == "commands_plus_controller_params":
        groups = ["commands", "controller_params"]
    elif x_schema == "commands_plus_state_plus_params":
        groups = ["commands", "state", "controller_params"]
    elif x_schema == "pooled_backend_mode_augmented":
        groups = ["commands", "state", "backend_mode"]
    elif x_schema == "full_augmented":
        groups = ["commands", "state", "controller_params", "backend_mode", "internal", "actuator_feedback"]
    elif x_schema == "feature_mapped_linear":
        groups = ["commands", "state", "backend_mode"]
    else:
        raise ValueError(f"未知 x_schema: {x_schema}")

    groups.extend(config.x_include_groups)
    groups = [group for group in groups if group not in set(config.x_exclude_groups)]
    feature_columns: list[str] = []
    for group in groups:
        if group == "commands":
            feature_columns.extend(COMMAND_COLUMNS)
        elif group == "state":
            feature_columns.extend(STATE_COLUMNS)
        elif group == "controller_params":
            feature_columns.extend(_controller_param_columns(table))
        elif group == "backend_mode":
            feature_columns.extend(_backend_mode_columns(table))
        elif group == "internal":
            feature_columns.extend([name for name in INTERNAL_COLUMNS if name in table.numeric_columns])
        elif group == "actuator_feedback":
            feature_columns.extend([name for name in ACTUATOR_COLUMNS if name in table.numeric_columns])
    if isinstance(config.run_level_covariates_as_inputs, bool) and config.run_level_covariates_as_inputs:
        feature_columns.extend(_controller_param_columns(table))
        feature_columns.extend(_backend_mode_columns(table))
    elif isinstance(config.run_level_covariates_as_inputs, list):
        feature_columns.extend([name for name in table.numeric_columns if name in config.run_level_covariates_as_inputs])
    return [name for name in _unique_in_order(feature_columns) if name in table.numeric_columns]


def _resolve_response_columns(table: PreparedSampleTable, config: StudyConfig, y_schema: str) -> list[str]:
    if y_schema in {"next_raw_state", "delta_state"}:
        columns = list(STATE_COLUMNS)
    elif y_schema == "selected_state_subset":
        if config.output_semantics == "delta_state":
            columns = [f"delta_state_{name}" for name in STATE_SUBSET_COLUMNS]
        elif config.output_semantics in {"current_raw_state", "raw_state"}:
            columns = list(STATE_SUBSET_COLUMNS)
        else:
            columns = [f"future_state_{name}" for name in STATE_SUBSET_COLUMNS]
    elif y_schema == "actuator_response":
        columns = [name for name in ACTUATOR_COLUMNS if name in table.numeric_columns]
    elif y_schema == "tracking_error_response":
        columns = [name for name in TRACKING_ERROR_COLUMNS if name in table.numeric_columns]
    elif y_schema == "window_summary_response":
        columns = [f"window_mean_{name}" for name in STATE_SUBSET_COLUMNS] + [f"window_peak_{name}" for name in STATE_SUBSET_COLUMNS]
    elif y_schema == "stability_proxy_response":
        columns = ["saturation_ratio", "control_effort_magnitude", "tracking_error_magnitude"]
    else:
        columns = list(STATE_SUBSET_COLUMNS)
    for group in config.y_include_groups:
        if group == "raw_state":
            columns.extend(STATE_COLUMNS)
        elif group == "selected_state_subset":
            columns.extend(STATE_SUBSET_COLUMNS)
        elif group == "actuator":
            columns.extend(ACTUATOR_COLUMNS)
        elif group == "tracking_error":
            columns.extend(TRACKING_ERROR_COLUMNS)
    columns = [name for name in _unique_in_order(columns) if name not in set(config.y_exclude_groups)]
    return [name for name in columns if name in table.numeric_columns or name.startswith("window_") or name.startswith("future_state_") or name.startswith("delta_state_")]


def build_schema_matrices(table: PreparedSampleTable, config: StudyConfig, x_schema: str, y_schema: str) -> SchemaMatrices:
    run_ids = table.string_column("run_id")
    requested_feature_columns = _resolve_feature_columns(table, config, x_schema)
    feature_columns, dropped_unavailable_features, partial_feature_columns = _filter_available_table_columns(
        table,
        requested_feature_columns,
    )
    base_X = np.column_stack([table.column(name) for name in feature_columns]) if feature_columns else np.empty((len(table.rows), 0))
    history_source_columns = [name for name in feature_columns if name.startswith("command_") or name in STATE_COLUMNS]
    history_block, history_names = _history_columns(table, history_source_columns, run_ids, config.history_length if x_schema in {"commands_plus_state_history", "full_augmented"} else 0)
    X = base_X if history_block.size == 0 else np.hstack([base_X, history_block])
    feature_names = feature_columns + history_names
    X, feature_names, feature_map_metadata = _apply_feature_map(X, feature_names, table, config, x_schema)

    dropped_unavailable_responses: list[str] = []
    partial_response_columns: dict[str, float] = {}
    requested_response_columns: list[str] = []
    if y_schema == "next_raw_state":
        requested_response_names = [f"future_state_{name}" for name in STATE_COLUMNS]
        requested_response_columns = list(requested_response_names)
        response_names, dropped_unavailable_responses, partial_response_columns = _filter_available_table_columns(
            table,
            requested_response_names,
        )
        Y = np.column_stack([table.column(name) for name in response_names]) if response_names else np.empty((len(table.rows), 0))
    elif y_schema == "delta_state":
        requested_response_names = [f"delta_state_{name}" for name in STATE_COLUMNS]
        requested_response_columns = list(requested_response_names)
        response_names, dropped_unavailable_responses, partial_response_columns = _filter_available_table_columns(
            table,
            requested_response_names,
        )
        Y = np.column_stack([table.column(name) for name in response_names]) if response_names else np.empty((len(table.rows), 0))
    elif y_schema == "future_state_horizon":
        block_names: list[str] = []
        blocks: list[np.ndarray] = []
        for horizon in range(1, config.prediction_horizon + 1):
            future_columns = []
            for name in STATE_SUBSET_COLUMNS:
                current = table.column(name)
                shifted = np.full_like(current, fill_value=np.nan, dtype=float)
                for index in range(len(current) - horizon):
                    if run_ids[index] == run_ids[index + horizon]:
                        shifted[index] = current[index + horizon]
                blocks.append(shifted.reshape(-1, 1))
                future_columns.append(f"{name}__h{horizon}")
            block_names.extend(future_columns)
        requested_response_columns = list(block_names)
        response_names = block_names
        Y = np.hstack(blocks) if blocks else np.empty((len(table.rows), 0))
        Y, response_names, dropped_unavailable_responses, partial_response_columns = _filter_available_matrix_columns(Y, response_names)
    else:
        requested_response_columns = _resolve_response_columns(table, config, y_schema)
        response_names, dropped_unavailable_responses, partial_response_columns = _filter_available_table_columns(
            table,
            requested_response_columns,
        )
        Y = np.column_stack([table.column(name) for name in response_names]) if response_names else np.empty((len(table.rows), 0))

    leakage_features = [name for name in feature_names if name in set(response_names)]
    if leakage_features:
        keep_mask = np.asarray([name not in set(response_names) for name in feature_names], dtype=bool)
        X = X[:, keep_mask] if X.size else X[:, :0]
        feature_names = [name for name, keep in zip(feature_names, keep_mask) if keep]

    valid_mask = _drop_invalid_rows(X, Y, run_ids)
    return SchemaMatrices(
        X=X,
        Y=Y,
        feature_names=feature_names,
        response_names=response_names,
        valid_mask=valid_mask,
        schema_metadata={
            "x_schema": x_schema,
            "y_schema": y_schema,
            "feature_count": len(feature_names),
            "response_count": len(response_names),
            "strict_raw_linear": feature_map_metadata["strict_raw_linear"],
            "requested_feature_columns": requested_feature_columns,
            "requested_response_columns": requested_response_columns,
            "dropped_unavailable_features": dropped_unavailable_features,
            "dropped_unavailable_responses": dropped_unavailable_responses,
            "partial_feature_columns": partial_feature_columns,
            "partial_response_columns": partial_response_columns,
            "dropped_response_leakage_features": leakage_features,
        },
    )
