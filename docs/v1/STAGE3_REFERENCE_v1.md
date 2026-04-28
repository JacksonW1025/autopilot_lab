# Stage 3 Reference For USDTA v1

## 定位

- 本文记录对一份外部参考材料的筛选结果，用于判断其是否值得进入 Stage 3 研究准备。
- 自本次归档起，本文只服务于已经落地并进入 Stage 4 official 评估的 `USDTA v1`；`USDTA v2` 另行定义，不回写到本文。

## 总判断

- 这份参考有价值，它把 Stage 2 的 `transport family` 证据组织成一个可执行的 Stage 3 研究框架。
- 最值得保留的核心主张是：搜索对象不应回到原始高维扰动空间，而应落在 Stage 1 / Stage 2 已支持的低维 `family coordinate` 上。

## 可直接采纳的部分

### 1. Stage 3 的主任务定义

- Stage 3 不应被理解为 `raw-space random attack`。
- 更准确的定义是：在 `budget`、`regime` 和 `family` 约束下，搜索能稳定放大闭环性能退化的结构化最坏方向。
- 这与当前 Stage 2 的 `family first / bundle first / support first` 叙事一致。

### 2. 六线继续按三类 family 组织

- `PX-STC/PX-STD` 应继续归入 `state_transport`。
- `AP-DAB` 应继续作为 `direct_transport` 的 canonical representative。
- `AP-HTM/AP-HTS/AP-HTG` 应继续归入 `history_transport`。
- Stage 3 的 evaluator、generator 和 baseline 都应围绕 `family registry` 展开，而不是回到逐线 `winner ranking`。

### 3. 搜索空间应是低维 family coordinate

- 推荐统一写成：

\[
w_t = \Phi(z, \mathcal{H}_t)
\]

- `z` 是低维搜索参数。
- `\Phi` 是 `family-aware` 的扰动生成器。
- `\mathcal{H}_t` 表示当前状态或短窗口历史。
- 真正应进入搜索空间的对象是：
  - `stable core basis`
  - `sparse support`
  - `transport mask`
  - `temporal basis`
  - `regime partition`
- 这与当前 Stage 2 强调的 `bundle / support / conditioning / regime` 优先级一致。

### 4. 目标函数应采用分解式退化指标

- 不应只用“是否失稳”或“是否坠机”这样的单一布尔指标。
- 更合理的 Stage 3 objective 应组合以下几类量：
  - `tracking deviation`
  - `attitude deviation`
  - `control saturation / boundary stress`
  - `recovery cost`
  - `budget penalty`
- 这样得到的是可比较、可复验的最坏情形评估器，而不是一次性的破坏展示。

### 5. 推荐的最小可行路径

- 先做 `single family + single backend + single mode` 的 `family-aware evaluator`。
- 先证明 `structured family search` 明显优于 `raw-space random search` 或 `bounded noise`。
- 先保证结果可解释，再追求更强的退化幅度。
- 这与 `docs/v1/STAGE2_DEEP_ANALYSIS_v1.md` 中“先做 family registry / bundle extraction / regime-aware chart”的顺序一致。

### 6. 复验必须跨场景进行

- 候选结构至少应跨以下维度复验：
  - `trajectory`
  - `seed`
  - `wind / noise`
  - `mode`
  - `backend`
- 但迁移对象应优先定义为 `family-level structure`，而不是具体参数值。
- 这与当前 Stage 2 对 `holdout`、`conditioning`、`regime` 的强调一致。

### 7. baseline 设计是有价值的

- `Random bounded noise`
- `Raw-space random search`
- `Family-agnostic low-dimensional search`
- `Family-aware search`
- 这组 baseline 能直接检验收益究竟来自“仅仅降维”，还是来自 Stage 1 / Stage 2 提炼出的结构理解。

## 应降格为研究假说的部分

- `state family` 一定对应“可稳定利用的局部仿射脆弱方向”。
- `direct family` 一定具有更高的单位预算退化效率。
- `history family` 的稳定对象一定是 `short causal kernel`，而不是其他时序表示。
- `family-aware > family-agnostic low-dim > raw-space random > bounded noise` 是值得检验的目标排序，但不是当前已证结论。
- `cross-backend transfer` 更可能发生在 `family geometry` 层，而不是参数值层；这仍需要 Stage 3 证据确认。

## 仅应作为工程偏好的部分

- `CEM` 适合作为首个黑箱优化器原型。
- `NES` 可作为连续、噪声较大的备选。
- `BO` 只适合极低维 `family parameter`。
- 这些判断可以指导首版实现，但它们不是当前 repo retained evidence 直接支持的研究结论。


## 对 Stage 3 的收束建议

- 如果 Stage 3 启动，其直接输入应来自 Stage 2 已整理出的结构对象：
  - `family registry`
  - `stable basis / support`
  - `target bundle projection`
  - `temporal basis`
  - `regime gate`
  - `budget projector`
- Stage 3 最先需要回答的问题不是“能否把系统搞崩”，而是：
  - Stage 2 的 family 证据，是否足以支持一个稳定、可解释、预算受限、可跨场景复验的 worst-case evaluator attack algorithm。
