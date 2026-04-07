# PJINFO.md

> 每次 Agent work 前先读本文件；完成后只更新“当前状态”和“最近变更”。

## 项目背景

- 核心目标：建立一个面向 UAV 输入-响应全局线性关系验证的研究平台
- 默认主线：`数据采集 -> X/Y 构造 -> 全局拟合 -> 稀疏性分析 -> 结论`
- 研究问题：在某个 study scope 下，是否存在固定的 `Y ≈ fX (+ b)`，以及 `f` 是否稀疏
- 当前重点：大胆探索 `X` 与 `Y` 的定义，并比较哪组 schema 最支持全局线性假设
- PX4 真实链路默认采用 `ROS 直录 + ULog 缺口回填`

## 环境基线

- 计算平台：Jetson AGX Orin 64G
- 操作系统：Ubuntu 22.04 aarch64
- ROS：Humble
- Gazebo：Harmonic
- 主仓库：`/home/car/autopilot_lab -> /mnt/nvme/autopilot_lab`
- PX4 固件：`/home/car/PX4-Autopilot`
- ArduPilot 固件：`/home/car/ardupilot`

## 目录与接口

- 共享层：`src/linearity_core`
- 分析层：`src/linearity_analysis`
- 编排层：`src/linearity_study`
- PX4 backend：`src/px4_ros2_backend`
- ArduPilot backend：`src/ardupilot_mavlink_backend`
- Raw run：`artifacts/raw/`
- Study 输出：`artifacts/studies/`
- 阶段报告：`docs/STAGE_REPORT_2026-04-07.md`

## 当前默认配置

- `configs/studies/global_linear_commands_only__next_raw_state.yaml`
- `configs/studies/global_linear_commands_plus_state__delta_state.yaml`
- `configs/studies/global_linear_pooled_backend_augmented__selected_state_subset.yaml`
- `configs/studies/global_linear_with_pid_sweep__delta_state.yaml`
- `configs/studies/global_linear_history_augmented__future_state_horizon.yaml`
- `configs/studies/global_linear_full_augmented__window_summary_response.yaml`
- `configs/ablations/default_schema_ablation.yaml`
- 真实 PX4：
  - `configs/studies/px4_real_nominal_posctl_capture.yaml`
  - `configs/studies/px4_real_nominal_offboard_attitude_capture.yaml`
  - `configs/studies/px4_real_nominal_broad_ablation_analysis.yaml`
  - `configs/ablations/px4_real_broad_ablation_balanced.yaml`

## 当前状态

- [2026-04-06] `linearity_core / linearity_study / linearity_analysis` 已形成当前平台默认前门
- [2026-04-06] study config 已支持 `x_schema / y_schema / pooling_mode / history_length / prediction_horizon / ablation_plan`
- [2026-04-06] 分析产物已统一为 `f / b / sparsity_mask / metrics / markdown report / summary json`
- [2026-04-07] PX4 raw capture 已支持 ULog 缺口回填，可补齐 rate / actuator / internal telemetry
- [2026-04-07] 条件数诊断已拆分为 `raw_condition_number` 与 `effective_condition_number`
- [2026-04-07] 当前权威 study 为 `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced`
- [2026-04-07] 当前权威 raw run 为：
  - `artifacts/raw/px4/20260407_025915_px4_manual_broad_composite_r1`
  - `artifacts/raw/px4/20260407_030010_px4_attitude_broad_composite_r1`
- [2026-04-07] 当前真实 PX4 最优主组合为 `commands_plus_state_history x next_raw_state | ols_affine | pooled`
- [2026-04-07] 当前结果摘要：
  - `median_test_r2 ≈ 0.9726`
  - `commands_only -> commands_plus_state` 提升 `≈ 1.0442`
  - `commands_plus_state -> history` 提升 `≈ 0.0064`
  - `actuator_response` 已进入有效比较
- [2026-04-07] 当前 `doctor_lab.sh` 口径为 `status=ready` 与 `px4_real_ready=true`
- [2026-04-07] 当前测试口径为 `python3 -m pytest -q tests -> 23 passed`

## 最近变更

- 新增 `src/linearity_core`
- 新增 `src/linearity_study`
- 新增 `src/linearity_analysis`
- 新增 `docs/RESEARCH_GOAL.md`
- 新增 `docs/XY_SCHEMA_GUIDE.md`
- 新增 `docs/EXPERIMENT_PROTOCOL.md`
- 新增 `docs/DATA_SCHEMA.md`
- 新增 `docs/STAGE_REPORT_2026-04-07.md`
- 新增 `scripts/run_linearity_study.sh`
- 新增 `scripts/compare_schemas.sh`
- 新增 `scripts/smoke_linearity.sh`
- 新增 `scripts/run_px4_broad_ablation.sh`
- 新增 PX4 ULog telemetry backfill
- 新增 raw/effective conditioning diagnostics

## 常用命令

先加载环境：

```bash
source /home/car/autopilot_lab/scripts/autopilot_lab_env.sh
```

环境体检：

```bash
/home/car/autopilot_lab/scripts/doctor_lab.sh
```

统一 smoke：

```bash
/home/car/autopilot_lab/scripts/smoke_linearity.sh
```

最小 CI：

```bash
/home/car/autopilot_lab/scripts/ci_minimal.sh
```

单次 study：

```bash
ros2 run linearity_study linearity_run_study \
  --config /home/car/autopilot_lab/configs/studies/global_linear_commands_plus_state__delta_state.yaml
```

统一分析：

```bash
ros2 run linearity_analysis linearity_analyze \
  --config /home/car/autopilot_lab/configs/studies/global_linear_commands_plus_state__delta_state.yaml \
  --study-dir /home/car/autopilot_lab/artifacts/raw/synthetic
```

真实 PX4 broad ablation：

```bash
/home/car/autopilot_lab/scripts/run_px4_broad_ablation.sh \
  --plan /home/car/autopilot_lab/configs/ablations/px4_real_broad_ablation_balanced.yaml
```

## 注意事项

- 所有文档和交互统一使用简体中文
- 如需系统级操作，可以使用 `sudo`
- 当前阶段日常建议入口是 balanced PX4 broad ablation
- `effective_condition_number` 当前仍偏大，现阶段视作诊断信号，不视作阻断项
