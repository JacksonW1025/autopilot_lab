# ArduPilot A2 STABILIZE Readiness

- ready_for_attack_v1: no
- next_step: iterate_capture_profile_only
- sign_ref: -1 (-0.430)
- blocking_reasons: nominal_accepted_target_not_met, nominal_direction_consistency_below_threshold, nominal_monotonicity_failed, proxy_dynamic_accepted_target_not_met, proxy_dynamic_direction_consistency_below_threshold, proxy_dynamic_predictability_cv_above_threshold, proxy_dynamic_failsafe_rate_above_threshold, throttle_biased_accepted_target_not_met, throttle_biased_direction_consistency_below_threshold, throttle_biased_predictability_cv_above_threshold, throttle_biased_small_tier_below_snr_gate, throttle_biased_monotonicity_failed, throttle_biased_failsafe_rate_above_threshold, throttle_biased_gate_rate_above_threshold

## Scenario Matrix

| scenario | ready | accepted_count | attempt_count | dir_consistency | predictability_cv | small_snr_gate | monotonicity | failsafe_rate | gate_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nominal | no | 1 | 2 | 0.000 | 0.333 | yes | no | 0.000 | 0.000 |
| proxy_dynamic | no | 0 | 0 | n/a | n/a | no | no | n/a | n/a |
| throttle_biased | no | 0 | 0 | n/a | n/a | no | no | n/a | n/a |

## nominal

- ready: no
- blocking_reasons: nominal_accepted_target_not_met, nominal_direction_consistency_below_threshold, nominal_monotonicity_failed
- small: accepted=1, snr=100000.000, slope_abs=20.000
- medium: accepted=1, snr=100000.000, slope_abs=10.000

## proxy_dynamic

- ready: no
- blocking_reasons: proxy_dynamic_accepted_target_not_met, proxy_dynamic_direction_consistency_below_threshold, proxy_dynamic_predictability_cv_above_threshold, proxy_dynamic_failsafe_rate_above_threshold
- small: accepted=0, snr=n/a, slope_abs=n/a
- medium: accepted=0, snr=n/a, slope_abs=n/a

## throttle_biased

- ready: no
- blocking_reasons: throttle_biased_accepted_target_not_met, throttle_biased_direction_consistency_below_threshold, throttle_biased_predictability_cv_above_threshold, throttle_biased_small_tier_below_snr_gate, throttle_biased_monotonicity_failed, throttle_biased_failsafe_rate_above_threshold, throttle_biased_gate_rate_above_threshold
- small: accepted=0, snr=n/a, slope_abs=n/a
- medium: accepted=0, snr=n/a, slope_abs=n/a
