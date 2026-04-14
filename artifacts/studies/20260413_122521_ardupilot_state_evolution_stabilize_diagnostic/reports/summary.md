# Global Linearity Study Summary: ardupilot_state_evolution_stabilize_diagnostic

## 研究目标
- 主线固定为：数据采集 -> X/Y 构造 -> 全局拟合 -> 稀疏性分析 -> 结论。
- 研究问题是：在当前 study scope 下，是否存在固定的全局线性/仿射映射 `Y ≈ fX (+ b)`。

## 结论摘要
- best_linear_schema: `commands_plus_state_history x selected_state_subset | ols_affine | pooled`
- best_sparse_and_stable_schema: `full_augmented x next_raw_state | ridge_affine | pooled`
- best_y_definition: `selected_state_subset`
- commands_only_to_commands_plus_state_r2_gain: nan
- commands_plus_state_to_history_r2_gain: nan

## 最优组合
- best_combo: `commands_plus_state_history x selected_state_subset | ols_affine | pooled`
- support: `partial`
- median_test_r2: 0.9289
- median_test_mse: 0.000000
- median_test_mae: 0.000107
- sparsity_ratio: 1.0000
- coefficient_stability: 0.8431

## Conditioning
- raw_condition_number: inf
- effective_condition_number: 7535808.5063
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

## Data Quality
- alignment_failure_ratio: 0.0000
- missing_attitude_ratio: 0.0000
- missing_local_position_ratio: 0.0000
- missing_actuator_ratio: 0.0000
- future_horizon_available_ratio: 0.9893
- window_summary_available_ratio: 0.9893
- median_alignment_attitude_ms: 0.2678
- median_alignment_position_ms: 0.4224

## Schema Ranking
- `commands_plus_state_history x selected_state_subset | ols_affine | pooled`: test R2=0.9289, sparsity=1.0000, support=partial
- `commands_plus_state_history x next_raw_state | lasso_affine | pooled`: test R2=0.9153, sparsity=0.8716, support=partial
- `full_augmented x next_raw_state | lasso_affine | pooled`: test R2=0.9153, sparsity=0.8630, support=partial
- `full_augmented x next_raw_state | ridge_affine | pooled`: test R2=0.9152, sparsity=0.8981, support=partial
- `full_augmented x next_raw_state | ols_affine | pooled`: test R2=0.9018, sparsity=0.8981, support=partial
- `commands_plus_state_history x next_raw_state | ridge_affine | pooled`: test R2=0.9010, sparsity=0.8980, support=partial
- `commands_plus_state_history x selected_state_subset | ridge_affine | pooled`: test R2=0.7139, sparsity=1.0000, support=partial
- `full_augmented x selected_state_subset | ols_affine | pooled`: test R2=0.6935, sparsity=1.0000, support=partial
- `full_augmented x selected_state_subset | ridge_affine | pooled`: test R2=0.6579, sparsity=1.0000, support=partial
- `full_augmented x selected_state_subset | lasso_affine | pooled`: test R2=0.2002, sparsity=0.9560, support=unsupported
- `commands_plus_state_history x selected_state_subset | lasso_affine | pooled`: test R2=0.1971, sparsity=0.9706, support=unsupported
- `commands_plus_state_history x next_raw_state | ols_affine | pooled`: test R2=-15700.6207, sparsity=0.8980, support=unsupported

## Diagnostics
- raw feature matrix 含有精确别名或 one-hot 依赖；报告已同时输出 effective conditioning 以避免把可解释 schema 误判为病态。

## Failure Attribution
- 暂无明确失败归因。

## Skipped Or Unsupported Combos
- 无。