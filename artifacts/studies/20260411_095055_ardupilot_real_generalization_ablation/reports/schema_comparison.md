# Schema Comparison: ardupilot_real_generalization_ablation

## Results
### commands_plus_state_history x selected_state_subset | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 32
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x selected_state_subset | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 5
- sparsity_ratio: 0.9561
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x future_state_horizon | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 10
- sparsity_ratio: 0.9561
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### full_augmented x selected_state_subset | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000021
- coefficient_stability: 0.9884
- nonzero_count: 16
- sparsity_ratio: 0.9690
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000021
- coefficient_stability: 0.9884
- nonzero_count: 32
- sparsity_ratio: 0.9690
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000004
- median_test_mae: 0.000387
- coefficient_stability: 0.9719
- nonzero_count: 35
- sparsity_ratio: 0.9661
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000005
- median_test_mae: 0.000367
- coefficient_stability: 1.0000
- nonzero_count: 48
- sparsity_ratio: 0.9474
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x window_summary_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000005
- median_test_mae: 0.000367
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9386
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### full_augmented x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000006
- median_test_mae: 0.001059
- coefficient_stability: 0.9574
- nonzero_count: 22
- sparsity_ratio: 0.9574
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000006
- median_test_mae: 0.001059
- coefficient_stability: 0.9574
- nonzero_count: 44
- sparsity_ratio: 0.9574
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000006
- median_test_mae: 0.000957
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000006
- median_test_mae: 0.000957
- coefficient_stability: 1.0000
- nonzero_count: 32
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000733
- coefficient_stability: 0.9512
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 2318301332.3926
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000010
- median_test_mae: 0.001409
- coefficient_stability: 0.9564
- nonzero_count: 44
- sparsity_ratio: 0.9574
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000010
- median_test_mae: 0.001321
- coefficient_stability: 1.0000
- nonzero_count: 32
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001082
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 2203070525.4702
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001161
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.7895
- raw_condition_number: inf
- effective_condition_number: 161803597.2409
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state_history x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001174
- coefficient_stability: 1.0000
- nonzero_count: 32
- sparsity_ratio: 0.8947
- raw_condition_number: inf
- effective_condition_number: 2203070525.4702
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000027
- median_test_mae: 0.002225
- coefficient_stability: 0.9737
- nonzero_count: 18
- sparsity_ratio: 0.9211
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000027
- median_test_mae: 0.002225
- coefficient_stability: 0.9737
- nonzero_count: 9
- sparsity_ratio: 0.9211
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000003
- median_test_mae: 0.001376
- coefficient_stability: 0.9474
- nonzero_count: 8
- sparsity_ratio: 0.8947
- raw_condition_number: inf
- effective_condition_number: 161803597.2409
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x window_summary_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000032
- median_test_mae: 0.002586
- coefficient_stability: 0.9737
- nonzero_count: 18
- sparsity_ratio: 0.9211
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### full_augmented x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9999
- median_test_mse: 0.000005
- median_test_mae: 0.001063
- coefficient_stability: 0.9360
- nonzero_count: 40
- sparsity_ratio: 0.8780
- raw_condition_number: inf
- effective_condition_number: 2318301332.3926
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9994
- median_test_mse: 0.000050
- median_test_mae: 0.005927
- coefficient_stability: 0.9967
- nonzero_count: 152
- sparsity_ratio: 0.5000
- raw_condition_number: inf
- effective_condition_number: 2203070525.4702
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9993
- median_test_mse: 0.000058
- median_test_mae: 0.006413
- coefficient_stability: 0.9512
- nonzero_count: 152
- sparsity_ratio: 0.5366
- raw_condition_number: inf
- effective_condition_number: 2318301332.3926
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9992
- median_test_mse: 0.000590
- median_test_mae: 0.012274
- coefficient_stability: 0.9649
- nonzero_count: 243
- sparsity_ratio: 0.4671
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9992
- median_test_mse: 0.000590
- median_test_mae: 0.012274
- coefficient_stability: 0.9649
- nonzero_count: 486
- sparsity_ratio: 0.4671
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9992
- median_test_mse: 0.000598
- median_test_mae: 0.012588
- coefficient_stability: 0.9649
- nonzero_count: 480
- sparsity_ratio: 0.4737
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9989
- median_test_mse: 0.000847
- median_test_mae: 0.015258
- coefficient_stability: 0.9399
- nonzero_count: 242
- sparsity_ratio: 0.5310
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9989
- median_test_mse: 0.000847
- median_test_mae: 0.015258
- coefficient_stability: 0.9399
- nonzero_count: 484
- sparsity_ratio: 0.5310
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9989
- median_test_mse: 0.000855
- median_test_mae: 0.015575
- coefficient_stability: 0.9399
- nonzero_count: 485
- sparsity_ratio: 0.5300
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9989
- median_test_mse: 0.000087
- median_test_mae: 0.007957
- coefficient_stability: 0.9474
- nonzero_count: 53
- sparsity_ratio: 0.3026
- raw_condition_number: inf
- effective_condition_number: 161803597.2409
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001078
- median_test_mae: 0.017185
- coefficient_stability: 0.9474
- nonzero_count: 72
- sparsity_ratio: 0.3684
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001078
- median_test_mae: 0.017185
- coefficient_stability: 0.9474
- nonzero_count: 144
- sparsity_ratio: 0.3684
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x window_summary_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001086
- median_test_mae: 0.017498
- coefficient_stability: 0.9474
- nonzero_count: 144
- sparsity_ratio: 0.3684
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_only x actuator_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9986
- median_test_mse: 0.000116
- median_test_mae: 0.009860
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.7500
- raw_condition_number: 1.5097
- effective_condition_number: 1.5097
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9985
- median_test_mse: 0.000116
- median_test_mae: 0.009870
- coefficient_stability: 1.0000
- nonzero_count: 12
- sparsity_ratio: 0.2500
- raw_condition_number: 1.5097
- effective_condition_number: 1.5097
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9985
- median_test_mse: 0.000116
- median_test_mae: 0.009873
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.7500
- raw_condition_number: 1.5097
- effective_condition_number: 1.5097
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.001852
- median_test_mae: 0.026616
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.8333
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.001852
- median_test_mae: 0.026616
- coefficient_stability: 1.0000
- nonzero_count: 8
- sparsity_ratio: 0.8333
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.001856
- median_test_mae: 0.026770
- coefficient_stability: 1.0000
- nonzero_count: 7
- sparsity_ratio: 0.8542
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.001859
- median_test_mae: 0.026637
- coefficient_stability: 1.0000
- nonzero_count: 15
- sparsity_ratio: 0.3750
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.001859
- median_test_mae: 0.026637
- coefficient_stability: 1.0000
- nonzero_count: 30
- sparsity_ratio: 0.3750
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.001859
- median_test_mae: 0.026640
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.8333
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.001859
- median_test_mae: 0.026640
- coefficient_stability: 1.0000
- nonzero_count: 8
- sparsity_ratio: 0.8333
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.001863
- median_test_mae: 0.026791
- coefficient_stability: 1.0000
- nonzero_count: 30
- sparsity_ratio: 0.3750
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.001863
- median_test_mae: 0.026794
- coefficient_stability: 1.0000
- nonzero_count: 7
- sparsity_ratio: 0.8542
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 191844930398.153412
- median_test_mae: 27586.284982
- coefficient_stability: 0.8211
- nonzero_count: 232
- sparsity_ratio: 0.1860
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 191846202623.320679
- median_test_mae: 27702.070065
- coefficient_stability: 0.8632
- nonzero_count: 62
- sparsity_ratio: 0.7825
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 191849484102.131287
- median_test_mae: 27862.797214
- coefficient_stability: 0.8491
- nonzero_count: 68
- sparsity_ratio: 0.7614
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state_history x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9167
- median_test_mse: 186268502599.237885
- median_test_mae: 36626.731549
- coefficient_stability: 0.8807
- nonzero_count: 213
- sparsity_ratio: 0.8132
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9167
- median_test_mse: 186272520832.945526
- median_test_mae: 36651.089042
- coefficient_stability: 0.8380
- nonzero_count: 243
- sparsity_ratio: 0.8116
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9167
- median_test_mse: 186299625507.296997
- median_test_mae: 36758.620942
- coefficient_stability: 0.8544
- nonzero_count: 272
- sparsity_ratio: 0.7614
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9167
- median_test_mse: 186314068180.672058
- median_test_mae: 36448.459645
- coefficient_stability: 0.8404
- nonzero_count: 849
- sparsity_ratio: 0.2553
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9167
- median_test_mse: 186315257607.736572
- median_test_mae: 36463.141223
- coefficient_stability: 0.8248
- nonzero_count: 893
- sparsity_ratio: 0.3078
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9164
- median_test_mse: 187012857960.334991
- median_test_mae: 38103.998550
- coefficient_stability: 0.8132
- nonzero_count: 312
- sparsity_ratio: 0.7581
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0992
- median_test_mse: 186270345758.517303
- median_test_mae: 36610.925603
- coefficient_stability: 0.8807
- nonzero_count: 180
- sparsity_ratio: 0.8421
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0992
- median_test_mse: 186274348921.318512
- median_test_mae: 36635.251974
- coefficient_stability: 0.8612
- nonzero_count: 198
- sparsity_ratio: 0.8465
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0991
- median_test_mse: 186299625507.085999
- median_test_mae: 36758.620930
- coefficient_stability: 0.8544
- nonzero_count: 248
- sparsity_ratio: 0.7825
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0990
- median_test_mse: 186323352123.426331
- median_test_mae: 36415.592013
- coefficient_stability: 0.8798
- nonzero_count: 449
- sparsity_ratio: 0.6061
- raw_condition_number: inf
- effective_condition_number: 2202809596.0917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0990
- median_test_mse: 186324507834.051178
- median_test_mae: 36429.479979
- coefficient_stability: 0.8674
- nonzero_count: 477
- sparsity_ratio: 0.6302
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0956
- median_test_mse: 187012857962.291077
- median_test_mae: 38103.998530
- coefficient_stability: 0.8217
- nonzero_count: 288
- sparsity_ratio: 0.7767
- raw_condition_number: inf
- effective_condition_number: 2400561975.9333
- conditioning_pruned_features: actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0575
- median_test_mse: 191844906488.179382
- median_test_mae: 27585.012322
- coefficient_stability: 0.8772
- nonzero_count: 138
- sparsity_ratio: 0.5158
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0575
- median_test_mse: 191845790045.748871
- median_test_mae: 27675.405847
- coefficient_stability: 0.8772
- nonzero_count: 39
- sparsity_ratio: 0.8632
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0574
- median_test_mse: 191849484102.130981
- median_test_mae: 27862.797214
- coefficient_stability: 0.8491
- nonzero_count: 51
- sparsity_ratio: 0.8211
- raw_condition_number: inf
- effective_condition_number: 166994890.9947
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_only x next_raw_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0474
- median_test_mse: 2313390793094.323242
- median_test_mae: 327907.900972
- coefficient_stability: 0.7000
- nonzero_count: 50
- sparsity_ratio: 0.1667
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0474
- median_test_mse: 2313390793094.337402
- median_test_mae: 327907.900977
- coefficient_stability: 0.7000
- nonzero_count: 27
- sparsity_ratio: 0.5500
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0474
- median_test_mse: 2313392548694.664062
- median_test_mae: 327907.210770
- coefficient_stability: 0.7000
- nonzero_count: 27
- sparsity_ratio: 0.5500
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0035
- median_test_mse: 202826474486.348267
- median_test_mae: 28707.034051
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0035
- median_test_mse: 202826474486.382446
- median_test_mae: 28707.034048
- coefficient_stability: 0.8667
- nonzero_count: 32
- sparsity_ratio: 0.4667
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0035
- median_test_mse: 202826493462.162506
- median_test_mae: 28706.818512
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.5098
- effective_condition_number: 1.5098
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000208
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5043
- effective_condition_number: 1.5043
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000208
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5043
- effective_condition_number: 1.5043
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000206
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5043
- effective_condition_number: 1.5043
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191866696472.968506
- median_test_mae: 37809.505922
- coefficient_stability: 0.8596
- nonzero_count: 26
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state x next_raw_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191960102351.655273
- median_test_mae: 37970.527772
- coefficient_stability: 0.8228
- nonzero_count: 26
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.9137
- median_test_mse: 210075615076.809082
- median_test_mae: 46287.336200
- coefficient_stability: 0.8789
- nonzero_count: 36
- sparsity_ratio: 0.8737
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2602
- median_test_mse: 0.000003
- median_test_mae: 0.000434
- coefficient_stability: 0.9868
- nonzero_count: 3
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000204
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 49634915.6308
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000202
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 49634915.6308
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000154
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 49634915.6308
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state_history x next_raw_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9121
- median_test_mse: 196936824271.182373
- median_test_mae: 51607.076433
- coefficient_stability: 0.8180
- nonzero_count: 100
- sparsity_ratio: 0.9123
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9111
- median_test_mse: 199074116678.892792
- median_test_mae: 51820.667480
- coefficient_stability: 0.8658
- nonzero_count: 104
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.8409
- median_test_mse: 357754277164.829895
- median_test_mae: 77483.011005
- coefficient_stability: 0.8579
- nonzero_count: 132
- sparsity_ratio: 0.8842
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2602
- median_test_mse: 0.000003
- median_test_mae: 0.000434
- coefficient_stability: 0.9868
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2602
- median_test_mse: 0.000003
- median_test_mae: 0.000439
- coefficient_stability: 0.9868
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state_history x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2440
- median_test_mse: 0.000003
- median_test_mae: 0.000494
- coefficient_stability: 0.9759
- nonzero_count: 4
- sparsity_ratio: 0.9912
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2440
- median_test_mse: 0.000003
- median_test_mae: 0.000494
- coefficient_stability: 0.9759
- nonzero_count: 8
- sparsity_ratio: 0.9912
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0564
- median_test_mse: 191819518562.590179
- median_test_mae: 37676.708626
- coefficient_stability: 0.8632
- nonzero_count: 26
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0557
- median_test_mse: 191960139048.679932
- median_test_mae: 37970.496833
- coefficient_stability: 0.8351
- nonzero_count: 26
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_only x next_raw_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0494
- median_test_mse: 2311861109317.956055
- median_test_mae: 332603.175929
- coefficient_stability: 0.7250
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0494
- median_test_mse: 2311861109318.138672
- median_test_mae: 332603.175926
- coefficient_stability: 0.7250
- nonzero_count: 22
- sparsity_ratio: 0.6333
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0494
- median_test_mse: 2311867630894.252441
- median_test_mae: 332602.337257
- coefficient_stability: 0.7250
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0464
- median_test_mse: 196938318963.127106
- median_test_mae: 51607.366312
- coefficient_stability: 0.8232
- nonzero_count: 100
- sparsity_ratio: 0.9123
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0363
- median_test_mse: 199011919708.734772
- median_test_mae: 51757.096369
- coefficient_stability: 0.8732
- nonzero_count: 104
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_only x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0036
- median_test_mse: 202535657607.610291
- median_test_mae: 29500.728880
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0036
- median_test_mse: 202535657607.658020
- median_test_mae: 29500.728876
- coefficient_stability: 0.8667
- nonzero_count: 14
- sparsity_ratio: 0.7667
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0036
- median_test_mse: 202535702491.379608
- median_test_mae: 29500.129060
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0217
- median_test_mse: 207690259166.357269
- median_test_mae: 45517.444895
- coefficient_stability: 0.8842
- nonzero_count: 34
- sparsity_ratio: 0.8807
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state_history x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.7128
- median_test_mse: 353723325839.168335
- median_test_mae: 77089.501649
- coefficient_stability: 0.9000
- nonzero_count: 117
- sparsity_ratio: 0.8974
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -118.1305
- median_test_mse: 0.000990
- median_test_mae: 0.004034
- coefficient_stability: 0.9912
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -118.1305
- median_test_mse: 0.000990
- median_test_mae: 0.004034
- coefficient_stability: 0.9912
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -118.1305
- median_test_mse: 0.000990
- median_test_mae: 0.004038
- coefficient_stability: 0.9912
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state_history x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -123.8523
- median_test_mse: 0.001038
- median_test_mae: 0.004098
- coefficient_stability: 0.9956
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -123.8523
- median_test_mse: 0.001038
- median_test_mae: 0.004098
- coefficient_stability: 0.9956
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -125.9081
- median_test_mse: 0.001055
- median_test_mae: 0.004118
- coefficient_stability: 0.9693
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -125.9081
- median_test_mse: 0.001055
- median_test_mae: 0.004118
- coefficient_stability: 0.9693
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -125.9081
- median_test_mse: 0.001055
- median_test_mae: 0.004124
- coefficient_stability: 0.9693
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### commands_plus_state_history x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -125.9102
- median_test_mse: 0.001055
- median_test_mae: 0.004118
- coefficient_stability: 0.9868
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -125.9102
- median_test_mse: 0.001055
- median_test_mae: 0.004118
- coefficient_stability: 0.9868
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_only x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -27255.0797
- median_test_mse: 0.000587
- median_test_mae: 0.010409
- coefficient_stability: 0.9583
- nonzero_count: 10
- sparsity_ratio: 0.7917
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -27255.0797
- median_test_mse: 0.000587
- median_test_mae: 0.010409
- coefficient_stability: 0.9583
- nonzero_count: 5
- sparsity_ratio: 0.7917
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -27255.0798
- median_test_mse: 0.000586
- median_test_mae: 0.010403
- coefficient_stability: 0.9583
- nonzero_count: 10
- sparsity_ratio: 0.7917
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -27791.6060
- median_test_mse: 0.000587
- median_test_mae: 0.010414
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -27791.6060
- median_test_mse: 0.000587
- median_test_mae: 0.010414
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -27791.6061
- median_test_mse: 0.000586
- median_test_mae: 0.010409
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -27806.9077
- median_test_mse: 0.000587
- median_test_mae: 0.010414
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -27806.9077
- median_test_mse: 0.000587
- median_test_mae: 0.010414
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -27806.9078
- median_test_mse: 0.000586
- median_test_mae: 0.010409
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5045
- effective_condition_number: 1.5045
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000218
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 807258251.0091
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000215
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 807258251.0091
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000153
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 807258251.0091
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9176
- median_test_mse: 184416432118.035156
- median_test_mae: 43572.481731
- coefficient_stability: 0.8333
- nonzero_count: 110
- sparsity_ratio: 0.9147
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9175
- median_test_mse: 184618371425.812531
- median_test_mae: 44120.902121
- coefficient_stability: 0.8147
- nonzero_count: 106
- sparsity_ratio: 0.9178
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.8900
- median_test_mse: 246760430269.094849
- median_test_mae: 64532.285233
- coefficient_stability: 0.8477
- nonzero_count: 140
- sparsity_ratio: 0.8915
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2440
- median_test_mse: 0.000003
- median_test_mae: 0.000494
- coefficient_stability: 0.9759
- nonzero_count: 8
- sparsity_ratio: 0.9912
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2070
- median_test_mse: 0.000014
- median_test_mae: 0.001613
- coefficient_stability: 0.9671
- nonzero_count: 10
- sparsity_ratio: 0.9903
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000276
- coefficient_stability: 0.9787
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 808519143.3248
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000271
- coefficient_stability: 0.9787
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 808519143.3248
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000134
- coefficient_stability: 0.9924
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 808519143.3248
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2070
- median_test_mse: 0.000014
- median_test_mae: 0.001608
- coefficient_stability: 0.9671
- nonzero_count: 10
- sparsity_ratio: 0.9903
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2070
- median_test_mse: 0.000014
- median_test_mae: 0.001613
- coefficient_stability: 0.9671
- nonzero_count: 5
- sparsity_ratio: 0.9903
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1070
- median_test_mse: 184411585732.045258
- median_test_mae: 43524.847762
- coefficient_stability: 0.8632
- nonzero_count: 110
- sparsity_ratio: 0.9147
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1060
- median_test_mse: 184618425201.647278
- median_test_mae: 44121.223735
- coefficient_stability: 0.8368
- nonzero_count: 106
- sparsity_ratio: 0.9178
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0612
- median_test_mse: 193886516754.955078
- median_test_mae: 50627.531505
- coefficient_stability: 0.8915
- nonzero_count: 123
- sparsity_ratio: 0.9047
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -6.8014
- median_test_mse: 0.000072
- median_test_mae: 0.002500
- coefficient_stability: 0.9496
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -6.8014
- median_test_mse: 0.000072
- median_test_mae: 0.002505
- coefficient_stability: 0.9496
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -6.8014
- median_test_mse: 0.000072
- median_test_mae: 0.002505
- coefficient_stability: 0.9496
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -6.8017
- median_test_mse: 0.000072
- median_test_mae: 0.002498
- coefficient_stability: 0.9486
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -6.8018
- median_test_mse: 0.000072
- median_test_mae: 0.002504
- coefficient_stability: 0.9486
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -6.8018
- median_test_mse: 0.000072
- median_test_mae: 0.002504
- coefficient_stability: 0.9486
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 809171545.1255
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -123.8523
- median_test_mse: 0.001038
- median_test_mae: 0.004103
- coefficient_stability: 0.9956
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -125.9102
- median_test_mse: 0.001055
- median_test_mae: 0.004124
- coefficient_stability: 0.9868
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 807910943.2737
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 5
- sparsity_ratio: 0.9603
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 10
- sparsity_ratio: 0.9603
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000064
- coefficient_stability: 1.0000
- nonzero_count: 5
- sparsity_ratio: 0.9786
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### feature_mapped_linear x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000064
- coefficient_stability: 1.0000
- nonzero_count: 10
- sparsity_ratio: 0.9786
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### pooled_backend_mode_augmented x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000229
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.8095
- raw_condition_number: inf
- effective_condition_number: 173207387.3894
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000005
- median_test_mae: 0.000362
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9444
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000010
- median_test_mae: 0.001677
- coefficient_stability: 0.9615
- nonzero_count: 16
- sparsity_ratio: 0.9316
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### feature_mapped_linear x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000010
- median_test_mae: 0.001677
- coefficient_stability: 0.9615
- nonzero_count: 32
- sparsity_ratio: 0.9316
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### pooled_backend_mode_augmented x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000804
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.8095
- raw_condition_number: inf
- effective_condition_number: 173207387.3894
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000014
- median_test_mae: 0.001913
- coefficient_stability: 0.9615
- nonzero_count: 32
- sparsity_ratio: 0.9316
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000018
- median_test_mae: 0.001900
- coefficient_stability: 0.9762
- nonzero_count: 12
- sparsity_ratio: 0.9048
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000018
- median_test_mae: 0.001900
- coefficient_stability: 0.9762
- nonzero_count: 24
- sparsity_ratio: 0.9048
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000002
- median_test_mae: 0.000962
- coefficient_stability: 0.9487
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3320056793.3765
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000023
- median_test_mae: 0.002259
- coefficient_stability: 0.9762
- nonzero_count: 24
- sparsity_ratio: 0.9048
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9993
- median_test_mse: 0.000057
- median_test_mae: 0.006232
- coefficient_stability: 0.9103
- nonzero_count: 98
- sparsity_ratio: 0.3718
- raw_condition_number: inf
- effective_condition_number: 3320056793.3765
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### feature_mapped_linear x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9992
- median_test_mse: 0.000627
- median_test_mae: 0.013057
- coefficient_stability: 0.8803
- nonzero_count: 132
- sparsity_ratio: 0.4359
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### feature_mapped_linear x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9992
- median_test_mse: 0.000627
- median_test_mae: 0.013057
- coefficient_stability: 0.8803
- nonzero_count: 264
- sparsity_ratio: 0.4359
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### feature_mapped_linear x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9992
- median_test_mse: 0.000635
- median_test_mae: 0.013385
- coefficient_stability: 0.8803
- nonzero_count: 262
- sparsity_ratio: 0.4402
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### pooled_backend_mode_augmented x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9989
- median_test_mse: 0.000087
- median_test_mae: 0.007957
- coefficient_stability: 0.9524
- nonzero_count: 53
- sparsity_ratio: 0.3690
- raw_condition_number: inf
- effective_condition_number: 173207387.3894
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001072
- median_test_mae: 0.017139
- coefficient_stability: 0.9524
- nonzero_count: 72
- sparsity_ratio: 0.4286
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001072
- median_test_mae: 0.017139
- coefficient_stability: 0.9524
- nonzero_count: 144
- sparsity_ratio: 0.4286
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001080
- median_test_mae: 0.017452
- coefficient_stability: 0.9524
- nonzero_count: 144
- sparsity_ratio: 0.4286
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9810
- median_test_mse: 0.016255
- median_test_mae: 0.021591
- coefficient_stability: 0.9316
- nonzero_count: 26
- sparsity_ratio: 0.9444
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### feature_mapped_linear x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191578547683.422211
- median_test_mae: 30242.812659
- coefficient_stability: 0.8239
- nonzero_count: 115
- sparsity_ratio: 0.8034
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### feature_mapped_linear x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191598888211.764282
- median_test_mae: 30378.051928
- coefficient_stability: 0.7111
- nonzero_count: 447
- sparsity_ratio: 0.2359
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191866696472.965546
- median_test_mae: 37809.505922
- coefficient_stability: 0.8730
- nonzero_count: 26
- sparsity_ratio: 0.9175
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191960102351.655273
- median_test_mae: 37970.527772
- coefficient_stability: 0.8397
- nonzero_count: 26
- sparsity_ratio: 0.9175
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 191844932564.246796
- median_test_mae: 27586.093944
- coefficient_stability: 0.8317
- nonzero_count: 234
- sparsity_ratio: 0.2571
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 191846230918.523254
- median_test_mae: 27703.116098
- coefficient_stability: 0.8635
- nonzero_count: 71
- sparsity_ratio: 0.7746
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 191855504675.840729
- median_test_mae: 27987.427716
- coefficient_stability: 0.8254
- nonzero_count: 79
- sparsity_ratio: 0.7492
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9137
- median_test_mse: 210075615076.809082
- median_test_mae: 46287.336200
- coefficient_stability: 0.8905
- nonzero_count: 36
- sparsity_ratio: 0.8857
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### feature_mapped_linear x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3118
- median_test_mse: 0.053208
- median_test_mae: 0.076841
- coefficient_stability: 0.7372
- nonzero_count: 40
- sparsity_ratio: 0.7436
- raw_condition_number: inf
- effective_condition_number: 3320056793.3765
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2602
- median_test_mse: 0.000003
- median_test_mae: 0.000434
- coefficient_stability: 0.9881
- nonzero_count: 3
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2602
- median_test_mse: 0.000003
- median_test_mae: 0.000434
- coefficient_stability: 0.9881
- nonzero_count: 6
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### feature_mapped_linear x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0588
- median_test_mse: 191578172989.761597
- median_test_mae: 30238.773751
- coefficient_stability: 0.8496
- nonzero_count: 78
- sparsity_ratio: 0.8667
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### feature_mapped_linear x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0587
- median_test_mse: 191596873991.099884
- median_test_mae: 30368.926613
- coefficient_stability: 0.8581
- nonzero_count: 236
- sparsity_ratio: 0.5966
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### pooled_backend_mode_augmented x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0575
- median_test_mse: 191844909201.399597
- median_test_mae: 27584.805012
- coefficient_stability: 0.8825
- nonzero_count: 140
- sparsity_ratio: 0.5556
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0575
- median_test_mse: 191845817510.497955
- median_test_mae: 27676.555530
- coefficient_stability: 0.8762
- nonzero_count: 43
- sparsity_ratio: 0.8635
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0574
- median_test_mse: 191855504675.844788
- median_test_mae: 27987.427717
- coefficient_stability: 0.8254
- nonzero_count: 62
- sparsity_ratio: 0.8032
- raw_condition_number: inf
- effective_condition_number: 178692930.1839
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -329.9390
- median_test_mse: 800354933338512.875000
- median_test_mae: 4074515.465732
- coefficient_stability: 0.6513
- nonzero_count: 182
- sparsity_ratio: 0.6889
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

### pooled_backend_mode_augmented x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000204
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 49634915.6308
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000202
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 49634915.6308
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000154
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 49634915.6308
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### feature_mapped_linear x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 192228404449.818268
- median_test_mae: 40043.790731
- coefficient_stability: 0.8256
- nonzero_count: 56
- sparsity_ratio: 0.9043
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9141
- median_test_mse: 208925249856.451782
- median_test_mae: 47088.525853
- coefficient_stability: 0.8222
- nonzero_count: 82
- sparsity_ratio: 0.8598
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2602
- median_test_mse: 0.000003
- median_test_mae: 0.000439
- coefficient_stability: 0.9881
- nonzero_count: 6
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### feature_mapped_linear x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2570
- median_test_mse: 0.000003
- median_test_mae: 0.000556
- coefficient_stability: 0.9701
- nonzero_count: 4
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2570
- median_test_mse: 0.000003
- median_test_mae: 0.000556
- coefficient_stability: 0.9701
- nonzero_count: 8
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0564
- median_test_mse: 191819518609.650818
- median_test_mae: 37676.708682
- coefficient_stability: 0.8762
- nonzero_count: 26
- sparsity_ratio: 0.9175
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0557
- median_test_mse: 191960139048.679932
- median_test_mae: 37970.496833
- coefficient_stability: 0.8508
- nonzero_count: 26
- sparsity_ratio: 0.9175
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### feature_mapped_linear x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0549
- median_test_mse: 192124507893.984558
- median_test_mae: 39889.009941
- coefficient_stability: 0.8419
- nonzero_count: 56
- sparsity_ratio: 0.9043
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.0217
- median_test_mse: 207690259166.357269
- median_test_mae: 45517.444895
- coefficient_stability: 0.8952
- nonzero_count: 34
- sparsity_ratio: 0.8921
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### feature_mapped_linear x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.0357
- median_test_mse: 210528329231.857483
- median_test_mae: 47687.562702
- coefficient_stability: 0.8778
- nonzero_count: 76
- sparsity_ratio: 0.8701
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.8851
- median_test_mse: 4573786279475.375000
- median_test_mae: 260135.968427
- coefficient_stability: 0.7436
- nonzero_count: 56
- sparsity_ratio: 0.9043
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -21.5006
- median_test_mse: 4573786530841.498047
- median_test_mae: 260135.960206
- coefficient_stability: 0.7607
- nonzero_count: 56
- sparsity_ratio: 0.9043
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -118.1305
- median_test_mse: 0.000990
- median_test_mae: 0.004034
- coefficient_stability: 0.9921
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -118.1305
- median_test_mse: 0.000990
- median_test_mae: 0.004034
- coefficient_stability: 0.9921
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -118.1305
- median_test_mse: 0.000990
- median_test_mae: 0.004038
- coefficient_stability: 0.9921
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -125.9081
- median_test_mse: 0.001055
- median_test_mae: 0.004118
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -125.9081
- median_test_mse: 0.001055
- median_test_mae: 0.004118
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -125.9081
- median_test_mse: 0.001055
- median_test_mae: 0.004124
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51315079.0912
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch_rate, position_y, position_z, velocity_x, yaw, yaw_rate

### feature_mapped_linear x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -154.1334
- median_test_mse: 0.001290
- median_test_mae: 0.004694
- coefficient_stability: 0.9637
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -154.1334
- median_test_mse: 0.001290
- median_test_mae: 0.004694
- coefficient_stability: 0.9637
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -160.2747
- median_test_mse: 0.001340
- median_test_mae: 0.004585
- coefficient_stability: 0.9573
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -160.2747
- median_test_mse: 0.001340
- median_test_mae: 0.004585
- coefficient_stability: 0.9573
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000001
- median_test_mae: 0.000380
- coefficient_stability: 0.9744
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 17371959139.7548
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000252
- coefficient_stability: 0.9808
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 17371959139.7548
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000153
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 17371959139.7548
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2570
- median_test_mse: 0.000003
- median_test_mae: 0.000558
- coefficient_stability: 0.9701
- nonzero_count: 8
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -154.1334
- median_test_mse: 0.001290
- median_test_mae: 0.004690
- coefficient_stability: 0.9637
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -160.2747
- median_test_mse: 0.001340
- median_test_mae: 0.004590
- coefficient_stability: 0.9573
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 18915762013.3534
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, yaw, yaw_rate

### feature_mapped_linear x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -3929.6034
- median_test_mse: 800354933347790.375000
- median_test_mae: 4074515.466700
- coefficient_stability: 0.6513
- nonzero_count: 165
- sparsity_ratio: 0.7179
- raw_condition_number: inf
- effective_condition_number: 3318862384.7428
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch, sq__roll

## Skipped
- 无。