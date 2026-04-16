# ArduPilot A2 STABILIZE Readiness

- ready_for_attack_v1: no
- next_step: iterate_capture_profile_only
- sign_ref: -1 (-0.430)
- blocking_reasons: nominal_accepted_target_not_met, nominal_predictability_cv_above_threshold, nominal_monotonicity_failed

## Scenario Matrix

| scenario | ready | accepted_count | attempt_count | dir_consistency | predictability_cv | small_snr_gate | monotonicity | failsafe_rate | gate_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nominal | no | 1 | 2 | 1.000 | 0.500 | yes | no | 0.000 | 0.000 |

## nominal

- ready: no
- blocking_reasons: nominal_accepted_target_not_met, nominal_predictability_cv_above_threshold, nominal_monotonicity_failed
- small: accepted=1, snr=100000.000, effect_abs=0.100, slope_abs=100.000
- medium: accepted=1, snr=100000.000, effect_abs=0.100, slope_abs=33.333
