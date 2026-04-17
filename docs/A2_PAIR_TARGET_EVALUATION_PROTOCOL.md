# A2 Pair-Target 评估协议

## 目的

这份协议规定当前 A2 在 `pair_target_readiness` 之后、进入真实 live evaluation 之前应该怎么评估。

当前顺序固定为：

1. `GUIDED_NOGPS` smoke
2. A2 main capture 或复用已有 `runs.csv`
3. `a2_target_scout`
4. `a2_pair_target_readiness`
5. `a2_pair_target_algorithm_evaluation`
6. `a2_pair_target_live_evaluation`
7. `a2_pair_target_live_campaign`

其中第 5 步是 offline gate，第 6 步是单 phase live gate，第 7 步是 medium robustness 聚合 gate。它们都不替代 decision layer，也不替代 pair readiness。

## Source of Truth

当前 canonical reference 仍然是 `2026-04-17` 这批真实 A2 artifact：

- `artifacts/studies/20260417_001924_151397_ardupilot_a2_target_scout`
- `artifacts/studies/20260417_001925_356349_ardupilot_a2_pair_target_readiness`

如果未来 canonical A2 chain 刷新，这份协议继续成立，但 reference artifact 要一起更新。

## 评估对象

当前只评估：

- `GUIDED_NOGPS`
- `pair_imbalance_12_vs_34`
- `direction=12_gt_34`
- `strategy=reference_pulse_train_v1`
- `mode=offline_replay`

当前不评估：

- live closed-loop
- adaptive optimizer
- 新 target family
- A1 算法壳层

当前已实现的 live gate 只做最小受控执行，不做更复杂的闭环优化。
当前已经实现的 campaign 层负责把多个 phase 的 live 结果聚合成 narrative review。

## 评估输入

必须提供：

- `a2_target_scout` 目录
- `a2_pair_target_readiness` 目录
- `runs_manifest` 或可从上述 artifact manifest 推导出的 `runs_manifest`

可选参数：

- `scenario`
- `reference_tier`
- `direction`
- `pulse_amplitude`
- `bias`
- `pulse_count`
- `pulse_width_s`
- `pulse_gap_s`

## 评估输出

每次评估至少要落盘：

- `reports/a2_pair_target_algorithm_evaluation.md`
- `summary/a2_pair_target_algorithm_evaluation.json`
- `tables/scenario_evaluation_matrix.csv`
- `tables/run_level_reference_alignment.csv`
- `tables/generated_schedule.csv`
- `manifest.yaml`

## 判读流程

### 1. Artifact 一致性

先检查：

- `target_scout` 仍推荐 `GUIDED_NOGPS + pair_imbalance_12_vs_34`
- `pair_target_readiness` 仍为 `ready_for_pair_attack_v1=true`
- `pair_target_readiness` 的 `dominant_direction` 仍为 `12_gt_34`

这一步不通过，直接判为 hard regression。

### 2. 协议包络

再检查参数是否还在 canonical 安全包络内：

- `pulse_amplitude: 0.02 ~ 0.10`
- `bias: 0.00 ~ 0.04`
- `pulse_count: 1 ~ 5`
- `pulse_width_s: 0.20 ~ 0.50`
- `pulse_gap_s: 0.50 ~ 1.20`

超出包络，直接判为 hard regression。

### 3. Replay Coverage

对所选 `scenario_scope`，每个 scenario 都要满足：

- 有 source raw runs
- 有 accepted runs
- 所选 `reference_tier` 至少有一个 accepted replay source

coverage 不足，直接判为 hard regression。

### 4. Observed Metrics

离线 observed metrics 继续复用 pair readiness 的正式门槛：

- `active_pair_rate >= 0.15`
- `baseline_pair_rate <= 0.05`
- `specificity >= 0.12`
- `sign_consistency >= 0.90`
- `pair_to_collective_ratio >= 0.70`
- `tier_range_specificity <= 0.08`

任何 scenario 失守，都判为 hard regression。

### 5. Canonical 对比

如果 observed metrics 仍然过线，再和 canonical reference 做退化判断：

- `active_pair_rate` 相对下降超过 `10%`
- `specificity` 相对下降超过 `10%`
- `pair_to_collective_ratio` 相对下降超过 `10%`
- `tier_range_specificity` 绝对恶化超过 `0.02`

满足任一项，判为 soft regression。

## 输出解释

`overall_decision` 当前固定解释成：

- `offline_ready_for_live_eval_v1=true`
  - 没有 hard regression，可以继续准备 live eval
- `live_eval_required=true`
  - offline replay 不是终点，后续仍需要真实运行
- `hard_regression_detected=true`
  - 先修 artifact、协议或参数问题
- `soft_regression_detected=true`
  - 可以继续本地试验，但不应该升级成新的 canonical claim

`recommended_next_step` 只允许三种值：

- `hold_for_live_eval`
- `tighten_algorithm_spec`
- `fix_artifact_or_protocol_mismatch`

## Live Evaluation

当前 live runner 入口是：

```bash
/home/car/autopilot_lab/scripts/run_ardupilot_a2_pair_target_live_evaluation.sh \
  --a2-target-scout-dir /home/car/autopilot_lab/artifacts/studies/20260417_001924_151397_ardupilot_a2_target_scout \
  --a2-pair-target-dir /home/car/autopilot_lab/artifacts/studies/20260417_001925_356349_ardupilot_a2_pair_target_readiness \
  --a2-algorithm-eval-dir <algorithm_eval_dir>
```

它当前只支持：

- 读取既有 `algorithm_evaluation` 的参数
- 生成最小 pulse-train live capture
- 用 pair readiness 同一套门槛判读 live success
- 产出独立 `a2_pair_target_live_evaluation` study

它当前不会：

- 自动刷新 `next_phase_decision_layer`
- 自动把 live artifact 升格成新的 canonical claim

## Live Campaign

当前 live campaign 入口是：

```bash
/home/car/autopilot_lab/scripts/run_ardupilot_a2_pair_target_live_campaign.sh \
  --campaign-spec /home/car/autopilot_lab/configs/studies/ardupilot_a2_pair_target_live_campaign_medium_v1.yaml
```

它当前固定做四个 phase：

- `probe_stability_r1`
- `probe_stability_r2`
- `micro_robustness_r1`
- `confirm_robustness_r1`

并输出：

- `reports/a2_pair_target_live_campaign.md`
- `summary/a2_pair_target_live_campaign.json`
- `tables/campaign_phase_board.csv`
- `tables/campaign_scenario_board.csv`
- `tables/failure_taxonomy.csv`

它当前仍然不会自动进入 `next_phase_decision_layer`。

## 当前默认入口

```bash
/home/car/autopilot_lab/scripts/run_ardupilot_a2_pair_target_algorithm_evaluation.sh \
  --a2-target-scout-dir /home/car/autopilot_lab/artifacts/studies/20260417_001924_151397_ardupilot_a2_target_scout \
  --a2-pair-target-dir /home/car/autopilot_lab/artifacts/studies/20260417_001925_356349_ardupilot_a2_pair_target_readiness \
  --output-root /tmp/a2_algorithm_eval
```

## 与 decision layer 的关系

- 当前 `a2_pair_target_algorithm_evaluation` 不进入 `next_phase_decision_layer`。
- 当前 `a2_pair_target_live_evaluation` 也不进入 `next_phase_decision_layer`。
- 只有当 live evidence 连续稳定之后，才考虑把 live layer 升级成新的正式 route-selection 输入。
