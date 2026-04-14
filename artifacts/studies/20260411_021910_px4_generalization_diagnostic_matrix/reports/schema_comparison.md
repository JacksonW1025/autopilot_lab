# Schema Comparison: px4_generalization_diagnostic_matrix

## Results
### full_augmented x next_raw_state | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.9991
- median_test_mse: 0.000260
- median_test_mae: 0.004153
- coefficient_stability: 0.9205
- nonzero_count: 31
- sparsity_ratio: 0.9765
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9991
- median_test_mse: 0.000259
- median_test_mae: 0.004706
- coefficient_stability: 0.9587
- nonzero_count: 29
- sparsity_ratio: 0.9780
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9990
- median_test_mse: 0.000259
- median_test_mae: 0.005571
- coefficient_stability: 0.9451
- nonzero_count: 546
- sparsity_ratio: 0.5864
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.9990
- median_test_mse: 0.000291
- median_test_mae: 0.004123
- coefficient_stability: 0.9105
- nonzero_count: 26
- sparsity_ratio: 0.9772
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9990
- median_test_mse: 0.000290
- median_test_mae: 0.004691
- coefficient_stability: 0.9566
- nonzero_count: 29
- sparsity_ratio: 0.9746
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9989
- median_test_mse: 0.000297
- median_test_mae: 0.005615
- coefficient_stability: 0.9417
- nonzero_count: 450
- sparsity_ratio: 0.6053
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9989
- median_test_mse: 0.000281
- median_test_mae: 0.004973
- coefficient_stability: 0.9750
- nonzero_count: 47
- sparsity_ratio: 0.9644
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9988
- median_test_mse: 0.000306
- median_test_mae: 0.004906
- coefficient_stability: 0.9702
- nonzero_count: 44
- sparsity_ratio: 0.9614
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9986
- median_test_mse: 0.000361
- median_test_mae: 0.004688
- coefficient_stability: 0.9394
- nonzero_count: 71
- sparsity_ratio: 0.9462
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x next_raw_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9985
- median_test_mse: 0.000358
- median_test_mae: 0.006751
- coefficient_stability: 0.9674
- nonzero_count: 1050
- sparsity_ratio: 0.2045
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9985
- median_test_mse: 0.000383
- median_test_mae: 0.004618
- coefficient_stability: 0.9360
- nonzero_count: 70
- sparsity_ratio: 0.9386
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x next_raw_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9984
- median_test_mse: 0.000386
- median_test_mae: 0.006617
- coefficient_stability: 0.9649
- nonzero_count: 912
- sparsity_ratio: 0.2000
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x next_raw_state | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.000636
- median_test_mae: 0.008101
- coefficient_stability: 0.9404
- nonzero_count: 10
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.000639
- median_test_mae: 0.008176
- coefficient_stability: 0.9789
- nonzero_count: 239
- sparsity_ratio: 0.1614
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9976
- median_test_mse: 0.000641
- median_test_mae: 0.008199
- coefficient_stability: 0.9930
- nonzero_count: 10
- sparsity_ratio: 0.9649
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x future_state_horizon | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9970
- median_test_mse: 0.000212
- median_test_mae: 0.003401
- coefficient_stability: 0.9735
- nonzero_count: 14
- sparsity_ratio: 0.9867
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x next_raw_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9967
- median_test_mse: 0.000813
- median_test_mae: 0.009284
- coefficient_stability: 0.9825
- nonzero_count: 17
- sparsity_ratio: 0.9404
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x next_raw_state | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9967
- median_test_mse: 0.000818
- median_test_mae: 0.009285
- coefficient_stability: 0.9965
- nonzero_count: 268
- sparsity_ratio: 0.0596
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x future_state_horizon | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9966
- median_test_mse: 0.000247
- median_test_mae: 0.003242
- coefficient_stability: 0.9715
- nonzero_count: 15
- sparsity_ratio: 0.9836
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9965
- median_test_mse: 0.000251
- median_test_mae: 0.004223
- coefficient_stability: 0.9792
- nonzero_count: 677
- sparsity_ratio: 0.3589
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9962
- median_test_mse: 0.000294
- median_test_mae: 0.003533
- coefficient_stability: 0.9403
- nonzero_count: 30
- sparsity_ratio: 0.9716
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9960
- median_test_mse: 0.000293
- median_test_mae: 0.004061
- coefficient_stability: 0.9748
- nonzero_count: 576
- sparsity_ratio: 0.3684
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9958
- median_test_mse: 0.000325
- median_test_mae: 0.003342
- coefficient_stability: 0.9386
- nonzero_count: 26
- sparsity_ratio: 0.9715
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9956
- median_test_mse: 0.000320
- median_test_mae: 0.004523
- coefficient_stability: 0.9640
- nonzero_count: 9
- sparsity_ratio: 0.9830
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x next_raw_state | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9955
- median_test_mse: 0.001145
- median_test_mae: 0.009267
- coefficient_stability: 0.9614
- nonzero_count: 17
- sparsity_ratio: 0.9404
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x selected_state_subset | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9950
- median_test_mse: 0.000363
- median_test_mae: 0.005503
- coefficient_stability: 0.9697
- nonzero_count: 361
- sparsity_ratio: 0.3163
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9949
- median_test_mse: 0.000377
- median_test_mae: 0.004433
- coefficient_stability: 0.9649
- nonzero_count: 8
- sparsity_ratio: 0.9825
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9945
- median_test_mse: 0.000422
- median_test_mae: 0.004673
- coefficient_stability: 0.9205
- nonzero_count: 16
- sparsity_ratio: 0.9697
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9941
- median_test_mse: 0.000434
- median_test_mae: 0.005433
- coefficient_stability: 0.9715
- nonzero_count: 312
- sparsity_ratio: 0.3158
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9939
- median_test_mse: 0.000474
- median_test_mae: 0.004555
- coefficient_stability: 0.9211
- nonzero_count: 15
- sparsity_ratio: 0.9671
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9930
- median_test_mse: 0.000519
- median_test_mae: 0.007087
- coefficient_stability: 0.9498
- nonzero_count: 24
- sparsity_ratio: 0.9773
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9926
- median_test_mse: 0.000544
- median_test_mae: 0.007505
- coefficient_stability: 0.9754
- nonzero_count: 774
- sparsity_ratio: 0.2670
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x future_state_horizon | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9923
- median_test_mse: 0.000594
- median_test_mae: 0.006088
- coefficient_stability: 0.9781
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x future_state_horizon | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9922
- median_test_mse: 0.000599
- median_test_mae: 0.006065
- coefficient_stability: 0.9956
- nonzero_count: 204
- sparsity_ratio: 0.1053
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x window_summary_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9921
- median_test_mse: 0.000597
- median_test_mae: 0.007276
- coefficient_stability: 0.8968
- nonzero_count: 45
- sparsity_ratio: 0.9574
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9918
- median_test_mse: 0.000615
- median_test_mae: 0.007664
- coefficient_stability: 0.9572
- nonzero_count: 23
- sparsity_ratio: 0.9748
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9911
- median_test_mse: 0.000667
- median_test_mae: 0.008283
- coefficient_stability: 0.9682
- nonzero_count: 678
- sparsity_ratio: 0.2566
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9910
- median_test_mse: 0.000692
- median_test_mae: 0.007785
- coefficient_stability: 0.9134
- nonzero_count: 47
- sparsity_ratio: 0.9485
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x future_state_horizon | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9891
- median_test_mse: 0.000901
- median_test_mae: 0.006054
- coefficient_stability: 0.9693
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x window_summary_response | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9882
- median_test_mse: 0.000896
- median_test_mae: 0.009552
- coefficient_stability: 0.9825
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x window_summary_response | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9882
- median_test_mse: 0.000902
- median_test_mae: 0.009539
- coefficient_stability: 1.0000
- nonzero_count: 217
- sparsity_ratio: 0.0482
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.9881
- median_test_mse: 0.000918
- median_test_mae: 0.008066
- coefficient_stability: 0.9737
- nonzero_count: 3
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | lasso_affine | pooled
- support: `supported`
- median_test_r2: 0.9881
- median_test_mse: 0.000921
- median_test_mae: 0.008046
- coefficient_stability: 0.9912
- nonzero_count: 104
- sparsity_ratio: 0.0877
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x window_summary_response | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9856
- median_test_mse: 0.001152
- median_test_mae: 0.009566
- coefficient_stability: 0.9474
- nonzero_count: 6
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ols_affine | pooled
- support: `supported`
- median_test_r2: 0.9840
- median_test_mse: 0.001330
- median_test_mae: 0.008027
- coefficient_stability: 0.9561
- nonzero_count: 3
- sparsity_ratio: 0.9737
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x future_state_horizon | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9489
- median_test_mse: 0.000220
- median_test_mae: 0.003843
- coefficient_stability: 0.9811
- nonzero_count: 245
- sparsity_ratio: 0.7680
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9480
- median_test_mse: 0.000234
- median_test_mae: 0.003469
- coefficient_stability: 0.9730
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x future_state_horizon | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.9466
- median_test_mse: 0.000240
- median_test_mae: 0.003510
- coefficient_stability: 0.9290
- nonzero_count: 11
- sparsity_ratio: 0.9896
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9413
- median_test_mse: 0.000271
- median_test_mae: 0.003725
- coefficient_stability: 0.9770
- nonzero_count: 186
- sparsity_ratio: 0.7961
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9403
- median_test_mse: 0.000276
- median_test_mae: 0.003293
- coefficient_stability: 0.9731
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x future_state_horizon | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.9392
- median_test_mse: 0.000280
- median_test_mae: 0.003292
- coefficient_stability: 0.9194
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9204
- median_test_mse: 0.000329
- median_test_mae: 0.004999
- coefficient_stability: 0.9744
- nonzero_count: 147
- sparsity_ratio: 0.7216
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9192
- median_test_mse: 0.000348
- median_test_mae: 0.004476
- coefficient_stability: 0.9602
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x selected_state_subset | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.9172
- median_test_mse: 0.000360
- median_test_mae: 0.004527
- coefficient_stability: 0.9081
- nonzero_count: 5
- sparsity_ratio: 0.9905
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9077
- median_test_mse: 0.000416
- median_test_mae: 0.005054
- coefficient_stability: 0.9715
- nonzero_count: 108
- sparsity_ratio: 0.7632
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9063
- median_test_mse: 0.000420
- median_test_mae: 0.004473
- coefficient_stability: 0.9638
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x selected_state_subset | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.9044
- median_test_mse: 0.000430
- median_test_mae: 0.004475
- coefficient_stability: 0.9013
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x future_state_horizon | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.9024
- median_test_mse: 0.000626
- median_test_mae: 0.005885
- coefficient_stability: 1.0000
- nonzero_count: 156
- sparsity_ratio: 0.3158
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x future_state_horizon | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.9023
- median_test_mse: 0.000629
- median_test_mae: 0.005920
- coefficient_stability: 0.9956
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x future_state_horizon | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.9019
- median_test_mse: 0.000623
- median_test_mae: 0.005826
- coefficient_stability: 0.9474
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.8546
- median_test_mse: 0.000965
- median_test_mae: 0.007784
- coefficient_stability: 1.0000
- nonzero_count: 84
- sparsity_ratio: 0.2632
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x selected_state_subset | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.8545
- median_test_mse: 0.000968
- median_test_mae: 0.007816
- coefficient_stability: 0.9912
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x window_summary_response | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.8540
- median_test_mse: 0.000541
- median_test_mae: 0.007356
- coefficient_stability: 0.9621
- nonzero_count: 344
- sparsity_ratio: 0.6742
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x selected_state_subset | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.8538
- median_test_mse: 0.000960
- median_test_mae: 0.007694
- coefficient_stability: 0.9298
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x window_summary_response | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.8511
- median_test_mse: 0.000543
- median_test_mae: 0.007142
- coefficient_stability: 0.9432
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x window_summary_response | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.8479
- median_test_mse: 0.000685
- median_test_mae: 0.007343
- coefficient_stability: 0.8712
- nonzero_count: 7
- sparsity_ratio: 0.9934
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.8284
- median_test_mse: 0.000627
- median_test_mae: 0.007574
- coefficient_stability: 0.9496
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.8271
- median_test_mse: 0.000652
- median_test_mae: 0.007952
- coefficient_stability: 0.9688
- nonzero_count: 297
- sparsity_ratio: 0.6743
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x window_summary_response | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.8264
- median_test_mse: 0.000763
- median_test_mae: 0.007745
- coefficient_stability: 0.8766
- nonzero_count: 1
- sparsity_ratio: 0.9989
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x window_summary_response | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.8130
- median_test_mse: 0.000921
- median_test_mae: 0.009278
- coefficient_stability: 0.9912
- nonzero_count: 179
- sparsity_ratio: 0.2149
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x window_summary_response | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.8128
- median_test_mse: 0.000923
- median_test_mae: 0.009304
- coefficient_stability: 0.9868
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x window_summary_response | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.8125
- median_test_mse: 0.000916
- median_test_mae: 0.009230
- coefficient_stability: 0.9211
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x delta_state | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.7536
- median_test_mse: 0.000251
- median_test_mae: 0.004328
- coefficient_stability: 0.9629
- nonzero_count: 23
- sparsity_ratio: 0.9826
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.7528
- median_test_mse: 0.000260
- median_test_mae: 0.004153
- coefficient_stability: 0.9205
- nonzero_count: 29
- sparsity_ratio: 0.9780
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | ridge_affine | stratified
- support: `supported`
- median_test_r2: 0.7270
- median_test_mse: 0.000282
- median_test_mae: 0.004317
- coefficient_stability: 0.9627
- nonzero_count: 23
- sparsity_ratio: 0.9798
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | ols_affine | stratified
- support: `supported`
- median_test_r2: 0.7257
- median_test_mse: 0.000291
- median_test_mae: 0.004123
- coefficient_stability: 0.9105
- nonzero_count: 24
- sparsity_ratio: 0.9789
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | lasso_affine | stratified
- support: `supported`
- median_test_r2: 0.7159
- median_test_mse: 0.000252
- median_test_mae: 0.005310
- coefficient_stability: 0.9765
- nonzero_count: 462
- sparsity_ratio: 0.6500
- raw_condition_number: inf
- effective_condition_number: 2455.3807
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | ridge_affine | pooled
- support: `supported`
- median_test_r2: 0.7102
- median_test_mse: 0.000282
- median_test_mae: 0.004718
- coefficient_stability: 0.9750
- nonzero_count: 44
- sparsity_ratio: 0.9667
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.6850
- median_test_mse: 0.000306
- median_test_mae: 0.004654
- coefficient_stability: 0.9711
- nonzero_count: 42
- sparsity_ratio: 0.9632
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.6835
- median_test_mse: 0.000290
- median_test_mae: 0.005361
- coefficient_stability: 0.9754
- nonzero_count: 368
- sparsity_ratio: 0.6772
- raw_condition_number: inf
- effective_condition_number: 2285.3534
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.6734
- median_test_mse: 0.000318
- median_test_mae: 0.006166
- coefficient_stability: 0.9879
- nonzero_count: 952
- sparsity_ratio: 0.2788
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.6414
- median_test_mse: 0.000349
- median_test_mae: 0.006113
- coefficient_stability: 0.9860
- nonzero_count: 823
- sparsity_ratio: 0.2781
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x delta_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.6300
- median_test_mse: 0.000361
- median_test_mae: 0.004688
- coefficient_stability: 0.9394
- nonzero_count: 71
- sparsity_ratio: 0.9462
- raw_condition_number: inf
- effective_condition_number: 3029.9939
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x delta_state | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.6077
- median_test_mse: 0.000383
- median_test_mae: 0.004618
- coefficient_stability: 0.9360
- nonzero_count: 69
- sparsity_ratio: 0.9395
- raw_condition_number: inf
- effective_condition_number: 2861.7963
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.5288
- median_test_mse: 0.057946
- median_test_mae: 0.197998
- coefficient_stability: 0.6809
- nonzero_count: 148
- sparsity_ratio: 0.5132
- raw_condition_number: inf
- effective_condition_number: 2870.4668
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.5264
- median_test_mse: 0.058242
- median_test_mae: 0.196850
- coefficient_stability: 0.6756
- nonzero_count: 160
- sparsity_ratio: 0.5238
- raw_condition_number: inf
- effective_condition_number: 2927.4021
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.5259
- median_test_mse: 0.058312
- median_test_mae: 0.197247
- coefficient_stability: 0.8363
- nonzero_count: 332
- sparsity_ratio: 0.0119
- raw_condition_number: inf
- effective_condition_number: 2927.4021
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.5256
- median_test_mse: 0.058341
- median_test_mae: 0.198637
- coefficient_stability: 0.8586
- nonzero_count: 303
- sparsity_ratio: 0.0033
- raw_condition_number: inf
- effective_condition_number: 2870.4668
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.5228
- median_test_mse: 0.058686
- median_test_mae: 0.198607
- coefficient_stability: 0.5789
- nonzero_count: 165
- sparsity_ratio: 0.4572
- raw_condition_number: inf
- effective_condition_number: 2870.4668
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x actuator_response | ridge_affine | pooled
- support: `partial`
- median_test_r2: 0.5138
- median_test_mse: 0.059704
- median_test_mae: 0.201833
- coefficient_stability: 0.8684
- nonzero_count: 20
- sparsity_ratio: 0.7368
- raw_condition_number: inf
- effective_condition_number: 614.5191
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x actuator_response | lasso_affine | pooled
- support: `partial`
- median_test_r2: 0.5137
- median_test_mse: 0.059714
- median_test_mae: 0.201867
- coefficient_stability: 0.8684
- nonzero_count: 76
- sparsity_ratio: 0.0000
- raw_condition_number: inf
- effective_condition_number: 614.5191
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.5034
- median_test_mse: 0.061096
- median_test_mae: 0.198274
- coefficient_stability: 0.5685
- nonzero_count: 180
- sparsity_ratio: 0.4643
- raw_condition_number: inf
- effective_condition_number: 2927.4021
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x actuator_response | ols_affine | pooled
- support: `partial`
- median_test_r2: 0.4902
- median_test_mse: 0.062635
- median_test_mae: 0.202156
- coefficient_stability: 0.7632
- nonzero_count: 20
- sparsity_ratio: 0.7368
- raw_condition_number: inf
- effective_condition_number: 614.5191
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state_history x actuator_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.4782
- median_test_mse: 0.063691
- median_test_mae: 0.178602
- coefficient_stability: 0.5280
- nonzero_count: 54
- sparsity_ratio: 0.8224
- raw_condition_number: inf
- effective_condition_number: 2289.9502
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.4493
- median_test_mse: 0.067201
- median_test_mae: 0.185647
- coefficient_stability: 0.6760
- nonzero_count: 293
- sparsity_ratio: 0.0362
- raw_condition_number: inf
- effective_condition_number: 2289.9502
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x actuator_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.4458
- median_test_mse: 0.067583
- median_test_mae: 0.190127
- coefficient_stability: 0.6447
- nonzero_count: 8
- sparsity_ratio: 0.8947
- raw_condition_number: inf
- effective_condition_number: 453.9219
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x actuator_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.4446
- median_test_mse: 0.067735
- median_test_mae: 0.190689
- coefficient_stability: 0.6908
- nonzero_count: 76
- sparsity_ratio: 0.0000
- raw_condition_number: inf
- effective_condition_number: 453.9219
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x actuator_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.4446
- median_test_mse: 0.067736
- median_test_mae: 0.190681
- coefficient_stability: 0.6908
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 453.9219
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### full_augmented x actuator_response | ridge_affine | stratified
- support: `partial`
- median_test_r2: 0.4417
- median_test_mse: 0.068268
- median_test_mae: 0.181714
- coefficient_stability: 0.5208
- nonzero_count: 58
- sparsity_ratio: 0.8274
- raw_condition_number: inf
- effective_condition_number: 2301.4729
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state_history x actuator_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.4350
- median_test_mse: 0.069020
- median_test_mae: 0.178153
- coefficient_stability: 0.4474
- nonzero_count: 133
- sparsity_ratio: 0.5625
- raw_condition_number: inf
- effective_condition_number: 2289.9502
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x actuator_response | ols_affine | stratified
- support: `partial`
- median_test_r2: 0.4085
- median_test_mse: 0.072354
- median_test_mae: 0.180521
- coefficient_stability: 0.4241
- nonzero_count: 115
- sparsity_ratio: 0.6577
- raw_condition_number: inf
- effective_condition_number: 2301.4729
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### full_augmented x actuator_response | lasso_affine | stratified
- support: `partial`
- median_test_r2: 0.4072
- median_test_mse: 0.072481
- median_test_mae: 0.189401
- coefficient_stability: 0.6533
- nonzero_count: 321
- sparsity_ratio: 0.0446
- raw_condition_number: inf
- effective_condition_number: 2301.4729
- conditioning_pruned_features: altitude, altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_offboard_attitude, mode_posctl, vertical_speed, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: altitude__lag_1, altitude__lag_2, altitude__lag_3, mode_posctl, vertical_speed__lag_1, vertical_speed__lag_2, vertical_speed__lag_3

### commands_plus_state x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2444
- median_test_mse: 0.000636
- median_test_mae: 0.008101
- coefficient_stability: 0.9404
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2419
- median_test_mse: 0.000641
- median_test_mae: 0.008188
- coefficient_stability: 1.0000
- nonzero_count: 219
- sparsity_ratio: 0.2316
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.2417
- median_test_mse: 0.000641
- median_test_mae: 0.008195
- coefficient_stability: 0.9930
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1911
- median_test_mse: 0.064678
- median_test_mae: 0.091603
- coefficient_stability: 0.8750
- nonzero_count: 24
- sparsity_ratio: 0.0000
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1911
- median_test_mse: 0.064678
- median_test_mae: 0.091604
- coefficient_stability: 0.8750
- nonzero_count: 1
- sparsity_ratio: 0.9583
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1911
- median_test_mse: 0.064678
- median_test_mae: 0.091606
- coefficient_stability: 0.8750
- nonzero_count: 1
- sparsity_ratio: 0.9583
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1908
- median_test_mse: 0.064331
- median_test_mae: 0.091233
- coefficient_stability: 0.8750
- nonzero_count: 48
- sparsity_ratio: 0.0000
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1908
- median_test_mse: 0.064331
- median_test_mae: 0.091234
- coefficient_stability: 0.8750
- nonzero_count: 2
- sparsity_ratio: 0.9583
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1908
- median_test_mse: 0.064331
- median_test_mae: 0.091235
- coefficient_stability: 0.8750
- nonzero_count: 2
- sparsity_ratio: 0.9583
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1898
- median_test_mse: 0.063063
- median_test_mae: 0.091193
- coefficient_stability: 0.8958
- nonzero_count: 47
- sparsity_ratio: 0.0208
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1898
- median_test_mse: 0.063063
- median_test_mae: 0.091194
- coefficient_stability: 0.8958
- nonzero_count: 2
- sparsity_ratio: 0.9583
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1898
- median_test_mse: 0.063063
- median_test_mae: 0.091195
- coefficient_stability: 0.8958
- nonzero_count: 2
- sparsity_ratio: 0.9583
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1591
- median_test_mse: 0.000813
- median_test_mae: 0.009280
- coefficient_stability: 0.9965
- nonzero_count: 266
- sparsity_ratio: 0.0667
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.1560
- median_test_mse: 0.000816
- median_test_mae: 0.009284
- coefficient_stability: 0.9895
- nonzero_count: 4
- sparsity_ratio: 0.9860
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0596
- median_test_mse: 0.000807
- median_test_mae: 0.009435
- coefficient_stability: 1.0000
- nonzero_count: 53
- sparsity_ratio: 0.1167
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0596
- median_test_mse: 0.000807
- median_test_mae: 0.009437
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0596
- median_test_mse: 0.000807
- median_test_mae: 0.009437
- coefficient_stability: 1.0000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0238
- median_test_mse: 0.119672
- median_test_mae: 0.305279
- coefficient_stability: 0.5000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0346
- effective_condition_number: 1.0346
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0238
- median_test_mse: 0.119674
- median_test_mae: 0.305278
- coefficient_stability: 0.5000
- nonzero_count: 16
- sparsity_ratio: 0.0000
- raw_condition_number: 1.0346
- effective_condition_number: 1.0346
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: 0.0238
- median_test_mse: 0.119676
- median_test_mae: 0.305277
- coefficient_stability: 0.5000
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0346
- effective_condition_number: 1.0346
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0016
- median_test_mse: 0.122688
- median_test_mae: 0.338207
- coefficient_stability: 0.7500
- nonzero_count: 16
- sparsity_ratio: 0.0000
- raw_condition_number: 1.0368
- effective_condition_number: 1.0368
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0016
- median_test_mse: 0.122688
- median_test_mae: 0.338207
- coefficient_stability: 0.7500
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0368
- effective_condition_number: 1.0368
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x actuator_response | ols_affine | pooled
- support: `unsupported`
- median_test_r2: 0.0016
- median_test_mse: 0.122688
- median_test_mae: 0.338207
- coefficient_stability: 0.7500
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0368
- effective_condition_number: 1.0368
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0037
- median_test_mse: 0.000970
- median_test_mae: 0.009995
- coefficient_stability: 0.9833
- nonzero_count: 59
- sparsity_ratio: 0.0167
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0038
- median_test_mse: 0.000970
- median_test_mae: 0.009997
- coefficient_stability: 0.9833
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0038
- median_test_mse: 0.000970
- median_test_mae: 0.009997
- coefficient_stability: 0.9833
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0328
- median_test_mse: 0.055708
- median_test_mae: 0.063636
- coefficient_stability: 0.9583
- nonzero_count: 22
- sparsity_ratio: 0.0833
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0329
- median_test_mse: 0.055705
- median_test_mae: 0.063639
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x selected_state_subset | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0329
- median_test_mse: 0.055709
- median_test_mae: 0.063637
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0338
- median_test_mse: 0.055568
- median_test_mae: 0.063528
- coefficient_stability: 0.9583
- nonzero_count: 45
- sparsity_ratio: 0.0625
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0339
- median_test_mse: 0.055566
- median_test_mae: 0.063530
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x future_state_horizon | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0339
- median_test_mse: 0.055569
- median_test_mae: 0.063529
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0390
- median_test_mse: 0.054726
- median_test_mae: 0.064113
- coefficient_stability: 0.9583
- nonzero_count: 45
- sparsity_ratio: 0.0625
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0391
- median_test_mse: 0.054723
- median_test_mae: 0.064115
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x window_summary_response | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.0391
- median_test_mse: 0.054727
- median_test_mae: 0.064114
- coefficient_stability: 0.9583
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0417
- median_test_mse: 0.260208
- median_test_mae: 0.250647
- coefficient_stability: 0.7167
- nonzero_count: 60
- sparsity_ratio: 0.0000
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ridge_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0417
- median_test_mse: 0.260208
- median_test_mae: 0.250648
- coefficient_stability: 0.7167
- nonzero_count: 3
- sparsity_ratio: 0.9500
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.0417
- median_test_mse: 0.260209
- median_test_mae: 0.250649
- coefficient_stability: 0.7167
- nonzero_count: 3
- sparsity_ratio: 0.9500
- raw_condition_number: 1.0369
- effective_condition_number: 1.0369
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_plus_state x delta_state | ols_affine | pooled
- support: `unsupported`
- median_test_r2: -0.1788
- median_test_mse: 0.001145
- median_test_mae: 0.009267
- coefficient_stability: 0.9614
- nonzero_count: 4
- sparsity_ratio: 0.9860
- raw_condition_number: inf
- effective_condition_number: 610.4425
- conditioning_pruned_features: altitude, vertical_speed
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ridge_affine | stratified
- support: `unsupported`
- median_test_r2: -0.1797
- median_test_mse: 0.274628
- median_test_mae: 0.241110
- coefficient_stability: 0.7083
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | lasso_affine | stratified
- support: `unsupported`
- median_test_r2: -0.1798
- median_test_mse: 0.274631
- median_test_mae: 0.241108
- coefficient_stability: 0.7083
- nonzero_count: 58
- sparsity_ratio: 0.0333
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### commands_only x next_raw_state | ols_affine | stratified
- support: `unsupported`
- median_test_r2: -0.1798
- median_test_mse: 0.274632
- median_test_mae: 0.241109
- coefficient_stability: 0.7083
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: 1.0349
- effective_condition_number: 1.0349
- conditioning_pruned_features: none
- conditioning_baseline_drops: none
- conditioning_extra_pruned_features: none

### feature_mapped_linear x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9978
- median_test_mse: 0.000570
- median_test_mae: 0.007803
- coefficient_stability: 0.9197
- nonzero_count: 10
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9978
- median_test_mse: 0.000550
- median_test_mae: 0.008221
- coefficient_stability: 0.9624
- nonzero_count: 30
- sparsity_ratio: 0.9487
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9978
- median_test_mse: 0.000573
- median_test_mae: 0.007832
- coefficient_stability: 0.9051
- nonzero_count: 10
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.000618
- median_test_mae: 0.008171
- coefficient_stability: 0.8573
- nonzero_count: 372
- sparsity_ratio: 0.3641
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.000587
- median_test_mae: 0.008225
- coefficient_stability: 0.9556
- nonzero_count: 31
- sparsity_ratio: 0.9470
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### pooled_backend_mode_augmented x next_raw_state | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.000636
- median_test_mae: 0.008101
- coefficient_stability: 0.9460
- nonzero_count: 10
- sparsity_ratio: 0.9683
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9977
- median_test_mse: 0.000639
- median_test_mae: 0.008176
- coefficient_stability: 0.9810
- nonzero_count: 239
- sparsity_ratio: 0.2413
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9976
- median_test_mse: 0.000641
- median_test_mae: 0.008199
- coefficient_stability: 0.9937
- nonzero_count: 10
- sparsity_ratio: 0.9683
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### feature_mapped_linear x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9975
- median_test_mse: 0.000625
- median_test_mae: 0.008780
- coefficient_stability: 0.9060
- nonzero_count: 509
- sparsity_ratio: 0.1299
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### pooled_backend_mode_augmented x next_raw_state | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9969
- median_test_mse: 0.000778
- median_test_mae: 0.009160
- coefficient_stability: 0.9841
- nonzero_count: 19
- sparsity_ratio: 0.9397
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x next_raw_state | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9968
- median_test_mse: 0.000803
- median_test_mae: 0.009331
- coefficient_stability: 0.9968
- nonzero_count: 275
- sparsity_ratio: 0.1270
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x next_raw_state | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9956
- median_test_mse: 0.001109
- median_test_mae: 0.009138
- coefficient_stability: 0.9651
- nonzero_count: 19
- sparsity_ratio: 0.9397
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### feature_mapped_linear x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9933
- median_test_mse: 0.000524
- median_test_mae: 0.005789
- coefficient_stability: 0.9658
- nonzero_count: 8
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9927
- median_test_mse: 0.000579
- median_test_mae: 0.005803
- coefficient_stability: 0.9573
- nonzero_count: 7
- sparsity_ratio: 0.9850
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9927
- median_test_mse: 0.000561
- median_test_mae: 0.006004
- coefficient_stability: 0.9338
- nonzero_count: 368
- sparsity_ratio: 0.2137
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9923
- median_test_mse: 0.000594
- median_test_mae: 0.006092
- coefficient_stability: 0.9802
- nonzero_count: 6
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9920
- median_test_mse: 0.000610
- median_test_mae: 0.006199
- coefficient_stability: 0.9960
- nonzero_count: 206
- sparsity_ratio: 0.1825
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### feature_mapped_linear x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9906
- median_test_mse: 0.000728
- median_test_mae: 0.008409
- coefficient_stability: 0.9509
- nonzero_count: 7
- sparsity_ratio: 0.9850
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9901
- median_test_mse: 0.000758
- median_test_mae: 0.008468
- coefficient_stability: 0.9209
- nonzero_count: 387
- sparsity_ratio: 0.1731
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9900
- median_test_mse: 0.000780
- median_test_mae: 0.008430
- coefficient_stability: 0.9359
- nonzero_count: 8
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9898
- median_test_mse: 0.000803
- median_test_mae: 0.007620
- coefficient_stability: 0.9487
- nonzero_count: 4
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9893
- median_test_mse: 0.000853
- median_test_mae: 0.007637
- coefficient_stability: 0.9316
- nonzero_count: 4
- sparsity_ratio: 0.9829
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9893
- median_test_mse: 0.000835
- median_test_mae: 0.007748
- coefficient_stability: 0.9145
- nonzero_count: 194
- sparsity_ratio: 0.1709
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9891
- median_test_mse: 0.000904
- median_test_mae: 0.006057
- coefficient_stability: 0.9722
- nonzero_count: 6
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9882
- median_test_mse: 0.000894
- median_test_mae: 0.009542
- coefficient_stability: 0.9841
- nonzero_count: 6
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9881
- median_test_mse: 0.000918
- median_test_mae: 0.008071
- coefficient_stability: 0.9762
- nonzero_count: 3
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9880
- median_test_mse: 0.000908
- median_test_mae: 0.009609
- coefficient_stability: 1.0000
- nonzero_count: 217
- sparsity_ratio: 0.1389
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9879
- median_test_mse: 0.000932
- median_test_mae: 0.008159
- coefficient_stability: 0.9921
- nonzero_count: 104
- sparsity_ratio: 0.1746
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x window_summary_response | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9855
- median_test_mse: 0.001154
- median_test_mae: 0.009556
- coefficient_stability: 0.9524
- nonzero_count: 6
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | pooled
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9839
- median_test_mse: 0.001334
- median_test_mae: 0.008031
- coefficient_stability: 0.9603
- nonzero_count: 3
- sparsity_ratio: 0.9762
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### feature_mapped_linear x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9028
- median_test_mse: 0.000563
- median_test_mae: 0.005496
- coefficient_stability: 0.9348
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9028
- median_test_mse: 0.000608
- median_test_mae: 0.005744
- coefficient_stability: 0.9220
- nonzero_count: 233
- sparsity_ratio: 0.5021
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### pooled_backend_mode_augmented x future_state_horizon | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9024
- median_test_mse: 0.000626
- median_test_mae: 0.005885
- coefficient_stability: 1.0000
- nonzero_count: 156
- sparsity_ratio: 0.3810
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x future_state_horizon | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9023
- median_test_mse: 0.000629
- median_test_mae: 0.005920
- coefficient_stability: 0.9960
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### feature_mapped_linear x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9021
- median_test_mse: 0.000564
- median_test_mae: 0.005495
- coefficient_stability: 0.9092
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### pooled_backend_mode_augmented x future_state_horizon | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.9019
- median_test_mse: 0.000623
- median_test_mae: 0.005826
- coefficient_stability: 0.9524
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### feature_mapped_linear x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8558
- median_test_mse: 0.000898
- median_test_mae: 0.007399
- coefficient_stability: 0.9081
- nonzero_count: 127
- sparsity_ratio: 0.4573
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8557
- median_test_mse: 0.000860
- median_test_mae: 0.007203
- coefficient_stability: 0.9124
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### pooled_backend_mode_augmented x selected_state_subset | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8546
- median_test_mse: 0.000965
- median_test_mae: 0.007784
- coefficient_stability: 1.0000
- nonzero_count: 84
- sparsity_ratio: 0.3333
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x selected_state_subset | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8545
- median_test_mse: 0.000968
- median_test_mae: 0.007816
- coefficient_stability: 0.9921
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### feature_mapped_linear x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8544
- median_test_mse: 0.000862
- median_test_mae: 0.007203
- coefficient_stability: 0.8846
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### pooled_backend_mode_augmented x selected_state_subset | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8538
- median_test_mse: 0.000960
- median_test_mae: 0.007694
- coefficient_stability: 0.9365
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### feature_mapped_linear x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8514
- median_test_mse: 0.000759
- median_test_mae: 0.007748
- coefficient_stability: 0.9092
- nonzero_count: 265
- sparsity_ratio: 0.4338
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8491
- median_test_mse: 0.000733
- median_test_mae: 0.007691
- coefficient_stability: 0.9124
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8472
- median_test_mse: 0.000733
- median_test_mae: 0.007700
- coefficient_stability: 0.8857
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### pooled_backend_mode_augmented x window_summary_response | lasso_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8130
- median_test_mse: 0.000921
- median_test_mae: 0.009278
- coefficient_stability: 0.9921
- nonzero_count: 179
- sparsity_ratio: 0.2897
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x window_summary_response | ridge_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8128
- median_test_mse: 0.000923
- median_test_mae: 0.009304
- coefficient_stability: 0.9881
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x window_summary_response | ols_affine | stratified
- appendix: `true`
- support: `supported`
- median_test_r2: 0.8125
- median_test_mse: 0.000916
- median_test_mae: 0.009230
- coefficient_stability: 0.9286
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5134
- median_test_mse: 0.059750
- median_test_mae: 0.201760
- coefficient_stability: 0.8810
- nonzero_count: 80
- sparsity_ratio: 0.0476
- raw_condition_number: inf
- effective_condition_number: 647.5406
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.5115
- median_test_mse: 0.059984
- median_test_mae: 0.202055
- coefficient_stability: 0.8810
- nonzero_count: 28
- sparsity_ratio: 0.6667
- raw_condition_number: inf
- effective_condition_number: 647.5406
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4903
- median_test_mse: 0.062613
- median_test_mae: 0.202379
- coefficient_stability: 0.7857
- nonzero_count: 28
- sparsity_ratio: 0.6667
- raw_condition_number: inf
- effective_condition_number: 647.5406
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### feature_mapped_linear x actuator_response | lasso_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4717
- median_test_mse: 0.064865
- median_test_mae: 0.192143
- coefficient_stability: 0.6923
- nonzero_count: 152
- sparsity_ratio: 0.0256
- raw_condition_number: inf
- effective_condition_number: 891.2789
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x actuator_response | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4705
- median_test_mse: 0.064997
- median_test_mae: 0.191169
- coefficient_stability: 0.6795
- nonzero_count: 40
- sparsity_ratio: 0.7436
- raw_condition_number: inf
- effective_condition_number: 891.2789
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x actuator_response | ols_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4531
- median_test_mse: 0.067135
- median_test_mae: 0.192037
- coefficient_stability: 0.5897
- nonzero_count: 40
- sparsity_ratio: 0.7436
- raw_condition_number: inf
- effective_condition_number: 891.2789
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### pooled_backend_mode_augmented x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4458
- median_test_mse: 0.067583
- median_test_mae: 0.190127
- coefficient_stability: 0.6786
- nonzero_count: 8
- sparsity_ratio: 0.9048
- raw_condition_number: inf
- effective_condition_number: 453.9219
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4446
- median_test_mse: 0.067735
- median_test_mae: 0.190689
- coefficient_stability: 0.7202
- nonzero_count: 76
- sparsity_ratio: 0.0952
- raw_condition_number: inf
- effective_condition_number: 453.9219
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4446
- median_test_mse: 0.067736
- median_test_mae: 0.190681
- coefficient_stability: 0.7202
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 453.9219
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### feature_mapped_linear x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `partial`
- median_test_r2: 0.4300
- median_test_mse: 0.000552
- median_test_mae: 0.008220
- coefficient_stability: 0.9658
- nonzero_count: 17
- sparsity_ratio: 0.9709
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3952
- median_test_mse: 0.000587
- median_test_mae: 0.008225
- coefficient_stability: 0.9556
- nonzero_count: 19
- sparsity_ratio: 0.9675
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3869
- median_test_mse: 0.000594
- median_test_mae: 0.008500
- coefficient_stability: 0.9573
- nonzero_count: 470
- sparsity_ratio: 0.1966
- raw_condition_number: inf
- effective_condition_number: 885.4550
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_yaw

### feature_mapped_linear x actuator_response | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.3860
- median_test_mse: 0.074931
- median_test_mae: 0.187715
- coefficient_stability: 0.5449
- nonzero_count: 144
- sparsity_ratio: 0.0769
- raw_condition_number: inf
- effective_condition_number: 609.8984
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2740
- median_test_mse: 0.000575
- median_test_mae: 0.007792
- coefficient_stability: 0.9325
- nonzero_count: 330
- sparsity_ratio: 0.4359
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2700
- median_test_mse: 0.000570
- median_test_mae: 0.007801
- coefficient_stability: 0.9188
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### feature_mapped_linear x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2598
- median_test_mse: 0.000573
- median_test_mae: 0.007832
- coefficient_stability: 0.9051
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 607.7141
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### pooled_backend_mode_augmented x delta_state | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2444
- median_test_mse: 0.000636
- median_test_mae: 0.008101
- coefficient_stability: 0.9460
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x delta_state | lasso_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2419
- median_test_mse: 0.000641
- median_test_mae: 0.008188
- coefficient_stability: 1.0000
- nonzero_count: 219
- sparsity_ratio: 0.3048
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### pooled_backend_mode_augmented x delta_state | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2417
- median_test_mse: 0.000641
- median_test_mae: 0.008195
- coefficient_stability: 0.9937
- nonzero_count: 0
- sparsity_ratio: 1.0000
- raw_condition_number: inf
- effective_condition_number: 452.0904
- conditioning_pruned_features: altitude, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: mode_posctl

### feature_mapped_linear x actuator_response | ridge_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.2217
- median_test_mse: 0.095005
- median_test_mae: 0.197956
- coefficient_stability: 0.6731
- nonzero_count: 12
- sparsity_ratio: 0.9231
- raw_condition_number: inf
- effective_condition_number: 609.8984
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### pooled_backend_mode_augmented x delta_state | ridge_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1924
- median_test_mse: 0.000781
- median_test_mae: 0.009160
- coefficient_stability: 0.9905
- nonzero_count: 6
- sparsity_ratio: 0.9810
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### pooled_backend_mode_augmented x delta_state | lasso_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.1881
- median_test_mse: 0.000785
- median_test_mae: 0.009169
- coefficient_stability: 0.9968
- nonzero_count: 273
- sparsity_ratio: 0.1333
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

### feature_mapped_linear x actuator_response | ols_affine | stratified
- appendix: `true`
- support: `unsupported`
- median_test_r2: 0.0110
- median_test_mse: 0.120757
- median_test_mae: 0.205718
- coefficient_stability: 0.6474
- nonzero_count: 10
- sparsity_ratio: 0.9359
- raw_condition_number: inf
- effective_condition_number: 609.8984
- conditioning_pruned_features: altitude, backend_px4__command_pitch, backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_offboard_attitude, mode_posctl, vertical_speed
- conditioning_baseline_drops: backend_px4__command_pitch, mode_offboard_attitude
- conditioning_extra_pruned_features: backend_px4__command_roll, backend_px4__command_throttle, backend_px4__command_yaw, clip__command_pitch, clip__command_roll, clip__command_throttle, clip__command_yaw, mode_posctl

### pooled_backend_mode_augmented x delta_state | ols_affine | pooled
- appendix: `true`
- support: `unsupported`
- median_test_r2: -0.1414
- median_test_mse: 0.001109
- median_test_mae: 0.009138
- coefficient_stability: 0.9651
- nonzero_count: 6
- sparsity_ratio: 0.9810
- raw_condition_number: inf
- effective_condition_number: 642.9853
- conditioning_pruned_features: altitude, mode_offboard_attitude, vertical_speed
- conditioning_baseline_drops: mode_offboard_attitude
- conditioning_extra_pruned_features: none

## Skipped
- 无。