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

`manifest.yaml` 承载跨 backend 的 research contract：

- `raw_schema_version`
- `research_tier`
- `research_acceptance`
- `research_rejection_reasons`
- `data_quality`

其中 `data_quality.acceptance` 的共享字段固定为：

- `experiment_started`
- `active_phase_present`
- `expected_active_samples`
- `active_sample_count`
- `active_nonzero_command_samples`
- `failsafe_during_experiment`
- `missing_topics_blocking`
- `accepted`
- `rejection_reasons`

## Prepared Sample Table

prepared sample table 放在：

- `artifacts/studies/<study_id>/prepared/sample_table.csv`

头部身份列顺序固定为：

- `sample_id`
- `run_id`
- `backend`
- `mode`
- `scenario`
- `config_profile`
- `research_tier`
- `research_acceptance`
- `seed`
- `timestamp`
- `logical_step`

one-hot / 参数前缀固定为：

- `backend_`
- `mode_`
- `scenario_`
- `config_profile_`
- `param_`

### `scenario` 在当前正式 study 里的角色

在当前 `generalization full` 正式 study 里，`scenario` 有两层作用：

1. 它是 prepared sample table 的固定身份列，用来标识样本来自 `nominal / dynamic / throttle_biased` 哪一档状态。
2. 它是 subgroup 报告维度，用来判断“同一个 `f` 是否跨 scenario 站得住”。

这意味着：

- `scenario` 仍然会出现在 prepared table 中；
- 但 formal generalization study 不依赖把 `scenario_` one-hot 混进正式 `X`，因为我们要验证的是“同一个 `f` 能不能跨 scenario 工作”，不是让模型直接记住 scenario 标签。

## Fit Artifact

每个 `X-schema × Y-schema × pooling_mode × model` 输出：

- `matrix_f.csv`
- `bias_b.csv`
- `sparsity_mask.csv`
- `metrics.json`
- `residuals.csv`

在 current generalization study 里，`metrics.json` 还会带：

- `scenario_consistency`
- `scenario_subgroup_metrics`

它们分别回答：

- 这个组合跨三档 scenario 是否一致；
- 每个 scenario 单独看时，`r2 / mse / mae` 分别是多少。

## Summary Artifact

study 级别输出：

- `reports/summary.md`
- `reports/schema_comparison.md`
- `reports/baseline_stability.md`
- `reports/diagnostic_gate.md`
- `reports/matrix_gallery.md`
- `reports/scenario_generalization.md`
- `summary/study_summary.json`
- `summary/baseline_stability.json`
- `summary/diagnostic_gate.json`
- `summary/matrix_gallery.json`
- `summary/scenario_generalization.json`
- `prepared/schema_inventory.yaml`

### `scenario_generalization` 的含义

`reports/scenario_generalization.md` / `summary/scenario_generalization.json` 只回答四件事：

- 哪些组合在三档 scenario pooled 后仍是 `generalized_supported`
- 哪些组合只是 `supported_but_local`
- 哪些组合 overall 不是 `supported`
- 当前 `f` 更像“跨状态常见映射”还是“局部 operating-point 映射”

这份产物不会改写 `supported / partial / unsupported` 的原始门槛；它是在原有 support 判读之外，再补一层“跨 scenario 是否站得住”的解释。

### `matrix_gallery` 的含义

`reports/matrix_gallery.md` / `summary/matrix_gallery.json` 会枚举当前 study 里所有 `support == supported` 的组合，并给出：

- `matrix_f.csv`
- `matrix_heatmap_abs.png`
- `matrix_heatmap_signed.png`

如果当前 study 没有任何 `supported` 组合，则会明确写出“该 study 未得到可接受的全局线性 f，因此没有矩阵图册”。
