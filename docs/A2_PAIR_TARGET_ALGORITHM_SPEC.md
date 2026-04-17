# A2 Pair-Target 算法规格

## 目标

这份文档定义当前 A2 主线在进入真实 live evaluation 之前的最小算法接口。它不描述攻击成功逻辑，也不描述闭环控制器；它只回答：

- 当前 canonical target 是什么
- 算法壳层读什么输入
- 允许调什么参数
- 产出什么离线评估结果
- 什么情况下允许进入下一步 live evaluation

当前 canonical target 固定为：

- `flight_mode=GUIDED_NOGPS`
- `target_signal=pair_imbalance_12_vs_34`
- `dominant_direction=12_gt_34`

## 范围

当前只支持：

- `mode=offline_replay`
- `strategy=reference_pulse_train_v1`

当前明确不做：

- 实时闭环控制生成
- live attack success 判定
- decision layer 自动接入
- A1 对称算法壳层

## 输入

当前算法壳层固定读取四类输入：

1. `a2_target_scout` artifact
   作用：确认当前 canonical mode/target 仍然是 `GUIDED_NOGPS + pair_imbalance_12_vs_34`。
2. `a2_pair_target_readiness` artifact
   作用：确认当前 canonical direction、pair thresholds、scenario readiness 仍然成立。
3. `runs.csv`
   作用：给出 raw run 清单，供离线 replay/reference 对齐。
4. raw run manifests / telemetry
   作用：复用已有 A2 pair-target 指标提取逻辑，得到 run-level 和 scenario-level observed metrics。

如果 CLI 没显式给 `--runs-manifest`，实现会先从 `a2_pair_target_readiness/manifest.yaml` 取；取不到再从 `a2_target_scout/manifest.yaml` 取。

## 可控量

当前允许的参数只有这组 pulse-train family 参数：

- `scenario_scope`
  - `nominal`
  - `throttle_biased`
  - `both`
- `reference_tier`
  - `micro`
  - `probe`
  - `confirm`
- `direction`
  - 当前 canonical 只接受 `12_gt_34`
- `pulse_amplitude`
  - 当前安全包络：`0.02 ~ 0.10`
- `bias`
  - 当前安全包络：`0.00 ~ 0.04`
  - 如果不显式传，按 scenario 使用 canonical bias
- `pulse_count`
  - 当前安全包络：`1 ~ 5`
- `pulse_width_s`
  - 当前安全包络：`0.20 ~ 0.50`
- `pulse_gap_s`
  - 当前安全包络：`0.50 ~ 1.20`

当前 canonical 默认值：

- `reference_tier=probe`
- `pulse_amplitude=0.05`
- `pulse_count=5`
- `pulse_width_s=0.35`
- `pulse_gap_s=0.95`
- `bias.nominal=0.00`
- `bias.throttle_biased=0.04`

## 输出

当前算法壳层输出的是一个独立 narrowing study：

- `reports/a2_pair_target_algorithm_evaluation.md`
- `summary/a2_pair_target_algorithm_evaluation.json`
- `tables/scenario_evaluation_matrix.csv`
- `tables/run_level_reference_alignment.csv`
- `tables/generated_schedule.csv`
- `manifest.yaml`

其中：

- `generated_schedule.csv` 是算法参数落盘后的候选 schedule
- `run_level_reference_alignment.csv` 是 reference raw run 与 canonical direction/target 的对齐表
- `scenario_evaluation_matrix.csv` 是 scenario 级 observed metrics 与 regression 判读

## 成功判据

### `offline_ready_for_live_eval_v1`

满足下面条件时，算法壳层可以把结果标成 `offline_ready_for_live_eval_v1=true`：

- `a2_target_scout` 仍推荐 `GUIDED_NOGPS + pair_imbalance_12_vs_34`
- `a2_pair_target_readiness` 仍为 `ready_for_pair_attack_v1=true`
- `a2_pair_target_readiness` 的 `dominant_direction` 与算法参数一致
- 所选 `scenario_scope` 在 source runs 中都有 coverage
- 所选 `reference_tier` 在每个被选 scenario 下至少有 accepted replay source
- 参数没有超出当前 canonical 安全包络
- 没有 hard regression

### `live_pair_target_success_v1`

这是未来 live evaluation 的协议目标，不在这一轮实现。未来如果要宣称 live success，至少要同时满足：

- `active_pair_rate >= 0.15`
- `baseline_pair_rate <= 0.05`
- `specificity >= 0.12`
- `sign_consistency >= 0.90`
- `pair_to_collective_ratio >= 0.70`
- `tier_range_specificity <= 0.08`
- 两个 scenario 都保持 `direction=12_gt_34`

## Regression 口径

### Hard Regression

以下任一项成立，就视为 hard regression：

- `recommended_mode` 不是 `GUIDED_NOGPS`
- `recommended_next_target` 不是 `pair_imbalance_12_vs_34`
- `recommended_next_step` 不是 `guided_nogps_pair_target_readiness`
- `ready_for_pair_attack_v1` 不成立
- `recommended_path` 不是 `start_guided_nogps_pair_attack_v1`
- direction 不一致
- 所选 scenario 或 reference tier 没有 accepted coverage
- 参数超出安全包络
- observed scenario metrics 重新掉出 pair readiness 门槛

### Soft Regression

仍然过 threshold，但相对当前 canonical reference metrics 出现明显退化时，视为 soft regression：

- `active_pair_rate` 下降超过 `10%` 相对幅度
- `specificity` 下降超过 `10%` 相对幅度
- `pair_to_collective_ratio` 下降超过 `10%` 相对幅度
- `tier_range_specificity` 比 canonical 恶化超过 `0.02`

soft regression 不阻止本地继续做 offline iteration，但不应该拿去升级 decision layer 叙事。

## 中止条件与安全边界

以下情况必须直接停下，不继续讲 live 结论：

- 任一 source artifact 缺失
- `runs_manifest` 缺失
- `target_signal` 不再是 `pair_imbalance_12_vs_34`
- `flight_mode` 不再是 `GUIDED_NOGPS`
- `dominant_direction` 不再是 `12_gt_34`
- 试图把 `offline_replay` 结果直接解释成 live attack success

## 正式入口

Python 入口：

- `linearity_analysis.ardupilot_a2_pair_target_algorithm_evaluation:main`

Shell 入口：

- `scripts/run_ardupilot_a2_pair_target_algorithm_evaluation.sh`
- `scripts/run_ardupilot_a2_pair_target_live_evaluation.sh`
- `scripts/run_ardupilot_a2_pair_target_live_campaign.sh`

推荐调用：

```bash
/home/car/autopilot_lab/scripts/run_ardupilot_a2_pair_target_algorithm_evaluation.sh \
  --a2-target-scout-dir /home/car/autopilot_lab/artifacts/studies/20260417_001924_151397_ardupilot_a2_target_scout \
  --a2-pair-target-dir /home/car/autopilot_lab/artifacts/studies/20260417_001925_356349_ardupilot_a2_pair_target_readiness \
  --output-root /tmp/a2_algorithm_eval
```

## 口径说明

- 当前算法评估 study 是独立 report，不是新的 canonical decision input。
- 当前 decision layer 仍只消费既有 A1 / A2 narrowing 结论，不消费 `algorithm_evaluation`。
- 当前 `live_evaluation` 和 `live_campaign` 只消费这里定义好的参数接口，不扩展新的控制策略族。
- 这份规格的作用是把 A2 从“readiness 已成立”推进到“有一个可复现、可审计、可比较的算法评估壳层和 live evidence 入口”。
