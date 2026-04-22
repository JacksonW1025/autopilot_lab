# autopilot_lab

`autopilot_lab` 当前保留三段正式研究链，外加一段 exploratory Stage 4 起步层：

`sparsity hypothesis -> empirical validation -> stage-2 common-cause synthesis -> stage-3 attack design -> stage-4 exploratory pilot`

## Source Of Truth

当前 repo-level canonical 文档只有三份：

1. `README.md`
2. `docs/STAGE1_SUMMARY.md`
3. `docs/STAGE2_SUMMARY.md`

扩展分析/设计文档：

- `docs/STAGE2_DEEP_ANALYSIS.md`
- `docs/STAGE3_REFERENCE.md`
- `docs/STAGE3_ATTACK_DESIGN.md`
- `docs/STAGE4_START.md`

说明：

- `docs/STAGE2_DEEP_ANALYSIS.md` 用于保存较深的解释框架、研究假说与后续分析建议。
- 它不是新的 canonical source of truth，不替代上面的三份文档。
- `docs/STAGE3_REFERENCE.md` 是 Stage 3 启动前的参考筛选结果。
- `docs/STAGE3_ATTACK_DESIGN.md` 是 Stage 3 design layer 文档，用于固定 `USDTA` 的算法设计与接口，不是新的 evidence summary。
- `docs/STAGE4_START.md` 是 Stage 4 exploratory kickoff 文档，用于说明第一轮 `PX-STC @ POSCTL` pilot 为什么这样开始、会看什么、不会宣称什么。

## 当前保留范围

- Stage 1：四个 generalization study，负责证明 `Y ≈ fX (+ b)` 在 PX4 与 ArduPilot 上都存在可重复的线性证据。
- Stage 2：一个六线共同成因 study，负责把机制证据组织成统一的机制账本、类比结构和 `USDTA` 设计约束。
- Stage 3：一个 attack design study，负责把 Stage 2 的 six-line / three-family 证据编译成统一 `USDTA` attack algorithm 的 family-aware 设计、runtime API 和 machine-readable contract。
- Stage 4：一个 exploratory PX4 pilot，负责把 `PX-STC` 的 Stage 3 contract 接到真实 rollout 链路中，先观察效果、失败模式和评估问题。

## Stage 1

当前保留的 Stage 1 artifact：

1. `artifacts/studies/20260410_224818_px4_real_generalization_ablation`
2. `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`
3. `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation`
4. `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix`

当前关键数字：

- PX4 baseline `accepted_run_count = 30`, `generalized_supported = 80`
- PX4 diagnostic `accepted_run_count = 48`, `generalized_supported = 111`
- ArduPilot baseline `accepted_run_count = 30`, `generalized_supported = 12`
- ArduPilot diagnostic `accepted_run_count = 48`, `generalized_supported = 12`

## Stage 2

当前 Stage 2 把六条机制线组织成六个带仿真器信息的机制代号：

- `PX-STC`: PX4 State Transport Continuation
- `PX-STD`: PX4 State Transport Differential
- `AP-DAB`: ArduPilot Direct Actuator Bundle
- `AP-HTM`: ArduPilot History Transport MixedMode
- `AP-HTS`: ArduPilot History Transport STABILIZE
- `AP-HTG`: ArduPilot History Transport GUIDED_NOGPS

当前 canonical Stage 2 study：

- `artifacts/studies/20260421_090255_stage2_six_line_common_cause_analysis`

新的 Stage 2 只回答三类问题：

- 哪些低维 `X` 子空间稳定映射到紧凑 `Y` bundle
- 哪些 `state / direct / history transport` 机制在不同 backend 与 regime 中复现
- 哪些边界真正由 leakage、conditioning 与 regime shift 主导

它直接导出 `USDTA` 的设计约束。

## Stage 3

当前 Stage 3 将 `USDTA` 正式落成 design layer：

- family-aware attack algorithm
- online runtime API
- offline design compiler
- machine-readable objective / regime / budget contract

当前 canonical Stage 3 study：

- `artifacts/studies/20260421_115334_stage3_attack_design`

当前 Stage 3 只回答三类问题：

- 如何把 `PX-STC/PX-STD/AP-DAB/AP-HTM/AP-HTS/AP-HTG` 统一编译成三类 family 下的六条 instantiation
- 如何把 `bundle / leakage / conditioning / regime / budget` 固定为 machine-readable attack contract
- 如何把 runtime 输出严格限制为 4 通道 command delta，同时把 state/history 只保留为 context

## 当前结论

- `Y ≈ fX (+ b)` 的 empirical validation 已成立。
- 六条机制线现在按统一代号组织。
- `PX-STC/PX-STD` 共同定义 PX4 的 state-transport 家族。
- PX4 当前最关键的 retained 信号来自把当前状态并入 `X`；history 的额外收益很小，因此更像短时闭环状态传播，而不是长记忆模板。
- `AP-DAB` 是 ArduPilot 的 direct-transport 实例。
- `AP-DAB` 仍是 ArduPilot 当前最干净、最稳的 retained direct line；代表组合仍是 `commands_only -> actuator_response -> ridge_affine -> pooled`。
- `AP-HTM/AP-HTS/AP-HTG` 共同定义 history-transport 家族，其中边界主要由 conditioning、mask collapse 和 regime split 决定。
- ArduPilot 的 history/state-evolution 路径不是没有线性，而是长期被 `conditioning` 或 `mixed` 阻塞；当前问题首先是可识别性和稳定性，而不只是 `R²`。
- 当前 Stage 2 的目标是为统一算法 `USDTA` 提供设计指导。
- 当前 Stage 3 已经把 `USDTA` 落成统一 runtime 公式：`δu_t = Π_budget(A_line ψ_family(z, q_t))`。
- 当前 Stage 3 明确规定 runtime 只能输出 4 通道 command delta；state/history 只能作为 context 进入 family generator。
- 当前 Stage 3 的产物是 design contract，不是 Stage 4 评估结果。
- 当前 Stage 4 只启动了 `PX-STC @ POSCTL` 的 exploratory pilot；它的目标是发现 integration/search/scoring 问题，不是输出最终 benchmark 结论。

## 阅读顺序

1. `README.md`
2. `docs/STAGE1_SUMMARY.md`
3. `docs/STAGE2_SUMMARY.md`
4. `docs/STAGE2_DEEP_ANALYSIS.md`
5. `docs/STAGE3_REFERENCE.md`
6. `docs/STAGE3_ATTACK_DESIGN.md`
7. `docs/STAGE4_START.md`
8. `artifacts/studies/20260421_090255_stage2_six_line_common_cause_analysis/reports/stage2_six_line_common_cause.md`
9. `artifacts/studies/20260421_115334_stage3_attack_design/reports/stage3_attack_design.md`

## 正式入口

Stage 1：

- `scripts/run_px4_generalization_full.sh`
- `scripts/run_ardupilot_generalization_full.sh`
- `scripts/visualize_fit_matrices.py`

Stage 2：

- `scripts/analyze_stage2_six_line_common_cause.py`

Stage 3：

- `scripts/analyze_stage3_attack_design.py`

Stage 4：

- `scripts/run_stage4_px4_px_stc_posctl.sh`

## 目录

- `artifacts/studies/`: 正式 study artifact
- `configs/`: Stage 1 retained config
- `docs/`: Stage 1/Stage 2 canonical summary、Stage 3 reference / design 文档，以及 Stage 4 exploratory kickoff 文档
- `scripts/`: 当前正式入口
- `src/`: retained analysis code
- `tests/`: 保留后的最小回归集
