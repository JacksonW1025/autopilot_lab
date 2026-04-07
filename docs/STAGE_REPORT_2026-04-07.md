# Stage Report — 2026-04-07

## Summary

当前平台已经进入第一份真实 PX4 broad ablation 完整交付期。默认 scope 固定为：

- backend: `px4`
- airframe: `gz_x500`
- world: `default`
- scenario: `nominal`
- modes: `POSCTL` 与 `OFFBOARD_ATTITUDE`

当前主线仍是：

- 数据采集
- X/Y 构造
- 全局拟合
- 稀疏性分析
- 结论

## Authoritative Artifacts

当前权威 raw run：

- `artifacts/raw/px4/20260407_025915_px4_manual_broad_composite_r1`
- `artifacts/raw/px4/20260407_030010_px4_attitude_broad_composite_r1`

当前权威 study：

- `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced`

权威报告与汇总：

- `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/reports/summary.md`
- `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/reports/schema_comparison.md`
- `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/summary/study_summary.json`

## Current Experimental Status

- 真实 PX4 raw capture -> prepared sample table -> broad ablation -> report 的闭环已经打通。
- PX4 默认数据链路采用 `ROS 直录 + ULog 缺口回填`。
- `actuator_response` 已进入真实比较矩阵。
- conditioning 采用双口径：
  - `raw_condition_number` 保留原始共线性事实
  - `effective_condition_number` 用于诊断和支持度判定

## Key Results

当前最优主组合：

- best schema: `commands_plus_state_history x next_raw_state | ols_affine | pooled`
- best sparse/stable schema: `commands_plus_state_history x next_raw_state | ridge_affine | pooled`
- best Y definition: `next_raw_state`

关键指标：

- `median_test_r2 = 0.9726`
- `median_test_mse = 0.000046`
- `median_test_mae = 0.003960`
- `sparsity_ratio = 0.7158`
- `coefficient_stability = 1.0000`
- `support = partial`

schema 增益：

- `commands_only -> commands_plus_state` 的 `R²` 提升 `≈ 1.0442`
- `commands_plus_state -> history` 的 `R²` 提升 `≈ 0.0064`

conditioning 摘要：

- `raw_condition_number = inf`
- `effective_condition_number ≈ 1259416.2092`
- 当前 conditioning 剪枝主要来自：
  - `altitude` 及其 history 列
  - `vertical_speed` 及其 history 列
  - 若干额外 history alias

data quality 摘要：

- `alignment_failure_ratio = 0.0000`
- `missing_attitude_ratio = 0.0000`
- `missing_local_position_ratio = 0.0000`
- `missing_actuator_ratio = 0.0000`
- `future_horizon_available_ratio = 0.9934`
- `window_summary_available_ratio = 0.9934`
- `median_alignment_attitude_ms = 2.4425`
- `median_alignment_position_ms = 2.5220`

fresh raw run 验收摘要：

- 两条 raw run 都满足 `missing_topics == []`
- `telemetry_backfill.topics.actuator_motors.source = ulog_backfill`
- `actuator_response_ratio_estimate = 1.0`

## Known Limitations

- `raw_condition_number` 仍为 `inf`，说明 raw feature matrix 仍存在精确共线性。
- `effective_condition_number` 仍偏高，当前阶段把它视作诊断信号，不视作阻断项。
- 当前真实主报告只覆盖 PX4，尚未进入 ArduPilot 对照。
- 当前只完成 pooled 主报告，尚未补一份同口径 stratified 对照附页。

## Next TODO

- 做一轮 PX4-only stratified vs pooled 对照报告。
- 继续压实高共线性解释、alias 诊断和 conditioning 展示。
- 把同一套 broad ablation 扩到 ArduPilot，对比 backend 异质性。
- 视需要把 `window_summary_response` 恢复到实盘报告矩阵。

## Repro Commands

环境体检：

```bash
/home/car/autopilot_lab/scripts/doctor_lab.sh
```

当前口径应返回：

- `status=ready`
- `px4_real_ready=true`

测试回归：

```bash
python3 -m pytest -q tests
```

当前口径应为：

- `23 passed`

重跑当前 balanced PX4 broad ablation：

```bash
/home/car/autopilot_lab/scripts/run_px4_broad_ablation.sh \
  --plan /home/car/autopilot_lab/configs/ablations/px4_real_broad_ablation_balanced.yaml
```
