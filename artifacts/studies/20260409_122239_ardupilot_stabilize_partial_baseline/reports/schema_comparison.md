# Schema Comparison: ardupilot_stabilize_partial_baseline

## Results
### commands_only x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4087685880709.1313
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4087685880709.1313
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4087685880709.1313
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_plus_state x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9241
- median_test_mse: 185341732987.346008
- median_test_mae: 44507.747924
- coefficient_stability: 0.8588
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9241
- median_test_mse: 185342543222.067993
- median_test_mae: 44290.282777
- coefficient_stability: 0.9608
- nonzero_count: 25
- sparsity_ratio: 0.9020
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9241
- median_test_mse: 185343326951.292480
- median_test_mae: 44298.597635
- coefficient_stability: 0.8588
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4651980493333.9824
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4651980493333.9824
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4651980493333.9824
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### full_augmented x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9208
- median_test_mse: 177966543827.860931
- median_test_mae: 50930.813924
- coefficient_stability: 0.8611
- nonzero_count: 94
- sparsity_ratio: 0.9130
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9208
- median_test_mse: 177969388937.255737
- median_test_mae: 50937.869084
- coefficient_stability: 0.8745
- nonzero_count: 88
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9207
- median_test_mse: 177980755537.338135
- median_test_mae: 51104.926380
- coefficient_stability: 0.8745
- nonzero_count: 88
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9207
- median_test_mse: 178002990722.556763
- median_test_mae: 50969.625327
- coefficient_stability: 0.9608
- nonzero_count: 73
- sparsity_ratio: 0.9284
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1498
- median_test_mse: 177969388937.255920
- median_test_mae: 50937.869084
- coefficient_stability: 0.8824
- nonzero_count: 88
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1498
- median_test_mse: 177974152709.322021
- median_test_mae: 50829.318760
- coefficient_stability: 0.8824
- nonzero_count: 88
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1496
- median_test_mse: 178008677435.555878
- median_test_mae: 50979.070700
- coefficient_stability: 0.9608
- nonzero_count: 60
- sparsity_ratio: 0.9412
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1003
- median_test_mse: 185342542690.000732
- median_test_mae: 44290.278859
- coefficient_stability: 0.9608
- nonzero_count: 18
- sparsity_ratio: 0.9294
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1003
- median_test_mse: 185343326951.292480
- median_test_mae: 44298.597635
- coefficient_stability: 0.8824
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1003
- median_test_mse: 185343633297.742767
- median_test_mae: 44232.351815
- coefficient_stability: 0.8824
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_only x next_raw_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0511
- median_test_mse: 2315774656140.432617
- median_test_mae: 331419.067345
- coefficient_stability: 0.4000
- nonzero_count: 36
- sparsity_ratio: 0.4000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x next_raw_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0511
- median_test_mse: 2315780193858.882812
- median_test_mae: 331044.409729
- coefficient_stability: 0.9667
- nonzero_count: 4
- sparsity_ratio: 0.9333
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x next_raw_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0511
- median_test_mse: 2315780578608.206055
- median_test_mae: 331041.405757
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0366
- median_test_mse: 198462637596.547485
- median_test_mae: 37893.784657
- coefficient_stability: 0.9667
- nonzero_count: 4
- sparsity_ratio: 0.9333
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0366
- median_test_mse: 198462666934.632080
- median_test_mae: 37889.523575
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0366
- median_test_mse: 198464451967.633667
- median_test_mae: 37716.999957
- coefficient_stability: 0.7333
- nonzero_count: 16
- sparsity_ratio: 0.7333
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_plus_state_history x selected_state_subset | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -1237267154.0621
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9902
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -1237267154.0621
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9902
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x future_state_horizon | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -3800810503.6385
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x window_summary_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -3800810503.6385
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x selected_state_subset | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -3800810503.6385
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state_history x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -10725454783151704.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000005
- coefficient_stability: 0.9902
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -10725454783151704.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000005
- coefficient_stability: 0.9902
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x future_state_horizon | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -48536911104422472.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x window_summary_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -48536911104422472.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -48536911104422480.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state_history x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -275169796459952896.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 7
- sparsity_ratio: 0.9828
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -275169796459952896.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9828
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x future_state_horizon | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -795625513633803904.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9314
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x window_summary_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -795625513633803904.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9314
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -795625513633804032.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 7
- sparsity_ratio: 0.9314
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_only x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -679517778792026079232.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001053
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x future_state_horizon | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -679517778792026079232.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001053
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x window_summary_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -679517778792026079232.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001053
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -679524158711544414208.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001053
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x future_state_horizon | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -679524158711544414208.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001053
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x window_summary_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -679524158711544414208.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001053
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x selected_state_subset | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -679743740463623831552.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001054
- coefficient_stability: 0.3333
- nonzero_count: 16
- sparsity_ratio: 0.3333
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x future_state_horizon | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -679743740463623831552.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001054
- coefficient_stability: 0.3333
- nonzero_count: 32
- sparsity_ratio: 0.3333
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x window_summary_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -679743740463623831552.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001054
- coefficient_stability: 0.3333
- nonzero_count: 32
- sparsity_ratio: 0.3333
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_plus_state_history x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7314022998286.6875
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7314022998286.6875
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7314022998286.6875
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9207
- median_test_mse: 177979003693.868164
- median_test_mae: 51102.123958
- coefficient_stability: 0.8611
- nonzero_count: 94
- sparsity_ratio: 0.9130
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9207
- median_test_mse: 178001554896.234192
- median_test_mae: 50956.936670
- coefficient_stability: 0.9565
- nonzero_count: 79
- sparsity_ratio: 0.9269
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1498
- median_test_mse: 177966543827.860962
- median_test_mae: 50930.813915
- coefficient_stability: 0.8759
- nonzero_count: 94
- sparsity_ratio: 0.9130
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1498
- median_test_mse: 177972422424.855957
- median_test_mae: 50825.431182
- coefficient_stability: 0.8759
- nonzero_count: 94
- sparsity_ratio: 0.9130
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1496
- median_test_mse: 178006684002.841064
- median_test_mae: 50978.944095
- coefficient_stability: 0.9574
- nonzero_count: 65
- sparsity_ratio: 0.9398
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -1237267154.0621
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9902
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -10725454783151704.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000005
- coefficient_stability: 0.9902
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -167940388040821440.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000023
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -167940388040821440.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000023
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -168839117912941536.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000023
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -168839117912941568.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000023
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -275169796459952896.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9828
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -411935638741014400.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000038
- coefficient_stability: 0.9977
- nonzero_count: 7
- sparsity_ratio: 0.9838
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7314022998286.6875
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7314022998286.6875
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7314022998286.6875
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -167940388040821440.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000023
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -168839117912941568.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000023
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -411935638741014400.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000038
- coefficient_stability: 0.9977
- nonzero_count: 14
- sparsity_ratio: 0.9838
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -411935638741014400.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000038
- coefficient_stability: 0.9977
- nonzero_count: 14
- sparsity_ratio: 0.9838
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_only x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4087685880709.1313
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4087685880709.1313
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4087685880709.1313
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_plus_state x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9241
- median_test_mse: 185341732987.346008
- median_test_mae: 44507.747924
- coefficient_stability: 0.8588
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.9241
- median_test_mse: 185342543222.067993
- median_test_mae: 44290.282777
- coefficient_stability: 0.9608
- nonzero_count: 25
- sparsity_ratio: 0.9020
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x next_raw_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9241
- median_test_mse: 185343326951.292480
- median_test_mae: 44298.597635
- coefficient_stability: 0.8588
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4651980493333.9824
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4651980493333.9824
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4651980493333.9824
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### full_augmented x next_raw_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9208
- median_test_mse: 177966543827.860931
- median_test_mae: 50930.813924
- coefficient_stability: 0.8611
- nonzero_count: 94
- sparsity_ratio: 0.9130
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9208
- median_test_mse: 177969388937.255737
- median_test_mae: 50937.869084
- coefficient_stability: 0.8745
- nonzero_count: 88
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9207
- median_test_mse: 177980755537.338135
- median_test_mae: 51104.926380
- coefficient_stability: 0.8745
- nonzero_count: 88
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.9207
- median_test_mse: 178002990722.556763
- median_test_mae: 50969.625327
- coefficient_stability: 0.9608
- nonzero_count: 73
- sparsity_ratio: 0.9284
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1498
- median_test_mse: 177969388937.255920
- median_test_mae: 50937.869084
- coefficient_stability: 0.8824
- nonzero_count: 88
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1498
- median_test_mse: 177974152709.322021
- median_test_mae: 50829.318760
- coefficient_stability: 0.8824
- nonzero_count: 88
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1496
- median_test_mse: 178008677435.555878
- median_test_mae: 50979.070700
- coefficient_stability: 0.9608
- nonzero_count: 60
- sparsity_ratio: 0.9412
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1003
- median_test_mse: 185342542690.000732
- median_test_mae: 44290.278859
- coefficient_stability: 0.9608
- nonzero_count: 18
- sparsity_ratio: 0.9294
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1003
- median_test_mse: 185343326951.292480
- median_test_mae: 44298.597635
- coefficient_stability: 0.8824
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1003
- median_test_mse: 185343633297.742767
- median_test_mae: 44232.351815
- coefficient_stability: 0.8824
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_only x next_raw_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0511
- median_test_mse: 2315774656140.432617
- median_test_mae: 331419.067345
- coefficient_stability: 0.4000
- nonzero_count: 36
- sparsity_ratio: 0.4000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x next_raw_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0511
- median_test_mse: 2315780193858.882812
- median_test_mae: 331044.409729
- coefficient_stability: 0.9667
- nonzero_count: 4
- sparsity_ratio: 0.9333
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x next_raw_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0511
- median_test_mse: 2315780578608.206055
- median_test_mae: 331041.405757
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0366
- median_test_mse: 198462637596.547485
- median_test_mae: 37893.784657
- coefficient_stability: 0.9667
- nonzero_count: 4
- sparsity_ratio: 0.9333
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0366
- median_test_mse: 198462666934.632080
- median_test_mae: 37889.523575
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0366
- median_test_mse: 198464451967.633667
- median_test_mae: 37716.999957
- coefficient_stability: 0.7333
- nonzero_count: 16
- sparsity_ratio: 0.7333
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_plus_state_history x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -1237267154.0621
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9902
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -1237267154.0621
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9902
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -3800810503.6385
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -3800810503.6385
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -3800810503.6385
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state_history x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -10725454783151704.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000005
- coefficient_stability: 0.9902
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -10725454783151704.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000005
- coefficient_stability: 0.9902
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -48536911104422472.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -48536911104422472.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -48536911104422480.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state_history x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -275169796459952896.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 7
- sparsity_ratio: 0.9828
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -275169796459952896.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9828
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -795625513633803904.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9314
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -795625513633803904.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9314
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_plus_state x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -795625513633804032.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 7
- sparsity_ratio: 0.9314
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### commands_only x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -679517778792026079232.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001053
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -679517778792026079232.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001053
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -679517778792026079232.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001053
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -679524158711544414208.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001053
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -679524158711544414208.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001053
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -679524158711544414208.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001053
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -679743740463623831552.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001054
- coefficient_stability: 0.3333
- nonzero_count: 16
- sparsity_ratio: 0.3333
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -679743740463623831552.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001054
- coefficient_stability: 0.3333
- nonzero_count: 32
- sparsity_ratio: 0.3333
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_only x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -679743740463623831552.0000
- median_test_mse: 0.000002
- median_test_mae: 0.001054
- coefficient_stability: 0.3333
- nonzero_count: 32
- sparsity_ratio: 0.3333
- raw_condition_number: inf
- effective_condition_number: 4164270569003.7686
- conditioning_pruned_features: command_pitch, command_yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw

### commands_plus_state_history x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7314022998286.6875
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7314022998286.6875
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7314022998286.6875
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9207
- median_test_mse: 177979003693.868164
- median_test_mae: 51102.123958
- coefficient_stability: 0.8611
- nonzero_count: 94
- sparsity_ratio: 0.9130
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.9207
- median_test_mse: 178001554896.234192
- median_test_mae: 50956.936670
- coefficient_stability: 0.9565
- nonzero_count: 79
- sparsity_ratio: 0.9269
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1498
- median_test_mse: 177966543827.860962
- median_test_mae: 50930.813915
- coefficient_stability: 0.8759
- nonzero_count: 94
- sparsity_ratio: 0.9130
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1498
- median_test_mse: 177972422424.855957
- median_test_mae: 50825.431182
- coefficient_stability: 0.8759
- nonzero_count: 94
- sparsity_ratio: 0.9130
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1496
- median_test_mse: 178006684002.841064
- median_test_mae: 50978.944095
- coefficient_stability: 0.9574
- nonzero_count: 65
- sparsity_ratio: 0.9398
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -1237267154.0621
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9902
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -10725454783151704.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000005
- coefficient_stability: 0.9902
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -167940388040821440.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000023
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -167940388040821440.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000023
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -168839117912941536.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000023
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -168839117912941568.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000023
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -275169796459952896.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9828
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -411935638741014400.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000038
- coefficient_stability: 0.9977
- nonzero_count: 7
- sparsity_ratio: 0.9838
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7314022998286.6875
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7314022998286.6875
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7314022998286.6875
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -167940388040821440.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000023
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -168839117912941568.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000023
- coefficient_stability: 0.9722
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -411935638741014400.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000038
- coefficient_stability: 0.9977
- nonzero_count: 14
- sparsity_ratio: 0.9838
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -411935638741014400.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000038
- coefficient_stability: 0.9977
- nonzero_count: 14
- sparsity_ratio: 0.9838
- raw_condition_number: inf
- effective_condition_number: 7875234528636.4941
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_pitch, command_pitch__lag_1, command_pitch__lag_2, command_pitch__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, command_yaw, command_yaw__lag_1, command_yaw__lag_2, command_yaw__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_z__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### pooled_backend_mode_augmented x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4651980493333.9824
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4651980493333.9824
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4651980493333.9824
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### feature_mapped_linear x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9259
- median_test_mse: 180904925590.638916
- median_test_mae: 40550.203499
- coefficient_stability: 0.8588
- nonzero_count: 50
- sparsity_ratio: 0.9020
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9259
- median_test_mse: 180906018859.258057
- median_test_mae: 40367.352480
- coefficient_stability: 0.9373
- nonzero_count: 61
- sparsity_ratio: 0.8804
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9259
- median_test_mse: 180906646706.275330
- median_test_mae: 40372.804575
- coefficient_stability: 0.8627
- nonzero_count: 50
- sparsity_ratio: 0.9020
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9241
- median_test_mse: 185341732987.346008
- median_test_mae: 44507.747924
- coefficient_stability: 0.8588
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9241
- median_test_mse: 185342543222.067993
- median_test_mae: 44290.282777
- coefficient_stability: 0.9608
- nonzero_count: 25
- sparsity_ratio: 0.9020
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9241
- median_test_mse: 185343326951.292480
- median_test_mae: 44298.597635
- coefficient_stability: 0.8588
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### feature_mapped_linear x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1218
- median_test_mse: 180906013474.262756
- median_test_mae: 40366.924313
- coefficient_stability: 0.9373
- nonzero_count: 46
- sparsity_ratio: 0.9098
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1218
- median_test_mse: 180906646706.275391
- median_test_mae: 40372.804575
- coefficient_stability: 0.8745
- nonzero_count: 50
- sparsity_ratio: 0.9020
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1218
- median_test_mse: 180907084769.305908
- median_test_mae: 40328.408386
- coefficient_stability: 0.8725
- nonzero_count: 50
- sparsity_ratio: 0.9020
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### pooled_backend_mode_augmented x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1003
- median_test_mse: 185342542690.000732
- median_test_mae: 44290.278859
- coefficient_stability: 0.9608
- nonzero_count: 18
- sparsity_ratio: 0.9294
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1003
- median_test_mse: 185343326951.292480
- median_test_mae: 44298.597635
- coefficient_stability: 0.8824
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1003
- median_test_mse: 185343633297.742767
- median_test_mae: 44232.351815
- coefficient_stability: 0.8824
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -3800810503.6385
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -3800810503.6385
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -3800810503.6385
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### feature_mapped_linear x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -12059048601.3371
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9853
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -12059048601.3371
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9853
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -45804781241376048.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9755
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -45804781241376048.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9755
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -48536911104422472.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -48536911104422472.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -48536911104422480.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### feature_mapped_linear x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -795625513633803904.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9657
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -795625513633803904.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9314
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -795625513633803904.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9314
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### feature_mapped_linear x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -795625513633804032.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 7
- sparsity_ratio: 0.9657
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -795625513633804032.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 7
- sparsity_ratio: 0.9314
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### feature_mapped_linear x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4657408978213.3945
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4657408978213.3945
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4657408978213.3945
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -12059048601.3371
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9853
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -45804781241376048.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9755
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -795625513633803904.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9657
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### pooled_backend_mode_augmented x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4651980493333.9824
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4651980493333.9824
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4651980493333.9824
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### feature_mapped_linear x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9259
- median_test_mse: 180904925590.638916
- median_test_mae: 40550.203499
- coefficient_stability: 0.8588
- nonzero_count: 50
- sparsity_ratio: 0.9020
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9259
- median_test_mse: 180906018859.258057
- median_test_mae: 40367.352480
- coefficient_stability: 0.9373
- nonzero_count: 61
- sparsity_ratio: 0.8804
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9259
- median_test_mse: 180906646706.275330
- median_test_mae: 40372.804575
- coefficient_stability: 0.8627
- nonzero_count: 50
- sparsity_ratio: 0.9020
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9241
- median_test_mse: 185341732987.346008
- median_test_mae: 44507.747924
- coefficient_stability: 0.8588
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9241
- median_test_mse: 185342543222.067993
- median_test_mae: 44290.282777
- coefficient_stability: 0.9608
- nonzero_count: 25
- sparsity_ratio: 0.9020
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9241
- median_test_mse: 185343326951.292480
- median_test_mae: 44298.597635
- coefficient_stability: 0.8588
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### feature_mapped_linear x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1218
- median_test_mse: 180906013474.262756
- median_test_mae: 40366.924313
- coefficient_stability: 0.9373
- nonzero_count: 46
- sparsity_ratio: 0.9098
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1218
- median_test_mse: 180906646706.275391
- median_test_mae: 40372.804575
- coefficient_stability: 0.8745
- nonzero_count: 50
- sparsity_ratio: 0.9020
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1218
- median_test_mse: 180907084769.305908
- median_test_mae: 40328.408386
- coefficient_stability: 0.8725
- nonzero_count: 50
- sparsity_ratio: 0.9020
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### pooled_backend_mode_augmented x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1003
- median_test_mse: 185342542690.000732
- median_test_mae: 44290.278859
- coefficient_stability: 0.9608
- nonzero_count: 18
- sparsity_ratio: 0.9294
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1003
- median_test_mse: 185343326951.292480
- median_test_mae: 44298.597635
- coefficient_stability: 0.8824
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1003
- median_test_mse: 185343633297.742767
- median_test_mae: 44232.351815
- coefficient_stability: 0.8824
- nonzero_count: 22
- sparsity_ratio: 0.9137
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -3800810503.6385
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -3800810503.6385
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -3800810503.6385
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### feature_mapped_linear x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -12059048601.3371
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9853
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -12059048601.3371
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9853
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -45804781241376048.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9755
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -45804781241376048.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9755
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -48536911104422472.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -48536911104422472.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -48536911104422480.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9706
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### feature_mapped_linear x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -795625513633803904.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9657
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -795625513633803904.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9314
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -795625513633803904.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9314
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### feature_mapped_linear x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -795625513633804032.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 7
- sparsity_ratio: 0.9657
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -795625513633804032.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 7
- sparsity_ratio: 0.9314
- raw_condition_number: inf
- effective_condition_number: 4740985034041.3750
- conditioning_pruned_features: altitude, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, yaw, yaw_rate

### feature_mapped_linear x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4657408978213.3945
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4657408978213.3945
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4657408978213.3945
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -12059048601.3371
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9853
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -45804781241376048.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000006
- coefficient_stability: 0.9755
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

### feature_mapped_linear x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -795625513633803904.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000033
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9657
- raw_condition_number: inf
- effective_condition_number: 4741198356590.9629
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, vertical_speed, yaw, yaw_rate
- conditioning_baseline_drops: backend_ardupilot__command_pitch
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, command_pitch, command_yaw, heading, pitch, position_y, position_z, roll, sq__command_pitch, sq__command_throttle, sq__command_yaw, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, yaw, yaw_rate

## Skipped
- 无。