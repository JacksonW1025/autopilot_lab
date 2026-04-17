# Formal V2 Next-Phase Decision Layer

## 这层解决什么问题

这不是新的 canonical Formal V2 主分析，也不是新实验。

它是一个薄的 aggregate decision layer，用来把已经存在的 4 类派生 artifact 收束成一个统一决策板：

- `formal_v2_anchor_deep_dive`
- `formal_v2_in_depth_analysis`
- `ardupilot_a2_pair_target_readiness`
- `px4_a1_roll_pitch_targeted_reproduction`

这层只回答下一阶段最关键的决策问题：

- 默认主入口是谁
- hard mode / backup line 是谁
- 哪些路径只是对照项
- 哪些路径只能作为 boundary / pathology evidence

## 和当前 Formal V2 主线的关系

- 不改写 existing canonical memo、milestone、appendix 或 acceptance gate。
- 不重跑 raw artifact，也不扫描所有历史 combo。
- 默认只读取已经存在的 `summary/*.json` 与 `tables/*.csv`。
- 只有当某个 candidate 缺少必要字段时，才允许回查对应 `metrics.json`、`matrix_f.csv`、`sparsity_mask.csv`。

因此，这层的职责是“统一决策口径”，不是“生成第二套 formal 结论”。

## 决策口径

### Bucket-first, score-second

先分桶，再在桶内排序。

固定 bucket：

- `primary_entry_ready`
- `mechanism_rich_hard_mode`
- `contrast_non_entry`
- `boundary_or_pathology`

固定 score 用途：

- 只做桶内排序
- 不允许 score 覆盖 bucket

## Candidate 字段

主表 `candidate_board.csv` 固定包含：

- `candidate_id`
- `anchor_family`
- `backend`
- `combo`
- `structure_type`
- `support_status`
- `generalization_status`
- `explicit_ready_signal`
- `conditioning_band`
- `mask_state`
- `decision_bucket`
- `decision_score`
- `decision_priority`
- `recommended_role`
- `recommended_next_phase`
- `downgrade_reasons`
- `rationale`
- `evidence_sources`

### 派生字段定义

`conditioning_band`

- `low < 1e2`
- `medium [1e2, 1e5)`
- `high [1e5, 1e8)`
- `extreme >= 1e8`

`mask_state`

- `stable_non_empty`
- `partial_non_empty`
- `empty`

`structure_type`

- `direct_control`
- `state_continuation`
- `autoregressive_blocked`
- `collapse_boundary`

## 输出物

运行后会生成：

- `reports/next_phase_decision_layer.md`
- `summary/next_phase_decision_layer.json`
- `tables/candidate_board.csv`
- `tables/decision_routing.csv`
- `tables/boundary_catalog.csv`
- `tables/stable_core_watchlist.csv`

其中：

- `candidate_board.csv` 是主候选板
- `decision_routing.csv` 是下一阶段路由建议
- `boundary_catalog.csv` 专门列出 non-entry boundary/pathology 样本
- `stable_core_watchlist.csv` 只做 generalized-supported peer 旁证，不参与主排序

## 当前 canonical 引用

当前 route-selection 的 canonical artifact 已刷新到：

- `artifacts/studies/20260417_001929_formal_v2_next_phase_decision_layer`

它当前消费的 A2 输入是：

- `artifacts/studies/20260417_001924_151397_ardupilot_a2_target_scout`
- `artifacts/studies/20260417_001925_356349_ardupilot_a2_pair_target_readiness`

当前正式结论保持不变：

- `default_entry=A2`
- `hard_mode=A1`
- `contrast_only=B1`
- `boundary_candidates=C1,D1,D2`

## 如何运行

自动发现最新派生 artifact：

```bash
/home/car/autopilot_lab/scripts/run_formal_v2_next_phase_decision.sh
```

显式指定输入：

```bash
python3 /home/car/autopilot_lab/scripts/analyze_formal_v2_next_phase_decision.py \
  --anchor-deep-dive /home/car/autopilot_lab/artifacts/studies/<anchor_dir> \
  --in-depth-analysis /home/car/autopilot_lab/artifacts/studies/<in_depth_dir> \
  --a2-pair-target /home/car/autopilot_lab/artifacts/studies/<a2_dir> \
  --a1-targeted-reproduction /home/car/autopilot_lab/artifacts/studies/<a1_dir> \
  --output-dir /home/car/autopilot_lab/artifacts/studies/<new_dir>
```

如果只是刷新 A2 主线输入，先跑：

```bash
/home/car/autopilot_lab/scripts/run_ardupilot_a2_guided_nogps_pair_pipeline.sh
```

它会先过现有 `GUIDED_NOGPS` smoke，再串起 `a2_target_scout`、`a2_pair_target_readiness`，最后把新的 A2 artifact 喂给 decision layer。

## 如何阅读结果

推荐顺序：

1. 先看 `reports/next_phase_decision_layer.md`
2. 再看 `tables/candidate_board.csv`
3. 如果要解释为什么不选某条线，再看 `tables/boundary_catalog.csv`
4. 如果要找 generalized-supported peer 旁证，再看 `tables/stable_core_watchlist.csv`

默认阅读结论应该是：

- `A2` 是 default entry
- `A1` 是 hard mode / backup line
- `B1` 是 contrast-only
- `C1 / D1 / D2` 是 boundary 或 pathology evidence

## 安全边界

这一层允许做的是：

- readiness / routing / boundary analysis
- bucketed candidate selection
- conservative rationale aggregation
- PI / 老师可读的报告自动化

这一层不允许做的是：

- attack generation
- controller manipulation implementation
- exploit code
- closed-loop adversarial optimization
- 把 insight 直接转成可执行破坏能力
