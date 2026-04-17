# A2 Pair-Target Campaign Plan

## 目标

这轮 campaign 的目标不是扩大 search，也不是设计更复杂的算法，而是把 A2 变成一条可批量运行、可聚合、可讲故事的 live evidence 主线。

范围固定为：

- `canonical probe stability`
- `tier robustness`

当前不做：

- temporal robustness
- decision-layer 升级
- A1 对称 campaign

## Medium Robustness Campaign

当前 canonical campaign spec 是：

- config: `configs/studies/ardupilot_a2_pair_target_live_campaign_medium_v1.yaml`
- runner: `scripts/run_ardupilot_a2_pair_target_live_campaign.sh`

phase 顺序固定为：

1. `probe_stability_r1`
2. `probe_stability_r2`
3. `micro_robustness_r1`
4. `confirm_robustness_r1`

参数固定为：

- `probe_stability_r1`: `reference_tier=probe`, `pulse_amplitude=0.05`
- `probe_stability_r2`: `reference_tier=probe`, `pulse_amplitude=0.05`
- `micro_robustness_r1`: `reference_tier=micro`, `pulse_amplitude=0.02`
- `confirm_robustness_r1`: `reference_tier=confirm`, `pulse_amplitude=0.10`

所有 phase 共同固定：

- `scenario_scope=both`
- `direction=12_gt_34`
- `use_canonical_bias_by_scenario=true`
- `pulse_count=5`
- `pulse_width_s=0.35`
- `pulse_gap_s=0.95`
- `accepted_target=5`
- `max_attempts_per_config=10`

## 目标规模

- 4 个 phase
- 每个 phase 跑 `nominal + throttle_biased`
- 每个 scenario `accepted_target=5`
- 总 accepted live runs 目标约 `40`

## Campaign Pass 条件

campaign summary 只看这几项：

- `probe_stability_passed=true`
- `tier_robustness_passed=true`
- `dominant_direction_consistent=true`
- `hard_regression_detected=false`

只有同时满足这些条件，才把结果标成：

- `ready_for_live_evidence_review_v1=true`

## Failure Taxonomy

campaign 固定把失败归到下面几类：

- `preflight_artifact_mismatch`
- `smoke_gate_failure`
- `algorithm_eval_hard_regression`
- `algorithm_eval_soft_regression`
- `live_capture_failure`
- `live_direction_mismatch`
- `live_threshold_regression`
- `live_soft_regression`

## 输出

campaign study 固定输出：

- `reports/a2_pair_target_live_campaign.md`
- `summary/a2_pair_target_live_campaign.json`
- `tables/campaign_phase_board.csv`
- `tables/campaign_scenario_board.csv`
- `tables/failure_taxonomy.csv`
- `manifest.yaml`

## 推荐调用

离线路径：

```bash
/home/car/autopilot_lab/scripts/run_ardupilot_a2_pair_target_live_campaign.sh \
  --campaign-spec /home/car/autopilot_lab/configs/studies/ardupilot_a2_pair_target_live_campaign_medium_v1.yaml \
  --skip-smoke \
  --skip-capture \
  --output-root /tmp/a2_live_campaign
```

真实路径：

```bash
/home/car/autopilot_lab/scripts/run_ardupilot_a2_pair_target_live_campaign.sh \
  --campaign-spec /home/car/autopilot_lab/configs/studies/ardupilot_a2_pair_target_live_campaign_medium_v1.yaml \
  --output-root /home/car/autopilot_lab/artifacts/studies
```
