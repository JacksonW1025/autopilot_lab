# Scenario Generalization

- status: `scenario_available`
- expected_scenarios: dynamic, nominal, throttle_biased

## Status Counts
- generalized_supported: 0
- supported_but_local: 0
- not_generalized: 12

## Combo Reading
- `commands_plus_state_history | selected_state_subset | ols_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.9289; scenario_consistency=0.9800; subgroup_r2=[dynamic=0.9800, nominal=1.0000, throttle_biased=1.0000]
- `commands_plus_state_history | next_raw_state | lasso_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.9153; scenario_consistency=0.9928; subgroup_r2=[dynamic=0.9143, nominal=0.9139, throttle_biased=0.9205]
- `full_augmented | next_raw_state | lasso_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.9153; scenario_consistency=0.9928; subgroup_r2=[dynamic=0.9143, nominal=0.9139, throttle_biased=0.9206]
- `full_augmented | next_raw_state | ridge_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.9152; scenario_consistency=0.9929; subgroup_r2=[dynamic=0.9143, nominal=0.9140, throttle_biased=0.9205]
- `full_augmented | next_raw_state | ols_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.9018; scenario_consistency=0.9900; subgroup_r2=[dynamic=0.9114, nominal=0.9140, throttle_biased=0.9205]
- `commands_plus_state_history | next_raw_state | ridge_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.9010; scenario_consistency=0.9886; subgroup_r2=[dynamic=0.9101, nominal=0.9140, throttle_biased=0.9205]
- `commands_plus_state_history | selected_state_subset | ridge_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.7139; scenario_consistency=0.9082; subgroup_r2=[dynamic=0.9082, nominal=1.0000, throttle_biased=1.0000]
- `full_augmented | selected_state_subset | ols_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.6935; scenario_consistency=0.8973; subgroup_r2=[dynamic=0.8973, nominal=1.0000, throttle_biased=1.0000]
- `full_augmented | selected_state_subset | ridge_affine | pooled`: generalization_status=not_generalized; support=partial; median_test_r2=0.6579; scenario_consistency=0.8880; subgroup_r2=[dynamic=0.8880, nominal=1.0000, throttle_biased=1.0000]
- `full_augmented | selected_state_subset | lasso_affine | pooled`: generalization_status=not_generalized; support=unsupported; median_test_r2=0.2002; scenario_consistency=0.7426; subgroup_r2=[dynamic=0.7426, nominal=1.0000, throttle_biased=1.0000]
- `commands_plus_state_history | selected_state_subset | lasso_affine | pooled`: generalization_status=not_generalized; support=unsupported; median_test_r2=0.1971; scenario_consistency=0.7416; subgroup_r2=[dynamic=0.7416, nominal=1.0000, throttle_biased=1.0000]
- `commands_plus_state_history | next_raw_state | ols_affine | pooled`: generalization_status=not_generalized; support=unsupported; median_test_r2=-15700.6207; scenario_consistency=0.0000; subgroup_r2=[dynamic=-3469.7197, nominal=0.9140, throttle_biased=0.9205]

## Conclusion
- 当前 study 尚未给出跨 scenario generalized_supported 的组合，高分结果更像局部状态下的线性近似。