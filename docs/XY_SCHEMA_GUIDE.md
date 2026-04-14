# X/Y Schema Guide

## 先怎么读当前 Formal V2 结果

如果你现在要读最新结果，不要再从 20260409 的 broad baseline 或准备性 artifact 开始。

当前推荐顺序是：

1. PX4 generalization full baseline
   - `../artifacts/studies/20260410_224818_px4_real_generalization_ablation`
2. PX4 generalization full diagnostic
   - `../artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`
3. ArduPilot generalization full baseline
   - `../artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation`
4. ArduPilot generalization full diagnostic
   - `../artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix`
5. ArduPilot targeted state-evolution validation
   - `../artifacts/studies/20260413_134505_ardupilot_state_evolution_validation`

理由很简单：Formal V2 现在同时回答“线性是否存在、是否跨 scenario 成立、以及 ArduPilot 的 state-evolution 在 mode-isolated 条件下是成熟正结论还是成熟负结论”。

## 当前最值得先看的代表性组合

### PX4：状态演化主线

- `full_augmented | next_raw_state | ols_affine | stratified`
- 路径：`../artifacts/studies/20260410_224818_px4_real_generalization_ablation`

### ArduPilot：当前最稳的跨场景主结构

- `commands_only | actuator_response | ridge_affine | pooled`
- 路径：`../artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation`

### ArduPilot targeted：mode-isolated state-evolution

- STABILIZE：status=`inconclusive`；combo=`commands_plus_state_history | selected_state_subset | ols_affine | pooled`
- GUIDED_NOGPS：status=`inconclusive`；combo=`commands_plus_state_history | selected_state_subset | ols_affine | pooled`
- 路径：`../artifacts/studies/20260413_134505_ardupilot_state_evolution_validation`
- STABILIZE targeted baseline：`../artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline`
- STABILIZE targeted diagnostic：`../artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic`
- GUIDED_NOGPS targeted baseline：`../artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline`
- GUIDED_NOGPS targeted diagnostic：`../artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic`

## 当前推荐的阅读方法

1. 先看 generalization full 的 `summary.md` 与 `scenario_generalization.md`。
2. 再看 targeted line 的 `state_evolution_validation.md`。
3. 如果某个 state-evolution 组合高 `R2` 但结论仍谨慎，再一起看：
   - `scenario_holdout.md`
   - `sparsity_overlap.md`
   - `state_evolution_audit.md`

## 当前最重要的阅读边界

- `best_result` 不一定等于“最稳的正式结论”。
- 对 ArduPilot 尤其要注意：高 `R2` 不等于已经得到稳定 state-evolution 结论，必须把 holdout、条件数、稳定性和 sparsity overlap 一起看。
