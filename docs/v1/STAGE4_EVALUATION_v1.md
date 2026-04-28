# STAGE4 正式六线仿真评估（USDTA v1）

## 当前状态

- `2026-04-23` 到 `2026-04-24` 间，`PART1` 到 `PART4` 已全部完成。
- 本文中的 `family_aware_usdta_v1` 结论全部对应 `USDTA v1`，不外推到 `USDTA v2`。
- 正式 Stage 4 共执行 `27` 个 unique official cells：
  - `24` 个 benchmark cells
  - `3` 个额外 crash-only cells：`AP-DAB/A4@throttle_biased`、`AP-HTS/A4@dynamic`、`AP-HTG/A4@dynamic`
- 四个 part 合计产出：
  - `81` 条 accepted reference runs
  - `108` 条 per-method winner rows
  - `48` 条 official transfer rows
  - `2712` 条 rollout rows
- 当前文档写入正式总评；`docs/v1/STAGE4_START_v1.md` 不再承担正式结论角色。

## Part Reports

1. [PART1 generated report](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/reports/STAGE4_PART1.generated.md): `PX-STC` + `AP-DAB`
2. [PART2 generated report](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/reports/STAGE4_PART2.generated.md): `PX-STD` + `AP-HTM`
3. [PART3 generated report](../../artifacts/studies/20260424_083814_stage4_part3_official_eval/reports/STAGE4_PART3.generated.md): `AP-HTS`
4. [PART4 generated report](../../artifacts/studies/20260424_132931_stage4_part4_official_eval/reports/STAGE4_PART4.generated.md): `AP-HTG`

## Stage 4 Contract 与排除项

- 正式 Stage 4 固定比较四个方法：
  - `family_aware_usdta_v1`
  - `low_dim_agnostic`
  - `raw_space_random`
  - `bounded_noise`
- 正式 Stage 4 固定使用 witness mode 合同，不再做双 mode 全覆盖。
- 正式主矩阵覆盖：
  - `A2 dominant_axis_sweep`
  - `A3 boundary_pulse_train`
  - 各 line 的 `nominal + targeted stress`
- crash slice 只恢复三个 unique `A4` cell，不把 Stage 4 扩大成全量 burst 普查。
- 跨线总评不把原始 `total_score` 当成唯一全局标尺；全局判断主要依赖：
  - cross-method cell wins
  - per-cell margin
  - margin vs reference
  - transfer retention
  - winner issue profile
- supplementary witness、illegal-mode sanity replay、exploratory artifact 不写入本文档主结论。

## 全局方法结论与 Family-Level 边界

| method | cross-method cell wins | mean margin vs reference | pooled transfer retention | winner issue-free rate | 总体判断 |
| --- | --- | --- | --- | --- | --- |
| `bounded_noise` | `17 / 27` | `+0.346` | `-2.322` | `0.000` | 全局 benchmark leader；主导 PX4、`AP-DAB` 与 `AP-HTS` |
| `family_aware_usdta_v1` | `10 / 27` | `+0.305` | `-1.902` | `0.000` | 非全局冠军；但在 `AP-HTM` 与 `AP-HTG` 上稳定占优 |
| `raw_space_random` | `0 / 27` | `+0.076` | `-1.509` | `0.000` | 偶尔接近前二，但没有任何正式 cell 冠军 |
| `low_dim_agnostic` | `0 / 27` | `-0.082` | `-1.275` | `0.000` | 全局最弱；较好的 pooled retention 主要来自“跌得没那么惨”，不是更强 cell 分数 |

说明：
- pooled transfer retention 会被 `AP-HTS` 的极端 collapse 明显拉低，因此它只能作为辅助指标，不能单独决定全局 winner。
- 四个方法在 official winner 集上 `issue_free_rate` 都是 `0`，说明 Stage 4 的“最佳候选”仍然全部带 issue tags。

### 全局主判断

1. 正式 Stage 4 的全局 benchmark winner 不是 `family_aware_usdta_v1`，而是 `bounded_noise`。它拿下 `27` 个 official cells 中的 `17` 个，覆盖两条 PX4 state-transport 线、`AP-DAB` direct-transport 线以及 `AP-HTS` collapse line。
2. `family_aware_usdta_v1` 的价值不是“全域统治”，而是“有选择地在特定 history-transport witness 上占优”。它完整拿下 `AP-HTM` 的 `4/4` 个 cell 和 `AP-HTG` 的 `5/5` 个 cell，并额外拿下 `AP-DAB` 的 `A2@throttle_biased`。
3. `low_dim_agnostic` 没有赢下任何 official cell，说明“去掉 line-aware inductive bias 但保留同维 latent search”并不能逼近正式 winner 水平。
4. 正式 crash superiority 没有建立。winner rollout 集上：
  - `regime_gate_blocked = 0`
  - `failsafe_or_truncation = 0`
  - `search_stagnation = 0`
  这说明 crash slice 最终仍停留在 soft degradation / instability 范围内，没有形成 winner-level 的硬失败主证据。

### Family-Level 边界

- `state_transport`：`PX-STC` + `PX-STD`
  - `bounded_noise` 以 `8 / 8` 完整拿下。
  - `family_aware_usdta_v1` 相对最强 baseline 的平均 margin 为负：
    - `PX-STC`: `-0.103`
    - `PX-STD`: `-0.116`
  - 结论：Stage 4 不支持把 PX4 的 state-transport 线写成 `family_aware_usdta_v1` 的强证据。

- `direct_transport`：`AP-DAB`
  - `bounded_noise` 拿下 `4 / 5`。
  - `family_aware_usdta_v1` 只在 `A2@throttle_biased` 赢一次。
  - 结论：direct-actuation line 仍主要偏向简单 noise baseline，而不是 family-aware latent design。

- `history_transport`：`AP-HTM` + `AP-HTS` + `AP-HTG`
  - `AP-HTM`: `family_aware_usdta_v1` 拿下 `4 / 4`
  - `AP-HTS`: `bounded_noise` 拿下 `5 / 5`
  - `AP-HTG`: `family_aware_usdta_v1` 拿下 `5 / 5`
  - 结论：history family 不是单一整体。`mixed-mode` 和 `guided_nogps` 支持 line-aware 设计，而 `stabilize-collapse` 线明确不支持。

## 六条线分章节结果

| line | official winner pattern | 当前正式结论 |
| --- | --- | --- |
| `PX-STC` | `bounded_noise 4 / 4` | `scenario projection decay` 仍更适合简单 noise baseline；`family_aware_usdta_v1` 没形成反超。 |
| `PX-STD` | `bounded_noise 4 / 4` | `locality drift` witness 下，line-aware latent 仍未胜过 baseline。 |
| `AP-DAB` | `bounded_noise 4 / 5` | `bundle leakage` 线总体仍由 baseline 主导；`family_aware_usdta_v1` 只在 `A2@throttle_biased` 给出单点突破。 |
| `AP-HTM` | `family_aware_usdta_v1 4 / 4` | 这是最干净的 family-aware 正证据：margin 不大，但四格都稳定占优。 |
| `AP-HTS` | `bounded_noise 5 / 5` | `collapse under regime shift` 线没有被 family-aware 修复；全方法 transfer 都很差。 |
| `AP-HTG` | `family_aware_usdta_v1 5 / 5` | 这是第二条 family-aware 正证据；但它更像“方法排序胜利”，不是“硬失败/强 crash superiority”。 |

### 补充说明

- `AP-HTM` 是 Stage 4 中最适合写成“family-aware gain is real”的主线。
- `AP-HTG` 虽然 `5 / 5` 全胜，但相对 reference 的平均提升只有 `+0.037`，因此证据强度弱于 `AP-HTM`。
- `AP-HTS` 则构成一个明确反例：同属 history-transport，但 `family_aware_usdta_v1` 在 witness contract 下并没有赢。

## Cross-Scenario / Cross-Mode Transfer

- 正式 Stage 4 的 official transfer 只比较 witness mode 内的 cross-scenario transfer。
- official matrix 没有把 cross-mode transfer 作为主结果，因此这里不写 cross-mode winner 结论。

### transfer 主结论

1. `AP-DAB` 是唯一一个对所有方法都保持正 retention 的 line。
   - `bounded_noise` 在 `A2` 上 retention `0.477`
   - `raw_space_random` 在 `A3` 上 retention `0.701`
   - `family_aware_usdta_v1` 只得到 `0.134` 与 `0.147`
2. `PX-STC`、`PX-STD`、`AP-HTM`、`AP-HTG` 的 retention 基本都围绕 `-1`，说明 nominal winner 迁移到 stress 后并不能稳定保持收益。
3. `AP-HTS` 是 transfer 最差的 line：
   - `family_aware_usdta_v1`: `-7.280`
   - `raw_space_random`: `-5.312`
   - `low_dim_agnostic`: `-3.387`
   - `bounded_noise`: `-10.119`
   这表明该线的主问题不是谁搜索得更强，而是 witness regime 本身会在 transfer 下快速 collapse。
4. 因此，Stage 4 不支持“`family_aware_usdta_v1` 具有全局 transfer superiority”的说法。

## Issue 与失败模式 Appendix

### winner rollout 总体画像

| issue | winner-rollout total | 解释 |
| --- | --- | --- |
| `active_horizon_exhausted` | `11452` | 最常见 issue；说明 winner 仍常在有效激活窗口耗尽后失去增益。 |
| `budget_saturation` | `5159` | 主要集中在 `low_dim_agnostic`，也出现在 `bounded_noise`。 |
| `zero_delta_collapse` | `2954` | `bounded_noise` winner 集里基本没有该问题，但 `low_dim_agnostic` 很严重。 |
| `alignment_failure` | `860` | 多出现在 history line 与 transfer rollout 中。 |
| `regime_gate_blocked` | `0` | official winner 不存在非法模式门禁主问题。 |
| `failsafe_or_truncation` | `0` | official winner 不支持“crash 主终点”结论。 |
| `search_stagnation` | `0` | 搜索器没有在主结果里表现为停滞性失败。 |

### 方法级 issue 特征

- `bounded_noise`
  - 优势：official winner 集里 `zero_delta_collapse = 0`
  - 代价：仍有明显 `budget_saturation`，且 transfer 在 `AP-HTS` 上最差

- `family_aware_usdta_v1`
  - 优势：winner 集的 `alignment_failure` 和 `budget_saturation` 都相对低
  - 代价：仍有 `active_horizon_exhausted` 与少量 `zero_delta_collapse`
  - 解释：它更像“更稳的 line-aware 改进”，而不是“能把系统推到硬失败”的方法

- `low_dim_agnostic`
  - 问题最重：`budget_saturation` 与 `zero_delta_collapse` 都是四方法里最差
  - 解释：去掉 line-aware structure 后，同预算 latent search 很难维持有效控制方向

- `raw_space_random`
  - 主要问题是 `active_horizon_exhausted`
  - 解释：raw-space baseline 有时能接近前二，但更像短时撞到局部有利方向，不够稳定

## Stage 4 总结

1. Stage 4 支持一个“有限而清晰”的主结论：
   `family_aware_usdta_v1` 不是全局 benchmark winner，但它确实在特定 history-transport witness 上提供了稳定增益，最强证据来自 `AP-HTM`，次强证据来自 `AP-HTG`。
2. Stage 4 同时给出明确边界：
   - 对 PX4 state-transport lines，`bounded_noise` 仍全面更强；
   - 对 `AP-DAB`，baseline 仍然主导；
   - 对 `AP-HTS`，family-aware 没能穿过 regime-shift collapse。
3. 因此，Stage 4 最合适的正式表述不是“family-aware globally wins”，而是：
   `family-aware attack design is selectively effective on specific history-transport regimes, but it does not displace simple noise baselines as the overall official Stage 4 winner.`
4. Stage 4 也不支持两个更强的说法：
   - 不支持“global transfer superiority”
   - 不支持“official crash superiority”

## Machine-Readable Artifact 与 Figure 链接

- [PART1 report](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/reports/STAGE4_PART1.generated.md)
- [PART2 report](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/reports/STAGE4_PART2.generated.md)
- [PART3 report](../../artifacts/studies/20260424_083814_stage4_part3_official_eval/reports/STAGE4_PART3.generated.md)
- [PART4 report](../../artifacts/studies/20260424_132931_stage4_part4_official_eval/reports/STAGE4_PART4.generated.md)
- [PART1 summary_json](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/summary/stage4_official_summary.json)
- [PART2 summary_json](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/summary/stage4_official_summary.json)
- [PART3 summary_json](../../artifacts/studies/20260424_083814_stage4_part3_official_eval/20260424_083815_stage4_official_six_line_eval/summary/stage4_official_summary.json)
- [PART4 summary_json](../../artifacts/studies/20260424_132931_stage4_part4_official_eval/20260424_132932_stage4_official_six_line_eval/summary/stage4_official_summary.json)
- [PART1 figures](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/reports/figures)
- [PART2 figures](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/reports/figures)
- [PART3 figures](../../artifacts/studies/20260424_083814_stage4_part3_official_eval/20260424_083815_stage4_official_six_line_eval/reports/figures)
- [PART4 figures](../../artifacts/studies/20260424_132931_stage4_part4_official_eval/20260424_132932_stage4_official_six_line_eval/reports/figures)
