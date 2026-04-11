# PJINFO.md

> 每次 Agent work 前先读本文件；完成后只更新“当前状态”和“最近变更”。

## 项目背景

- 核心目标：验证无人机输入 `X` 与未来响应 `Y` 之间是否存在稳定、可解释的全局线性/仿射映射 `Y ≈ fX (+ b)`
- 当前正式叙事：统一 schema 口径下的线性关系 `f`，以及它是否能跨 `nominal / dynamic / throttle_biased` 三档状态继续成立
- backend 角色：PX4 与 ArduPilot 都只是证据来源，不是比赛对象
- 主要结论标准：
  - `support == supported` 才能作为“得到了可接受线性 `f`”的证据
  - `generalized_supported` 才能作为“这个 `f` 不只是局部拟合，而是跨 scenario 仍然成立”的证据

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
- Matrix 输出：`artifacts/px4_matrix/`、`artifacts/ardupilot_matrix/`
- Study 输出：`artifacts/studies/`

## 当前正式配置

- 当前 canonical compare：
  - `artifacts/studies/20260411_124108_px4_vs_ardupilot_compare`
- PX4 formal baseline study：
  - `artifacts/studies/20260410_224818_px4_real_generalization_ablation`
- PX4 formal diagnostic study：
  - `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`
- ArduPilot formal baseline study：
  - `artifacts/studies/20260411_095055_ardupilot_real_generalization_ablation`
- ArduPilot formal diagnostic study：
  - `artifacts/studies/20260411_105433_ardupilot_generalization_diagnostic_matrix`

- 当前 formal analysis configs：
  - `configs/studies/px4_real_generalization_ablation_analysis.yaml`
  - `configs/ablations/px4_real_generalization_ablation.yaml`
  - `configs/studies/px4_generalization_diagnostic_matrix_analysis.yaml`
  - `configs/ablations/px4_generalization_diagnostic_matrix.yaml`
  - `configs/studies/ardupilot_real_generalization_ablation_analysis.yaml`
  - `configs/ablations/ardupilot_real_generalization_ablation.yaml`
  - `configs/studies/ardupilot_generalization_diagnostic_matrix_analysis.yaml`
  - `configs/ablations/ardupilot_generalization_diagnostic_matrix.yaml`

- 当前 formal scripts：
  - `scripts/run_px4_generalization_pilot.sh`
  - `scripts/run_px4_generalization_full.sh`
  - `scripts/run_ardupilot_generalization_pilot.sh`
  - `scripts/run_ardupilot_generalization_full.sh`

## 当前状态

- [2026-04-11] generalization full 已全部完成：
  - PX4 full baseline: done
  - PX4 full diagnostic: done
  - ArduPilot full baseline: done
  - ArduPilot full diagnostic: done
- [2026-04-11] canonical compare 已切到 `20260411_124108_px4_vs_ardupilot_compare`
- [2026-04-11] canonical docs 已全部刷新到 generalization full：
  - `docs/MILESTONE_LINEAR_F_REPORT.md`
  - `docs/MILESTONE_LINEAR_F_APPENDIX.md`
  - `docs/RESEARCH_GOAL.md`
  - `docs/EXPERIMENT_PROTOCOL.md`
  - `docs/DATA_SCHEMA.md`
  - `docs/XY_SCHEMA_GUIDE.md`
- [2026-04-11] 当前 formal conclusion：
  - 线性关系 `Y ≈ fX (+ b)` 已可作为正面结论正式汇报
  - 两个 backend 都已给出跨 scenario 的 `generalized_supported` 证据
  - PX4 generalized-supported 组合明显更多
  - compare 仍是 `baseline_stability_unresolved`，因此 backend 差异还不是最终主结论
- [2026-04-11] 当前关键数字：
  - PX4 baseline generalized_supported=`80`
  - PX4 diagnostic generalized_supported=`111`
  - ArduPilot baseline generalized_supported=`12`
  - ArduPilot diagnostic generalized_supported=`12`

## 最近变更

- compare payload / markdown 已纳入 `scenario_generalization`
- milestone report / appendix 已切到 latest generalization full 四个 study
- `latest_milestone_refresh.json` 已更新到最新 canonical compare
- `README.md` 已加入当前结论和推荐阅读顺序
- `RESEARCH_GOAL.md`、`EXPERIMENT_PROTOCOL.md`、`DATA_SCHEMA.md`、`XY_SCHEMA_GUIDE.md` 已与 latest formal line 同步

## 常用命令

先加载环境：

```bash
source /home/car/autopilot_lab/scripts/autopilot_lab_env.sh
```

环境体检：

```bash
/home/car/autopilot_lab/scripts/doctor_lab.sh
```

最小 CI：

```bash
/home/car/autopilot_lab/scripts/ci_minimal.sh
```

当前 formal line：

```bash
/home/car/autopilot_lab/scripts/run_px4_generalization_pilot.sh
/home/car/autopilot_lab/scripts/run_px4_generalization_full.sh
/home/car/autopilot_lab/scripts/run_ardupilot_generalization_pilot.sh
/home/car/autopilot_lab/scripts/run_ardupilot_generalization_full.sh
```

支持性 / 历史链路：

```bash
/home/car/autopilot_lab/scripts/run_px4_visual_demos.sh
/home/car/autopilot_lab/scripts/run_ardupilot_visual_demos.sh --include-guided-nogps
/home/car/autopilot_lab/scripts/run_ardupilot_guided_nogps_smoke.sh
/home/car/autopilot_lab/scripts/run_ardupilot_stabilize_partial_baseline.sh
/home/car/autopilot_lab/scripts/run_ardupilot_stabilize_throttle_diagnostic.sh
/home/car/autopilot_lab/scripts/run_px4_authoritative_baseline.sh
/home/car/autopilot_lab/scripts/run_px4_diagnostic_matrix.sh
/home/car/autopilot_lab/scripts/run_ardupilot_authoritative_baseline.sh
/home/car/autopilot_lab/scripts/run_ardupilot_diagnostic_matrix.sh
```

## 注意事项

- 所有文档和交互统一使用简体中文
- 当前正式主标题是“线性关系 `f` 的证据及其跨 scenario 泛化性”，不是“backend 对比”
- 只有最新 generalization full artifact 可以进入当前里程碑汇报
- `20260409` broad baseline / diagnostic 仍保留，但只作为历史阶段背景
