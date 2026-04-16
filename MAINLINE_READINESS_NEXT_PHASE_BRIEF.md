# 主线 Readiness Confirmation + Next-Phase Analysis Brief

## 一句话结论

可以进入下一阶段，但要带边界：当前 Formal V2 主线 empirical validation 已足够可靠，足以从“线性关系是否存在/是否跨 scenario 成立”转入 in-depth analysis；ArduPilot targeted state-evolution 子线当前仍是 `inconclusive`，但它只阻塞更窄的 mode-isolated state-evolution 子问题，不阻塞主线前进。

## 1. Source-of-Truth 说明

- 最终口径按以下优先级执行：
  1. `docs/MILESTONE_LINEAR_F_REPORT.md`
  2. `docs/MILESTONE_LINEAR_F_APPENDIX.md`
  3. `docs/EXPERIMENT_PROTOCOL.md`
  4. 最新 Formal V2 artifact 报告与 summary JSON
  5. `README.md`
  6. `docs/RESEARCH_GOAL.md`
  7. `docs/DATA_SCHEMA.md`
  8. `docs/XY_SCHEMA_GUIDE.md`
  9. `docs/figures/heatmaps/README.md`
- `PJINFO.md` 已读取，文件非空，且与 milestone 口径一致，但仅作辅助理解，不替代 canonical 文档。
- 当前正式文档与主分析代码已经统一；generalization full study 的正式附加输出以 `scenario_generalization` 与 `sparsity_overlap` 为准。

## 2. 研究叙事复述

- 当前阶段不是写最终 paper，也不是做攻击算法；当前任务是把理论假设 `Y ≈ fX (+ b)` 先站稳成 empirical validation。
- 在仓库语境里：
  - `X` 是当前可用解释信息，如命令、状态、短历史、执行器反馈或其线性特征。
  - `Y` 是稍后要预测的响应，如 `next_raw_state`、`selected_state_subset`、`future_state_horizon`、`actuator_response`。
  - `f` 是固定矩阵，可理解为局部 Jacobian / influence matrix 式的线性作用。
- 同时跑 PX4 和 ArduPilot 的目的不是“比输赢”，而是在统一 schema、统一数据契约、统一判读口径下，验证线性关系本身是否可重复、是否跨 backend 仍然出现。

## 3. 术语口径

- `support`
  - 对单个组合当前 study 下是否达到可接受线性证据门槛的判读维度。
- `supported`
  - 该组合已经过线，可以作为“当前 study 下存在可接受线性 `f`”的证据。
- `supported_but_local`
  - overall 虽然 `supported`，但跨 scenario 不够稳，更像局部 operating point 结果。
- `generalized_supported`
  - 该组合不仅 `supported`，而且在 `nominal / dynamic / throttle_biased` 三档下都保持可接受且一致。
- `baseline_stability`
  - baseline 结果是否稳定到足以支撑更强 compare 结论；当前 compare 里 ArduPilot 这项仍未完全压实。
- `scenario_generalization`
  - 看 pooled 后的同一 `f` 是否还能跨三档 scenario 成立。
- `sparsity_overlap`
  - 看 sparse mask / dominant edges 在 baseline、diagnostic、加厚数据之间是否稳定重现。
- `diagnostic_gate`
  - 看 diagnostic 数据质量与 acceptance gate 是否过关，用来剔除“高分但边界动作/实验质量不稳”的结果。
- `state-evolution`
  - 输出是未来状态本身，如 `next_raw_state`、`selected_state_subset`、`future_state_horizon`。
- `actuator_response`
  - 输出是执行器层响应，不是完整状态演化。
- `mature_positive`
  - 至少一个 strict-raw-linear state-evolution 组合同时在 baseline、diagnostic 和 sparse-edge overlap 上保持稳定。
- `mature_negative`
  - 长期呈现“高 R2 + 高条件数 + 稳定 sparse edges”，足以成熟地下负结论。
- `inconclusive`
  - targeted line 已有正式 artifact，但还没有收敛到成熟正/负结论。

## 4. 主线 empirical validation 的完成度判断

### 事实

- milestone、appendix、compare JSON 和四个 generalization full study 一致表明，两 backend 都已出现 `generalized_supported` 组合。
- PX4 的 generalized-supported 范围更宽。
- ArduPilot 的 generalized-supported 结果更窄，但正式存在。

### 判断

- 主线已经足够进入 in-depth analysis，而且这个判断必须表述为“可以，但有边界”。
- 这里的“可以”意味着：
  - 主问题“线性关系存在且具有跨 scenario 正面证据”已经站稳。
  - 下一步应转向 insight extraction，而不是再回到 broad validation 起点。
- 这里的“边界”意味着：
  - 这不是“所有子问题都解决”。
  - backend 差异仍不能过度上升为最终主标题。
  - ArduPilot state-evolution 仍未成熟收敛。

### 置信度

- 主线 readiness：中高。
- targeted `inconclusive` 判读：高。

## 5. 主线已站稳的部分

- PX4 主线已不是孤立高分。
  - baseline `generalized_supported=80`
  - diagnostic `generalized_supported=111`
  - supported 组合数分别为 `120` 与 `126`
  - 代表组合都指向 `full_augmented | next_raw_state | ols_affine | stratified`
- ArduPilot 主线也不是“没有线性”。
  - baseline 与 diagnostic 都有 `generalized_supported=12`
  - 正式 supported 主集合集中在 `commands_only` pooled 路径
  - 代表锚点是 `commands_only | actuator_response | ridge_affine | pooled`
- compare 已明确支持：
  - `difference_driver=baseline_stability_unresolved`
  - `generalization_difference_driver=both_support_cross_scenario_linearity_but_px4_is_broader`
- 热力图与上述判读一致：
  - PX4 主图呈现可读的块状/带状与 lag 重复结构，说明主线已经进入“可读矩阵结构”的阶段。
  - ArduPilot 主线锚点几乎是单一 command-to-actuator 主边，说明其稳定证据更集中、更简单。

## 6. 主线仍未完全站稳的部分

- PX4 主线的更强结构解释仍要依赖 `scenario_generalization`、`sparsity_overlap` 与热力图联合阅读，不能只看 generalized-supported 计数。
- ArduPilot 的高分 state-evolution 路径仍未站稳。
  - generalization full baseline/diagnostic 的 best combo 都是 `commands_plus_state_history | selected_state_subset | ols_affine | pooled`
  - `median_test_r2=1.0000`
  - 但 `support=partial`
  - 主阻塞是超大 `effective_condition_number` 与 `condition_number/mixed`
  - 阻塞并不是 R2
- 不是所有高分都能进入正式主结论。
  - 典型反例是 ArduPilot 这些 `R2≈1` 的 state-evolution 组合。
  - 另一个反例是 targeted STABILIZE baseline 的单独正结果。
  - 它们都不能跳过 conditioning、diagnostic、scenario generalization 与 overlap。
- `supported_but_local` 仍存在于 PX4。
  - baseline 有 `40` 个
  - diagnostic 有 `15` 个
  - 它们不能当跨 scenario 主证据

## 7. ArduPilot targeted state-evolution 子线状态判断

### 事实

- targeted aggregate 的 `overall_status=mode_isolated_state_evolution_still_inconclusive`
- `STABILIZE=inconclusive`
- `GUIDED_NOGPS=inconclusive`
- STABILIZE baseline 一度出现：
  - `generalized_supported=10`
- 但 STABILIZE diagnostic 立刻降为：
  - `generalized_supported=0`
- GUIDED_NOGPS baseline 与 diagnostic 都是：
  - `generalized_supported=0`
  - 主阻塞稳定指向 `condition_number`

### 判断

- targeted 子线当前既不是 `mature_positive`，也不是 `mature_negative`，而是正式的 `inconclusive`。
- 这个结果不阻塞主线进入下一阶段。
- 它只阻塞“ArduPilot mode-isolated state-evolution 已成熟收敛”这一更窄结论。

## 8. 支持判断的核心证据

### PX4

- `artifacts/studies/20260410_224818_px4_real_generalization_ablation/reports/summary.md`
- `artifacts/studies/20260410_224818_px4_real_generalization_ablation/reports/scenario_generalization.md`
- `artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/study_summary.json`
- `artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/scenario_generalization.json`
- `artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/matrix_gallery.json`
- `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/reports/summary.md`
- `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/reports/scenario_generalization.md`
- `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/study_summary.json`
- `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/scenario_generalization.json`
- `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/matrix_gallery.json`

结论要点：

- 大面积 `supported` / `generalized_supported`
- 代表组合稳定落在 `next_raw_state` 主线
- mainline 不是单点高分

### ArduPilot generalization full

- `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/reports/summary.md`
- `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/reports/scenario_generalization.md`
- `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/reports/sparsity_overlap.md`
- `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/reports/state_evolution_audit.md`
- `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix/reports/summary.md`
- `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix/reports/scenario_generalization.md`
- `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix/reports/sparsity_overlap.md`
- `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix/reports/state_evolution_audit.md`

结论要点：

- 正式 supported 主集合只有 12 个 `commands_only` pooled 组合
- `supported_state_evolution=[]`
- 主阻塞是 `condition_number/mixed`

### targeted validation

- `artifacts/studies/20260413_134505_ardupilot_state_evolution_validation/reports/state_evolution_validation.md`
- `artifacts/studies/20260413_134505_ardupilot_state_evolution_validation/summary/state_evolution_validation.json`
- 四个 targeted study 下的：
  - `reports/summary.md`
  - `summary/scenario_generalization.json`
  - `summary/sparsity_overlap.json`
  - `summary/state_evolution_audit.json`

结论要点：

- STABILIZE 是“baseline 有正象，但 diagnostic 不复现”
- GUIDED_NOGPS 是“始终高分，但始终 partial”
- aggregate 正式给出 `inconclusive`

### compare

- `artifacts/studies/20260413_134755_px4_vs_ardupilot_compare/reports/backend_compare.md`
- `artifacts/studies/20260413_134755_px4_vs_ardupilot_compare/summary/backend_compare.json`

你要求显式读取的字段全部支持当前口径：

- `comparison.difference_driver=baseline_stability_unresolved`
- `comparison.generalization_difference_driver=both_support_cross_scenario_linearity_but_px4_is_broader`
- `px4.baseline.scenario_generalization={80,40,96}`
- `px4.diagnostic.scenario_generalization={111,15,90}`
- `ardupilot.baseline.scenario_generalization={12,0,204}`
- `ardupilot.diagnostic.scenario_generalization={12,0,204}`

## 9. 为什么现在可以进入下一阶段

- 因为主问题已经从“有没有线性”升级成了“这些已成立的线性结构到底是什么”。
- 因为两 backend 都已经给出跨 scenario 的正式正面证据，主线不再依赖单 backend、单 scenario、单组合。
- 因为剩余不确定性主要是机制归因，不是 existence 判定。
- 因为 targeted 子线的 unresolved 是窄问题，继续盲目扩 broad validation 的边际收益已经低于读透现有矩阵。

## 10. 如果进入下一阶段，最该优先做的 5 个 in-depth analysis 任务

1. 系统阅读所有 `generalized_supported` 组合的 `matrix_f`，按命令块、当前状态块、历史 lag 块拆解 dominant edges。
2. 在 PX4 主线里显式区分“物理映射”与“状态延续”：比较 command-to-future、state-to-same-state、lag-to-future 的相对贡献与重复图案。
3. 做 backend-shared / backend-specific 结构对齐：在可比 schema 上比较 dominant edges，而不是只比较计数。
4. 专门分析 ArduPilot state-evolution 的 conditioning 失败机理：把 `conditioning_pruned_features`、`effective_condition_number`、`support` 降级路径和 heatmap 一起读。
5. 做 stability-boundary analysis：围绕 `generalized_supported` 与 `partial/not_generalized` 的边界组合，解释到底是 throttle、stratification、mode mixture 还是 feature collinearity 触发退化。

## 11. 当前阶段的主要研究风险

- 把“PX4 更宽”过度表述成 backend 胜负；当前 compare 明确不支持这么写。
- 把 ArduPilot 的高 R2 partial state-evolution 误写成正式正结论。
- 把 `sparsity_overlap` 单独当成正结论；它必须和基础 `support` 与 `scenario_generalization` 一起读。
- 忽略 targeted line 仍是 `inconclusive`，导致 state-evolution 表述过满。

## 12. 建议给 PI / 老师汇报时如何表述

- 当前 Formal V2 已经把“统一 schema 下固定线性/仿射映射 `Y ≈ fX (+ b)` 存在，且不只限于 nominal，而在三档 scenario 下有跨场景证据”作为正式结论站稳。
- PX4 的 generalized-supported 组合更宽。
- ArduPilot 的正式证据更集中在 `commands_only -> actuator_response`。
- 需要同步加一句边界：
  - ArduPilot mode-isolated state-evolution targeted line 已完成正式验证，但目前仍是 `inconclusive`。
  - 这不推翻主线 readiness，只说明更窄的 state-evolution 子问题尚未成熟收敛。

## 13. 证据来源清单

### 文档

- `README.md`
- `PJINFO.md`
- `docs/MILESTONE_LINEAR_F_REPORT.md`
- `docs/MILESTONE_LINEAR_F_APPENDIX.md`
- `docs/RESEARCH_GOAL.md`
- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/DATA_SCHEMA.md`
- `docs/XY_SCHEMA_GUIDE.md`
- `docs/figures/heatmaps/README.md`

### compare

- `artifacts/studies/20260413_134755_px4_vs_ardupilot_compare/reports/backend_compare.md`
- `artifacts/studies/20260413_134755_px4_vs_ardupilot_compare/summary/backend_compare.json`

### PX4 baseline

- `artifacts/studies/20260410_224818_px4_real_generalization_ablation/reports/summary.md`
- `artifacts/studies/20260410_224818_px4_real_generalization_ablation/reports/scenario_generalization.md`
- `artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/study_summary.json`
- `artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/scenario_generalization.json`
- `artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/matrix_gallery.json`
- `artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/baseline_stability.json`
- `artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/diagnostic_gate.json`
- `artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/state_evolution_audit.json`

### PX4 diagnostic

- `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/reports/summary.md`
- `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/reports/scenario_generalization.md`
- `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/study_summary.json`
- `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/scenario_generalization.json`
- `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/matrix_gallery.json`
- `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/baseline_stability.json`
- `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/diagnostic_gate.json`
- `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/state_evolution_audit.json`

### ArduPilot generalization full

- `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/reports/summary.md`
- `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/reports/scenario_generalization.md`
- `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/reports/sparsity_overlap.md`
- `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/reports/state_evolution_audit.md`
- `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix/reports/summary.md`
- `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix/reports/scenario_generalization.md`
- `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix/reports/sparsity_overlap.md`
- `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix/reports/state_evolution_audit.md`
- 对应的 `summary/*.json`

### targeted aggregate

- `artifacts/studies/20260413_134505_ardupilot_state_evolution_validation/reports/state_evolution_validation.md`
- `artifacts/studies/20260413_134505_ardupilot_state_evolution_validation/summary/state_evolution_validation.json`

### 四个 targeted study

- `artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline`
- `artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic`
- `artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline`
- `artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic`
- 已实际使用其中的：
  - `reports/summary.md`
  - `summary/scenario_generalization.json`
  - `summary/sparsity_overlap.json`
  - `summary/state_evolution_audit.json`

### 热力图

- `docs/figures/heatmaps/px4_baseline_generalized_main_abs.png`
- `docs/figures/heatmaps/ardupilot_full_baseline_main_abs.png`
- `docs/figures/heatmaps/ardupilot_targeted_stabilize_abs.png`
- `docs/figures/heatmaps/ardupilot_targeted_guided_nogps_abs.png`
