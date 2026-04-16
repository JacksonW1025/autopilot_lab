# autopilot_lab

`autopilot_lab` 是一个面向无人机输入到响应关系研究的实验仓库。当前正式主线仍是 `Formal V2`，但仓库状态已经不只停留在 milestone summary；截至 `2026-04-14`，基于当前 repo artifact 的 insight-phase 分析也已经完成，并落到：

- [FORMAL_V2_INSIGHT_PHASE_MEMO.md](docs/FORMAL_V2_INSIGHT_PHASE_MEMO.md)
- [20260414_064153_formal_v2_anchor_deep_dive](/home/car/autopilot_lab/artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive)
- [20260414_064902_formal_v2_in_depth_analysis](/home/car/autopilot_lab/artifacts/studies/20260414_064902_formal_v2_in_depth_analysis)

Formal V2 的基本问题仍然是：

> 在统一的 `X / Y schema` 口径下，验证 PX4 与 ArduPilot 是否都存在稳定、可解释的全局线性或仿射映射 `Y ≈ fX (+ b)`；并进一步检查它是否能跨 `nominal / dynamic / throttle_biased` 三档 scenario 成立，以及 ArduPilot 的 mode-isolated state-evolution 能否形成成熟结论。

这里的重点不是比较两种飞控“谁更强”，而是回答三件事：

1. 线性关系 `f` 本身是否成立。
2. 它在多种 scenario 下是否还能站得住。
3. ArduPilot 的 state-evolution 在不混 mode 时，是否已经形成成熟正结论或成熟负结论。

## 当前正式结果

当前 canonical Formal V2 artifact 是：

- compare artifact: [20260413_134755_px4_vs_ardupilot_compare](/home/car/autopilot_lab/artifacts/studies/20260413_134755_px4_vs_ardupilot_compare)
- PX4 full baseline: [20260410_224818_px4_real_generalization_ablation](/home/car/autopilot_lab/artifacts/studies/20260410_224818_px4_real_generalization_ablation)
- PX4 full diagnostic: [20260411_021910_px4_generalization_diagnostic_matrix](/home/car/autopilot_lab/artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix)
- ArduPilot full baseline: [20260413_070802_ardupilot_real_generalization_ablation](/home/car/autopilot_lab/artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation)
- ArduPilot full diagnostic: [20260413_091420_ardupilot_generalization_diagnostic_matrix](/home/car/autopilot_lab/artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix)
- ArduPilot targeted validation: [20260413_134505_ardupilot_state_evolution_validation](/home/car/autopilot_lab/artifacts/studies/20260413_134505_ardupilot_state_evolution_validation)
- latest insight memo: [FORMAL_V2_INSIGHT_PHASE_MEMO.md](docs/FORMAL_V2_INSIGHT_PHASE_MEMO.md)
- latest insight aggregate: [20260414_064153_formal_v2_anchor_deep_dive](/home/car/autopilot_lab/artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive), [20260414_064902_formal_v2_in_depth_analysis](/home/car/autopilot_lab/artifacts/studies/20260414_064902_formal_v2_in_depth_analysis)

当前最简明的结论是：

- 线性关系 `Y ≈ fX (+ b)` 已经可以作为正面结论正式汇报。
- 两个 backend 都出现了跨 scenario 的 `generalized_supported` 组合。
- PX4 的 generalized-supported 证据更宽，ArduPilot 的正式证据更窄但真实存在。
- ArduPilot 的 mode-isolated targeted line 已经形成正式 artifact，但 `overall_status=mode_isolated_state_evolution_still_inconclusive`。
- compare 当前仍然是 `baseline_stability_unresolved`，所以 backend 差异仍然不是主标题。

如果只看当前 repo-state 下最重要的 insight 结果，可以再压缩成下面 6 条：

- PX4 当前最可靠的 generalized-supported 结构不是 command-only，而是 state-dominated 的短时传播结构；stable-core=`80`。
- ArduPilot 当前最可靠的 generalized-supported 结构是 `commands_only` 主导的低维 direct-control path；stable-core=`12`。
- ArduPilot 最适合作为后续 attack principal anchor 的是 `commands_only -> actuator_response`，尤其是 `command_throttle -> actuator_1~4`。
- `commands_plus_state_history -> selected_state_subset` 一类高分路径不是没结构，而是被 conditioning / mask-collapse / raw-collapse 卡住，因此目前仍不能当正式主攻击基础。
- backend-shared 的是语义输出家族，不是 support pattern 本身；shared alignment key=`9`，但 top-edge overlap 平均接近 `0`。
- 当前已经足够支持的 design principle 是：低维优先、稳定非空 support 优先、direct-control path 优先、高分病态路径降权；PX4 若继续推进，更应考虑 state/feedback channel。

## 建议阅读顺序

如果你是第一次进仓库，按这个顺序读：

1. [FORMAL_V2_INSIGHT_PHASE_MEMO.md](docs/FORMAL_V2_INSIGHT_PHASE_MEMO.md)
2. [MILESTONE_LINEAR_F_REPORT.md](docs/MILESTONE_LINEAR_F_REPORT.md)
3. [MILESTONE_LINEAR_F_APPENDIX.md](docs/MILESTONE_LINEAR_F_APPENDIX.md)
4. [RESEARCH_GOAL.md](docs/RESEARCH_GOAL.md)
5. [EXPERIMENT_PROTOCOL.md](docs/EXPERIMENT_PROTOCOL.md)
6. [DATA_SCHEMA.md](docs/DATA_SCHEMA.md)
7. [XY_SCHEMA_GUIDE.md](docs/XY_SCHEMA_GUIDE.md)
8. [docs/figures/heatmaps/README.md](docs/figures/heatmaps/README.md)

如果要直接看最新正式 artifact，建议从这里开始：

1. [FORMAL_V2_INSIGHT_PHASE_MEMO.md](docs/FORMAL_V2_INSIGHT_PHASE_MEMO.md)
2. [backend_compare.md](/home/car/autopilot_lab/artifacts/studies/20260413_134755_px4_vs_ardupilot_compare/reports/backend_compare.md)
3. [state_evolution_validation.md](/home/car/autopilot_lab/artifacts/studies/20260413_134505_ardupilot_state_evolution_validation/reports/state_evolution_validation.md)
4. [anchor_deep_dive.json](/home/car/autopilot_lab/artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/summary/anchor_deep_dive.json)
5. [in_depth_analysis.json](/home/car/autopilot_lab/artifacts/studies/20260414_064902_formal_v2_in_depth_analysis/summary/in_depth_analysis.json)
6. [PX4 scenario_generalization.md](/home/car/autopilot_lab/artifacts/studies/20260410_224818_px4_real_generalization_ablation/reports/scenario_generalization.md)
7. [ArduPilot scenario_generalization.md](/home/car/autopilot_lab/artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/reports/scenario_generalization.md)
8. [ArduPilot sparsity_overlap.md](/home/car/autopilot_lab/artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/reports/sparsity_overlap.md)

## 当前研究口径

- 正式实验线：
  - `generalization full`：回答“线性关系是否存在，以及它是否能跨 scenario 成立”
  - `ArduPilot targeted state-evolution validation`：回答“state-evolution 在不混 mode 时是否形成成熟正/负结论”
- 正式 backend：`px4`、`ardupilot`
- 正式 scenario：`nominal`、`dynamic`、`throttle_biased`
- 正式 baseline mode：
  - PX4: `POSCTL`、`OFFBOARD_ATTITUDE`
  - ArduPilot: `STABILIZE`、`GUIDED_NOGPS`
- generalization full analysis matrix：
  - `x_schemas`: `commands_only`, `commands_plus_state`, `commands_plus_state_history`, `full_augmented`, `pooled_backend_mode_augmented`, `feature_mapped_linear`
  - `y_schemas`: `next_raw_state`, `delta_state`, `selected_state_subset`, `future_state_horizon`, `actuator_response`, `window_summary_response`
  - `models`: `ols_affine`, `ridge_affine`, `lasso_affine`
  - `pooling_modes`: `pooled`, `stratified`
- ArduPilot targeted line 只分析：
  - `x_schemas`: `commands_plus_state_history`, `full_augmented`
  - `y_schemas`: `next_raw_state`, `selected_state_subset`
  - `models`: `ols_affine`, `ridge_affine`, `lasso_affine`
  - `pooling_mode`: `pooled`

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

## Artifact 保留策略

- 远端 Git 只保留 current latest Formal V2 的 `artifacts/studies/**` 与正式文档。
- `artifacts/raw/**` 继续作为本地实验产物存在，用于复现、审计和排查问题，但不再作为远端仓库的长期跟踪内容。
- `artifacts/px4_matrix/**` 与 `artifacts/ardupilot_matrix/**` 属于临时 matrix 目录，不进入 current canonical remote 集合。

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

当前推荐入口已经切到 Formal V2：

```bash
/home/car/autopilot_lab/scripts/run_px4_generalization_full.sh
/home/car/autopilot_lab/scripts/run_ardupilot_generalization_full.sh
/home/car/autopilot_lab/scripts/run_ardupilot_state_evolution_validation_full.sh
/home/car/autopilot_lab/scripts/run_formal_v2_ardupilot_refresh.sh
```

如果只想跑 targeted line 的某一段：

```bash
/home/car/autopilot_lab/scripts/run_ardupilot_state_evolution_baseline.sh --mode stabilize
/home/car/autopilot_lab/scripts/run_ardupilot_state_evolution_diagnostic.sh --mode stabilize
/home/car/autopilot_lab/scripts/run_ardupilot_state_evolution_baseline.sh --mode guided_nogps
/home/car/autopilot_lab/scripts/run_ardupilot_state_evolution_diagnostic.sh --mode guided_nogps
```

支持性和历史阶段入口仍保留，但不再进入当前正式口径：

```bash
/home/car/autopilot_lab/scripts/run_px4_visual_demos.sh
/home/car/autopilot_lab/scripts/run_ardupilot_visual_demos.sh --include-guided-nogps
/home/car/autopilot_lab/scripts/run_ardupilot_guided_nogps_smoke.sh
/home/car/autopilot_lab/scripts/run_ardupilot_stabilize_partial_baseline.sh
/home/car/autopilot_lab/scripts/run_ardupilot_stabilize_throttle_diagnostic.sh
/home/car/autopilot_lab/scripts/run_cross_backend_contract_audit.sh --px4-run <accepted_px4_raw_dir> --ardupilot-run <accepted_ardupilot_raw_dir>
```

## Study 产物

每个 current generalization full / targeted study 至少包含：

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
- `reports/sparsity_overlap.md`
- `summary/study_summary.json`
- `summary/baseline_stability.json`
- `summary/diagnostic_gate.json`
- `summary/matrix_gallery.json`
- `summary/scenario_generalization.json`
- `summary/sparsity_overlap.json`

ArduPilot targeted study 额外包含：

- `reports/state_evolution_audit.md`
- `summary/state_evolution_audit.json`

ArduPilot targeted aggregate 额外包含：

- `reports/state_evolution_validation.md`
- `summary/state_evolution_validation.json`

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
- [docs/figures/heatmaps/README.md](docs/figures/heatmaps/README.md)

当前里程碑汇报和附录只以 latest Formal V2 artifact 为准。`20260409` broad baseline、旧 ArduPilot full studies 和旧 compare 已经移出当前正式引用集。
