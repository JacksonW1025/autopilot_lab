# Scenario Holdout

- status: `holdout_available`
- expected_scenarios: dynamic, nominal, throttle_biased

## Status Counts
- all_holdouts_supported: 0
- supported_but_holdout_local: 0
- holdout_failed: 12
- representative_combo: `commands_plus_state_history | selected_state_subset | ols_affine | pooled`

## Combo Reading
- `commands_plus_state_history | selected_state_subset | ols_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9289; coefficient_stability=0.8431; effective_condition_number=7535808.5063; holdouts=[dynamic=1.0000:partial, nominal=1.0000:supported, throttle_biased=-4357.7862:unsupported]
- `commands_plus_state_history | next_raw_state | lasso_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9153; coefficient_stability=0.9176; effective_condition_number=7535808.5063; holdouts=[dynamic=0.9020:partial, nominal=0.9131:supported, throttle_biased=0.9134:partial]
- `full_augmented | next_raw_state | lasso_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9153; coefficient_stability=0.9037; effective_condition_number=7535808.5063; holdouts=[dynamic=0.9019:partial, nominal=0.9131:supported, throttle_biased=0.9134:partial]
- `full_augmented | next_raw_state | ridge_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9152; coefficient_stability=0.7519; effective_condition_number=7535808.5063; holdouts=[dynamic=0.9026:partial, nominal=0.9131:supported, throttle_biased=0.7706:partial]
- `full_augmented | next_raw_state | ols_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9018; coefficient_stability=0.7519; effective_condition_number=7535808.5063; holdouts=[dynamic=0.8998:partial, nominal=0.9131:supported, throttle_biased=-343.9593:unsupported]
- `commands_plus_state_history | next_raw_state | ridge_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9010; coefficient_stability=0.7725; effective_condition_number=7535808.5063; holdouts=[dynamic=0.9014:partial, nominal=0.9131:supported, throttle_biased=0.8999:partial]
- `commands_plus_state_history | selected_state_subset | ridge_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.7139; coefficient_stability=0.8431; effective_condition_number=7535808.5063; holdouts=[dynamic=0.8995:partial, nominal=1.0000:supported, throttle_biased=-69.5162:unsupported]
- `full_augmented | selected_state_subset | ols_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.6935; coefficient_stability=0.8148; effective_condition_number=7535808.5063; holdouts=[dynamic=0.9068:partial, nominal=1.0000:supported, throttle_biased=-59.2797:unsupported]
- `full_augmented | selected_state_subset | ridge_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.6579; coefficient_stability=0.8148; effective_condition_number=7535808.5063; holdouts=[dynamic=0.8885:partial, nominal=1.0000:supported, throttle_biased=-72.3405:unsupported]
- `full_augmented | selected_state_subset | lasso_affine | pooled`: holdout_status=holdout_failed; support=unsupported; median_test_r2=0.2002; coefficient_stability=0.9931; effective_condition_number=7535808.5063; holdouts=[dynamic=0.7426:partial, nominal=0.9999:supported, throttle_biased=1.0000:partial]
- `commands_plus_state_history | selected_state_subset | lasso_affine | pooled`: holdout_status=holdout_failed; support=unsupported; median_test_r2=0.1971; coefficient_stability=1.0000; effective_condition_number=7535808.5063; holdouts=[dynamic=0.7420:partial, nominal=0.9999:supported, throttle_biased=1.0000:partial]
- `commands_plus_state_history | next_raw_state | ols_affine | pooled`: holdout_status=holdout_failed; support=unsupported; median_test_r2=-15700.6207; coefficient_stability=0.7333; effective_condition_number=7535808.5063; holdouts=[dynamic=-3225.6455:unsupported, nominal=0.9131:supported, throttle_biased=-19260433888.2431:unsupported]

## Conclusion
- 当前 study 还没有出现跨三个 holdout 都稳定通过的组合，leave-one-scenario-out 证据仍偏弱。