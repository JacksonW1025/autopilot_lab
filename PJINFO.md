# PJINFO.md

> 每次 Agent work 前先读本文件；完成后优先更新“当前状态”和“最近变更”。

## 项目背景

- 核心目标：验证无人机输入 `X` 与未来响应 `Y` 之间是否存在稳定、可解释的全局线性/仿射映射 `Y ≈ fX (+ b)`
- 当前正式叙事：`Formal V2 = generalization full + ArduPilot targeted state-evolution validation`
- backend 角色：PX4 与 ArduPilot 都只是证据来源，不是比赛对象
- 当前正式判断标准：
  - `support == supported` 才能作为“得到了可接受线性 `f`”的证据
  - `generalized_supported` 才能作为“这个 `f` 跨 scenario 仍然成立”的证据
  - `all_holdouts_supported` 才能作为“leave-one-scenario-out 后仍然稳定”的证据
  - `mature_positive / mature_negative / inconclusive` 是 targeted line 的正式状态

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
- Raw run：`artifacts/raw/`，本地保留但默认不再推送到远端 Git
- Matrix 输出：`artifacts/px4_matrix/`、`artifacts/ardupilot_matrix/`
- Study 输出：`artifacts/studies/`

## Artifact 策略

- remote canonical 集合只保留 latest Formal V2 `artifacts/studies/**` 与正式文档。
- `artifacts/raw/**` 只作为本地实验数据保留，用于复现、审计和调试。
- `artifacts/*_matrix/**` 不属于当前正式远端保留集。

## 当前正式配置

- 当前 canonical compare：
  - `artifacts/studies/20260413_134755_px4_vs_ardupilot_compare`
- PX4 formal baseline study：
  - `artifacts/studies/20260410_224818_px4_real_generalization_ablation`
- PX4 formal diagnostic study：
  - `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`
- ArduPilot formal baseline study：
  - `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation`
- ArduPilot formal diagnostic study：
  - `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix`
- ArduPilot targeted aggregate：
  - `artifacts/studies/20260413_134505_ardupilot_state_evolution_validation`
- ArduPilot targeted input studies：
  - `artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline`
  - `artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic`
  - `artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline`
  - `artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic`

- 当前 formal analysis configs：
  - `configs/studies/px4_real_generalization_ablation_analysis.yaml`
  - `configs/ablations/px4_real_generalization_ablation.yaml`
  - `configs/studies/px4_generalization_diagnostic_matrix_analysis.yaml`
  - `configs/ablations/px4_generalization_diagnostic_matrix.yaml`
  - `configs/studies/ardupilot_real_generalization_ablation_analysis.yaml`
  - `configs/ablations/ardupilot_real_generalization_ablation.yaml`
  - `configs/studies/ardupilot_generalization_diagnostic_matrix_analysis.yaml`
  - `configs/ablations/ardupilot_generalization_diagnostic_matrix.yaml`
  - `configs/studies/ardupilot_state_evolution_targeted_baseline_analysis.yaml`
  - `configs/ablations/ardupilot_state_evolution_targeted_baseline.yaml`
  - `configs/studies/ardupilot_state_evolution_targeted_diagnostic_analysis.yaml`
  - `configs/ablations/ardupilot_state_evolution_targeted_diagnostic.yaml`

- 当前 formal scripts：
  - `scripts/run_px4_generalization_full.sh`
  - `scripts/run_ardupilot_generalization_full.sh`
  - `scripts/run_ardupilot_state_evolution_validation_full.sh`
  - `scripts/run_formal_v2_ardupilot_refresh.sh`
  - `scripts/run_ardupilot_state_evolution_baseline.sh`
  - `scripts/run_ardupilot_state_evolution_diagnostic.sh`

## 当前状态

- [2026-04-13] Formal V2 ArduPilot refresh 已完整结束：
  - ArduPilot full baseline: done
  - ArduPilot full diagnostic: done
  - STABILIZE targeted baseline: done
  - STABILIZE targeted diagnostic: done
  - GUIDED_NOGPS targeted baseline: done
  - GUIDED_NOGPS targeted diagnostic: done
  - targeted aggregate: done
  - compare refresh: done
  - docs refresh: done
  - prune old artifact: done
- [2026-04-13] current canonical compare 已切到 `20260413_134755_px4_vs_ardupilot_compare`
- [2026-04-13] current canonical docs 已刷新到 latest Formal V2：
  - `docs/MILESTONE_LINEAR_F_REPORT.md`
  - `docs/MILESTONE_LINEAR_F_APPENDIX.md`
  - `docs/RESEARCH_GOAL.md`
  - `docs/EXPERIMENT_PROTOCOL.md`
  - `docs/DATA_SCHEMA.md`
  - `docs/XY_SCHEMA_GUIDE.md`
  - `docs/figures/heatmaps/README.md`
  - `README.md`
- [2026-04-13] targeted aggregate status：
  - `overall_status=mode_isolated_state_evolution_still_inconclusive`
  - `STABILIZE=inconclusive`
  - `GUIDED_NOGPS=inconclusive`
- [2026-04-13] current formal conclusion：
  - 线性关系 `Y ≈ fX (+ b)` 已可作为正面结论正式汇报
  - 两个 backend 都已给出跨 scenario 的 `generalized_supported` 证据
  - PX4 generalized-supported 组合明显更多
  - ArduPilot targeted line 已经正式落盘，但 state-evolution 仍未收敛到成熟正/负结论
  - compare 仍是 `baseline_stability_unresolved`，因此 backend 差异还不是最终主结论
- [2026-04-13] 当前关键数字：
  - PX4 baseline generalized_supported=`80`
  - PX4 diagnostic generalized_supported=`111`
  - ArduPilot baseline generalized_supported=`12`
  - ArduPilot diagnostic generalized_supported=`12`

## 最近变更

- `scenario_holdout` 与 `sparsity_overlap` 已进入正式 artifact 链路
- ArduPilot mode-isolated targeted line 已加入 Formal V2 正式口径
- milestone report / appendix 已显式引用 targeted aggregate 与四个 targeted input study
- `README.md`、`PJINFO.md`、`docs/RESEARCH_GOAL.md`、`docs/DATA_SCHEMA.md` 已与 latest Formal V2 同步
- 旧 `20260409` 准备性 artifact、旧 ArduPilot full studies、旧 compare 已从当前正式引用集移除并完成 prune

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

当前 Formal V2 主入口：

```bash
/home/car/autopilot_lab/scripts/run_px4_generalization_full.sh
/home/car/autopilot_lab/scripts/run_ardupilot_generalization_full.sh
/home/car/autopilot_lab/scripts/run_ardupilot_state_evolution_validation_full.sh
/home/car/autopilot_lab/scripts/run_formal_v2_ardupilot_refresh.sh
```

targeted line 局部入口：

```bash
/home/car/autopilot_lab/scripts/run_ardupilot_state_evolution_baseline.sh --mode stabilize
/home/car/autopilot_lab/scripts/run_ardupilot_state_evolution_diagnostic.sh --mode stabilize
/home/car/autopilot_lab/scripts/run_ardupilot_state_evolution_baseline.sh --mode guided_nogps
/home/car/autopilot_lab/scripts/run_ardupilot_state_evolution_diagnostic.sh --mode guided_nogps
```

## 注意事项

- 所有文档和交互统一使用简体中文
- 当前正式主标题是“线性关系 `f` 的证据及其跨 scenario 泛化性”，不是“backend 对比”
- Formal V2 有两条同级正式线：generalization full 和 ArduPilot targeted validation
- targeted aggregate 和四个 targeted input study 都属于当前正式 artifact，不是 supplementary
- 只有 latest Formal V2 artifact 可以进入当前里程碑汇报
- `20260409` broad baseline、旧 ArduPilot `20260411` full studies 和旧 compare 已从当前正式口径移出
