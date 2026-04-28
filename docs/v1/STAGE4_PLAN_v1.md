# STAGE4 精简正式评估计划（USDTA v1, method-centered + crash endpoint）

## Summary

- `docs/v1/STAGE4_PLAN_v1.md` 作为正式执行合同，`docs/v1/STAGE4_START_v1.md` 仅保留 exploratory 记录，不参与正式主结果。
- 自本次归档起，本文是 `USDTA v1` 的正式执行合同归档；后续 `USDTA v2` 方案不回写到这份 plan。
- 正式 Stage 4 的首要目标不再是做六条 line 的全景覆盖，而是在一组代表性、肉眼可见差异明显、且具备异质性的 official benchmark cells 上，证明 `family_aware_usdta_v1` 相比其他 baseline 具有更高胜率、更大优势幅度和更好稳定性。
- 与此同时，正式 Stage 4 显式加入 `crash_or_hard_failure` 与 `crash_rate`，不再把 crash 相关现象只藏在 issue appendix 中。
- 正式 Stage 4 继续冻结四个官方方法：
  - `family_aware_usdta_v1`
  - `low_dim_agnostic`
  - `raw_space_random`
  - `bounded_noise`
- 正式 Stage 4 继续沿用三类官方 scenario 语义：
  - `nominal`
  - `dynamic`
  - `throttle_biased`
- 正式 Stage 4 继续沿用 Stage 3 的：
  - line-specific objective contract
  - budget contract
  - accepted / replay 规则
  - official issue registry
- 精简的对象是：
  - mode 数量
  - action 数量
  - scenario 数量
  - transfer 数量
- 不精简的对象是：
  - baseline 方法数量
  - baseline 搜索预算
  - baseline replay 合同
  - objective / issue / accepted 口径

---

## Stage Goal

### Primary Goal A：证明 USTDA 优于 baseline
在一组精简但具代表性的 official benchmark cells 上，证明：

1. `family_aware_usdta_v1` 在多数正式 cell 中优于最强 baseline；
2. 这种优势不仅体现在单次高分，也体现在 replay 后的均值优势与稳定性优势；
3. 这种优势不仅在 `nominal` 下成立，也能在选定 stress scenario 下保持；
4. 这种优势不是依赖单一 line，而是在跨 PX4 / ArduPilot、跨不同风险 family 的异质环境中重复出现。

### Primary Goal B：显式比较 crash / hard-failure 能力
在一个额外的小型 crash-focused 官方切片上，比较不同方法将系统推入明显硬失败的能力，形成：

1. `crash_rate`
2. `crash_margin_vs_best_baseline`
3. `USTDA crash win rate`
4. `stress_crash_retention`

### Non-Goals
以下内容不再作为正式 Stage 4 的主目标：

- 不追求六条 line 的全景覆盖叙事；
- 不追求双 mode 全覆盖；
- 不追求所有动作模板全覆盖；
- 不追求三类 scenario 在所有 line 上统一铺满；
- 不追求对所有方法做全量 cross-mode / illegal-mode / burst 边界普查。

这些内容若需要，仅作为 supplementary。

---

## Design Principles

### Principle 1: line 是 benchmark 载体，不是主角
六条 line 全部保留，是为了提供不同攻击语义、不同 primary risk、不同 backend 约束；
但正式主结果不围绕“哪条线最重要”展开，而围绕“USTDA 是否稳定优于 baseline”展开。

### Principle 2: 不削弱 cell 内公平比较，只压缩总矩阵
每个正式 cell 内，四方法仍按统一 budget、统一 scoring、统一 replay 规则比较。
精简的是总矩阵规模，不是方法间公平性。

### Principle 3: 只保留最容易拉开方法差距、且肉眼可见变化明显的 cell
正式主矩阵优先选择：
- 更容易观察到姿态偏转、轨迹漂移、明显波动的动作；
- 更容易放大 primary risk 的 stress scenario；
- 最能代表该 line 的 witness mode。

### Principle 4: crash 作为正式 endpoint 单独报告
`failsafe_or_truncation` 与未 accepted 的硬失败不再只作为 issue 附录存在；
必须汇总为显式的 `crash_or_hard_failure` 与 `crash_rate`。

---

## Frozen Official Elements

以下元素继续保持冻结，不因精简而改变。

### Methods
- `family_aware_usdta_v1`
- `low_dim_agnostic`
- `raw_space_random`
- `bounded_noise`

### Scenario Semantics
- `nominal`: 当前 baseline 频率/幅值。
- `dynamic`: 幅值 ×1.35、频率上移、PX4 提高起飞高度和 clearance。
- `throttle_biased`: nominal 频率不变，throttle scale ×1.2 且加 `+0.04` 归一化 bias，按 backend 字段等价落地。

### Action Template Definitions
- `A1 continuation_multibroad`: `profile_type=multi_broad`
- `A2 dominant_axis_sweep`: `profile_type=sweep`
- `A3 boundary_pulse_train`: `profile_type=pulse_train`
- `A4 alternating_memory_burst`: `profile_type=alternating_pulse_train`

### Objective / Budget / Issue Contracts
- 继续沿用 Stage 3 的 line-specific objective contract；
- 继续沿用当前四方法 budget 合同；
- 继续沿用 accepted / issue registry / replay 口径；
- 不增加新 baseline，不改权重，不改 regime gate 语义。

---

## Official Matrix Overview

正式 Stage 4 分为两层矩阵：

### Matrix A：official benchmark matrix
用于回答：
- USTDA 是否整体优于 baseline
- 优势幅度有多大
- 在 stress 下能否保持

### Matrix B：official crash slice
用于回答：
- USTDA 是否更容易把系统推到 crash / hard-failure
- 这种优势是否在高风险组合下更明显

---

## Matrix A：Official Benchmark Matrix

## 1. Witness Mode Selection

正式 Stage 4 不再对双 mode 线做双 mode 全覆盖。
每条 line 只保留一个最适合作为正式 benchmark 的 witness mode。

| line | witness mode | rationale |
| --- | --- | --- |
| `PX-STC` | `OFFBOARD_ATTITUDE` | 更容易观察到持续姿态偏转与可视偏离 |
| `PX-STD` | `OFFBOARD_ATTITUDE` | 更容易观察到局部漂移与轨迹失真 |
| `AP-DAB` | `STABILIZE` | 更直接暴露 throttle 主导耦合与 bundle leakage |
| `AP-HTM` | `STABILIZE` | 更容易观察到 conditioning saturation 的显著飞行变化 |
| `AP-HTS` | `STABILIZE` | 单 mode 保持不变 |
| `AP-HTG` | `GUIDED_NOGPS` | 单 mode 保持不变 |

说明：
- witness mode 的目标不是覆盖全部 mode 语义，而是为正式方法对比选择最清晰、最稳定、最容易拉开差距的观测窗口。
- 非 witness mode 仅作 supplementary witness，不进入正式主矩阵。

---

## 2. Official Action Selection

Matrix A 只保留两个动作：

- `A2 dominant_axis_sweep`
- `A3 boundary_pulse_train`

### 保留原因

#### A2 dominant_axis_sweep
- 更容易观察到持续偏转、轨迹漂移、姿态变化；
- 对方法优劣的可视差异通常更清晰；
- 更适合作为持续性攻击代表。

#### A3 boundary_pulse_train
- 更容易激发边界响应、突变、failsafe/truncation 前兆；
- 对方法在边界条件下的能力差异更敏感；
- 更适合作为边界激发型攻击代表。

### 降级处理
以下动作不进入 Matrix A：
- `A1 continuation_multibroad`
- `A4 alternating_memory_burst`

其中：
- `A1` 只在某条 line 的 A2/A3 证据不足时补跑；
- `A4` 不进入 benchmark matrix，但会在 Matrix B 的 crash slice 中部分恢复。

---

## 3. Official Scenario Selection

Matrix A 不再对每条 line 统一全跑 `nominal / dynamic / throttle_biased`。
改为每条 line 只保留：
- `1` 个 baseline scenario：`nominal`
- `1` 个最 relevant stress scenario

| line | nominal | targeted stress |
| --- | --- | --- |
| `PX-STC` | `nominal` | `dynamic` |
| `PX-STD` | `nominal` | `dynamic` |
| `AP-DAB` | `nominal` | `throttle_biased` |
| `AP-HTM` | `nominal` | `dynamic` |
| `AP-HTS` | `nominal` | `dynamic` |
| `AP-HTG` | `nominal` | `dynamic` |

说明：
- `dynamic` 是默认 stress，用于放大大多数 line 的可见运动变化；
- `AP-DAB` 的主风险更直接关联 throttle，因此保留 `throttle_biased`；
- 未进入正式矩阵的第三 scenario 不删除，但只用于 supplementary transfer 或补充复核。

---

## 4. Matrix A Cell Count

Matrix A 总计：

- `6 lines`
- `× 1 witness mode`
- `× 2 official actions`
- `× 2 scenarios`

即：

`6 × 1 × 2 × 2 = 24 official benchmark cells`

这 24 个 cell 是正式 Stage 4 的主 benchmark。

---

## 5. Matrix A Table

| line | witness mode | official scenarios | official actions |
| --- | --- | --- | --- |
| `PX-STC` | `OFFBOARD_ATTITUDE` | `nominal`, `dynamic` | `A2`, `A3` |
| `PX-STD` | `OFFBOARD_ATTITUDE` | `nominal`, `dynamic` | `A2`, `A3` |
| `AP-DAB` | `STABILIZE` | `nominal`, `throttle_biased` | `A2`, `A3` |
| `AP-HTM` | `STABILIZE` | `nominal`, `dynamic` | `A2`, `A3` |
| `AP-HTS` | `STABILIZE` | `nominal`, `dynamic` | `A2`, `A3` |
| `AP-HTG` | `GUIDED_NOGPS` | `nominal`, `dynamic` | `A2`, `A3` |

---

## Matrix B：Official Crash Slice

Matrix B 是一个小型 crash-focused 官方切片，用于显式比较不同方法触发硬失败的能力。

## 1. Crash Slice Design Rule

- 只挑最可能放大 crash / hard-failure 的高风险组合；
- 不追求全矩阵覆盖；
- 只保留最有展示价值的 line / scenario / action；
- 保持四方法预算公平，不降低 baseline 强度。

## 2. Crash Slice Cell List

| line | mode | scenario | action | rationale |
| --- | --- | --- | --- | --- |
| `PX-STC` | `OFFBOARD_ATTITUDE` | `dynamic` | `A3` | 边界脉冲下更容易出现明显失稳 |
| `AP-DAB` | `STABILIZE` | `throttle_biased` | `A3` | throttle 偏置 + 边界脉冲，最容易放大 bundle leakage |
| `AP-DAB` | `STABILIZE` | `throttle_biased` | `A4` | throttle 偏置 + burst，对短时硬失败更敏感 |
| `AP-HTS` | `STABILIZE` | `dynamic` | `A3` | regime shift 下边界脉冲更容易触发 collapse |
| `AP-HTS` | `STABILIZE` | `dynamic` | `A4` | burst 更容易放大失稳与掉控 |
| `AP-HTG` | `GUIDED_NOGPS` | `dynamic` | `A3` | empty-mask instability 在边界脉冲下更容易可见化 |
| `AP-HTG` | `GUIDED_NOGPS` | `dynamic` | `A4` | 交替 burst 更容易暴露 hard-failure 倾向 |

## 3. Matrix B Cell Count

Matrix B 总计：

`7 official crash cells`

---

## Total Official Execution Scope

正式 Stage 4 的官方执行范围为：

- Matrix A：`24` 个 benchmark cells
- Matrix B：`7` 个 crash cells

总计：

`31 official cells`

说明：
- Matrix B 并不是把全量 Stage 4 再做大，而是用最小附加成本补出“crash superiority”证据。
- 若某个 crash cell 与 Matrix A 完全重合，则只执行一次，并同时纳入两个统计口径。

---

## Execution Topology

### Backend Lanes
- `PX4 lane` 与 `ArduPilot lane` 并行执行，互不干扰。
- lane 内继续使用 backend persistent session。
- 继续支持 `checkpoint / resume`，避免掉线后重跑已 accepted 的 config attempts。

### Matrix Granularity
每个 official cell 绑定一个稳定 matrix root，便于：
- reference 采集
- 四方法正式搜索
- winner replay
- crash statistics
- transfer
- 断点续跑与复核

### Official Priority Order
建议正式执行顺序如下：

1. 先完成 Matrix A 的全部 `nominal` cells；
2. 再完成 Matrix A 的全部 stress cells；
3. 再完成 Matrix B crash cells；
4. 再做 winner-only transfer；
5. 最后视需要补做 supplementary。

---

## Part Schedule

正式 Stage 4 继续拆成四个 part：

| part | lines | official report |
| --- | --- | --- |
| `PART1` | `PX-STC` + `AP-DAB` | `docs/v1/STAGE4_PART1_v1.md` |
| `PART2` | `PX-STD` + `AP-HTM` | `docs/v1/STAGE4_PART2_v1.md` |
| `PART3` | `AP-HTS` | `docs/v1/STAGE4_PART3_v1.md` |
| `PART4` | `AP-HTG` | `docs/v1/STAGE4_PART4_v1.md` |

### Part Completion Definition
一个 part 完成，当且仅当：
- 对应 lines 的全部 Matrix A cells 已完成；
- 对应 lines 的全部 Matrix B crash cells 已完成；
- 每个 official cell 的四方法 winner 已确定；
- winner replay 已完成；
- 当前 part 的正式 markdown 报告已写入。

### Final Completion Definition
正式 Stage 4 完成，当且仅当：
- `PART1` 到 `PART4` 全部完成；
- `docs/v1/STAGE4_EVALUATION_v1.md` 已写入跨 part 的方法级总汇总；
- 已生成方法级主图与 crash 主图；
- supplementary 内容若存在，明确标注为附录，不混入主榜单。

---

## Execution And Scoring

## 1. Reference Collection

每个 official cell 先采：

- `3` 条 `no_attack` accepted reference runs

并固定：
- 取中位 `reference trace` 作为参考；
- accepted 不足时继续补采；
- 不允许用 exploratory 数据补齐 official reference。

---

## 2. Search Budget Contract

每个 official cell 内四方法搜索预算继续保持冻结，不作修改：

- `family_aware_usdta_v1`: `4` 轮 CEM × `6` candidates`
- `low_dim_agnostic`: 与 `family_aware_usdta_v1` 同维、同 optimizer、同预算
- `raw_space_random`: `16` 个 piecewise-knot candidates
- `bounded_noise`: `8` 个固定 seed candidates

说明：
- 精简 Stage 4 不通过削弱 baseline 预算来“制造胜利”；
- 正式主结论必须建立在 cell 内公平比较的基础上。

---

## 3. Candidate Selection And Replay

每个 official cell 内固定：

- 所有候选先各跑 `1` 条 accepted rollout；
- `family_aware_usdta_v1` 与 `low_dim_agnostic` 取 top-3 再各补 `2` 条 replay；
- `raw_space_random` 与 `bounded_noise` 取 top-2 再各补 `2` 条 replay；
- cell winner 以 replay 后的 `mean total_score` 决定；
- 同时保留：
  - `term_means`
  - `active_ratio`
  - `issue counts`
  - accepted 数量

说明：
- 若后续执行压力极大，允许将 replay 简化为统一 top-2 再补 `2` 条，但该修改必须一次性全局生效，不能只针对某一方法单独改动。
- 若未统一修改，则默认保持现合同不变。

---

## 4. Crash Endpoint Definition

`crash_or_hard_failure` 作为 Stage 4 的正式报告指标，不再只放在 issue appendix。

### 单条 rollout 记为 `crash_or_hard_failure = 1` 的条件
满足以下任一条件即可：

1. issue registry 命中 `failsafe_or_truncation`
2. rollout 未 accepted，且终止原因为明显硬失败/异常终止
3. 若当前 runner 暂无细粒度终止原因，则先采用保守代理：
   - `failsafe_or_truncation`
   - `not_accepted_rollout`

### 说明
- `crash_or_hard_failure` 的统计底层是所有执行过的 rollout，而不是只统计 accepted rollout。
- 这样可以避免因为“不 accepted 不入榜”而系统性低估 crash。

---

## 5. Official Metrics

### A. Cell-Level Primary Winner
每个 official cell 输出：
- 四方法 `mean total_score`
- winner
- winner margin vs second-best
- winner margin vs best baseline
- replay 稳定性指标
- issue 统计

### B. Crash Metrics Per Cell
每个 `(line, mode, action, scenario, method)` 必须额外报告：

- `crash_rate = crash_or_hard_failure_rollouts / all_executed_rollouts`
- `accepted_rate = accepted_rollouts / all_executed_rollouts`
- `winner_replay_crash_rate`
- `crash_margin_vs_best_baseline`

### C. Stage-Level Main Metrics
正式全局主结果统一围绕以下方法级指标展开：

1. `USTDA cell win rate`
   - `family_aware_usdta_v1` 在 Matrix A official cells 中赢了多少个

2. `winner_margin_vs_best_baseline`
   - 对每个 Matrix A cell，计算 USTDA 相对最强 baseline 的优势幅度

3. `issue-free win rate`
   - 统计 USTDA 获胜且没有关键 issue 污染的比例

4. `cross-scenario retention`
   - 统计 USTDA 在 stress 场景下保留优势的能力

5. `USTDA crash win rate`
   - 在多少 official cells 上，USTDA 的 `crash_rate` 高于最强 baseline

6. `crash_margin_vs_best_baseline`
   - 对每个 official cell，计算  
     `crash_rate(USTDA) - max(crash_rate(baselines))`

7. `stress_crash_retention`
   - 在 stress scenario 下，USTDA 的 crash / hard-failure 优势是否保持

8. `active_ratio`
   - 作为攻击活跃度与生效程度辅助指标

### D. Cross-Line Summary Rule
- line 内主榜单使用原始 `total_score`；
- 跨线总览不直接比较 raw `total_score`；
- 跨线总览只汇总方法级派生指标，不做 line-specific raw objective 的错误横比。

---

## Transfer Policy

### Official Transfer

#### within-scenario
- 每个 official scenario 独立搜索；
- 这是正式主结果的一部分。

#### cross-scenario transfer
- 不再对每个 `(line, mode, action, method)` 全量做 transfer；
- 改为：只对每个 Matrix A official cell 的 winner 做 transfer；
- 每个 winner transfer 到该 line 未被用于正式搜索的剩余 scenario；
- 每个 transfer 做 `3` 条 accepted repeats；
- transfer 结果只用于评估胜者的泛化保真度，不重开新的方法竞赛榜单。

### Crash Slice Transfer
- Matrix B 不强制全做 transfer；
- 仅当某个 crash cell 里：
  - USTDA 明显高于 baseline，或
  - 最强 baseline 明显高于 USTDA
  时，才补做 `winner-only` replay transfer 作为附加说明。

### Supplementary Transfer
以下内容降为 supplementary：
- cross-mode transfer
- illegal-mode sanity
- 对所有方法全量做 cross-scenario transfer

---

## Supplementary Policy

以下内容不再阻塞正式主结论：

### Supplementary A
- `A1 continuation_multibroad`
- 非 crash slice 里的 `A4 alternating_memory_burst`

### Supplementary B
- 非 witness mode 对照实验
- `AP-HTS` / `AP-HTG` 的 illegal mode gate sanity replay
- cross-mode transfer chart
- 所有剩余 scenario 的补充结果

### Trigger Conditions
只有在以下情况之一发生时，才触发 supplementary 补跑：

1. official cell 中 USTDA 与最强 baseline 差距极小，主结论不稳；
2. official cell 的轨迹/姿态可视差异不明显，不足以支持展示；
3. 某条 line 的 primary risk 没有被 A2/A3 成功激发；
4. nominal 与 targeted stress 表现几乎一致，无法体现方法差异；
5. winner replay 波动异常，需要额外动作或额外 mode 复核；
6. crash 证据不足，需要额外补跑 `A4` 或剩余高风险场景。

---

## Interfaces And Outputs

- 不改 Stage 3 design contract；Stage 4 数据面只负责把六线/四方法/动作矩阵编排成正式实验。
- 继续沿用并扩展以下数据结构：
  - `Stage4ActionTemplate`
  - `Stage4EvalCell`
  - `cell_registry`
  - `reference_registry`
  - `winner_registry`
  - `method_leaderboard`
  - `transfer_results`
  - `issue_registry`
  - `term_decomposition`

### 新增或显式要求的字段
- `all_executed_rollouts`
- `accepted_rollouts`
- `crash_or_hard_failure_rollouts`
- `crash_rate`
- `accepted_rate`
- `crash_margin_vs_best_baseline`

### Per-Line Figures
每 line 至少产出：
- `leaderboard`
- `term_decomposition`
- `representative_trace`
- `issue_profile`

### Global Figures
全局至少产出：
- `method_win_overview`
- `winner_margin_heatmap`
- `crash_rate_overview`
- `crash_margin_heatmap`
- `stress_retention_summary`

### Representative Crash Figures
至少挑选 `3~5` 个最有展示力的 crash cells，给出：
- `no_attack`
- `USTDA winner`
- `best baseline winner`
- 关键姿态/轨迹/高度/控制量对比图
- 明确标注 crash / hard-failure 发生时刻

---

## Reporting Structure

## 1. Official Per-Part Reports
每个 `STAGE4_PARTx.md` 只写对应 lines 的正式结果，结构如下：

1. line 简介与 witness mode 说明
2. official benchmark table
3. official crash slice table
4. 每个 official cell 的四方法结果表
5. winner 分析
6. crash metrics 分析
7. 代表性轨迹/姿态图
8. 当前 part 的方法级小结

## 2. Final Evaluation Report
`docs/v1/STAGE4_EVALUATION_v1.md` 的顺序改为：

### Section A: 方法级主结论
- `USTDA cell win rate`
- `winner_margin_vs_best_baseline`
- `issue-free win rate`
- `cross-scenario retention`

### Section B: Crash 主结论
- `USTDA crash win rate`
- `crash_margin_vs_best_baseline`
- `stress_crash_retention`
- 代表性 crash / hard-failure 图

### Section C: 代表性可视化证据
挑选 `4~6` 个最有展示力的 official benchmark cells，给出：
- `no_attack`
- `USTDA winner`
- `best baseline winner`
- 关键姿态/轨迹/高度/控制量对比图

### Section D: line 级结果汇总
- 六条 line 各自的简明结论
- 但 line 不再是全文主线，只是 supporting evidence

### Section E: Supplementary And Boundary Notes
- `A1`
- supplementary `A4`
- cross-mode
- illegal-mode
- 其他补充边界

---

## Acceptance And QA

### Official Completion Criteria
正式 Stage 4 完成标准改为：

1. Matrix A 的 `24` 个 official benchmark cells 都有 `3` 条 accepted reference；
2. Matrix B 的 `7` 个 official crash cells 都有 `3` 条 accepted reference；
3. 全部 official cells 都完成四方法正式比较；
4. 全部 official cells 都产出 winner；
5. 全部 official cells 的 winner replay 已完成；
6. 全部 official cells 都生成：
   - `mean total_score`
   - `crash_rate`
   - `accepted_rate`
   - `issue counts`
7. 已生成方法级总表、crash 总表与主图；
8. `docs/v1/STAGE4_EVALUATION_v1.md` 已完成；
9. supplementary 不作为正式完成门槛。

### Result Admission Rules
- rollout 若未 accepted，不入主榜单，但必须进入 issue registry 和 crash 统计；
- winner 若 replay 后均值不稳定或 accepted runs 不足，必须重跑该 cell；
- 不允许把 exploratory 结果混入正式表格与正式图；
- 所有正式 figure 必须标注 `n`、CI/error bar、固定颜色、统一 legend；
- line 内 y 轴统一；方法级 summary 图和 crash 图的坐标口径统一。

### Official Issue Registry
继续沿用并扩展当前 Stage 4 的官方 issue 口径：
- `regime_gate_blocked`
- `active_horizon_exhausted`
- `budget_saturation`
- `alignment_failure`
- `failsafe_or_truncation`
- `zero_delta_collapse`
- `search_stagnation`

### Pre-Run Gating Rule
- 执行前只允许做环境门禁；
- 不允许把门禁结果写成正式结论；
- 门禁只用于保证 orchestration、alignment、attack trace、report pipeline 可用。

---

## Assumptions

- `docs/v1/STAGE4_PLAN_v1.md` 与 `docs/v1/STAGE4_EVALUATION_v1.md` 使用中文书写。
- `docs/v1/STAGE4_PART1_v1.md` 到 `docs/v1/STAGE4_PART4_v1.md` 同样使用中文书写，且只写各自 part 的正式结果。
- 官方 Stage 4 只评估现有四方法，不增加新 baseline，不改 Stage 3 budgets、objective weights、regime gates。
- 核心 scenario 继续沿用 `nominal / dynamic / throttle_biased`，不引入第四类 scenario 名称。
- 对外主结论默认写成：
  - `family_aware_usdta_v1` 在多少 official cells 上优于 baseline
  - 优势幅度有多大
  - crash / hard-failure 优势是否存在
  - 在 stress 下是否仍然保持
- 不再默认把对外结论写成“哪条 line 更值得研究”或“哪条 line 的风险边界最复杂”。

---

## One-Sentence Decision Rule

正式 Stage 4 的执行原则只有一句话：

**优先保留最能稳定拉开 `family_aware_usdta_v1` 与 baseline 差距、且肉眼能观察到明显飞行变化的 official benchmark cells；同时用一个最小化的 official crash slice，把 crash / hard-failure 能力作为显式正式指标补齐。**
