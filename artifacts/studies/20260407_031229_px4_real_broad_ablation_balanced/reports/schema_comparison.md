# Schema Comparison: px4_real_broad_ablation_balanced

## Results
### commands_plus_state_history x next_raw_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.9726
- median_test_mse: 0.000046
- median_test_mae: 0.003960
- coefficient_stability: 1.0000
- nonzero_count: 324
- sparsity_ratio: 0.7158
- raw_condition_number: inf
- effective_condition_number: 1259416.2092
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.9672
- median_test_mse: 0.000055
- median_test_mae: 0.004629
- coefficient_stability: 1.0000
- nonzero_count: 357
- sparsity_ratio: 0.6868
- raw_condition_number: inf
- effective_condition_number: 1259416.2092
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x next_raw_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9663
- median_test_mse: 0.000059
- median_test_mae: 0.004892
- coefficient_stability: 1.0000
- nonzero_count: 173
- sparsity_ratio: 0.3930
- raw_condition_number: inf
- effective_condition_number: 501499.7471
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x next_raw_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.9600
- median_test_mse: 0.000067
- median_test_mae: 0.005391
- coefficient_stability: 1.0000
- nonzero_count: 20
- sparsity_ratio: 0.9825
- raw_condition_number: inf
- effective_condition_number: 1259416.2092
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x next_raw_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9595
- median_test_mse: 0.000070
- median_test_mae: 0.005759
- coefficient_stability: 1.0000
- nonzero_count: 9
- sparsity_ratio: 0.9684
- raw_condition_number: inf
- effective_condition_number: 501499.7471
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9545
- median_test_mse: 0.000079
- median_test_mae: 0.006268
- coefficient_stability: 1.0000
- nonzero_count: 58
- sparsity_ratio: 0.7965
- raw_condition_number: inf
- effective_condition_number: 501499.7471
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x next_raw_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.8755
- median_test_mse: 0.000207
- median_test_mae: 0.007704
- coefficient_stability: 1.0000
- nonzero_count: 414
- sparsity_ratio: 0.6933
- raw_condition_number: inf
- effective_condition_number: 1481157.8962
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.6627
- median_test_mse: 0.000022
- median_test_mae: 0.001515
- coefficient_stability: 1.0000
- nonzero_count: 123
- sparsity_ratio: 0.8651
- raw_condition_number: inf
- effective_condition_number: 1259416.2092
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x future_state_horizon | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.5852
- median_test_mse: 0.000027
- median_test_mae: 0.001774
- coefficient_stability: 1.0000
- nonzero_count: 88
- sparsity_ratio: 0.6140
- raw_condition_number: inf
- effective_condition_number: 501499.7471
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.5780
- median_test_mse: 0.000028
- median_test_mae: 0.002072
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 1259416.2092
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.4997
- median_test_mse: 0.000033
- median_test_mae: 0.002062
- coefficient_stability: 1.0000
- nonzero_count: 73
- sparsity_ratio: 0.8399
- raw_condition_number: inf
- effective_condition_number: 1259416.2092
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x future_state_horizon | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.4679
- median_test_mse: 0.000035
- median_test_mae: 0.003044
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 501499.7471
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x future_state_horizon | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.4646
- median_test_mse: 0.000035
- median_test_mae: 0.003075
- coefficient_stability: 1.0000
- nonzero_count: 36
- sparsity_ratio: 0.8421
- raw_condition_number: inf
- effective_condition_number: 501499.7471
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x future_state_horizon | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.4432
- median_test_mse: 0.000037
- median_test_mae: 0.002011
- coefficient_stability: 1.0000
- nonzero_count: 204
- sparsity_ratio: 0.7763
- raw_condition_number: inf
- effective_condition_number: 1259416.2092
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.3955
- median_test_mse: 0.000040
- median_test_mae: 0.002450
- coefficient_stability: 1.0000
- nonzero_count: 51
- sparsity_ratio: 0.5526
- raw_condition_number: inf
- effective_condition_number: 501499.7471
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.3866
- median_test_mse: 0.000041
- median_test_mae: 0.002870
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 1259416.2092
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.3520
- median_test_mse: 0.001078
- median_test_mae: 0.017026
- coefficient_stability: 1.0000
- nonzero_count: 20
- sparsity_ratio: 0.9852
- raw_condition_number: inf
- effective_condition_number: 1481157.8962
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2222
- median_test_mse: 0.000052
- median_test_mae: 0.002650
- coefficient_stability: 1.0000
- nonzero_count: 106
- sparsity_ratio: 0.7675
- raw_condition_number: inf
- effective_condition_number: 1259416.2092
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2213
- median_test_mse: 0.000051
- median_test_mae: 0.003974
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 501499.7471
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2154
- median_test_mse: 0.000052
- median_test_mae: 0.004021
- coefficient_stability: 1.0000
- nonzero_count: 18
- sparsity_ratio: 0.8421
- raw_condition_number: inf
- effective_condition_number: 501499.7471
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x next_raw_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1839
- median_test_mse: 0.001357
- median_test_mae: 0.018164
- coefficient_stability: 1.0000
- nonzero_count: 422
- sparsity_ratio: 0.6874
- raw_condition_number: inf
- effective_condition_number: 1481157.8962
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0169
- median_test_mse: 0.000036
- median_test_mae: 0.003702
- coefficient_stability: 1.0000
- nonzero_count: 281
- sparsity_ratio: 0.7535
- raw_condition_number: inf
- effective_condition_number: 1259416.2092
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_only x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0780
- median_test_mse: 0.000071
- median_test_mae: 0.003744
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 446498.1789
- effective_condition_number: 446498.1789
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0785
- median_test_mse: 0.000071
- median_test_mae: 0.003748
- coefficient_stability: 1.0000
- nonzero_count: 18
- sparsity_ratio: 0.2500
- raw_condition_number: 446498.1789
- effective_condition_number: 446498.1789
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0793
- median_test_mse: 0.000071
- median_test_mae: 0.003741
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 446498.1789
- effective_condition_number: 446498.1789
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0794
- median_test_mse: 0.000071
- median_test_mae: 0.003676
- coefficient_stability: 1.0000
- nonzero_count: 15
- sparsity_ratio: 0.3750
- raw_condition_number: 446498.1789
- effective_condition_number: 446498.1789
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0798
- median_test_mse: 0.000071
- median_test_mae: 0.003744
- coefficient_stability: 1.0000
- nonzero_count: 36
- sparsity_ratio: 0.2500
- raw_condition_number: 446498.1789
- effective_condition_number: 446498.1789
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0804
- median_test_mse: 0.000071
- median_test_mae: 0.003664
- coefficient_stability: 1.0000
- nonzero_count: 30
- sparsity_ratio: 0.3750
- raw_condition_number: 446498.1789
- effective_condition_number: 446498.1789
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.2710
- median_test_mse: 0.000046
- median_test_mae: 0.003960
- coefficient_stability: 1.0000
- nonzero_count: 322
- sparsity_ratio: 0.7175
- raw_condition_number: inf
- effective_condition_number: 1259416.2092
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.3735
- median_test_mse: 0.000049
- median_test_mae: 0.004636
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.9965
- raw_condition_number: inf
- effective_condition_number: 1259416.2092
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_only x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.4098
- median_test_mse: 0.000051
- median_test_mae: 0.003835
- coefficient_stability: 1.0000
- nonzero_count: 29
- sparsity_ratio: 0.5167
- raw_condition_number: 446498.1789
- effective_condition_number: 446498.1789
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.4104
- median_test_mse: 0.139587
- median_test_mae: 0.262085
- coefficient_stability: 1.0000
- nonzero_count: 28
- sparsity_ratio: 0.6316
- raw_condition_number: inf
- effective_condition_number: 501369.1358
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.4298
- median_test_mse: 0.141499
- median_test_mae: 0.264199
- coefficient_stability: 1.0000
- nonzero_count: 76
- sparsity_ratio: 0.0000
- raw_condition_number: inf
- effective_condition_number: 501369.1358
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.4341
- median_test_mse: 0.141925
- median_test_mae: 0.264377
- coefficient_stability: 1.0000
- nonzero_count: 48
- sparsity_ratio: 0.3684
- raw_condition_number: inf
- effective_condition_number: 501369.1358
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.4631
- median_test_mse: 0.000052
- median_test_mae: 0.003942
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 446498.1789
- effective_condition_number: 446498.1789
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.4647
- median_test_mse: 0.000053
- median_test_mae: 0.003945
- coefficient_stability: 1.0000
- nonzero_count: 45
- sparsity_ratio: 0.2500
- raw_condition_number: 446498.1789
- effective_condition_number: 446498.1789
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.4834
- median_test_mse: 0.147102
- median_test_mae: 0.268105
- coefficient_stability: 1.0000
- nonzero_count: 88
- sparsity_ratio: 0.7105
- raw_condition_number: inf
- effective_condition_number: 1254579.6544
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.5061
- median_test_mse: 0.149355
- median_test_mae: 0.271506
- coefficient_stability: 1.0000
- nonzero_count: 266
- sparsity_ratio: 0.1250
- raw_condition_number: inf
- effective_condition_number: 1254579.6544
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.5762
- median_test_mse: 0.000057
- median_test_mae: 0.004706
- coefficient_stability: 1.0000
- nonzero_count: 162
- sparsity_ratio: 0.4316
- raw_condition_number: inf
- effective_condition_number: 501499.7471
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.7474
- median_test_mse: 0.172931
- median_test_mae: 0.272547
- coefficient_stability: 1.0000
- nonzero_count: 12
- sparsity_ratio: 0.2500
- raw_condition_number: 446496.4788
- effective_condition_number: 446496.4788
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.7478
- median_test_mse: 0.172971
- median_test_mae: 0.272564
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 446496.4788
- effective_condition_number: 446496.4788
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.7506
- median_test_mse: 0.173250
- median_test_mae: 0.272707
- coefficient_stability: 1.0000
- nonzero_count: 12
- sparsity_ratio: 0.2500
- raw_condition_number: 446496.4788
- effective_condition_number: 446496.4788
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -1.1216
- median_test_mse: 0.210391
- median_test_mae: 0.348473
- coefficient_stability: 1.0000
- nonzero_count: 245
- sparsity_ratio: 0.1941
- raw_condition_number: inf
- effective_condition_number: 1254579.6544
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -1.1516
- median_test_mse: 0.000077
- median_test_mae: 0.006201
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 501499.7471
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -1.1995
- median_test_mse: 0.000079
- median_test_mae: 0.006268
- coefficient_stability: 1.0000
- nonzero_count: 49
- sparsity_ratio: 0.8281
- raw_condition_number: inf
- effective_condition_number: 501499.7471
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x future_state_horizon | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -2.4700
- median_test_mse: 0.000231
- median_test_mae: 0.006808
- coefficient_stability: 1.0000
- nonzero_count: 163
- sparsity_ratio: 0.8491
- raw_condition_number: inf
- effective_condition_number: 1481157.8962
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -3.3059
- median_test_mse: 0.000154
- median_test_mae: 0.006696
- coefficient_stability: 1.0000
- nonzero_count: 312
- sparsity_ratio: 0.7689
- raw_condition_number: inf
- effective_condition_number: 1481157.8962
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -5.0053
- median_test_mse: 0.000400
- median_test_mae: 0.009589
- coefficient_stability: 1.0000
- nonzero_count: 96
- sparsity_ratio: 0.8222
- raw_condition_number: inf
- effective_condition_number: 1481157.8962
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -10.5199
- median_test_mse: 0.000766
- median_test_mae: 0.013438
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 1481157.8962
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -14.4599
- median_test_mse: 0.001030
- median_test_mae: 0.016324
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 1481157.8962
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -19.1810
- median_test_mse: 0.000723
- median_test_mae: 0.014586
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.9970
- raw_condition_number: inf
- effective_condition_number: 1481157.8962
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -22.2654
- median_test_mse: 2.307166
- median_test_mae: 1.014384
- coefficient_stability: 1.0000
- nonzero_count: 64
- sparsity_ratio: 0.8140
- raw_condition_number: inf
- effective_condition_number: 1371832.8588
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -23.6343
- median_test_mse: 2.442920
- median_test_mae: 1.034869
- coefficient_stability: 1.0000
- nonzero_count: 267
- sparsity_ratio: 0.2238
- raw_condition_number: inf
- effective_condition_number: 1371832.8588
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -23.6805
- median_test_mse: 2.447497
- median_test_mae: 1.030348
- coefficient_stability: 1.0000
- nonzero_count: 252
- sparsity_ratio: 0.2674
- raw_condition_number: inf
- effective_condition_number: 1371832.8588
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -24.6362
- median_test_mse: 0.001705
- median_test_mae: 0.018418
- coefficient_stability: 1.0000
- nonzero_count: 276
- sparsity_ratio: 0.7444
- raw_condition_number: inf
- effective_condition_number: 1481157.8962
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -35.7566
- median_test_mse: 0.002449
- median_test_mae: 0.022912
- coefficient_stability: 1.0000
- nonzero_count: 153
- sparsity_ratio: 0.7167
- raw_condition_number: inf
- effective_condition_number: 1481157.8962
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -36.9026
- median_test_mse: 0.001357
- median_test_mae: 0.018164
- coefficient_stability: 1.0000
- nonzero_count: 420
- sparsity_ratio: 0.6889
- raw_condition_number: inf
- effective_condition_number: 1481157.8962
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_offboard_attitude_nominal, config_profile_px4_real_posctl_nominal, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: config_profile_px4_real_offboard_attitude_nominal, mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, command_throttle__lag_1, command_throttle__lag_2, command_throttle__lag_3, config_profile_px4_real_posctl_nominal, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_only x next_raw_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -119.7585
- median_test_mse: 0.209481
- median_test_mae: 0.185943
- coefficient_stability: 1.0000
- nonzero_count: 2
- sparsity_ratio: 0.9667
- raw_condition_number: 446498.1789
- effective_condition_number: 446498.1789
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -119.8793
- median_test_mse: 0.209691
- median_test_mae: 0.185965
- coefficient_stability: 1.0000
- nonzero_count: 41
- sparsity_ratio: 0.3167
- raw_condition_number: 446498.1789
- effective_condition_number: 446498.1789
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -120.0332
- median_test_mse: 0.209958
- median_test_mae: 0.186123
- coefficient_stability: 1.0000
- nonzero_count: 47
- sparsity_ratio: 0.2167
- raw_condition_number: 446498.1789
- effective_condition_number: 446498.1789
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

## Skipped
- 无。