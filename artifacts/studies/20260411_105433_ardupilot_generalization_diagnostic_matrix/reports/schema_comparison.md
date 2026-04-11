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
- effective_condition_number: 872717109.7904
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
- effective_condition_number: 872717109.7904
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
- effective_condition_number: 13670108.3366
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
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### full_augmented x selected_state_subset | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9942
- nonzero_count: 16
- sparsity_ratio: 0.9690
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 0.9942
- nonzero_count: 32
- sparsity_ratio: 0.9690
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000331
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 872717109.7904
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000331
- coefficient_stability: 1.0000
- nonzero_count: 32
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 872717109.7904
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000160
- coefficient_stability: 0.9695
- nonzero_count: 40
- sparsity_ratio: 0.8780
- raw_condition_number: inf
- effective_condition_number: 934140867.2301
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x window_summary_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000322
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9386
- raw_condition_number: inf
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state_history x window_summary_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000322
- coefficient_stability: 1.0000
- nonzero_count: 48
- sparsity_ratio: 0.9474
- raw_condition_number: inf
- effective_condition_number: 872717109.7904
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000002
- median_test_mae: 0.000650
- coefficient_stability: 1.0000
- nonzero_count: 32
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 872717109.7904
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000007
- median_test_mae: 0.000795
- coefficient_stability: 0.9787
- nonzero_count: 22
- sparsity_ratio: 0.9574
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000007
- median_test_mae: 0.000795
- coefficient_stability: 0.9787
- nonzero_count: 44
- sparsity_ratio: 0.9574
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000009
- median_test_mae: 0.001106
- coefficient_stability: 0.9767
- nonzero_count: 44
- sparsity_ratio: 0.9574
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000010
- median_test_mae: 0.001183
- coefficient_stability: 0.9912
- nonzero_count: 6
- sparsity_ratio: 0.9474
- raw_condition_number: inf
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000010
- median_test_mae: 0.001183
- coefficient_stability: 0.9912
- nonzero_count: 12
- sparsity_ratio: 0.9474
- raw_condition_number: inf
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x window_summary_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000011
- median_test_mae: 0.001496
- coefficient_stability: 0.9912
- nonzero_count: 12
- sparsity_ratio: 0.9474
- raw_condition_number: inf
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### full_augmented x window_summary_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000035
- median_test_mae: 0.001468
- coefficient_stability: 0.9719
- nonzero_count: 60
- sparsity_ratio: 0.9419
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000004
- median_test_mae: 0.001179
- coefficient_stability: 1.0000
- nonzero_count: 32
- sparsity_ratio: 0.8947
- raw_condition_number: inf
- effective_condition_number: 869028878.4370
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000004
- median_test_mae: 0.001174
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.7895
- raw_condition_number: inf
- effective_condition_number: 13437252.4978
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state_history x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000004
- median_test_mae: 0.001224
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 869028878.4370
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9999
- median_test_mse: 0.000005
- median_test_mae: 0.001412
- coefficient_stability: 1.0000
- nonzero_count: 8
- sparsity_ratio: 0.8947
- raw_condition_number: inf
- effective_condition_number: 13437252.4978
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### full_augmented x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9999
- median_test_mse: 0.000005
- median_test_mae: 0.001294
- coefficient_stability: 0.9512
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 934140867.2301
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9993
- median_test_mse: 0.000060
- median_test_mae: 0.004509
- coefficient_stability: 1.0000
- nonzero_count: 169
- sparsity_ratio: 0.4441
- raw_condition_number: inf
- effective_condition_number: 869028878.4370
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9991
- median_test_mse: 0.000742
- median_test_mae: 0.010157
- coefficient_stability: 0.9737
- nonzero_count: 253
- sparsity_ratio: 0.4452
- raw_condition_number: inf
- effective_condition_number: 872717109.7904
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9991
- median_test_mse: 0.000742
- median_test_mae: 0.010157
- coefficient_stability: 0.9737
- nonzero_count: 506
- sparsity_ratio: 0.4452
- raw_condition_number: inf
- effective_condition_number: 872717109.7904
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9991
- median_test_mse: 0.000742
- median_test_mae: 0.010313
- coefficient_stability: 0.9737
- nonzero_count: 509
- sparsity_ratio: 0.4419
- raw_condition_number: inf
- effective_condition_number: 872717109.7904
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9991
- median_test_mse: 0.000080
- median_test_mae: 0.005665
- coefficient_stability: 0.9695
- nonzero_count: 187
- sparsity_ratio: 0.4299
- raw_condition_number: inf
- effective_condition_number: 934140867.2301
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9988
- median_test_mse: 0.000106
- median_test_mae: 0.005651
- coefficient_stability: 0.9079
- nonzero_count: 64
- sparsity_ratio: 0.1579
- raw_condition_number: inf
- effective_condition_number: 13437252.4978
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### full_augmented x window_summary_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9985
- median_test_mse: 0.001266
- median_test_mae: 0.014064
- coefficient_stability: 0.9554
- nonzero_count: 549
- sparsity_ratio: 0.4680
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9985
- median_test_mse: 0.001267
- median_test_mae: 0.013915
- coefficient_stability: 0.9535
- nonzero_count: 271
- sparsity_ratio: 0.4748
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9985
- median_test_mse: 0.001267
- median_test_mae: 0.013915
- coefficient_stability: 0.9535
- nonzero_count: 542
- sparsity_ratio: 0.4748
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9983
- median_test_mse: 0.001464
- median_test_mae: 0.014942
- coefficient_stability: 0.9561
- nonzero_count: 88
- sparsity_ratio: 0.2281
- raw_condition_number: inf
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9983
- median_test_mse: 0.001464
- median_test_mae: 0.014942
- coefficient_stability: 0.9561
- nonzero_count: 176
- sparsity_ratio: 0.2281
- raw_condition_number: inf
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x window_summary_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9983
- median_test_mse: 0.001465
- median_test_mae: 0.015099
- coefficient_stability: 0.9561
- nonzero_count: 175
- sparsity_ratio: 0.2325
- raw_condition_number: inf
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_only x actuator_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9982
- median_test_mse: 0.000155
- median_test_mae: 0.006934
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.7500
- raw_condition_number: 1.0351
- effective_condition_number: 1.0351
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9982
- median_test_mse: 0.000155
- median_test_mae: 0.006919
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.1250
- raw_condition_number: 1.0351
- effective_condition_number: 1.0351
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9982
- median_test_mse: 0.000155
- median_test_mae: 0.006916
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.7500
- raw_condition_number: 1.0351
- effective_condition_number: 1.0351
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002564
- median_test_mae: 0.025185
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.8333
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002564
- median_test_mae: 0.025185
- coefficient_stability: 1.0000
- nonzero_count: 8
- sparsity_ratio: 0.8333
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002562
- median_test_mae: 0.025180
- coefficient_stability: 1.0000
- nonzero_count: 8
- sparsity_ratio: 0.8333
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002565
- median_test_mae: 0.025162
- coefficient_stability: 1.0000
- nonzero_count: 22
- sparsity_ratio: 0.0833
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002565
- median_test_mae: 0.025162
- coefficient_stability: 1.0000
- nonzero_count: 44
- sparsity_ratio: 0.0833
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002565
- median_test_mae: 0.025163
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.8333
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002565
- median_test_mae: 0.025163
- coefficient_stability: 1.0000
- nonzero_count: 8
- sparsity_ratio: 0.8333
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002563
- median_test_mae: 0.025157
- coefficient_stability: 1.0000
- nonzero_count: 44
- sparsity_ratio: 0.0833
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.002563
- median_test_mae: 0.025158
- coefficient_stability: 1.0000
- nonzero_count: 8
- sparsity_ratio: 0.8333
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9213
- median_test_mse: 191425030145.318909
- median_test_mae: 29880.897641
- coefficient_stability: 0.8561
- nonzero_count: 73
- sparsity_ratio: 0.7439
- raw_condition_number: inf
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9213
- median_test_mse: 191426970189.849640
- median_test_mae: 29863.199490
- coefficient_stability: 0.8737
- nonzero_count: 63
- sparsity_ratio: 0.7789
- raw_condition_number: inf
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9213
- median_test_mse: 191437546177.815338
- median_test_mae: 29839.023514
- coefficient_stability: 0.8351
- nonzero_count: 250
- sparsity_ratio: 0.1228
- raw_condition_number: inf
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state_history x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9132
- median_test_mse: 194413012850.509003
- median_test_mae: 33278.343683
- coefficient_stability: 0.8649
- nonzero_count: 255
- sparsity_ratio: 0.7763
- raw_condition_number: inf
- effective_condition_number: 872717109.7904
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9132
- median_test_mse: 194528710634.063354
- median_test_mae: 32785.791409
- coefficient_stability: 0.8504
- nonzero_count: 245
- sparsity_ratio: 0.8101
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9132
- median_test_mse: 194528971683.393921
- median_test_mae: 32757.744996
- coefficient_stability: 0.8781
- nonzero_count: 215
- sparsity_ratio: 0.8114
- raw_condition_number: inf
- effective_condition_number: 872717109.7904
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9132
- median_test_mse: 194597891236.778748
- median_test_mae: 34030.860018
- coefficient_stability: 0.8171
- nonzero_count: 308
- sparsity_ratio: 0.7612
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9131
- median_test_mse: 194777834298.753204
- median_test_mae: 32383.381883
- coefficient_stability: 0.8217
- nonzero_count: 924
- sparsity_ratio: 0.2837
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9131
- median_test_mse: 194778199057.042725
- median_test_mae: 32331.178085
- coefficient_stability: 0.8421
- nonzero_count: 843
- sparsity_ratio: 0.2605
- raw_condition_number: inf
- effective_condition_number: 872717109.7904
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0591
- median_test_mse: 194413012851.611084
- median_test_mae: 33278.343681
- coefficient_stability: 0.8649
- nonzero_count: 231
- sparsity_ratio: 0.7974
- raw_condition_number: inf
- effective_condition_number: 872717109.7904
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0588
- median_test_mse: 191425030145.348145
- median_test_mae: 29880.897641
- coefficient_stability: 0.8561
- nonzero_count: 56
- sparsity_ratio: 0.8035
- raw_condition_number: inf
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0588
- median_test_mse: 191427388902.367981
- median_test_mae: 29849.948715
- coefficient_stability: 0.8807
- nonzero_count: 44
- sparsity_ratio: 0.8456
- raw_condition_number: inf
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### commands_plus_state x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0587
- median_test_mse: 191436592401.625793
- median_test_mae: 29832.612653
- coefficient_stability: 0.8807
- nonzero_count: 137
- sparsity_ratio: 0.5193
- raw_condition_number: inf
- effective_condition_number: 13670108.3366
- conditioning_pruned_features: altitude, heading, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading

### full_augmented x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0586
- median_test_mse: 194528663636.486084
- median_test_mae: 32773.244638
- coefficient_stability: 0.8636
- nonzero_count: 200
- sparsity_ratio: 0.8450
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0586
- median_test_mse: 194528926522.023834
- median_test_mae: 32744.958295
- coefficient_stability: 0.8798
- nonzero_count: 182
- sparsity_ratio: 0.8404
- raw_condition_number: inf
- effective_condition_number: 872717109.7904
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0582
- median_test_mse: 194597891238.546204
- median_test_mae: 34030.860016
- coefficient_stability: 0.8202
- nonzero_count: 284
- sparsity_ratio: 0.7798
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0574
- median_test_mse: 194777467439.730316
- median_test_mae: 32386.952264
- coefficient_stability: 0.8698
- nonzero_count: 510
- sparsity_ratio: 0.6047
- raw_condition_number: inf
- effective_condition_number: 1034389359.5226
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, mode_guided_nogps, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0574
- median_test_mse: 194777553973.798035
- median_test_mae: 32328.800551
- coefficient_stability: 0.8807
- nonzero_count: 474
- sparsity_ratio: 0.5842
- raw_condition_number: inf
- effective_condition_number: 872717109.7904
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_only x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0006
- median_test_mse: 203258980474.736267
- median_test_mae: 29230.277825
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0006
- median_test_mse: 203259019021.690796
- median_test_mae: 29230.424661
- coefficient_stability: 0.8667
- nonzero_count: 32
- sparsity_ratio: 0.4667
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0006
- median_test_mse: 203259019021.821594
- median_test_mae: 29230.424663
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0040
- median_test_mse: 2442858698963.198242
- median_test_mae: 343464.479488
- coefficient_stability: 0.7000
- nonzero_count: 19
- sparsity_ratio: 0.6833
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0040
- median_test_mse: 2442860170611.362305
- median_test_mae: 343464.481592
- coefficient_stability: 0.7000
- nonzero_count: 58
- sparsity_ratio: 0.0333
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0040
- median_test_mse: 2442860170612.115234
- median_test_mae: 343464.481595
- coefficient_stability: 0.7000
- nonzero_count: 19
- sparsity_ratio: 0.6833
- raw_condition_number: 1.0352
- effective_condition_number: 1.0352
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000216
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000216
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000217
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9382
- median_test_mse: 0.000000
- median_test_mae: 0.000058
- coefficient_stability: 0.9211
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state x future_state_horizon | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9382
- median_test_mse: 0.000000
- median_test_mae: 0.000058
- coefficient_stability: 0.9211
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000183
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3863287.4285
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000184
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3863287.4285
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000164
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3863287.4285
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state_history x selected_state_subset | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9382
- median_test_mse: 0.000000
- median_test_mae: 0.000056
- coefficient_stability: 0.9298
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9382
- median_test_mse: 0.000000
- median_test_mae: 0.000056
- coefficient_stability: 0.9298
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x window_summary_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9382
- median_test_mse: 0.000000
- median_test_mae: 0.000058
- coefficient_stability: 0.9211
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### full_augmented x future_state_horizon | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9357
- median_test_mse: 0.000000
- median_test_mae: 0.000090
- coefficient_stability: 0.9729
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9216
- median_test_mse: 190592681155.058929
- median_test_mae: 36504.735155
- coefficient_stability: 0.8246
- nonzero_count: 22
- sparsity_ratio: 0.9228
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.9216
- median_test_mse: 190595377706.459167
- median_test_mae: 36465.590841
- coefficient_stability: 0.8614
- nonzero_count: 33
- sparsity_ratio: 0.8842
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state_history x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.9144
- median_test_mse: 191696899182.903931
- median_test_mae: 39301.820313
- coefficient_stability: 0.8605
- nonzero_count: 107
- sparsity_ratio: 0.9061
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9144
- median_test_mse: 191729557805.921631
- median_test_mae: 39400.058163
- coefficient_stability: 0.8474
- nonzero_count: 88
- sparsity_ratio: 0.9228
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.8510
- median_test_mse: 0.000000
- median_test_mae: 0.000058
- coefficient_stability: 0.9518
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.8510
- median_test_mse: 0.000000
- median_test_mae: 0.000058
- coefficient_stability: 0.9518
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x future_state_horizon | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.8078
- median_test_mse: 0.000000
- median_test_mae: 0.000064
- coefficient_stability: 0.9254
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state x window_summary_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.8078
- median_test_mse: 0.000000
- median_test_mae: 0.000064
- coefficient_stability: 0.9254
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state x selected_state_subset | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.8078
- median_test_mse: 0.000000
- median_test_mae: 0.000064
- coefficient_stability: 0.9254
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state x selected_state_subset | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.5066
- median_test_mse: 0.000001
- median_test_mae: 0.000098
- coefficient_stability: 0.9781
- nonzero_count: 3
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state x future_state_horizon | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.5066
- median_test_mse: 0.000001
- median_test_mae: 0.000098
- coefficient_stability: 0.9781
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state x window_summary_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.5066
- median_test_mse: 0.000001
- median_test_mae: 0.000098
- coefficient_stability: 0.9781
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state_history x selected_state_subset | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.5056
- median_test_mse: 0.000001
- median_test_mae: 0.000109
- coefficient_stability: 0.9759
- nonzero_count: 5
- sparsity_ratio: 0.9890
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.5056
- median_test_mse: 0.000001
- median_test_mae: 0.000109
- coefficient_stability: 0.9759
- nonzero_count: 10
- sparsity_ratio: 0.9890
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0720
- median_test_mse: 191696586033.997894
- median_test_mae: 39301.679406
- coefficient_stability: 0.8917
- nonzero_count: 100
- sparsity_ratio: 0.9123
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0719
- median_test_mse: 191725217772.105774
- median_test_mae: 39364.727551
- coefficient_stability: 0.8737
- nonzero_count: 88
- sparsity_ratio: 0.9228
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0626
- median_test_mse: 190595379911.744781
- median_test_mae: 36465.581268
- coefficient_stability: 0.8825
- nonzero_count: 30
- sparsity_ratio: 0.8947
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0626
- median_test_mse: 190596168193.784912
- median_test_mae: 36467.077980
- coefficient_stability: 0.8649
- nonzero_count: 22
- sparsity_ratio: 0.9228
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_only x next_raw_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0013
- median_test_mse: 2435870648471.074219
- median_test_mae: 341787.199910
- coefficient_stability: 0.7500
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0013
- median_test_mse: 2435875914802.075684
- median_test_mae: 341786.877532
- coefficient_stability: 0.7500
- nonzero_count: 27
- sparsity_ratio: 0.5500
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0013
- median_test_mse: 2435875914805.358398
- median_test_mae: 341786.877530
- coefficient_stability: 0.7500
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0050
- median_test_mse: 204345867299.769135
- median_test_mae: 31502.276782
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0050
- median_test_mse: 204346559283.765869
- median_test_mae: 31503.319454
- coefficient_stability: 0.8667
- nonzero_count: 16
- sparsity_ratio: 0.7333
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0050
- median_test_mse: 204346559284.412140
- median_test_mae: 31503.319456
- coefficient_stability: 0.8667
- nonzero_count: 8
- sparsity_ratio: 0.8667
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x next_raw_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -18.4398
- median_test_mse: 43652399037010.351562
- median_test_mae: 494519.076999
- coefficient_stability: 0.8096
- nonzero_count: 90
- sparsity_ratio: 0.9211
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -210.1501
- median_test_mse: 43652400285734.906250
- median_test_mae: 494519.079853
- coefficient_stability: 0.8447
- nonzero_count: 90
- sparsity_ratio: 0.9211
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_only x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -2213.0507
- median_test_mse: 0.000977
- median_test_mae: 0.016071
- coefficient_stability: 1.0000
- nonzero_count: 11
- sparsity_ratio: 0.5417
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -2213.0507
- median_test_mse: 0.000977
- median_test_mae: 0.016071
- coefficient_stability: 1.0000
- nonzero_count: 22
- sparsity_ratio: 0.5417
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -2213.0507
- median_test_mse: 0.000977
- median_test_mae: 0.016071
- coefficient_stability: 1.0000
- nonzero_count: 22
- sparsity_ratio: 0.5417
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -2231.1030
- median_test_mse: 0.000977
- median_test_mae: 0.016071
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -2231.1030
- median_test_mse: 0.000977
- median_test_mae: 0.016071
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -2231.1030
- median_test_mse: 0.000977
- median_test_mae: 0.016071
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -2231.1807
- median_test_mse: 0.000977
- median_test_mae: 0.016071
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -2231.1807
- median_test_mse: 0.000977
- median_test_mae: 0.016071
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -2231.1807
- median_test_mse: 0.000977
- median_test_mae: 0.016071
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0193
- effective_condition_number: 1.0193
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -2359.6195
- median_test_mse: 5754756867265094.000000
- median_test_mae: 5295330.009444
- coefficient_stability: 0.7965
- nonzero_count: 31
- sparsity_ratio: 0.8912
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -28279.7665
- median_test_mse: 5754775500451037.000000
- median_test_mae: 5295336.878284
- coefficient_stability: 0.8386
- nonzero_count: 31
- sparsity_ratio: 0.8912
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: heading, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### commands_plus_state_history x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000183
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 253617969.6483
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000184
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 253617969.6483
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000164
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 253617969.6483
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9382
- median_test_mse: 0.000000
- median_test_mae: 0.000056
- coefficient_stability: 0.9298
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9357
- median_test_mse: 0.000000
- median_test_mae: 0.000090
- coefficient_stability: 0.9729
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.9144
- median_test_mse: 191744510097.155457
- median_test_mae: 39561.587612
- coefficient_stability: 0.8512
- nonzero_count: 115
- sparsity_ratio: 0.9109
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.9144
- median_test_mse: 191804258596.889587
- median_test_mae: 39821.179970
- coefficient_stability: 0.8244
- nonzero_count: 94
- sparsity_ratio: 0.9271
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9141
- median_test_mse: 192418707510.583008
- median_test_mae: 41562.750983
- coefficient_stability: 0.8190
- nonzero_count: 94
- sparsity_ratio: 0.9271
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.8856
- median_test_mse: 0.000000
- median_test_mae: 0.000130
- coefficient_stability: 0.9331
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.8856
- median_test_mse: 0.000000
- median_test_mae: 0.000130
- coefficient_stability: 0.9331
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.8510
- median_test_mse: 0.000000
- median_test_mae: 0.000058
- coefficient_stability: 0.9518
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.5056
- median_test_mse: 0.000001
- median_test_mae: 0.000109
- coefficient_stability: 0.9759
- nonzero_count: 10
- sparsity_ratio: 0.9890
- raw_condition_number: inf
- effective_condition_number: 254628688.0220
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.4615
- median_test_mse: 0.000072
- median_test_mae: 0.001607
- coefficient_stability: 0.9758
- nonzero_count: 5
- sparsity_ratio: 0.9903
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000247
- coefficient_stability: 0.9817
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 253868084.3138
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000242
- coefficient_stability: 0.9832
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 253868084.3138
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000142
- coefficient_stability: 0.9939
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 253868084.3138
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9357
- median_test_mse: 0.000000
- median_test_mae: 0.000090
- coefficient_stability: 0.9729
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.8856
- median_test_mse: 0.000000
- median_test_mae: 0.000130
- coefficient_stability: 0.9331
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x future_state_horizon | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.4615
- median_test_mse: 0.000072
- median_test_mae: 0.001607
- coefficient_stability: 0.9758
- nonzero_count: 10
- sparsity_ratio: 0.9903
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x window_summary_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.4615
- median_test_mse: 0.000072
- median_test_mae: 0.001607
- coefficient_stability: 0.9758
- nonzero_count: 10
- sparsity_ratio: 0.9903
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0718
- median_test_mse: 191743332110.938904
- median_test_mae: 39573.922336
- coefficient_stability: 0.8833
- nonzero_count: 108
- sparsity_ratio: 0.9163
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0715
- median_test_mse: 191799916257.739471
- median_test_mae: 39784.989561
- coefficient_stability: 0.8574
- nonzero_count: 94
- sparsity_ratio: 0.9271
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0685
- median_test_mse: 192418701800.067047
- median_test_mae: 41562.716076
- coefficient_stability: 0.8364
- nonzero_count: 94
- sparsity_ratio: 0.9271
- raw_condition_number: inf
- effective_condition_number: 255234067.5058
- conditioning_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_guided_nogps, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: actuator_1, actuator_2, actuator_3, actuator_4, altitude__lag_1, altitude__lag_2, altitude__lag_3, control_output_pitch, control_output_roll, control_output_yaw, heading, heading__lag_1, heading__lag_2, heading__lag_3, integrator_yaw, mode_stabilize, pitch, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, position_y, position_y__lag_1, position_y__lag_2, position_y__lag_3, position_z, position_z__lag_1, position_z__lag_2, position_z__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, velocity_x, velocity_x__lag_1, velocity_x__lag_2, velocity_x__lag_3, velocity_y, velocity_y__lag_1, velocity_y__lag_2, velocity_y__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### feature_mapped_linear x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 5
- sparsity_ratio: 0.9786
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### feature_mapped_linear x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 10
- sparsity_ratio: 0.9786
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

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
- effective_condition_number: 14580096.5716
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
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000175
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.8095
- raw_condition_number: inf
- effective_condition_number: 14332694.9421
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000321
- coefficient_stability: 1.0000
- nonzero_count: 14
- sparsity_ratio: 0.9444
- raw_condition_number: inf
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000245
- coefficient_stability: 0.9615
- nonzero_count: 28
- sparsity_ratio: 0.8205
- raw_condition_number: inf
- effective_condition_number: 21366445.7282
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### feature_mapped_linear x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000004
- median_test_mae: 0.000282
- coefficient_stability: 0.9701
- nonzero_count: 32
- sparsity_ratio: 0.9316
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### feature_mapped_linear x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000009
- median_test_mae: 0.001184
- coefficient_stability: 0.9615
- nonzero_count: 14
- sparsity_ratio: 0.9402
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### feature_mapped_linear x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000009
- median_test_mae: 0.001184
- coefficient_stability: 0.9615
- nonzero_count: 28
- sparsity_ratio: 0.9402
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000010
- median_test_mae: 0.001200
- coefficient_stability: 0.9921
- nonzero_count: 7
- sparsity_ratio: 0.9444
- raw_condition_number: inf
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000010
- median_test_mae: 0.001200
- coefficient_stability: 0.9921
- nonzero_count: 14
- sparsity_ratio: 0.9444
- raw_condition_number: inf
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000657
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.8095
- raw_condition_number: inf
- effective_condition_number: 14332694.9421
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000011
- median_test_mae: 0.001508
- coefficient_stability: 0.9921
- nonzero_count: 14
- sparsity_ratio: 0.9444
- raw_condition_number: inf
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000011
- median_test_mae: 0.001487
- coefficient_stability: 0.9573
- nonzero_count: 29
- sparsity_ratio: 0.9380
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### feature_mapped_linear x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000001
- median_test_mae: 0.000717
- coefficient_stability: 0.9551
- nonzero_count: 12
- sparsity_ratio: 0.9231
- raw_condition_number: inf
- effective_condition_number: 21366445.7282
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### feature_mapped_linear x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9988
- median_test_mse: 0.000105
- median_test_mae: 0.006368
- coefficient_stability: 0.8718
- nonzero_count: 116
- sparsity_ratio: 0.2564
- raw_condition_number: inf
- effective_condition_number: 21366445.7282
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### pooled_backend_mode_augmented x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9988
- median_test_mse: 0.000106
- median_test_mae: 0.005649
- coefficient_stability: 0.9167
- nonzero_count: 63
- sparsity_ratio: 0.2500
- raw_condition_number: inf
- effective_condition_number: 14332694.9421
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001238
- median_test_mae: 0.013935
- coefficient_stability: 0.8611
- nonzero_count: 306
- sparsity_ratio: 0.3462
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### feature_mapped_linear x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001239
- median_test_mae: 0.013818
- coefficient_stability: 0.8590
- nonzero_count: 153
- sparsity_ratio: 0.3462
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### feature_mapped_linear x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9986
- median_test_mse: 0.001239
- median_test_mae: 0.013818
- coefficient_stability: 0.8590
- nonzero_count: 306
- sparsity_ratio: 0.3462
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9983
- median_test_mse: 0.001483
- median_test_mae: 0.014984
- coefficient_stability: 0.9603
- nonzero_count: 91
- sparsity_ratio: 0.2778
- raw_condition_number: inf
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9983
- median_test_mse: 0.001483
- median_test_mae: 0.014984
- coefficient_stability: 0.9603
- nonzero_count: 182
- sparsity_ratio: 0.2778
- raw_condition_number: inf
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9983
- median_test_mse: 0.001484
- median_test_mae: 0.015142
- coefficient_stability: 0.9603
- nonzero_count: 182
- sparsity_ratio: 0.2778
- raw_condition_number: inf
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9382
- median_test_mse: 0.000000
- median_test_mae: 0.000058
- coefficient_stability: 0.9286
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9382
- median_test_mse: 0.000000
- median_test_mae: 0.000058
- coefficient_stability: 0.9286
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9216
- median_test_mse: 190592681155.060059
- median_test_mae: 36504.735155
- coefficient_stability: 0.8413
- nonzero_count: 22
- sparsity_ratio: 0.9302
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9216
- median_test_mse: 190595377706.459167
- median_test_mae: 36465.590841
- coefficient_stability: 0.8746
- nonzero_count: 33
- sparsity_ratio: 0.8952
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### feature_mapped_linear x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9213
- median_test_mse: 191390869815.161713
- median_test_mae: 31256.703346
- coefficient_stability: 0.7282
- nonzero_count: 458
- sparsity_ratio: 0.2171
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### pooled_backend_mode_augmented x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9213
- median_test_mse: 191424286520.201477
- median_test_mae: 29937.996985
- coefficient_stability: 0.8635
- nonzero_count: 77
- sparsity_ratio: 0.7556
- raw_condition_number: inf
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9213
- median_test_mse: 191426463001.772217
- median_test_mae: 29884.138396
- coefficient_stability: 0.8730
- nonzero_count: 65
- sparsity_ratio: 0.7937
- raw_condition_number: inf
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9213
- median_test_mse: 191437538144.188721
- median_test_mae: 29838.997213
- coefficient_stability: 0.8444
- nonzero_count: 260
- sparsity_ratio: 0.1746
- raw_condition_number: inf
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9213
- median_test_mse: 191542326516.653381
- median_test_mae: 31707.550407
- coefficient_stability: 0.8188
- nonzero_count: 115
- sparsity_ratio: 0.8034
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### feature_mapped_linear x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9212
- median_test_mse: 191675241604.784302
- median_test_mae: 32043.817336
- coefficient_stability: 0.7880
- nonzero_count: 153
- sparsity_ratio: 0.7385
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### feature_mapped_linear x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0590
- median_test_mse: 191389832288.236298
- median_test_mae: 31251.128529
- coefficient_stability: 0.8444
- nonzero_count: 232
- sparsity_ratio: 0.6034
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### pooled_backend_mode_augmented x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0588
- median_test_mse: 191424286520.210724
- median_test_mae: 29937.996985
- coefficient_stability: 0.8635
- nonzero_count: 60
- sparsity_ratio: 0.8095
- raw_condition_number: inf
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0588
- median_test_mse: 191426880930.359009
- median_test_mae: 29870.987004
- coefficient_stability: 0.8794
- nonzero_count: 44
- sparsity_ratio: 0.8603
- raw_condition_number: inf
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### pooled_backend_mode_augmented x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0587
- median_test_mse: 191436578905.701843
- median_test_mae: 29832.569167
- coefficient_stability: 0.8857
- nonzero_count: 143
- sparsity_ratio: 0.5460
- raw_condition_number: inf
- effective_condition_number: 14580096.5716
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, vertical_speed
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading

### feature_mapped_linear x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0582
- median_test_mse: 191543305563.137634
- median_test_mae: 31689.655104
- coefficient_stability: 0.8410
- nonzero_count: 82
- sparsity_ratio: 0.8598
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### feature_mapped_linear x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0576
- median_test_mse: 191675241604.849121
- median_test_mae: 32043.817335
- coefficient_stability: 0.7880
- nonzero_count: 136
- sparsity_ratio: 0.7675
- raw_condition_number: inf
- effective_condition_number: 21735045.9424
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, sq__roll, vertical_speed
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, sq__roll

### pooled_backend_mode_augmented x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000183
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3863287.4285
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000184
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3863287.4285
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000164
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3863287.4285
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9382
- median_test_mse: 0.000000
- median_test_mae: 0.000058
- coefficient_stability: 0.9286
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### feature_mapped_linear x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9206
- median_test_mse: 193093373085.555084
- median_test_mae: 39426.185454
- coefficient_stability: 0.8256
- nonzero_count: 64
- sparsity_ratio: 0.8906
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9203
- median_test_mse: 193803811487.677856
- median_test_mae: 40530.705268
- coefficient_stability: 0.8145
- nonzero_count: 50
- sparsity_ratio: 0.9145
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.8078
- median_test_mse: 0.000000
- median_test_mae: 0.000064
- coefficient_stability: 0.9325
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.8078
- median_test_mse: 0.000000
- median_test_mae: 0.000064
- coefficient_stability: 0.9325
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.8078
- median_test_mse: 0.000000
- median_test_mae: 0.000064
- coefficient_stability: 0.9325
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5066
- median_test_mse: 0.000001
- median_test_mae: 0.000098
- coefficient_stability: 0.9802
- nonzero_count: 3
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5066
- median_test_mse: 0.000001
- median_test_mae: 0.000098
- coefficient_stability: 0.9802
- nonzero_count: 6
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5066
- median_test_mse: 0.000001
- median_test_mae: 0.000098
- coefficient_stability: 0.9802
- nonzero_count: 6
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### feature_mapped_linear x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5062
- median_test_mse: 0.000001
- median_test_mae: 0.000214
- coefficient_stability: 0.9722
- nonzero_count: 6
- sparsity_ratio: 0.9744
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5062
- median_test_mse: 0.000001
- median_test_mae: 0.000214
- coefficient_stability: 0.9722
- nonzero_count: 12
- sparsity_ratio: 0.9744
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0626
- median_test_mse: 190595379911.744781
- median_test_mae: 36465.581268
- coefficient_stability: 0.8937
- nonzero_count: 30
- sparsity_ratio: 0.9048
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0626
- median_test_mse: 190596168193.786011
- median_test_mae: 36467.077980
- coefficient_stability: 0.8778
- nonzero_count: 22
- sparsity_ratio: 0.9302
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### feature_mapped_linear x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0505
- median_test_mse: 193056179603.661285
- median_test_mae: 39427.495512
- coefficient_stability: 0.8769
- nonzero_count: 56
- sparsity_ratio: 0.9043
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0468
- median_test_mse: 193801008331.462402
- median_test_mae: 40485.649396
- coefficient_stability: 0.8496
- nonzero_count: 50
- sparsity_ratio: 0.9145
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -25.8379
- median_test_mse: 0.000160
- median_test_mae: 0.001168
- coefficient_stability: 0.9274
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -25.8379
- median_test_mse: 0.000160
- median_test_mae: 0.001168
- coefficient_stability: 0.9274
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -25.9490
- median_test_mse: 0.000161
- median_test_mae: 0.001309
- coefficient_stability: 0.9338
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -25.9490
- median_test_mse: 0.000161
- median_test_mae: 0.001309
- coefficient_stability: 0.9338
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -2359.6195
- median_test_mse: 5754756867265094.000000
- median_test_mae: 5295330.009444
- coefficient_stability: 0.8159
- nonzero_count: 31
- sparsity_ratio: 0.9016
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### pooled_backend_mode_augmented x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -28279.7665
- median_test_mse: 5754775500451037.000000
- median_test_mae: 5295336.878284
- coefficient_stability: 0.8540
- nonzero_count: 31
- sparsity_ratio: 0.9016
- raw_condition_number: inf
- effective_condition_number: 3912283.1118
- conditioning_pruned_features: altitude, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: mode_guided_nogps
- conditioning_extra_pruned_features: heading, mode_stabilize, pitch, position_y, position_z, velocity_x, velocity_y, yaw

### feature_mapped_linear x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -54731.2839
- median_test_mse: 133427268372945712.000000
- median_test_mae: 25379224.601501
- coefficient_stability: 0.7692
- nonzero_count: 66
- sparsity_ratio: 0.8872
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -655702.2195
- median_test_mse: 133427250500788592.000000
- median_test_mae: 25379221.004673
- coefficient_stability: 0.8068
- nonzero_count: 66
- sparsity_ratio: 0.8872
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000317
- coefficient_stability: 0.9615
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8672352.0509
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000246
- coefficient_stability: 0.9904
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8672352.0509
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: nan
- median_test_mse: 0.000000
- median_test_mae: 0.000167
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8672352.0509
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5062
- median_test_mse: 0.000001
- median_test_mae: 0.000214
- coefficient_stability: 0.9722
- nonzero_count: 12
- sparsity_ratio: 0.9744
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -25.8379
- median_test_mse: 0.000160
- median_test_mae: 0.001168
- coefficient_stability: 0.9274
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

### feature_mapped_linear x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -25.9490
- median_test_mse: 0.000161
- median_test_mae: 0.001309
- coefficient_stability: 0.9338
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 8750228.4520
- conditioning_pruned_features: altitude, backend_ardupilot__command_pitch, backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_guided_nogps, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, vertical_speed, yaw
- conditioning_baseline_drops: backend_ardupilot__command_pitch, mode_guided_nogps
- conditioning_extra_pruned_features: backend_ardupilot__command_roll, backend_ardupilot__command_throttle, backend_ardupilot__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, heading, mode_stabilize, pitch, position_y, position_z, sq__pitch, sq__pitch_rate, sq__roll, sq__roll_rate, sq__yaw, sq__yaw_rate, velocity_x, velocity_y, yaw

## Skipped
- 无。