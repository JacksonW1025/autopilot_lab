# PX4 A1 Roll/Pitch Targeted Reproduction

- selected_family: attitude_roll_pitch_continuation
- selected_responses: future_state_roll, future_state_pitch
- ready_for_targeted_reproduction_v1: yes
- recommended_path: lock_px4_a1_roll_pitch_targeted_scope
- blocking_reasons: none

## Phase Generalization

- baseline_scenario_consistency=0.990, baseline_min_scenario_r2=0.953
- diagnostic_scenario_consistency=0.998, diagnostic_min_scenario_r2=0.992

## Responses

- future_state_roll: top1=roll/roll, direct=0.314/0.360, lag=0.282/0.378, same_axis=0.596/0.738, command=0.096/0.052, cross_axis=0.021/0.029, top5_same_axis=3/4, blocking=none
- future_state_pitch: top1=pitch/pitch, direct=0.310/0.363, lag=0.279/0.319, same_axis=0.590/0.682, command=0.131/0.053, cross_axis=0.010/0.018, top5_same_axis=4/4, blocking=none

## Top Features

- future_state_roll baseline_top5: roll (2.390), roll__lag_1 (-1.683), roll__lag_3 (0.331), yaw__lag_3 (0.192), heading__lag_3 (-0.173)
- future_state_roll diagnostic_top5: roll (2.302), roll__lag_1 (-1.283), roll__lag_2 (-0.630), roll__lag_3 (0.507), yaw__lag_1 (-0.116)
- future_state_pitch baseline_top5: pitch (2.215), pitch__lag_1 (-1.336), pitch__lag_2 (-0.340), pitch__lag_3 (0.319), heading__lag_3 (0.192)
- future_state_pitch diagnostic_top5: pitch (2.118), pitch__lag_1 (-1.177), pitch__lag_2 (-0.362), pitch__lag_3 (0.322), heading__lag_2 (0.113)
