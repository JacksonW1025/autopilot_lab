# Scenario Generalization

- status: `scenario_available`
- expected_scenarios: dynamic, nominal, throttle_biased

## Status Counts
- generalized_supported: 0
- supported_but_local: 0
- not_generalized: 12

## Combo Reading
- `commands_plus_state_history | selected_state_subset | ols_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=1.0000; scenario_consistency=1.0000; subgroup_r2=[dynamic=1.0000, nominal=1.0000, throttle_biased=1.0000]
- `full_augmented | selected_state_subset | ols_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=1.0000; scenario_consistency=1.0000; subgroup_r2=[dynamic=1.0000, nominal=1.0000, throttle_biased=1.0000]
- `commands_plus_state_history | selected_state_subset | ridge_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=1.0000; scenario_consistency=1.0000; subgroup_r2=[dynamic=1.0000, nominal=1.0000, throttle_biased=1.0000]
- `full_augmented | selected_state_subset | ridge_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=1.0000; scenario_consistency=1.0000; subgroup_r2=[dynamic=1.0000, nominal=1.0000, throttle_biased=1.0000]
- `commands_plus_state_history | selected_state_subset | lasso_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=1.0000; scenario_consistency=1.0000; subgroup_r2=[dynamic=1.0000, nominal=1.0000, throttle_biased=1.0000]
- `full_augmented | selected_state_subset | lasso_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=1.0000; scenario_consistency=1.0000; subgroup_r2=[dynamic=1.0000, nominal=1.0000, throttle_biased=1.0000]
- `commands_plus_state_history | next_raw_state | ridge_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.9168; scenario_consistency=0.9952; subgroup_r2=[dynamic=0.9140, nominal=0.9174, throttle_biased=0.9184]
- `commands_plus_state_history | next_raw_state | ols_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.9168; scenario_consistency=0.9948; subgroup_r2=[dynamic=0.9139, nominal=0.9177, throttle_biased=0.9187]
- `full_augmented | next_raw_state | ridge_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.9168; scenario_consistency=0.9952; subgroup_r2=[dynamic=0.9139, nominal=0.9174, throttle_biased=0.9183]
- `commands_plus_state_history | next_raw_state | lasso_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.9167; scenario_consistency=0.9956; subgroup_r2=[dynamic=0.9141, nominal=0.9170, throttle_biased=0.9181]
- `full_augmented | next_raw_state | ols_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.9166; scenario_consistency=0.9949; subgroup_r2=[dynamic=0.9138, nominal=0.9176, throttle_biased=0.9185]
- `full_augmented | next_raw_state | lasso_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.9165; scenario_consistency=0.9957; subgroup_r2=[dynamic=0.9140, nominal=0.9170, throttle_biased=0.9179]

## Conclusion
- 当前 study 尚未给出跨 scenario generalized_supported 的组合，高分结果更像局部状态下的线性近似。