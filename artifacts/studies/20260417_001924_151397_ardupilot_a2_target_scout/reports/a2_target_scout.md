# ArduPilot A2 Target Scout

- recommended_next_target: pair_imbalance_12_vs_34
- recommended_next_step: guided_nogps_pair_target_readiness
- recommended_mode: GUIDED_NOGPS
- blocking_reasons: single_actuator_symmetry_collapse, single_actuator_symmetry_collapse

## Scenario Matrix

| mode | scenario | recommended_target | accepted_count | collective_specificity | pair_specificity | best_single | spread |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GUIDED_NOGPS | nominal | pair_imbalance_12_vs_34 | 15 | 0.215 | 0.187 | actuator_1 | 0.000 |
| GUIDED_NOGPS | throttle_biased | pair_imbalance_12_vs_34 | 15 | 0.205 | 0.193 | actuator_1 | 0.000 |

## GUIDED_NOGPS / nominal

- recommended_target: pair_imbalance_12_vs_34
- recommended_path: guided_nogps_pair_target_readiness
- collective_floor: specificity=0.215, tier_range=0.023
- pair_imbalance: specificity=0.187, active_rate=0.206, sign_consistency=1.000, direction=12_gt_34
- best_single_actuator: actuator_1 (specificity=0.215, tier_range=0.023)
- dominant_states: active=0.000|0.000|0.000|0.000 (1.000), baseline=0.000|0.000|0.000|0.000 (1.000)
- blocking_reasons: single_actuator_symmetry_collapse

## GUIDED_NOGPS / throttle_biased

- recommended_target: pair_imbalance_12_vs_34
- recommended_path: guided_nogps_pair_target_readiness
- collective_floor: specificity=0.205, tier_range=0.018
- pair_imbalance: specificity=0.193, active_rate=0.206, sign_consistency=1.000, direction=12_gt_34
- best_single_actuator: actuator_1 (specificity=0.205, tier_range=0.018)
- dominant_states: active=0.000|0.000|0.000|0.000 (1.000), baseline=0.000|0.000|0.000|0.000 (1.000)
- blocking_reasons: single_actuator_symmetry_collapse
