# ArduPilot A2 Target Scout

- recommended_next_target: none
- recommended_next_step: no_target_signal_identified
- recommended_mode: none
- blocking_reasons: pair_active_rate_below_threshold, pair_sign_consistency_below_threshold, pair_specificity_below_threshold, single_actuator_symmetry_collapse, pair_active_rate_below_threshold, pair_sign_consistency_below_threshold, pair_specificity_below_threshold, single_actuator_symmetry_collapse

## Scenario Matrix

| mode | scenario | recommended_target | accepted_count | collective_specificity | pair_specificity | best_single | spread |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STABILIZE | nominal | collective_floor_state | 15 | 0.204 | 0.000 | actuator_1 | 0.000 |
| STABILIZE | throttle_biased | collective_floor_state | 15 | 0.220 | 0.000 | actuator_1 | 0.000 |

## STABILIZE / nominal

- recommended_target: collective_floor_state
- recommended_path: collective_only_no_new_target_gain
- collective_floor: specificity=0.204, tier_range=0.021
- pair_imbalance: specificity=0.000, active_rate=0.000, sign_consistency=n/a, direction=none
- best_single_actuator: actuator_1 (specificity=0.204, tier_range=0.021)
- dominant_states: active=0.000|0.000|0.000|0.000 (1.000), baseline=0.100|0.100|0.100|0.100 (1.000)
- blocking_reasons: pair_active_rate_below_threshold, pair_sign_consistency_below_threshold, pair_specificity_below_threshold, single_actuator_symmetry_collapse

## STABILIZE / throttle_biased

- recommended_target: collective_floor_state
- recommended_path: collective_only_no_new_target_gain
- collective_floor: specificity=0.220, tier_range=0.019
- pair_imbalance: specificity=0.000, active_rate=0.000, sign_consistency=n/a, direction=none
- best_single_actuator: actuator_1 (specificity=0.220, tier_range=0.019)
- dominant_states: active=0.000|0.000|0.000|0.000 (1.000), baseline=0.100|0.100|0.100|0.100 (1.000)
- blocking_reasons: pair_active_rate_below_threshold, pair_sign_consistency_below_threshold, pair_specificity_below_threshold, single_actuator_symmetry_collapse
