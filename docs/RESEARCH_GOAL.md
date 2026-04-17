# 研究目标

`autopilot_lab` 当前阶段的正式主问题已经切到 `Formal V2`，它同时回答两条同级问题：

> 1. 在统一 schema 口径下，是否存在一个固定的全局线性或仿射映射 `Y ≈ fX (+ b)`，并且它能在多种 scenario 下继续保持可接受的解释力？
>
> 2. 对 ArduPilot 而言，当我们把 mode 拆开以后，state-evolution 这条更难的线性关系，是否已经形成成熟正结论；如果没有，是否已经足够形成成熟负结论？

所以当前重点不只是“线性 `f` 是否存在”，还包括：

- 这个 `f` 是否只在单一 `nominal` 条件下看起来成立；
- 还是在 `nominal / dynamic / throttle_biased` 三档状态下，仍然能保持 `generalized_supported`；
- ArduPilot 的 state-evolution 在 `STABILIZE`、`GUIDED_NOGPS` 两个 mode 各自隔离后，是否仍能稳定成立。

## X、Y、f 分别代表什么

- `X` 是当前能拿来解释未来响应的信息。
  例如命令、当前状态、短历史、执行器反馈，或者这些量的线性特征映射。
- `Y` 是稍后要预测的结果。
  例如下一时刻状态、状态子集、未来短窗响应，或者执行器响应。
- `f` 是一张固定矩阵，`b` 是固定偏置项。

如果同一张矩阵在大量数据上都能稳定工作，而且不是靠个别片段凑出来的，就说明这里有可接受的线性证据。

## 当前正式判读标准

- `supported`
  当前 study 下，已经得到可接受的线性证据。
- `generalized_supported`
  不仅 overall 是 `supported`，而且三个 scenario 的 subgroup 指标都过线，并且跨 scenario 一致性足够高。
- `supported_but_local`
  overall 虽然 `supported`，但更像只在局部 operating point 站得住。
- `not_generalized`
  当前还不能把它当成跨 scenario 的常见映射。
- `mature_positive`
  至少一个 strict-raw-linear state-evolution 组合同时在 baseline、diagnostic 和 sparse-edge overlap 上保持稳定。
- `mature_negative`
  state-evolution 长期表现为高 `R2`、高条件数和稳定 sparse edges，因此已经足够形成成熟负结论。
- `inconclusive`
  targeted line 已有正式 artifact，但 state-evolution 还没有收敛到成熟正/负结论。

## 当前 repo-stage 判断

如果按 `sparsity hypothesis -> empirical validation -> insight -> attack algorithm -> evaluation` 这条故事看当前仓库：

- `theory / hypothesis` 已完成
- `empirical validation` 已完成
- `insight` 已完成
- 当前真正的工作重点已经从“继续证明线性存在”切到“从 insight 中抽出可执行的窄 target”

这一步现在分成两条线：

- A2 主线
  - 目标：把 ArduPilot 的 direct-control 结构收敛成可评估、可进入 live evidence 的算法接口
  - 当前状态：`GUIDED_NOGPS + pair_imbalance_12_vs_34` 已经 `ready_for_pair_attack_v1`，并进入 `algorithm spec + offline evaluation + live evaluation + live campaign`
- A1 对照线
  - 目标：把 PX4 的 state-continuation 结构收窄成可复现、可讲述的 contrast line
  - 当前状态：`future_state_roll / future_state_pitch` 已经 `ready_for_targeted_reproduction_v1`

## 当前解释原则

- backend 差异始终是次级解释。
  主解释永远先看“统一 schema 下的线性关系是否存在，以及是否跨 scenario 站得住”。
- generalization full 回答“线性关系总体是否存在、是否跨 scenario 反复出现”。
- ArduPilot targeted line 回答“state-evolution 在不混 mode 的条件下，是否已经足够成熟”。
- 如果 PX4 和 ArduPilot 都出现相似的 `generalized_supported` 结果，这会增强“线性结论本身可信”的解释力度。
- 如果一边更宽、一边更窄，也先解释为“线性证据的范围不同”，而不是立刻上升为“backend 输赢”。
- 如果出现高 `R2` 但 support 不稳的结果，必须同时看条件数、系数稳定性、scenario generalization 和 sparsity overlap，不能只看拟合分数。
- 当前 next-step 的优先级不是“再开更宽的 validation”，而是：
  - 主线把 A2 从 readiness 推进到 `algorithm spec + offline/live evaluation + medium robustness campaign`
  - 对照线把 A1 保持为 reproducible continuation evidence
