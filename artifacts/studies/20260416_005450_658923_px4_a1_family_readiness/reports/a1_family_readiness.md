# PX4 A1 Family Readiness

- selected_family: attitude_roll_pitch_continuation
- ready_for_reproduction_v1: yes
- recommended_path: continue_px4_a1_attitude_reproduction
- blocking_reasons: none

## Readiness

- baseline_scenario_consistency=0.990, diagnostic_scenario_consistency=0.998
- baseline_min_scenario_r2=0.953, diagnostic_min_scenario_r2=0.992
- baseline_same_family_share=0.593, diagnostic_same_family_share=0.710
- median_command_share=0.083, median_mode_share=0.000
- top1_stability_rate=1.000, top1_sign_match_rate=1.000, median_top5_jaccard=0.548

## Responses

- future_state_roll: baseline_top1=roll (2.390), diagnostic_top1=roll (2.302), same_family=0.596/0.738, top5_jaccard=0.429
- future_state_pitch: baseline_top1=pitch (2.215), diagnostic_top1=pitch (2.118), same_family=0.590/0.682, top5_jaccard=0.667
