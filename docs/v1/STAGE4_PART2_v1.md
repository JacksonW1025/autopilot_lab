# STAGE4 PART2 正式分批评估（USDTA v1）

## Part Contract

- 完成时间：`2026-04-24 05:02:24 PDT`
- 本文中所有 `family_aware_usdta_v1` 结果默认都指 `USDTA v1`。
- line scope: `PX-STD`, `AP-HTM`
- 有效 umbrella study: [20260423_133429_stage4_part2_official_eval](../../artifacts/studies/20260423_133429_stage4_part2_official_eval)
- 正式 nested eval: [20260423_133429_stage4_official_six_line_eval](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval)
- Matrix A unique benchmark cells: `8`
- references 已完成 `24` 条 accepted runs，transfer 已完成 `16` 条 emitted rows，见 [ardupilot_checkpoint.json](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/summary/lanes/ardupilot_checkpoint.json) 和 [px4_checkpoint.json](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/summary/lanes/px4_checkpoint.json)

本报告不直接照抄自动生成的 [STAGE4_PART2.generated.md](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/reports/STAGE4_PART2.generated.md)。

- 自动生成 markdown 的 `cell_wins` 是按“每方法都有一个 winner candidate”聚合，不是 cell-level primary winner。
- 当前 runner 发出的 transfer 是“all-method nominal -> dynamic transfer”，不是正式叙述里更有解释力的 winner-only transfer。

因此下面的主结论使用 `winner_registry.csv` 里每个 cell 的最高 `mean_score` 来定义 primary winner；transfer 只保留 `4` 条 winner-only rows。

## Main Findings

- `PART2` 呈现出非常清晰的 line split：`family_aware_usdta_v1` 赢下 `4/8` 个 official cells，而且这 `4` 格全部来自 `AP-HTM`；`bounded_noise` 也赢下 `4/8`，且全部来自 `PX-STD`。
- `USTDA` 相对最强 baseline 的 overall 平均 margin 只有 `-0.0104`，表面上接近打平；但按 line 拆开后是 `AP-HTM +0.0956`、`PX-STD -0.1164`，说明它不是“整体均匀略弱”，而是“在 AP 上有效、在 PX4 上失效”。
- `AP-HTM` 上 `USTDA` 最强的一格是 `A3 / dynamic`，margin `+0.2161`；最弱的一格是 `A2 / nominal`，margin 也还有 `+0.0248`。`PX-STD` 上最接近翻盘的是 `A3 / nominal`，但 margin 仍是 `-0.0549`。
- winner-only transfer 同样是 line split：`AP-HTM` 的 nominal winners 迁到 dynamic 后都明显掉分，`A2` 和 `A3` 分别是 `-0.9589`、`-0.9641`；`PX-STD` 的 nominal winners 迁到 dynamic 后基本持平，甚至小幅改善 `+0.0128`、`+0.0530`。
- 当前 part 没有任何 issue-free 的 primary winner。自动汇总里四种方法的 `issue_free_win_rate` 都是 `0`；issue profile 主要由 `active_horizon_exhausted = 46114`、`budget_saturation = 17278`、`zero_delta_collapse = 11485` 主导。

## Cell Winners

| cell | winner | winner score | USTDA margin vs best baseline |
| --- | --- | --- | --- |
| `PX-STD / A2 / nominal` | `bounded_noise c04` | `-1.6979` | `-0.1452` |
| `PX-STD / A2 / dynamic` | `bounded_noise c03` | `-1.7267` | `-0.1506` |
| `PX-STD / A3 / nominal` | `bounded_noise c08` | `-2.0865` | `-0.0549` |
| `PX-STD / A3 / dynamic` | `bounded_noise c02` | `-2.0784` | `-0.1148` |
| `AP-HTM / A2 / nominal` | `family_aware_usdta_v1 i02_c04` | `-12.8703` | `+0.0248` |
| `AP-HTM / A2 / dynamic` | `family_aware_usdta_v1 i02_c05` | `-12.8295` | `+0.0319` |
| `AP-HTM / A3 / nominal` | `family_aware_usdta_v1 i02_c04` | `-12.9059` | `+0.1097` |
| `AP-HTM / A3 / dynamic` | `family_aware_usdta_v1 i03_c03` | `-12.8685` | `+0.2161` |

## Per-Line Takeaways

### `PX-STD`

- `bounded_noise` 赢下 `4/4` 个 official cells，`USTDA` 没有翻盘。
- `USTDA` 最接近 baseline 的一格是 `A3 / nominal`，margin `-0.0549`；其余三格都在 `-0.11` 到 `-0.15` 区间。
- winner-only transfer 没有显示明显 locality collapse：`A2 nominal -> dynamic` 的 delta 是 `+0.0128`，`A3 nominal -> dynamic` 的 delta 是 `+0.0530`。
- 自动报告给出的 primary risk 是 `locality drift`，见 [px-std_transfer_heatmap.png](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/reports/figures/px-std_transfer_heatmap.png) 和 [px-std_issue_profile.png](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/reports/figures/px-std_issue_profile.png)。

### `AP-HTM`

- `family_aware_usdta_v1` 赢下 `4/4` 个 official cells，是 `PART2` 里唯一被它完整吃下的一条线。
- 四格 margin 分别是 `+0.0248`、`+0.0319`、`+0.1097`、`+0.2161`，说明 `A3` 比 `A2` 更像它的优势区。
- 但 nominal winners 迁到 dynamic 后都明显掉分：`A2` 是 `-0.9589`，`A3` 是 `-0.9641`，所以它在 `AP-HTM` 上更像 within-scenario winner，而不是稳健的 cross-scenario winner。
- 自动报告给出的 primary risk 是 `conditioning saturation`，见 [ap-htm_transfer_heatmap.png](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/reports/figures/ap-htm_transfer_heatmap.png) 和 [ap-htm_issue_profile.png](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/reports/figures/ap-htm_issue_profile.png)。

## Transfer Appendix

当前 emitted transfer rows 一共 `16` 条：

- `PX-STD`: `A2 nominal -> dynamic` 与 `A3 nominal -> dynamic`，四方法全量 transfer，共 `8` 条
- `AP-HTM`: `A2 nominal -> dynamic` 与 `A3 nominal -> dynamic`，四方法全量 transfer，共 `8` 条

正式叙述只保留 winner-only 子集。该子集一共 `4` 条：

| source winner | target scenario | method | source mean | transfer mean | delta |
| --- | --- | --- | --- | --- | --- |
| `PX-STD / A2 / nominal` | `dynamic` | `bounded_noise c04` | `-1.6979` | `-1.6852` | `+0.0128` |
| `PX-STD / A3 / nominal` | `dynamic` | `bounded_noise c08` | `-2.0865` | `-2.0336` | `+0.0530` |
| `AP-HTM / A2 / nominal` | `dynamic` | `family_aware_usdta_v1 i02_c04` | `-12.8703` | `-13.8291` | `-0.9589` |
| `AP-HTM / A3 / nominal` | `dynamic` | `family_aware_usdta_v1 i02_c04` | `-12.9059` | `-13.8700` | `-0.9641` |

所以 `PART2` 的 transfer 结论不是“winner 全部退化”，而是：

- `PX-STD` winners 基本保留了 nominal 下的强度。
- `AP-HTM` winners 在 dynamic 下明显退化，说明 `USTDA` 的收益更依赖 nominal 条件。

## Issue Appendix

| issue | count |
| --- | --- |
| `regime_gate_blocked` | `0` |
| `active_horizon_exhausted` | `46114` |
| `budget_saturation` | `17278` |
| `alignment_failure` | `467` |
| `failsafe_or_truncation` | `0` |
| `zero_delta_collapse` | `11485` |
| `search_stagnation` | `0` |

## Artifacts

- 综合 summary: [stage4_official_summary.json](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/summary/stage4_official_summary.json)
- 自动生成报告: [STAGE4_PART2.generated.md](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/reports/STAGE4_PART2.generated.md)
- 顶层表格:
  - [cell_registry.csv](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/tables/cell_registry.csv)
  - [winner_registry.csv](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/tables/winner_registry.csv)
  - [transfer_results.csv](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/tables/transfer_results.csv)
  - [issue_registry.csv](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/tables/issue_registry.csv)
  - [term_decomposition.csv](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/tables/term_decomposition.csv)
- Lane tables:
  - [ardupilot_rollout_registry.csv](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/tables/lanes/ardupilot_rollout_registry.csv)
  - [px4_rollout_registry.csv](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/tables/lanes/px4_rollout_registry.csv)
  - [ardupilot_transfer_results.csv](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/tables/lanes/ardupilot_transfer_results.csv)
  - [px4_transfer_results.csv](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/tables/lanes/px4_transfer_results.csv)
  - [ardupilot_issue_registry.csv](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/tables/lanes/ardupilot_issue_registry.csv)
  - [px4_issue_registry.csv](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/tables/lanes/px4_issue_registry.csv)
- Figures:
  - [px-std_leaderboard.png](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/reports/figures/px-std_leaderboard.png)
  - [ap-htm_leaderboard.png](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/reports/figures/ap-htm_leaderboard.png)
  - [px-std_transfer_heatmap.png](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/reports/figures/px-std_transfer_heatmap.png)
  - [ap-htm_transfer_heatmap.png](../../artifacts/studies/20260423_133429_stage4_part2_official_eval/20260423_133429_stage4_official_six_line_eval/reports/figures/ap-htm_transfer_heatmap.png)
