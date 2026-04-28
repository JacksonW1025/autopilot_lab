# STAGE4 PART1 正式分批评估（USDTA v1）

## Part Contract

- 完成时间：`2026-04-23 13:18:53 PDT`
- 本文中所有 `family_aware_usdta_v1` 结果默认都指 `USDTA v1`。
- line scope: `PX-STC`, `AP-DAB`
- 有效 umbrella study: [20260423_074820_stage4_part1_official_eval](../../artifacts/studies/20260423_074820_stage4_part1_official_eval)
- 正式 nested eval: [20260423_074820_stage4_official_six_line_eval](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval)
- Matrix A unique benchmark cells: `8`
- Matrix B unique crash cells in this part: `3`
  - 其中 `PX-STC / A3 / dynamic` 与 `AP-DAB / A3 / throttle_biased` 同时属于 `Matrix A + Matrix B`
  - 本 part 额外的 `Matrix B-only` cell 是 `AP-DAB / A4 / throttle_biased`
- references 已完成 `27` 条 accepted runs，transfer 已完成 `16` 条 accepted runs，见 [ardupilot_checkpoint.json](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/summary/lanes/ardupilot_checkpoint.json) 和 [px4_checkpoint.json](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/summary/lanes/px4_checkpoint.json)

本报告不直接照抄自动生成的 [STAGE4_PART1.generated.md](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/reports/STAGE4_PART1.generated.md)。原因有两点：

- 自动生成 markdown 的 `cell_wins` 是按“每方法候选 winner”聚合，不是 `STAGE4_PLAN` 要求的 cell-level primary winner。
- `winner_registry.csv` 中个别 baseline 会指向未 replay 的搜索候选，因此这里改用 `rollout_count >= 3` 的 replayed candidates 先确定每方法 official winner，再比较 cell winner。

另外，当前 runner 发出的 transfer 也是“all-method nominal -> stress transfer”，不是严格的 `winner-only transfer`。因此下面的 transfer 结论只使用从这 `16` 条 emitted rows 里裁出的 `4` 条 winner-only rows。

## Main Findings

- `family_aware_usdta_v1` 只赢了 `1/8` 个 Matrix A benchmark cells：`AP-DAB / STABILIZE / A2 / throttle_biased`。
- `bounded_noise` 是当前 `PART1` 的主导 baseline：赢下 `6/8` 个 Matrix A cells，并扫掉全部 `3/3` crash-slice cells。
- 剩下的 `1/8` benchmark cell 由 `raw_space_random` 获胜：`AP-DAB / STABILIZE / A2 / nominal`。
- USTDA 相对最强 baseline 的平均 margin 是 `-0.1608`，中位 margin 是 `-0.1599`；`PART1` 不支持“USTDA 在 `PX-STC + AP-DAB` 上整体优于 baseline”的主结论。
- cross-scenario retention 是 `0/4`：没有任何一个 `(line, action)` 对在 nominal 与 stress 两个 official cells 上同时保持 USTDA 正 margin。
- USTDA 的 crash win rate 是 `1/9`，唯一正 crash margin 出现在 `AP-DAB / A3 / nominal`，但官方 crash slice 本身是 `bounded_noise 3/3` 全胜。
- 在 critical-issue proxy `regime_gate_blocked + alignment_failure + failsafe_or_truncation` 下，USTDA 的 issue-free win rate 是 `0/1`。

## Cell Winners

`winner score` 只在 cell 内有意义；跨线比较以 `margin` 和 `crash margin` 为主，不直接横比 raw `total_score`。

`USTDA crash margin = crash_rate(family_aware_usdta_v1) - max(crash_rate(baselines))`，底层口径是所有执行 attempts，不只看 accepted runs。

| cell | role | winner | winner score | USTDA margin vs best baseline | USTDA crash margin |
| --- | --- | --- | --- | --- | --- |
| `PX-STC / A2 / nominal` | `Matrix A` | `bounded_noise c01` | `-1.4038` | `-0.0801` | `-0.0526` |
| `PX-STC / A2 / dynamic` | `Matrix A` | `bounded_noise c06` | `-1.3519` | `-0.0121` | `-0.0089` |
| `PX-STC / A3 / nominal` | `Matrix A` | `bounded_noise c07` | `-1.2138` | `-0.2018` | `0.0000` |
| `PX-STC / A3 / dynamic` | `Matrix A + B` | `bounded_noise c04` | `-1.2707` | `-0.1180` | `-0.0625` |
| `AP-DAB / A2 / nominal` | `Matrix A` | `raw_space_random c10` | `0.8001` | `-0.3036` | `0.0000` |
| `AP-DAB / A2 / throttle_biased` | `Matrix A` | `family_aware_usdta_v1 i03_c01` | `1.0285` | `+0.0875` | `0.0000` |
| `AP-DAB / A3 / nominal` | `Matrix A` | `bounded_noise c02` | `0.9861` | `-0.3564` | `+0.0333` |
| `AP-DAB / A3 / throttle_biased` | `Matrix A + B` | `bounded_noise c06` | `0.8199` | `-0.3020` | `-0.1333` |
| `AP-DAB / A4 / throttle_biased` | `Matrix B only` | `bounded_noise c05` | `0.9131` | `-0.4066` | `-0.0169` |

## Per-Line Takeaways

### `PX-STC`

- `bounded_noise` 赢下 `4/4` benchmark cells。
- USTDA 最接近 baseline 的一格是 `A2 / dynamic`，但 margin 仍是 `-0.0121`，没有翻盘。
- 官方 crash slice `PX-STC / A3 / dynamic` 同样由 `bounded_noise` 获胜，USTDA 的 crash margin 是 `-0.0625`。

### `AP-DAB`

- USTDA 只在 `A2 / throttle_biased` 这一格赢了 `bounded_noise`，margin `+0.0875`。
- `A2 / nominal` 被 `raw_space_random` 拿走；`A3 / nominal`、`A3 / throttle_biased`、`A4 / throttle_biased` 都由 `bounded_noise` 获胜。
- Crash slice 里最重要的两格 `A3 / throttle_biased` 和 `A4 / throttle_biased` 都不是 USTDA 优势区。

## Transfer Appendix

当前 emitted transfer rows 是 `16` 条：

- `AP-DAB`: `A2 nominal -> throttle_biased` 与 `A3 nominal -> throttle_biased`，四方法全量 transfer，共 `8` 条
- `PX-STC`: `A2 nominal -> dynamic` 与 `A3 nominal -> dynamic`，四方法全量 transfer，共 `8` 条

这比 `STAGE4_PLAN` 里的 winner-only transfer 更宽，因此正式叙述只保留 winner-only 子集。该子集一共 `4` 条，而且 `4/4` 都出现了负向迁移：

| source winner | target scenario | method | source mean | transfer mean | delta |
| --- | --- | --- | --- | --- | --- |
| `PX-STC / A2 / nominal` | `dynamic` | `bounded_noise c01` | `-1.4038` | `-1.5642` | `-0.1604` |
| `PX-STC / A3 / nominal` | `dynamic` | `bounded_noise c07` | `-1.2138` | `-1.5863` | `-0.3725` |
| `AP-DAB / A2 / nominal` | `throttle_biased` | `raw_space_random c10` | `0.8001` | `0.2509` | `-0.5492` |
| `AP-DAB / A3 / nominal` | `throttle_biased` | `bounded_noise c02` | `0.9861` | `0.4600` | `-0.5261` |

所以 `PART1` 的 nominal winners 在 stress scenario 下没有体现出强 transfer retention；即使是最终获胜的方法，迁移后分数也都明显下滑。

## Artifacts

- 综合 summary: [stage4_official_summary.json](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/summary/stage4_official_summary.json)
- Lane tables:
  - [ardupilot_rollout_registry.csv](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/tables/lanes/ardupilot_rollout_registry.csv)
  - [px4_rollout_registry.csv](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/tables/lanes/px4_rollout_registry.csv)
  - [ardupilot_issue_registry.csv](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/tables/lanes/ardupilot_issue_registry.csv)
  - [px4_issue_registry.csv](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/tables/lanes/px4_issue_registry.csv)
  - [ardupilot_transfer_results.csv](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/tables/lanes/ardupilot_transfer_results.csv)
  - [px4_transfer_results.csv](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/tables/lanes/px4_transfer_results.csv)
- Figures:
  - [px-stc_leaderboard.png](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/reports/figures/px-stc_leaderboard.png)
  - [ap-dab_leaderboard.png](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/reports/figures/ap-dab_leaderboard.png)
  - [px-stc_transfer_heatmap.png](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/reports/figures/px-stc_transfer_heatmap.png)
  - [ap-dab_transfer_heatmap.png](../../artifacts/studies/20260423_074820_stage4_part1_official_eval/20260423_074820_stage4_official_six_line_eval/reports/figures/ap-dab_transfer_heatmap.png)
