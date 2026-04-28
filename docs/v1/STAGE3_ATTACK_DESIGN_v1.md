# Stage 3 USDTA v1 Attack Design

## 定位

- 本文记录 Stage 3 的正式设计层，不是 Stage 4 评估结论。
- 自本次归档起，本文固定对应已经实现并完成 Stage 4 official 评估的 `USDTA v1`；`USDTA v2` 另见 [USDTA_V2_CHECKLIST.md](../v2/USDTA_V2_CHECKLIST.md)。
- Stage 3 的任务是把 Stage 2 的 six-line / three-family 证据编译成一个统一、可解释、预算受限、可直接进入后续评估器的 `USDTA` 攻击算法规范。
- 本文直接建立在以下输入上：
  - `docs/v1/STAGE2_SUMMARY_v1.md`
  - `docs/v1/STAGE2_DEEP_ANALYSIS_v1.md`
  - `docs/v1/STAGE2_MATHEVIDENCE_v1.md`
  - `docs/v1/STAGE3_REFERENCE_v1.md`
  - `artifacts/studies/20260421_090255_stage2_six_line_common_cause_analysis/summary/stage2_six_line_common_cause.json`

## 证据链

- `docs/v1/STAGE2_SUMMARY_v1.md` 已经给出三条硬约束：目标写成 `Y` bundle direction、算法统一支持 `state_transport/direct_transport/history_transport`、以及 leakage/conditioning 需要内生进入算法。
- `docs/v1/STAGE2_DEEP_ANALYSIS_v1.md` 明确要求后续实现遵守 `family first / bundle first / regime-gated / history must be compressed`。
- `docs/v1/STAGE2_MATHEVIDENCE_v1.md` 提供了六线共用的数学骨架：`Y ≈ XW + b`、target bundle compactness、off-target leakage、effective condition number、transport kernel share。
- `docs/v1/STAGE3_REFERENCE_v1.md` 进一步把 Stage 3 收束为 low-dimensional family coordinate search，而不是 raw-space random attack。
- 因此，本设计不再把六条线写成六套互不相干的 winner-specific 算法，而是写成三类 family + 六条 instantiation 的统一 `USDTA`。

## 六线到三 Family 的映射

- `PX-STC`、`PX-STD` 归入 `state_transport`。
- `AP-DAB` 归入 `direct_transport`。
- `AP-HTM`、`AP-HTS`、`AP-HTG` 归入 `history_transport`。
- 这不是重新排名，而是把 Stage 2 的 family registry 直接提升为 Stage 3 的 attack registry。

## Runtime 公式

统一 runtime contract 写成：

```text
δu_t = Π_budget(A_line ψ_family(z, q_t))
```

其中：

- `δu_t` 是 4 通道 command delta，顺序固定为 `command_roll / command_pitch / command_yaw / command_throttle`。
- `Π_budget` 是 command-space budget projector，负责幅值上限、slew 上限、总能量上限和 active horizon。
- `A_line` 是 line-specific command mixing matrix，由 family template、target bundle geometry、dominant feature/response axis 和 line variant 编译得到。
- `ψ_family(z, q_t)` 是 family-aware latent generator；`z` 是低维 latent，`q_t` 是当前 context。

## 为什么 state/history 只能是 Context，不是直接 Actuation

- Stage 2 的 `X` 包含 `state_current` 和 `history`，但这只是解释系统传播结构，不代表这些量在运行时可以直接被操控。
- 真实可注入系统的对象仍然是 command 通道，因此 Stage 3 强制把 runtime 输出限制为 4 通道 `δu_t`。
- `state_transport` 与 `history_transport` 的 state/history 项只进入 `q_t = H_t` 上下文，用于调制攻击方向和强度。
- 这正是 Stage 2 的证据边界：稳定对象更像 family-level direction / bundle / temporal basis，而不是“可以直接优化的任意 raw feature”。

## Latent Schema

- 公共 latent 字段固定为：
  - `axis_weights[4]`
  - `bundle_weights`
  - `gain`
  - `feedback_gain`
  - `temporal_weights[4]`
  - `leakage_weight`
  - `conditioning_weight`
  - `recovery_weight`
  - `active_horizon_fraction`
- 这些字段在所有 family 上都存在，从而保证 Stage 4 可以直接在统一 latent space 上接 baseline 和 optimizer。

## Family 设计

### `state_transport`

- context basis 固定为 `current_state / state_delta / lag_mean / lag_energy`。
- 设计理由是 PX4 在 retained evidence 里一旦把当前状态并入 `X`，解释力几乎饱和；history 的额外收益很小，因此这里只保留短时 lag summary，而不是长记忆模板。
- `PX-STC` 与 `PX-STD` 共用同一个 family registry，但 target geometry 不同：
  - `PX-STC`: `future_state_bundle_direction`
  - `PX-STD`: `delta_state_bundle_direction`
- `PX-STD` 比 `PX-STC` 使用更短的 active horizon 和更快的 slew，以反映 differential / local target geometry。

### `direct_transport`

- `AP-DAB` 是 canonical direct line，因为 command share 近似为 1，conditioning 极低，row dominance 极强。
- direct family 的核心不是状态传播，而是 row-dominant command basis，因此 line matrix 被编译成 throttle-first actuation，并配套更强的 leakage penalty。
- 这条线在设计里承担 command-space direct baseline representative 的角色。

### `history_transport`

- history family 不暴露 raw lag coefficient，只暴露 `mean / slope / curvature / energy` 的 temporal basis。
- 窗口固定为 `current + lag1 + lag2 + lag3`，对应 Stage 2 retained config 的 `history_length = 3`。
- `AP-HTM` 保留 mixed-mode，但默认高 conditioning penalty。
- `AP-HTS` 只允许 `STABILIZE`，并使用最保守 budget。
- `AP-HTG` 只允许 `GUIDED_NOGPS`，保留 memory-preserving design，但仍把 empty-mask / conditioning 风险写进 penalty 和 gate。

## Objective 分解

- 正项固定为：`bundle_gain`、`tracking_deviation`、`attitude_deviation`、`boundary_stress`、`recovery_cost`。
- 罚项固定为：`off_target_leakage`、`conditioning`、`budget`。
- 这些项全部进入 machine-readable objective contract，而不是留在文字说明里。
- 设计选择的含义是：Stage 3 优先构建一个可比较、可复验、可解释的 worst-case evaluator-ready attack objective，而不是一次性的“搞崩”展示。

## Regime 与 Budget 规则

- 所有 line 的 budget 都固定在 normalized command space：每通道 amplitude、每通道 slew、总能量、active horizon。
- `AP-HTS`：仅 `STABILIZE`。
- `AP-HTG`：仅 `GUIDED_NOGPS`。
- `AP-HTM`：`STABILIZE + GUIDED_NOGPS`，但 conditioning penalty 保持最高梯队。
- `PX-STC/PX-STD`：共享 PX4 state family registry，允许 `POSCTL + OFFBOARD_ATTITUDE`。

## 各 Family 的设计预期

- `state_transport` 预期更适合形成可解释的、短时闭环放大型 command pattern；它的收益应更多来自 family structure，而不是长 history。
- `direct_transport` 预期会给出最干净的 unit-budget direct stress pattern，但 leakage penalty 仍必须保持显式，否则 direct line 很容易退化成无约束 command pushing。
- `history_transport` 预期能表达 regime-specific memory-sensitive direction，但更容易被 conditioning、mask collapse 和 mode split 限制，因此必须先以 compressed temporal basis 的形式进入 Stage 4。
- 这些都是 Stage 3 设计预期，不是 Stage 4 已证结论。

## Baseline Registry

- `bounded_noise`
- `raw_space_random`
- `low_dim_agnostic`
- `family_aware_usdta_v1`

## 产物

- Stage 3 study artifact: `artifacts/studies/20260421_115334_stage3_attack_design`
- Machine-readable summary: `summary/stage3_attack_design.json`
- Tables: `family_registry.csv`, `line_attack_specs.csv`, `attack_coordinate_catalog.csv`, `objective_contract.csv`, `regime_budget_contract.csv`
- Runtime API: `linearity_core.attack_runtime.Stage3AttackGenerator`

## 最后说明

- `USDTA` 在这一轮被正式落成 design layer：family-aware、regime-aware、conditioning-aware、budgeted command-space attack generator。
- 这一层的职责到此为止：整理设计、固定接口、冻结 contract；Stage 4 再负责 baseline 对比、评估和结果归纳。
