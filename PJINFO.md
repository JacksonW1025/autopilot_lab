# PJINFO.md

> 每次 Agent work 前先读本文件；完成后优先更新“当前状态”和“最近变更”。

## 项目背景

- 核心目标：验证无人机输入 `X` 与未来响应 `Y` 之间是否存在稳定、可解释的全局线性/仿射映射 `Y ≈ fX (+ b)`
- 当前正式叙事：`Formal V2 = generalization full + ArduPilot targeted state-evolution validation`
- backend 角色：PX4 与 ArduPilot 都只是证据来源，不是比赛对象
- 当前正式判断标准：
  - `support == supported` 才能作为“得到了可接受线性 `f`”的证据
  - `generalized_supported` 才能作为“这个 `f` 跨 scenario 仍然成立”的证据
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

- 当前 next-phase narrowing scripts：
  - `scripts/run_ardupilot_a2_stabilize_readiness.sh`
  - `scripts/run_ardupilot_a2_stabilize_boundary_readiness.sh`
  - `scripts/run_ardupilot_a2_guided_nogps_boundary_readiness.sh`
  - `scripts/run_ardupilot_a2_target_scout.sh`
  - `scripts/run_ardupilot_a2_guided_nogps_pair_target_readiness.sh`
  - `scripts/run_px4_a1_target_scout.sh`
  - `scripts/run_px4_a1_attitude_family_readiness.sh`
  - `scripts/run_px4_a1_roll_pitch_targeted_reproduction.sh`
  - `scripts/run_formal_v2_next_phase_decision.sh`

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
- [2026-04-14] 当前 insight-phase 结果 memo 已完成：
  - `docs/FORMAL_V2_INSIGHT_PHASE_MEMO.md`
  - anchor deep dive artifact: `artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive`
  - full in-depth synthesis artifact: `artifacts/studies/20260414_064902_formal_v2_in_depth_analysis`
- [2026-04-15] A2 readiness / boundary narrowing 已完成：
  - `STABILIZE + throttle -> mean/min actuator` 这条 collective boundary 线已经被正式排除
- [2026-04-16] `GUIDED_NOGPS target-scout` 选中的下一个 target 是 `pair_imbalance_12_vs_34`
- [2026-04-16] A2 当前正式状态：
  - `artifacts/studies/20260416_003634_371133_ardupilot_a2_pair_target_readiness`
  - `ready_for_pair_attack_v1=yes`
  - `recommended_path=start_guided_nogps_pair_attack_v1`
- [2026-04-16] A1 当前正式状态：
  - `artifacts/studies/20260416_005450_652002_px4_a1_target_scout`
  - `artifacts/studies/20260416_005450_658923_px4_a1_family_readiness`
  - `artifacts/studies/20260416_010626_381143_px4_a1_roll_pitch_targeted_reproduction`
  - `ready_for_targeted_reproduction_v1=yes`
  - `recommended_path=lock_px4_a1_roll_pitch_targeted_scope`
- [2026-04-16] 统一决策层已完成：
  - `artifacts/studies/20260416_064841_formal_v2_next_phase_decision_layer`
  - `default_entry=A2`
  - `hard_mode=A1`
  - `contrast_only=B1`
  - `boundary_candidates=C1,D1,D2`
- [2026-04-16] 当前故事阶段：
  - 全项目主线：`theory -> empirical validation -> insight` 已完成
  - A2 子线：已到 `attack algorithm` 入口
  - A1 子线：已收窄成 `roll/pitch targeted reproduction`，当前仍是 reproduction/contrast line，不是 attack-ready line

## 当前 live TODO

- A2 主线：
  - 从 `GUIDED_NOGPS + pair_imbalance_12_vs_34` 的 readiness 进入具体 attack algorithm 设计
- A1 对照线：
  - 保持 `future_state_roll / future_state_pitch` 作为可复现 continuation / contrast line
- 文档与决策口径：
  - 默认以 `artifacts/studies/20260416_064841_formal_v2_next_phase_decision_layer` 作为当前 route-selection 入口

## 已完成 / 不再作为 live TODO

- `NEXT.md` 里的 intervention-readiness / next-phase decision layer 构建任务已完成，不要再把它当成当前待办。
- broad validation 扩展不是当前优先级；当前不建议再回头扩更宽的 generalized combo 搜索。
- A2 的 collective throttle-floor / collective actuator boundary 线已正式排除，不再作为主线目标。

## 当前 insight 摘要

- [2026-04-14] 当前这份 insight memo 是结果文档，不是计划：
  - `docs/FORMAL_V2_INSIGHT_PHASE_MEMO.md`
- [2026-04-14] generalized-supported 的稳定结构现在可以压缩成两类：
  - PX4：state-dominated 的短时传播结构，stable-core=`80`
  - ArduPilot：`commands_only` 主导的低维 direct-control 结构，stable-core=`12`
- [2026-04-14] PX4 最可靠的 generalized-supported 证据更像 `current state + short lag -> future/summary`，不是 command-only 主导。
- [2026-04-14] ArduPilot 最可靠的 generalized-supported 证据集中在 `commands_only -> actuator_response`，其中 `command_throttle` 对 `actuator_1~4` 的支配最稳定。
- [2026-04-16] 上面的 A2 仍是 insight anchor，不等于最终 executable target；当前真正通过 narrowing 站住的是 pair target，而不是 collective throttle-floor。
- [2026-04-14] ArduPilot `commands_plus_state_history -> selected_state_subset` 这类高分路径不是“没结构”，而是被 formal boundary 卡住：
  - `C1`：stable partial mask + 极高 condition number
  - `D2`：empty mask + stable raw template
  - `D1`：empty mask + raw collapse
- [2026-04-14] backend-shared 的是语义输出家族，不是 support pattern 本身：
  - shared alignment key=`9`
  - top-edge overlap 平均接近 `0`
- [2026-04-14] 当前已足够支持后续 attack design 的最小原则：
  - 低维优先
  - 非空且跨 study 稳定的 support 优先
  - direct-control path 优先
  - 高分但病态路径降权
  - PX4 若继续推进，应优先考虑 state/feedback channel，不默认走 throttle
- [2026-04-16] A2 的最新 narrowing 结论：
  - 可用 target 不是 collective throttle-floor，也不是 `mean(actuator_1..4)`
  - 当前最稳 target 是 `GUIDED_NOGPS + pair_imbalance_12_vs_34`
  - dominant direction 固定为 `12_gt_34`
- [2026-04-16] A1 的最新 narrowing 结论：
  - 当前最稳 family 是 `attitude_roll_pitch_continuation`
  - 当前最稳 exact reproduction scope 是 `future_state_roll / future_state_pitch`
  - baseline/diagnostic 两相的 top1 都稳定落在 `roll / pitch`

## 最近变更

- `docs/FORMAL_V2_INSIGHT_PHASE_MEMO.md` 已从 checkpoint 扩展为当前 repo-state 下的完整 insight-phase 结果 memo
- 新增 `artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive`
- 新增 `artifacts/studies/20260414_064902_formal_v2_in_depth_analysis`
- 新增 `scripts/analyze_anchor_deep_dive.py` 与 `src/linearity_analysis/linearity_analysis/anchor_deep_dive.py`
- `scenario_generalization` 与 `sparsity_overlap` 已进入正式 artifact 链路
- ArduPilot mode-isolated targeted line 已加入 Formal V2 正式口径
- milestone report / appendix 已显式引用 targeted aggregate 与四个 targeted input study
- `README.md`、`PJINFO.md`、`docs/RESEARCH_GOAL.md`、`docs/DATA_SCHEMA.md` 已与 latest Formal V2 同步
- 旧 `20260409` 准备性 artifact、旧 ArduPilot full studies、旧 compare 已从当前正式引用集移除并完成 prune
- 新增 A2 narrowing analysis：
  - `src/linearity_analysis/linearity_analysis/ardupilot_a2_readiness.py`
  - `src/linearity_analysis/linearity_analysis/ardupilot_a2_boundary_readiness.py`
  - `src/linearity_analysis/linearity_analysis/ardupilot_a2_target_scout.py`
  - `src/linearity_analysis/linearity_analysis/ardupilot_a2_pair_target_readiness.py`
- 新增 A1 narrowing analysis：
  - `src/linearity_analysis/linearity_analysis/px4_a1_target_scout.py`
  - `src/linearity_analysis/linearity_analysis/px4_a1_family_readiness.py`
  - `src/linearity_analysis/linearity_analysis/px4_a1_roll_pitch_targeted_reproduction.py`
- 新增最新 decisive narrowing artifacts：
  - `artifacts/studies/20260416_003634_371133_ardupilot_a2_pair_target_readiness`
  - `artifacts/studies/20260416_010626_381143_px4_a1_roll_pitch_targeted_reproduction`
- 新增统一决策层：
  - `src/linearity_analysis/linearity_analysis/next_phase_decision_layer.py`
  - `scripts/analyze_formal_v2_next_phase_decision.py`
  - `scripts/run_formal_v2_next_phase_decision.sh`
  - `docs/NEXT_PHASE_DECISION_LAYER.md`
  - `artifacts/studies/20260416_064841_formal_v2_next_phase_decision_layer`

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

next-phase narrowing 入口：

```bash
/home/car/autopilot_lab/scripts/run_ardupilot_a2_target_scout.sh
/home/car/autopilot_lab/scripts/run_ardupilot_a2_guided_nogps_pair_target_readiness.sh
/home/car/autopilot_lab/scripts/run_px4_a1_target_scout.sh
/home/car/autopilot_lab/scripts/run_px4_a1_attitude_family_readiness.sh
/home/car/autopilot_lab/scripts/run_px4_a1_roll_pitch_targeted_reproduction.sh
```

## 注意事项

- 所有文档和交互统一使用简体中文
- 当前正式主标题是“线性关系 `f` 的证据及其跨 scenario 泛化性”，不是“backend 对比”
- Formal V2 有两条同级正式线：generalization full 和 ArduPilot targeted validation
- next-phase narrowing studies 是 Formal V2 之后的窄分析线；它们依赖 canonical artifact，但不替代 Formal V2 主线
- targeted aggregate 和四个 targeted input study 都属于当前正式 artifact，不是 supplementary
- 只有 latest Formal V2 artifact 可以进入当前里程碑汇报
- `20260409` broad baseline、旧 ArduPilot `20260411` full studies 和旧 compare 已从当前正式口径移出
- 当前建议优先级：
  - 主线：A2 `GUIDED_NOGPS / pair_imbalance_12_vs_34`
  - 对照线：A1 `roll/pitch targeted reproduction`
