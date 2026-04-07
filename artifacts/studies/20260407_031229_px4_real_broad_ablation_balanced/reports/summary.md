# Global Linearity Study Summary: px4_real_broad_ablation_balanced

## 研究目标
- 主线固定为：数据采集 -> X/Y 构造 -> 全局拟合 -> 稀疏性分析 -> 结论。
- 研究问题是：在当前 study scope 下，是否存在固定的全局线性/仿射映射 `Y ≈ fX (+ b)`。

## 真实 PX4 Broad Ablation 结论模板
- best_linear_schema: `commands_plus_state_history x next_raw_state | ols_affine | pooled`
- best_sparse_and_stable_schema: `commands_plus_state_history x next_raw_state | ridge_affine | pooled`
- best_y_definition: `next_raw_state`
- commands_only_to_commands_plus_state_r2_gain: 1.0442
- commands_plus_state_to_history_r2_gain: 0.0064

## 最优组合
- best_combo: `commands_plus_state_history x next_raw_state | ols_affine | pooled`
- support: `partial`
- median_test_r2: 0.9726
- median_test_mse: 0.000046
- median_test_mae: 0.003960
- sparsity_ratio: 0.7158
- coefficient_stability: 1.0000

## Conditioning
- raw_condition_number: inf
- effective_condition_number: 1259416.2092
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

## Data Quality
- alignment_failure_ratio: 0.0000
- missing_attitude_ratio: 0.0000
- missing_local_position_ratio: 0.0000
- missing_actuator_ratio: 0.0000
- future_horizon_available_ratio: 0.9934
- window_summary_available_ratio: 0.9934
- median_alignment_attitude_ms: 2.4425
- median_alignment_position_ms: 2.5220

## Schema Ranking
- `commands_plus_state_history x next_raw_state | ols_affine | pooled`: test R2=0.9726, sparsity=0.7158, support=partial
- `commands_plus_state_history x next_raw_state | lasso_affine | pooled`: test R2=0.9672, sparsity=0.6868, support=partial
- `commands_plus_state x next_raw_state | lasso_affine | pooled`: test R2=0.9663, sparsity=0.3930, support=supported
- `commands_plus_state_history x next_raw_state | ridge_affine | pooled`: test R2=0.9600, sparsity=0.9825, support=partial
- `commands_plus_state x next_raw_state | ridge_affine | pooled`: test R2=0.9595, sparsity=0.9684, support=supported
- `commands_plus_state x next_raw_state | ols_affine | pooled`: test R2=0.9545, sparsity=0.7965, support=supported
- `full_augmented x next_raw_state | lasso_affine | pooled`: test R2=0.8755, sparsity=0.6933, support=partial
- `commands_plus_state_history x future_state_horizon | lasso_affine | pooled`: test R2=0.6627, sparsity=0.8651, support=partial
- `commands_plus_state x future_state_horizon | lasso_affine | pooled`: test R2=0.5852, sparsity=0.6140, support=partial
- `commands_plus_state_history x future_state_horizon | ridge_affine | pooled`: test R2=0.5780, sparsity=1.0000, support=partial
- `commands_plus_state_history x selected_state_subset | lasso_affine | pooled`: test R2=0.4997, sparsity=0.8399, support=partial
- `commands_plus_state x future_state_horizon | ridge_affine | pooled`: test R2=0.4679, sparsity=1.0000, support=partial
- `commands_plus_state x future_state_horizon | ols_affine | pooled`: test R2=0.4646, sparsity=0.8421, support=partial
- `commands_plus_state_history x future_state_horizon | ols_affine | pooled`: test R2=0.4432, sparsity=0.7763, support=partial
- `commands_plus_state x selected_state_subset | lasso_affine | pooled`: test R2=0.3955, sparsity=0.5526, support=unsupported
- `commands_plus_state_history x selected_state_subset | ridge_affine | pooled`: test R2=0.3866, sparsity=1.0000, support=unsupported
- `full_augmented x next_raw_state | ridge_affine | pooled`: test R2=0.3520, sparsity=0.9852, support=unsupported
- `commands_plus_state_history x selected_state_subset | ols_affine | pooled`: test R2=0.2222, sparsity=0.7675, support=unsupported
- `commands_plus_state x selected_state_subset | ridge_affine | pooled`: test R2=0.2213, sparsity=1.0000, support=unsupported
- `commands_plus_state x selected_state_subset | ols_affine | pooled`: test R2=0.2154, sparsity=0.8421, support=unsupported
- `full_augmented x next_raw_state | ols_affine | pooled`: test R2=0.1839, sparsity=0.6874, support=unsupported
- `commands_plus_state_history x delta_state | lasso_affine | pooled`: test R2=-0.0169, sparsity=0.7535, support=unsupported
- `commands_only x selected_state_subset | ridge_affine | pooled`: test R2=-0.0780, sparsity=1.0000, support=unsupported
- `commands_only x selected_state_subset | ols_affine | pooled`: test R2=-0.0785, sparsity=0.2500, support=unsupported
- `commands_only x future_state_horizon | ridge_affine | pooled`: test R2=-0.0793, sparsity=1.0000, support=unsupported
- `commands_only x selected_state_subset | lasso_affine | pooled`: test R2=-0.0794, sparsity=0.3750, support=unsupported
- `commands_only x future_state_horizon | ols_affine | pooled`: test R2=-0.0798, sparsity=0.2500, support=unsupported
- `commands_only x future_state_horizon | lasso_affine | pooled`: test R2=-0.0804, sparsity=0.3750, support=unsupported
- `commands_plus_state_history x delta_state | ols_affine | pooled`: test R2=-0.2710, sparsity=0.7175, support=unsupported
- `commands_plus_state_history x delta_state | ridge_affine | pooled`: test R2=-0.3735, sparsity=0.9965, support=unsupported
- `commands_only x delta_state | lasso_affine | pooled`: test R2=-0.4098, sparsity=0.5167, support=unsupported
- `commands_plus_state x actuator_response | ridge_affine | pooled`: test R2=-0.4104, sparsity=0.6316, support=unsupported
- `commands_plus_state x actuator_response | lasso_affine | pooled`: test R2=-0.4298, sparsity=0.0000, support=unsupported
- `commands_plus_state x actuator_response | ols_affine | pooled`: test R2=-0.4341, sparsity=0.3684, support=unsupported
- `commands_only x delta_state | ridge_affine | pooled`: test R2=-0.4631, sparsity=1.0000, support=unsupported
- `commands_only x delta_state | ols_affine | pooled`: test R2=-0.4647, sparsity=0.2500, support=unsupported
- `commands_plus_state_history x actuator_response | ridge_affine | pooled`: test R2=-0.4834, sparsity=0.7105, support=unsupported
- `commands_plus_state_history x actuator_response | lasso_affine | pooled`: test R2=-0.5061, sparsity=0.1250, support=unsupported
- `commands_plus_state x delta_state | lasso_affine | pooled`: test R2=-0.5762, sparsity=0.4316, support=unsupported
- `commands_only x actuator_response | lasso_affine | pooled`: test R2=-0.7474, sparsity=0.2500, support=unsupported
- `commands_only x actuator_response | ridge_affine | pooled`: test R2=-0.7478, sparsity=1.0000, support=unsupported
- `commands_only x actuator_response | ols_affine | pooled`: test R2=-0.7506, sparsity=0.2500, support=unsupported
- `commands_plus_state_history x actuator_response | ols_affine | pooled`: test R2=-1.1216, sparsity=0.1941, support=unsupported
- `commands_plus_state x delta_state | ridge_affine | pooled`: test R2=-1.1516, sparsity=1.0000, support=unsupported
- `commands_plus_state x delta_state | ols_affine | pooled`: test R2=-1.1995, sparsity=0.8281, support=unsupported
- `full_augmented x future_state_horizon | lasso_affine | pooled`: test R2=-2.4700, sparsity=0.8491, support=unsupported
- `full_augmented x delta_state | lasso_affine | pooled`: test R2=-3.3059, sparsity=0.7689, support=unsupported
- `full_augmented x selected_state_subset | lasso_affine | pooled`: test R2=-5.0053, sparsity=0.8222, support=unsupported
- `full_augmented x future_state_horizon | ridge_affine | pooled`: test R2=-10.5199, sparsity=1.0000, support=unsupported
- `full_augmented x selected_state_subset | ridge_affine | pooled`: test R2=-14.4599, sparsity=1.0000, support=unsupported
- `full_augmented x delta_state | ridge_affine | pooled`: test R2=-19.1810, sparsity=0.9970, support=unsupported
- `full_augmented x actuator_response | ridge_affine | pooled`: test R2=-22.2654, sparsity=0.8140, support=unsupported
- `full_augmented x actuator_response | lasso_affine | pooled`: test R2=-23.6343, sparsity=0.2238, support=unsupported
- `full_augmented x actuator_response | ols_affine | pooled`: test R2=-23.6805, sparsity=0.2674, support=unsupported
- `full_augmented x future_state_horizon | ols_affine | pooled`: test R2=-24.6362, sparsity=0.7444, support=unsupported
- `full_augmented x selected_state_subset | ols_affine | pooled`: test R2=-35.7566, sparsity=0.7167, support=unsupported
- `full_augmented x delta_state | ols_affine | pooled`: test R2=-36.9026, sparsity=0.6889, support=unsupported
- `commands_only x next_raw_state | ridge_affine | pooled`: test R2=-119.7585, sparsity=0.9667, support=unsupported
- `commands_only x next_raw_state | lasso_affine | pooled`: test R2=-119.8793, sparsity=0.3167, support=unsupported
- `commands_only x next_raw_state | ols_affine | pooled`: test R2=-120.0332, sparsity=0.2167, support=unsupported

## Diagnostics
- 缺少必要 state/context；把当前状态并入 X 后显著提高了全局拟合效果。
- raw feature matrix 含有精确别名或 one-hot 依赖；报告已同时输出 effective conditioning 以避免把可解释 schema 误判为病态。

## Failure Attribution
- 更像缺 state/context，而不是纯 command 输入本身不足。

## Skipped Or Unsupported Combos
- 无。