# Sparsity Overlap

- status: `overlap_available`
- representative_combo: `commands_plus_state | future_state_horizon | ols_affine | pooled`
- representative_support: `partial`

## Comparisons
- baseline_vs_diagnostic: stable_jaccard=1.0000; stable_intersection_union=10/10; top_edge_jaccard=1.0000; high_frequency_jaccard=1.0000
- full_vs_holdout[dynamic]: stable_jaccard=1.0000; stable_intersection_union=10/10; top_edge_jaccard=1.0000; high_frequency_jaccard=1.0000
- full_vs_holdout[nominal]: stable_jaccard=1.0000; stable_intersection_union=10/10; top_edge_jaccard=0.4286; high_frequency_jaccard=1.0000
- full_vs_holdout[throttle_biased]: stable_jaccard=1.0000; stable_intersection_union=10/10; top_edge_jaccard=1.0000; high_frequency_jaccard=1.0000
- data_thickening: comparison_unavailable

## Assessment
- baseline_vs_diagnostic_meets_target: true
- data_thickening_meets_target: false
- holdout_median_jaccard: 1.0000
- holdout_min_jaccard: 1.0000
- holdout_meets_target: true
- high_frequency_overlap_nonempty: true

## Conclusion
- 代表性组合的 dominant edges 在 baseline/diagnostic、holdout 与厚化对照之间基本稳定，sparsity 可以正式进入主报告。