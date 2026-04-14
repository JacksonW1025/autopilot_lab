# Scenario Holdout

- status: `holdout_available`
- expected_scenarios: dynamic, nominal, throttle_biased

## Status Counts
- all_holdouts_supported: 0
- supported_but_holdout_local: 0
- holdout_failed: 12
- representative_combo: `commands_plus_state_history | selected_state_subset | ols_affine | pooled`

## Combo Reading
- `commands_plus_state_history | selected_state_subset | ols_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=1.0000; coefficient_stability=1.0000; effective_condition_number=1601897234.1406; holdouts=[dynamic=0.9881:partial, nominal=1.0000:partial, throttle_biased=1.0000:partial]
- `full_augmented | selected_state_subset | ols_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=1.0000; coefficient_stability=1.0000; effective_condition_number=1607623878.9328; holdouts=[dynamic=0.9728:partial, nominal=0.9984:partial, throttle_biased=0.9958:partial]
- `commands_plus_state_history | selected_state_subset | ridge_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=1.0000; coefficient_stability=1.0000; effective_condition_number=1601897234.1406; holdouts=[dynamic=0.9569:partial, nominal=1.0000:partial, throttle_biased=1.0000:partial]
- `full_augmented | selected_state_subset | ridge_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=1.0000; coefficient_stability=0.9841; effective_condition_number=1607623878.9328; holdouts=[dynamic=-2524.4343:unsupported, nominal=0.9975:partial, throttle_biased=0.9948:partial]
- `commands_plus_state_history | selected_state_subset | lasso_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=1.0000; coefficient_stability=0.9474; effective_condition_number=1601897234.1406; holdouts=[dynamic=0.9981:partial, nominal=1.0000:partial, throttle_biased=1.0000:partial]
- `full_augmented | selected_state_subset | lasso_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=1.0000; coefficient_stability=0.9524; effective_condition_number=1607623878.9328; holdouts=[dynamic=0.9976:partial, nominal=0.9939:partial, throttle_biased=0.9967:partial]
- `commands_plus_state_history | next_raw_state | ridge_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9168; coefficient_stability=0.8439; effective_condition_number=1601897234.1406; holdouts=[dynamic=-28.4507:unsupported, nominal=0.9165:partial, throttle_biased=0.8983:partial]
- `commands_plus_state_history | next_raw_state | ols_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9168; coefficient_stability=0.8123; effective_condition_number=1601897234.1406; holdouts=[dynamic=-3976931258261140144128.0000:unsupported, nominal=0.9168:partial, throttle_biased=0.8928:partial]
- `full_augmented | next_raw_state | ridge_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9168; coefficient_stability=0.8056; effective_condition_number=1607623878.9328; holdouts=[dynamic=-27258.1682:unsupported, nominal=0.9085:partial, throttle_biased=0.8978:partial]
- `commands_plus_state_history | next_raw_state | lasso_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9167; coefficient_stability=0.7596; effective_condition_number=1601897234.1406; holdouts=[dynamic=0.9005:partial, nominal=0.9164:partial, throttle_biased=0.8980:partial]
- `full_augmented | next_raw_state | ols_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9166; coefficient_stability=0.7817; effective_condition_number=1607623878.9328; holdouts=[dynamic=-12735125336900967071744.0000:unsupported, nominal=0.8992:partial, throttle_biased=0.8930:partial]
- `full_augmented | next_raw_state | lasso_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9165; coefficient_stability=0.7452; effective_condition_number=1607623878.9328; holdouts=[dynamic=-11.0782:unsupported, nominal=0.9132:partial, throttle_biased=0.8958:partial]

## Conclusion
- 当前 study 还没有出现跨三个 holdout 都稳定通过的组合，leave-one-scenario-out 证据仍偏弱。