# Schema Comparison: ardupilot_state_evolution_guided_nogps_baseline

## Results
### commands_plus_state_history x selected_state_subset | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 1601897234.1406
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ols_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000000
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 1607623878.9328
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000002
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 1601897234.1406
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000024
- coefficient_stability: 0.9841
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 1607623878.9328
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000048
- coefficient_stability: 0.9474
- nonzero_count: 55
- sparsity_ratio: 0.8794
- raw_condition_number: inf
- effective_condition_number: 1601897234.1406
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000050
- coefficient_stability: 0.9524
- nonzero_count: 54
- sparsity_ratio: 0.8929
- raw_condition_number: inf
- effective_condition_number: 1607623878.9328
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9168
- median_test_mse: 185946435552.130981
- median_test_mae: 39127.090264
- coefficient_stability: 0.8439
- nonzero_count: 188
- sparsity_ratio: 0.8351
- raw_condition_number: inf
- effective_condition_number: 1601897234.1406
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9168
- median_test_mse: 186003964617.350952
- median_test_mae: 39661.678745
- coefficient_stability: 0.8123
- nonzero_count: 237
- sparsity_ratio: 0.7921
- raw_condition_number: inf
- effective_condition_number: 1601897234.1406
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9168
- median_test_mse: 186114033984.900574
- median_test_mae: 39783.193162
- coefficient_stability: 0.8056
- nonzero_count: 202
- sparsity_ratio: 0.8397
- raw_condition_number: inf
- effective_condition_number: 1607623878.9328
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9167
- median_test_mse: 186255544185.176025
- median_test_mae: 37918.470526
- coefficient_stability: 0.7596
- nonzero_count: 618
- sparsity_ratio: 0.4579
- raw_condition_number: inf
- effective_condition_number: 1601897234.1406
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9166
- median_test_mse: 186545220849.071045
- median_test_mae: 41692.606171
- coefficient_stability: 0.7817
- nonzero_count: 252
- sparsity_ratio: 0.8000
- raw_condition_number: inf
- effective_condition_number: 1607623878.9328
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9165
- median_test_mse: 186611619884.797699
- median_test_mae: 39141.747728
- coefficient_stability: 0.7452
- nonzero_count: 664
- sparsity_ratio: 0.4730
- raw_condition_number: inf
- effective_condition_number: 1607623878.9328
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

## Skipped
- 无。