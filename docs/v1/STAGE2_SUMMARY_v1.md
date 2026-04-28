# Stage 2 Summary

## 目标

当前 Stage 2 把六条机制线组织成一组共同成因问题：

- 哪些低维 `X` 子空间稳定地映射到紧凑 `Y` bundle
- 哪些 `state / direct / history transport` 机制在不同仿真器与 regime 中重复出现
- 哪些边界真正由 leakage、conditioning 和 regime shift 主导

## 术语直观解释

- `X`：输入侧，也就是我们能施加或选取的那些量。
- `Y`：输出侧，也就是系统最后表现出来的响应。
- `bundle`：一组会一起变化的响应，不是单个输出量。
- `state transport`：状态传递，意思是当前状态会继续影响后续状态。
- `direct transport`：直接传递，意思是控制指令比较直接地推到执行器响应上。
- `history transport`：历史传递，意思是系统不只看当前，还会保留一段过去的记忆。
- `regime`：工况或模式范围，例如不同飞行模式下的工作区间。
- `conditioning`：数值稳定性；数值越差，说明关系虽然存在，但越难稳定利用。
- `leakage`：外溢；本来只想推动目标响应，结果别的响应也被带着一起动。

## 输入 artifact

- PX4 baseline: `artifacts/studies/20260410_224818_px4_real_generalization_ablation`
- PX4 diagnostic: `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`
- ArduPilot baseline: `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation`
- ArduPilot diagnostic: `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix`
- Current Stage 2 study: `artifacts/studies/20260421_090255_stage2_six_line_common_cause_analysis`

## 六线机制账本

| line_code | display_name | transport_family | regime_scope | evidence_tags |
| --- | --- | --- | --- | --- |
| `PX-STC` | PX4 State Transport Continuation | `state_transport` | `POSCTL+OFFBOARD_ATTITUDE` | `support_backed` |
| `PX-STD` | PX4 State Transport Differential | `state_transport` | `POSCTL+OFFBOARD_ATTITUDE` | `support_backed, delta_local` |
| `AP-DAB` | ArduPilot Direct Actuator Bundle | `direct_transport` | `GUIDED_NOGPS+STABILIZE` | `support_backed, low_conditioning` |
| `AP-HTM` | ArduPilot History Transport MixedMode | `history_transport` | `GUIDED_NOGPS+STABILIZE` | `partial_mask, conditioning_limited` |
| `AP-HTS` | ArduPilot History Transport STABILIZE | `history_transport` | `STABILIZE` | `collapse_prone, regime_limited` |
| `AP-HTG` | ArduPilot History Transport GUIDED_NOGPS | `history_transport` | `GUIDED_NOGPS` | `raw_stable, empty_mask` |

## 六线机制怎么理解

- “六线” 不是六根真实的物理线，而是六种在数据里反复出现、能把输入变化传到响应变化上的稳定路径。
- 可以把它理解成六条“常见传递通道”：有的主要靠当前状态往后传，有的主要靠当前指令直接推，有的主要靠过去一段历史慢慢累积。
- 之所以现在写成六条，不是先验规定必须有六条，而是当前 retained evidence 里稳定保留下来的就是这六种解释最强的路径。
- 这六条线最后还能再归并成三大家族：`PX-STC/PX-STD` 属于 `state_transport`，`AP-DAB` 属于 `direct_transport`，`AP-HTM/AP-HTS/AP-HTG` 属于 `history_transport`。
- 所以 Stage 2 真正关心的不是“六选一”，而是确认系统里到底存在哪几类可重复利用的传递结构。

## 六条线的一句话解释

| line_code | 简单理解 |
| --- | --- |
| `PX-STC` | 看“当前状态”会不会沿原来的趋势继续往后传，并持续影响后续响应。 |
| `PX-STD` | 看“当前状态差异”会不会传到目标响应差异上，决定输出往哪个方向分化。 |
| `AP-DAB` | 看控制指令能不能比较直接、比较干净地推着一组执行器一起动。 |
| `AP-HTM` | 看系统在混合模式下，会不会把前一段历史记忆带到当前响应里。 |
| `AP-HTS` | 看 `STABILIZE` 模式下，历史记忆这条路是否还能稳定成立。 |
| `AP-HTG` | 看 `GUIDED_NOGPS` 模式下，历史记忆这条路是否还能稳定成立。 |

## 共同成因

- `PX-STC` 与 `PX-STD` 共同定义 PX4 的 state-transport 家族，只是在 continuation 与 differential target geometry 上分化。
- `AP-DAB` 是最干净的 direct-transport 实例，显示出低条件数、强 row dominance 与 actuator bundle targeting。
- `AP-HTM`、`AP-HTS`、`AP-HTG` 共同定义 history-transport 家族；它们的差异主要来自 mode/regime 与 conditioning，而不是有没有线性结构。

## 当前可直接采纳的进一步判断

- 六条 retained lines 更适合被理解为三类 `transport family` 的不同投影，而不是六条互不相干的 winner line。当前 Stage 2 的主任务是组织 family 账本、边界与设计约束，不是重新做单线排名。
- PX4 的关键增益来自把当前状态并入 `X`。当前 Stage 1 summary 显示，baseline/diagnostic 中 `commands_only -> commands_plus_state` 的 `R²` 增益约为 `0.486 / 0.807`，而 `commands_plus_state -> history` 仅约 `0.0013`；这说明 PX4 更像短时闭环状态传播，而不是长记忆模板。
- PX4 的 state-evolution 路径目前是直接 supported 的。当前 retained audit 中，PX4 baseline/diagnostic 分别有 `75 / 78` 个 supported state-evolution combo，这与 `PX-STC/PX-STD` 的 state-transport 解释一致。
- ArduPilot 当前最干净、最稳的 retained direct line 仍是 `AP-DAB`。Stage 1 的 canonical representative combo 仍是 `commands_only -> actuator_response -> ridge_affine -> pooled`；leave-one-scenario-out 结果也保持 `all_holdouts_supported`，且条件数在 baseline/diagnostic 中约为 `1.51 / 1.04`。
- ArduPilot 的 history/state-evolution 路径不是“没有结构”，而是长期被 `conditioning`、`mask collapse` 与 `regime split` 限制。当前 retained audit 中，ArduPilot baseline/diagnostic 的 supported state-evolution combo 都是 `0` 个；主阻塞项是 `condition_number` 或 `mixed`，不是单纯 `R²` 不够。
- 因此，Stage 2 的实际筛选顺序应是 `support / holdout / overlap / conditioning / regime` 优先，分数其次。

## 通俗解释

- Stage 2 的核心判断不是“哪一条线最值得做”，而是这六条线本质上都在说明同一种可利用结构存在。
- 这六条线都说明：系统响应不是完全杂乱的，而是存在少数关键输入方向，能稳定推动一组相关输出一起变化。
- `PX-STC` 和 `PX-STD` 说明 PX4 里主要是“状态往后传”的结构，也就是当前状态会继续影响后面的状态。
- `AP-DAB` 说明 ArduPilot 里存在一条更直接的通道，控制指令可以比较干净地带动执行器成组响应。
- `AP-HTM`、`AP-HTS`、`AP-HTG` 说明 ArduPilot 里还存在“历史记忆”结构，也就是系统会受到前面一段时间的输入和状态影响。
- 真正限制这些线能不能被稳定利用的，不是线性关系有没有，而是外溢太大、数值太不稳定，或者一换模式规律就变形。

## 数学结构与边界

- 六条线都更像低维方向映射，而不是任意高维拟合。
- 当前 artifact 更稳地支持 bundle-level 目标与 family-level 边界，而不是 entry-wise 系数真值。尤其在 `AP-HT*` 上，更可信的是 response bundle、conditioning 边界与 regime 分裂，而不是固定边权重。
- 真正需要进入 `USDTA` 的对象是 response bundle、kernel selector、leakage penalty 和 conditioning-aware regularization。
- 历史 transport 家族的边界主要体现在 mask 弱、empty-mask、raw-top-edge 迁移和 regime sensitivity。

## 使用边界

- 本文只记录当前 retained artifact 已经直接支持的结论。
- 更强的数学解释，例如 `sufficient statistic`、`temporal kernel`、`matrix equivalence class` 或 “稳定对象是子空间而不是系数”，适合进入扩展分析文档作为研究假说，不应在当前 summary 中写成既成事实。

## USDTA 设计启示

- 自本次归档起，本节默认对应后续已经实现并完成 Stage 4 official 评估的 `USDTA v1` 设计启示；`USDTA v2` 不回写到这里。
- 目标必须写成 `Y` 子空间中的 bundle direction。
- 算法必须统一支持 `state_transport`、`direct_transport`、`history_transport` 三类 kernel。
- leakage suppression 和 conditioning regularization 必须是内生项，不是事后解释。

## 推荐阅读

1. `README.md`
2. `docs/v1/STAGE1_SUMMARY_v1.md`
3. 本文
4. `docs/v1/STAGE2_DEEP_ANALYSIS_v1.md`
5. `artifacts/studies/20260421_090255_stage2_six_line_common_cause_analysis/reports/stage2_six_line_common_cause.md`
