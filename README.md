# autopilot_lab

`autopilot_lab` 当前保留的是一条已经完成到 `USDTA v1` 正式评估、并开始进入 `USDTA v2` 重设计的研究链：

`sparsity hypothesis -> empirical validation -> stage-2 common-cause synthesis -> stage-3 USDTA v1 attack design -> stage-4 official USDTA v1 evaluation -> USDTA v2 redesign checklist`

## Docs Layout

- `docs/v1/`: 当前已经冻结的 `USDTA v1` 文档链，覆盖 Stage 1 到 Stage 4 official 结果。
- `docs/v2/`: 下一版方法的修改清单与后续设计入口。

## Source Of Truth

当前 repo-level source of truth 按优先级看这几份：

1. `README.md`
2. `docs/v1/STAGE1_SUMMARY_v1.md`
3. `docs/v1/STAGE2_SUMMARY_v1.md`
4. `docs/v1/STAGE4_EVALUATION_v1.md`

扩展分析/设计文档：

- `docs/v1/STAGE2_DEEP_ANALYSIS_v1.md`
- `docs/v1/STAGE2_MATHEVIDENCE_v1.md`
- `docs/v1/STAGE3_REFERENCE_v1.md`
- `docs/v1/STAGE3_ATTACK_DESIGN_v1.md`
- `docs/v1/STAGE4_PLAN_v1.md`
- `docs/v1/STAGE4_PART1_v1.md`
- `docs/v1/STAGE4_PART2_v1.md`
- `docs/v1/STAGE4_PART3_v1.md`
- `docs/v1/STAGE4_PART4_v1.md`
- `docs/v2/USDTA_V2_CHECKLIST.md`

说明：

- `docs/v1/` 下的文档默认都只对应 `USDTA v1`。
- `docs/v2/` 下的文档只代表下一版设计方向，不代表已经完成的实验结果。
- 代码里的规范方法名是 `family_aware_usdta_v1`；`family_aware_usdta` 只作为历史兼容别名保留。

## Current Status

- Stage 1 已完成：建立了 `Y ≈ fX (+ b)` 在 PX4 和 ArduPilot 上都可复现的线性 evidence。
- Stage 2 已完成：把六条机制线整理为统一的 six-line / three-family 结构，并给出 `USDTA` 设计约束。
- Stage 3 已完成：把 `USDTA v1` 固定成 design layer、runtime API 和 machine-readable contract。
- Stage 4 official 已完成：四个 part 全部闭环，正式结果已经写入 `docs/v1/STAGE4_EVALUATION_v1.md`。
- 当前工作重心已经转到 `USDTA v2`，入口文档是 `docs/v2/USDTA_V2_CHECKLIST.md`。

## Current Conclusions

- `bounded_noise` 是当前 official Stage 4 的全局 winner，拿下 `27` 个 official cells 里的 `17` 个。
- `family_aware_usdta_v1` 不是全局冠军，只拿下 `10 / 27`，但在 `AP-HTM` 和 `AP-HTG` 上给出了稳定正证据。
- `family_aware_usdta_v1` 没有建立 global transfer superiority，也没有建立 official crash superiority。
- 当前 `USDTA v1` 更像一个对特定 history-transport witness 有效的结构化攻击器，而不是能全域压过随机噪声基线的统一方法。
- `USDTA v2` 的目标不是微调现有低维 latent，而是补齐 weak lines 上缺失的表达力，尤其是 `PX-STC`、`PX-STD`、`AP-DAB`、`AP-HTS`。

## Retained Studies

Stage 1 retained studies：

1. `artifacts/studies/20260410_224818_px4_real_generalization_ablation`
2. `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`
3. `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation`
4. `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix`

Stage 2 retained study：

1. `artifacts/studies/20260421_090255_stage2_six_line_common_cause_analysis`

Stage 3 retained study：

1. `artifacts/studies/20260421_115334_stage3_attack_design`

Stage 4 official retained studies：

1. `artifacts/studies/20260423_074820_stage4_part1_official_eval`
2. `artifacts/studies/20260423_133429_stage4_part2_official_eval`
3. `artifacts/studies/20260424_083814_stage4_part3_official_eval`
4. `artifacts/studies/20260424_132931_stage4_part4_official_eval`

## Reading Order

1. `README.md`
2. `docs/v1/STAGE1_SUMMARY_v1.md`
3. `docs/v1/STAGE2_SUMMARY_v1.md`
4. `docs/v1/STAGE2_DEEP_ANALYSIS_v1.md`
5. `docs/v1/STAGE2_MATHEVIDENCE_v1.md`
6. `docs/v1/STAGE3_REFERENCE_v1.md`
7. `docs/v1/STAGE3_ATTACK_DESIGN_v1.md`
8. `docs/v1/STAGE4_PLAN_v1.md`
9. `docs/v1/STAGE4_PART1_v1.md`
10. `docs/v1/STAGE4_PART2_v1.md`
11. `docs/v1/STAGE4_PART3_v1.md`
12. `docs/v1/STAGE4_PART4_v1.md`
13. `docs/v1/STAGE4_EVALUATION_v1.md`
14. `docs/v2/USDTA_V2_CHECKLIST.md`

## Formal Entry Points

Stage 1：

- `scripts/run_px4_generalization_full.sh`
- `scripts/run_ardupilot_generalization_full.sh`
- `scripts/visualize_fit_matrices.py`

Stage 2：

- `scripts/analyze_stage2_six_line_common_cause.py`

Stage 3：

- `scripts/analyze_stage3_attack_design.py`

Stage 4 official：

- `scripts/run_stage4_part1_official.py`
- `scripts/run_stage4_part2_official.py`
- `scripts/run_stage4_part4_official.py`

说明：

- Stage 4 的 official artifacts 已经完成闭环；当前保留这些入口主要是为了复验与后续 rerun。
- `docs/v2/USDTA_V2_CHECKLIST.md` 是下一步实现入口，不是执行脚本。

## Directory Guide

- `artifacts/studies/`: 正式 study artifacts
- `configs/`: 实验配置
- `docs/v1/`: 冻结的 `USDTA v1` 文档链
- `docs/v2/`: `USDTA v2` 设计清单
- `scripts/`: 保留的正式入口
- `src/`: 分析、runtime 与 backend 代码
- `tests/`: 当前最小回归集
