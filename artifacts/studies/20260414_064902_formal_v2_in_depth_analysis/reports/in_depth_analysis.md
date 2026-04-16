# Formal V2 In-Depth Analysis

## Inputs
- px4_baseline: `../../20260410_224818_px4_real_generalization_ablation`
- px4_diagnostic: `../../20260411_021910_px4_generalization_diagnostic_matrix`
- ardupilot_baseline: `../../20260413_070802_ardupilot_real_generalization_ablation`
- ardupilot_diagnostic: `../../20260413_091420_ardupilot_generalization_diagnostic_matrix`
- targeted_validation: `../../20260413_134505_ardupilot_state_evolution_validation`
- top_k: `10`

## 1. Stable-core Matrix Readout
- px4 stable_core_count: `80`; baseline_subset_of_diagnostic=`true`; diagnostic_only=`31`
- ardupilot stable_core_count: `12`; baseline_subset_of_diagnostic=`true`; diagnostic_only=`0`
- table: `../tables/stable_core_matrix_readout.csv`
- representative_px4_combo: `commands_plus_state | future_state_horizon | lasso_affine | pooled`
- representative_px4_matrix: `../../20260410_224818_px4_real_generalization_ablation/fits/commands_plus_state__future_state_horizon__pooled/lasso_affine/matrix_f.csv`
- representative_px4_metrics: `../../20260410_224818_px4_real_generalization_ablation/fits/commands_plus_state__future_state_horizon__pooled/lasso_affine/metrics.json`
- representative_ardupilot_combo: `commands_only | actuator_response | lasso_affine | pooled`
- representative_ardupilot_matrix: `../../20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/lasso_affine/matrix_f.csv`
- representative_ardupilot_metrics: `../../20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/lasso_affine/metrics.json`

## 2. PX4 Physical vs State Continuation
- main_scope_count: `53`; appendix_scope_count: `27`
- table: `../tables/px4_physical_vs_state_continuation.csv`
- repeated_pattern: `same_state:pitch->pitch` count=`72`
- repeated_pattern: `same_state:roll->roll` count=`69`
- repeated_pattern: `same_state:yaw_rate->yaw_rate` count=`67`
- repeated_pattern: `same_state:yaw->yaw` count=`60`
- repeated_pattern: `same_state:pitch_rate->pitch_rate` count=`38`

## 3. Backend Alignment
- strict_schema_overlap_count: `0`
- shared_alignment_key_count: `9`
- table: `../tables/backend_alignment.csv`
- shared_alignment: `future_state_horizon | pooled | ols_affine` => px4=`commands_plus_state | future_state_horizon | ols_affine | pooled` vs ardupilot=`commands_only | future_state_horizon | ols_affine | pooled`; top_edge_jaccard=`0.0000`
- shared_alignment: `future_state_horizon | pooled | ridge_affine` => px4=`commands_plus_state | future_state_horizon | ridge_affine | pooled` vs ardupilot=`commands_only | future_state_horizon | ridge_affine | pooled`; top_edge_jaccard=`0.0000`
- shared_alignment: `future_state_horizon | pooled | lasso_affine` => px4=`commands_plus_state | future_state_horizon | lasso_affine | pooled` vs ardupilot=`commands_only | future_state_horizon | lasso_affine | pooled`; top_edge_jaccard=`0.0000`

## 4. ArduPilot Conditioning Failure
- table: `../tables/ardupilot_conditioning_failure.csv`
- `mixed_mode_full` combo=`commands_plus_state_history | selected_state_subset | ols_affine | pooled`
  baseline_metrics=`../../20260413_070802_ardupilot_real_generalization_ablation/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/metrics.json` diagnostic_metrics=`../../20260413_091420_ardupilot_generalization_diagnostic_matrix/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/metrics.json` top_edge_jaccard=`0.1111`
- `stabilize_baseline_to_diagnostic_collapse` combo=`commands_plus_state_history | selected_state_subset | ols_affine | pooled`
  baseline_metrics=`../../20260413_115811_ardupilot_state_evolution_stabilize_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/metrics.json` diagnostic_metrics=`../../20260413_122521_ardupilot_state_evolution_stabilize_diagnostic/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/metrics.json` top_edge_jaccard=`0.0000`
- `guided_nogps_persistent_high_r2_high_cond` combo=`commands_plus_state_history | selected_state_subset | ols_affine | pooled`
  baseline_metrics=`../../20260413_124654_ardupilot_state_evolution_guided_nogps_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/metrics.json` diagnostic_metrics=`../../20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/metrics.json` top_edge_jaccard=`0.4286`

## 5. Stability Boundary
- row_count: `270`
- primary_driver_counts: `{'none': 44, 'stratification': 43, 'feature_collinearity': 183}`
- table: `../tables/stability_boundary.csv`
- primary_driver `feature_collinearity`: `183`
- primary_driver `none`: `44`
- primary_driver `stratification`: `43`
