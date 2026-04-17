# ArduPilot A2 Pair-Target Readiness

- ready_for_pair_attack_v1: yes
- recommended_path: start_guided_nogps_pair_attack_v1
- dominant_direction: 12_gt_34
- blocking_reasons: none

## Scenario Matrix

| scenario | ready | accepted_count | active_pair_rate | baseline_pair_rate | specificity | sign_consistency | ratio | direction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nominal | yes | 15 | 0.206 | 0.019 | 0.187 | 1.000 | 0.917 | 12_gt_34 |
| throttle_biased | yes | 15 | 0.206 | 0.019 | 0.193 | 1.000 | 0.946 | 12_gt_34 |

## nominal

- ready: yes
- pair metrics: active_rate=0.206, baseline_rate=0.019, specificity=0.187, sign_consistency=1.000, pair_to_collective_ratio=0.917, tier_range=0.024, direction=12_gt_34
- blocking_reasons: none

## throttle_biased

- ready: yes
- pair metrics: active_rate=0.206, baseline_rate=0.019, specificity=0.193, sign_consistency=1.000, pair_to_collective_ratio=0.946, tier_range=0.000, direction=12_gt_34
- blocking_reasons: none
