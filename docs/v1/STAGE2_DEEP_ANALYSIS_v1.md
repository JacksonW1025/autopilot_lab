# Stage 2 Deep Analysis

## 定位

本文是对当前 Stage 2 retained evidence 的扩展整理，用来保存更深入的解释框架、数学化直觉与后续实现建议。

- 当前 canonical source of truth 仍然只有三份文档：
  - `README.md`
  - `docs/v1/STAGE1_SUMMARY_v1.md`
  - `docs/v1/STAGE2_SUMMARY_v1.md`
- 本文不替代上述三份文档；它的职责是把较深的解释、合理推断与后续工作方向组织清楚。
- 本文不提供可执行实施流程、参数搜索步骤或脚本；只讨论机理重建、数学解释和后续分析框架。

## 1. 证据基线

### 1.1 当前可直接引用的 retained artifact

- Stage 1 retained study：
  - `artifacts/studies/20260410_224818_px4_real_generalization_ablation`
  - `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`
  - `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation`
  - `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix`
- Stage 2 retained study：
  - `artifacts/studies/20260421_090255_stage2_six_line_common_cause_analysis`
- 与这五个 study 直接配套、当前仍在主树中的 supporting artifact：
  - `study_summary.json`
  - `scenario_generalization.json` / `scenario_holdout.json`
  - `sparsity_overlap.json`
  - `diagnostic_gate.json`
  - `state_evolution_audit.json`

### 1.2 历史材料的使用边界

- 历史 `formal-v2` 相关材料现在不属于当前 repo 的 canonical 入口。
- 它们可以作为背景知识或启发，但不应作为当前主结论的唯一证据来源。
- 因此，本文所有“当前已成立”的判断，都以 retained Stage 1 / Stage 2 artifact 为准。

## 2. 执行摘要

当前仓库已经不只是“证明线性存在”。

更准确地说，当前研究已经进入这样一个阶段：

- Stage 1 负责证明 `Y ≈ fX (+ b)` 在 PX4 与 ArduPilot 上都存在可重复的正面 evidence。
- Stage 2 负责把 retained evidence 组织成六条机制线，再进一步归并为三类 `transport family`。
- 当前最有价值的输出不再是“哪条线分数最高”，而是：
  - 哪类 family 在当前 regime 下最可信；
  - 哪些边界由 `leakage / conditioning / regime shift` 主导；
  - 统一算法在 family、bundle 与 regime 上必须遵守哪些设计约束。

本文的核心判断分两层：

- 当前 retained artifact 已经直接支持：
  - `PX-STC/PX-STD` 构成 PX4 的 state-transport 家族；
  - `AP-DAB` 是 ArduPilot 最干净的 direct-transport 实例；
  - `AP-HTM/AP-HTS/AP-HTG` 确实构成 history-transport 家族，但边界明显受 `conditioning / mask collapse / regime split` 限制。
- 当前 retained artifact 还没有完全证明、但已经值得作为研究假说推进：
  - family 可以被理解为不同的 `sufficient-statistic hypothesis`；
  - history family 的稳定对象更可能是 temporal subspace，而不是逐项 lag 系数；
  - 稳定结构更可能体现在 bundle graph / low-dimensional subspace 上，而不是 raw matrix entry。

## 3. 证据链重建

### 3.1 仓库主叙事已经改变

当前仓库主链是：

`sparsity hypothesis -> empirical validation -> stage-2 common-cause synthesis`

这意味着当前研究重点已经从“找 winner line”转到“组织共同成因与设计约束”。

### 3.2 六条线已经是 Stage 2 的正式对象

当前正式六线代号为：

- `PX-STC`
- `PX-STD`
- `AP-DAB`
- `AP-HTM`
- `AP-HTS`
- `AP-HTG`

这六条线在代码中也被固定写入 `LINE_SPECS`，而不是口头叙事。

### 3.3 Stage 1 依然提供最关键的底层统计事实

当前 retained Stage 1 还在回答三个最硬的问题：

- 是否存在跨场景重复出现的线性/仿射映射；
- 哪些组合在 holdout 下仍成立；
- 哪些路径更干净，哪些路径虽然高分但病态。

### 3.4 `state_evolution_audit` 提供了关键边界信息

这一步很重要，因为它揭示了：

- PX4 的 state-evolution 路径已经是大规模 supported；
- ArduPilot 的 state-evolution 路径不是没有线性，而是长期被 `condition_number` 或 `mixed` 阻塞。

## 4. 当前可直接采纳的判断

### 4.1 六条线应被理解为三类 family，而不是六条独立 winner line

当前 retained evidence 最自然的统一解释是三大家族：

- PX4 State Transport Family：
  - `PX-STC`
  - `PX-STD`
- ArduPilot Direct Transport Family：
  - `AP-DAB`
- ArduPilot History Transport Family：
  - `AP-HTM`
  - `AP-HTS`
  - `AP-HTG`

这一点已经是当前 `README`、`STAGE2_SUMMARY` 与 Stage 2 脚本的共同叙事，不再是个人解释。

### 4.2 PX4：当前状态一旦进入 `X`，拟合质量几乎饱和

当前 Stage 1 summary 里的 `schema_stepups` 很直接：

- PX4 baseline：`commands_only -> commands_plus_state` 的 `R²` 增益约为 `0.486`
- PX4 diagnostic：同一步骤的 `R²` 增益约为 `0.807`
- 但 `commands_plus_state -> history` 的进一步增益只有约 `0.0013`

这说明：

- PX4 的主要信息增益来自把当前状态并入 `X`
- 长 history 在 retained 设置下几乎不再带来额外解释力
- 因而当前最稳的解释是“短时闭环状态传播”，不是“长记忆模板”

`state_evolution_audit` 也支持这一点：

- PX4 baseline 当前有 `75` 个 supported state-evolution combo
- PX4 diagnostic 当前有 `78` 个 supported state-evolution combo

所以，`PX-STC/PX-STD` 被解释为 state-transport 家族，不只是命名方便，而是与 retained evidence 一致。

### 4.3 ArduPilot：当前最干净的稳定核心仍是 direct transport

当前 Stage 1 的 canonical representative combo 仍然是：

- `commands_only -> actuator_response -> ridge_affine -> pooled`

同时，当前 leave-one-scenario-out holdout 结果显示：

- baseline `all_holdouts_supported = 24`
- diagnostic `all_holdouts_supported = 24`
- representative combo 仍然都是 `commands_only | actuator_response | ridge_affine | pooled`

再结合 Stage 2 当前命名：

- `AP-DAB` 的 evidence tag 是 `support_backed, low_conditioning`
- baseline / diagnostic 条件数约为 `1.51 / 1.04`

因此可以直接采纳的判断是：

- 在当前 retained Stage 2 命名体系内，`AP-DAB` 是 ArduPilot 侧最干净、最稳定、最容易解释的 direct-transport 代表线。

这里需要保留一个精确限定：

- 这并不意味着 ArduPilot 只有 actuator-response 这一条 commands-only 结构；
- 它的意思是，在当前六线体系里，`AP-DAB` 是 direct family 的 canonical representative。

### 4.4 ArduPilot history family：线性痕迹真实存在，但边界明显

`AP-HTM/AP-HTS/AP-HTG` 共同说明 history transport 不是虚构现象。

但 retained artifact 同样显示，这个家族与 `AP-DAB` 完全不同：

- `AP-HTM`
  - `partial_mask`
  - baseline / diagnostic 条件数约为 `2.16e9 / 8.99e8`
  - feature mass 中 history 约占 `0.75`
  - top-edge 在跨阶段上会迁移
- `AP-HTS`
  - `collapse_prone, regime_limited`
  - 两阶段 `support_nonzero_count = 0`
  - 仍能给出高 `R²`
  - 说明 regime 内确实有结构，但支撑面容易塌掉
- `AP-HTG`
  - `raw_stable, empty_mask`
  - 两阶段 `support_nonzero_count = 0`
  - history mass 约为 `0.75`
  - raw top edge 能保留一部分，但稳定 mask 仍为空

更关键的是 `state_evolution_audit`：

- ArduPilot baseline：`current_supported_state_evolution_count = 0`
- ArduPilot diagnostic：`current_supported_state_evolution_count = 0`
- 主阻塞项长期是 `condition_number` 或 `mixed`

因此当前可直接采纳的结论不是“history family 没有结构”，而是：

- 它确实存在强线性痕迹；
- 但当前 retained pipeline 里，最主要的问题已经不是 `R²`，而是可识别性与数值稳定性。

### 4.5 当前更可信的是 bundle、subspace 和 regime，而不是单个系数

这一点在 retained artifact 里已经有足够迹象：

- Stage 2 一开始就把目标写成 `compact Y bundle`
- `AP-HTM/AP-HTG` 中反复出现多个 lag 近乎均分到同一 response 的现象
- `AP-HTS/AP-HTG` 在 raw top-edge、mask 与 regime 上表现出明显分裂

所以当前最合理的表述是：

- 真正稳定的对象更像 family 级别的方向、bundle 与 regime 边界；
- raw matrix 的逐项系数不应被直接当成最终机制真相。

## 5. 可以推进、但仍应标为研究假说的解释

下面这些判断与 retained evidence 一致，但当前 repo 还没有把它们证明为 canonical fact。

### 5.1 `sufficient statistic` 假说

可以把三大家族理解成三种“谁在当前 regime 下最像充分统计量”的假说：

- PX4：
  - 当前状态最像充分统计量
- `AP-DAB`：
  - 紧凑 command bundle 最像充分统计量
- `AP-HT*`：
  - temporal subspace 最像充分统计量

这是很有解释力的统一视角，但目前应写成工作假说，而不是已证定理。

### 5.2 temporal subspace / temporal kernel 假说

在 history family 里，未来状态经常被 `current + lag1 + lag2 + lag3` 近乎平均地表示。

这更像：

- 一个 temporal subspace
- 或一个低阶 temporal kernel

而不是：

- “系统真的需要这四个时刻的精确固定系数”

这个解释很值得推进，但目前更适合作为后续分析方向。

### 5.3 矩阵等价类与 bundle graph 假说

由于存在：

- 重参数化
- 强 lag collinearity
- mode / regime split

稳定对象可能不是某个固定矩阵，而是：

- 一个低维结构等价类
- 一个 bundle-to-bundle graph
- 一个 family 内可交换的子空间表示

这同样是合理推断，但当前 retained artifact 还没有把它完全形式化。

## 6. 对后续算法/分析设计的约束

### 6.1 当前已经被证据强烈支持的约束

- `family first`
  - 先区分 `state_transport / direct_transport / history_transport`
- `support first, score second`
  - 先看 `support / holdout / overlap / conditioning / regime`
  - 再看 `R²`
- `bundle first`
  - 先追 bundle、dominant subspace 与 response family
  - 不要先盯某条单边
- `regime-gated`
  - history family 的解释必须保留 mode / regime 条件

### 6.2 当前更像工程建议而非既成结论的约束

- `history must be compressed`
  - history family 不应直接把 raw lag coefficient 当成机制真相
  - 更合理的做法是先压到 temporal basis，再做解释
- `piecewise-affine over global-affine`
  - family-aware、regime-aware 的局部 chart，比一个全局大矩阵更符合 retained evidence

## 7. 建议的工程化方向

如果后续要把这套解释落成代码，建议把“证据统一”与“机制解释”拆开。

### 7.1 Evidence normalization

建议先补一个统一注册层，例如：

- `family_registry.py`
  - 统一记录 line code、family、backend、mode、scenario、support、conditioning、holdout 状态

### 7.2 Bundle extraction

- `stable_bundle_extractor.py`
  - 从 top edges、block share、target bundle compactness 中提取稳定 bundle
  - 优先输出 family-level 的重复结构

### 7.3 History compression

- `temporal_basis.py`
  - 专门服务于 history family
  - 把 raw lag 特征压成 mean / slope / curvature / energy 等时间基

### 7.4 Regime-aware local charts

- `regime_gate.py`
  - 按 backend / mode / scenario 做 gating
- `local_chart_builder.py`
  - 在 family × regime 上构建局部 affine chart

### 7.5 Evaluation / reporting

- `robustness_probe.py`
  - 做 simulation-only 的 family sensitivity / regime boundary 评估
- `countermeasure_report.py`
  - 输出 bundle、conditioning 与 regime 相关的监测/约束建议

## 8. 建议的产出顺序

一个更稳妥的实现顺序是：

1. 统一解析 Stage 1 / Stage 2 retained artifact
2. 构建 family registry
3. 抽取 stable bundle 与 dominant blocker
4. 对 history family 先做 temporal basis 压缩
5. 在 family × regime 上构建局部 chart
6. 输出 report 与 machine-readable summary

## 9. 当前最值得保留的十条表述

### 9.1 当前 evidence-backed 的表述

- PX4 的主线性证据更像闭环状态的短时传播，而不是裸命令的直接读出。
- ArduPilot 当前最干净的 retained direct line 是 `commands_only -> actuator_response` 所代表的 `AP-DAB`。
- ArduPilot 的 history 线并非没有价值；它们的问题首先是 `conditioning / mask / regime`，而不是 `R²` 不高。
- 高 `R²` 只能证明存在低误差表示，不能证明存在唯一稳定机制。
- 当前更可信的是 bundle-level 与 family-level 结构，而不是 raw entry-wise 权重。
- backend 之间当前共享的重点是 transport family 的抽象几何，而不是逐边重合。

### 9.2 当前更适合作为研究假说的表述

- 三大家族可以被理解成三种 `sufficient-statistic hypothesis`。
- history family 的稳定对象更可能是 temporal subspace，而不是固定 lag 系数。
- 稳定性边界的核心问题是识别问题，而不只是拟合问题。
- 后续统一算法应该是 family-aware、regime-aware、conditioning-aware 的局部 chart 系统。

## 10. 附录：本分析主要依赖的 artifact 类型

- 当前 `README.md` 的阶段叙事与保留范围
- 当前 `docs/v1/STAGE1_SUMMARY_v1.md`
- 当前 `docs/v1/STAGE2_SUMMARY_v1.md`
- Stage 2 六线共同成因报告与配套表格
- Stage 1 的 `study_summary`
- scenario generalization / scenario holdout
- sparsity overlap
- diagnostic gate
- state-evolution audit

## 11. 最后判断

如果只看 Stage 1，可以得到的结论是：

- PX4 有线性 evidence
- ArduPilot 也有线性 evidence

但把 retained Stage 2 六线命名、Stage 1 代表组合、holdout、overlap 与 state-evolution 一起看之后，更深的一步是：

- 当前仓库真正的价值，不再只是“线性已经证明”；
- 而是“线性 evidence 已经被组织成 family，并且这些 family 的稳定性来源、失败来源与设计边界已经开始清晰化”。

这也是本文建议保留的主叙事。
