# Schema Comparison: px4_real_generalization_ablation

## Results
### full_augmented x next_raw_state | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.9995
- median_test_mse: 0.000092
- median_test_mae: 0.003705
- coefficient_stability: 0.8958
- nonzero_count: 47
- sparsity_ratio: 0.9644
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9995
- median_test_mse: 0.000100
- median_test_mae: 0.004302
- coefficient_stability: 0.9610
- nonzero_count: 29
- sparsity_ratio: 0.9780
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.9994
- median_test_mse: 0.000112
- median_test_mae: 0.003474
- coefficient_stability: 0.8947
- nonzero_count: 39
- sparsity_ratio: 0.9658
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9994
- median_test_mse: 0.000124
- median_test_mae: 0.004131
- coefficient_stability: 0.9610
- nonzero_count: 29
- sparsity_ratio: 0.9746
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9993
- median_test_mse: 0.000136
- median_test_mae: 0.005031
- coefficient_stability: 0.9473
- nonzero_count: 507
- sparsity_ratio: 0.6159
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9992
- median_test_mse: 0.000134
- median_test_mae: 0.004119
- coefficient_stability: 0.9470
- nonzero_count: 143
- sparsity_ratio: 0.8917
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9992
- median_test_mse: 0.000134
- median_test_mae: 0.004609
- coefficient_stability: 0.9795
- nonzero_count: 63
- sparsity_ratio: 0.9523
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9992
- median_test_mse: 0.000164
- median_test_mae: 0.004892
- coefficient_stability: 0.9421
- nonzero_count: 452
- sparsity_ratio: 0.6035
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9991
- median_test_mse: 0.000148
- median_test_mae: 0.003757
- coefficient_stability: 0.9404
- nonzero_count: 142
- sparsity_ratio: 0.8754
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9991
- median_test_mse: 0.000149
- median_test_mae: 0.004233
- coefficient_stability: 0.9737
- nonzero_count: 57
- sparsity_ratio: 0.9500
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9990
- median_test_mse: 0.000173
- median_test_mae: 0.006216
- coefficient_stability: 0.9667
- nonzero_count: 1056
- sparsity_ratio: 0.2000
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9990
- median_test_mse: 0.000179
- median_test_mae: 0.005618
- coefficient_stability: 0.9640
- nonzero_count: 915
- sparsity_ratio: 0.1974
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x next_raw_state | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.9982
- median_test_mse: 0.000376
- median_test_mae: 0.006471
- coefficient_stability: 0.9421
- nonzero_count: 14
- sparsity_ratio: 0.9509
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9982
- median_test_mse: 0.000382
- median_test_mae: 0.006562
- coefficient_stability: 0.9772
- nonzero_count: 212
- sparsity_ratio: 0.2561
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9982
- median_test_mse: 0.000383
- median_test_mae: 0.006578
- coefficient_stability: 0.9807
- nonzero_count: 10
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.000397
- median_test_mae: 0.007220
- coefficient_stability: 0.9789
- nonzero_count: 31
- sparsity_ratio: 0.8912
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.000399
- median_test_mae: 0.007412
- coefficient_stability: 1.0000
- nonzero_count: 278
- sparsity_ratio: 0.0246
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.000400
- median_test_mae: 0.007420
- coefficient_stability: 1.0000
- nonzero_count: 17
- sparsity_ratio: 0.9404
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x future_state_horizon | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9975
- median_test_mse: 0.000128
- median_test_mae: 0.003543
- coefficient_stability: 0.9688
- nonzero_count: 27
- sparsity_ratio: 0.9744
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9974
- median_test_mse: 0.000133
- median_test_mae: 0.003594
- coefficient_stability: 0.9233
- nonzero_count: 76
- sparsity_ratio: 0.9280
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9972
- median_test_mse: 0.000145
- median_test_mae: 0.004234
- coefficient_stability: 0.9924
- nonzero_count: 659
- sparsity_ratio: 0.3759
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.000152
- median_test_mae: 0.003134
- coefficient_stability: 0.9583
- nonzero_count: 23
- sparsity_ratio: 0.9748
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9969
- median_test_mse: 0.000156
- median_test_mae: 0.003154
- coefficient_stability: 0.9112
- nonzero_count: 78
- sparsity_ratio: 0.9145
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9968
- median_test_mse: 0.000164
- median_test_mae: 0.003721
- coefficient_stability: 0.9912
- nonzero_count: 579
- sparsity_ratio: 0.3651
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9962
- median_test_mse: 0.000196
- median_test_mae: 0.004754
- coefficient_stability: 0.9564
- nonzero_count: 17
- sparsity_ratio: 0.9678
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9960
- median_test_mse: 0.000204
- median_test_mae: 0.004814
- coefficient_stability: 0.8996
- nonzero_count: 51
- sparsity_ratio: 0.9034
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9958
- median_test_mse: 0.000215
- median_test_mae: 0.005460
- coefficient_stability: 0.9886
- nonzero_count: 358
- sparsity_ratio: 0.3220
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9954
- median_test_mse: 0.000235
- median_test_mae: 0.004272
- coefficient_stability: 0.9452
- nonzero_count: 14
- sparsity_ratio: 0.9693
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9953
- median_test_mse: 0.000242
- median_test_mae: 0.004299
- coefficient_stability: 0.8838
- nonzero_count: 51
- sparsity_ratio: 0.8882
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9950
- median_test_mse: 0.000253
- median_test_mae: 0.004999
- coefficient_stability: 0.9868
- nonzero_count: 307
- sparsity_ratio: 0.3268
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9947
- median_test_mse: 0.000260
- median_test_mae: 0.006410
- coefficient_stability: 0.9706
- nonzero_count: 37
- sparsity_ratio: 0.9650
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9946
- median_test_mse: 0.000268
- median_test_mae: 0.006548
- coefficient_stability: 0.9186
- nonzero_count: 103
- sparsity_ratio: 0.9025
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9945
- median_test_mse: 0.000273
- median_test_mae: 0.006720
- coefficient_stability: 0.9877
- nonzero_count: 774
- sparsity_ratio: 0.2670
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9943
- median_test_mse: 0.000283
- median_test_mae: 0.006658
- coefficient_stability: 0.9726
- nonzero_count: 35
- sparsity_ratio: 0.9616
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9941
- median_test_mse: 0.000291
- median_test_mae: 0.006704
- coefficient_stability: 0.9101
- nonzero_count: 111
- sparsity_ratio: 0.8783
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9939
- median_test_mse: 0.000302
- median_test_mae: 0.007122
- coefficient_stability: 0.9890
- nonzero_count: 650
- sparsity_ratio: 0.2873
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9924
- median_test_mse: 0.000386
- median_test_mae: 0.005566
- coefficient_stability: 0.9649
- nonzero_count: 15
- sparsity_ratio: 0.9342
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x future_state_horizon | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9923
- median_test_mse: 0.000388
- median_test_mae: 0.005732
- coefficient_stability: 1.0000
- nonzero_count: 214
- sparsity_ratio: 0.0614
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x future_state_horizon | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9923
- median_test_mse: 0.000388
- median_test_mae: 0.005756
- coefficient_stability: 1.0000
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x window_summary_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9900
- median_test_mse: 0.000495
- median_test_mae: 0.008349
- coefficient_stability: 0.9649
- nonzero_count: 20
- sparsity_ratio: 0.9123
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x window_summary_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9899
- median_test_mse: 0.000497
- median_test_mae: 0.008480
- coefficient_stability: 1.0000
- nonzero_count: 220
- sparsity_ratio: 0.0351
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x window_summary_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9899
- median_test_mse: 0.000497
- median_test_mae: 0.008502
- coefficient_stability: 1.0000
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9883
- median_test_mse: 0.000594
- median_test_mae: 0.007338
- coefficient_stability: 0.9649
- nonzero_count: 7
- sparsity_ratio: 0.9386
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9882
- median_test_mse: 0.000597
- median_test_mae: 0.007569
- coefficient_stability: 1.0000
- nonzero_count: 110
- sparsity_ratio: 0.0351
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9882
- median_test_mse: 0.000598
- median_test_mae: 0.007589
- coefficient_stability: 1.0000
- nonzero_count: 3
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x future_state_horizon | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.8837
- median_test_mse: 0.000117
- median_test_mae: 0.003532
- coefficient_stability: 0.9806
- nonzero_count: 198
- sparsity_ratio: 0.8125
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.8811
- median_test_mse: 0.000098
- median_test_mae: 0.003313
- coefficient_stability: 0.9555
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.8780
- median_test_mse: 0.000100
- median_test_mae: 0.003418
- coefficient_stability: 0.8925
- nonzero_count: 10
- sparsity_ratio: 0.9905
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.8689
- median_test_mse: 0.000162
- median_test_mae: 0.003312
- coefficient_stability: 0.9764
- nonzero_count: 165
- sparsity_ratio: 0.8191
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.8652
- median_test_mse: 0.000135
- median_test_mae: 0.003012
- coefficient_stability: 0.9539
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.8644
- median_test_mse: 0.000131
- median_test_mae: 0.002989
- coefficient_stability: 0.8969
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.8209
- median_test_mse: 0.000177
- median_test_mae: 0.004604
- coefficient_stability: 0.9735
- nonzero_count: 124
- sparsity_ratio: 0.7652
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.8175
- median_test_mse: 0.000153
- median_test_mae: 0.004381
- coefficient_stability: 0.9394
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.8111
- median_test_mse: 0.000157
- median_test_mae: 0.004528
- coefficient_stability: 0.8542
- nonzero_count: 6
- sparsity_ratio: 0.9886
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.8105
- median_test_mse: 0.000092
- median_test_mae: 0.003705
- coefficient_stability: 0.8958
- nonzero_count: 45
- sparsity_ratio: 0.9659
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x future_state_horizon | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.8070
- median_test_mse: 0.000423
- median_test_mae: 0.005054
- coefficient_stability: 0.9956
- nonzero_count: 133
- sparsity_ratio: 0.4167
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x future_state_horizon | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.8069
- median_test_mse: 0.000419
- median_test_mae: 0.004985
- coefficient_stability: 0.9430
- nonzero_count: 2
- sparsity_ratio: 0.9912
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x future_state_horizon | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.8068
- median_test_mse: 0.000424
- median_test_mae: 0.005083
- coefficient_stability: 0.9956
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x delta_state | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.8054
- median_test_mse: 0.000093
- median_test_mae: 0.003867
- coefficient_stability: 0.9621
- nonzero_count: 22
- sparsity_ratio: 0.9833
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.7959
- median_test_mse: 0.000251
- median_test_mae: 0.004429
- coefficient_stability: 0.9682
- nonzero_count: 97
- sparsity_ratio: 0.7873
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.7915
- median_test_mse: 0.000214
- median_test_mae: 0.004069
- coefficient_stability: 0.9408
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.7904
- median_test_mse: 0.000208
- median_test_mae: 0.004039
- coefficient_stability: 0.8662
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.7847
- median_test_mse: 0.000112
- median_test_mae: 0.003474
- coefficient_stability: 0.8947
- nonzero_count: 37
- sparsity_ratio: 0.9675
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.7745
- median_test_mse: 0.000116
- median_test_mae: 0.003699
- coefficient_stability: 0.9636
- nonzero_count: 22
- sparsity_ratio: 0.9807
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.7706
- median_test_mse: 0.000110
- median_test_mae: 0.004490
- coefficient_stability: 0.9837
- nonzero_count: 346
- sparsity_ratio: 0.7379
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.7570
- median_test_mse: 0.000130
- median_test_mae: 0.004254
- coefficient_stability: 0.9773
- nonzero_count: 53
- sparsity_ratio: 0.9598
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.7458
- median_test_mse: 0.000134
- median_test_mae: 0.004119
- coefficient_stability: 0.9470
- nonzero_count: 142
- sparsity_ratio: 0.8924
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.7332
- median_test_mse: 0.000140
- median_test_mae: 0.004366
- coefficient_stability: 0.9838
- nonzero_count: 290
- sparsity_ratio: 0.7456
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.7291
- median_test_mse: 0.000145
- median_test_mae: 0.003899
- coefficient_stability: 0.9719
- nonzero_count: 47
- sparsity_ratio: 0.9588
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.7257
- median_test_mse: 0.000146
- median_test_mae: 0.005184
- coefficient_stability: 0.9947
- nonzero_count: 934
- sparsity_ratio: 0.2924
- raw_condition_number: inf
- effective_condition_number: 3613.2124
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.7205
- median_test_mse: 0.000148
- median_test_mae: 0.003757
- coefficient_stability: 0.9404
- nonzero_count: 140
- sparsity_ratio: 0.8772
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x selected_state_subset | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.7175
- median_test_mse: 0.000662
- median_test_mae: 0.006647
- coefficient_stability: 0.9956
- nonzero_count: 77
- sparsity_ratio: 0.3246
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.7174
- median_test_mse: 0.000655
- median_test_mae: 0.006542
- coefficient_stability: 0.9430
- nonzero_count: 2
- sparsity_ratio: 0.9825
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.7173
- median_test_mse: 0.000664
- median_test_mae: 0.006675
- coefficient_stability: 0.9956
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x window_summary_response | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.7017
- median_test_mse: 0.000318
- median_test_mae: 0.006554
- coefficient_stability: 0.9715
- nonzero_count: 232
- sparsity_ratio: 0.7456
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.6963
- median_test_mse: 0.000276
- median_test_mae: 0.006272
- coefficient_stability: 0.9249
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.6918
- median_test_mse: 0.000274
- median_test_mae: 0.006318
- coefficient_stability: 0.8509
- nonzero_count: 1
- sparsity_ratio: 0.9989
- raw_condition_number: inf
- effective_condition_number: 3248.4323
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.6906
- median_test_mse: 0.000265
- median_test_mae: 0.006188
- coefficient_stability: 0.9706
- nonzero_count: 261
- sparsity_ratio: 0.7528
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.6906
- median_test_mse: 0.000164
- median_test_mae: 0.004970
- coefficient_stability: 0.9939
- nonzero_count: 808
- sparsity_ratio: 0.2912
- raw_condition_number: inf
- effective_condition_number: 3424.1423
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.6870
- median_test_mse: 0.000242
- median_test_mae: 0.006067
- coefficient_stability: 0.9347
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.6823
- median_test_mse: 0.000248
- median_test_mae: 0.006202
- coefficient_stability: 0.8551
- nonzero_count: 9
- sparsity_ratio: 0.9915
- raw_condition_number: inf
- effective_condition_number: 3435.5927
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x window_summary_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.6756
- median_test_mse: 0.000545
- median_test_mae: 0.007604
- coefficient_stability: 0.9912
- nonzero_count: 158
- sparsity_ratio: 0.3070
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x window_summary_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.6754
- median_test_mse: 0.000546
- median_test_mae: 0.007623
- coefficient_stability: 0.9846
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x window_summary_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.6753
- median_test_mse: 0.000544
- median_test_mae: 0.007602
- coefficient_stability: 0.9298
- nonzero_count: 4
- sparsity_ratio: 0.9825
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x actuator_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.6085
- median_test_mse: 0.046632
- median_test_mae: 0.163373
- coefficient_stability: 0.7368
- nonzero_count: 76
- sparsity_ratio: 0.0000
- raw_condition_number: inf
- effective_condition_number: 722.2598
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x actuator_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.6085
- median_test_mse: 0.046633
- median_test_mae: 0.163382
- coefficient_stability: 0.7368
- nonzero_count: 5
- sparsity_ratio: 0.9342
- raw_condition_number: inf
- effective_condition_number: 722.2598
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x actuator_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.6084
- median_test_mse: 0.046636
- median_test_mae: 0.163280
- coefficient_stability: 0.7105
- nonzero_count: 12
- sparsity_ratio: 0.8421
- raw_condition_number: inf
- effective_condition_number: 722.2598
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x actuator_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.6024
- median_test_mse: 0.047368
- median_test_mae: 0.162191
- coefficient_stability: 0.6151
- nonzero_count: 287
- sparsity_ratio: 0.0559
- raw_condition_number: inf
- effective_condition_number: 3253.3917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.5866
- median_test_mse: 0.049227
- median_test_mae: 0.164538
- coefficient_stability: 0.4951
- nonzero_count: 76
- sparsity_ratio: 0.7500
- raw_condition_number: inf
- effective_condition_number: 3253.3917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.5751
- median_test_mse: 0.050600
- median_test_mae: 0.166362
- coefficient_stability: 0.4309
- nonzero_count: 122
- sparsity_ratio: 0.5987
- raw_condition_number: inf
- effective_condition_number: 3253.3917
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x actuator_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.5342
- median_test_mse: 0.055718
- median_test_mae: 0.172294
- coefficient_stability: 0.6458
- nonzero_count: 319
- sparsity_ratio: 0.0506
- raw_condition_number: inf
- effective_condition_number: 3268.6605
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x actuator_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.5216
- median_test_mse: 0.057198
- median_test_mae: 0.174627
- coefficient_stability: 0.5164
- nonzero_count: 75
- sparsity_ratio: 0.7768
- raw_condition_number: inf
- effective_condition_number: 3268.6605
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_only x actuator_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.5120
- median_test_mse: 0.058209
- median_test_mae: 0.194259
- coefficient_stability: 0.8438
- nonzero_count: 4
- sparsity_ratio: 0.7500
- raw_condition_number: 1.5809
- effective_condition_number: 1.5809
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.5120
- median_test_mse: 0.058209
- median_test_mae: 0.194263
- coefficient_stability: 0.8438
- nonzero_count: 16
- sparsity_ratio: 0.0000
- raw_condition_number: 1.5809
- effective_condition_number: 1.5809
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.5120
- median_test_mse: 0.058210
- median_test_mae: 0.194272
- coefficient_stability: 0.8438
- nonzero_count: 4
- sparsity_ratio: 0.7500
- raw_condition_number: 1.5809
- effective_condition_number: 1.5809
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x actuator_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.5072
- median_test_mse: 0.058934
- median_test_mae: 0.177231
- coefficient_stability: 0.3988
- nonzero_count: 128
- sparsity_ratio: 0.6190
- raw_condition_number: inf
- effective_condition_number: 3268.6605
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.4481
- median_test_mse: 0.066762
- median_test_mae: 0.214896
- coefficient_stability: 0.6310
- nonzero_count: 206
- sparsity_ratio: 0.3869
- raw_condition_number: inf
- effective_condition_number: 3486.4951
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.4477
- median_test_mse: 0.066825
- median_test_mae: 0.216041
- coefficient_stability: 0.6447
- nonzero_count: 183
- sparsity_ratio: 0.3980
- raw_condition_number: inf
- effective_condition_number: 3434.0002
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.4450
- median_test_mse: 0.067137
- median_test_mae: 0.215568
- coefficient_stability: 0.4494
- nonzero_count: 213
- sparsity_ratio: 0.3661
- raw_condition_number: inf
- effective_condition_number: 3486.4951
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.4449
- median_test_mse: 0.067161
- median_test_mae: 0.217250
- coefficient_stability: 0.4671
- nonzero_count: 197
- sparsity_ratio: 0.3520
- raw_condition_number: inf
- effective_condition_number: 3434.0002
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.4414
- median_test_mse: 0.067589
- median_test_mae: 0.218216
- coefficient_stability: 0.7566
- nonzero_count: 299
- sparsity_ratio: 0.0164
- raw_condition_number: inf
- effective_condition_number: 3434.0002
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.4231
- median_test_mse: 0.069665
- median_test_mae: 0.224309
- coefficient_stability: 0.7368
- nonzero_count: 12
- sparsity_ratio: 0.8421
- raw_condition_number: inf
- effective_condition_number: 1130.9594
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.4229
- median_test_mse: 0.069829
- median_test_mae: 0.221738
- coefficient_stability: 0.6905
- nonzero_count: 324
- sparsity_ratio: 0.0357
- raw_condition_number: inf
- effective_condition_number: 3486.4951
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.4229
- median_test_mse: 0.069691
- median_test_mae: 0.224527
- coefficient_stability: 0.8421
- nonzero_count: 12
- sparsity_ratio: 0.8421
- raw_condition_number: inf
- effective_condition_number: 1130.9594
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.4229
- median_test_mse: 0.069694
- median_test_mae: 0.224539
- coefficient_stability: 0.8421
- nonzero_count: 76
- sparsity_ratio: 0.0000
- raw_condition_number: inf
- effective_condition_number: 1130.9594
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.3236
- median_test_mse: 0.000376
- median_test_mae: 0.006471
- coefficient_stability: 0.9421
- nonzero_count: 4
- sparsity_ratio: 0.9860
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.3169
- median_test_mse: 0.019231
- median_test_mae: 0.033305
- coefficient_stability: 0.8750
- nonzero_count: 47
- sparsity_ratio: 0.0208
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.3168
- median_test_mse: 0.019231
- median_test_mae: 0.033305
- coefficient_stability: 0.8750
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.3168
- median_test_mse: 0.019231
- median_test_mae: 0.033311
- coefficient_stability: 0.8750
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.3167
- median_test_mse: 0.000383
- median_test_mae: 0.006572
- coefficient_stability: 0.9912
- nonzero_count: 203
- sparsity_ratio: 0.2877
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.3167
- median_test_mse: 0.000383
- median_test_mae: 0.006581
- coefficient_stability: 0.9807
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2990
- median_test_mse: 0.019292
- median_test_mae: 0.032671
- coefficient_stability: 0.8750
- nonzero_count: 24
- sparsity_ratio: 0.0000
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2989
- median_test_mse: 0.019292
- median_test_mae: 0.032678
- coefficient_stability: 0.8750
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2989
- median_test_mse: 0.019292
- median_test_mae: 0.032672
- coefficient_stability: 0.8750
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2976
- median_test_mse: 0.019396
- median_test_mae: 0.032846
- coefficient_stability: 0.8750
- nonzero_count: 47
- sparsity_ratio: 0.0208
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2975
- median_test_mse: 0.019396
- median_test_mae: 0.032853
- coefficient_stability: 0.8750
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2975
- median_test_mse: 0.019396
- median_test_mae: 0.032848
- coefficient_stability: 0.8750
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2622
- median_test_mse: 0.037294
- median_test_mae: 0.061267
- coefficient_stability: 0.9167
- nonzero_count: 24
- sparsity_ratio: 0.0000
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2622
- median_test_mse: 0.037294
- median_test_mae: 0.061268
- coefficient_stability: 0.9167
- nonzero_count: 2
- sparsity_ratio: 0.9167
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2622
- median_test_mse: 0.037294
- median_test_mae: 0.061272
- coefficient_stability: 0.9167
- nonzero_count: 2
- sparsity_ratio: 0.9167
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2617
- median_test_mse: 0.037149
- median_test_mae: 0.060946
- coefficient_stability: 0.9167
- nonzero_count: 48
- sparsity_ratio: 0.0000
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2617
- median_test_mse: 0.037149
- median_test_mae: 0.060946
- coefficient_stability: 0.9167
- nonzero_count: 4
- sparsity_ratio: 0.9167
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2617
- median_test_mse: 0.037150
- median_test_mae: 0.060950
- coefficient_stability: 0.9167
- nonzero_count: 4
- sparsity_ratio: 0.9167
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2594
- median_test_mse: 0.036437
- median_test_mae: 0.060879
- coefficient_stability: 0.8958
- nonzero_count: 48
- sparsity_ratio: 0.0000
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2594
- median_test_mse: 0.036437
- median_test_mae: 0.060879
- coefficient_stability: 0.8958
- nonzero_count: 4
- sparsity_ratio: 0.9167
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2594
- median_test_mse: 0.036437
- median_test_mae: 0.060883
- coefficient_stability: 0.8958
- nonzero_count: 4
- sparsity_ratio: 0.9167
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2417
- median_test_mse: 0.000397
- median_test_mae: 0.007220
- coefficient_stability: 0.9789
- nonzero_count: 18
- sparsity_ratio: 0.9368
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2365
- median_test_mse: 0.000400
- median_test_mae: 0.007418
- coefficient_stability: 1.0000
- nonzero_count: 4
- sparsity_ratio: 0.9860
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.2354
- median_test_mse: 0.000400
- median_test_mae: 0.007421
- coefficient_stability: 1.0000
- nonzero_count: 270
- sparsity_ratio: 0.0526
- raw_condition_number: inf
- effective_condition_number: 1123.6466
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0492
- median_test_mse: 0.000541
- median_test_mae: 0.007647
- coefficient_stability: 0.9917
- nonzero_count: 46
- sparsity_ratio: 0.2333
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0491
- median_test_mse: 0.000541
- median_test_mae: 0.007648
- coefficient_stability: 0.9917
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0491
- median_test_mse: 0.000541
- median_test_mae: 0.007648
- coefficient_stability: 0.9917
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0401
- median_test_mse: 0.147135
- median_test_mae: 0.174416
- coefficient_stability: 0.7833
- nonzero_count: 60
- sparsity_ratio: 0.0000
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0401
- median_test_mse: 0.147135
- median_test_mae: 0.174422
- coefficient_stability: 0.7833
- nonzero_count: 2
- sparsity_ratio: 0.9667
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0401
- median_test_mse: 0.147135
- median_test_mae: 0.174417
- coefficient_stability: 0.7833
- nonzero_count: 2
- sparsity_ratio: 0.9667
- raw_condition_number: 1.5815
- effective_condition_number: 1.5815
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0147
- median_test_mse: 0.118962
- median_test_mae: 0.328653
- coefficient_stability: 0.5000
- nonzero_count: 16
- sparsity_ratio: 0.0000
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0147
- median_test_mse: 0.118962
- median_test_mae: 0.328652
- coefficient_stability: 0.5000
- nonzero_count: 3
- sparsity_ratio: 0.8125
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0147
- median_test_mse: 0.118962
- median_test_mae: 0.328650
- coefficient_stability: 0.5000
- nonzero_count: 3
- sparsity_ratio: 0.8125
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0059
- median_test_mse: 0.000526
- median_test_mae: 0.008449
- coefficient_stability: 1.0000
- nonzero_count: 59
- sparsity_ratio: 0.0167
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0060
- median_test_mse: 0.000526
- median_test_mae: 0.008453
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0060
- median_test_mse: 0.000526
- median_test_mae: 0.008453
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.1065
- median_test_mse: 0.195318
- median_test_mae: 0.224883
- coefficient_stability: 0.8667
- nonzero_count: 12
- sparsity_ratio: 0.8000
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.1065
- median_test_mse: 0.195318
- median_test_mae: 0.224884
- coefficient_stability: 0.8667
- nonzero_count: 60
- sparsity_ratio: 0.0000
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.1065
- median_test_mse: 0.195319
- median_test_mae: 0.224888
- coefficient_stability: 0.8667
- nonzero_count: 12
- sparsity_ratio: 0.8000
- raw_condition_number: 1.5509
- effective_condition_number: 1.5509
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### feature_mapped_linear x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9983
- median_test_mse: 0.000345
- median_test_mae: 0.006182
- coefficient_stability: 0.8496
- nonzero_count: 19
- sparsity_ratio: 0.9675
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9983
- median_test_mse: 0.000348
- median_test_mae: 0.006204
- coefficient_stability: 0.9026
- nonzero_count: 10
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9983
- median_test_mse: 0.000354
- median_test_mae: 0.006409
- coefficient_stability: 0.8521
- nonzero_count: 358
- sparsity_ratio: 0.3880
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### pooled_backend_mode_augmented x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9982
- median_test_mse: 0.000376
- median_test_mae: 0.006471
- coefficient_stability: 0.9476
- nonzero_count: 14
- sparsity_ratio: 0.9556
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9982
- median_test_mse: 0.000382
- median_test_mae: 0.006562
- coefficient_stability: 0.9794
- nonzero_count: 212
- sparsity_ratio: 0.3270
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9982
- median_test_mse: 0.000383
- median_test_mae: 0.006578
- coefficient_stability: 0.9825
- nonzero_count: 10
- sparsity_ratio: 0.9683
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### feature_mapped_linear x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9981
- median_test_mse: 0.000333
- median_test_mae: 0.006659
- coefficient_stability: 0.9556
- nonzero_count: 24
- sparsity_ratio: 0.9590
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9981
- median_test_mse: 0.000333
- median_test_mae: 0.006681
- coefficient_stability: 0.8530
- nonzero_count: 109
- sparsity_ratio: 0.8137
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9980
- median_test_mse: 0.000341
- median_test_mae: 0.006992
- coefficient_stability: 0.9128
- nonzero_count: 514
- sparsity_ratio: 0.1214
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### pooled_backend_mode_augmented x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.000397
- median_test_mae: 0.007501
- coefficient_stability: 0.9810
- nonzero_count: 39
- sparsity_ratio: 0.8762
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.000400
- median_test_mae: 0.007677
- coefficient_stability: 1.0000
- nonzero_count: 23
- sparsity_ratio: 0.9270
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.000408
- median_test_mae: 0.008068
- coefficient_stability: 0.9873
- nonzero_count: 285
- sparsity_ratio: 0.0952
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### feature_mapped_linear x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9937
- median_test_mse: 0.000317
- median_test_mae: 0.004870
- coefficient_stability: 0.8739
- nonzero_count: 79
- sparsity_ratio: 0.8312
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9937
- median_test_mse: 0.000317
- median_test_mae: 0.004897
- coefficient_stability: 0.9530
- nonzero_count: 10
- sparsity_ratio: 0.9786
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9936
- median_test_mse: 0.000321
- median_test_mae: 0.005103
- coefficient_stability: 0.9402
- nonzero_count: 373
- sparsity_ratio: 0.2030
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9928
- median_test_mse: 0.000357
- median_test_mae: 0.006607
- coefficient_stability: 0.8526
- nonzero_count: 80
- sparsity_ratio: 0.8291
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9927
- median_test_mse: 0.000358
- median_test_mae: 0.006624
- coefficient_stability: 0.9530
- nonzero_count: 8
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9926
- median_test_mse: 0.000364
- median_test_mae: 0.006840
- coefficient_stability: 0.9338
- nonzero_count: 387
- sparsity_ratio: 0.1731
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9924
- median_test_mse: 0.000386
- median_test_mae: 0.005777
- coefficient_stability: 0.9683
- nonzero_count: 18
- sparsity_ratio: 0.9286
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9923
- median_test_mse: 0.000388
- median_test_mae: 0.005951
- coefficient_stability: 1.0000
- nonzero_count: 10
- sparsity_ratio: 0.9603
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9922
- median_test_mse: 0.000394
- median_test_mae: 0.006259
- coefficient_stability: 1.0000
- nonzero_count: 214
- sparsity_ratio: 0.1508
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### feature_mapped_linear x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9905
- median_test_mse: 0.000482
- median_test_mae: 0.006363
- coefficient_stability: 0.8376
- nonzero_count: 41
- sparsity_ratio: 0.8248
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9905
- median_test_mse: 0.000483
- median_test_mae: 0.006392
- coefficient_stability: 0.9359
- nonzero_count: 6
- sparsity_ratio: 0.9744
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9904
- median_test_mse: 0.000486
- median_test_mae: 0.006488
- coefficient_stability: 0.9231
- nonzero_count: 194
- sparsity_ratio: 0.1709
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### pooled_backend_mode_augmented x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9897
- median_test_mse: 0.000505
- median_test_mae: 0.008765
- coefficient_stability: 0.9643
- nonzero_count: 26
- sparsity_ratio: 0.8968
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9897
- median_test_mse: 0.000508
- median_test_mae: 0.008894
- coefficient_stability: 1.0000
- nonzero_count: 12
- sparsity_ratio: 0.9524
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9897
- median_test_mse: 0.000509
- median_test_mae: 0.009049
- coefficient_stability: 1.0000
- nonzero_count: 221
- sparsity_ratio: 0.1230
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9883
- median_test_mse: 0.000594
- median_test_mae: 0.007629
- coefficient_stability: 0.9683
- nonzero_count: 10
- sparsity_ratio: 0.9206
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9882
- median_test_mse: 0.000598
- median_test_mae: 0.007855
- coefficient_stability: 1.0000
- nonzero_count: 6
- sparsity_ratio: 0.9524
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9881
- median_test_mse: 0.000602
- median_test_mae: 0.008049
- coefficient_stability: 1.0000
- nonzero_count: 110
- sparsity_ratio: 0.1270
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8070
- median_test_mse: 0.000423
- median_test_mae: 0.005054
- coefficient_stability: 0.9960
- nonzero_count: 133
- sparsity_ratio: 0.4722
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8069
- median_test_mse: 0.000419
- median_test_mae: 0.004985
- coefficient_stability: 0.9484
- nonzero_count: 2
- sparsity_ratio: 0.9921
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8068
- median_test_mse: 0.000424
- median_test_mae: 0.005083
- coefficient_stability: 0.9960
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### feature_mapped_linear x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7963
- median_test_mse: 0.000399
- median_test_mae: 0.004845
- coefficient_stability: 0.9231
- nonzero_count: 201
- sparsity_ratio: 0.5705
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7960
- median_test_mse: 0.000399
- median_test_mae: 0.004836
- coefficient_stability: 0.8782
- nonzero_count: 3
- sparsity_ratio: 0.9936
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7959
- median_test_mse: 0.000398
- median_test_mae: 0.004844
- coefficient_stability: 0.9295
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7422
- median_test_mse: 0.000443
- median_test_mae: 0.006329
- coefficient_stability: 0.9071
- nonzero_count: 231
- sparsity_ratio: 0.5064
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7417
- median_test_mse: 0.000442
- median_test_mae: 0.006362
- coefficient_stability: 0.9071
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7417
- median_test_mse: 0.000442
- median_test_mae: 0.006339
- coefficient_stability: 0.8632
- nonzero_count: 4
- sparsity_ratio: 0.9915
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7175
- median_test_mse: 0.000662
- median_test_mae: 0.006647
- coefficient_stability: 0.9960
- nonzero_count: 77
- sparsity_ratio: 0.3889
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7174
- median_test_mse: 0.000655
- median_test_mae: 0.006542
- coefficient_stability: 0.9484
- nonzero_count: 2
- sparsity_ratio: 0.9841
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7173
- median_test_mse: 0.000664
- median_test_mae: 0.006675
- coefficient_stability: 0.9960
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### feature_mapped_linear x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7034
- median_test_mse: 0.000620
- median_test_mae: 0.006303
- coefficient_stability: 0.9060
- nonzero_count: 113
- sparsity_ratio: 0.5171
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7031
- median_test_mse: 0.000621
- median_test_mae: 0.006310
- coefficient_stability: 0.8483
- nonzero_count: 2
- sparsity_ratio: 0.9915
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.7030
- median_test_mse: 0.000621
- median_test_mae: 0.006325
- coefficient_stability: 0.9081
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6815
- median_test_mse: 0.037955
- median_test_mae: 0.135869
- coefficient_stability: 0.5737
- nonzero_count: 12
- sparsity_ratio: 0.9231
- raw_condition_number: inf
- effective_condition_number: 1016.1104
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6756
- median_test_mse: 0.000545
- median_test_mae: 0.007604
- coefficient_stability: 0.9921
- nonzero_count: 158
- sparsity_ratio: 0.3730
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6754
- median_test_mse: 0.000546
- median_test_mae: 0.007623
- coefficient_stability: 0.9861
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6753
- median_test_mse: 0.000544
- median_test_mae: 0.007602
- coefficient_stability: 0.9365
- nonzero_count: 4
- sparsity_ratio: 0.9841
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### feature_mapped_linear x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6713
- median_test_mse: 0.039198
- median_test_mae: 0.138562
- coefficient_stability: 0.5833
- nonzero_count: 6
- sparsity_ratio: 0.9615
- raw_condition_number: inf
- effective_condition_number: 1016.1104
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6705
- median_test_mse: 0.039291
- median_test_mae: 0.138828
- coefficient_stability: 0.6122
- nonzero_count: 131
- sparsity_ratio: 0.1603
- raw_condition_number: inf
- effective_condition_number: 1016.1104
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6457
- median_test_mse: 0.042778
- median_test_mae: 0.166834
- coefficient_stability: 0.8269
- nonzero_count: 36
- sparsity_ratio: 0.7692
- raw_condition_number: inf
- effective_condition_number: 10389.6157
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6401
- median_test_mse: 0.043458
- median_test_mae: 0.166800
- coefficient_stability: 0.6538
- nonzero_count: 40
- sparsity_ratio: 0.7436
- raw_condition_number: inf
- effective_condition_number: 10389.6157
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6247
- median_test_mse: 0.045320
- median_test_mae: 0.175235
- coefficient_stability: 0.8333
- nonzero_count: 152
- sparsity_ratio: 0.0256
- raw_condition_number: inf
- effective_condition_number: 10389.6157
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### pooled_backend_mode_augmented x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6085
- median_test_mse: 0.046632
- median_test_mae: 0.163373
- coefficient_stability: 0.7619
- nonzero_count: 76
- sparsity_ratio: 0.0952
- raw_condition_number: inf
- effective_condition_number: 722.2598
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6085
- median_test_mse: 0.046633
- median_test_mae: 0.163382
- coefficient_stability: 0.7619
- nonzero_count: 5
- sparsity_ratio: 0.9405
- raw_condition_number: inf
- effective_condition_number: 722.2598
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.6084
- median_test_mse: 0.046636
- median_test_mae: 0.163280
- coefficient_stability: 0.7381
- nonzero_count: 12
- sparsity_ratio: 0.8571
- raw_condition_number: inf
- effective_condition_number: 722.2598
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4462
- median_test_mse: 0.066855
- median_test_mae: 0.219512
- coefficient_stability: 0.6429
- nonzero_count: 20
- sparsity_ratio: 0.7619
- raw_condition_number: inf
- effective_condition_number: 1177.6133
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4452
- median_test_mse: 0.066981
- median_test_mae: 0.220598
- coefficient_stability: 0.7262
- nonzero_count: 20
- sparsity_ratio: 0.7619
- raw_condition_number: inf
- effective_condition_number: 1177.6133
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4304
- median_test_mse: 0.068789
- median_test_mae: 0.223638
- coefficient_stability: 0.7619
- nonzero_count: 80
- sparsity_ratio: 0.0476
- raw_condition_number: inf
- effective_condition_number: 1177.6133
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### feature_mapped_linear x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3642
- median_test_mse: 0.000333
- median_test_mae: 0.006658
- coefficient_stability: 0.9556
- nonzero_count: 11
- sparsity_ratio: 0.9812
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3635
- median_test_mse: 0.000333
- median_test_mae: 0.006681
- coefficient_stability: 0.8530
- nonzero_count: 97
- sparsity_ratio: 0.8342
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3610
- median_test_mse: 0.000345
- median_test_mae: 0.006182
- coefficient_stability: 0.8496
- nonzero_count: 9
- sparsity_ratio: 0.9846
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3591
- median_test_mse: 0.000348
- median_test_mae: 0.006210
- coefficient_stability: 0.9034
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3514
- median_test_mse: 0.000356
- median_test_mae: 0.006351
- coefficient_stability: 0.9274
- nonzero_count: 307
- sparsity_ratio: 0.4752
- raw_condition_number: inf
- effective_condition_number: 1013.7843
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3510
- median_test_mse: 0.000340
- median_test_mae: 0.006829
- coefficient_stability: 0.9624
- nonzero_count: 466
- sparsity_ratio: 0.2034
- raw_condition_number: inf
- effective_condition_number: 10353.5270
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### pooled_backend_mode_augmented x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3236
- median_test_mse: 0.000376
- median_test_mae: 0.006471
- coefficient_stability: 0.9476
- nonzero_count: 4
- sparsity_ratio: 0.9873
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3167
- median_test_mse: 0.000383
- median_test_mae: 0.006572
- coefficient_stability: 0.9921
- nonzero_count: 203
- sparsity_ratio: 0.3556
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3167
- median_test_mse: 0.000383
- median_test_mae: 0.006581
- coefficient_stability: 0.9825
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 719.9767
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2416
- median_test_mse: 0.000397
- median_test_mae: 0.007501
- coefficient_stability: 0.9810
- nonzero_count: 26
- sparsity_ratio: 0.9175
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2376
- median_test_mse: 0.000399
- median_test_mae: 0.007440
- coefficient_stability: 1.0000
- nonzero_count: 277
- sparsity_ratio: 0.1206
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2361
- median_test_mse: 0.000400
- median_test_mae: 0.007673
- coefficient_stability: 1.0000
- nonzero_count: 10
- sparsity_ratio: 0.9683
- raw_condition_number: inf
- effective_condition_number: 1169.8804
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

## Skipped
- 无。