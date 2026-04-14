# Experiment Protocol

## 当前正式实验线

当前仓库的正式结论已经切换到 `Formal V2`。

它由两条同级正式线组成：

- generalization full：回答“线性关系是否存在，以及它是否能跨 scenario 成立”。
- ArduPilot targeted state-evolution validation：回答“在不混 mode 时，state-evolution 是否形成成熟正结论；否则是否可以成熟地下负结论”。

## 当前正式顺序

### PX4

1. 复用现有 generalization full baseline：`../artifacts/studies/20260410_224818_px4_real_generalization_ablation`
2. 复用现有 generalization full diagnostic：`../artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`

### ArduPilot

1. generalization full baseline：`../artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation`
2. generalization full diagnostic：`../artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix`
3. STABILIZE targeted baseline：`../artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline`
4. STABILIZE targeted diagnostic：`../artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic`
5. GUIDED_NOGPS targeted baseline：`../artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline`
6. GUIDED_NOGPS targeted diagnostic：`../artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic`
7. targeted validation aggregate：`../artifacts/studies/20260413_134505_ardupilot_state_evolution_validation`

## 历史完成项

以下内容已移出 Formal V2 正式文档引用集，不再作为当前正式 compare 主输入：

- `20260409` 的 broad baseline / diagnostic
- ArduPilot `GUIDED_NOGPS` smoke
- `STABILIZE` partial baseline
- `STABILIZE` throttle-only diagnostic
- cross-backend contract audit

## 当前正式输出物

每个 generalization full study 至少要输出：

- `reports/summary.md`
- `reports/scenario_generalization.md`
- `reports/scenario_holdout.md`
- `reports/sparsity_overlap.md`
- `summary/study_summary.json`
- `summary/scenario_generalization.json`
- `summary/scenario_holdout.json`
- `summary/sparsity_overlap.json`

每个 targeted study 额外要输出：

- `reports/state_evolution_audit.md`
- `summary/state_evolution_audit.json`

targeted 聚合还要输出：

- `reports/state_evolution_validation.md`
- `summary/state_evolution_validation.json`

## 当前结论口径

- `supported`：当前 study 中已经得到可接受的线性 `f`。
- `generalized_supported`：当前 `supported` 结果在多个 scenario 下仍然稳定成立。
- `all_holdouts_supported`：leave-one-scenario-out 之后仍然稳定通过。
- `mature_positive`：至少一个 strict-raw-linear state-evolution 组合同时通过 baseline、diagnostic 和全部 holdout。
- `mature_negative`：state-evolution 长期表现为高 `R2` + 高条件数 + stable sparse edges，因此可以成熟地下负结论。
