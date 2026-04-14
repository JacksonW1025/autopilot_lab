# Scenario Generalization

- status: `scenario_available`
- expected_scenarios: dynamic, nominal, throttle_biased

## Status Counts
- generalized_supported: 10
- supported_but_local: 0
- not_generalized: 2

## Combo Reading
- `commands_plus_state_history | selected_state_subset | ols_affine | pooled`: generalization_status=generalized_supported; support=supported; median_test_r2=1.0000; scenario_consistency=1.0000; subgroup_r2=[dynamic=1.0000, nominal=1.0000, throttle_biased=1.0000]
- `commands_plus_state_history | next_raw_state | ols_affine | pooled`: generalization_status=generalized_supported; support=supported; median_test_r2=0.9171; scenario_consistency=0.9932; subgroup_r2=[dynamic=0.9132, nominal=0.9192, throttle_biased=0.9195]
- `full_augmented | next_raw_state | ols_affine | pooled`: generalization_status=generalized_supported; support=supported; median_test_r2=0.9171; scenario_consistency=0.9932; subgroup_r2=[dynamic=0.9132, nominal=0.9192, throttle_biased=0.9195]
- `full_augmented | next_raw_state | lasso_affine | pooled`: generalization_status=generalized_supported; support=supported; median_test_r2=0.9171; scenario_consistency=0.9933; subgroup_r2=[dynamic=0.9132, nominal=0.9191, throttle_biased=0.9193]
- `commands_plus_state_history | next_raw_state | lasso_affine | pooled`: generalization_status=generalized_supported; support=supported; median_test_r2=0.9171; scenario_consistency=0.9933; subgroup_r2=[dynamic=0.9132, nominal=0.9191, throttle_biased=0.9193]
- `full_augmented | next_raw_state | ridge_affine | pooled`: generalization_status=generalized_supported; support=supported; median_test_r2=0.9171; scenario_consistency=0.9932; subgroup_r2=[dynamic=0.9131, nominal=0.9191, throttle_biased=0.9194]
- `commands_plus_state_history | next_raw_state | ridge_affine | pooled`: generalization_status=generalized_supported; support=supported; median_test_r2=0.9171; scenario_consistency=0.9932; subgroup_r2=[dynamic=0.9131, nominal=0.9191, throttle_biased=0.9194]
- `commands_plus_state_history | selected_state_subset | ridge_affine | pooled`: generalization_status=generalized_supported; support=supported; median_test_r2=0.7423; scenario_consistency=0.7135; subgroup_r2=[dynamic=0.7135, nominal=1.0000, throttle_biased=1.0000]
- `full_augmented | selected_state_subset | ols_affine | pooled`: generalization_status=generalized_supported; support=supported; median_test_r2=0.7168; scenario_consistency=1.0000; subgroup_r2=[dynamic=1.0000, nominal=1.0000, throttle_biased=1.0000]
- `full_augmented | selected_state_subset | ridge_affine | pooled`: generalization_status=generalized_supported; support=supported; median_test_r2=0.7084; scenario_consistency=0.9927; subgroup_r2=[dynamic=0.9927, nominal=1.0000, throttle_biased=1.0000]
- `full_augmented | selected_state_subset | lasso_affine | pooled`: generalization_status=not_generalized; support=unsupported; median_test_r2=0.0816; scenario_consistency=0.0000; subgroup_r2=[dynamic=-0.2232, nominal=0.9999, throttle_biased=1.0000]
- `commands_plus_state_history | selected_state_subset | lasso_affine | pooled`: generalization_status=not_generalized; support=unsupported; median_test_r2=-0.3618; scenario_consistency=0.0000; subgroup_r2=[dynamic=-0.7779, nominal=0.9999, throttle_biased=1.0000]

## Conclusion
- 当前 study 里已经出现跨 scenario 仍然保持 supported 的组合，f 更像常见映射而不是单一 operating-point 拟合。