# Schema Comparison: ardupilot_state_evolution_guided_nogps_diagnostic

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
- effective_condition_number: 557227689.1334
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
- effective_condition_number: 558973307.0566
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
- effective_condition_number: 557227689.1334
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000008
- coefficient_stability: 0.9881
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 558973307.0566
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000025
- coefficient_stability: 0.9408
- nonzero_count: 86
- sparsity_ratio: 0.8114
- raw_condition_number: inf
- effective_condition_number: 557227689.1334
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 1.0000
- median_test_mse: 0.000000
- median_test_mae: 0.000028
- coefficient_stability: 0.9464
- nonzero_count: 87
- sparsity_ratio: 0.8274
- raw_condition_number: inf
- effective_condition_number: 558973307.0566
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9126
- median_test_mse: 193597222703.510498
- median_test_mae: 33828.491597
- coefficient_stability: 0.8289
- nonzero_count: 601
- sparsity_ratio: 0.4728
- raw_condition_number: inf
- effective_condition_number: 557227689.1334
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9126
- median_test_mse: 193619178261.877258
- median_test_mae: 33955.305148
- coefficient_stability: 0.8807
- nonzero_count: 191
- sparsity_ratio: 0.8325
- raw_condition_number: inf
- effective_condition_number: 557227689.1334
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9126
- median_test_mse: 193634604609.619385
- median_test_mae: 34129.775943
- coefficient_stability: 0.8632
- nonzero_count: 245
- sparsity_ratio: 0.7851
- raw_condition_number: inf
- effective_condition_number: 557227689.1334
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9126
- median_test_mse: 193792244694.230591
- median_test_mae: 34908.879258
- coefficient_stability: 0.8024
- nonzero_count: 665
- sparsity_ratio: 0.4722
- raw_condition_number: inf
- effective_condition_number: 558973307.0566
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9125
- median_test_mse: 193821498377.901550
- median_test_mae: 35022.150390
- coefficient_stability: 0.8365
- nonzero_count: 201
- sparsity_ratio: 0.8405
- raw_condition_number: inf
- effective_condition_number: 558973307.0566
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

### full_augmented x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9125
- median_test_mse: 193840359366.266174
- median_test_mae: 35138.466792
- coefficient_stability: 0.8270
- nonzero_count: 259
- sparsity_ratio: 0.7944
- raw_condition_number: inf
- effective_condition_number: 558973307.0566
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, heading, heading__lag_1, heading__lag_2, heading__lag_3, pitch__lag_1, pitch__lag_2, pitch__lag_3, pitch_rate__lag_1, pitch_rate__lag_2, pitch_rate__lag_3, roll__lag_1, roll__lag_2, roll__lag_3, roll_rate__lag_1, roll_rate__lag_2, roll_rate__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3, yaw__lag_1, yaw__lag_2, yaw__lag_3, yaw_rate__lag_1, yaw_rate__lag_2, yaw_rate__lag_3

## Skipped
- 无。