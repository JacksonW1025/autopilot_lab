# Curated Heatmaps

当前目录放的是 `Formal V2` 最值得直接看的几张热力图拷贝。

## 1. PX4 generalization full baseline 主图
- 组合：`full_augmented | next_raw_state | ols_affine | stratified`
- 来源矩阵目录：`../../../artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__next_raw_state__stratified/ols_affine/`
- 图片：
  - `px4_baseline_generalized_main_abs.png`
  - `px4_baseline_generalized_main_signed.png`

## 2. PX4 generalization full diagnostic 主图
- 组合：`full_augmented | next_raw_state | ols_affine | stratified`
- 来源矩阵目录：`../../../artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/fits/full_augmented__next_raw_state__stratified/ols_affine/`
- 图片：
  - `px4_diagnostic_generalized_main_abs.png`
  - `px4_diagnostic_generalized_main_signed.png`

## 3. ArduPilot generalization full baseline 主图
- 组合：`commands_only | actuator_response | ridge_affine | pooled`
- 来源矩阵目录：`../../../artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/`
- 图片：
  - `ardupilot_full_baseline_main_abs.png`
  - `ardupilot_full_baseline_main_signed.png`

## 4. ArduPilot targeted STABILIZE 代表图
- validation_status：`inconclusive`
- 组合：`commands_plus_state_history | selected_state_subset | ols_affine | pooled`
- 来源矩阵目录：`../../../artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/`
- 图片：
  - `ardupilot_targeted_stabilize_abs.png`
  - `ardupilot_targeted_stabilize_signed.png`

## 5. ArduPilot targeted GUIDED_NOGPS 代表图
- validation_status：`inconclusive`
- 组合：`commands_plus_state_history | selected_state_subset | ols_affine | pooled`
- 来源矩阵目录：`../../../artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/`
- 图片：
  - `ardupilot_targeted_guided_nogps_abs.png`
  - `ardupilot_targeted_guided_nogps_signed.png`
