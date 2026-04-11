# Experiment Protocol

## 当前正式实验线

当前仓库的正式结论，已经切换到 `generalization full` 这条实验线。

它的目标不是再问一次“线性关系是否存在”，而是更进一步回答：

> 在统一 schema 口径下，同一类线性映射 `f` 是否能在 `nominal / dynamic / throttle_biased` 三档状态下继续成立？

## 当前正式顺序

这条线已经按下面顺序完整落地：

### PX4

1. `scripts/run_px4_generalization_pilot.sh`
   - baseline pilot：`2 modes × 3 scenarios × 3 accepted`
   - diagnostic pilot：控制组 sweep + 扩展 throttle / random 动作
2. `scripts/run_px4_generalization_full.sh`
   - baseline full：`2 modes × 3 scenarios × 5 accepted`
   - diagnostic full：完整 generalization diagnostic

### ArduPilot

1. `scripts/run_ardupilot_generalization_pilot.sh`
   - baseline pilot：`2 modes × 3 scenarios × 3 accepted`
   - diagnostic pilot：镜像 PX4 的同名 scenario 与 profile 家族
2. `scripts/run_ardupilot_generalization_full.sh`
   - baseline full：`2 modes × 3 scenarios × 5 accepted`
   - diagnostic full：完整 generalization diagnostic

## 历史完成项

以下内容仍保留，但现在是历史阶段，不再是当前正式 compare 的主输入：

- `20260409` 的 broad baseline / diagnostic
- ArduPilot `GUIDED_NOGPS` smoke
- `STABILIZE` partial baseline
- `STABILIZE` throttle-only diagnostic
- cross-backend contract audit

这些内容仍然重要，因为它们证明了：

- mode-entry 已经打通；
- throttle gate 已经打通；
- 两个 backend 的 manifest / acceptance / sample table / schema naming 契约一致。

## 统一分析口径

PX4 和 ArduPilot 的正式 generalization analysis 使用同一套：

- `x_schemas`
- `y_schemas`
- `models`
- `pooling_modes`
- `history_length`
- `prediction_horizon`
- sparsity / stability / reporting 参数

backend 差异只允许出现在：

- raw capture 能提供哪些列
- 哪些 run 被 acceptance gate 拒收

backend 差异不允许体现在：

- schema 名称
- analysis 口径
- 报告结构

## Acceptance 与研究层级

- baseline 以“每个 `mode × scenario` 达到目标 accepted run 数”为准，不以 attempts 数代替。
- demo / smoke / partial baseline / throttle-only diagnostic 作为支持性证据保留，但当前正式线性结论来自 generalization full。
- raw run 是否能进入正式分析，仍取决于统一的 `data_quality.acceptance`：
  - `experiment_started`
  - `active_phase_present`
  - `active_nonzero_command_samples`
  - `failsafe_during_experiment`
  - `missing_topics_blocking`

## 当前正式输出物

每个 generalization full study 至少要输出：

- `matrix_f.csv`
- `bias_b.csv`
- `sparsity_mask.csv`
- `metrics.json`
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

## 当前结论口径

- `supported`
  当前 study 中已经得到可接受的线性 `f`
- `generalized_supported`
  当前 `supported` 结果在三档 scenario 下仍然稳定成立
- `supported_but_local`
  当前结果只更像局部 operating-point 映射
- `not_generalized`
  当前还不能把它当成跨状态常见映射

当前正式结论层同时看两件事：

1. 线性关系是否存在；
2. 它是否能跨 scenario 保持 generalized-supported。
