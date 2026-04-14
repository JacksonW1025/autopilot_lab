# Scenario Holdout

- status: `holdout_available`
- expected_scenarios: dynamic, nominal, throttle_biased

## Status Counts
- all_holdouts_supported: 0
- supported_but_holdout_local: 0
- holdout_failed: 12
- representative_combo: `commands_plus_state_history | selected_state_subset | ols_affine | pooled`

## Combo Reading
- `commands_plus_state_history | selected_state_subset | ols_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=1.0000; coefficient_stability=1.0000; effective_condition_number=557227689.1334; holdouts=[dynamic=1.0000:partial, nominal=1.0000:partial, throttle_biased=1.0000:partial]
- `full_augmented | selected_state_subset | ols_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=1.0000; coefficient_stability=1.0000; effective_condition_number=558973307.0566; holdouts=[dynamic=1.0000:partial, nominal=1.0000:partial, throttle_biased=1.0000:partial]
- `commands_plus_state_history | selected_state_subset | ridge_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=1.0000; coefficient_stability=1.0000; effective_condition_number=557227689.1334; holdouts=[dynamic=1.0000:partial, nominal=1.0000:partial, throttle_biased=1.0000:partial]
- `full_augmented | selected_state_subset | ridge_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=1.0000; coefficient_stability=0.9881; effective_condition_number=558973307.0566; holdouts=[dynamic=0.9967:partial, nominal=0.9989:partial, throttle_biased=0.9998:partial]
- `commands_plus_state_history | selected_state_subset | lasso_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=1.0000; coefficient_stability=0.9408; effective_condition_number=557227689.1334; holdouts=[dynamic=1.0000:partial, nominal=1.0000:partial, throttle_biased=1.0000:partial]
- `full_augmented | selected_state_subset | lasso_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=1.0000; coefficient_stability=0.9464; effective_condition_number=558973307.0566; holdouts=[dynamic=0.9990:partial, nominal=0.9735:partial, throttle_biased=1.0000:partial]
- `commands_plus_state_history | next_raw_state | lasso_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9126; coefficient_stability=0.8289; effective_condition_number=557227689.1334; holdouts=[dynamic=0.9021:partial, nominal=0.9118:partial, throttle_biased=0.9135:partial]
- `commands_plus_state_history | next_raw_state | ridge_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9126; coefficient_stability=0.8807; effective_condition_number=557227689.1334; holdouts=[dynamic=0.9035:partial, nominal=0.9117:partial, throttle_biased=0.8739:partial]
- `commands_plus_state_history | next_raw_state | ols_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9126; coefficient_stability=0.8632; effective_condition_number=557227689.1334; holdouts=[dynamic=0.9018:partial, nominal=0.9116:partial, throttle_biased=-12372889826486252.0000:unsupported]
- `full_augmented | next_raw_state | lasso_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9126; coefficient_stability=0.8024; effective_condition_number=558973307.0566; holdouts=[dynamic=0.9018:partial, nominal=0.9115:partial, throttle_biased=0.9135:partial]
- `full_augmented | next_raw_state | ridge_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9125; coefficient_stability=0.8365; effective_condition_number=558973307.0566; holdouts=[dynamic=0.9033:partial, nominal=0.9114:partial, throttle_biased=0.9106:partial]
- `full_augmented | next_raw_state | ols_affine | pooled`: holdout_status=holdout_failed; support=partial; median_test_r2=0.9125; coefficient_stability=0.8270; effective_condition_number=558973307.0566; holdouts=[dynamic=-343170571.8618:unsupported, nominal=0.9106:partial, throttle_biased=-13528585344716996.0000:unsupported]

## Conclusion
- 当前 study 还没有出现跨三个 holdout 都稳定通过的组合，leave-one-scenario-out 证据仍偏弱。