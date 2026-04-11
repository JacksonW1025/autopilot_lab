# Global Linearity Study Summary: ardupilot_diagnostic_stabilize_throttle

## 研究目标
- 主线固定为：数据采集 -> X/Y 构造 -> 全局拟合 -> 稀疏性分析 -> 结论。
- 研究问题是：在当前 study scope 下，是否存在固定的全局线性/仿射映射 `Y ≈ fX (+ b)`。

## 结论摘要
- best_linear_schema: `commands_only x actuator_response | ols_affine | pooled`
- best_sparse_and_stable_schema: `commands_plus_state x next_raw_state | lasso_affine | pooled`
- best_y_definition: `next_raw_state`
- commands_only_to_commands_plus_state_r2_gain: nan
- commands_plus_state_to_history_r2_gain: -0.0001

## 最优组合
- best_combo: `commands_only x actuator_response | ols_affine | pooled`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- sparsity_ratio: 1.0000
- coefficient_stability: 1.0000

## Conditioning
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

## Data Quality
- alignment_failure_ratio: 0.0000
- missing_attitude_ratio: 0.0000
- missing_local_position_ratio: 0.0000
- missing_actuator_ratio: 0.0000
- future_horizon_available_ratio: 0.9894
- window_summary_available_ratio: 0.9894
- median_alignment_attitude_ms: 0.2516
- median_alignment_position_ms: 0.3937

## Schema Ranking
- `commands_only x actuator_response | ols_affine | pooled`: test R2=nan, sparsity=1.0000, support=unsupported
- `commands_only x actuator_response | ridge_affine | pooled`: test R2=nan, sparsity=1.0000, support=unsupported
- `commands_only x actuator_response | lasso_affine | pooled`: test R2=nan, sparsity=1.0000, support=unsupported
- `commands_plus_state x selected_state_subset | ols_affine | pooled`: test R2=1.0000, sparsity=1.0000, support=supported
- `commands_plus_state x future_state_horizon | ols_affine | pooled`: test R2=1.0000, sparsity=1.0000, support=supported
- `commands_plus_state x actuator_response | ols_affine | pooled`: test R2=nan, sparsity=1.0000, support=unsupported
- `commands_plus_state x actuator_response | ridge_affine | pooled`: test R2=nan, sparsity=1.0000, support=unsupported
- `commands_plus_state x actuator_response | lasso_affine | pooled`: test R2=nan, sparsity=1.0000, support=unsupported
- `commands_plus_state_history x selected_state_subset | ols_affine | pooled`: test R2=0.9999, sparsity=1.0000, support=supported
- `commands_plus_state_history x actuator_response | ols_affine | pooled`: test R2=nan, sparsity=1.0000, support=unsupported
- `commands_plus_state_history x actuator_response | ridge_affine | pooled`: test R2=nan, sparsity=1.0000, support=unsupported
- `commands_plus_state_history x actuator_response | lasso_affine | pooled`: test R2=nan, sparsity=1.0000, support=unsupported
- `full_augmented x selected_state_subset | ols_affine | pooled`: test R2=1.0000, sparsity=1.0000, support=supported
- `full_augmented x future_state_horizon | ols_affine | pooled`: test R2=1.0000, sparsity=1.0000, support=supported
- `commands_plus_state_history x future_state_horizon | ols_affine | pooled`: test R2=0.9999, sparsity=1.0000, support=supported
- `full_augmented x next_raw_state | ridge_affine | pooled`: test R2=0.9236, sparsity=0.9196, support=supported
- `full_augmented x next_raw_state | ols_affine | pooled`: test R2=0.9236, sparsity=0.9238, support=supported
- `full_augmented x next_raw_state | lasso_affine | pooled`: test R2=0.9236, sparsity=0.9185, support=supported
- `commands_plus_state_history x next_raw_state | ridge_affine | pooled`: test R2=0.9235, sparsity=0.9238, support=supported
- `commands_plus_state_history x next_raw_state | ols_affine | pooled`: test R2=0.9235, sparsity=0.9286, support=supported
- `commands_plus_state_history x next_raw_state | lasso_affine | pooled`: test R2=0.9235, sparsity=0.9214, support=supported
- `commands_plus_state x next_raw_state | ridge_affine | pooled`: test R2=0.9217, sparsity=0.9238, support=supported
- `commands_plus_state x next_raw_state | ols_affine | pooled`: test R2=0.9217, sparsity=0.9238, support=supported
- `commands_plus_state x next_raw_state | lasso_affine | pooled`: test R2=0.9217, sparsity=0.9333, support=supported
- `full_augmented x delta_state | ridge_affine | pooled`: test R2=0.1789, sparsity=0.9196, support=unsupported
- `full_augmented x delta_state | ols_affine | pooled`: test R2=0.1789, sparsity=0.9238, support=unsupported
- `full_augmented x delta_state | lasso_affine | pooled`: test R2=0.1788, sparsity=0.9228, support=unsupported
- `commands_plus_state_history x delta_state | ridge_affine | pooled`: test R2=0.1786, sparsity=0.9238, support=unsupported
- `commands_plus_state_history x delta_state | ols_affine | pooled`: test R2=0.1785, sparsity=0.9286, support=unsupported
- `commands_plus_state_history x delta_state | lasso_affine | pooled`: test R2=0.1785, sparsity=0.9238, support=unsupported
- `commands_plus_state x delta_state | ols_affine | pooled`: test R2=0.0716, sparsity=0.9238, support=unsupported
- `commands_plus_state x delta_state | lasso_affine | pooled`: test R2=0.0716, sparsity=0.9333, support=unsupported
- `commands_plus_state x delta_state | ridge_affine | pooled`: test R2=0.0716, sparsity=0.9238, support=unsupported
- `commands_only x next_raw_state | ridge_affine | pooled`: test R2=0.0058, sparsity=0.8667, support=unsupported
- `commands_only x next_raw_state | lasso_affine | pooled`: test R2=0.0058, sparsity=0.7333, support=unsupported
- `commands_only x next_raw_state | ols_affine | pooled`: test R2=0.0058, sparsity=0.8667, support=unsupported
- `commands_only x delta_state | ridge_affine | pooled`: test R2=0.0019, sparsity=0.8667, support=unsupported
- `commands_only x delta_state | lasso_affine | pooled`: test R2=0.0019, sparsity=0.7333, support=unsupported
- `commands_only x delta_state | ols_affine | pooled`: test R2=0.0019, sparsity=0.8667, support=unsupported
- `full_augmented x selected_state_subset | ridge_affine | pooled`: test R2=-4294778419.6761, sparsity=1.0000, support=unsupported
- `full_augmented x future_state_horizon | ridge_affine | pooled`: test R2=-4294778420.5329, sparsity=1.0000, support=unsupported
- `commands_plus_state_history x future_state_horizon | ridge_affine | pooled`: test R2=-3635858288408.6665, sparsity=1.0000, support=unsupported
- `commands_plus_state_history x selected_state_subset | ridge_affine | pooled`: test R2=-3635858288438.1978, sparsity=1.0000, support=unsupported
- `commands_plus_state x selected_state_subset | ridge_affine | pooled`: test R2=-6256594828821.4131, sparsity=1.0000, support=unsupported
- `commands_plus_state x future_state_horizon | ridge_affine | pooled`: test R2=-6256594828821.4131, sparsity=1.0000, support=unsupported
- `commands_plus_state x selected_state_subset | lasso_affine | pooled`: test R2=-138085659911445.3906, sparsity=1.0000, support=unsupported
- `commands_plus_state x future_state_horizon | lasso_affine | pooled`: test R2=-138085659911445.3906, sparsity=1.0000, support=unsupported
- `full_augmented x selected_state_subset | lasso_affine | pooled`: test R2=-145359812282889.8438, sparsity=1.0000, support=unsupported
- `full_augmented x future_state_horizon | lasso_affine | pooled`: test R2=-145359812282889.8438, sparsity=1.0000, support=unsupported
- `commands_plus_state_history x selected_state_subset | lasso_affine | pooled`: test R2=-145588290115770.5938, sparsity=1.0000, support=unsupported
- `commands_plus_state_history x future_state_horizon | lasso_affine | pooled`: test R2=-145588290115770.5938, sparsity=1.0000, support=unsupported
- `commands_only x future_state_horizon | lasso_affine | pooled`: test R2=-215028990430623072.0000, sparsity=1.0000, support=unsupported
- `commands_only x selected_state_subset | lasso_affine | pooled`: test R2=-215028990430623104.0000, sparsity=1.0000, support=unsupported
- `commands_only x future_state_horizon | ridge_affine | pooled`: test R2=-217511573300210720.0000, sparsity=1.0000, support=unsupported
- `commands_only x selected_state_subset | ridge_affine | pooled`: test R2=-217511573300210752.0000, sparsity=1.0000, support=unsupported
- `commands_only x future_state_horizon | ols_affine | pooled`: test R2=-217521997177265472.0000, sparsity=1.0000, support=unsupported
- `commands_only x selected_state_subset | ols_affine | pooled`: test R2=-217521997177265504.0000, sparsity=1.0000, support=unsupported
- `full_augmented x actuator_response | ols_affine | pooled`: test R2=nan, sparsity=1.0000, support=unsupported
- `full_augmented x actuator_response | ridge_affine | pooled`: test R2=nan, sparsity=1.0000, support=unsupported
- `full_augmented x actuator_response | lasso_affine | pooled`: test R2=nan, sparsity=1.0000, support=unsupported

## Diagnostics
- 当前 study scope 下，全局固定线性/仿射映射解释力不足，可能需要更强上下文、更多历史，或线性假设本身不成立。

## Failure Attribution
- 更像全局线性假设不足或噪声/异质性仍然过强。

## Skipped Or Unsupported Combos
- 无。