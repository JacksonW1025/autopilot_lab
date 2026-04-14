# Sparsity Overlap

- status: `overlap_available`
- representative_combo: `commands_plus_state_history | selected_state_subset | ols_affine | pooled`
- representative_support: `partial`

## Comparisons
- baseline_vs_diagnostic: stable_jaccard=nan; stable_intersection_union=0/0; top_edge_jaccard=0.0000; high_frequency_jaccard=nan
- full_vs_holdout[dynamic]: stable_jaccard=nan; stable_intersection_union=0/0; top_edge_jaccard=0.1765; high_frequency_jaccard=nan
- full_vs_holdout[nominal]: stable_jaccard=nan; stable_intersection_union=0/0; top_edge_jaccard=0.0000; high_frequency_jaccard=nan
- full_vs_holdout[throttle_biased]: stable_jaccard=nan; stable_intersection_union=0/0; top_edge_jaccard=0.2500; high_frequency_jaccard=nan
- data_thickening: comparison_unavailable

## Assessment
- baseline_vs_diagnostic_meets_target: false
- data_thickening_meets_target: false
- holdout_median_jaccard: nan
- holdout_min_jaccard: nan
- holdout_meets_target: false
- high_frequency_overlap_nonempty: false

## Conclusion
- 当前只有代表性组合本体，缺少可用的 holdout/thickening overlap，因此 sparsity 还不能单独升格。