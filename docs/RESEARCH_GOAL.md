# 研究目标

`autopilot_lab` 当前阶段的正式主问题是：

> 在统一 schema 口径下，是否存在一个固定的全局线性或仿射映射 `Y ≈ fX (+ b)`，并且它能在多种 scenario 下继续保持可接受的解释力？

这里的重点已经不只是“线性 `f` 是否存在”，而是进一步追问：

- 这个 `f` 是否只在单一 `nominal` 条件下看起来成立；
- 还是在 `nominal / dynamic / throttle_biased` 三档状态下，仍然能保持 `generalized_supported`。

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

## 当前解释原则

- backend 差异始终是次级解释。
  主解释永远先看“统一 schema 下的线性关系是否存在，以及是否跨 scenario 站得住”。
- 如果 PX4 和 ArduPilot 都出现相似的 `generalized_supported` 结果，这会增强“线性结论本身可信”的解释力度。
- 如果一边更宽、一边更窄，也先解释为“线性证据的范围不同”，而不是立刻上升为“backend 输赢”。
- 如果出现高 `R2` 但 support 不稳的结果，必须同时看条件数和系数稳定性，不能只看拟合分数。
