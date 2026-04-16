# ArduPilot A2 STABILIZE Boundary Readiness

- ready_for_binary_attack_v1: no
- recommended_path: iterate_boundary_protocol_only
- blocking_reasons: nominal_micro_trigger_rate_above_ceiling, nominal_micro_floor_hit_rate_above_ceiling, nominal_micro_baseline_false_trigger_rate_above_ceiling, nominal_probe_trigger_rate_below_floor, nominal_probe_recovery_rate_below_floor, nominal_confirm_floor_hit_rate_regressed, nominal_confirm_recovery_rate_below_floor, throttle_biased_micro_trigger_rate_above_ceiling, throttle_biased_micro_floor_hit_rate_above_ceiling, throttle_biased_micro_baseline_false_trigger_rate_above_ceiling, throttle_biased_probe_trigger_rate_below_floor, throttle_biased_probe_recovery_rate_below_floor, throttle_biased_confirm_recovery_rate_below_floor

## Scenario Matrix

| scenario | ready | threshold_window_present | accepted_count | attempt_count | failsafe_rate | gate_rate |
| --- | --- | --- | --- | --- | --- | --- |
| nominal | no | no | 5 | 15 | 0.000 | 0.000 |
| throttle_biased | no | no | 5 | 15 | 0.000 | 0.000 |

## nominal

- ready: no
- threshold_window_present: no
- blocking_reasons: nominal_micro_trigger_rate_above_ceiling, nominal_micro_floor_hit_rate_above_ceiling, nominal_micro_baseline_false_trigger_rate_above_ceiling, nominal_probe_trigger_rate_below_floor, nominal_probe_recovery_rate_below_floor, nominal_confirm_floor_hit_rate_regressed, nominal_confirm_recovery_rate_below_floor
- micro: accepted=5, trigger_rate=0.600, floor_hit_rate=0.594, baseline_false_trigger_rate=0.391, hit_latency_ms=0.000, recovery_rate=0.500, pattern_consistency=1.000
- probe: accepted=5, trigger_rate=0.600, floor_hit_rate=0.606, baseline_false_trigger_rate=0.386, hit_latency_ms=0.000, recovery_rate=0.500, pattern_consistency=1.000
- confirm: accepted=5, trigger_rate=0.600, floor_hit_rate=0.588, baseline_false_trigger_rate=0.386, hit_latency_ms=0.000, recovery_rate=0.500, pattern_consistency=1.000

## throttle_biased

- ready: no
- threshold_window_present: no
- blocking_reasons: throttle_biased_micro_trigger_rate_above_ceiling, throttle_biased_micro_floor_hit_rate_above_ceiling, throttle_biased_micro_baseline_false_trigger_rate_above_ceiling, throttle_biased_probe_trigger_rate_below_floor, throttle_biased_probe_recovery_rate_below_floor, throttle_biased_confirm_recovery_rate_below_floor
- micro: accepted=5, trigger_rate=0.600, floor_hit_rate=0.594, baseline_false_trigger_rate=0.389, hit_latency_ms=0.000, recovery_rate=0.500, pattern_consistency=1.000
- probe: accepted=5, trigger_rate=0.600, floor_hit_rate=0.606, baseline_false_trigger_rate=0.386, hit_latency_ms=0.000, recovery_rate=0.500, pattern_consistency=1.000
- confirm: accepted=5, trigger_rate=0.600, floor_hit_rate=0.606, baseline_false_trigger_rate=0.386, hit_latency_ms=0.000, recovery_rate=0.474, pattern_consistency=1.000
