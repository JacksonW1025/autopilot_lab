# A2 Pair-Target Live Protocol V1

## 目的

这份文档把当前 A2 live evidence 的正式执行口径写死。它回答的是：

- 当前 live target 是什么
- canonical probe 参数是什么
- live success 继续沿用什么门槛
- campaign 什么时候必须停

它不负责：

- adaptive optimizer
- multi-strategy family
- decision-layer 自动接入
- A1 对称 live campaign

## Canonical Target

当前 live protocol 固定为：

- `flight_mode=GUIDED_NOGPS`
- `target_signal=pair_imbalance_12_vs_34`
- `dominant_direction=12_gt_34`

这是从当前 canonical narrowing chain 固定下来的正式口径，不在这轮放宽。

## Canonical Probe 参数

当前 canonical probe 配置固定为：

- `pulse_amplitude=0.05`
- `bias.nominal=0.00`
- `bias.throttle_biased=0.04`
- `pulse_count=5`
- `pulse_width_s=0.35`
- `pulse_gap_s=0.95`

这个 probe 配置是当前 medium robustness campaign 的稳定性锚点。

## Live Success 门槛

当前 live success 继续复用 pair-target readiness 的六个正式门槛：

- `active_pair_rate >= 0.15`
- `baseline_pair_rate <= 0.05`
- `specificity >= 0.12`
- `sign_consistency >= 0.90`
- `pair_to_collective_ratio >= 0.70`
- `tier_range_specificity <= 0.08`

同时必须满足：

- 两个 scenario 都通过
- `dominant_direction == 12_gt_34`

## Stop Rules

当前 campaign stop rules 固定为：

- 任一 phase 出现 `direction != 12_gt_34`，整轮 campaign 立即停止
- 任一 `probe_stability` phase 出现 hard regression，整轮 campaign 立即停止
- `micro_robustness` 失败只记录，不提前中断 `confirm_robustness`
- `confirm_robustness` 出现 hard regression，campaign 直接失败

## Runtime 约束

- campaign 级 smoke 只在入口跑一次
- phase 内部的 `live_evaluation` 一律 `skip_smoke=true`
- 当前默认 runtime 仍然是 `headless`
- 可视化必须显式传 `--enable-visualization`

## 与评估层的关系

当前 live stack 的正式顺序是：

1. `a2_target_scout`
2. `a2_pair_target_readiness`
3. `a2_pair_target_algorithm_evaluation`
4. `a2_pair_target_live_evaluation`
5. `a2_pair_target_live_campaign`

其中：

- `algorithm_evaluation` 是 offline gate
- `live_evaluation` 是单 phase live gate
- `live_campaign` 是 medium robustness 的聚合证据层

当前三层都不会自动进入 `next_phase_decision_layer`。
