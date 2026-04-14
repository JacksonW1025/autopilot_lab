# 统一 Schema 口径下全局线性 `f` 的技术附录

## 1. 正式 artifact 清单

- PX4 baseline study: `../artifacts/studies/20260410_224818_px4_real_generalization_ablation`
- ArduPilot baseline study: `../artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation`
- PX4 diagnostic study: `../artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`
- ArduPilot diagnostic study: `../artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix`
- final compare: `../artifacts/studies/20260413_134755_px4_vs_ardupilot_compare`
- ArduPilot targeted validation: `../artifacts/studies/20260413_134505_ardupilot_state_evolution_validation`
- STABILIZE targeted baseline: `../artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline`
- STABILIZE targeted diagnostic: `../artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic`
- GUIDED_NOGPS targeted baseline: `../artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline`
- GUIDED_NOGPS targeted diagnostic: `../artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic`

## 3. baseline 关键数字

- PX4 accepted runs: `30`
- PX4 supported anchor: `full_augmented | next_raw_state | ols_affine | stratified`
- PX4 best combo: `full_augmented | next_raw_state | ols_affine | stratified`
- PX4 matrix gallery supported_count: `120`
- ArduPilot accepted runs: `30`
- ArduPilot supported anchor: `commands_only | actuator_response | ridge_affine | pooled`
- ArduPilot best combo: `commands_plus_state_history | selected_state_subset | ols_affine | pooled`
- ArduPilot baseline stability: `unknown`
- ArduPilot matrix gallery supported_count: `12`

## 4. scenario_generalization 核心数字

- PX4 baseline: generalized_supported=`80`, supported_but_local=`40`, not_generalized=`96`
- PX4 diagnostic: generalized_supported=`111`, supported_but_local=`15`, not_generalized=`90`
- ArduPilot baseline: generalized_supported=`12`, supported_but_local=`0`, not_generalized=`204`
- ArduPilot diagnostic: generalized_supported=`12`, supported_but_local=`0`, not_generalized=`204`
- generalization_difference_driver: `both_support_cross_scenario_linearity_but_px4_is_broader`

## 5. state-evolution audit 摘要

- audit_status: `audit_available`
- comparison_status: `comparison_unavailable`
- current_supported_state_evolution_count: `0`
- conclusion: `厚化 baseline 没有改变 ArduPilot 当前明确 supported 的主集合，state-evolution 路径的主阻塞仍然是 condition_number/mixed，而不是单纯 R2 不够。`
- report: `../artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/reports/state_evolution_audit.md`

## 6. Formal V2 targeted line 摘要

- targeted_overall_status: `mode_isolated_state_evolution_still_inconclusive`
- STABILIZE: `inconclusive`
- GUIDED_NOGPS: `inconclusive`
- targeted_conclusion: `Formal V2 targeted line 已经形成正式 artifact，但 state-evolution 还没有完全收敛到成熟正/负结论。`

## 7. diagnostic gate 摘要

- PX4 throttle_boundary: `mixed`; nonzero_gate_blocked=`true`
- ArduPilot throttle_boundary: `none`; nonzero_gate_blocked=`false`

## 8. 代表性组合与矩阵图

- PX4 baseline supported combo: `full_augmented | next_raw_state | ols_affine | stratified`
  - matrix: `../artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__next_raw_state__stratified/ols_affine/matrix_f.csv`
  - abs heatmap: `../artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__next_raw_state__stratified/ols_affine/matrix_heatmap_abs.png`
- ArduPilot baseline supported combo: `commands_only | actuator_response | ridge_affine | pooled`
  - matrix: `../artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/matrix_f.csv`
  - abs heatmap: `../artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/matrix_heatmap_abs.png`

## 9. compare 摘要

- compare_dir: `../artifacts/studies/20260413_134755_px4_vs_ardupilot_compare`
- difference_driver: `baseline_stability_unresolved`
- both_baselines_stable: `false`
- throttle_boundary_consistent: `false`

## 10. 历史阶段 artifact

- 20260409 broad baseline / diagnostic 与准备性 artifact 已移出 Formal V2 正式文档引用集。

## 11. 当前稳妥的技术结论

- 两个 backend 的正式 baseline 和 diagnostic 都已经形成完整 artifact。
- 两个 backend 都已经给出跨 scenario generalized-supported 证据。
- PX4 对状态演化类线性映射的 generalized-supported 支持继续更强、更宽。
- ArduPilot 的高分 state-evolution 结果仍需要结合条件数和稳定性一起解释。
- 因此现在可以把“线性关系存在且具有一定跨场景泛化性”作为正面结论汇报，但不应把“backend 差异”写成最终主结论。