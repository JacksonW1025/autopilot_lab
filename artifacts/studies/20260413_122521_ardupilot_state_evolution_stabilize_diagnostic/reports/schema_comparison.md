# Schema Comparison: ardupilot_state_evolution_stabilize_diagnostic

## Results
### commands_plus_state_history x selected_state_subset | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9289
- median_test_mse: 0.000000
- median_test_mae: 0.000107
- coefficient_stability: 0.8431
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7535808.5063
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9153
- median_test_mse: 189200583041.479187
- median_test_mae: 43342.890024
- coefficient_stability: 0.9176
- nonzero_count: 131
- sparsity_ratio: 0.8716
- raw_condition_number: inf
- effective_condition_number: 7535808.5063
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9153
- median_test_mse: 189228903951.085938
- median_test_mae: 43402.046282
- coefficient_stability: 0.9037
- nonzero_count: 148
- sparsity_ratio: 0.8630
- raw_condition_number: inf
- effective_condition_number: 7535808.5063
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9152
- median_test_mse: 189338778604.512390
- median_test_mae: 43893.271523
- coefficient_stability: 0.7519
- nonzero_count: 110
- sparsity_ratio: 0.8981
- raw_condition_number: inf
- effective_condition_number: 7535808.5063
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9018
- median_test_mse: 219152107088.065704
- median_test_mae: 55655.450433
- coefficient_stability: 0.7519
- nonzero_count: 110
- sparsity_ratio: 0.8981
- raw_condition_number: inf
- effective_condition_number: 7535808.5063
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9010
- median_test_mse: 221204773342.913025
- median_test_mae: 55294.796950
- coefficient_stability: 0.7725
- nonzero_count: 104
- sparsity_ratio: 0.8980
- raw_condition_number: inf
- effective_condition_number: 7535808.5063
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.7139
- median_test_mse: 0.000001
- median_test_mae: 0.000252
- coefficient_stability: 0.8431
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7535808.5063
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.6935
- median_test_mse: 0.000001
- median_test_mae: 0.000266
- coefficient_stability: 0.8148
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7535808.5063
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.6579
- median_test_mse: 0.000001
- median_test_mae: 0.000278
- coefficient_stability: 0.8148
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 7535808.5063
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2002
- median_test_mse: 0.000003
- median_test_mae: 0.000402
- coefficient_stability: 0.9931
- nonzero_count: 19
- sparsity_ratio: 0.9560
- raw_condition_number: inf
- effective_condition_number: 7535808.5063
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1971
- median_test_mse: 0.000003
- median_test_mae: 0.000404
- coefficient_stability: 1.0000
- nonzero_count: 12
- sparsity_ratio: 0.9706
- raw_condition_number: inf
- effective_condition_number: 7535808.5063
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -15700.6207
- median_test_mse: 34991234005120508.000000
- median_test_mae: 14743081.874476
- coefficient_stability: 0.7333
- nonzero_count: 104
- sparsity_ratio: 0.8980
- raw_condition_number: inf
- effective_condition_number: 7535808.5063
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

## Skipped
- 无。