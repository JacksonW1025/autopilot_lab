# Curated Heatmaps

当前目录放的是这轮 `generalization full` 里最值得直接看的几张热力图拷贝。

## 1. PX4 baseline 主图

- 含义：当前 PX4 baseline 最强的 `generalized-supported` 组合。
- 组合：`full_augmented | next_raw_state | ols_affine | stratified`
- 来源矩阵目录：
  - `../../../artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__next_raw_state__stratified/ols_affine/`
- 图片：
  - `px4_baseline_generalized_full_augmented_next_raw_state_ols_stratified_abs.png`
  - `px4_baseline_generalized_full_augmented_next_raw_state_ols_stratified_signed.png`

## 2. PX4 baseline 对照图

- 含义：当前 PX4 baseline 里 `supported-but-local` 的代表组合，用来和 generalized-supported 主图对照。
- 组合：`feature_mapped_linear | next_raw_state | ols_affine | stratified`
- 来源矩阵目录：
  - `../../../artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/feature_mapped_linear__next_raw_state__stratified/ols_affine/`
- 图片：
  - `px4_baseline_local_feature_mapped_next_raw_state_ols_stratified_abs.png`
  - `px4_baseline_local_feature_mapped_next_raw_state_ols_stratified_signed.png`

## 3. PX4 diagnostic 主图

- 含义：当前 PX4 diagnostic 里最能代表跨动作后仍然稳定的组合。
- 组合：`full_augmented | next_raw_state | ols_affine | stratified`
- 来源矩阵目录：
  - `../../../artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/fits/full_augmented__next_raw_state__stratified/ols_affine/`
- 图片：
  - `px4_diagnostic_generalized_full_augmented_next_raw_state_ols_stratified_abs.png`
  - `px4_diagnostic_generalized_full_augmented_next_raw_state_ols_stratified_signed.png`

## 4. ArduPilot baseline 主图

- 含义：当前 ArduPilot 最稳的 `generalized-supported` 组合。
- 组合：`commands_only | actuator_response | ridge_affine | pooled`
- 来源矩阵目录：
  - `../../../artifacts/studies/20260411_095055_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/`
- 图片：
  - `ardupilot_baseline_generalized_commands_only_actuator_response_ridge_pooled_abs.png`
  - `ardupilot_baseline_generalized_commands_only_actuator_response_ridge_pooled_signed.png`

## 5. ArduPilot 高分但不稳对照图

- 含义：当前 ArduPilot `R2` 很高但仍然不能当作正式 supported 主结论的 state-evolution 组合。
- 组合：`commands_plus_state_history | selected_state_subset | ols_affine | pooled`
- 来源矩阵目录：
  - `../../../artifacts/studies/20260411_095055_ardupilot_real_generalization_ablation/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/`
- 图片：
  - `ardupilot_baseline_partial_commands_plus_state_history_selected_state_subset_ols_pooled_abs.png`
  - `ardupilot_baseline_partial_commands_plus_state_history_selected_state_subset_ols_pooled_signed.png`
