# AGENTLOG.md

## 目标

围绕 `Y ≈ fX (+ b)` 构建一个可持续推进的 UAV 全局线性研究平台。默认主线固定为：

- 构造候选 `X`
- 构造候选 `Y`
- 拟合全局线性/仿射矩阵 `f`
- 估计稀疏性
- 比较不同 `X/Y schema`

## 2026-04-06

- 建立 `linearity_core / linearity_study / linearity_analysis` 三层结构
- 统一 study config、sample table、fit artifact、study summary 的输出口径
- 新增 `linearity_run_study / linearity_analyze / linearity_compare_schemas`
- 新增 `scripts/run_linearity_study.sh`、`scripts/compare_schemas.sh`、`scripts/smoke_linearity.sh`
- 建立 synthetic backendless smoke 与基础测试集

## 2026-04-07

### 真实 PX4 主报告链路

- 固定真实 PX4 scope：`gz_x500/default + nominal + POSCTL/OFFBOARD_ATTITUDE`
- 新增真实 capture config、analysis config 与 balanced broad ablation plan
- `scripts/run_px4_broad_ablation.sh` 成为当前真实 PX4 主入口
- 当前权威 raw run：
  - `artifacts/raw/px4/20260407_025915_px4_manual_broad_composite_r1`
  - `artifacts/raw/px4/20260407_030010_px4_attitude_broad_composite_r1`
- 当前权威 study：
  - `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced`

### PX4 telemetry 与 conditioning

- PX4 raw capture 现支持 `ROS 直录 + ULog 缺口回填`
- 已补齐 rate / actuator / internal telemetry 的分析输入链路
- 条件数诊断现拆分为：
  - `raw_condition_number`
  - `effective_condition_number`
- `selected_state_subset` 已按 `output_semantics` 解释，不再混淆当前态与未来响应

### 当前结果

- best schema: `commands_plus_state_history x next_raw_state | ols_affine | pooled`
- best sparse/stable schema: `commands_plus_state_history x next_raw_state | ridge_affine | pooled`
- `median_test_r2 ≈ 0.9726`
- `commands_only -> commands_plus_state` 提升 `≈ 1.0442`
- `commands_plus_state -> history` 提升 `≈ 0.0064`
- `actuator_response` 已进入有效比较
- `raw_condition_number = inf`
- `effective_condition_number ≈ 1259416.2092`

### 当前文档入口

- `README.md`
- `PJINFO.md`
- `docs/STAGE_REPORT_2026-04-07.md`
