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

## Artifact 保留口径

- current remote Git 只保留 latest Formal V2 studies 与正式文档。
- `../artifacts/raw/**` 是本地实验运行输出；它用于追溯 study 输入，但不再作为远端仓库的长期跟踪对象。
- `../artifacts/px4_matrix/**` 与 `../artifacts/ardupilot_matrix/**` 视为临时 matrix 目录，不进入 current canonical remote 集合。

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
- `reports/sparsity_overlap.md`
- `summary/study_summary.json`
- `summary/scenario_generalization.json`
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
- `mature_positive`：至少一个 strict-raw-linear state-evolution 组合同时在 baseline、diagnostic 和 sparse-edge overlap 上保持稳定。
- `mature_negative`：state-evolution 长期表现为高 `R2` + 高条件数 + stable sparse edges，因此可以成熟地下负结论。

## Formal V2 之后的 narrowing studies

这些 study 不是新的 `Formal V3`，也不替代 canonical Formal V2。它们的作用是把已经成立的 insight 压缩成更窄的执行线。

### ArduPilot A2 narrowing

推荐按下面顺序读：

1. `artifacts/studies/20260416_003238_183129_ardupilot_a2_target_scout`
2. `artifacts/studies/20260416_003634_371133_ardupilot_a2_pair_target_readiness`

当前正式结论：

- `STABILIZE + throttle collective boundary` 线已经被排除
- 当前最稳 target 是 `GUIDED_NOGPS + pair_imbalance_12_vs_34`
- `ready_for_pair_attack_v1=yes`

### PX4 A1 narrowing

推荐按下面顺序读：

1. `artifacts/studies/20260416_005450_652002_px4_a1_target_scout`
2. `artifacts/studies/20260416_005450_658923_px4_a1_family_readiness`
3. `artifacts/studies/20260416_010626_381143_px4_a1_roll_pitch_targeted_reproduction`

当前正式结论：

- 当前最稳 family 是 `attitude_roll_pitch_continuation`
- 当前最稳 exact scope 是 `future_state_roll / future_state_pitch`
- 这条线当前是 `targeted reproduction / contrast line`，不是 attack-ready line

## 当前推荐入口

Formal V2 主入口之外，当前常用的 narrowing 入口是：

```bash
../scripts/run_ardupilot_a2_target_scout.sh
../scripts/run_ardupilot_a2_guided_nogps_pair_target_readiness.sh
../scripts/run_px4_a1_target_scout.sh
../scripts/run_px4_a1_attitude_family_readiness.sh
../scripts/run_px4_a1_roll_pitch_targeted_reproduction.sh
```
