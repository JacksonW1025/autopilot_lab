# Data Schema

## Formal V2 Study Types

当前正式 artifact 分成三类：

- `generalization full` baseline / diagnostic
  回答“统一 schema 下的线性关系是否存在，以及它是否跨 scenario 成立”
- `ArduPilot targeted` baseline / diagnostic
  回答“mode-isolated state-evolution 在更窄配置里是否站得住”
- `ArduPilot targeted aggregate`
  汇总上面四个 targeted study，给出 `mature_positive / mature_negative / inconclusive`

在 Formal V2 之后，仓库里还新增了一组 `narrowing studies`。它们不再回答“线性是否存在”，而是回答“已经成立的主锚点能否被收窄成可执行 target 或可复现 response family”。

- `A2 readiness / target-scout / pair-target readiness`
- `A1 target-scout / family readiness / targeted reproduction`

## Raw Run

raw run 放在：

- `artifacts/raw/<backend>/<run_id>/`

保留策略：

- `artifacts/raw/**` 继续作为本地实验目录存在。
- 它不再是远端 Git 的长期跟踪集合；remote canonical 集合只保留 latest Formal V2 `artifacts/studies/**` 与正式文档。

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

在当前 Formal V2 study 里，`scenario` 有两层作用：

1. 它是 prepared sample table 的固定身份列，用来标识样本来自 `nominal / dynamic / throttle_biased` 哪一档状态。
2. 它是 subgroup 和 generalization 报告维度，用来判断“同一个 `f` 是否跨 scenario 站得住”。

这意味着：

- `scenario` 会一直保留在 prepared table 中；
- 但 formal study 不依赖把 `scenario_` one-hot 混进正式 `X`，因为我们要验证的是“同一个 `f` 能不能跨 scenario 工作”，不是让模型直接记住 scenario 标签。

## Fit Artifact

每个 `X-schema × Y-schema × pooling_mode × model` 输出：

- `matrix_f.csv`
- `bias_b.csv`
- `sparsity_mask.csv`
- `metrics.json`
- `residuals.csv`

如果当前组合被判成 `supported`，还会额外输出：

- `matrix_heatmap_abs.png`
- `matrix_heatmap_signed.png`

在 current Formal V2 study 里，`metrics.json` 还会带：

- `scenario_consistency`
- `scenario_subgroup_metrics`

它们分别回答：

- 这个组合跨三档 scenario 是否一致；
- 每个 scenario 单独看时，`r2 / mse / mae` 分别是多少。

## Summary Artifact

### Generalization Full / Targeted Study

study 级别正式输出：

- `reports/summary.md`
- `reports/schema_comparison.md`
- `reports/baseline_stability.md`
- `reports/diagnostic_gate.md`
- `reports/matrix_gallery.md`
- `reports/scenario_generalization.md`
- `reports/sparsity_overlap.md`
- `summary/study_summary.json`
- `summary/baseline_stability.json`
- `summary/diagnostic_gate.json`
- `summary/matrix_gallery.json`
- `summary/scenario_generalization.json`
- `summary/sparsity_overlap.json`
- `prepared/schema_inventory.yaml`

ArduPilot targeted study 额外输出：

- `reports/state_evolution_audit.md`
- `summary/state_evolution_audit.json`

### Targeted Aggregate

ArduPilot targeted aggregate 输出：

- `reports/state_evolution_validation.md`
- `summary/state_evolution_validation.json`

### Narrowing Studies

这类 study 通常不再产出 `prepared/` 与 `fits/`，而是直接消费已有 canonical study 或新的窄 matrix run，并输出：

- `reports/*.md`
- `summary/*.json`
- `tables/*.csv`
- `manifest.yaml`

当前已经落地的 narrowing artifact 类型包括：

- `a2_readiness`
- `a2_boundary_readiness`
- `a2_target_scout`
- `a2_pair_target_readiness`
- `a1_target_scout`
- `a1_family_readiness`
- `a1_roll_pitch_targeted_reproduction`

## Current Artifact Meanings

### `scenario_generalization`

`reports/scenario_generalization.md` / `summary/scenario_generalization.json` 回答四件事：

- 哪些组合在三档 scenario pooled 后仍是 `generalized_supported`
- 哪些组合只是 `supported_but_local`
- 哪些组合 overall 不是 `supported`
- 当前 `f` 更像“跨状态常见映射”还是“局部 operating-point 映射”

这份产物不会改写 `supported / partial / unsupported` 的原始门槛；它是在原有 support 判读之外，再补一层“跨 scenario 是否站得住”的解释。

### `sparsity_overlap`

`reports/sparsity_overlap.md` / `summary/sparsity_overlap.json` 回答：

- baseline 与 diagnostic 的 sparse mask 是否稳定
- current study 与更厚数据版本相比，主边是否基本不变

这里会正式输出：

- stable-mask `Jaccard`
- `intersection / union`
- `top_edge_overlap`
- `high_frequency_edge_overlap`
- dominant edge 列表

### `state_evolution_audit`

`reports/state_evolution_audit.md` / `summary/state_evolution_audit.json` 只在 ArduPilot study 中出现。它回答：

- 当前 `supported` 主集合有没有因为加厚数据而改变
- state-evolution 路径的主阻塞更像是 `R2`、条件数、还是 mode/mixture 问题

### `state_evolution_validation`

`reports/state_evolution_validation.md` / `summary/state_evolution_validation.json` 是 targeted aggregate。它给出：

- `overall_status`
- `STABILIZE` mode 的正式结论
- `GUIDED_NOGPS` mode 的正式结论
- 当前 targeted line 是：
  - `mature_positive`
  - `mature_negative`
  - `mode_isolated_state_evolution_still_inconclusive`

### `matrix_gallery`

`reports/matrix_gallery.md` / `summary/matrix_gallery.json` 会枚举当前 study 里所有 `support == supported` 的组合，并给出：

- `matrix_f.csv`
- `matrix_heatmap_abs.png`
- `matrix_heatmap_signed.png`

如果当前 study 没有任何 `supported` 组合，则会明确写出“该 study 未得到可接受的全局线性 f，因此没有矩阵图册”。

### `a2_target_scout`

`reports/a2_target_scout.md` / `summary/a2_target_scout.json` 回答：

- 当前 actuator 层还有哪些 target family 值得继续追
- 哪个 scenario / mode 下最值得继续 narrowing
- 当前推荐的 next target 是 collective 还是 pair/pattern

### `a2_pair_target_readiness`

`reports/a2_pair_target_readiness.md` / `summary/a2_pair_target_readiness.json` 回答：

- 选中的 pair target 是否已经稳定、可重复、具方向一致性
- 当前是否达到 `ready_for_pair_attack_v1`
- 当前 dominant direction 是什么

### `a1_target_scout`

`reports/a1_target_scout.md` / `summary/a1_target_scout.json` 回答：

- 在 PX4 A1 里，哪个 response family 最值得继续收窄
- 当前 continuation family 更像 attitude、yaw 还是位置/速度

### `a1_family_readiness`

`reports/a1_family_readiness.md` / `summary/a1_family_readiness.json` 回答：

- 选中的 response family 是否足够稳定到可以进入 reproduction
- 当前是否 `ready_for_reproduction_v1`

### `a1_roll_pitch_targeted_reproduction`

`reports/a1_roll_pitch_targeted_reproduction.md` / `summary/a1_roll_pitch_targeted_reproduction.json` 回答：

- `future_state_roll / future_state_pitch` 是否已经被压缩成 exact continuation scope
- 同轴 direct-share / lag-share / top-feature pattern 是否在 baseline 和 diagnostic 下保持稳定
