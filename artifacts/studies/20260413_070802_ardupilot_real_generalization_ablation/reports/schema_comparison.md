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
- effective_condition_number: 2157859719.2097
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
- effective_condition_number: 2157859719.2097
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
- effective_condition_number: 174538579.6148
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
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### full_augmented x selected_state_subset | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000059
- coefficient_stability: 0.9961
- nonzero_count: 16
- sparsity_ratio: 0.9690
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000059
- coefficient_stability: 0.9961
- nonzero_count: 32
- sparsity_ratio: 0.9690
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9997
- median_test_mse: 0.000241
- median_test_mae: 0.003354
- coefficient_stability: 0.9457
- nonzero_count: 22
- sparsity_ratio: 0.9574
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9997
- median_test_mse: 0.000241
- median_test_mae: 0.003354
- coefficient_stability: 0.9457
- nonzero_count: 44
- sparsity_ratio: 0.9574
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9997
- median_test_mse: 0.000246
- median_test_mae: 0.004019
- coefficient_stability: 0.9419
- nonzero_count: 44
- sparsity_ratio: 0.9574
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9997
- median_test_mse: 0.000262
- median_test_mae: 0.002576
- coefficient_stability: 0.9912
- nonzero_count: 16
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 2157859719.2097
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9997
- median_test_mse: 0.000262
- median_test_mae: 0.002576
- coefficient_stability: 0.9912
- nonzero_count: 32
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 2157859719.2097
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9996
- median_test_mse: 0.000268
- median_test_mae: 0.003260
- coefficient_stability: 0.9868
- nonzero_count: 32
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 2157859719.2097
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9996
- median_test_mse: 0.000295
- median_test_mae: 0.003507
- coefficient_stability: 0.9737
- nonzero_count: 8
- sparsity_ratio: 0.9298
- raw_condition_number: inf
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9996
- median_test_mse: 0.000295
- median_test_mae: 0.003507
- coefficient_stability: 0.9737
- nonzero_count: 16
- sparsity_ratio: 0.9298
- raw_condition_number: inf
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### full_augmented x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9996
- median_test_mse: 0.000030
- median_test_mae: 0.002098
- coefficient_stability: 0.9207
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 2238694525.3060
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x window_summary_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9996
- median_test_mse: 0.000298
- median_test_mae: 0.004032
- coefficient_stability: 0.9649
- nonzero_count: 16
- sparsity_ratio: 0.9298
- raw_condition_number: inf
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x window_summary_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9995
- median_test_mse: 0.000343
- median_test_mae: 0.002501
- coefficient_stability: 0.9868
- nonzero_count: 14
- sparsity_ratio: 0.9386
- raw_condition_number: inf
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state_history x window_summary_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9995
- median_test_mse: 0.000354
- median_test_mae: 0.002534
- coefficient_stability: 0.9912
- nonzero_count: 48
- sparsity_ratio: 0.9474
- raw_condition_number: inf
- effective_condition_number: 2157859719.2097
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9994
- median_test_mse: 0.000043
- median_test_mae: 0.002801
- coefficient_stability: 0.9474
- nonzero_count: 8
- sparsity_ratio: 0.8947
- raw_condition_number: inf
- effective_condition_number: 169722306.2266
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state_history x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9992
- median_test_mse: 0.000058
- median_test_mae: 0.002733
- coefficient_stability: 0.9474
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 2156723008.9311
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9992
- median_test_mse: 0.000063
- median_test_mae: 0.006667
- coefficient_stability: 0.9634
- nonzero_count: 135
- sparsity_ratio: 0.5884
- raw_condition_number: inf
- effective_condition_number: 2238694525.3060
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9990
- median_test_mse: 0.000079
- median_test_mae: 0.007323
- coefficient_stability: 1.0000
- nonzero_count: 127
- sparsity_ratio: 0.5822
- raw_condition_number: inf
- effective_condition_number: 2156723008.9311
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9990
- median_test_mse: 0.000800
- median_test_mae: 0.013389
- coefficient_stability: 0.9825
- nonzero_count: 172
- sparsity_ratio: 0.6228
- raw_condition_number: inf
- effective_condition_number: 2157859719.2097
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9990
- median_test_mse: 0.000800
- median_test_mae: 0.013389
- coefficient_stability: 0.9825
- nonzero_count: 344
- sparsity_ratio: 0.6228
- raw_condition_number: inf
- effective_condition_number: 2157859719.2097
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9990
- median_test_mse: 0.000802
- median_test_mae: 0.013615
- coefficient_stability: 0.9825
- nonzero_count: 340
- sparsity_ratio: 0.6272
- raw_condition_number: inf
- effective_condition_number: 2157859719.2097
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9988
- median_test_mse: 0.000096
- median_test_mae: 0.008284
- coefficient_stability: 0.9474
- nonzero_count: 52
- sparsity_ratio: 0.3158
- raw_condition_number: inf
- effective_condition_number: 169722306.2266
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001075
- median_test_mae: 0.017623
- coefficient_stability: 0.9474
- nonzero_count: 74
- sparsity_ratio: 0.3509
- raw_condition_number: inf
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001075
- median_test_mae: 0.017623
- coefficient_stability: 0.9474
- nonzero_count: 148
- sparsity_ratio: 0.3509
- raw_condition_number: inf
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x window_summary_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001077
- median_test_mae: 0.017818
- coefficient_stability: 0.9474
- nonzero_count: 150
- sparsity_ratio: 0.3421
- raw_condition_number: inf
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_only x actuator_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9986
- median_test_mse: 0.000115
- median_test_mae: 0.009822
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.7500
- raw_condition_number: 1.5102
- effective_condition_number: 1.5102
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9986
- median_test_mse: 0.000115
- median_test_mae: 0.009832
- coefficient_stability: 1.0000
- nonzero_count: 12
- sparsity_ratio: 0.2500
- raw_condition_number: 1.5102
- effective_condition_number: 1.5102
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9985
- median_test_mse: 0.000116
- median_test_mae: 0.009835
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.7500
- raw_condition_number: 1.5102
- effective_condition_number: 1.5102
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9984
- median_test_mse: 0.001200
- median_test_mae: 0.017510
- coefficient_stability: 0.9399
- nonzero_count: 192
- sparsity_ratio: 0.6279
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9984
- median_test_mse: 0.001200
- median_test_mae: 0.017510
- coefficient_stability: 0.9399
- nonzero_count: 384
- sparsity_ratio: 0.6279
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9984
- median_test_mse: 0.001200
- median_test_mae: 0.017700
- coefficient_stability: 0.9399
- nonzero_count: 387
- sparsity_ratio: 0.6250
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9977
- median_test_mse: 0.000178
- median_test_mae: 0.003957
- coefficient_stability: 0.9055
- nonzero_count: 28
- sparsity_ratio: 0.9146
- raw_condition_number: inf
- effective_condition_number: 2238694525.3060
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_only x selected_state_subset | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9972
- median_test_mse: 0.002218
- median_test_mae: 0.029684
- coefficient_stability: 1.0000
- nonzero_count: 3
- sparsity_ratio: 0.8750
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9972
- median_test_mse: 0.002218
- median_test_mae: 0.029684
- coefficient_stability: 1.0000
- nonzero_count: 6
- sparsity_ratio: 0.8750
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9972
- median_test_mse: 0.002217
- median_test_mae: 0.029645
- coefficient_stability: 1.0000
- nonzero_count: 6
- sparsity_ratio: 0.8750
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9972
- median_test_mse: 0.002225
- median_test_mae: 0.029709
- coefficient_stability: 1.0000
- nonzero_count: 19
- sparsity_ratio: 0.2083
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9972
- median_test_mse: 0.002225
- median_test_mae: 0.029709
- coefficient_stability: 1.0000
- nonzero_count: 38
- sparsity_ratio: 0.2083
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9972
- median_test_mse: 0.002225
- median_test_mae: 0.029715
- coefficient_stability: 1.0000
- nonzero_count: 3
- sparsity_ratio: 0.8750
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9972
- median_test_mse: 0.002225
- median_test_mae: 0.029715
- coefficient_stability: 1.0000
- nonzero_count: 6
- sparsity_ratio: 0.8750
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9972
- median_test_mse: 0.002224
- median_test_mae: 0.029670
- coefficient_stability: 1.0000
- nonzero_count: 37
- sparsity_ratio: 0.2292
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9972
- median_test_mse: 0.002224
- median_test_mae: 0.029674
- coefficient_stability: 1.0000
- nonzero_count: 6
- sparsity_ratio: 0.8750
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9949
- median_test_mse: 0.000387
- median_test_mae: 0.005904
- coefficient_stability: 0.9474
- nonzero_count: 24
- sparsity_ratio: 0.9211
- raw_condition_number: inf
- effective_condition_number: 2156723008.9311
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9949
- median_test_mse: 0.000387
- median_test_mae: 0.005903
- coefficient_stability: 0.9474
- nonzero_count: 6
- sparsity_ratio: 0.9211
- raw_condition_number: inf
- effective_condition_number: 169722306.2266
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 192104044153.508820
- median_test_mae: 27690.589445
- coefficient_stability: 0.8386
- nonzero_count: 229
- sparsity_ratio: 0.1965
- raw_condition_number: inf
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 192104914573.598694
- median_test_mae: 27764.502822
- coefficient_stability: 0.8632
- nonzero_count: 61
- sparsity_ratio: 0.7860
- raw_condition_number: inf
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 192138070089.521484
- median_test_mae: 28131.788182
- coefficient_stability: 0.8456
- nonzero_count: 67
- sparsity_ratio: 0.7649
- raw_condition_number: inf
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state_history x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9168
- median_test_mse: 186134452417.223755
- median_test_mae: 36762.248011
- coefficient_stability: 0.8719
- nonzero_count: 212
- sparsity_ratio: 0.8140
- raw_condition_number: inf
- effective_condition_number: 2157859719.2097
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9168
- median_test_mse: 186143808202.225708
- median_test_mae: 36825.482718
- coefficient_stability: 0.8279
- nonzero_count: 242
- sparsity_ratio: 0.8124
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9168
- median_test_mse: 186169468778.859680
- median_test_mae: 36924.374945
- coefficient_stability: 0.8254
- nonzero_count: 270
- sparsity_ratio: 0.7632
- raw_condition_number: inf
- effective_condition_number: 2157859719.2097
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9168
- median_test_mse: 186192073309.169708
- median_test_mae: 36580.496338
- coefficient_stability: 0.8544
- nonzero_count: 772
- sparsity_ratio: 0.3228
- raw_condition_number: inf
- effective_condition_number: 2157859719.2097
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9168
- median_test_mse: 186193170173.841003
- median_test_mae: 36589.436938
- coefficient_stability: 0.8171
- nonzero_count: 831
- sparsity_ratio: 0.3558
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1011
- median_test_mse: 186136624269.872650
- median_test_mae: 36744.424743
- coefficient_stability: 0.8807
- nonzero_count: 180
- sparsity_ratio: 0.8421
- raw_condition_number: inf
- effective_condition_number: 2157859719.2097
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1010
- median_test_mse: 186145942746.770477
- median_test_mae: 36808.269990
- coefficient_stability: 0.8605
- nonzero_count: 198
- sparsity_ratio: 0.8465
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1009
- median_test_mse: 186169468778.800293
- median_test_mae: 36924.374940
- coefficient_stability: 0.8254
- nonzero_count: 246
- sparsity_ratio: 0.7842
- raw_condition_number: inf
- effective_condition_number: 2157859719.2097
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1008
- median_test_mse: 186202959377.627716
- median_test_mae: 36547.597779
- coefficient_stability: 0.8789
- nonzero_count: 448
- sparsity_ratio: 0.6070
- raw_condition_number: inf
- effective_condition_number: 2157859719.2097
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1008
- median_test_mse: 186204029195.464203
- median_test_mae: 36555.704575
- coefficient_stability: 0.8690
- nonzero_count: 445
- sparsity_ratio: 0.6550
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0842
- median_test_mse: 0.692272
- median_test_mae: 0.109429
- coefficient_stability: 0.9302
- nonzero_count: 64
- sparsity_ratio: 0.9380
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0574
- median_test_mse: 192104110778.725525
- median_test_mae: 27688.055415
- coefficient_stability: 0.8807
- nonzero_count: 131
- sparsity_ratio: 0.5404
- raw_condition_number: inf
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0574
- median_test_mse: 192104530824.546600
- median_test_mae: 27738.334801
- coefficient_stability: 0.8772
- nonzero_count: 38
- sparsity_ratio: 0.8667
- raw_condition_number: inf
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0573
- median_test_mse: 192138070089.525513
- median_test_mae: 28131.788182
- coefficient_stability: 0.8456
- nonzero_count: 50
- sparsity_ratio: 0.8246
- raw_condition_number: inf
- effective_condition_number: 174538579.6148
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_only x next_raw_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0485
- median_test_mse: 2313523976168.594238
- median_test_mae: 328021.143851
- coefficient_stability: 0.7000
- nonzero_count: 26
- sparsity_ratio: 0.5667
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0485
- median_test_mse: 2313523976168.663574
- median_test_mae: 328021.143846
- coefficient_stability: 0.7000
- nonzero_count: 55
- sparsity_ratio: 0.0833
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0485
- median_test_mse: 2313526034063.608887
- median_test_mae: 328020.543594
- coefficient_stability: 0.7000
- nonzero_count: 26
- sparsity_ratio: 0.5667
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0036
- median_test_mse: 203070384661.281525
- median_test_mae: 28736.590009
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0036
- median_test_mse: 203070384661.328796
- median_test_mae: 28736.590007
- coefficient_stability: 0.8667
- nonzero_count: 32
- sparsity_ratio: 0.4667
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0036
- median_test_mse: 203070408887.115906
- median_test_mae: 28736.398255
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.5103
- effective_condition_number: 1.5103
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x next_raw_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -1.2653
- median_test_mse: 5074321341095.052734
- median_test_mae: 235344.127771
- coefficient_stability: 0.7798
- nonzero_count: 324
- sparsity_ratio: 0.7488
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -23.4847
- median_test_mse: 5074321338399.224609
- median_test_mae: 235344.127697
- coefficient_stability: 0.7822
- nonzero_count: 300
- sparsity_ratio: 0.7674
- raw_condition_number: inf
- effective_condition_number: 2401622636.7944
- conditioning_pruned_features: actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_stabilize, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_only x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000184
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5083
- effective_condition_number: 1.5083
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000184
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5083
- effective_condition_number: 1.5083
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000187
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5083
- effective_condition_number: 1.5083
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ols_affine | stratified
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9342
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x future_state_horizon | ols_affine | stratified
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9342
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000146
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 49461220.7347
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000146
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 49461220.7347
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000146
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 49461220.7347
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state_history x selected_state_subset | ols_affine | stratified
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9474
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | stratified
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9474
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x window_summary_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9342
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9208
- median_test_mse: 190667318419.819702
- median_test_mae: 34418.361646
- coefficient_stability: 0.8614
- nonzero_count: 26
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.9207
- median_test_mse: 190671437259.374573
- median_test_mae: 34372.228874
- coefficient_stability: 0.8842
- nonzero_count: 35
- sparsity_ratio: 0.8772
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x next_raw_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9207
- median_test_mse: 190677943498.602295
- median_test_mae: 34511.990960
- coefficient_stability: 0.8211
- nonzero_count: 26
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state_history x next_raw_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9179
- median_test_mse: 181533118415.684387
- median_test_mae: 39972.748302
- coefficient_stability: 0.8123
- nonzero_count: 104
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9178
- median_test_mse: 181818299117.393066
- median_test_mae: 39998.649494
- coefficient_stability: 0.8711
- nonzero_count: 104
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.9177
- median_test_mse: 181932841631.263031
- median_test_mae: 39288.600793
- coefficient_stability: 0.8610
- nonzero_count: 131
- sparsity_ratio: 0.8851
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9148
- median_test_mse: 0.000000
- median_test_mae: 0.000014
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9148
- median_test_mse: 0.000000
- median_test_mae: 0.000014
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x selected_state_subset | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9068
- median_test_mse: 0.000000
- median_test_mae: 0.000048
- coefficient_stability: 0.9912
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x future_state_horizon | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9068
- median_test_mse: 0.000000
- median_test_mae: 0.000048
- coefficient_stability: 0.9912
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x window_summary_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9068
- median_test_mse: 0.000000
- median_test_mae: 0.000048
- coefficient_stability: 0.9912
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state_history x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1229
- median_test_mse: 181533118417.572083
- median_test_mae: 39972.748296
- coefficient_stability: 0.8333
- nonzero_count: 104
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1215
- median_test_mse: 181824150562.141052
- median_test_mae: 39967.736965
- coefficient_stability: 0.8746
- nonzero_count: 104
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1209
- median_test_mse: 181949311100.265228
- median_test_mae: 39306.950662
- coefficient_stability: 0.8987
- nonzero_count: 116
- sparsity_ratio: 0.8982
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0641
- median_test_mse: 190668103539.210663
- median_test_mae: 34345.208996
- coefficient_stability: 0.8667
- nonzero_count: 26
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0641
- median_test_mse: 190671436566.903656
- median_test_mae: 34372.234647
- coefficient_stability: 0.8982
- nonzero_count: 32
- sparsity_ratio: 0.8877
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0640
- median_test_mse: 190677943661.274902
- median_test_mae: 34511.991065
- coefficient_stability: 0.8474
- nonzero_count: 26
- sparsity_ratio: 0.9088
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_only x next_raw_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0518
- median_test_mse: 2281373906645.422363
- median_test_mae: 330774.667258
- coefficient_stability: 0.7250
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0518
- median_test_mse: 2281373906645.661133
- median_test_mae: 330774.667261
- coefficient_stability: 0.7250
- nonzero_count: 20
- sparsity_ratio: 0.6667
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0518
- median_test_mse: 2281380811935.826172
- median_test_mae: 330773.752678
- coefficient_stability: 0.7250
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0036
- median_test_mse: 202982560040.270996
- median_test_mae: 29618.447631
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0036
- median_test_mse: 202982560040.315430
- median_test_mae: 29618.447627
- coefficient_stability: 0.8667
- nonzero_count: 14
- sparsity_ratio: 0.7667
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0036
- median_test_mse: 202982599171.718781
- median_test_mae: 29617.826625
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -1.0315
- median_test_mse: 0.000000
- median_test_mae: 0.000017
- coefficient_stability: 0.9825
- nonzero_count: 8
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -1.0315
- median_test_mse: 0.000000
- median_test_mae: 0.000017
- coefficient_stability: 0.9825
- nonzero_count: 8
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -1.0315
- median_test_mse: 0.000000
- median_test_mae: 0.000017
- coefficient_stability: 0.9825
- nonzero_count: 4
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### commands_plus_state_history x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -1.0880
- median_test_mse: 0.000000
- median_test_mae: 0.000080
- coefficient_stability: 0.9814
- nonzero_count: 6
- sparsity_ratio: 0.9868
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -1.0880
- median_test_mse: 0.000000
- median_test_mae: 0.000080
- coefficient_stability: 0.9814
- nonzero_count: 12
- sparsity_ratio: 0.9868
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_only x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -33645.5069
- median_test_mse: 0.001227
- median_test_mae: 0.015647
- coefficient_stability: 0.9583
- nonzero_count: 4
- sparsity_ratio: 0.9167
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -33645.5069
- median_test_mse: 0.001227
- median_test_mae: 0.015647
- coefficient_stability: 0.9583
- nonzero_count: 4
- sparsity_ratio: 0.9167
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -33645.5069
- median_test_mse: 0.001227
- median_test_mae: 0.015647
- coefficient_stability: 0.9583
- nonzero_count: 2
- sparsity_ratio: 0.9167
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -33717.3604
- median_test_mse: 0.001227
- median_test_mae: 0.015643
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -33717.3604
- median_test_mse: 0.001227
- median_test_mae: 0.015643
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -33717.3604
- median_test_mse: 0.001227
- median_test_mae: 0.015643
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -33718.1400
- median_test_mse: 0.001227
- median_test_mae: 0.015643
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -33718.1400
- median_test_mse: 0.001227
- median_test_mae: 0.015643
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -33718.1400
- median_test_mse: 0.001227
- median_test_mae: 0.015643
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5085
- effective_condition_number: 1.5085
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000146
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 793130917.9143
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000146
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 793130917.9143
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000146
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 793130917.9143
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9474
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9748
- median_test_mse: 0.000055
- median_test_mae: 0.002647
- coefficient_stability: 0.9428
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9748
- median_test_mse: 0.000055
- median_test_mae: 0.002647
- coefficient_stability: 0.9428
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000001
- median_test_mae: 0.000434
- coefficient_stability: 0.9771
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 795576282.4503
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000263
- coefficient_stability: 0.9802
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 795576282.4503
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000142
- coefficient_stability: 0.9954
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 795576282.4503
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9748
- median_test_mse: 0.000055
- median_test_mae: 0.002647
- coefficient_stability: 0.9428
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9747
- median_test_mse: 0.000056
- median_test_mae: 0.002651
- coefficient_stability: 0.9419
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9747
- median_test_mse: 0.000056
- median_test_mae: 0.002651
- coefficient_stability: 0.9419
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9747
- median_test_mse: 0.000056
- median_test_mae: 0.002651
- coefficient_stability: 0.9419
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.9158
- median_test_mse: 186120614197.593811
- median_test_mae: 49047.588266
- coefficient_stability: 0.8434
- nonzero_count: 141
- sparsity_ratio: 0.8907
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9148
- median_test_mse: 0.000000
- median_test_mae: 0.000014
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9144
- median_test_mse: 189279593415.812622
- median_test_mae: 52796.330855
- coefficient_stability: 0.8240
- nonzero_count: 110
- sparsity_ratio: 0.9147
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9130
- median_test_mse: 192257558585.424133
- median_test_mae: 56002.215718
- coefficient_stability: 0.8031
- nonzero_count: 110
- sparsity_ratio: 0.9147
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1021
- median_test_mse: 185850993168.764221
- median_test_mae: 48597.038442
- coefficient_stability: 0.8876
- nonzero_count: 122
- sparsity_ratio: 0.9054
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0856
- median_test_mse: 189263379362.359833
- median_test_mae: 52756.623274
- coefficient_stability: 0.8558
- nonzero_count: 110
- sparsity_ratio: 0.9147
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0712
- median_test_mse: 192257558342.492676
- median_test_mae: 56002.214572
- coefficient_stability: 0.8287
- nonzero_count: 110
- sparsity_ratio: 0.9147
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -1.0880
- median_test_mse: 0.000000
- median_test_mae: 0.000080
- coefficient_stability: 0.9814
- nonzero_count: 12
- sparsity_ratio: 0.9868
- raw_condition_number: inf
- effective_condition_number: 793951286.0993
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -1.0965
- median_test_mse: 0.000020
- median_test_mae: 0.001395
- coefficient_stability: 0.9651
- nonzero_count: 20
- sparsity_ratio: 0.9806
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -1.0965
- median_test_mse: 0.000020
- median_test_mae: 0.001395
- coefficient_stability: 0.9651
- nonzero_count: 20
- sparsity_ratio: 0.9806
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -1.0965
- median_test_mse: 0.000020
- median_test_mae: 0.001395
- coefficient_stability: 0.9651
- nonzero_count: 10
- sparsity_ratio: 0.9806
- raw_condition_number: inf
- effective_condition_number: 796445655.3722
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9405
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9405
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000097
- coefficient_stability: 0.9872
- nonzero_count: 5
- sparsity_ratio: 0.9786
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### feature_mapped_linear x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000097
- coefficient_stability: 0.9872
- nonzero_count: 10
- sparsity_ratio: 0.9786
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000091
- coefficient_stability: 0.9921
- nonzero_count: 5
- sparsity_ratio: 0.9603
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000091
- coefficient_stability: 0.9921
- nonzero_count: 10
- sparsity_ratio: 0.9603
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### pooled_backend_mode_augmented x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000038
- median_test_mae: 0.001211
- coefficient_stability: 0.9643
- nonzero_count: 22
- sparsity_ratio: 0.9127
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9998
- median_test_mse: 0.000116
- median_test_mae: 0.002516
- coefficient_stability: 0.9762
- nonzero_count: 8
- sparsity_ratio: 0.9365
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9998
- median_test_mse: 0.000116
- median_test_mae: 0.002516
- coefficient_stability: 0.9762
- nonzero_count: 16
- sparsity_ratio: 0.9365
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9998
- median_test_mse: 0.000119
- median_test_mae: 0.002995
- coefficient_stability: 0.9722
- nonzero_count: 16
- sparsity_ratio: 0.9365
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### pooled_backend_mode_augmented x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9998
- median_test_mse: 0.000017
- median_test_mae: 0.001728
- coefficient_stability: 0.9524
- nonzero_count: 8
- sparsity_ratio: 0.9048
- raw_condition_number: inf
- effective_condition_number: 175497929.0544
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### feature_mapped_linear x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9998
- median_test_mse: 0.000180
- median_test_mae: 0.003077
- coefficient_stability: 0.9188
- nonzero_count: 16
- sparsity_ratio: 0.9316
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### feature_mapped_linear x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9998
- median_test_mse: 0.000180
- median_test_mae: 0.003077
- coefficient_stability: 0.9188
- nonzero_count: 32
- sparsity_ratio: 0.9316
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### feature_mapped_linear x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9998
- median_test_mse: 0.000187
- median_test_mae: 0.003627
- coefficient_stability: 0.9145
- nonzero_count: 31
- sparsity_ratio: 0.9338
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### feature_mapped_linear x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9996
- median_test_mse: 0.000323
- median_test_mae: 0.002279
- coefficient_stability: 0.9402
- nonzero_count: 26
- sparsity_ratio: 0.9444
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### pooled_backend_mode_augmented x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9994
- median_test_mse: 0.000044
- median_test_mae: 0.002015
- coefficient_stability: 0.9524
- nonzero_count: 14
- sparsity_ratio: 0.8333
- raw_condition_number: inf
- effective_condition_number: 175497929.0544
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### feature_mapped_linear x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9993
- median_test_mse: 0.000050
- median_test_mae: 0.002593
- coefficient_stability: 0.8782
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 223556540.4496
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### feature_mapped_linear x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9990
- median_test_mse: 0.000084
- median_test_mae: 0.006960
- coefficient_stability: 0.9231
- nonzero_count: 108
- sparsity_ratio: 0.3077
- raw_condition_number: inf
- effective_condition_number: 223556540.4496
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### feature_mapped_linear x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9990
- median_test_mse: 0.000839
- median_test_mae: 0.013295
- coefficient_stability: 0.8632
- nonzero_count: 127
- sparsity_ratio: 0.4573
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### feature_mapped_linear x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9990
- median_test_mse: 0.000839
- median_test_mae: 0.013295
- coefficient_stability: 0.8632
- nonzero_count: 254
- sparsity_ratio: 0.4573
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### feature_mapped_linear x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9989
- median_test_mse: 0.000847
- median_test_mae: 0.013676
- coefficient_stability: 0.8590
- nonzero_count: 259
- sparsity_ratio: 0.4466
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### feature_mapped_linear x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9988
- median_test_mse: 0.000091
- median_test_mae: 0.002802
- coefficient_stability: 0.8910
- nonzero_count: 26
- sparsity_ratio: 0.8333
- raw_condition_number: inf
- effective_condition_number: 223556540.4496
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### pooled_backend_mode_augmented x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9988
- median_test_mse: 0.000096
- median_test_mae: 0.008284
- coefficient_stability: 0.9524
- nonzero_count: 52
- sparsity_ratio: 0.3810
- raw_condition_number: inf
- effective_condition_number: 175497929.0544
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001074
- median_test_mae: 0.017606
- coefficient_stability: 0.9524
- nonzero_count: 76
- sparsity_ratio: 0.3968
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001074
- median_test_mae: 0.017606
- coefficient_stability: 0.9524
- nonzero_count: 152
- sparsity_ratio: 0.3968
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001075
- median_test_mae: 0.017801
- coefficient_stability: 0.9524
- nonzero_count: 155
- sparsity_ratio: 0.3849
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### feature_mapped_linear x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191867433150.361023
- median_test_mae: 30636.511195
- coefficient_stability: 0.7043
- nonzero_count: 441
- sparsity_ratio: 0.2462
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### feature_mapped_linear x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9211
- median_test_mse: 191884548759.402344
- median_test_mae: 30902.988816
- coefficient_stability: 0.7897
- nonzero_count: 115
- sparsity_ratio: 0.8034
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 192104044830.364929
- median_test_mae: 27690.570460
- coefficient_stability: 0.8476
- nonzero_count: 234
- sparsity_ratio: 0.2571
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 192104934671.951996
- median_test_mae: 27767.693271
- coefficient_stability: 0.8667
- nonzero_count: 65
- sparsity_ratio: 0.7937
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### pooled_backend_mode_augmented x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9210
- median_test_mse: 192109647508.115906
- median_test_mae: 27906.616016
- coefficient_stability: 0.8508
- nonzero_count: 83
- sparsity_ratio: 0.7365
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### feature_mapped_linear x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.8768
- median_test_mse: 299554627771.196655
- median_test_mae: 60552.324766
- coefficient_stability: 0.7162
- nonzero_count: 162
- sparsity_ratio: 0.7231
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### feature_mapped_linear x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0586
- median_test_mse: 191865768346.786377
- median_test_mae: 30622.621201
- coefficient_stability: 0.8564
- nonzero_count: 231
- sparsity_ratio: 0.6051
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### feature_mapped_linear x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0585
- median_test_mse: 191884233172.991882
- median_test_mae: 30895.919931
- coefficient_stability: 0.8325
- nonzero_count: 78
- sparsity_ratio: 0.8667
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### pooled_backend_mode_augmented x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0574
- median_test_mse: 192104112414.311951
- median_test_mae: 27688.025656
- coefficient_stability: 0.8857
- nonzero_count: 133
- sparsity_ratio: 0.5778
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### pooled_backend_mode_augmented x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0574
- median_test_mse: 192104549261.979675
- median_test_mae: 27741.312022
- coefficient_stability: 0.8794
- nonzero_count: 42
- sparsity_ratio: 0.8667
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### pooled_backend_mode_augmented x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0574
- median_test_mse: 192109647507.376709
- median_test_mae: 27906.615973
- coefficient_stability: 0.8540
- nonzero_count: 66
- sparsity_ratio: 0.7905
- raw_condition_number: inf
- effective_condition_number: 180462701.8538
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize

### feature_mapped_linear x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.4693
- median_test_mse: 299554627731.624146
- median_test_mae: 60552.324706
- coefficient_stability: 0.7214
- nonzero_count: 145
- sparsity_ratio: 0.7521
- raw_condition_number: inf
- effective_condition_number: 229622684.5373
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, sq__pitch, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, sq__pitch, sq__roll

### pooled_backend_mode_augmented x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000146
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 49461220.7347
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000146
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 49461220.7347
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000146
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 49461220.7347
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9405
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9993
- median_test_mse: 0.000002
- median_test_mae: 0.000376
- coefficient_stability: 0.9338
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9993
- median_test_mse: 0.000002
- median_test_mae: 0.000376
- coefficient_stability: 0.9338
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9208
- median_test_mse: 190615290853.931396
- median_test_mae: 36298.682658
- coefficient_stability: 0.8162
- nonzero_count: 85
- sparsity_ratio: 0.8547
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9208
- median_test_mse: 190667318419.820190
- median_test_mae: 34418.361646
- coefficient_stability: 0.8746
- nonzero_count: 26
- sparsity_ratio: 0.9175
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9207
- median_test_mse: 190671437259.374573
- median_test_mae: 34372.228874
- coefficient_stability: 0.8952
- nonzero_count: 35
- sparsity_ratio: 0.8889
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9207
- median_test_mse: 190677943498.602295
- median_test_mae: 34511.990960
- coefficient_stability: 0.8381
- nonzero_count: 26
- sparsity_ratio: 0.9175
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9204
- median_test_mse: 191391415110.452301
- median_test_mae: 37894.467442
- coefficient_stability: 0.8068
- nonzero_count: 56
- sparsity_ratio: 0.9043
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9091
- median_test_mse: 0.000003
- median_test_mae: 0.000522
- coefficient_stability: 0.9359
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9091
- median_test_mse: 0.000003
- median_test_mae: 0.000522
- coefficient_stability: 0.9359
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9068
- median_test_mse: 0.000000
- median_test_mae: 0.000048
- coefficient_stability: 0.9921
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9068
- median_test_mse: 0.000000
- median_test_mae: 0.000048
- coefficient_stability: 0.9921
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9068
- median_test_mse: 0.000000
- median_test_mae: 0.000048
- coefficient_stability: 0.9921
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.8986
- median_test_mse: 243798274452.981079
- median_test_mae: 57607.561456
- coefficient_stability: 0.7359
- nonzero_count: 56
- sparsity_ratio: 0.9043
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0648
- median_test_mse: 190526513781.576904
- median_test_mae: 36101.508765
- coefficient_stability: 0.8744
- nonzero_count: 74
- sparsity_ratio: 0.8735
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0641
- median_test_mse: 190668103539.210938
- median_test_mae: 34345.208996
- coefficient_stability: 0.8794
- nonzero_count: 26
- sparsity_ratio: 0.9175
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0641
- median_test_mse: 190671436566.903656
- median_test_mae: 34372.234647
- coefficient_stability: 0.9079
- nonzero_count: 32
- sparsity_ratio: 0.8984
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0640
- median_test_mse: 190677943661.274902
- median_test_mae: 34511.991065
- coefficient_stability: 0.8619
- nonzero_count: 26
- sparsity_ratio: 0.9175
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0605
- median_test_mse: 191390825552.699402
- median_test_mae: 37821.425344
- coefficient_stability: 0.8385
- nonzero_count: 56
- sparsity_ratio: 0.9043
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.1977
- median_test_mse: 243798270165.559998
- median_test_mae: 57607.561535
- coefficient_stability: 0.7675
- nonzero_count: 56
- sparsity_ratio: 0.9043
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -1.0315
- median_test_mse: 0.000000
- median_test_mae: 0.000017
- coefficient_stability: 0.9841
- nonzero_count: 8
- sparsity_ratio: 0.9683
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -1.0315
- median_test_mse: 0.000000
- median_test_mae: 0.000017
- coefficient_stability: 0.9841
- nonzero_count: 8
- sparsity_ratio: 0.9683
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -1.0315
- median_test_mse: 0.000000
- median_test_mae: 0.000017
- coefficient_stability: 0.9841
- nonzero_count: 4
- sparsity_ratio: 0.9683
- raw_condition_number: inf
- effective_condition_number: 51012490.8449
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -1.0321
- median_test_mse: 0.000001
- median_test_mae: 0.000307
- coefficient_stability: 0.9722
- nonzero_count: 12
- sparsity_ratio: 0.9744
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -1.0321
- median_test_mse: 0.000001
- median_test_mae: 0.000307
- coefficient_stability: 0.9722
- nonzero_count: 6
- sparsity_ratio: 0.9744
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000275
- coefficient_stability: 0.9744
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 6559921320.7999
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000212
- coefficient_stability: 0.9840
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 6559921320.7999
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000152
- coefficient_stability: 0.9968
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 6559921320.7999
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9993
- median_test_mse: 0.000002
- median_test_mae: 0.000376
- coefficient_stability: 0.9338
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9091
- median_test_mse: 0.000003
- median_test_mae: 0.000522
- coefficient_stability: 0.9359
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

### feature_mapped_linear x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -1.0321
- median_test_mse: 0.000001
- median_test_mae: 0.000307
- coefficient_stability: 0.9722
- nonzero_count: 12
- sparsity_ratio: 0.9744
- raw_condition_number: inf
- effective_condition_number: 8123693042.5716
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw_rate

## Skipped
- 无。