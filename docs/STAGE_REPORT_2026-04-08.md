# Stage Report — 2026-04-08

## Summary

当前 PX4 已经完成一份 accepted-only authoritative baseline 重建，并且可以作为第一阶段正式结论的唯一口径。

默认 authoritative scope 固定为：

- backend: `px4`
- airframe: `gz_x500`
- world: `default`
- scenario: `nominal`
- modes: `POSCTL` 与 `OFFBOARD_ATTITUDE`

当前正式判断是：

- PX4 研究链路已经稳定到 accepted-only baseline 口径
- 在当前 scope 下，`next_raw_state` 仍然是最强的主 Y 定义
- 全局固定仿射模型可以给出很强近似，但最佳 pooled 组合仍带有明显 conditioning 压力
- `pooled` 与 `stratified` 都支持“强线性可近似，但不应把它解释为完美、全局、稳定、物理可解释的线性真相”

## Authoritative Artifacts

当前 accepted-only authoritative raw runs：

- `artifacts/raw/px4/20260408_054443_px4_manual_broad_composite_r1`
- `artifacts/raw/px4/20260408_054826_px4_manual_broad_composite_r3`
- `artifacts/raw/px4/20260408_060432_px4_manual_broad_composite_r1`
- `artifacts/raw/px4/20260408_054531_px4_attitude_broad_composite_r1`
- `artifacts/raw/px4/20260408_054736_px4_attitude_broad_composite_r2`
- `artifacts/raw/px4/20260408_054917_px4_attitude_broad_composite_r3`

当前 authoritative study：

- `artifacts/studies/20260408_062436_px4_real_broad_ablation`

当前 authoritative 报告与汇总：

- `artifacts/studies/20260408_062436_px4_real_broad_ablation/prepared/schema_inventory.yaml`
- `artifacts/studies/20260408_062436_px4_real_broad_ablation/reports/summary.md`
- `artifacts/studies/20260408_062436_px4_real_broad_ablation/reports/schema_comparison.md`
- `artifacts/studies/20260408_062436_px4_real_broad_ablation/summary/study_summary.json`

当前 diagnostic study：

- `artifacts/studies/20260408_074744_px4_diagnostic_axis_matrix_balanced`

当前 diagnostic gate 摘要来源：

- `artifacts/studies/20260408_074744_px4_diagnostic_axis_matrix_balanced/prepared/schema_inventory.yaml`

## Legacy Artifacts

以下 artifacts 不再属于 authoritative baseline：

- `artifacts/raw/px4/20260407_025915_px4_manual_broad_composite_r1`
- `artifacts/raw/px4/20260407_030010_px4_attitude_broad_composite_r1`
- `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced`
- `artifacts/studies/20260408_054955_px4_real_broad_ablation`
- `artifacts/studies/20260408_060524_px4_real_broad_ablation`

其中：

- `20260407_*` 与 `20260407_031229_*` 属于 pre-acceptance-gate 时代的旧口径
- `20260408_054955_*` 是初次 3-repeat authoritative matrix 失败后的不完整 study
- `20260408_060524_*` 是断电前中断的 accepted-only study，不再作为正式依据

## Baseline Recovery

这轮 accepted-only baseline 不是“一次跑成”，而是经过了显式恢复：

- 初次 authoritative matrix：`artifacts/px4_matrix/20260408_054432_default`
- 原计划 `POSCTL x 3` 与 `OFFBOARD_ATTITUDE x 3`
- 实际出现一条 `POSCTL` matrix-layer 失败：`topics_not_ready`
- 随后的两次 POSCTL 补采 raw run 都被 research gate 拒收：
  - `20260408_060217_px4_manual_broad_composite_r1`
  - `20260408_060323_px4_manual_broad_composite_r1`
- 这两条拒收原因一致：
  - `active_phase_missing`
  - `experiment_not_started`
  - `insufficient_active_nonzero_command_samples`
- 第三次 POSCTL 补采成功并 accepted：
  - `20260408_060432_px4_manual_broad_composite_r1`

因此，当前 authoritative baseline 应理解为：

- `POSCTL`: 3 accepted
- `OFFBOARD_ATTITUDE`: 3 accepted
- accepted-only 重分析后进入正式 study

## Accepted-Only Gate Status

`artifacts/studies/20260408_062436_px4_real_broad_ablation/prepared/schema_inventory.yaml` 当前明确给出：

- `run_count = 6`
- `accepted_run_count = 6`
- `rejected_run_count = 0`
- `excluded_runs = []`
- `row_count = 2194`

data quality 摘要：

- `alignment_failure_ratio = 0.0000`
- `missing_attitude_ratio = 0.0000`
- `missing_local_position_ratio = 0.0000`
- `missing_actuator_ratio = 0.0000`
- `future_horizon_available_ratio = 0.9945`
- `window_summary_available_ratio = 0.9945`
- `actuator_response_available_ratio = 1.0000`
- `median_alignment_attitude_ms = 2.4713`
- `median_alignment_position_ms = 2.6158`

## Authoritative Results

study 自动汇总给出的主结论是：

- best linear schema: `full_augmented x next_raw_state | ols_affine | pooled`
- best sparse and stable schema: `commands_plus_state_history x delta_state | ridge_affine | stratified`
- best Y definition: `next_raw_state`
- `commands_only -> commands_plus_state` 的 `R²` 提升：`0.6107`
- `commands_plus_state -> history` 的 `R²` 提升：`0.0028`

当前 best overall 组合：

- combo: `full_augmented x next_raw_state | ols_affine | pooled`
- support: `partial`
- `median_test_r2 = 0.9996`
- `median_test_mse = 0.000085`
- `median_test_mae = 0.004353`
- `sparsity_ratio = 0.6867`
- `coefficient_stability = 0.7844`
- `effective_condition_number = 1039336.3683`

更适合作为“高性能且仍被 summary 判为 supported”的 pooled anchor：

- combo: `commands_plus_state_history x next_raw_state | ols_affine | pooled`
- support: `supported`
- `median_test_r2 = 0.9994`
- `median_test_mse = 0.000133`
- `median_test_mae = 0.004308`
- `effective_condition_number = 996260.5635`

conditioning 摘要：

- `raw_condition_number = inf`
- `effective_condition_number ≈ 1.039e6` for best overall pooled combo
- 主要被剪枝的 conditioning 特征包括：
  - `altitude` 及其 history
  - `vertical_speed` 及其 history
  - `mode/config_profile` one-hot alias

## Pooled vs Stratified

accepted-only authoritative study 同时给出了 `pooled` 与 `stratified` 结果。

按当前 study 的排序口径，最优 pooled 组合是：

- `full_augmented x next_raw_state | ols_affine | pooled`
- support: `partial`
- `median_test_r2 = 0.9996`
- `effective_condition_number = 1039336.3683`

按同一排序口径，当前最优 stratified 组合是：

- `commands_plus_state_history x next_raw_state | ols_affine | stratified`
- support: `partial`
- `median_test_r2 = 0.9984`
- `effective_condition_number = 913354.2145`

如果只看 `supported` 组合，则更稳的两条 anchor 是：

- pooled supported anchor:
  - `commands_plus_state_history x next_raw_state | ols_affine | pooled`
  - `median_test_r2 = 0.9994`
  - `effective_condition_number = 996260.5635`
- stratified supported anchor:
  - `full_augmented x next_raw_state | ols_affine | stratified`
  - `median_test_r2 = 0.9977`
  - `effective_condition_number = 964549.0012`

因此当前更严谨的 pooled vs stratified 口径是：

- `pooled` 仍给出最高绝对 `R²`
- 但最优 pooled 组合仍然只到 `partial`，且 conditioning 压力更高
- `stratified` 没有把线性近似推翻，反而继续支持 `next_raw_state` 主结论
- 只是它把“最高 R²”与“更稳 supported”两类组合进一步分开了

## Diagnostic Matrix

这轮 PX4-only diagnostic matrix 只使用预期的 24 条诊断 raw run，显式排除了意外混入 `runs.csv` 的非诊断 synthetic rows。

accepted-only diagnostic study 当前已经固定出：

- `run_count = 18`
- `accepted_run_count = 18`
- `rejected_run_count = 0`
- `research_tiers = [diagnostic_research]`

被 accepted-only analysis 排除的 6 条 rejected diagnostic runs 全部都是 throttle：

- `POSCTL throttle small`
- `POSCTL throttle medium`
- `POSCTL throttle large`
- `OFFBOARD_ATTITUDE throttle small`
- `OFFBOARD_ATTITUDE throttle medium`
- `OFFBOARD_ATTITUDE throttle large`

这 6 条的拒收原因完全一致：

- `insufficient_active_nonzero_command_samples`

当前 diagnostic gate 呈现出的结论非常清楚：

- `roll / pitch / yaw` 在两个 mode 下、三档 amplitude 下全部 accepted
- `throttle` 是最先系统性破坏 raw-run acceptance 的通道
- 因此 PX4-only 诊断集已经能够把“最先破坏全局线性前提的控制轴”单独分离出来

这里的 diagnostic 结论是非 authoritative 的：

- 它用于解释和定位线性假设的失效边界
- 不进入 authoritative 主结论排序

## Current Status

到 2026-04-08 这一轮为止，PX4 的更准确状态应理解为：

- accepted-only authoritative baseline 已重建完成
- 第一阶段主结论已经可以完全切换到新 baseline 口径
- `pooled vs stratified` 已有正式依据
- PX4-only diagnostic acceptance 模式已经明确
- 旧 raw/study artifacts 已经可以正式降级为 `legacy`

但这仍不等于“PX4 已经是最终无争议基线”。

当前最准确的说法是：

- 研究链路已稳
- 主结论已稳
- accepted-only gate 已稳
- 诊断集已经显示 throttle 通道需要单独对待
- 后续引入 ArduPilot 时，应直接沿用这套 accepted-only contract 与同一实验矩阵

## Repro Commands

测试回归：

```bash
python3 -m pytest -q tests
```

accepted-only authoritative baseline：

```bash
/home/car/autopilot_lab/scripts/run_px4_authoritative_baseline.sh
```

PX4-only diagnostic matrix：

```bash
/home/car/autopilot_lab/scripts/run_px4_diagnostic_matrix.sh
```
