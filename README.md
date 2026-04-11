# autopilot_lab

`autopilot_lab` 是一个面向无人机输入到响应关系研究的实验仓库。当前正式主线是：

> 在统一的 `X / Y schema` 口径下，验证 PX4 与 ArduPilot 是否都存在稳定、可解释的全局线性或仿射映射 `Y ≈ fX (+ b)`，并进一步检查它是否能在多种 scenario 下继续保持可接受的解释力。

这里的重点不是比较两种飞控“谁更强”，而是回答两件事：

1. 线性关系 `f` 本身是否成立。
2. 它在 `nominal / dynamic / throttle_biased` 三档状态下是否还能站得住。

## 当前正式结果

当前 canonical compare 已切到 generalization full：

- compare artifact: [20260411_124108_px4_vs_ardupilot_compare](/home/car/autopilot_lab/artifacts/studies/20260411_124108_px4_vs_ardupilot_compare)
- PX4 full baseline: [20260410_224818_px4_real_generalization_ablation](/home/car/autopilot_lab/artifacts/studies/20260410_224818_px4_real_generalization_ablation)
- PX4 full diagnostic: [20260411_021910_px4_generalization_diagnostic_matrix](/home/car/autopilot_lab/artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix)
- ArduPilot full baseline: [20260411_095055_ardupilot_real_generalization_ablation](/home/car/autopilot_lab/artifacts/studies/20260411_095055_ardupilot_real_generalization_ablation)
- ArduPilot full diagnostic: [20260411_105433_ardupilot_generalization_diagnostic_matrix](/home/car/autopilot_lab/artifacts/studies/20260411_105433_ardupilot_generalization_diagnostic_matrix)

当前最简明的结论是：

- 线性关系 `Y ≈ fX (+ b)` 已经可以作为正面结论正式汇报。
- 两个 backend 都出现了跨 scenario 的 `generalized_supported` 组合。
- PX4 的 generalized-supported 证据更宽，ArduPilot 的证据更窄但是真实存在。
- 现在还不适合把“backend 差异”写成最终主结论，因为 compare 仍然显示 `baseline_stability_unresolved`。

## 建议阅读顺序

如果你是第一次进仓库，按这个顺序读：

1. [MILESTONE_LINEAR_F_REPORT.md](docs/MILESTONE_LINEAR_F_REPORT.md)
   先看当前阶段到底得出了什么结论。
2. [MILESTONE_LINEAR_F_APPENDIX.md](docs/MILESTONE_LINEAR_F_APPENDIX.md)
   再看 artifact 清单、核心数字和代表性组合路径。
3. [RESEARCH_GOAL.md](docs/RESEARCH_GOAL.md)
   明确项目真正想回答的问题，以及 `generalized_supported` 现在意味着什么。
4. [EXPERIMENT_PROTOCOL.md](docs/EXPERIMENT_PROTOCOL.md)
   了解当前正式实验线已经变成什么顺序，旧 broad baseline 现在只是历史阶段。
5. [DATA_SCHEMA.md](docs/DATA_SCHEMA.md)
   确认 raw/study contract、prepared sample table 和 `scenario_generalization` 产物的口径。
6. [XY_SCHEMA_GUIDE.md](docs/XY_SCHEMA_GUIDE.md)
   最后再看 `X/Y schema` 应该怎么读、现在先看哪些代表性组合。

如果要直接看最新正式对照：

1. [backend_compare.md](/home/car/autopilot_lab/artifacts/studies/20260411_124108_px4_vs_ardupilot_compare/reports/backend_compare.md)
2. [scenario_generalization.md](/home/car/autopilot_lab/artifacts/studies/20260410_224818_px4_real_generalization_ablation/reports/scenario_generalization.md)
3. [scenario_generalization.md](/home/car/autopilot_lab/artifacts/studies/20260411_095055_ardupilot_real_generalization_ablation/reports/scenario_generalization.md)

## 当前研究口径

- 正式 backend：`px4`、`ardupilot`
- 正式 scenario：`nominal`、`dynamic`、`throttle_biased`
- 正式 baseline mode：
  - PX4: `POSCTL`、`OFFBOARD_ATTITUDE`
  - ArduPilot: `STABILIZE`、`GUIDED_NOGPS`
- 正式 analysis matrix：
  - `x_schemas`: `commands_only`, `commands_plus_state`, `commands_plus_state_history`, `full_augmented`, `pooled_backend_mode_augmented`, `feature_mapped_linear`
  - `y_schemas`: `next_raw_state`, `delta_state`, `selected_state_subset`, `future_state_horizon`, `actuator_response`, `window_summary_response`
  - `models`: `ols_affine`, `ridge_affine`, `lasso_affine`
  - `pooling_modes`: `pooled`, `stratified`

## 仓库结构

```text
autopilot_lab/
├── artifacts/
│   ├── raw/
│   ├── px4_matrix/
│   ├── ardupilot_matrix/
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

## 环境入口

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

最小回归：

```bash
/home/car/autopilot_lab/scripts/ci_minimal.sh
```

## 当前正式实验入口

当前 formal line 是 generalization 线。建议优先看这些入口：

```bash
/home/car/autopilot_lab/scripts/run_px4_generalization_pilot.sh
/home/car/autopilot_lab/scripts/run_px4_generalization_full.sh
/home/car/autopilot_lab/scripts/run_ardupilot_generalization_pilot.sh
/home/car/autopilot_lab/scripts/run_ardupilot_generalization_full.sh
```

支持性实验与历史阶段入口仍保留：

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

辅助入口：

```bash
/home/car/autopilot_lab/scripts/run_cross_backend_contract_audit.sh --px4-run <accepted_px4_raw_dir> --ardupilot-run <accepted_ardupilot_raw_dir>
/home/car/autopilot_lab/scripts/compare_schemas.sh --help
/home/car/autopilot_lab/scripts/visualize_fit_matrices.py --help
```

## Study 产物

每个正式 study 至少包含：

- `prepared/sample_table.csv`
- `prepared/schema_inventory.yaml`
- `fits/<combo>/<model>/matrix_f.csv`
- `fits/<combo>/<model>/bias_b.csv`
- `fits/<combo>/<model>/sparsity_mask.csv`
- `fits/<combo>/<model>/metrics.json`
- `reports/summary.md`
- `reports/schema_comparison.md`
- `reports/baseline_stability.md`
- `reports/diagnostic_gate.md`
- `reports/matrix_gallery.md`
- `reports/scenario_generalization.md`
- `summary/study_summary.json`
- `summary/baseline_stability.json`
- `summary/diagnostic_gate.json`
- `summary/matrix_gallery.json`
- `summary/scenario_generalization.json`

当某个组合被判为 `supported` 时，还会自动生成：

- `fits/<combo>/<model>/matrix_heatmap_abs.png`
- `fits/<combo>/<model>/matrix_heatmap_signed.png`

## 文档

- [MILESTONE_LINEAR_F_REPORT.md](docs/MILESTONE_LINEAR_F_REPORT.md)
- [MILESTONE_LINEAR_F_APPENDIX.md](docs/MILESTONE_LINEAR_F_APPENDIX.md)
- [RESEARCH_GOAL.md](docs/RESEARCH_GOAL.md)
- [EXPERIMENT_PROTOCOL.md](docs/EXPERIMENT_PROTOCOL.md)
- [DATA_SCHEMA.md](docs/DATA_SCHEMA.md)
- [XY_SCHEMA_GUIDE.md](docs/XY_SCHEMA_GUIDE.md)

当前里程碑汇报和附录只以最新 generalization full artifact 为准。20260409 的 broad baseline / diagnostic 仍保留，但只作为历史阶段背景。
