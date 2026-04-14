# Scenario Holdout

- status: `holdout_available`
- expected_scenarios: dynamic, nominal, throttle_biased

## Status Counts
- all_holdouts_supported: 9
- supported_but_holdout_local: 1
- holdout_failed: 2
- representative_combo: `commands_plus_state_history | selected_state_subset | ols_affine | pooled`

## Combo Reading
- `commands_plus_state_history | selected_state_subset | ols_affine | pooled`: holdout_status=all_holdouts_supported; support=supported; median_test_r2=1.0000; coefficient_stability=0.8431; effective_condition_number=549554.6354; holdouts=[dynamic=1.0000:supported, nominal=1.0000:supported, throttle_biased=1.0000:supported]
- `commands_plus_state_history | next_raw_state | ols_affine | pooled`: holdout_status=all_holdouts_supported; support=supported; median_test_r2=0.9171; coefficient_stability=0.7294; effective_condition_number=549554.6354; holdouts=[dynamic=0.7926:supported, nominal=0.9186:supported, throttle_biased=0.9006:supported]
- `full_augmented | next_raw_state | ols_affine | pooled`: holdout_status=all_holdouts_supported; support=supported; median_test_r2=0.9171; coefficient_stability=0.7481; effective_condition_number=549554.6354; holdouts=[dynamic=0.7926:supported, nominal=0.9186:supported, throttle_biased=0.9006:supported]
- `full_augmented | next_raw_state | lasso_affine | pooled`: holdout_status=all_holdouts_supported; support=supported; median_test_r2=0.9171; coefficient_stability=0.9130; effective_condition_number=549554.6354; holdouts=[dynamic=0.9014:supported, nominal=0.9186:supported, throttle_biased=0.9040:supported]
- `commands_plus_state_history | next_raw_state | lasso_affine | pooled`: holdout_status=all_holdouts_supported; support=supported; median_test_r2=0.9171; coefficient_stability=0.9186; effective_condition_number=549554.6354; holdouts=[dynamic=0.9014:supported, nominal=0.9186:supported, throttle_biased=0.9039:supported]
- `full_augmented | next_raw_state | ridge_affine | pooled`: holdout_status=all_holdouts_supported; support=supported; median_test_r2=0.9171; coefficient_stability=0.7519; effective_condition_number=549554.6354; holdouts=[dynamic=0.8842:supported, nominal=0.9186:supported, throttle_biased=0.9029:supported]
- `commands_plus_state_history | next_raw_state | ridge_affine | pooled`: holdout_status=all_holdouts_supported; support=supported; median_test_r2=0.9171; coefficient_stability=0.7725; effective_condition_number=549554.6354; holdouts=[dynamic=0.8842:supported, nominal=0.9186:supported, throttle_biased=0.9028:supported]
- `full_augmented | selected_state_subset | ols_affine | pooled`: holdout_status=all_holdouts_supported; support=supported; median_test_r2=0.7168; coefficient_stability=0.8148; effective_condition_number=549554.6354; holdouts=[dynamic=1.0000:supported, nominal=1.0000:supported, throttle_biased=1.0000:supported]
- `full_augmented | selected_state_subset | ridge_affine | pooled`: holdout_status=all_holdouts_supported; support=supported; median_test_r2=0.7084; coefficient_stability=0.8148; effective_condition_number=549554.6354; holdouts=[dynamic=0.9101:supported, nominal=1.0000:supported, throttle_biased=1.0000:supported]
- `commands_plus_state_history | selected_state_subset | ridge_affine | pooled`: holdout_status=supported_but_holdout_local; support=supported; median_test_r2=0.7423; coefficient_stability=0.8431; effective_condition_number=549554.6354; holdouts=[dynamic=-0.2253:unsupported, nominal=1.0000:supported, throttle_biased=1.0000:supported]
- `full_augmented | selected_state_subset | lasso_affine | pooled`: holdout_status=holdout_failed; support=unsupported; median_test_r2=0.0816; coefficient_stability=0.9907; effective_condition_number=549554.6354; holdouts=[dynamic=-2.5438:unsupported, nominal=0.9999:supported, throttle_biased=0.9999:supported]
- `commands_plus_state_history | selected_state_subset | lasso_affine | pooled`: holdout_status=holdout_failed; support=unsupported; median_test_r2=-0.3618; coefficient_stability=1.0000; effective_condition_number=549554.6354; holdouts=[dynamic=-2.8129:unsupported, nominal=0.9999:supported, throttle_biased=0.9999:supported]

## Conclusion
- 当前 study 已出现 leave-one-scenario-out 仍然全部保持 supported 的组合，线性关系不只是在 pooled 数据上成立。