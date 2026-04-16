# ArduPilot A2 STABILIZE Readiness

- ready_for_attack_v1: no
- next_step: iterate_capture_profile_only
- sign_ref: -1 (-0.430)
- blocking_reasons: nominal_monotonicity_failed, proxy_dynamic_accepted_target_not_met, proxy_dynamic_direction_consistency_below_threshold, proxy_dynamic_predictability_cv_above_threshold, proxy_dynamic_failsafe_rate_above_threshold, throttle_biased_monotonicity_failed

## Scenario Matrix

| scenario | ready | accepted_count | attempt_count | dir_consistency | predictability_cv | small_snr_gate | monotonicity | failsafe_rate | gate_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nominal | no | 5 | 10 | 1.000 | 0.333 | yes | no | 0.000 | 0.000 |
| proxy_dynamic | no | 0 | 0 | n/a | n/a | no | no | n/a | n/a |
| throttle_biased | no | 5 | 10 | 1.000 | 0.333 | yes | no | 0.000 | 0.000 |

## nominal

- ready: no
- blocking_reasons: nominal_monotonicity_failed
- small: accepted=5, snr=100000.000, effect_abs=0.100, slope_abs=3.704
- medium: accepted=5, snr=100000.000, effect_abs=0.100, slope_abs=1.852

## proxy_dynamic

- ready: no
- blocking_reasons: proxy_dynamic_accepted_target_not_met, proxy_dynamic_direction_consistency_below_threshold, proxy_dynamic_predictability_cv_above_threshold, proxy_dynamic_failsafe_rate_above_threshold
- small: accepted=0, snr=n/a, effect_abs=n/a, slope_abs=n/a
- medium: accepted=0, snr=n/a, effect_abs=n/a, slope_abs=n/a

## throttle_biased

- ready: no
- blocking_reasons: throttle_biased_monotonicity_failed
- small: accepted=5, snr=100000.000, effect_abs=0.100, slope_abs=3.086
- medium: accepted=5, snr=100000.000, effect_abs=0.100, slope_abs=1.543
