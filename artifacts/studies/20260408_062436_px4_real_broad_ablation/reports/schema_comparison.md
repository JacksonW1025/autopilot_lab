# Schema Comparison: px4_real_broad_ablation

## Results
### full_augmented x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9996
- median_test_mse: 0.000085
- median_test_mae: 0.004353
- coefficient_stability: 0.7844
- nonzero_count: 423
- sparsity_ratio: 0.6867
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9994
- median_test_mse: 0.000133
- median_test_mae: 0.004308
- coefficient_stability: 0.7404
- nonzero_count: 394
- sparsity_ratio: 0.6544
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9993
- median_test_mse: 0.000143
- median_test_mae: 0.006718
- coefficient_stability: 0.9630
- nonzero_count: 58
- sparsity_ratio: 0.9570
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9992
- median_test_mse: 0.000094
- median_test_mae: 0.003983
- coefficient_stability: 0.7667
- nonzero_count: 298
- sparsity_ratio: 0.7241
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9991
- median_test_mse: 0.000185
- median_test_mae: 0.006453
- coefficient_stability: 0.9667
- nonzero_count: 57
- sparsity_ratio: 0.9500
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9991
- median_test_mse: 0.000113
- median_test_mae: 0.004437
- coefficient_stability: 0.9787
- nonzero_count: 17
- sparsity_ratio: 0.9843
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9991
- median_test_mse: 0.000201
- median_test_mae: 0.007903
- coefficient_stability: 0.9822
- nonzero_count: 782
- sparsity_ratio: 0.4207
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9988
- median_test_mse: 0.000249
- median_test_mae: 0.007838
- coefficient_stability: 0.9825
- nonzero_count: 657
- sparsity_ratio: 0.4237
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9988
- median_test_mse: 0.000146
- median_test_mae: 0.005030
- coefficient_stability: 0.9898
- nonzero_count: 424
- sparsity_ratio: 0.6074
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9988
- median_test_mse: 0.000149
- median_test_mae: 0.005413
- coefficient_stability: 0.7278
- nonzero_count: 181
- sparsity_ratio: 0.6648
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9987
- median_test_mse: 0.000164
- median_test_mae: 0.003911
- coefficient_stability: 0.7018
- nonzero_count: 276
- sparsity_ratio: 0.6974
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9985
- median_test_mse: 0.000178
- median_test_mae: 0.005975
- coefficient_stability: 0.9685
- nonzero_count: 10
- sparsity_ratio: 0.9815
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9985
- median_test_mse: 0.000189
- median_test_mae: 0.004323
- coefficient_stability: 0.9737
- nonzero_count: 19
- sparsity_ratio: 0.9792
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.9984
- median_test_mse: 0.000142
- median_test_mae: 0.004719
- coefficient_stability: 0.5728
- nonzero_count: 211
- sparsity_ratio: 0.8149
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9981
- median_test_mse: 0.000230
- median_test_mae: 0.006765
- coefficient_stability: 0.9870
- nonzero_count: 232
- sparsity_ratio: 0.5704
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9981
- median_test_mse: 0.000231
- median_test_mae: 0.005181
- coefficient_stability: 0.9912
- nonzero_count: 371
- sparsity_ratio: 0.5932
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9978
- median_test_mse: 0.000268
- median_test_mae: 0.005400
- coefficient_stability: 0.6645
- nonzero_count: 161
- sparsity_ratio: 0.6469
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.000180
- median_test_mae: 0.006130
- coefficient_stability: 0.6111
- nonzero_count: 216
- sparsity_ratio: 0.8400
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9975
- median_test_mse: 0.000306
- median_test_mae: 0.005918
- coefficient_stability: 0.9627
- nonzero_count: 10
- sparsity_ratio: 0.9781
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9974
- median_test_mse: 0.000262
- median_test_mae: 0.008927
- coefficient_stability: 0.9075
- nonzero_count: 22
- sparsity_ratio: 0.9807
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9973
- median_test_mse: 0.000327
- median_test_mae: 0.008083
- coefficient_stability: 0.7046
- nonzero_count: 397
- sparsity_ratio: 0.6324
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.000372
- median_test_mae: 0.007005
- coefficient_stability: 0.9890
- nonzero_count: 207
- sparsity_ratio: 0.5461
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9969
- median_test_mse: 0.000379
- median_test_mae: 0.008886
- coefficient_stability: 0.9509
- nonzero_count: 28
- sparsity_ratio: 0.9741
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9966
- median_test_mse: 0.000410
- median_test_mae: 0.009210
- coefficient_stability: 0.9769
- nonzero_count: 528
- sparsity_ratio: 0.5111
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x next_raw_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9966
- median_test_mse: 0.000744
- median_test_mae: 0.011272
- coefficient_stability: 0.7965
- nonzero_count: 76
- sparsity_ratio: 0.7333
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x window_summary_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9965
- median_test_mse: 0.000420
- median_test_mae: 0.008658
- coefficient_stability: 0.6634
- nonzero_count: 376
- sparsity_ratio: 0.5877
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x next_raw_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9965
- median_test_mse: 0.000756
- median_test_mae: 0.011311
- coefficient_stability: 0.9825
- nonzero_count: 241
- sparsity_ratio: 0.1544
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9965
- median_test_mse: 0.000763
- median_test_mae: 0.011572
- coefficient_stability: 0.9825
- nonzero_count: 17
- sparsity_ratio: 0.9404
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x next_raw_state | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9963
- median_test_mse: 0.000337
- median_test_mae: 0.010623
- coefficient_stability: 0.8941
- nonzero_count: 22
- sparsity_ratio: 0.9837
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9962
- median_test_mse: 0.000424
- median_test_mae: 0.009544
- coefficient_stability: 0.9110
- nonzero_count: 187
- sparsity_ratio: 0.8360
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9962
- median_test_mse: 0.000462
- median_test_mae: 0.009247
- coefficient_stability: 0.9539
- nonzero_count: 25
- sparsity_ratio: 0.9726
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9958
- median_test_mse: 0.000507
- median_test_mae: 0.009598
- coefficient_stability: 0.9792
- nonzero_count: 443
- sparsity_ratio: 0.5143
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x next_raw_state | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9958
- median_test_mse: 0.000557
- median_test_mae: 0.011377
- coefficient_stability: 0.9386
- nonzero_count: 10
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state x next_raw_state | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.9958
- median_test_mse: 0.000560
- median_test_mae: 0.011096
- coefficient_stability: 0.7018
- nonzero_count: 61
- sparsity_ratio: 0.7860
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### full_augmented x next_raw_state | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9958
- median_test_mse: 0.000469
- median_test_mae: 0.010234
- coefficient_stability: 0.9070
- nonzero_count: 239
- sparsity_ratio: 0.8230
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x next_raw_state | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9954
- median_test_mse: 0.000645
- median_test_mae: 0.011266
- coefficient_stability: 0.9404
- nonzero_count: 137
- sparsity_ratio: 0.5193
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9927
- median_test_mse: 0.000890
- median_test_mae: 0.010150
- coefficient_stability: 0.7982
- nonzero_count: 46
- sparsity_ratio: 0.7982
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x future_state_horizon | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9926
- median_test_mse: 0.000899
- median_test_mae: 0.010177
- coefficient_stability: 0.9912
- nonzero_count: 178
- sparsity_ratio: 0.2193
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x future_state_horizon | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9926
- median_test_mse: 0.000902
- median_test_mae: 0.010278
- coefficient_stability: 0.9912
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x window_summary_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9912
- median_test_mse: 0.001054
- median_test_mae: 0.013199
- coefficient_stability: 0.7895
- nonzero_count: 51
- sparsity_ratio: 0.7763
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x window_summary_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9912
- median_test_mse: 0.001055
- median_test_mae: 0.013200
- coefficient_stability: 0.9912
- nonzero_count: 186
- sparsity_ratio: 0.1842
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x window_summary_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9912
- median_test_mse: 0.001059
- median_test_mae: 0.013313
- coefficient_stability: 0.9912
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9885
- median_test_mse: 0.001399
- median_test_mae: 0.013359
- coefficient_stability: 0.7982
- nonzero_count: 23
- sparsity_ratio: 0.7982
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9884
- median_test_mse: 0.001415
- median_test_mae: 0.013447
- coefficient_stability: 0.9912
- nonzero_count: 94
- sparsity_ratio: 0.1754
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9883
- median_test_mse: 0.001418
- median_test_mae: 0.013553
- coefficient_stability: 0.9912
- nonzero_count: 3
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x delta_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9311
- median_test_mse: 0.000085
- median_test_mae: 0.004353
- coefficient_stability: 0.7844
- nonzero_count: 421
- sparsity_ratio: 0.6881
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9104
- median_test_mse: 0.000110
- median_test_mae: 0.005426
- coefficient_stability: 0.9711
- nonzero_count: 27
- sparsity_ratio: 0.9800
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.8923
- median_test_mse: 0.000133
- median_test_mae: 0.004308
- coefficient_stability: 0.7404
- nonzero_count: 392
- sparsity_ratio: 0.6561
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.8859
- median_test_mse: 0.000286
- median_test_mae: 0.005704
- coefficient_stability: 0.9627
- nonzero_count: 53
- sparsity_ratio: 0.9419
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.8731
- median_test_mse: 0.000156
- median_test_mae: 0.005274
- coefficient_stability: 0.9754
- nonzero_count: 29
- sparsity_ratio: 0.9746
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.8690
- median_test_mse: 0.000300
- median_test_mae: 0.006003
- coefficient_stability: 0.9639
- nonzero_count: 70
- sparsity_ratio: 0.9352
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.8646
- median_test_mse: 0.000166
- median_test_mae: 0.006638
- coefficient_stability: 0.9911
- nonzero_count: 543
- sparsity_ratio: 0.5978
- raw_condition_number: inf
- effective_condition_number: 1039336.3683
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.8546
- median_test_mse: 0.000173
- median_test_mae: 0.005125
- coefficient_stability: 0.9391
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.8277
- median_test_mse: 0.000212
- median_test_mae: 0.006556
- coefficient_stability: 0.9956
- nonzero_count: 468
- sparsity_ratio: 0.5895
- raw_condition_number: inf
- effective_condition_number: 996260.5635
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.8157
- median_test_mse: 0.000419
- median_test_mae: 0.007559
- coefficient_stability: 0.9507
- nonzero_count: 33
- sparsity_ratio: 0.9276
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.8091
- median_test_mse: 0.000188
- median_test_mae: 0.005600
- coefficient_stability: 0.9296
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.7918
- median_test_mse: 0.000424
- median_test_mae: 0.007725
- coefficient_stability: 0.9537
- nonzero_count: 43
- sparsity_ratio: 0.9204
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x future_state_horizon | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.7714
- median_test_mse: 0.000459
- median_test_mae: 0.007461
- coefficient_stability: 0.9649
- nonzero_count: 66
- sparsity_ratio: 0.7105
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state_history x selected_state_subset | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.7639
- median_test_mse: 0.000262
- median_test_mae: 0.006818
- coefficient_stability: 0.9200
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x future_state_horizon | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.7356
- median_test_mse: 0.000483
- median_test_mae: 0.008071
- coefficient_stability: 0.9496
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state x future_state_horizon | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.7214
- median_test_mse: 0.000525
- median_test_mae: 0.008471
- coefficient_stability: 0.7149
- nonzero_count: 43
- sparsity_ratio: 0.8114
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### full_augmented x selected_state_subset | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.6994
- median_test_mse: 0.000272
- median_test_mae: 0.007286
- coefficient_stability: 0.9130
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x selected_state_subset | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.6490
- median_test_mse: 0.000727
- median_test_mae: 0.010009
- coefficient_stability: 0.9474
- nonzero_count: 39
- sparsity_ratio: 0.6579
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state x selected_state_subset | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.6000
- median_test_mse: 0.000765
- median_test_mae: 0.010710
- coefficient_stability: 0.9342
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state x selected_state_subset | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.5774
- median_test_mse: 0.000827
- median_test_mae: 0.011189
- coefficient_stability: 0.6974
- nonzero_count: 23
- sparsity_ratio: 0.7982
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state_history x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.5610
- median_test_mse: 0.055539
- median_test_mae: 0.176840
- coefficient_stability: 0.7664
- nonzero_count: 167
- sparsity_ratio: 0.4507
- raw_condition_number: inf
- effective_condition_number: 994010.4089
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.5609
- median_test_mse: 0.055550
- median_test_mae: 0.177099
- coefficient_stability: 0.8487
- nonzero_count: 256
- sparsity_ratio: 0.1579
- raw_condition_number: inf
- effective_condition_number: 994010.4089
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.5535
- median_test_mse: 0.000151
- median_test_mae: 0.003899
- coefficient_stability: 0.5927
- nonzero_count: 151
- sparsity_ratio: 0.8344
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.5497
- median_test_mse: 0.056959
- median_test_mae: 0.180142
- coefficient_stability: 0.6316
- nonzero_count: 48
- sparsity_ratio: 0.3684
- raw_condition_number: inf
- effective_condition_number: 438807.4263
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.5483
- median_test_mse: 0.057138
- median_test_mae: 0.180771
- coefficient_stability: 0.8421
- nonzero_count: 36
- sparsity_ratio: 0.5263
- raw_condition_number: inf
- effective_condition_number: 438807.4263
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.5478
- median_test_mse: 0.057197
- median_test_mae: 0.180869
- coefficient_stability: 0.8421
- nonzero_count: 68
- sparsity_ratio: 0.1053
- raw_condition_number: inf
- effective_condition_number: 438807.4263
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x delta_state | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.5418
- median_test_mse: 0.000150
- median_test_mae: 0.006504
- coefficient_stability: 0.9215
- nonzero_count: 8
- sparsity_ratio: 0.9930
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.5326
- median_test_mse: 0.059120
- median_test_mae: 0.183878
- coefficient_stability: 0.1414
- nonzero_count: 250
- sparsity_ratio: 0.1776
- raw_condition_number: inf
- effective_condition_number: 994010.4089
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.4993
- median_test_mse: 0.000213
- median_test_mae: 0.007141
- coefficient_stability: 0.9636
- nonzero_count: 77
- sparsity_ratio: 0.9325
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.4873
- median_test_mse: 0.000166
- median_test_mae: 0.004827
- coefficient_stability: 0.6241
- nonzero_count: 160
- sparsity_ratio: 0.8519
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.4653
- median_test_mse: 0.000142
- median_test_mae: 0.004719
- coefficient_stability: 0.5728
- nonzero_count: 211
- sparsity_ratio: 0.8149
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x window_summary_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.4292
- median_test_mse: 0.000545
- median_test_mae: 0.010569
- coefficient_stability: 0.9430
- nonzero_count: 86
- sparsity_ratio: 0.6228
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### full_augmented x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.4053
- median_test_mse: 0.075235
- median_test_mae: 0.189291
- coefficient_stability: 0.5698
- nonzero_count: 161
- sparsity_ratio: 0.5320
- raw_condition_number: inf
- effective_condition_number: 1010019.6908
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.3937
- median_test_mse: 0.000744
- median_test_mae: 0.011272
- coefficient_stability: 0.7965
- nonzero_count: 63
- sparsity_ratio: 0.7789
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.3859
- median_test_mse: 0.075817
- median_test_mae: 0.233946
- coefficient_stability: 0.8438
- nonzero_count: 4
- sparsity_ratio: 0.7500
- raw_condition_number: inf
- effective_condition_number: 327796.8804
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_only x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.3859
- median_test_mse: 0.075819
- median_test_mae: 0.233970
- coefficient_stability: 0.9062
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 327796.8804
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.3815
- median_test_mse: 0.000759
- median_test_mae: 0.011266
- coefficient_stability: 0.9825
- nonzero_count: 230
- sparsity_ratio: 0.1930
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.3801
- median_test_mse: 0.076535
- median_test_mae: 0.234568
- coefficient_stability: 0.0000
- nonzero_count: 16
- sparsity_ratio: 0.0000
- raw_condition_number: inf
- effective_condition_number: 327796.8804
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.3780
- median_test_mse: 0.000763
- median_test_mae: 0.011465
- coefficient_stability: 0.9825
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 439711.6289
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.3769
- median_test_mse: 0.078821
- median_test_mae: 0.194932
- coefficient_stability: 0.7209
- nonzero_count: 283
- sparsity_ratio: 0.1773
- raw_condition_number: inf
- effective_condition_number: 1010019.6908
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.3690
- median_test_mse: 0.000445
- median_test_mae: 0.009698
- coefficient_stability: 0.9474
- nonzero_count: 73
- sparsity_ratio: 0.9200
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.3592
- median_test_mse: 0.000586
- median_test_mae: 0.011337
- coefficient_stability: 0.9298
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### full_augmented x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.3492
- median_test_mse: 0.000230
- median_test_mae: 0.007877
- coefficient_stability: 0.9574
- nonzero_count: 102
- sparsity_ratio: 0.9244
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.3474
- median_test_mse: 0.000612
- median_test_mae: 0.011641
- coefficient_stability: 0.6952
- nonzero_count: 41
- sparsity_ratio: 0.8202
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### full_augmented x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.3422
- median_test_mse: 0.083214
- median_test_mae: 0.192496
- coefficient_stability: 0.1163
- nonzero_count: 264
- sparsity_ratio: 0.2326
- raw_condition_number: inf
- effective_condition_number: 1010019.6908
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, config_profile_px4_real_posctl_nominal, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_only x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2919
- median_test_mse: 0.013783
- median_test_mae: 0.028251
- coefficient_stability: 0.9271
- nonzero_count: 10
- sparsity_ratio: 0.7917
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_only x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2917
- median_test_mse: 0.013783
- median_test_mae: 0.028271
- coefficient_stability: 0.9062
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_only x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2910
- median_test_mse: 0.013868
- median_test_mae: 0.028414
- coefficient_stability: 0.0938
- nonzero_count: 40
- sparsity_ratio: 0.1667
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_only x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2899
- median_test_mse: 0.013969
- median_test_mae: 0.027877
- coefficient_stability: 0.9375
- nonzero_count: 8
- sparsity_ratio: 0.6667
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### full_augmented x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2899
- median_test_mse: 0.000475
- median_test_mae: 0.009071
- coefficient_stability: 0.9463
- nonzero_count: 98
- sparsity_ratio: 0.9093
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_only x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2898
- median_test_mse: 0.013969
- median_test_mae: 0.027898
- coefficient_stability: 0.9167
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_only x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2896
- median_test_mse: 0.014039
- median_test_mae: 0.028017
- coefficient_stability: 0.1042
- nonzero_count: 20
- sparsity_ratio: 0.1667
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state_history x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2885
- median_test_mse: 0.000402
- median_test_mae: 0.009624
- coefficient_stability: 0.8931
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_only x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2881
- median_test_mse: 0.013869
- median_test_mae: 0.027922
- coefficient_stability: 0.9375
- nonzero_count: 16
- sparsity_ratio: 0.6667
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_only x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2879
- median_test_mse: 0.013869
- median_test_mae: 0.027943
- coefficient_stability: 0.9271
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_only x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2877
- median_test_mse: 0.013937
- median_test_mae: 0.028062
- coefficient_stability: 0.1042
- nonzero_count: 40
- sparsity_ratio: 0.1667
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### full_augmented x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2704
- median_test_mse: 0.000194
- median_test_mae: 0.007873
- coefficient_stability: 0.9078
- nonzero_count: 8
- sparsity_ratio: 0.9941
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2340
- median_test_mse: 0.000253
- median_test_mae: 0.005494
- coefficient_stability: 0.5581
- nonzero_count: 79
- sparsity_ratio: 0.8268
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2320
- median_test_mse: 0.000180
- median_test_mae: 0.006130
- coefficient_stability: 0.6111
- nonzero_count: 216
- sparsity_ratio: 0.8400
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1697
- median_test_mse: 0.000263
- median_test_mae: 0.006700
- coefficient_stability: 0.5917
- nonzero_count: 84
- sparsity_ratio: 0.8444
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.1355
- median_test_mse: 0.000445
- median_test_mae: 0.009199
- coefficient_stability: 0.8861
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_only x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0376
- median_test_mse: 0.000562
- median_test_mae: 0.008320
- coefficient_stability: 1.0000
- nonzero_count: 9
- sparsity_ratio: 0.8500
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_only x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0375
- median_test_mse: 0.000562
- median_test_mae: 0.008323
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_only x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0362
- median_test_mse: 0.117240
- median_test_mae: 0.155457
- coefficient_stability: 1.0000
- nonzero_count: 16
- sparsity_ratio: 0.3333
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0362
- median_test_mse: 0.117240
- median_test_mae: 0.155457
- coefficient_stability: 1.0000
- nonzero_count: 1
- sparsity_ratio: 0.9583
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0358
- median_test_mse: 0.117154
- median_test_mae: 0.155037
- coefficient_stability: 1.0000
- nonzero_count: 33
- sparsity_ratio: 0.3125
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0358
- median_test_mse: 0.117154
- median_test_mae: 0.155037
- coefficient_stability: 1.0000
- nonzero_count: 2
- sparsity_ratio: 0.9583
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0354
- median_test_mse: 0.000563
- median_test_mae: 0.008351
- coefficient_stability: 0.1250
- nonzero_count: 45
- sparsity_ratio: 0.2500
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_only x window_summary_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0348
- median_test_mse: 0.115894
- median_test_mae: 0.155682
- coefficient_stability: 1.0000
- nonzero_count: 32
- sparsity_ratio: 0.3333
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0347
- median_test_mse: 0.115894
- median_test_mae: 0.155685
- coefficient_stability: 1.0000
- nonzero_count: 2
- sparsity_ratio: 0.9583
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0341
- median_test_mse: 0.117492
- median_test_mae: 0.155545
- coefficient_stability: 0.2500
- nonzero_count: 19
- sparsity_ratio: 0.2083
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0337
- median_test_mse: 0.117404
- median_test_mae: 0.155116
- coefficient_stability: 0.2500
- nonzero_count: 38
- sparsity_ratio: 0.2083
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0327
- median_test_mse: 0.116134
- median_test_mae: 0.155764
- coefficient_stability: 0.2500
- nonzero_count: 38
- sparsity_ratio: 0.2083
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0199
- median_test_mse: 0.001199
- median_test_mae: 0.013516
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0198
- median_test_mse: 0.001200
- median_test_mae: 0.013511
- coefficient_stability: 1.0000
- nonzero_count: 34
- sparsity_ratio: 0.4333
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0183
- median_test_mse: 0.001201
- median_test_mae: 0.013535
- coefficient_stability: 0.2500
- nonzero_count: 45
- sparsity_ratio: 0.2500
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0016
- median_test_mse: 0.126263
- median_test_mae: 0.345131
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 342443.2500
- effective_condition_number: 342443.2500
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0016
- median_test_mse: 0.126263
- median_test_mae: 0.345132
- coefficient_stability: 1.0000
- nonzero_count: 8
- sparsity_ratio: 0.5000
- raw_condition_number: 342443.2500
- effective_condition_number: 342443.2500
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0003
- median_test_mse: 0.126499
- median_test_mae: 0.345383
- coefficient_stability: 0.2500
- nonzero_count: 12
- sparsity_ratio: 0.2500
- raw_condition_number: 342443.2500
- effective_condition_number: 342443.2500
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0435
- median_test_mse: 0.000475
- median_test_mae: 0.009844
- coefficient_stability: 0.9561
- nonzero_count: 120
- sparsity_ratio: 0.5789
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state_history x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0498
- median_test_mse: 0.000442
- median_test_mae: 0.009384
- coefficient_stability: 0.5395
- nonzero_count: 164
- sparsity_ratio: 0.8202
- raw_condition_number: inf
- effective_condition_number: 913354.2145
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -0.1748
- median_test_mse: 0.000530
- median_test_mae: 0.010760
- coefficient_stability: 0.9404
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.2143
- median_test_mse: 0.000560
- median_test_mae: 0.011096
- coefficient_stability: 0.7018
- nonzero_count: 51
- sparsity_ratio: 0.8211
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### full_augmented x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.4185
- median_test_mse: 0.174651
- median_test_mae: 0.272745
- coefficient_stability: 0.1323
- nonzero_count: 175
- sparsity_ratio: 0.4913
- raw_condition_number: inf
- effective_condition_number: 924317.3671
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -0.4298
- median_test_mse: 0.176134
- median_test_mae: 0.286320
- coefficient_stability: 0.5233
- nonzero_count: 11
- sparsity_ratio: 0.9680
- raw_condition_number: inf
- effective_condition_number: 924317.3671
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.5442
- median_test_mse: 0.190148
- median_test_mae: 0.293585
- coefficient_stability: 0.6032
- nonzero_count: 216
- sparsity_ratio: 0.3721
- raw_condition_number: inf
- effective_condition_number: 924317.3671
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.6340
- median_test_mse: 0.000536
- median_test_mae: 0.009733
- coefficient_stability: 0.5833
- nonzero_count: 174
- sparsity_ratio: 0.8389
- raw_condition_number: inf
- effective_condition_number: 964549.0012
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.6424
- median_test_mse: 0.202540
- median_test_mae: 0.354299
- coefficient_stability: 0.5000
- nonzero_count: 60
- sparsity_ratio: 0.2105
- raw_condition_number: inf
- effective_condition_number: 404558.3580
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -0.6463
- median_test_mse: 0.203029
- median_test_mae: 0.355619
- coefficient_stability: 0.4868
- nonzero_count: 2
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 404558.3580
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_plus_state x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.6860
- median_test_mse: 0.207962
- median_test_mae: 0.361927
- coefficient_stability: 0.3553
- nonzero_count: 25
- sparsity_ratio: 0.6711
- raw_condition_number: inf
- effective_condition_number: 404558.3580
- conditioning_pruned_features: altitude, command_throttle, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_only x next_raw_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.7026
- median_test_mse: 0.356780
- median_test_mae: 0.362763
- coefficient_stability: 0.2167
- nonzero_count: 52
- sparsity_ratio: 0.1333
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.7051
- median_test_mse: 0.357223
- median_test_mae: 0.363361
- coefficient_stability: 0.9667
- nonzero_count: 42
- sparsity_ratio: 0.3000
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.7051
- median_test_mse: 0.357228
- median_test_mae: 0.363355
- coefficient_stability: 0.9667
- nonzero_count: 7
- sparsity_ratio: 0.8833
- raw_condition_number: 342443.4752
- effective_condition_number: 342443.4752
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -0.8238
- median_test_mse: 0.225088
- median_test_mae: 0.367604
- coefficient_stability: 0.4326
- nonzero_count: 33
- sparsity_ratio: 0.8914
- raw_condition_number: inf
- effective_condition_number: 910939.1389
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.9458
- median_test_mse: 0.240069
- median_test_mae: 0.383171
- coefficient_stability: 0.5510
- nonzero_count: 214
- sparsity_ratio: 0.2961
- raw_condition_number: inf
- effective_condition_number: 910939.1389
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.9952
- median_test_mse: 0.246211
- median_test_mae: 0.363270
- coefficient_stability: 0.0839
- nonzero_count: 212
- sparsity_ratio: 0.3026
- raw_condition_number: inf
- effective_condition_number: 910939.1389
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_only x next_raw_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -5.6657
- median_test_mse: 0.433496
- median_test_mae: 0.272577
- coefficient_stability: 0.8750
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_only x next_raw_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -5.6657
- median_test_mse: 0.433496
- median_test_mae: 0.272563
- coefficient_stability: 0.8833
- nonzero_count: 16
- sparsity_ratio: 0.7333
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### commands_only x next_raw_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -5.6665
- median_test_mse: 0.433536
- median_test_mae: 0.272899
- coefficient_stability: 0.0750
- nonzero_count: 56
- sparsity_ratio: 0.0667
- raw_condition_number: inf
- effective_condition_number: 327798.8429
- conditioning_pruned_features: command_throttle
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: command_throttle

### feature_mapped_linear x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9968
- median_test_mse: 0.000688
- median_test_mae: 0.009888
- coefficient_stability: 0.9252
- nonzero_count: 20
- sparsity_ratio: 0.9675
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9967
- median_test_mse: 0.000707
- median_test_mae: 0.010650
- coefficient_stability: 0.8290
- nonzero_count: 103
- sparsity_ratio: 0.7014
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### feature_mapped_linear x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9967
- median_test_mse: 0.000712
- median_test_mae: 0.010429
- coefficient_stability: 0.9220
- nonzero_count: 395
- sparsity_ratio: 0.3577
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### feature_mapped_linear x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9967
- median_test_mse: 0.000712
- median_test_mae: 0.009909
- coefficient_stability: 0.5122
- nonzero_count: 300
- sparsity_ratio: 0.5122
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9966
- median_test_mse: 0.000741
- median_test_mae: 0.011475
- coefficient_stability: 0.9739
- nonzero_count: 250
- sparsity_ratio: 0.2754
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9966
- median_test_mse: 0.000741
- median_test_mae: 0.011207
- coefficient_stability: 0.9855
- nonzero_count: 23
- sparsity_ratio: 0.9333
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### feature_mapped_linear x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9962
- median_test_mse: 0.000496
- median_test_mae: 0.010297
- coefficient_stability: 0.8634
- nonzero_count: 9
- sparsity_ratio: 0.9854
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9958
- median_test_mse: 0.000557
- median_test_mae: 0.011377
- coefficient_stability: 0.9493
- nonzero_count: 10
- sparsity_ratio: 0.9710
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### pooled_backend_mode_augmented x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9958
- median_test_mse: 0.000560
- median_test_mae: 0.011096
- coefficient_stability: 0.7536
- nonzero_count: 61
- sparsity_ratio: 0.8232
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### feature_mapped_linear x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9957
- median_test_mse: 0.000598
- median_test_mae: 0.010063
- coefficient_stability: 0.8715
- nonzero_count: 164
- sparsity_ratio: 0.7333
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9954
- median_test_mse: 0.000645
- median_test_mae: 0.011266
- coefficient_stability: 0.9507
- nonzero_count: 137
- sparsity_ratio: 0.6029
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9929
- median_test_mse: 0.000863
- median_test_mae: 0.009610
- coefficient_stability: 0.8297
- nonzero_count: 69
- sparsity_ratio: 0.7500
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9928
- median_test_mse: 0.000875
- median_test_mae: 0.009881
- coefficient_stability: 0.9928
- nonzero_count: 182
- sparsity_ratio: 0.3406
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### feature_mapped_linear x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9928
- median_test_mse: 0.000879
- median_test_mae: 0.008647
- coefficient_stability: 0.9248
- nonzero_count: 9
- sparsity_ratio: 0.9817
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### feature_mapped_linear x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9928
- median_test_mse: 0.000869
- median_test_mae: 0.010219
- coefficient_stability: 0.9187
- nonzero_count: 10
- sparsity_ratio: 0.9797
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9927
- median_test_mse: 0.000885
- median_test_mae: 0.009941
- coefficient_stability: 0.9928
- nonzero_count: 10
- sparsity_ratio: 0.9638
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### feature_mapped_linear x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9927
- median_test_mse: 0.000876
- median_test_mae: 0.010265
- coefficient_stability: 0.9309
- nonzero_count: 282
- sparsity_ratio: 0.4268
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### feature_mapped_linear x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9927
- median_test_mse: 0.000890
- median_test_mae: 0.008812
- coefficient_stability: 0.9350
- nonzero_count: 258
- sparsity_ratio: 0.4756
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### feature_mapped_linear x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9925
- median_test_mse: 0.000913
- median_test_mae: 0.008809
- coefficient_stability: 0.5081
- nonzero_count: 236
- sparsity_ratio: 0.5203
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### feature_mapped_linear x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9924
- median_test_mse: 0.000914
- median_test_mae: 0.010454
- coefficient_stability: 0.5041
- nonzero_count: 246
- sparsity_ratio: 0.5000
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9918
- median_test_mse: 0.000991
- median_test_mae: 0.012616
- coefficient_stability: 0.8188
- nonzero_count: 65
- sparsity_ratio: 0.7645
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9916
- median_test_mse: 0.001010
- median_test_mae: 0.012817
- coefficient_stability: 0.9928
- nonzero_count: 190
- sparsity_ratio: 0.3116
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9916
- median_test_mse: 0.001014
- median_test_mae: 0.012870
- coefficient_stability: 0.9928
- nonzero_count: 13
- sparsity_ratio: 0.9529
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9889
- median_test_mse: 0.001355
- median_test_mae: 0.012632
- coefficient_stability: 0.8261
- nonzero_count: 39
- sparsity_ratio: 0.7174
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9887
- median_test_mse: 0.001380
- median_test_mae: 0.013086
- coefficient_stability: 0.9928
- nonzero_count: 95
- sparsity_ratio: 0.3116
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### feature_mapped_linear x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9886
- median_test_mse: 0.000938
- median_test_mae: 0.013390
- coefficient_stability: 0.4829
- nonzero_count: 228
- sparsity_ratio: 0.6293
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### feature_mapped_linear x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9886
- median_test_mse: 0.001388
- median_test_mae: 0.011394
- coefficient_stability: 0.9106
- nonzero_count: 5
- sparsity_ratio: 0.9797
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9886
- median_test_mse: 0.001391
- median_test_mae: 0.013096
- coefficient_stability: 0.9928
- nonzero_count: 6
- sparsity_ratio: 0.9565
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### feature_mapped_linear x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9885
- median_test_mse: 0.001405
- median_test_mae: 0.011617
- coefficient_stability: 0.9228
- nonzero_count: 138
- sparsity_ratio: 0.4390
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### feature_mapped_linear x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.9881
- median_test_mse: 0.001443
- median_test_mae: 0.011589
- coefficient_stability: 0.4756
- nonzero_count: 122
- sparsity_ratio: 0.5041
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### feature_mapped_linear x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7868
- median_test_mse: 0.000432
- median_test_mae: 0.006494
- coefficient_stability: 0.9065
- nonzero_count: 78
- sparsity_ratio: 0.8415
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7714
- median_test_mse: 0.000459
- median_test_mae: 0.007461
- coefficient_stability: 0.9710
- nonzero_count: 66
- sparsity_ratio: 0.7609
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### feature_mapped_linear x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7695
- median_test_mse: 0.000452
- median_test_mae: 0.007309
- coefficient_stability: 0.8648
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7356
- median_test_mse: 0.000483
- median_test_mae: 0.008071
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7214
- median_test_mse: 0.000525
- median_test_mae: 0.008471
- coefficient_stability: 0.7645
- nonzero_count: 43
- sparsity_ratio: 0.8442
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### feature_mapped_linear x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6737
- median_test_mse: 0.000689
- median_test_mae: 0.008746
- coefficient_stability: 0.8882
- nonzero_count: 46
- sparsity_ratio: 0.8130
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6490
- median_test_mse: 0.000727
- median_test_mae: 0.010009
- coefficient_stability: 0.9565
- nonzero_count: 39
- sparsity_ratio: 0.7174
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### feature_mapped_linear x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6451
- median_test_mse: 0.000719
- median_test_mae: 0.009765
- coefficient_stability: 0.8415
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6000
- median_test_mse: 0.000765
- median_test_mae: 0.010710
- coefficient_stability: 0.9457
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### feature_mapped_linear x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5960
- median_test_mse: 0.051102
- median_test_mae: 0.165648
- coefficient_stability: 0.8049
- nonzero_count: 126
- sparsity_ratio: 0.2317
- raw_condition_number: inf
- effective_condition_number: 580497.3875
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### feature_mapped_linear x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5927
- median_test_mse: 0.051518
- median_test_mae: 0.165398
- coefficient_stability: 0.7073
- nonzero_count: 56
- sparsity_ratio: 0.6585
- raw_condition_number: inf
- effective_condition_number: 580497.3875
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### feature_mapped_linear x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5905
- median_test_mse: 0.000459
- median_test_mae: 0.008268
- coefficient_stability: 0.8984
- nonzero_count: 103
- sparsity_ratio: 0.7907
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5774
- median_test_mse: 0.000827
- median_test_mae: 0.011189
- coefficient_stability: 0.7500
- nonzero_count: 23
- sparsity_ratio: 0.8333
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### feature_mapped_linear x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5758
- median_test_mse: 0.053653
- median_test_mae: 0.169087
- coefficient_stability: 0.2439
- nonzero_count: 112
- sparsity_ratio: 0.3171
- raw_condition_number: inf
- effective_condition_number: 580497.3875
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### feature_mapped_linear x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5547
- median_test_mse: 0.000510
- median_test_mae: 0.008783
- coefficient_stability: 0.4888
- nonzero_count: 167
- sparsity_ratio: 0.6606
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### pooled_backend_mode_augmented x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5497
- median_test_mse: 0.056962
- median_test_mae: 0.180429
- coefficient_stability: 0.8587
- nonzero_count: 50
- sparsity_ratio: 0.4565
- raw_condition_number: inf
- effective_condition_number: 456943.8881
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5487
- median_test_mse: 0.057088
- median_test_mae: 0.180690
- coefficient_stability: 0.5978
- nonzero_count: 64
- sparsity_ratio: 0.3043
- raw_condition_number: inf
- effective_condition_number: 456943.8881
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5479
- median_test_mse: 0.057189
- median_test_mae: 0.180796
- coefficient_stability: 0.8696
- nonzero_count: 72
- sparsity_ratio: 0.2174
- raw_condition_number: inf
- effective_condition_number: 456943.8881
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### feature_mapped_linear x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5393
- median_test_mse: 0.000520
- median_test_mae: 0.009563
- coefficient_stability: 0.8628
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### feature_mapped_linear x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5147
- median_test_mse: 0.000583
- median_test_mae: 0.010441
- coefficient_stability: 0.4756
- nonzero_count: 165
- sparsity_ratio: 0.6646
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### feature_mapped_linear x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4342
- median_test_mse: 0.000693
- median_test_mae: 0.009792
- coefficient_stability: 0.9252
- nonzero_count: 7
- sparsity_ratio: 0.9886
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4292
- median_test_mse: 0.000545
- median_test_mae: 0.010569
- coefficient_stability: 0.9529
- nonzero_count: 86
- sparsity_ratio: 0.6884
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### pooled_backend_mode_augmented x delta_state | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4238
- median_test_mse: 0.000707
- median_test_mae: 0.010650
- coefficient_stability: 0.8290
- nonzero_count: 90
- sparsity_ratio: 0.7391
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### feature_mapped_linear x delta_state | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4178
- median_test_mse: 0.000712
- median_test_mae: 0.009909
- coefficient_stability: 0.5122
- nonzero_count: 288
- sparsity_ratio: 0.5317
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### feature_mapped_linear x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4118
- median_test_mse: 0.000720
- median_test_mae: 0.010245
- coefficient_stability: 0.9398
- nonzero_count: 329
- sparsity_ratio: 0.4650
- raw_condition_number: inf
- effective_condition_number: 580627.8475
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3958
- median_test_mse: 0.000741
- median_test_mae: 0.011106
- coefficient_stability: 0.9855
- nonzero_count: 6
- sparsity_ratio: 0.9826
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3829
- median_test_mse: 0.000757
- median_test_mae: 0.011242
- coefficient_stability: 0.9855
- nonzero_count: 232
- sparsity_ratio: 0.3275
- raw_condition_number: inf
- effective_condition_number: 457653.9629
- conditioning_pruned_features: altitude, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: config_profile_px4_real_posctl_nominal

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3592
- median_test_mse: 0.000586
- median_test_mae: 0.011337
- coefficient_stability: 0.9420
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### pooled_backend_mode_augmented x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3474
- median_test_mse: 0.000612
- median_test_mae: 0.011641
- coefficient_stability: 0.7482
- nonzero_count: 41
- sparsity_ratio: 0.8514
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### feature_mapped_linear x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3230
- median_test_mse: 0.000803
- median_test_mae: 0.011449
- coefficient_stability: 0.4837
- nonzero_count: 89
- sparsity_ratio: 0.6382
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### feature_mapped_linear x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0255
- median_test_mse: 0.000469
- median_test_mae: 0.009145
- coefficient_stability: 0.9041
- nonzero_count: 132
- sparsity_ratio: 0.7854
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### feature_mapped_linear x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.0277
- median_test_mse: 0.000465
- median_test_mae: 0.009739
- coefficient_stability: 0.8626
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### pooled_backend_mode_augmented x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.0435
- median_test_mse: 0.000475
- median_test_mae: 0.009844
- coefficient_stability: 0.9638
- nonzero_count: 120
- sparsity_ratio: 0.6522
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### pooled_backend_mode_augmented x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.1748
- median_test_mse: 0.000530
- median_test_mae: 0.010760
- coefficient_stability: 0.9507
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### pooled_backend_mode_augmented x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.2143
- median_test_mse: 0.000560
- median_test_mae: 0.011096
- coefficient_stability: 0.7536
- nonzero_count: 51
- sparsity_ratio: 0.8522
- raw_condition_number: inf
- effective_condition_number: 405359.1058
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### pooled_backend_mode_augmented x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.6424
- median_test_mse: 0.202540
- median_test_mae: 0.354299
- coefficient_stability: 0.5870
- nonzero_count: 60
- sparsity_ratio: 0.3478
- raw_condition_number: inf
- effective_condition_number: 404558.3580
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### pooled_backend_mode_augmented x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.6463
- median_test_mse: 0.203029
- median_test_mae: 0.355619
- coefficient_stability: 0.5761
- nonzero_count: 2
- sparsity_ratio: 0.9783
- raw_condition_number: inf
- effective_condition_number: 404558.3580
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### feature_mapped_linear x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.6706
- median_test_mse: 0.206034
- median_test_mae: 0.340016
- coefficient_stability: 0.6159
- nonzero_count: 81
- sparsity_ratio: 0.5061
- raw_condition_number: inf
- effective_condition_number: 503205.0023
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### pooled_backend_mode_augmented x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.6860
- median_test_mse: 0.207962
- median_test_mae: 0.361927
- coefficient_stability: 0.4674
- nonzero_count: 25
- sparsity_ratio: 0.7283
- raw_condition_number: inf
- effective_condition_number: 404558.3580
- conditioning_pruned_features: altitude, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl

### feature_mapped_linear x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.6906
- median_test_mse: 0.208547
- median_test_mae: 0.344553
- coefficient_stability: 0.4878
- nonzero_count: 4
- sparsity_ratio: 0.9756
- raw_condition_number: inf
- effective_condition_number: 503205.0023
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### feature_mapped_linear x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -2.7753
- median_test_mse: 0.464478
- median_test_mae: 0.498888
- coefficient_stability: 0.2409
- nonzero_count: 74
- sparsity_ratio: 0.5488
- raw_condition_number: inf
- effective_condition_number: 503205.0023
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

### feature_mapped_linear x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: -3.1333
- median_test_mse: 0.000938
- median_test_mae: 0.013390
- coefficient_stability: 0.4829
- nonzero_count: 218
- sparsity_ratio: 0.6455
- raw_condition_number: inf
- effective_condition_number: 504164.1196
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, sq__command_throttle, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, command_throttle, config_profile_px4_real_posctl_nominal, mode_posctl, sq__command_throttle

## Skipped
- 无。