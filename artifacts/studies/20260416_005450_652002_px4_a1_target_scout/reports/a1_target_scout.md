# PX4 A1 Target Scout

- recommended_next_target: attitude_roll_pitch_continuation
- recommended_next_step: start_px4_a1_attitude_family_readiness
- selected_family: attitude_roll_pitch_continuation
- combo_ready: yes

## Family Matrix

| family | supported | baseline_same | diagnostic_same | command | top1_stable | top5_jaccard |
| --- | --- | --- | --- | --- | --- | --- |
| attitude_roll_pitch_continuation | yes | 0.593 | 0.710 | 0.083 | 1.000 | 0.548 |
| yaw_heading_continuation | yes | 0.467 | 0.511 | 0.113 | 1.000 | 0.429 |
| horizontal_position_continuation | no | 0.380 | 0.565 | 0.020 | 1.000 | 0.250 |
| vertical_dual_continuation | no | 0.308 | 0.506 | 0.026 | 1.000 | 0.250 |
| horizontal_velocity_continuation | no | 0.252 | 0.347 | 0.071 | 1.000 | 0.548 |

## attitude_roll_pitch_continuation

- responses: future_state_roll, future_state_pitch
- baseline_same_family_share=0.593, diagnostic_same_family_share=0.710, median_command_share=0.083, median_mode_share=0.000
- top1_stability_rate=1.000, top1_sign_match_rate=1.000, median_top5_jaccard=0.548
- blocking_reasons: none

## yaw_heading_continuation

- responses: future_state_yaw, future_state_heading, future_state_yaw_rate
- baseline_same_family_share=0.467, diagnostic_same_family_share=0.511, median_command_share=0.113, median_mode_share=0.000
- top1_stability_rate=1.000, top1_sign_match_rate=1.000, median_top5_jaccard=0.429
- blocking_reasons: none

## horizontal_position_continuation

- responses: future_state_position_x, future_state_position_y
- baseline_same_family_share=0.380, diagnostic_same_family_share=0.565, median_command_share=0.020, median_mode_share=0.000
- top1_stability_rate=1.000, top1_sign_match_rate=1.000, median_top5_jaccard=0.250
- blocking_reasons: baseline_same_family_share_below_threshold, top5_overlap_below_threshold

## vertical_dual_continuation

- responses: future_state_position_z, future_state_altitude
- baseline_same_family_share=0.308, diagnostic_same_family_share=0.506, median_command_share=0.026, median_mode_share=0.000
- top1_stability_rate=1.000, top1_sign_match_rate=1.000, median_top5_jaccard=0.250
- blocking_reasons: baseline_same_family_share_below_threshold, top5_overlap_below_threshold

## horizontal_velocity_continuation

- responses: future_state_velocity_x, future_state_velocity_y
- baseline_same_family_share=0.252, diagnostic_same_family_share=0.347, median_command_share=0.071, median_mode_share=0.000
- top1_stability_rate=1.000, top1_sign_match_rate=1.000, median_top5_jaccard=0.548
- blocking_reasons: baseline_same_family_share_below_threshold, diagnostic_same_family_share_below_threshold
