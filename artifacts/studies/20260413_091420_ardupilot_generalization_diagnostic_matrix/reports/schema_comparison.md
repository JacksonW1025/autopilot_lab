# Schema Comparison: ardupilot_generalization_diagnostic_matrix

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
- effective_condition_number: 898540353.8492
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
- effective_condition_number: 898540353.8492
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
- effective_condition_number: 17205387.9426
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
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### full_augmented x selected_state_subset | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9961
- nonzero_count: 16
- sparsity_ratio: 0.9690
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9961
- nonzero_count: 32
- sparsity_ratio: 0.9690
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000207
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 898540353.8492
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000207
- coefficient_stability: 1.0000
- nonzero_count: 32
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 898540353.8492
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000198
- coefficient_stability: 0.9573
- nonzero_count: 40
- sparsity_ratio: 0.8780
- raw_condition_number: inf
- effective_condition_number: 950164190.1459
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000004
- median_test_mae: 0.000706
- coefficient_stability: 0.9912
- nonzero_count: 6
- sparsity_ratio: 0.9474
- raw_condition_number: inf
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000004
- median_test_mae: 0.000706
- coefficient_stability: 0.9912
- nonzero_count: 12
- sparsity_ratio: 0.9474
- raw_condition_number: inf
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x window_summary_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000005
- median_test_mae: 0.000581
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9386
- raw_condition_number: inf
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state_history x window_summary_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000006
- median_test_mae: 0.000588
- coefficient_stability: 1.0000
- nonzero_count: 48
- sparsity_ratio: 0.9474
- raw_condition_number: inf
- effective_condition_number: 898540353.8492
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000006
- median_test_mae: 0.000788
- coefficient_stability: 1.0000
- nonzero_count: 32
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 898540353.8492
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000006
- median_test_mae: 0.000903
- coefficient_stability: 0.9787
- nonzero_count: 22
- sparsity_ratio: 0.9574
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000006
- median_test_mae: 0.000903
- coefficient_stability: 0.9787
- nonzero_count: 44
- sparsity_ratio: 0.9574
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x window_summary_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000010
- median_test_mae: 0.001272
- coefficient_stability: 0.9912
- nonzero_count: 12
- sparsity_ratio: 0.9474
- raw_condition_number: inf
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### full_augmented x window_summary_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000012
- median_test_mae: 0.001518
- coefficient_stability: 0.9758
- nonzero_count: 44
- sparsity_ratio: 0.9574
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000027
- median_test_mae: 0.001316
- coefficient_stability: 0.9700
- nonzero_count: 60
- sparsity_ratio: 0.9419
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000004
- median_test_mae: 0.001489
- coefficient_stability: 0.9512
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 950164190.1459
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9999
- median_test_mse: 0.000005
- median_test_mae: 0.001679
- coefficient_stability: 1.0000
- nonzero_count: 8
- sparsity_ratio: 0.8947
- raw_condition_number: inf
- effective_condition_number: 16916596.3081
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state_history x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9999
- median_test_mse: 0.000005
- median_test_mae: 0.001722
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 887225679.3029
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9999
- median_test_mse: 0.000005
- median_test_mae: 0.001751
- coefficient_stability: 1.0000
- nonzero_count: 32
- sparsity_ratio: 0.8947
- raw_condition_number: inf
- effective_condition_number: 887225679.3029
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9999
- median_test_mse: 0.000005
- median_test_mae: 0.001756
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.7895
- raw_condition_number: inf
- effective_condition_number: 16916596.3081
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### full_augmented x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9992
- median_test_mse: 0.000067
- median_test_mae: 0.004805
- coefficient_stability: 0.9634
- nonzero_count: 165
- sparsity_ratio: 0.4970
- raw_condition_number: inf
- effective_condition_number: 950164190.1459
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9992
- median_test_mse: 0.000072
- median_test_mae: 0.005010
- coefficient_stability: 1.0000
- nonzero_count: 166
- sparsity_ratio: 0.4539
- raw_condition_number: inf
- effective_condition_number: 887225679.3029
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9990
- median_test_mse: 0.000866
- median_test_mae: 0.010325
- coefficient_stability: 0.9759
- nonzero_count: 249
- sparsity_ratio: 0.4539
- raw_condition_number: inf
- effective_condition_number: 898540353.8492
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9990
- median_test_mse: 0.000866
- median_test_mae: 0.010325
- coefficient_stability: 0.9759
- nonzero_count: 498
- sparsity_ratio: 0.4539
- raw_condition_number: inf
- effective_condition_number: 898540353.8492
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9990
- median_test_mse: 0.000872
- median_test_mae: 0.010786
- coefficient_stability: 0.9759
- nonzero_count: 503
- sparsity_ratio: 0.4485
- raw_condition_number: inf
- effective_condition_number: 898540353.8492
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9989
- median_test_mse: 0.000970
- median_test_mae: 0.011668
- coefficient_stability: 0.9399
- nonzero_count: 264
- sparsity_ratio: 0.4884
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9989
- median_test_mse: 0.000970
- median_test_mae: 0.011668
- coefficient_stability: 0.9399
- nonzero_count: 528
- sparsity_ratio: 0.4884
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9989
- median_test_mse: 0.000976
- median_test_mae: 0.012150
- coefficient_stability: 0.9390
- nonzero_count: 531
- sparsity_ratio: 0.4855
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9985
- median_test_mse: 0.000133
- median_test_mae: 0.007278
- coefficient_stability: 0.9474
- nonzero_count: 57
- sparsity_ratio: 0.2500
- raw_condition_number: inf
- effective_condition_number: 16916596.3081
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9982
- median_test_mse: 0.001588
- median_test_mae: 0.015341
- coefficient_stability: 0.9474
- nonzero_count: 84
- sparsity_ratio: 0.2632
- raw_condition_number: inf
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9982
- median_test_mse: 0.001588
- median_test_mae: 0.015341
- coefficient_stability: 0.9474
- nonzero_count: 168
- sparsity_ratio: 0.2632
- raw_condition_number: inf
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x window_summary_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9982
- median_test_mse: 0.001594
- median_test_mae: 0.015792
- coefficient_stability: 0.9430
- nonzero_count: 169
- sparsity_ratio: 0.2588
- raw_condition_number: inf
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_only x actuator_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9981
- median_test_mse: 0.000163
- median_test_mae: 0.007019
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.7500
- raw_condition_number: 1.0364
- effective_condition_number: 1.0364
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9981
- median_test_mse: 0.000163
- median_test_mae: 0.007004
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.0000
- raw_condition_number: 1.0364
- effective_condition_number: 1.0364
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9981
- median_test_mse: 0.000163
- median_test_mae: 0.007000
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.7500
- raw_condition_number: 1.0364
- effective_condition_number: 1.0364
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002557
- median_test_mae: 0.024213
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.8333
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002557
- median_test_mae: 0.024213
- coefficient_stability: 1.0000
- nonzero_count: 8
- sparsity_ratio: 0.8333
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002558
- median_test_mae: 0.024186
- coefficient_stability: 1.0000
- nonzero_count: 24
- sparsity_ratio: 0.0000
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002558
- median_test_mae: 0.024186
- coefficient_stability: 1.0000
- nonzero_count: 48
- sparsity_ratio: 0.0000
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002558
- median_test_mae: 0.024186
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.8333
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002558
- median_test_mae: 0.024186
- coefficient_stability: 1.0000
- nonzero_count: 8
- sparsity_ratio: 0.8333
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002556
- median_test_mae: 0.024158
- coefficient_stability: 1.0000
- nonzero_count: 8
- sparsity_ratio: 0.8333
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002557
- median_test_mae: 0.024131
- coefficient_stability: 1.0000
- nonzero_count: 48
- sparsity_ratio: 0.0000
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002557
- median_test_mae: 0.024132
- coefficient_stability: 1.0000
- nonzero_count: 8
- sparsity_ratio: 0.8333
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191885638118.472839
- median_test_mae: 30136.893211
- coefficient_stability: 0.8596
- nonzero_count: 73
- sparsity_ratio: 0.7439
- raw_condition_number: inf
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191889497106.624054
- median_test_mae: 30151.699718
- coefficient_stability: 0.8737
- nonzero_count: 63
- sparsity_ratio: 0.7789
- raw_condition_number: inf
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191903510821.052002
- median_test_mae: 30130.604490
- coefficient_stability: 0.8316
- nonzero_count: 248
- sparsity_ratio: 0.1298
- raw_condition_number: inf
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state_history x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9133
- median_test_mse: 194065349822.368652
- median_test_mae: 32749.819429
- coefficient_stability: 0.8667
- nonzero_count: 267
- sparsity_ratio: 0.7658
- raw_condition_number: inf
- effective_condition_number: 898540353.8492
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9133
- median_test_mse: 194081133195.735657
- median_test_mae: 33032.095052
- coefficient_stability: 0.8171
- nonzero_count: 314
- sparsity_ratio: 0.7566
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9132
- median_test_mse: 194224806219.112732
- median_test_mae: 32303.405615
- coefficient_stability: 0.8496
- nonzero_count: 238
- sparsity_ratio: 0.8155
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9132
- median_test_mse: 194227067163.362976
- median_test_mae: 32317.815460
- coefficient_stability: 0.8789
- nonzero_count: 208
- sparsity_ratio: 0.8175
- raw_condition_number: inf
- effective_condition_number: 898540353.8492
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9130
- median_test_mse: 194670526174.083313
- median_test_mae: 31907.350081
- coefficient_stability: 0.8295
- nonzero_count: 922
- sparsity_ratio: 0.2853
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9130
- median_test_mse: 194673458497.080078
- median_test_mae: 31942.252056
- coefficient_stability: 0.8570
- nonzero_count: 858
- sparsity_ratio: 0.2474
- raw_condition_number: inf
- effective_condition_number: 898540353.8492
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0635
- median_test_mse: 194065349821.325226
- median_test_mae: 32749.819426
- coefficient_stability: 0.8667
- nonzero_count: 243
- sparsity_ratio: 0.7868
- raw_condition_number: inf
- effective_condition_number: 898540353.8492
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0635
- median_test_mse: 194081133194.773590
- median_test_mae: 33032.095054
- coefficient_stability: 0.8194
- nonzero_count: 290
- sparsity_ratio: 0.7752
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0628
- median_test_mse: 194224004157.650818
- median_test_mae: 32289.061216
- coefficient_stability: 0.8620
- nonzero_count: 195
- sparsity_ratio: 0.8488
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0628
- median_test_mse: 194226262528.801392
- median_test_mae: 32303.820836
- coefficient_stability: 0.8798
- nonzero_count: 177
- sparsity_ratio: 0.8447
- raw_condition_number: inf
- effective_condition_number: 898540353.8492
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0606
- median_test_mse: 194669430771.376617
- median_test_mae: 31905.079633
- coefficient_stability: 0.8713
- nonzero_count: 521
- sparsity_ratio: 0.5961
- raw_condition_number: inf
- effective_condition_number: 1060548730.8719
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0606
- median_test_mse: 194672360962.462006
- median_test_mae: 31939.462830
- coefficient_stability: 0.8807
- nonzero_count: 493
- sparsity_ratio: 0.5675
- raw_condition_number: inf
- effective_condition_number: 898540353.8492
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0592
- median_test_mse: 191885638118.473572
- median_test_mae: 30136.893211
- coefficient_stability: 0.8596
- nonzero_count: 56
- sparsity_ratio: 0.8035
- raw_condition_number: inf
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0592
- median_test_mse: 191889885822.496948
- median_test_mae: 30138.038079
- coefficient_stability: 0.8807
- nonzero_count: 44
- sparsity_ratio: 0.8456
- raw_condition_number: inf
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0592
- median_test_mse: 191902412875.098938
- median_test_mae: 30125.097007
- coefficient_stability: 0.8737
- nonzero_count: 149
- sparsity_ratio: 0.4772
- raw_condition_number: inf
- effective_condition_number: 17205387.9426
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_only x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0005
- median_test_mse: 203859466094.927032
- median_test_mae: 29395.334879
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0005
- median_test_mse: 203859508308.942993
- median_test_mae: 29395.487060
- coefficient_stability: 0.8667
- nonzero_count: 32
- sparsity_ratio: 0.4667
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0005
- median_test_mse: 203859508309.078369
- median_test_mae: 29395.487062
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0047
- median_test_mse: 2443036081739.262695
- median_test_mae: 342818.147850
- coefficient_stability: 0.7000
- nonzero_count: 19
- sparsity_ratio: 0.6833
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0047
- median_test_mse: 2443037882314.834961
- median_test_mae: 342818.145337
- coefficient_stability: 0.7000
- nonzero_count: 60
- sparsity_ratio: 0.0000
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0047
- median_test_mse: 2443037882315.605957
- median_test_mae: 342818.145339
- coefficient_stability: 0.7000
- nonzero_count: 19
- sparsity_ratio: 0.6833
- raw_condition_number: 1.0366
- effective_condition_number: 1.0366
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000195
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000195
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000194
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9566
- median_test_mse: 0.000000
- median_test_mae: 0.000083
- coefficient_stability: 0.9211
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x future_state_horizon | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9566
- median_test_mse: 0.000000
- median_test_mae: 0.000083
- coefficient_stability: 0.9211
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000202
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3684488.5581
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000201
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3684488.5581
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000177
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3684488.5581
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state_history x selected_state_subset | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9566
- median_test_mse: 0.000000
- median_test_mae: 0.000083
- coefficient_stability: 0.9298
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9566
- median_test_mse: 0.000000
- median_test_mae: 0.000083
- coefficient_stability: 0.9298
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x window_summary_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9566
- median_test_mse: 0.000000
- median_test_mae: 0.000083
- coefficient_stability: 0.9211
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state_history x selected_state_subset | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9472
- median_test_mse: 0.000000
- median_test_mae: 0.000105
- coefficient_stability: 0.9298
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9472
- median_test_mse: 0.000000
- median_test_mae: 0.000105
- coefficient_stability: 0.9298
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x selected_state_subset | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9410
- median_test_mse: 0.000000
- median_test_mae: 0.000119
- coefficient_stability: 0.9211
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x future_state_horizon | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9410
- median_test_mse: 0.000000
- median_test_mae: 0.000119
- coefficient_stability: 0.9211
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x window_summary_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9410
- median_test_mse: 0.000000
- median_test_mae: 0.000119
- coefficient_stability: 0.9211
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191142568506.395020
- median_test_mae: 36665.684594
- coefficient_stability: 0.8632
- nonzero_count: 36
- sparsity_ratio: 0.8737
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 191208309876.509186
- median_test_mae: 36581.865012
- coefficient_stability: 0.8211
- nonzero_count: 26
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x next_raw_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9193
- median_test_mse: 195442359010.977722
- median_test_mae: 39458.144690
- coefficient_stability: 0.8035
- nonzero_count: 26
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state_history x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.9142
- median_test_mse: 191059735491.286011
- median_test_mae: 39451.452302
- coefficient_stability: 0.8658
- nonzero_count: 125
- sparsity_ratio: 0.8904
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9096
- median_test_mse: 201617864540.639984
- median_test_mae: 46046.284642
- coefficient_stability: 0.8386
- nonzero_count: 104
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.8774
- median_test_mse: 274170360762.257935
- median_test_mae: 58809.975020
- coefficient_stability: 0.8224
- nonzero_count: 104
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.8601
- median_test_mse: 0.000001
- median_test_mae: 0.000189
- coefficient_stability: 0.9682
- nonzero_count: 5
- sparsity_ratio: 0.9890
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.8601
- median_test_mse: 0.000001
- median_test_mae: 0.000189
- coefficient_stability: 0.9682
- nonzero_count: 10
- sparsity_ratio: 0.9890
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x selected_state_subset | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.8601
- median_test_mse: 0.000001
- median_test_mae: 0.000172
- coefficient_stability: 0.9737
- nonzero_count: 3
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x future_state_horizon | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.8601
- median_test_mse: 0.000001
- median_test_mae: 0.000172
- coefficient_stability: 0.9737
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x window_summary_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.8601
- median_test_mse: 0.000001
- median_test_mae: 0.000172
- coefficient_stability: 0.9737
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state_history x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0785
- median_test_mse: 191059493385.219269
- median_test_mae: 39449.954626
- coefficient_stability: 0.8943
- nonzero_count: 113
- sparsity_ratio: 0.9009
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0633
- median_test_mse: 191142497449.701385
- median_test_mae: 36664.966649
- coefficient_stability: 0.8825
- nonzero_count: 32
- sparsity_ratio: 0.8877
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0630
- median_test_mse: 191210411796.952606
- median_test_mae: 36540.308206
- coefficient_stability: 0.8632
- nonzero_count: 26
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0425
- median_test_mse: 195442359010.938599
- median_test_mae: 39458.144643
- coefficient_stability: 0.8439
- nonzero_count: 26
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state_history x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0280
- median_test_mse: 201623227225.337128
- median_test_mae: 46020.331395
- coefficient_stability: 0.8737
- nonzero_count: 104
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_only x next_raw_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0024
- median_test_mse: 2427745819303.976074
- median_test_mae: 340595.606567
- coefficient_stability: 0.7417
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0024
- median_test_mse: 2427753362527.651367
- median_test_mae: 340595.581428
- coefficient_stability: 0.7417
- nonzero_count: 30
- sparsity_ratio: 0.5000
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0024
- median_test_mse: 2427753362531.277832
- median_test_mae: 340595.581427
- coefficient_stability: 0.7417
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0052
- median_test_mse: 205139633131.863678
- median_test_mae: 31665.527568
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0052
- median_test_mse: 205140344726.965759
- median_test_mae: 31666.595658
- coefficient_stability: 0.8667
- nonzero_count: 16
- sparsity_ratio: 0.7333
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0052
- median_test_mse: 205140344727.626343
- median_test_mae: 31666.595660
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.3184
- median_test_mse: 274170360758.015320
- median_test_mae: 58809.974972
- coefficient_stability: 0.8575
- nonzero_count: 104
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_only x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -1.1029
- median_test_mse: 0.000603
- median_test_mae: 0.013544
- coefficient_stability: 0.9792
- nonzero_count: 11
- sparsity_ratio: 0.5417
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -1.1029
- median_test_mse: 0.000603
- median_test_mae: 0.013544
- coefficient_stability: 0.9792
- nonzero_count: 22
- sparsity_ratio: 0.5417
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -1.1029
- median_test_mse: 0.000603
- median_test_mae: 0.013544
- coefficient_stability: 0.9792
- nonzero_count: 22
- sparsity_ratio: 0.5417
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -1.1031
- median_test_mse: 0.000603
- median_test_mae: 0.013545
- coefficient_stability: 0.9792
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -1.1031
- median_test_mse: 0.000603
- median_test_mae: 0.013545
- coefficient_stability: 0.9792
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -1.1031
- median_test_mse: 0.000603
- median_test_mae: 0.013545
- coefficient_stability: 0.9792
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -1.1031
- median_test_mse: 0.000603
- median_test_mae: 0.013545
- coefficient_stability: 0.9792
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -1.1031
- median_test_mse: 0.000603
- median_test_mae: 0.013545
- coefficient_stability: 0.9792
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -1.1031
- median_test_mse: 0.000603
- median_test_mae: 0.013545
- coefficient_stability: 0.9792
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0184
- effective_condition_number: 1.0184
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000202
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 254495017.3744
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000201
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 254495017.3744
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000178
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 254495017.3744
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9566
- median_test_mse: 0.000000
- median_test_mae: 0.000083
- coefficient_stability: 0.9298
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9472
- median_test_mse: 0.000000
- median_test_mae: 0.000105
- coefficient_stability: 0.9298
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9365
- median_test_mse: 0.000000
- median_test_mae: 0.000112
- coefficient_stability: 0.9225
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9365
- median_test_mse: 0.000000
- median_test_mae: 0.000112
- coefficient_stability: 0.9225
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9365
- median_test_mse: 0.000000
- median_test_mae: 0.000164
- coefficient_stability: 0.9079
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9365
- median_test_mse: 0.000000
- median_test_mae: 0.000164
- coefficient_stability: 0.9079
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.9137
- median_test_mse: 192228374370.426208
- median_test_mae: 43550.289668
- coefficient_stability: 0.8589
- nonzero_count: 132
- sparsity_ratio: 0.8977
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9125
- median_test_mse: 195019707961.991699
- median_test_mae: 48071.280587
- coefficient_stability: 0.8128
- nonzero_count: 110
- sparsity_ratio: 0.9147
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.8602
- median_test_mse: 0.000001
- median_test_mae: 0.000198
- coefficient_stability: 0.9680
- nonzero_count: 5
- sparsity_ratio: 0.9903
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000208
- coefficient_stability: 0.9802
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 254638718.7698
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000211
- coefficient_stability: 0.9802
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 254638718.7698
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000137
- coefficient_stability: 0.9924
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 254638718.7698
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9365
- median_test_mse: 0.000000
- median_test_mae: 0.000112
- coefficient_stability: 0.9225
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9365
- median_test_mse: 0.000000
- median_test_mae: 0.000164
- coefficient_stability: 0.9079
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.8602
- median_test_mse: 0.000001
- median_test_mae: 0.000198
- coefficient_stability: 0.9680
- nonzero_count: 10
- sparsity_ratio: 0.9903
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.8602
- median_test_mse: 0.000001
- median_test_mae: 0.000198
- coefficient_stability: 0.9680
- nonzero_count: 10
- sparsity_ratio: 0.9903
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.8601
- median_test_mse: 0.000001
- median_test_mae: 0.000189
- coefficient_stability: 0.9682
- nonzero_count: 10
- sparsity_ratio: 0.9890
- raw_condition_number: inf
- effective_condition_number: 256798102.0075
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0728
- median_test_mse: 192222147617.907501
- median_test_mae: 43535.952509
- coefficient_stability: 0.8837
- nonzero_count: 119
- sparsity_ratio: 0.9078
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0595
- median_test_mse: 194966568909.887512
- median_test_mae: 48021.627805
- coefficient_stability: 0.8578
- nonzero_count: 110
- sparsity_ratio: 0.9147
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -89874844650.0445
- median_test_mse: 200073518434877414834176.000000
- median_test_mae: 30732919642.777916
- coefficient_stability: 0.8078
- nonzero_count: 110
- sparsity_ratio: 0.9147
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -969805924657.2860
- median_test_mse: 200068830864237091880960.000000
- median_test_mae: 30732671849.898582
- coefficient_stability: 0.8465
- nonzero_count: 110
- sparsity_ratio: 0.9147
- raw_condition_number: inf
- effective_condition_number: 256980471.9657
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

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
- effective_condition_number: 18347083.4023
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
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000004
- coefficient_stability: 0.9872
- nonzero_count: 5
- sparsity_ratio: 0.9786
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### feature_mapped_linear x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000004
- coefficient_stability: 0.9872
- nonzero_count: 10
- sparsity_ratio: 0.9786
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### pooled_backend_mode_augmented x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000195
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.8095
- raw_condition_number: inf
- effective_condition_number: 18038190.0060
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000227
- coefficient_stability: 0.9380
- nonzero_count: 29
- sparsity_ratio: 0.9380
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### feature_mapped_linear x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000396
- coefficient_stability: 0.8718
- nonzero_count: 36
- sparsity_ratio: 0.7692
- raw_condition_number: inf
- effective_condition_number: 24027715.9391
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### pooled_backend_mode_augmented x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000005
- median_test_mae: 0.000664
- coefficient_stability: 0.9960
- nonzero_count: 16
- sparsity_ratio: 0.9365
- raw_condition_number: inf
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000740
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.8095
- raw_condition_number: inf
- effective_condition_number: 18038190.0060
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000011
- median_test_mae: 0.001245
- coefficient_stability: 0.9921
- nonzero_count: 7
- sparsity_ratio: 0.9444
- raw_condition_number: inf
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000011
- median_test_mae: 0.001245
- coefficient_stability: 0.9921
- nonzero_count: 14
- sparsity_ratio: 0.9444
- raw_condition_number: inf
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000786
- coefficient_stability: 0.9744
- nonzero_count: 12
- sparsity_ratio: 0.9231
- raw_condition_number: inf
- effective_condition_number: 24027715.9391
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000016
- median_test_mae: 0.001810
- coefficient_stability: 0.9921
- nonzero_count: 14
- sparsity_ratio: 0.9444
- raw_condition_number: inf
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000018
- median_test_mae: 0.001808
- coefficient_stability: 0.9487
- nonzero_count: 12
- sparsity_ratio: 0.9487
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### feature_mapped_linear x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000018
- median_test_mae: 0.001808
- coefficient_stability: 0.9487
- nonzero_count: 24
- sparsity_ratio: 0.9487
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### feature_mapped_linear x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000021
- median_test_mae: 0.002224
- coefficient_stability: 0.9466
- nonzero_count: 25
- sparsity_ratio: 0.9466
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### feature_mapped_linear x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9988
- median_test_mse: 0.000106
- median_test_mae: 0.006717
- coefficient_stability: 0.8974
- nonzero_count: 122
- sparsity_ratio: 0.2179
- raw_condition_number: inf
- effective_condition_number: 24027715.9391
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### feature_mapped_linear x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9987
- median_test_mse: 0.001160
- median_test_mae: 0.013807
- coefficient_stability: 0.8590
- nonzero_count: 155
- sparsity_ratio: 0.3376
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### feature_mapped_linear x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9987
- median_test_mse: 0.001160
- median_test_mae: 0.013807
- coefficient_stability: 0.8590
- nonzero_count: 310
- sparsity_ratio: 0.3376
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### feature_mapped_linear x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001165
- median_test_mae: 0.014176
- coefficient_stability: 0.8590
- nonzero_count: 314
- sparsity_ratio: 0.3291
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### pooled_backend_mode_augmented x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9985
- median_test_mse: 0.000133
- median_test_mae: 0.007268
- coefficient_stability: 0.9524
- nonzero_count: 61
- sparsity_ratio: 0.2738
- raw_condition_number: inf
- effective_condition_number: 18038190.0060
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9981
- median_test_mse: 0.001600
- median_test_mae: 0.015385
- coefficient_stability: 0.9524
- nonzero_count: 87
- sparsity_ratio: 0.3095
- raw_condition_number: inf
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9981
- median_test_mse: 0.001600
- median_test_mae: 0.015385
- coefficient_stability: 0.9524
- nonzero_count: 174
- sparsity_ratio: 0.3095
- raw_condition_number: inf
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9981
- median_test_mse: 0.001605
- median_test_mae: 0.015835
- coefficient_stability: 0.9484
- nonzero_count: 176
- sparsity_ratio: 0.3016
- raw_condition_number: inf
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9566
- median_test_mse: 0.000000
- median_test_mae: 0.000083
- coefficient_stability: 0.9286
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9566
- median_test_mse: 0.000000
- median_test_mae: 0.000083
- coefficient_stability: 0.9286
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191838818601.037354
- median_test_mae: 31448.428077
- coefficient_stability: 0.7179
- nonzero_count: 466
- sparsity_ratio: 0.2034
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### pooled_backend_mode_augmented x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191880866037.262695
- median_test_mae: 30143.796284
- coefficient_stability: 0.8603
- nonzero_count: 77
- sparsity_ratio: 0.7556
- raw_condition_number: inf
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191882547294.521301
- median_test_mae: 31698.499831
- coefficient_stability: 0.8017
- nonzero_count: 113
- sparsity_ratio: 0.8068
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191887674533.306458
- median_test_mae: 30152.544325
- coefficient_stability: 0.8730
- nonzero_count: 69
- sparsity_ratio: 0.7810
- raw_condition_number: inf
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191903337605.483521
- median_test_mae: 30130.229199
- coefficient_stability: 0.8413
- nonzero_count: 259
- sparsity_ratio: 0.1778
- raw_condition_number: inf
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191958861816.692963
- median_test_mae: 31982.504041
- coefficient_stability: 0.7709
- nonzero_count: 151
- sparsity_ratio: 0.7419
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### feature_mapped_linear x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0595
- median_test_mse: 191839448408.011597
- median_test_mae: 31458.563769
- coefficient_stability: 0.8513
- nonzero_count: 241
- sparsity_ratio: 0.5880
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### pooled_backend_mode_augmented x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0593
- median_test_mse: 191880866037.263123
- median_test_mae: 30143.796284
- coefficient_stability: 0.8603
- nonzero_count: 60
- sparsity_ratio: 0.8095
- raw_condition_number: inf
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0592
- median_test_mse: 191883994183.489349
- median_test_mae: 31683.441124
- coefficient_stability: 0.8308
- nonzero_count: 84
- sparsity_ratio: 0.8564
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### pooled_backend_mode_augmented x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0592
- median_test_mse: 191888061763.556458
- median_test_mae: 30139.011686
- coefficient_stability: 0.8794
- nonzero_count: 48
- sparsity_ratio: 0.8476
- raw_condition_number: inf
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0592
- median_test_mse: 191902246919.151672
- median_test_mae: 30124.780099
- coefficient_stability: 0.8794
- nonzero_count: 155
- sparsity_ratio: 0.5079
- raw_condition_number: inf
- effective_condition_number: 18347083.4023
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0589
- median_test_mse: 191958861816.708496
- median_test_mae: 31982.504039
- coefficient_stability: 0.7761
- nonzero_count: 134
- sparsity_ratio: 0.7709
- raw_condition_number: inf
- effective_condition_number: 24424243.3585
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__pitch, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__pitch

### pooled_backend_mode_augmented x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000202
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3684488.5581
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000201
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3684488.5581
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000177
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3684488.5581
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9566
- median_test_mse: 0.000000
- median_test_mae: 0.000083
- coefficient_stability: 0.9286
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9535
- median_test_mse: 0.000000
- median_test_mae: 0.000106
- coefficient_stability: 0.9359
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9535
- median_test_mse: 0.000000
- median_test_mae: 0.000106
- coefficient_stability: 0.9359
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9410
- median_test_mse: 0.000000
- median_test_mae: 0.000119
- coefficient_stability: 0.9286
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9410
- median_test_mse: 0.000000
- median_test_mae: 0.000119
- coefficient_stability: 0.9286
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9410
- median_test_mse: 0.000000
- median_test_mae: 0.000119
- coefficient_stability: 0.9286
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9368
- median_test_mse: 0.000002
- median_test_mae: 0.000399
- coefficient_stability: 0.9231
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9368
- median_test_mse: 0.000002
- median_test_mae: 0.000399
- coefficient_stability: 0.9231
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191142568506.395020
- median_test_mae: 36665.684594
- coefficient_stability: 0.8762
- nonzero_count: 36
- sparsity_ratio: 0.8857
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 191208309876.510956
- median_test_mae: 36581.865012
- coefficient_stability: 0.8381
- nonzero_count: 26
- sparsity_ratio: 0.9175
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9200
- median_test_mse: 193654807142.634491
- median_test_mae: 39732.893741
- coefficient_stability: 0.8085
- nonzero_count: 56
- sparsity_ratio: 0.9043
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9200
- median_test_mse: 193857768203.067688
- median_test_mae: 39957.330232
- coefficient_stability: 0.8299
- nonzero_count: 74
- sparsity_ratio: 0.8735
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9194
- median_test_mse: 195204338463.593811
- median_test_mae: 41399.711817
- coefficient_stability: 0.7735
- nonzero_count: 56
- sparsity_ratio: 0.9043
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9193
- median_test_mse: 195442359010.977722
- median_test_mae: 39458.144690
- coefficient_stability: 0.8222
- nonzero_count: 26
- sparsity_ratio: 0.9175
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.8601
- median_test_mse: 0.000001
- median_test_mae: 0.000172
- coefficient_stability: 0.9762
- nonzero_count: 3
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.8601
- median_test_mse: 0.000001
- median_test_mae: 0.000172
- coefficient_stability: 0.9762
- nonzero_count: 6
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.8601
- median_test_mse: 0.000001
- median_test_mae: 0.000172
- coefficient_stability: 0.9762
- nonzero_count: 6
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.8541
- median_test_mse: 0.000005
- median_test_mae: 0.000608
- coefficient_stability: 0.9679
- nonzero_count: 4
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.8541
- median_test_mse: 0.000005
- median_test_mae: 0.000608
- coefficient_stability: 0.9679
- nonzero_count: 8
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0633
- median_test_mse: 191142497449.701385
- median_test_mae: 36664.966649
- coefficient_stability: 0.8937
- nonzero_count: 32
- sparsity_ratio: 0.8984
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0630
- median_test_mse: 191210411796.953735
- median_test_mae: 36540.308206
- coefficient_stability: 0.8762
- nonzero_count: 26
- sparsity_ratio: 0.9175
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0511
- median_test_mse: 193651660815.863739
- median_test_mae: 39691.268761
- coefficient_stability: 0.8462
- nonzero_count: 56
- sparsity_ratio: 0.9043
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0508
- median_test_mse: 193704333219.029541
- median_test_mae: 39800.967376
- coefficient_stability: 0.8744
- nonzero_count: 67
- sparsity_ratio: 0.8855
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0435
- median_test_mse: 195204338462.894714
- median_test_mae: 41399.711757
- coefficient_stability: 0.8068
- nonzero_count: 56
- sparsity_ratio: 0.9043
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0425
- median_test_mse: 195442359010.938599
- median_test_mae: 39458.144643
- coefficient_stability: 0.8587
- nonzero_count: 26
- sparsity_ratio: 0.9175
- raw_condition_number: inf
- effective_condition_number: 3747974.1805
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000002
- median_test_mae: 0.000498
- coefficient_stability: 0.9423
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4375376.9490
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000288
- coefficient_stability: 0.9840
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4375376.9490
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000168
- coefficient_stability: 0.9936
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4375376.9490
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9535
- median_test_mse: 0.000000
- median_test_mae: 0.000106
- coefficient_stability: 0.9359
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9368
- median_test_mse: 0.000002
- median_test_mae: 0.000399
- coefficient_stability: 0.9231
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.8541
- median_test_mse: 0.000005
- median_test_mae: 0.000608
- coefficient_stability: 0.9679
- nonzero_count: 8
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 4449097.0897
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, pitch_rate, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

## Skipped
- 无。