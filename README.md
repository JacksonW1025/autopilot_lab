# autopilot_lab

`autopilot_lab` 是一个面向 UAV 输入-响应全局线性关系验证的研究平台。默认问题是：

> 在给定 study scope 下，是否存在固定的全局线性或仿射映射 `Y ≈ fX (+ b)`，并且 `f` 是否稀疏？

平台主线固定为：

- 数据采集
- X/Y 构造
- 全局拟合
- 稀疏性分析
- 结论与 schema 对比

## 当前状态

当前权威实验固定为：

- raw run: `artifacts/raw/px4/20260407_025915_px4_manual_broad_composite_r1`
- raw run: `artifacts/raw/px4/20260407_030010_px4_attitude_broad_composite_r1`
- study: `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced`

当前结果摘要：

- best schema: `commands_plus_state_history x next_raw_state | ols_affine | pooled`
- best sparse/stable schema: `commands_plus_state_history x next_raw_state | ridge_affine | pooled`
- `median_test_r2 ≈ 0.9726`
- `commands_only -> commands_plus_state` 提升 `≈ 1.0442`
- `commands_plus_state -> history` 提升 `≈ 0.0064`
- `actuator_response` 已进入有效比较
- `raw_condition_number = inf`
- `effective_condition_number ≈ 1259416.2092`

详细状态见 [`docs/STAGE_REPORT_2026-04-07.md`](docs/STAGE_REPORT_2026-04-07.md)。

## 仓库结构

```text
autopilot_lab/
├── artifacts/
│   ├── raw/
│   └── studies/
├── configs/
│   ├── ablations/
│   └── studies/
├── docs/
├── scripts/
├── lab.lock.json
└── src/
    ├── linearity_core/
    ├── linearity_analysis/
    ├── linearity_study/
    ├── px4_ros2_backend/
    ├── ardupilot_mavlink_backend/
    ├── px4_msgs/
    └── px4_ros_com/
```

## Quick Start

加载环境：

```bash
source /home/car/autopilot_lab/scripts/autopilot_lab_env.sh
```

环境准备：

```bash
/home/car/autopilot_lab/scripts/bootstrap_lab.sh
```

环境体检：

```bash
/home/car/autopilot_lab/scripts/doctor_lab.sh
```

默认 smoke：

```bash
/home/car/autopilot_lab/scripts/smoke_linearity.sh
```

默认真实 PX4 broad ablation：

```bash
/home/car/autopilot_lab/scripts/run_px4_broad_ablation.sh \
  --plan /home/car/autopilot_lab/configs/ablations/px4_real_broad_ablation_balanced.yaml
```

## 默认入口

主实验入口：

```bash
ros2 run linearity_study linearity_run_study \
  --config /home/car/autopilot_lab/configs/studies/global_linear_commands_plus_state__delta_state.yaml
```

统一分析入口：

```bash
ros2 run linearity_analysis linearity_analyze \
  --config /home/car/autopilot_lab/configs/studies/global_linear_commands_plus_state__delta_state.yaml \
  --study-dir /home/car/autopilot_lab/artifacts/raw/synthetic
```

Schema 对比入口：

```bash
ros2 run linearity_analysis linearity_compare_schemas \
  --config /home/car/autopilot_lab/configs/studies/global_linear_commands_plus_state__delta_state.yaml \
  --plan /home/car/autopilot_lab/configs/ablations/default_schema_ablation.yaml \
  --study-dir /home/car/autopilot_lab/artifacts/raw/synthetic
```

Shell 包装：

```bash
/home/car/autopilot_lab/scripts/run_linearity_study.sh \
  --config /home/car/autopilot_lab/configs/studies/global_linear_commands_plus_state__delta_state.yaml

/home/car/autopilot_lab/scripts/compare_schemas.sh \
  --config /home/car/autopilot_lab/configs/studies/global_linear_commands_plus_state__delta_state.yaml \
  --plan /home/car/autopilot_lab/configs/ablations/default_schema_ablation.yaml \
  --study-dir /home/car/autopilot_lab/artifacts/raw/synthetic
```

## 真实 PX4 主报告

当前真实 PX4 scope 固定为：

- backend: `px4`
- airframe: `gz_x500`
- world: `default`
- scenario: `nominal`
- modes: `POSCTL` 与 `OFFBOARD_ATTITUDE`

当前链路采用：

- ROS 直录可见 topic
- 对缺失的 rate / actuator / internal topic 做 `.ulg` 缺口回填

当前默认配置：

- `configs/studies/px4_real_nominal_posctl_capture.yaml`
- `configs/studies/px4_real_nominal_offboard_attitude_capture.yaml`
- `configs/studies/px4_real_nominal_broad_ablation_analysis.yaml`
- `configs/ablations/px4_real_broad_ablation_balanced.yaml`

当前权威报告产物：

- `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/reports/summary.md`
- `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/reports/schema_comparison.md`
- `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/summary/study_summary.json`

## 内置 Schema

X 侧：

- `commands_only`
- `commands_plus_state`
- `commands_plus_state_history`
- `commands_plus_controller_params`
- `commands_plus_state_plus_params`
- `pooled_backend_mode_augmented`
- `full_augmented`
- `feature_mapped_linear`

Y 侧：

- `next_raw_state`
- `delta_state`
- `selected_state_subset`
- `future_state_horizon`
- `actuator_response`
- `tracking_error_response`
- `window_summary_response`
- `stability_proxy_response`

## 产物结构

Raw run：

- `artifacts/raw/<backend>/<run_id>/`

Study 输出：

- `prepared/sample_table.csv`
- `prepared/schema_inventory.yaml`
- `fits/<combo>/<model>/matrix_f.csv`
- `fits/<combo>/<model>/bias_b.csv`
- `fits/<combo>/<model>/sparsity_mask.csv`
- `fits/<combo>/<model>/metrics.json`
- `reports/summary.md`
- `reports/schema_comparison.md`
- `summary/study_summary.json`

## 文档

- `docs/RESEARCH_GOAL.md`
- `docs/XY_SCHEMA_GUIDE.md`
- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/DATA_SCHEMA.md`
- `docs/STAGE_REPORT_2026-04-07.md`

## 回归门

```bash
/home/car/autopilot_lab/scripts/ci_minimal.sh
```
