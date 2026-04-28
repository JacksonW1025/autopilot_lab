# Stage 1 Summary

## 目标

Stage 1 的目标是给出真实实验层面的正面证据，证明在统一 `X/Y` schema 下存在稳定线性或仿射映射：

`Y ≈ fX (+ b)`

这里的 `f` 被解释为输入到响应的稀疏导数矩阵。Stage 1 只回答“这种矩阵是否存在并跨场景复现”，不回答“哪条线应该被升级成后续执行主线”。

## Canonical Study Board

| artifact | backend | accepted runs | generalized_supported | canonical representative combo |
| --- | --- | ---: | ---: | --- |
| `20260410_224818_px4_real_generalization_ablation` | PX4 | 30 | 80 | `full_augmented -> next_raw_state -> ols_affine -> stratified` |
| `20260411_021910_px4_generalization_diagnostic_matrix` | PX4 | 48 | 111 | `full_augmented -> next_raw_state -> ols_affine -> stratified` |
| `20260413_070802_ardupilot_real_generalization_ablation` | ArduPilot | 30 | 12 | `commands_only -> actuator_response -> ridge_affine -> pooled` |
| `20260413_091420_ardupilot_generalization_diagnostic_matrix` | ArduPilot | 48 | 12 | `commands_only -> actuator_response -> ridge_affine -> pooled` |

## 关键观察

### PX4

- retained evidence 更宽
- canonical structure 是 state-dominated propagation
- representative combo 为 `full_augmented -> next_raw_state -> ols_affine -> stratified`

### ArduPilot

- retained evidence 更窄，但 direct mapping 更干净
- canonical structure 是 command-to-actuator direct transport
- representative combo 为 `commands_only -> actuator_response -> ridge_affine -> pooled`

## Stage 1 结论

- `Y ≈ fX (+ b)` 在 PX4 与 ArduPilot 上都得到了正面 evidence。
- 这些 evidence 不是单场景偶然拟合，而是在 `nominal / dynamic / throttle_biased` 下重复出现。
- Stage 1 给出了两类重要结构线索：
  - PX4 偏向 state propagation
  - ArduPilot 偏向 direct transport

## Stage 1 的边界

Stage 1 不负责回答下面的问题：

- 如何把 retained evidence 统一组织成六线共同成因
- leakage、conditioning 和 regime shift 怎样决定边界
- 后续统一算法应如何定义 kernel、target bundle 和 regularization

这些问题由新的 Stage 2 接手。

## 下一步

新的 Stage 2 统一解释六个机制代号：

- `PX-STC`
- `PX-STD`
- `AP-DAB`
- `AP-HTM`
- `AP-HTS`
- `AP-HTG`

继续阅读：

1. `README.md`
2. `docs/v1/STAGE2_SUMMARY_v1.md`
