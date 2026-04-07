# Data Schema

## Raw Run

raw run 放在：

- `artifacts/raw/<backend>/<run_id>/`

最小结构：

- `manifest.yaml`
- `telemetry/*.csv`
- `logs/`
- `metadata/`
- `analysis_inputs/`

synthetic backend 会直接写：

- `analysis_inputs/canonical_samples.csv`

## Prepared Sample Table

prepared sample table 放在：

- `artifacts/studies/<study_id>/prepared/sample_table.csv`

每条样本至少包含：

- `sample_id`
- `run_id`
- `backend`
- `mode`
- `scenario`
- `config_profile`
- `seed`
- `timestamp`
- `logical_step`
- `command_*`
- 当前状态列
- `future_state_*`
- `delta_state_*`
- `baseline_state_*`
- one-hot covariates
- `param_*`
- internal signal
- actuator / tracking error / proxy 列

## Fit Artifact

每个 `X-schema × Y-schema × pooling_mode × model` 输出：

- `matrix_f.csv`
- `bias_b.csv`
- `sparsity_mask.csv`
- `metrics.json`
- `residuals.csv`

## Summary Artifact

study 级别输出：

- `reports/summary.md`
- `reports/schema_comparison.md`
- `summary/study_summary.json`
- `prepared/schema_inventory.yaml`
