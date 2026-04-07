from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from .canonical import ACTUATOR_COLUMNS, STATE_COLUMNS
from .config import StudyConfig
from .io import ensure_raw_run_directories, write_rows_csv, write_yaml


def _parameter_row(config: StudyConfig) -> dict[str, float]:
    overrides = config.parameter_overrides_for_backend("synthetic")
    if overrides:
        return {f"param_{name}": float(value) for name, value in overrides.items()}
    return {"param_ctrl_p": 0.18, "param_ctrl_d": 0.03}


def generate_synthetic_raw_runs(config: StudyConfig, output_root: Path | None = None) -> list[Path]:
    sample_count = int(config.synthetic.get("sample_count", 480))
    noise_std = float(config.synthetic.get("noise_std", 0.03))
    state_scale = float(config.synthetic.get("state_scale", 0.8))
    actuator_scale = float(config.synthetic.get("actuator_scale", 0.4))
    backend_cycle = config.synthetic.get("backend_identity_cycle", ["px4", "ardupilot"])
    mode_cycle = config.synthetic.get("mode_cycle", ["POSCTL", "STABILIZE"])
    seed_offset = int(config.synthetic.get("seed_offset", 0))
    parameter_row = _parameter_row(config)

    raw_dirs: list[Path] = []
    for repeat_index in range(1, config.repeat_count + 1):
        run_config = config.with_repeat_index(repeat_index)
        run_id = run_config.build_run_id(datetime.now(timezone.utc).astimezone(), repeat_index=repeat_index)
        paths = ensure_raw_run_directories("synthetic", run_id, root=output_root)
        rng = np.random.default_rng(run_config.seed + seed_offset + repeat_index)
        commands = rng.normal(0.0, 0.5, size=(sample_count, 4))
        params = np.column_stack([np.full(sample_count, value) for value in parameter_row.values()])
        states = np.zeros((sample_count, len(STATE_COLUMNS)), dtype=float)
        backend_identity = backend_cycle[(repeat_index - 1) % len(backend_cycle)]
        mode_identity = mode_cycle[(repeat_index - 1) % len(mode_cycle)]

        feature_count = 4 + len(STATE_COLUMNS) + params.shape[1]
        density = float(run_config.synthetic.get("sparse_matrix_density", 0.20))
        mask = rng.random((feature_count, len(STATE_COLUMNS))) < density
        transition = rng.normal(0.0, state_scale, size=(feature_count, len(STATE_COLUMNS))) * mask
        bias = rng.normal(0.0, 0.1, size=(len(STATE_COLUMNS),))

        for index in range(sample_count - 1):
            feature = np.concatenate([commands[index], states[index], params[index]])
            delta = feature @ transition + bias + rng.normal(0.0, noise_std, size=(len(STATE_COLUMNS),))
            states[index + 1] = states[index] + delta * 0.1

        rows: list[dict[str, Any]] = []
        start_timestamp_ns = int(datetime.now(timezone.utc).timestamp() * 1_000_000_000)
        for index in range(sample_count):
            row = {
                "sample_id": f"{run_id}:{index:06d}",
                "run_id": run_id,
                "backend": backend_identity,
                "mode": mode_identity,
                "scenario": run_config.scenario,
                "config_profile": run_config.config_profile,
                "seed": run_config.seed,
                "timestamp": start_timestamp_ns + int(index * run_config.period_s * 1_000_000_000),
                "logical_step": index,
                "command_roll": float(commands[index, 0]),
                "command_pitch": float(commands[index, 1]),
                "command_yaw": float(commands[index, 2]),
                "command_throttle": float(commands[index, 3]),
            }
            for state_index, name in enumerate(STATE_COLUMNS):
                row[name] = float(states[index, state_index])
            row["integrator_roll"] = float(0.2 * states[index, 3])
            row["integrator_pitch"] = float(0.2 * states[index, 4])
            row["integrator_yaw"] = float(0.2 * states[index, 5])
            row["control_output_roll"] = float(0.3 * commands[index, 0] + 0.1 * states[index, 3])
            row["control_output_pitch"] = float(0.3 * commands[index, 1] + 0.1 * states[index, 4])
            row["control_output_yaw"] = float(0.3 * commands[index, 2] + 0.1 * states[index, 5])
            row["torque_achieved"] = float(1.0 - min(0.8, abs(commands[index, 0]) * 0.1))
            row["thrust_achieved"] = float(1.0 - min(0.8, abs(commands[index, 3]) * 0.1))
            row["saturation_ratio"] = float(np.clip(np.mean(np.abs(commands[index])) * 0.4, 0.0, 1.0))
            row["tracking_error_roll"] = float(0.1 * commands[index, 0] - 0.05 * states[index, 0])
            row["tracking_error_pitch"] = float(0.1 * commands[index, 1] - 0.05 * states[index, 1])
            row["tracking_error_yaw"] = float(0.1 * commands[index, 2] - 0.05 * states[index, 2])
            row["tracking_error_rate_roll"] = float(0.1 * commands[index, 0] - 0.05 * states[index, 3])
            row["tracking_error_rate_pitch"] = float(0.1 * commands[index, 1] - 0.05 * states[index, 4])
            row["tracking_error_rate_yaw"] = float(0.1 * commands[index, 2] - 0.05 * states[index, 5])
            for actuator_index, column in enumerate(ACTUATOR_COLUMNS):
                row[column] = float(np.clip(0.5 + actuator_scale * commands[index, actuator_index % 4], 0.0, 1.0))
            row["tracking_error_magnitude"] = float(
                np.linalg.norm(
                    [
                        row["tracking_error_roll"],
                        row["tracking_error_pitch"],
                        row["tracking_error_yaw"],
                        row["tracking_error_rate_roll"],
                        row["tracking_error_rate_pitch"],
                        row["tracking_error_rate_yaw"],
                    ]
                )
            )
            row["control_effort_magnitude"] = float(np.mean([row[column] for column in ACTUATOR_COLUMNS]))
            for name, value in parameter_row.items():
                row[name] = float(value)
            rows.append(row)

        write_rows_csv(paths["canonical_samples_path"], rows)
        manifest = {
            "kind": "linearity_raw_run",
            "raw_schema_version": 1,
            "run_id": run_id,
            "backend": "synthetic",
            "status": "completed",
            "study_name": run_config.study_name,
            "flight_mode": run_config.mode_under_test_for_backend("synthetic"),
            "scenario": run_config.scenario,
            "config_profile": run_config.config_profile,
            "seed": run_config.seed,
            "repeat_index": repeat_index,
            "telemetry_files": ["analysis_inputs/canonical_samples.csv"],
            "parameter_snapshot_before": parameter_row,
            "parameter_snapshot_after": parameter_row,
            "synthetic_ground_truth": {
                "state_transition_shape": [int(transition.shape[0]), int(transition.shape[1])],
                "density": density,
                "noise_std": noise_std,
            },
            "study_config": run_config.to_dict(),
        }
        write_yaml(paths["manifest_path"], manifest)
        paths["notes_path"].write_text(
            "\n".join(
                [
                    f"# {run_id}",
                    "- synthetic backend raw run",
                    f"- backend_identity: {backend_identity}",
                    f"- mode_identity: {mode_identity}",
                    f"- sample_count: {sample_count}",
                ]
            ),
            encoding="utf-8",
        )
        raw_dirs.append(paths["base_dir"])
    return raw_dirs
