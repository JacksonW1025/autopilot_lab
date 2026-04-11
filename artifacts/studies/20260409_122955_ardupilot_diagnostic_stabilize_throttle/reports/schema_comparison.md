# Schema Comparison: ardupilot_diagnostic_stabilize_throttle

## Results
### commands_only x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.8929
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 272.3376
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### commands_plus_state x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.8929
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 272.3376
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### commands_plus_state x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 272.3098
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### commands_plus_state x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 272.3098
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### commands_plus_state x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 272.3098
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### commands_plus_state_history x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9999
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9405
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 538.8798
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 538.9350
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 538.9350
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 538.9350
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9233
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 648.7338
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9233
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 648.7338
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9999
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9405
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 538.8798
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9236
- median_test_mse: 170709095350.807770
- median_test_mae: 45668.053308
- coefficient_stability: 0.8360
- nonzero_count: 76
- sparsity_ratio: 0.9196
- raw_condition_number: inf
- effective_condition_number: 648.7338
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9236
- median_test_mse: 170713629471.100891
- median_test_mae: 45635.691874
- coefficient_stability: 0.8360
- nonzero_count: 72
- sparsity_ratio: 0.9238
- raw_condition_number: inf
- effective_condition_number: 648.7338
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9236
- median_test_mse: 170726488298.934753
- median_test_mae: 45610.079270
- coefficient_stability: 0.9418
- nonzero_count: 77
- sparsity_ratio: 0.9185
- raw_condition_number: inf
- effective_condition_number: 648.7338
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9235
- median_test_mse: 170775383625.450195
- median_test_mae: 46063.109277
- coefficient_stability: 0.8476
- nonzero_count: 64
- sparsity_ratio: 0.9238
- raw_condition_number: inf
- effective_condition_number: 538.8798
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9235
- median_test_mse: 170780105106.046692
- median_test_mae: 45930.516144
- coefficient_stability: 0.8381
- nonzero_count: 60
- sparsity_ratio: 0.9286
- raw_condition_number: inf
- effective_condition_number: 538.8798
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9235
- median_test_mse: 170793570661.380310
- median_test_mae: 46051.517014
- coefficient_stability: 0.9488
- nonzero_count: 66
- sparsity_ratio: 0.9214
- raw_condition_number: inf
- effective_condition_number: 538.8798
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x next_raw_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9217
- median_test_mse: 189955464529.902374
- median_test_mae: 38887.592915
- coefficient_stability: 0.8000
- nonzero_count: 16
- sparsity_ratio: 0.9238
- raw_condition_number: inf
- effective_condition_number: 272.3376
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### commands_plus_state x next_raw_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9217
- median_test_mse: 189955869975.041626
- median_test_mae: 38800.843250
- coefficient_stability: 0.7667
- nonzero_count: 16
- sparsity_ratio: 0.9238
- raw_condition_number: inf
- effective_condition_number: 272.3376
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### commands_plus_state x next_raw_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9217
- median_test_mse: 189956874990.748962
- median_test_mae: 38738.655213
- coefficient_stability: 0.9381
- nonzero_count: 14
- sparsity_ratio: 0.9333
- raw_condition_number: inf
- effective_condition_number: 272.3376
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### full_augmented x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1789
- median_test_mse: 170704652345.565491
- median_test_mae: 45556.437703
- coefficient_stability: 0.8794
- nonzero_count: 76
- sparsity_ratio: 0.9196
- raw_condition_number: inf
- effective_condition_number: 648.7338
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1789
- median_test_mse: 170713629471.100891
- median_test_mae: 45635.691874
- coefficient_stability: 0.8772
- nonzero_count: 72
- sparsity_ratio: 0.9238
- raw_condition_number: inf
- effective_condition_number: 648.7338
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1788
- median_test_mse: 170726661661.250061
- median_test_mae: 45609.439507
- coefficient_stability: 0.9450
- nonzero_count: 73
- sparsity_ratio: 0.9228
- raw_condition_number: inf
- effective_condition_number: 648.7338
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1786
- median_test_mse: 170771051674.001434
- median_test_mae: 45949.561731
- coefficient_stability: 0.8762
- nonzero_count: 64
- sparsity_ratio: 0.9238
- raw_condition_number: inf
- effective_condition_number: 538.8798
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1785
- median_test_mse: 170780105106.047546
- median_test_mae: 45930.516144
- coefficient_stability: 0.8762
- nonzero_count: 60
- sparsity_ratio: 0.9286
- raw_condition_number: inf
- effective_condition_number: 538.8798
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1785
- median_test_mse: 170793742288.695831
- median_test_mae: 46050.830505
- coefficient_stability: 0.9524
- nonzero_count: 64
- sparsity_ratio: 0.9238
- raw_condition_number: inf
- effective_condition_number: 538.8798
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0716
- median_test_mse: 189955869975.041595
- median_test_mae: 38800.843250
- coefficient_stability: 0.8286
- nonzero_count: 16
- sparsity_ratio: 0.9238
- raw_condition_number: inf
- effective_condition_number: 272.3376
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### commands_plus_state x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0716
- median_test_mse: 189956876693.662231
- median_test_mae: 38738.603600
- coefficient_stability: 0.9524
- nonzero_count: 14
- sparsity_ratio: 0.9333
- raw_condition_number: inf
- effective_condition_number: 272.3376
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### commands_plus_state x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0716
- median_test_mse: 189956920699.136017
- median_test_mae: 38715.270340
- coefficient_stability: 0.8571
- nonzero_count: 16
- sparsity_ratio: 0.9238
- raw_condition_number: inf
- effective_condition_number: 272.3376
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### commands_only x next_raw_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0058
- median_test_mse: 2413122914332.630859
- median_test_mae: 343663.062999
- coefficient_stability: 0.8667
- nonzero_count: 2
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0058
- median_test_mse: 2413125420660.258789
- median_test_mae: 343662.872081
- coefficient_stability: 0.8667
- nonzero_count: 4
- sparsity_ratio: 0.7333
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0058
- median_test_mse: 2413125420660.713867
- median_test_mae: 343662.872080
- coefficient_stability: 0.8667
- nonzero_count: 2
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0019
- median_test_mse: 204217729081.883942
- median_test_mae: 29451.922431
- coefficient_stability: 0.8667
- nonzero_count: 2
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0019
- median_test_mse: 204217824791.472351
- median_test_mae: 29453.896615
- coefficient_stability: 0.8667
- nonzero_count: 4
- sparsity_ratio: 0.7333
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0019
- median_test_mse: 204217824791.571533
- median_test_mae: 29453.896618
- coefficient_stability: 0.8667
- nonzero_count: 2
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -4294778419.6761
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9233
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 648.7338
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -4294778420.5329
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9233
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 648.7338
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -3635858288408.6665
- median_test_mse: 0.000000
- median_test_mae: 0.000001
- coefficient_stability: 0.9405
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 538.8798
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -3635858288438.1978
- median_test_mse: 0.000000
- median_test_mae: 0.000001
- coefficient_stability: 0.9405
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 538.8798
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -6256594828821.4131
- median_test_mse: 0.000000
- median_test_mae: 0.000002
- coefficient_stability: 0.9048
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 272.3376
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### commands_plus_state x future_state_horizon | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -6256594828821.4131
- median_test_mse: 0.000000
- median_test_mae: 0.000002
- coefficient_stability: 0.9048
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 272.3376
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### commands_plus_state x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -138085659911445.3906
- median_test_mse: 0.000000
- median_test_mae: 0.000010
- coefficient_stability: 0.9643
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 272.3376
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### commands_plus_state x future_state_horizon | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -138085659911445.3906
- median_test_mse: 0.000000
- median_test_mae: 0.000010
- coefficient_stability: 0.9643
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 272.3376
- conditioning_pruned_features: altitude, heading, pitch, pitch_rate, position_y, position_z, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, pitch_rate, position_y, position_z, yaw, yaw_rate

### full_augmented x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -145359812282889.8438
- median_test_mse: 0.000000
- median_test_mae: 0.000010
- coefficient_stability: 0.9921
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 648.7338
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -145359812282889.8438
- median_test_mse: 0.000000
- median_test_mae: 0.000010
- coefficient_stability: 0.9921
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 648.7338
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -145588290115770.5938
- median_test_mse: 0.000000
- median_test_mae: 0.000010
- coefficient_stability: 0.9911
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 538.8798
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -145588290115770.5938
- median_test_mse: 0.000000
- median_test_mae: 0.000010
- coefficient_stability: 0.9911
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 538.8798
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_only x future_state_horizon | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -215028990430623072.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000312
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -215028990430623104.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000312
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -217511573300210720.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000312
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -217511573300210752.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000312
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -217521997177265472.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000312
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -217521997177265504.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000312
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0000
- effective_condition_number: 1.0000
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 648.8505
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 648.8505
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 648.8505
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_ardupilot_diagnostic_stabilize_throttle__large, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: config_profile_ardupilot_diagnostic_stabilize_throttle__large
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

## Skipped
- 无。