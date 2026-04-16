# Formal V2 Insight Phase Research Memo

本文现在覆盖了当前 repo-state 下 insight phase 的主要分析对象与核心结论；它是结果性 research memo，不是待执行计划。它仍不是“永远最终版”，因为 repo 还会继续演化，但本轮已经把 generalized structure、semantic interpretation、failure boundary、cross-backend structure 和 attack-relevant extraction 一次性补齐。当前文档除了固化 repo-state inventory、analysis manifest、anchor catalog、指标方案和 priority combos，还包含 `A1 vs B1`、`A2 vs C1/D1/D2` 的 focused deep dive，以及基于 `formal_v2_in_depth_analysis` 的全局结构综合。

## 压缩版结论

- [事实][高置信] 这份 memo 是当前 repo-state 下的结果文档，不是计划。主结果由 `artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive` 与 `artifacts/studies/20260414_064902_formal_v2_in_depth_analysis` 两套 aggregate analysis artifact 支撑。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/summary/anchor_deep_dive.json`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/summary/in_depth_analysis.json`。
- [事实][高置信] 当前 generalized-supported 的稳定结构分成两类：PX4 是 state-dominated 的短时传播结构，ArduPilot 是 `commands_only` 主导的低维 direct-control 结构。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stable_core_matrix_readout.csv`。
- [事实][高置信] PX4 stable-core 有 `80` 个组合，主要覆盖 `next_raw_state / future_state_horizon / selected_state_subset / window_summary_response`，且 `state_current + lagged state` 明显主导；ArduPilot stable-core 只有 `12` 个组合，全部是 `commands_only`，全部由 command block 主导。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/summary/in_depth_analysis.json`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stable_core_matrix_readout.csv`。
- [解释][高置信] 因此 PX4 当前最可靠的线性证据更像 mixed propagation / state continuation，而 ArduPilot 当前最可靠的线性证据更像 direct control path。
- [事实][高置信] `A1 vs B1` 的关键分界不是 conditioning，也不是 raw sparsity 差很多，而是 scenario stability：A1 是 generalized-supported，B1 是 supported-but-local。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/px4_a1_b1_matrix_comparison.csv`。
- [事实][高置信] ArduPilot state-evolution 的 `C1/D1/D2` 不是“没结构”，而是“高分但被 formal boundary 卡住”：`C1` 是 stable partial mask + extreme conditioning，`D2` 是 empty mask + stable raw template，`D1` 是 empty mask + raw collapse。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/ardupilot_conditioning_failure.csv`。
- [解释][高置信] 所以 targeted state-evolution 当前仍然是 inconclusive，但这只是 state-evolution 子问题的边界，不是对“主线存在稳定线性结构”的反证。
- [事实][高置信] backend-shared 的是语义输出家族，不是 support pattern 本身。两边共有 `9` 个 shared alignment key，但 top-edge overlap Jaccard 平均只有 `0.0175`。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/backend_alignment.csv`。
- [解释][高置信] 这意味着“两边都能稳定拟合同一类输出”不等于“两边依赖同一组输入结构”。
- [事实][高置信] 当前最适合后续 attack design 的主锚点是 ArduPilot `commands_only -> actuator_response`，尤其是 `A2`：`command_throttle` 以非空、低维、跨 study 稳定的 support 主导 `actuator_1~4`。证据：`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`、`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`。
- [解释][高置信] 当前已经足够支撑的 design principle 是：低维优先、非空且稳定 support 优先、direct-control path 优先、高分但病态路径降权；PX4 若继续推进，更应考虑 state/feedback channel，而不是默认 throttle 或 commands-only 入口。

## 研究边界与方法

- [事实] 本文结论只来自当前仓库中真实存在的 artifact、summary 和相关分析代码，而不是既有叙事文档。主证据入口是 `artifacts/studies/**`、`artifacts/studies/*/prepared/sample_table.csv`、`artifacts/studies/*/prepared/schema_inventory.yaml`、`artifacts/studies/*/fits/**/{matrix_f.csv,sparsity_mask.csv,metrics.json,bias_b.csv}`、`artifacts/studies/*/summary/*.json`、`src/linearity_analysis/linearity_analysis/in_depth_analysis.py`、`src/linearity_core/linearity_core/study_artifacts.py`、`src/linearity_core/linearity_core/fit.py`、`scripts/analyze_formal_v2_in_depth.py`、`scripts/visualize_fit_matrices.py`、`configs/studies/*`、`configs/ablations/*`。
- [事实] `README`、milestone 和 appendix 文档只被用来定位 study 名称和路径，不作为本文的 source of truth。定位文档是 `README.md`、`docs/MILESTONE_LINEAR_F_REPORT.md`、`docs/MILESTONE_LINEAR_F_APPENDIX.md`、`docs/XY_SCHEMA_GUIDE.md`。
- [事实] 本轮不重做 broad validation，不扩新的 schema/mode/scenario sweep，也不实现 attack algorithm；只整理当前 repo 已经存在的 Formal V2 mainline 与 targeted artifacts。直接工作范围是 `artifacts/studies/20260410_224818_px4_real_generalization_ablation` 至 `artifacts/studies/20260413_134755_px4_vs_ardupilot_compare`。
- [解释] 由于 ArduPilot 路径的 heatmap 覆盖明显不均匀，主分析对象必须下钻到 `matrix_f.csv`、`sparsity_mask.csv`、`metrics.json` 和 `sample_table.csv/schema_inventory.yaml`，不能只看 `summary/*.json`。对照路径见 `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/**`、`artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix/fits/**`。
- [假设] 后续真正能支撑 attack design principle 的，不会是“哪个 backend 更强”，而是哪些 low-dimensional support 能跨 scenario、跨 study 保持稳定；这也是后续分析顺序优先锁 A1/A2/B1/C1/D1 的原因。

## 当前 repo-state inventory

- [事实] 当前 repo 内可直接用于 insight phase 的对象分成三类：4 个 formal mainline fit studies、4 个 targeted mode-isolated fit studies、2 个 aggregate-only studies。主线目录是 `artifacts/studies/20260410_224818_px4_real_generalization_ablation`、`artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`、`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation`、`artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix`；targeted 目录是 `artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline`、`artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic`、`artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline`、`artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic`；aggregate-only 目录是 `artifacts/studies/20260413_134505_ardupilot_state_evolution_validation` 与 `artifacts/studies/20260413_134755_px4_vs_ardupilot_compare`。
- [事实] 8 个 fit studies 都具备 `prepared/sample_table.csv` 与 `prepared/schema_inventory.yaml`；2 个 aggregate-only studies 只有 `manifest.yaml`、`summary/*.json` 和 `reports/*.md`，没有 `prepared/` 与 `fits/`。证据：`artifacts/studies/20260413_134505_ardupilot_state_evolution_validation/summary/state_evolution_validation.json`、`artifacts/studies/20260413_134755_px4_vs_ardupilot_compare/summary/backend_compare.json`。
- [事实] fit-count 分布是：4 个 mainline study 各 `216` 个 combo-model fit；4 个 targeted study 各 `12` 个 combo-model fit。证据：对应 study 目录下的 `fits/*/*`。
- [事实] heatmap 覆盖并不均匀：PX4 baseline `120/216`、PX4 diagnostic `126/216`、ArduPilot baseline `12/216`、ArduPilot diagnostic `12/216`、targeted STABILIZE baseline `10/12`、targeted STABILIZE diagnostic `0/12`、targeted GUIDED_NOGPS baseline `1/12`、targeted GUIDED_NOGPS diagnostic `0/12`。证据：上述各 study 的 `fits/**/matrix_heatmap_abs.png` 与 `fits/**/matrix_heatmap_signed.png`。
- [解释] 这意味着 PX4 可以同时依赖 summary + matrix + heatmap 三层读结构；ArduPilot 尤其是 targeted GUIDED_NOGPS，必须以 `matrix_f.csv`/`sparsity_mask.csv`/`metrics.json` 为主，heatmap 只能当附加证据。

## Analysis Manifest（当前可见对象）

- [事实] 下表只记录当前 repo 中真实存在的对象；aggregate-only study 不伪装成 fit study，也不把 compare/validation aggregate 混成矩阵证据。证据：各目录下是否存在 `prepared/` 与 `fits/`。

### Study-Level Table

| artifact | backend | mode | scenario coverage | x_schema | y_schema | model | pooling | support | generalization_status | targeted_line | has_matrix | has_mask | has_metrics | has_heatmap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `artifacts/studies/20260410_224818_px4_real_generalization_ablation` | px4 | OFFBOARD_ATTITUDE, POSCTL | dynamic, nominal, throttle_biased | `*` | `*` | `*` | pooled + stratified | mixed | `80 GS / 40 local / 96 non-gen` | no | yes (`216/216`) | yes (`216/216`) | yes (`216/216`) | yes (`120/216`) |
| `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix` | px4 | OFFBOARD_ATTITUDE, POSCTL | dynamic, nominal, throttle_biased | `*` | `*` | `*` | pooled + stratified | mixed | `111 GS / 15 local / 90 non-gen` | no | yes (`216/216`) | yes (`216/216`) | yes (`216/216`) | yes (`126/216`) |
| `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation` | ardupilot | GUIDED_NOGPS, STABILIZE | dynamic, nominal, throttle_biased | `*` | `*` | `*` | pooled + stratified | mixed | `12 GS / 0 local / 204 non-gen` | no | yes (`216/216`) | yes (`216/216`) | yes (`216/216`) | yes (`12/216`) |
| `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix` | ardupilot | GUIDED_NOGPS, STABILIZE | dynamic, nominal, throttle_biased | `*` | `*` | `*` | pooled + stratified | mixed | `12 GS / 0 local / 204 non-gen` | no | yes (`216/216`) | yes (`216/216`) | yes (`216/216`) | yes (`12/216`) |
| `artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline` | ardupilot | STABILIZE | dynamic, nominal, throttle_biased | `*` | `*` | `*` | pooled | mixed | `10 GS / 0 local / 2 non-gen` | yes | yes (`12/12`) | yes (`12/12`) | yes (`12/12`) | yes (`10/12`) |
| `artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic` | ardupilot | STABILIZE | dynamic, nominal, throttle_biased | `*` | `*` | `*` | pooled | mixed | `0 GS / 0 local / 12 non-gen` | yes | yes (`12/12`) | yes (`12/12`) | yes (`12/12`) | no (`0/12`) |
| `artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline` | ardupilot | GUIDED_NOGPS | dynamic, nominal, throttle_biased | `*` | `*` | `*` | pooled | mixed | `0 GS / 0 local / 12 non-gen` | yes | yes (`12/12`) | yes (`12/12`) | yes (`12/12`) | yes (`1/12`) |
| `artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic` | ardupilot | GUIDED_NOGPS | dynamic, nominal, throttle_biased | `*` | `*` | `*` | pooled | mixed | `0 GS / 0 local / 12 non-gen` | yes | yes (`12/12`) | yes (`12/12`) | yes (`12/12`) | no (`0/12`) |
| `artifacts/studies/20260413_134505_ardupilot_state_evolution_validation` | aggregate | STABILIZE, GUIDED_NOGPS | aggregate | `-` | `-` | `-` | `-` | aggregate only | `inconclusive aggregate` | yes | no | no | no | no |
| `artifacts/studies/20260413_134755_px4_vs_ardupilot_compare` | aggregate | aggregate | aggregate | `-` | `-` | `-` | `-` | aggregate only | `compare aggregate` | no | no | no | no | no |

### Combo-Level Condensed Table

| artifact | backend | mode | scenario coverage | x_schema | y_schema | model | pooling | support | generalization_status | targeted_line | has_matrix | has_mask | has_metrics | has_heatmap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `A1 / P1 / artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__next_raw_state__stratified/ols_affine` | px4 | OFFBOARD_ATTITUDE, POSCTL | dynamic, nominal, throttle_biased | full_augmented | next_raw_state | ols_affine | stratified | supported | generalized_supported | no | yes | yes | yes | yes |
| `A2 / P2 / artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine` | ardupilot | GUIDED_NOGPS, STABILIZE | dynamic, nominal, throttle_biased | commands_only | actuator_response | ridge_affine | pooled | supported | generalized_supported | no | yes | yes | yes | yes |
| `B1 / P3 / artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__delta_state__stratified/ols_affine` | px4 | OFFBOARD_ATTITUDE, POSCTL | dynamic, nominal, throttle_biased | full_augmented | delta_state | ols_affine | stratified | supported | supported_but_local | no | yes | yes | yes | yes |
| `C1 / P4 / artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine` | ardupilot | GUIDED_NOGPS, STABILIZE | dynamic, nominal, throttle_biased | commands_plus_state_history | selected_state_subset | ols_affine | pooled | partial | not_generalized | no | yes | yes | yes | no |
| `D1 / P5 / artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine` + `artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine` | ardupilot | STABILIZE | dynamic, nominal, throttle_biased | commands_plus_state_history | selected_state_subset | ols_affine | pooled | supported -> partial | generalized_supported -> not_generalized | yes | yes | yes | yes | baseline yes / diagnostic no |
| `D2 / artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine` + `artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine` | ardupilot | GUIDED_NOGPS | dynamic, nominal, throttle_biased | commands_plus_state_history | selected_state_subset | ols_affine | pooled | partial -> partial | not_generalized -> not_generalized | yes | yes | yes | yes | baseline yes / diagnostic no |
| `D3 / artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/diagnostic_gate.json` | px4 | OFFBOARD_ATTITUDE, POSCTL | nominal throttle sweeps inside diagnostic matrix | `n/a` | throttle boundary | gate artifact | `n/a` | attitude accepted / throttle mixed | boundary | no | no | no | no | no |

- [解释] study-level table 用来锁“当前 repo 里有哪些正式分析对象”；combo-level table 用来锁“后续要重点深挖哪几个代表路径”。两张表不能混用，尤其不能把 aggregate-only study 误读成 matrix-level 证据。

## Anchor Catalog

### A1: PX4 generalized anchor

- [事实] 选择理由：它是当前 PX4 mainline 中最稳定、最典型的 generalized-supported 主锚点，适合回答 generalized 组合到底长什么样。证据：`artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/study_summary.json`、`artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/scenario_generalization.json`。
- [事实] 主要回答：Q1、Q2、Q5。它直接覆盖 generalized-supported 的稀疏形态、主导块和跨 study 稳定性。证据：`artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__next_raw_state__stratified/ols_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`。
- [事实] 一行证据摘要：baseline `median_test_r2=0.9995277520082995`、`coefficient_stability=0.8958333333333334`、`effective_condition_number=3435.5927411399257`，且 `generalization_status=generalized_supported`。证据：`artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__next_raw_state__stratified/ols_affine/metrics.json`、`artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/scenario_generalization.json`。
- [解释] 从 `matrix_f.csv` 和 `sparsity_mask.csv` 看，它更像短时 state propagation，而不是纯 `commands_only` 式 direct-control path。

### A2: ArduPilot generalized anchor

- [事实] 选择理由：它是当前 ArduPilot mainline 中最干净、最稳的 generalized-supported 组合，也是最适合抽 attack-relevant low-dimensional insight 的 direct-control 锚点。证据：`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/summary/study_summary.json`、`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/summary/scenario_generalization.json`。
- [事实] 主要回答：Q1、Q5、Q6。它能说明 backend-shared 的低维控制入口长什么样，也能说明哪些输出会被极少量输入主导。证据：`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`。
- [事实] 一行证据摘要：baseline `median_test_r2=0.9985567527124973`、`coefficient_stability=1.0`、`effective_condition_number=1.51018879444059`、`nonzero_count=4`，且 `generalization_status=generalized_supported`。证据：`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/metrics.json`、`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/summary/scenario_generalization.json`。
- [解释] 这个锚点不是“广义状态传播”，而是极端低维、近乎单列主导的 direct-control 映射；它与 A1 的结构对照非常关键。

### B1: PX4 local anchor

- [事实] 选择理由：它是更干净的 supported-but-local 对照组；相比 `feature_mapped_linear -> next_raw_state`，它在 PX4 baseline 和 diagnostic 两边都稳定停留在 local，而不是中途翻类。证据：`artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/scenario_generalization.json`、`artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/scenario_generalization.json`。
- [事实] 主要回答：Q2、Q3。它能把“overall 分数看起来够高”和“scenario 下站不住”明确拆开。证据：`artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__delta_state__stratified/ols_affine/metrics.json`、`artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/fits/full_augmented__delta_state__stratified/ols_affine/metrics.json`。
- [事实] 一行证据摘要：baseline `median_test_r2=0.810488665014081` 但 `scenario_consistency=0.0`，三档 subgroup R2 全为负；diagnostic 仍是 `supported_but_local`，`median_test_r2=0.7527773664164563`，三档 subgroup R2 仍为负。证据：上述两份 `metrics.json` 与两份 `summary/scenario_generalization.json`。
- [解释] 这类 local 现象的根本问题不是 overall R2 不够，而是 scenario shift 后同一张 `F` 无法保持解释力。

### C1: ArduPilot high-score-blocked anchor

- [事实] 选择理由：它是当前 ArduPilot mainline 中“高分但不能立为正式主结论”的最典型 blocked 组合。证据：`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/summary/study_summary.json`、`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/summary/scenario_generalization.json`。
- [事实] 主要回答：Q3、Q4、Q6。它直接说明 supported-but-formally-blocked 与 generalized-supported 的差别不只是分数，而是 conditioning 和可解释 support。证据：`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`。
- [事实] 一行证据摘要：`median_test_r2=1.0`、`coefficient_stability=1.0`，但 `effective_condition_number=2157859719.2097044`，`generalization_status=not_generalized`，只能停在 `partial`。证据：`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/metrics.json`、`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/summary/scenario_generalization.json`。
- [解释] 它在 `matrix_f.csv` 里呈现了非常规整的自回归模板，但这不等于已经获得可以正式使用的 sparse support。

### D1: Targeted STABILIZE boundary

- [事实] 选择理由：它是 mode isolation 之后最值得看的边界样本，因为 baseline 还能被判成 generalized-supported，但 diagnostic 立刻掉回 not_generalized。证据：`artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline/summary/scenario_generalization.json`、`artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic/summary/scenario_generalization.json`。
- [事实] 主要回答：Q4、Q6。它能说明“mode isolation 本身”并不自动带来稳健 support，反而可能把 alias-cancellation 暴露得更明显。证据：`artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`、`artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`。
- [事实] 一行证据摘要：baseline `median_test_r2=0.9999990204539585`、`coefficient_stability=0.8431372549019608`、`effective_condition_number=549554.6354084611` 且 `generalized_supported`；diagnostic 同组合降为 `partial`，`median_test_r2=0.9288821542563672`、`effective_condition_number=7535808.506302983`，`generalization_status=not_generalized`。证据：上述两份 `metrics.json` 与两份 `summary/scenario_generalization.json`。
- [解释] 这是当前最清楚的“高分不等于站稳”边界样本之一。

### D2: Targeted GUIDED_NOGPS boundary

- [事实] 选择理由：它是 targeted line 中最接近“稳定模板但正式判据过不去”的样本，适合用来区分 raw structure stability 和 formal support stability。证据：`artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline/summary/scenario_generalization.json`、`artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic/summary/scenario_generalization.json`。
- [事实] 主要回答：Q4、Q6。它能说明 targeted state-evolution 当前为何仍只能标成 inconclusive，而不能被拉成正式正面结论。证据：`artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`、`artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`。
- [事实] 一行证据摘要：baseline `median_test_r2=1.0`、`coefficient_stability=1.0`、`effective_condition_number=1601897234.140586`；diagnostic 同组合 `median_test_r2=1.0`、`coefficient_stability=1.0`、`effective_condition_number=557227689.1334366`，但两边都只是 `partial` 且 `generalization_status=not_generalized`。证据：上述两份 `metrics.json` 与两份 `summary/scenario_generalization.json`。
- [解释] 这个样本说明“高 R2 + 高 stability”本身仍不足以盖过严重的识别病态。

### D3: PX4 throttle diagnostic boundary

- [事实] 选择理由：它是最明确的 channel boundary 锚点，能提醒后续 attack design 不要把 throttle 默认当成稳健入口。证据：`artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/diagnostic_gate.json`。
- [事实] 主要回答：Q4、Q5、Q6。它帮助区分“backend-specific control structure”与“diagnostic gate / data quality boundary”。证据：`artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/diagnostic_gate.json`、`artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix/summary/diagnostic_gate.json`。
- [事实] 一行证据摘要：PX4 throttle 在 `OFFBOARD_ATTITUDE` 的 `medium` tier 首次出问题，在 `POSCTL` 的 `large` tier 首次出问题；拒收原因包含 `active_phase_missing`、`experiment_not_started`、`insufficient_active_nonzero_command_samples`、`experiment_truncated_before_expected_active_samples`、`failsafe_during_experiment`，而 ArduPilot diagnostic 的 throttle 当前没有系统性拒收。证据：上述两份 `summary/diagnostic_gate.json`。
- [解释] 这不是“throttle 没有线性”，而是“throttle 更早触碰 diagnostic gate 和 execution boundary”。

## 指标计算方案

- [事实] mask-based sparsity：以后续轮次为每个组合统一计算全局 nnz ratio、每行 nnz、每列 nnz、active feature count、active response count；主输入是 `sparsity_mask.csv`。证据对象：`artifacts/studies/*/fits/**/sparsity_mask.csv`。
- [事实] matrix-mass concentration：在 `matrix_f.csv` 上计算每列 `top-1 / top-3 / top-5 mass share`、Gini、HHI 或 effective support size，用来区分“真正低维主导”与“只是 threshold 后看起来稀疏”。证据对象：`artifacts/studies/*/fits/**/matrix_f.csv`。
- [事实] block structure：把 X 维统一分成 `command / state_current / state_lag_1 / state_lag_2 / state_lag_3 / other_augmented`，并观察 support 和 mass 是否集中在少数块。分类入口已经在 `src/linearity_analysis/linearity_analysis/in_depth_analysis.py` 的 `classify_feature_block` 中定义。
- [事实] stability：默认先做 mask edge Jaccard；如果 `sparsity_mask.csv` 退化为空或近空，再回退到 `matrix_f.csv` 的 raw top-k support overlap 和 sign consistency。主证据对象：`artifacts/studies/*/fits/**/{sparsity_mask.csv,matrix_f.csv}`。
- [事实] conditioning：后续会严格分开报告 `X` 的 effective condition number 和 `F` 本身的 SVD/rank/effective-rank；前者直接读 `metrics.json`，后者直接对 `matrix_f.csv` 做数值分解。现有 `X` conditioning 的产出来源是 `src/linearity_core/linearity_core/fit.py` 与对应 `metrics.json`。
- [事实] locality：使用 `scenario_subgroup_r2` 与 `scenario_consistency` 来定义 local，不把 “overall R2 高” 误认为 generalized-supported。主证据对象：`artifacts/studies/*/summary/scenario_generalization.json`、`artifacts/studies/*/fits/**/metrics.json`。
- [解释] 当 `sparsity_mask.csv` 全空但 `matrix_f.csv` 仍呈现强结构时，后续报告会把它记成“raw structure stable but formally blocked”，而不是误记成“没有结构”。

## 当前最值得优先分析的前 5 个组合

1. [事实] `full_augmented -> next_raw_state | ols_affine | stratified` on PX4 baseline。它是 generalized 主锚点，优先用于读 generalized-supported 的结构稀疏形态。证据：`artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__next_raw_state__stratified/ols_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`、`artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/scenario_generalization.json`。
2. [事实] `commands_only -> actuator_response | ridge_affine | pooled` on ArduPilot baseline。它是最干净的 direct-control 锚点，优先用于提取低维 attack-relevant support。证据：`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`、`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/summary/scenario_generalization.json`。
3. [事实] `full_augmented -> delta_state | ols_affine | stratified` on PX4 baseline。它是当前更干净的 local 对照组，优先用于区分 “supported-but-local” 与 generalized-supported。证据：`artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__delta_state__stratified/ols_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`、`artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/scenario_generalization.json`。
4. [事实] `commands_plus_state_history -> selected_state_subset | ols_affine | pooled` on ArduPilot baseline。它是高分但被 blocked 的主锚点，优先用于解释为什么 `R2=1.0` 仍不足以成为正式主结论。证据：`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`、`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/summary/scenario_generalization.json`。
5. [事实] `commands_plus_state_history -> selected_state_subset | ols_affine | pooled` on targeted STABILIZE baseline/diagnostic pair。它是最关键的 mode-isolated boundary 对照，优先用于解释 failure boundary 和 formal support collapse。证据：`artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`、`artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`。

## 第一轮已确认的观察

- [事实] PX4 generalized anchor 更像 state-propagation dominated，而不是 direct-control dominated。A1 的 active block 主要落在 `state_current` 与 `state_lag_*`，而不是 `commands_only` 单块。证据：`artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__next_raw_state__stratified/ols_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`。
- [解释] 这意味着当前最可靠的 PX4 generalized 线性证据，主要反映短时状态传播和局部动力学延续，而不是单步控制分配。

- [事实] ArduPilot generalized anchor 是极端低维的 direct-control path。A2 的 `metrics.json` 给出 `nonzero_count=4`、`sparsity_ratio=0.75`，而 `matrix_f.csv` 与 `sparsity_mask.csv` 都显示四个 actuator 基本都被 `command_throttle` 单行主导。证据：`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/{matrix_f.csv,sparsity_mask.csv,metrics.json}`。
- [解释] 这条线已经足以支持“低维攻击入口优先”的设计原则候选，但它更接近 actuator-level direct path，不代表 ArduPilot 的 state-evolution 主线已经站稳。

- [事实] ArduPilot blocked state-evolution 路径确实存在高分，但它们仍被 conditioning 绑定住。C1、D1、D2 都给出接近或等于 `1.0` 的 `median_test_r2`，但 `effective_condition_number` 分别达到 `2.157859719e9`、`5.495546354e5 -> 7.535808506e6`、`1.601897234e9 -> 5.572276891e8`。证据：`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/metrics.json`、`artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/metrics.json`、`artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/metrics.json`、`artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/metrics.json`、`artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/metrics.json`。
- [解释] 因此“高 R2”与“可正式采用的 stable support”在当前 ArduPilot state-evolution 子线上必须彻底分开。

- [事实] mask collapse 和 raw-structure stability 必须被当成两种不同现象。D2 的 baseline 和 diagnostic 都在 `matrix_f.csv` 中呈现非常规整的 `0.25 x {current, lag1, lag2, lag3}` 模板，但两边 `sparsity_mask.csv` 仍可全空；C1 则是 raw 模板存在且 mask 只剩部分列能过 threshold。证据：`artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/{matrix_f.csv,sparsity_mask.csv}`、`artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/{matrix_f.csv,sparsity_mask.csv}`、`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/{matrix_f.csv,sparsity_mask.csv}`。
- [解释] 后续报告里，前者会被记为 “raw structure stable but formally blocked”，后者会被记为 “partial support with pathological conditioning”；两者都不能直接升级成正式 attack basis。

## 深挖线 I：A1 vs B1 的 Matrix-Level Sparsity/Stability 对照

这一线只回答三个问题：A1 的 sparsity 更接近哪种 structured sparsity，B1 为什么只能停在 local，以及二者差别是不是主要来自 scenario stability。主汇总表已经程序化生成于 `artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/px4_a1_b1_matrix_comparison.csv`，机器摘要位于 `artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/summary/anchor_deep_dive.json`。

| anchor | generalization_status | scenario_consistency | mask nnz | state_current+lag mass | command mass | pair mask/raw-top4 jaccard |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `A1_baseline` | generalized_supported | `0.9903` | `47` | `0.9126` | `0.0255` | `0.625 / 0.2903` |
| `A1_diagnostic` | generalized_supported | `0.9976` | `31` | `0.9102` | `0.0110` | `0.625 / 0.2903` |
| `B1_baseline` | supported_but_local | `0.0` | `45` | `0.9079` | `0.0269` | `0.6087 / 0.2500` |
| `B1_diagnostic` | supported_but_local | `0.0` | `29` | `0.8993` | `0.0124` | `0.6087 / 0.2500` |

- [事实] A1 与 B1 的 block mass 形状非常接近，都是明显的 `state_current + state_lag_1/2/3` 主导，而不是 `command` 主导。A1 baseline/diagnostic 的 `state_current+lag` 质量分别约为 `0.9126/0.9102`；B1 baseline/diagnostic 约为 `0.9079/0.8993`；四行的 `command` 质量都只有 `0.0110~0.0269`。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/px4_a1_b1_matrix_comparison.csv`、`artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__next_raw_state__stratified/ols_affine/matrix_f.csv`、`artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__delta_state__stratified/ols_affine/matrix_f.csv`。
- [解释] 因此 A1 的 sparsity 不是“极端 entry sparsity”，而更接近 scenario-stable 的 temporal/state-propagation structured sparsity：support 和质量集中在少数 state block 上，但不是单行或单列式 direct-control。

- [事实] A1 与 B1 的 baseline↔diagnostic pair overlap 也处在相近量级，而不是一边稳一边散。A1 的 `same_combo_mask_jaccard_to_pair=0.625`、`same_combo_raw_top4_jaccard_to_pair=0.2903`；B1 分别是 `0.6087` 与 `0.2500`。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/px4_a1_b1_matrix_comparison.csv`。
- [解释] 所以 B1 之所以只是 local，并不是因为它在 baseline/diagnostic 之间完全失去 support 结构；A1 和 B1 的真正分水岭不在 pair overlap，而在 scenario-level可迁移性。

- [事实] scenario stability 才是 A1 和 B1 的核心分界。A1 baseline/diagnostic 的 `scenario_consistency=0.9903/0.9976`，3 个 subgroup R2 都稳定在 `0.95+`；B1 baseline/diagnostic 的 `scenario_consistency=0.0/0.0`，baseline 的 subgroup R2 为 `-10.91/-13.72/-12.84`，diagnostic 仍为负。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/px4_a1_b1_matrix_comparison.csv`、`artifacts/studies/20260410_224818_px4_real_generalization_ablation/summary/scenario_generalization.json`、`artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/scenario_generalization.json`。
- [解释] 这说明 B1 的 `supported_but_local` 本质上是“同一类 state-propagation 结构对 `delta_state` 输出不具 scenario-stable 解释力”，而不是“矩阵看起来太乱”或“overall R2 太低”。

- [事实] A1 与 B1 的 `X` conditioning 并没有拉开决定性差距。baseline 都是 `3435.5927`，diagnostic 都是 `2455.3807`；但 `generalization_status` 仍然稳定分裂为 `generalized_supported` 与 `supported_but_local`。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/px4_a1_b1_matrix_comparison.csv`。
- [解释] 对这组 PX4 对照来说，conditioning 不是主导解释变量；scenario stability 才是。

- [假设] 下一层 semantic interpretation 很可能会把 A1 与 B1 的差异进一步落到“`next_raw_state` 仍保留短时传播的可解释主干，而 `delta_state` 把同一模板变成对 scenario 更敏感的差分残差”上；这一点需要在后续把 response 语义与列级 sign/magnitude drift 对上。证据入口：`artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__next_raw_state__stratified/ols_affine/matrix_f.csv`、`artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__delta_state__stratified/ols_affine/matrix_f.csv`。

## 深挖线 II：A2 vs C1/D1/D2 的 Mask-Collapse 与 Conditioning 机制

这一线只回答五个问题：为什么 A2 可作为 attack-friendly anchor，为什么 C1 仍是 high-score-but-blocked，为什么 D1 会从 targeted baseline 走向 collapse，为什么 D2 会呈现 persistent raw template but formal blockage，以及 mask collapse、conditioning、raw structure stability 之间到底是什么关系。主汇总表已经程序化生成于 `artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`，机器摘要位于 `artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/summary/anchor_deep_dive.json`。

| anchor | generalization_status | x cond | mask nnz | pair mask/raw-top4 jaccard | mean top1 | dominant responses |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| `A2_baseline` | generalized_supported | `1.51e0` | `4` | `1.0 / 1.0` | `0.9928` | `4` |
| `C1_baseline` | not_generalized | `2.16e9` | `16` | `1.0 / 1.0` | `0.2292` | `0` |
| `D1_baseline` | generalized_supported | `5.50e5` | `0` | `NaN / 0.0` | `0.0788` | `0` |
| `D1_diagnostic` | not_generalized | `7.54e6` | `0` | `NaN / 0.0` | `0.3172` | `0` |
| `D2_baseline` | not_generalized | `1.60e9` | `0` | `NaN / 1.0` | `0.2292` | `0` |
| `D2_diagnostic` | not_generalized | `5.57e8` | `0` | `NaN / 1.0` | `0.2292` | `0` |

- [事实] A2 是真正的低维 direct-control anchor，而不是仅仅“分数高”。它的 `mask_nonzero_count=4`、`active_feature_count=1`、`dominant_response_count=4`，baseline/diagnostic 都满足 `pair_mask_jaccard=1.0`，且 `mean_top1_share=0.9928/0.9945`；原始 `sparsity_mask.csv` 进一步显示 4 个 actuator 只保留 `command_throttle` 一行。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`、`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/sparsity_mask.csv`、`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/matrix_f.csv`。
- [解释] 这正是后续 attack design 最想要的结构：少量输入、明确输出、低条件数、跨 study mask 不漂移。A2 可以作为 attack-friendly 主锚点。

- [事实] C1 不是“缺少结构”，而是“结构太稳定但病态”。它 baseline/diagnostic 都有 `pair_mask_jaccard=1.0`、`pair_raw_top4_jaccard=1.0`、`pair_raw_top4_sign_match=1.0`，`median_test_r2=1.0/1.0`，但 `x_effective_condition_number=2.16e9/8.99e8`，`generalization_status` 始终是 `not_generalized`，且 `mean_top1_share` 只有 `0.2292`，`dominant_response_count=0`。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`、`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/matrix_f.csv`、`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/sparsity_mask.csv`。
- [解释] C1 的高分来源更接近稳定的自回归模板，而不是低维、可控、可迁移的 sparse support。它能说明结构，但不能直接当主攻击基础。

- [事实] D1 代表的不是“raw template 还稳，但 formal gate 没过”，而是更强的 collapse：baseline/diagnostic 两边 `mask_nonzero_count` 都是 `0`，`pair_mask_jaccard=NaN`，且 `pair_raw_top4_jaccard=0.0`。同时 `x_effective_condition_number` 从 `5.50e5` 升到 `7.54e6`，`generalization_status` 从 `generalized_supported` 掉到 `not_generalized`。对应 `matrix_f.csv` 中，baseline 由 `altitude/position_z` 对消块主导，而 diagnostic 转成 roll-led 大幅值模板。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`、`artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/matrix_f.csv`、`artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/matrix_f.csv`。
- [解释] 所以 D1 的问题不只是 mask 空，而是 mode-isolated baseline 的表面正结论在 diagnostic 下连 raw support 模板也保不住；这是更强的 failure boundary。

- [事实] D2 则是另一种 blocked 机制：baseline/diagnostic 两边 `mask_nonzero_count=0`、`pair_mask_jaccard=NaN`，但 `pair_raw_top4_jaccard=1.0`、`pair_raw_top4_sign_match=1.0`，`f_rank=6/6`、`f_effective_rank=5.9575/5.9575` 也几乎不动。对应 `matrix_f.csv` 持续保留 `0.25 x {current, lag1, lag2, lag3}` 的自回归模板。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`、`artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/matrix_f.csv`、`artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/matrix_f.csv`。
- [解释] D2 因而是“persistent raw template but formal blockage”的标准样本。它可以当 insight 证据，但不能直接升级成正式 attack basis。

- [事实] A2、C1、D1、D2 已经把三种现象明确拆开了。A2 是 `low conditioning + non-empty stable mask + low-dimensional domination`；C1 是 `huge conditioning + stable partial mask + stable raw template`；D2 是 `huge conditioning + empty mask + stable raw template`；D1 是 `worsening conditioning + empty mask + raw template collapse`。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`、`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/summary/anchor_deep_dive.json`。
- [解释] 这说明 `mask collapse`、`conditioning`、`raw structure stability` 是三条不同轴，不能被压成一个“分数好不好”的单变量判断。conditioning 很关键，但它既可以对应 `stable but blocked`，也可以对应 `collapse`。

- [假设] 对 attack 设计而言，A2 可以进入主路径；C1 与 D2 更适合作为“状态传播模板存在但不宜直接拿来施加主攻击”的次级启发；D1 更像反例和边界样本。证据入口：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/summary/anchor_deep_dive.json`、`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`。

## Generalized-Supported 的结构特征

这一节回答的不是“哪个 backend 更强”，而是 generalized-supported 组合本身到底长什么样。主全局证据来自 `artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stable_core_matrix_readout.csv` 与 `artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/px4_physical_vs_state_continuation.csv`；它们只统计 baseline 与 diagnostic 交集里的 stable-core 组合。

| backend | stable-core count | dominant x families | dominant y families | mean command share | mean state_current share | mean lag share sum |
| --- | ---: | --- | --- | ---: | ---: | ---: |
| `px4` | `80` | `commands_plus_state_history(19)`, `full_augmented(19)`, `commands_plus_state(15)`, `pooled_backend_mode_augmented(15)` | `next_raw_state(27)`, `future_state_horizon(19)`, `selected_state_subset(19)`, `window_summary_response(15)` | `0.1308` | `0.5393` | `0.2823` |
| `ardupilot` | `12` | `commands_only(12)` | `actuator_response(3)`, `future_state_horizon(3)`, `selected_state_subset(3)`, `window_summary_response(3)` | `1.0000` | `0.0000` | `0.0000` |

- [事实][高置信] 当前 stable-core 的覆盖宽度在 PX4 与 ArduPilot 上完全不同。PX4 baseline↔diagnostic 交集中有 `80` 个 generalized-supported 组合，而 ArduPilot 只有 `12` 个；两边的 baseline generalized-supported 都是 diagnostic generalized-supported 的子集。代表组合：`A1`、`A2`。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/summary/in_depth_analysis.json`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stable_core_matrix_readout.csv`。
- [解释][高置信] 这不是简单的“PX4 更多、ArduPilot 更少”，而是说明 generalized-supported 的结构家族在 PX4 更宽，在 ArduPilot 更集中。

- [事实][高置信] PX4 generalized-supported 组合的主结构是 state-dominated structured sparsity，而不是 command-only sparsity。stable-core 中 `state_current_share` 平均值 `0.5393`，`state_lag_1/2/3` 合计平均 `0.2823`，而 `command_share` 平均仅 `0.1308`。代表组合：`A1`、PX4 stable-core 的 `commands_plus_state | future_state_horizon | * | pooled` 家族。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stable_core_matrix_readout.csv`、`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/px4_a1_b1_matrix_comparison.csv`。
- [解释][高置信] 对 PX4 而言，generalized-supported 更像“短时状态传播算子族”，表现为 row/column 支持集中在少数 current-state 与 lagged-state block，而不是少数命令列。

- [事实][高置信] PX4 的 physical/semantic readout 进一步验证了这种结论。`px4_physical_vs_state_continuation.csv` 的 main-scope 均值显示：`command_to_future_share=0.0649`，`state_current_to_same_state_share=0.2341`，`lag_to_future_share=0.4261`；最高的一批组合都落在 `commands_plus_state` 或 `commands_plus_state_history` 的 `future_state_horizon / selected_state_subset / window_summary_response` 上。代表组合：`commands_plus_state | future_state_horizon | lasso_affine | pooled`、`commands_plus_state_history | selected_state_subset | ols_affine | pooled`。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/px4_physical_vs_state_continuation.csv`。
- [解释][高置信] generalized-supported 的 PX4 主体不是“命令直接推未来”，而是“当前状态和短时记忆主导未来短视窗输出”。

- [事实][高置信] ArduPilot generalized-supported 组合则完全相反：stable-core 的 12 个交集组合全部是 `commands_only`、全部是 `pooled`，`command_share` 均值 `1.0`，`state_current_share` 和所有 lag share 都是 `0.0`。代表组合：`A2`。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stable_core_matrix_readout.csv`、`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`。
- [解释][高置信] 这说明 ArduPilot 当前站稳的 generalized-supported 不是 state-evolution family，而是纯 command-driven 低维映射家族。

- [事实][中置信] PX4 stable-core 里 pooled 组合明显多于 stratified 组合，比例约 `60 : 20`；ArduPilot stable-core 则没有 stratified 成员。代表组合：PX4 `commands_plus_state | next_raw_state | * | pooled`，ArduPilot `commands_only | actuator_response | * | pooled`。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stable_core_matrix_readout.csv`。
- [解释][中置信] 这说明当前 generalized-supported 的稳定主干更偏 pooled/shared structure；stratified 在 PX4 里存在但不是主流，在 ArduPilot 稳定主干里几乎不存在。

## Semantic Interpretation Layer

这一节把矩阵结构重新映射回飞控语义，不再只讨论稀疏率。主证据来自 `stable_core` 的 dominant edge 统计、`px4_physical_vs_state_continuation.csv`，以及 anchor deep-dive 的 raw matrix 路径。

- [事实][高置信] PX4 stable-core 中反复出现的输入是 `yaw`、`roll`、`yaw_rate`、`pitch`，最常出现的输出是 `future_state_yaw`、`future_state_yaw_rate`、`future_state_roll`、`future_state_roll_rate`、`future_state_pitch`。最常重复的 edge 包括 `yaw_rate -> future_state_yaw_rate`、`pitch -> future_state_pitch`、`roll -> future_state_roll`、`yaw -> future_state_yaw`、`yaw -> future_state_heading`。代表组合：PX4 stable-core 主线。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/summary/in_depth_analysis.json`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stable_core_matrix_readout.csv`。
- [解释][高置信] 这些 edge 不是长链条控制分配，而更像同状态或近邻状态在短时 horizon 上的传播与延续，语义上属于 mixed propagation path。

- [事实][高置信] ArduPilot stable-core 中压倒性的主输入是 `command_throttle`，其次才是 `command_yaw` 与 `command_pitch`；反复出现的输出包括 `actuator_1~4`、`future_state_yaw_rate`、`future_state_roll_rate`、`future_state_yaw` 和若干 horizon/summary 派生量。最常重复的 pair 是 `command_throttle -> actuator_i`。代表组合：`A2`、ArduPilot stable-core 的 `commands_only | actuator_response | * | pooled` 家族。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/summary/in_depth_analysis.json`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stable_core_matrix_readout.csv`、`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/matrix_f.csv`。
- [解释][高置信] 这条线在语义上属于 direct control path，而且是非常强的单输入主导 direct-control path。

- [事实][高置信] `commands_plus_state_history -> selected_state_subset` 这条 blocked 家族在语义上并不表现为 direct-control，而表现为 autoregressive path。`C1` 和 `D2` 的 `matrix_f.csv` 都呈现 `{current, lag1, lag2, lag3}` 的四项模板，`D1` baseline 则被 `altitude/position_z` 的成对抵消块主导。代表组合：`C1`、`D1`、`D2`。证据：`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/matrix_f.csv`、`artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/matrix_f.csv`、`artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline/fits/commands_plus_state_history__selected_state_subset__pooled/ols_affine/matrix_f.csv`。
- [解释][高置信] 所以这条高分路径更接近时间延续/自回归残留，而不是“命令对目标状态的清晰因果控制”。

- [事实][中置信] PX4 `next_raw_state` 是语义上最接近“完整短时状态传播”的家族，但它并没有在 ArduPilot stable-core 中出现共享对应物；反过来，ArduPilot `actuator_response` 也没有 PX4 stable-core 对应物。代表组合：PX4 `commands_plus_state | next_raw_state | *`，ArduPilot `commands_only | actuator_response | *`。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/backend_alignment.csv`。
- [解释][中置信] 这说明 backend-specific 结构并不只是“分数差异”，而是控制架构与可观测语义的差异。

## Backend-Shared vs Backend-Specific Structure

这一节只做结构对照，不做排名。主证据来自 `artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/backend_alignment.csv`。

| category | count | representative pattern |
| --- | ---: | --- |
| shared semantic alignment keys | `9` | 两边都稳定支持 `future_state_horizon / selected_state_subset / window_summary_response`，但 PX4 最小稳定 X 是 `commands_plus_state`，ArduPilot 是 `commands_only` |
| px4-only stable family | `6` | `next_raw_state | pooled/stratified | ols/ridge/lasso` |
| ardupilot-only stable family | `3` | `actuator_response | pooled | ols/ridge/lasso` |

- [事实][高置信] 两个 backend 之间确实存在 shared structure，但共享的是“语义家族”，不是“support pattern 本身”。共有 `9` 个 shared alignment keys，而它们的 top-edge overlap Jaccard 平均仅 `0.0175`，中位数是 `0.0`，最大也只有 `0.0526`。代表组合：`future_state_horizon | pooled | *`、`selected_state_subset | pooled | *`、`window_summary_response | pooled | *`。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/backend_alignment.csv`。
- [解释][高置信] 也就是说，两边都能稳定拟合同一类语义输出，但依赖的输入支持结构并不相同。

- [事实][高置信] shared alignment 的最小稳定 X 在两边系统性不同。9 个 shared alignment key 里，PX4 一律对应 `commands_plus_state`，ArduPilot 一律对应 `commands_only`。代表组合：`selected_state_subset | pooled | ols_affine`。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/backend_alignment.csv`。
- [解释][高置信] 这是当前最清楚的 backend-shared vs backend-specific 分界线之一：shared 的是输出语义，不 shared 的是实现这些输出所需的稳定输入结构。

- [事实][高置信] PX4-only 的 stable family 集中在 `next_raw_state`，共 `6` 个条目，覆盖 pooled/stratified 与 ols/ridge/lasso 三种模型；ArduPilot-only 的 stable family 集中在 `actuator_response`，共 `3` 个条目，覆盖三种模型。代表组合：`commands_plus_state | next_raw_state | ols_affine | pooled`、`commands_only | actuator_response | ridge_affine | pooled`。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/backend_alignment.csv`。
- [解释][高置信] `next_raw_state` 是 PX4-specific 的稳定结构，`actuator_response` 是 ArduPilot-specific 的稳定结构；这不是偶然分布，而是当前 stable-core 的主干差异。

- [事实][中置信] 在 shared semantic families 里，PX4 的 dominant edge 经常是 `yaw/yaw_rate/roll/pitch -> corresponding future state`，而 ArduPilot 的 dominant edge 则几乎总是 `command_throttle -> corresponding future/horizon/summary output`。代表组合：`future_state_horizon | pooled | ridge_affine`。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/backend_alignment.csv`。
- [解释][中置信] 这更像控制架构本身的差异，而不是单纯的数据质量差异：PX4 的稳定结构更依赖当前状态传播，ArduPilot 的稳定结构更接近油门主导的控制分配/短视窗响应。

- [假设][中置信] ArduPilot state-evolution 仍无法下正式正/负结论，更可能是“state-evolution 子问题仍被病态与模式混合卡住”，而不是“ArduPilot 整体不存在稳定线性结构”。代表组合：`A2` 与 `C1/D2`。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/summary/anchor_deep_dive.json`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/ardupilot_conditioning_failure.csv`。

## Failure Boundary Summary

这一节把主失败机制收束成当前 repo-state 下最重要的边界，而不是列术语。主证据来自 `artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stability_boundary.csv`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/ardupilot_conditioning_failure.csv` 和 `A2/C1/D1/D2` deep-dive table。

- [事实][高置信] 当前最大的 formal failure boundary 是 ArduPilot state-evolution 家族的 feature collinearity / conditioning。`stability_boundary.csv` 共有 `270` 行，其中 `ardupilot_partial_not_generalized_state_evolution` 占 `180` 行，且 primary driver 全部是 `feature_collinearity`。代表组合：`C1` family。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stability_boundary.csv`。
- [解释][高置信] 这说明当前 state-evolution 主线的正式阻塞不是偶发异常，而是系统性的识别病态边界。

- [事实][高置信] PX4 `supported_but_local` 的主失败机制与 ArduPilot 不同。`supported_but_local` 共 `55` 行，其中 `43` 行的 primary driver 是 `stratification`，`12` 行没有归到显式驱动；并没有出现 ArduPilot 那种成片的 feature-collinearity 支配。代表组合：`B1` family。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stability_boundary.csv`、`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/px4_a1_b1_matrix_comparison.csv`。
- [解释][高置信] 所以 PX4 local 的根本边界更像 scenario/stratification 不稳，而不是数值病态。

- [事实][高置信] ArduPilot 三条关键 blocked 路径对应三种不同 failure 形态。`mixed_mode_full` 的 baseline/diagnostic condition number 是 `2.16e9 / 8.99e8`，top-edge overlap 仅 `0.1111`；`stabilize_baseline_to_diagnostic_collapse` 是 `5.50e5 -> 7.54e6`，top-edge overlap `0.0`；`guided_nogps_persistent_high_r2_high_cond` 是 `1.60e9 -> 5.57e8`，top-edge overlap `0.4286`。代表组合：`C1`、`D1`、`D2`。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/ardupilot_conditioning_failure.csv`、`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`。
- [解释][高置信] 这再次说明高分不稳不是单一机制：有的是 partial-but-stable template，有的是 raw collapse，有的是 stable raw template + empty mask。

- [事实][中置信] PX4 throttle 仍然是单独的 channel boundary，而不是 generalized structure 的主失败源。D3 证据显示 throttle 在 `OFFBOARD_ATTITUDE` 的 `medium` tier、`POSCTL` 的 `large` tier 就开始触发 gate；但 `stability_boundary.csv` 中 PX4 diagnostic-only generalized 条目并没有被 throttle 主导。代表组合：`D3`。证据：`artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/diagnostic_gate.json`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stability_boundary.csv`。
- [解释][中置信] throttle 更像执行边界与实验门槛边界，而不是 PX4 generalized-supported 结构本身的主解释变量。

## Attack-Relevant Insight Extraction

这一节只提炼已经足够支撑下一阶段 attack design principle 的 insight，不实现算法。主证据来自 `artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/*.csv`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/*.csv` 和对应 summary JSON。

- [事实][高置信] 当前最稳定、最可直接利用的关键输入是 ArduPilot 的 `command_throttle`。它在 stable-core dominant edge 统计里出现 `87` 次，在 `A2` 中以 `active_feature_count=1`、`dominant_response_count=4`、`pair_mask_jaccard=1.0` 的形式稳定主导 `actuator_1~4`。代表组合：`A2`、ArduPilot `commands_only` stable-core 家族。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/summary/in_depth_analysis.json`、`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`。
- [解释][高置信] 这已经足以支持第一条 attack design principle：优先选择低维、低条件数、mask 稳定、单输入主导的 direct-control path。

- [事实][高置信] 当前最稳定、最可解释的目标输出是 ArduPilot 的 `actuator_response`。它是 backend-specific stable family，3 个模型都稳定出现，且每个 response 的 `mean_top1_share` 约 `0.99`。代表组合：`commands_only | actuator_response | ols/ridge/lasso | pooled`。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/backend_alignment.csv`、`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`。
- [解释][高置信] 这条线比 state-evolution 路径更适合作为正式攻击入口，因为它同时满足物理意义明确和 support 低维稳定。

- [事实][中置信] PX4 侧更可靠的不是 command-only 输入，而是 `current state + short lag` 对 `future_state_horizon / selected_state_subset / next_raw_state` 的稳定传播。重复最高的 pair 是 `yaw_rate -> future_state_yaw_rate`、`pitch -> future_state_pitch`、`roll -> future_state_roll`、`yaw -> future_state_yaw`。代表组合：PX4 stable-core 主线，尤其是 `commands_plus_state | future_state_horizon | * | pooled` 与 `A1`。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/summary/in_depth_analysis.json`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stable_core_matrix_readout.csv`、`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/px4_a1_b1_matrix_comparison.csv`。
- [解释][中置信] 这支持第二条 design principle：如果后续要在 PX4 上设计攻击，主入口更像 state/estimation-feedback channel，而不是假设 commands-only 会像 ArduPilot 那样给出稳定低维主导。

- [事实][高置信] `C1`、`D2` 这类高分路径不适合作为正式攻击基础。它们的 `pair_raw_top4_jaccard` 虽然可达 `1.0`，但分别属于 `stable partial mask + billion-scale conditioning` 与 `empty mask + stable raw template`。代表组合：`C1`、`D2`。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/ardupilot_conditioning_failure.csv`。
- [解释][高置信] 这支持第三条 design principle：对“高分但病态”的路径必须降权，只能作为次级启发、模板先验，或在线自适应更新的候选，不应当作主攻击骨架。

- [事实][中置信] `D1` 更不适合作为攻击基础，因为它不仅 mask 空，而且 baseline↔diagnostic 的 raw top-k overlap 也降到 `0.0`。代表组合：`D1`。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`。
- [解释][高置信] 这支持第四条 design principle：优先避开 mode-isolated 下仍会 raw-collapse 的边界路径。

- [事实][中置信] 对 PX4 throttle 入口必须降权。它不是 generalized-supported 的核心稳定支点，而且更早触发 diagnostic gate。代表组合：`D3`。证据：`artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix/summary/diagnostic_gate.json`。
- [解释][中置信] 这支持第五条 design principle：在 backend-specific 入口选择上，PX4 不应优先走 throttle channel，而应优先走已经显示出稳定传播结构的 state-aligned targets。

- [解释][高置信] 综合起来，当前已经足够支撑的 attack design principle 草案是“低维优先、非空且跨 study 稳定的 support 优先、direct-control path 优先于 autoregressive path、低 conditioning 优先且高分病态路径降权、PX4 若继续推进则需要把可控输入假设从 command-only 转向 state/feedback channel”。代表组合：`A2`、`A1`、`C1`、`D2`。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/summary/anchor_deep_dive.json`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stable_core_matrix_readout.csv`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/backend_alignment.csv`。

## Open Questions

- [假设][中置信] PX4 的 `31` 个 diagnostic-only generalized-supported 组合为什么能在 diagnostic 站稳、却不在 baseline 交集中出现，当前 `stability_boundary.csv` 里还没有被明确解释为 throttle、stratification 或其他单一驱动。代表组合：`commands_plus_state | future_state_horizon | * | stratified` 一批 diagnostic-only 条目。证据：`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/stability_boundary.csv`。
- [假设][中置信] ArduPilot `commands_only` 的稳定结构为何如此强烈地被 `command_throttle` 单输入主导，当前更像控制分配/油门主导架构的真实特征，但仍值得进一步排查是否叠加了记录口径或归一化因素。代表组合：`A2`、ArduPilot stable-core。证据：`artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/matrix_f.csv`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/summary/in_depth_analysis.json`。
- [假设][中置信] `C1/D2` 的 autoregressive 模板到底有多少是真实动态结构、多少是时间冗余导致的可辨识性假象，当前仍不能正式下正/负结论。代表组合：`C1`、`D2`。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/ardupilot_conditioning_failure.csv`。
- [假设][中置信] PX4 state-dominated stable structure 是否最终能转化成可操作的 attack surface，取决于后续是否存在现实可控的 state/feedback perturbation channel；这已经超出当前 linear artifact 自身，需要在攻击阶段单独验证。代表组合：`A1` 与 PX4 stable-core 主线。证据：`artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/px4_a1_b1_matrix_comparison.csv`、`artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/tables/px4_physical_vs_state_continuation.csv`。

## 本轮新增脚本/文件

- [事实] 第二轮 anchor deep dive 新增了分析模块 `src/linearity_analysis/linearity_analysis/anchor_deep_dive.py`、内部 CLI `scripts/analyze_anchor_deep_dive.py` 和集成测试 `tests/test_anchor_deep_dive.py`。
- [事实] 本轮还复用了并重新生成了 `formal_v2_in_depth_analysis` aggregate artifact；对应入口是既有的 `src/linearity_analysis/linearity_analysis/in_depth_analysis.py` 与 `scripts/analyze_formal_v2_in_depth.py`。
- [事实] 本轮生成的两个主要 aggregate artifact 是 `artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive` 与 `artifacts/studies/20260414_064902_formal_v2_in_depth_analysis`。
- [事实] `artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive` 包含 `manifest.yaml`、`summary/anchor_deep_dive.json`、`tables/px4_a1_b1_matrix_comparison.csv`、`tables/ardupilot_a2_c1_d1_d2_boundary.csv`。
- [事实] `artifacts/studies/20260414_064902_formal_v2_in_depth_analysis` 包含 `manifest.yaml`、`summary/in_depth_analysis.json`、`tables/stable_core_matrix_readout.csv`、`tables/px4_physical_vs_state_continuation.csv`、`tables/backend_alignment.csv`、`tables/ardupilot_conditioning_failure.csv`、`tables/stability_boundary.csv`。
- [事实] 当前 memo `docs/FORMAL_V2_INSIGHT_PHASE_MEMO.md` 已更新为当前 repo-state 下的完整 insight-phase 研究备忘录；本轮仍未重跑 fit、未扩 broad validation、未实现 attack algorithm。
