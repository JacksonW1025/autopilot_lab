# autopilot_lab

`autopilot_lab` 当前只保留两段正式研究链：

`sparsity hypothesis -> empirical validation -> stage-2 common-cause synthesis`

## Source Of Truth

当前 repo-level canonical 文档只有三份：

1. `README.md`
2. `docs/STAGE1_SUMMARY.md`
3. `docs/STAGE2_SUMMARY.md`

## 当前保留范围

- Stage 1：四个 generalization study，负责证明 `Y ≈ fX (+ b)` 在 PX4 与 ArduPilot 上都存在可重复的线性证据。
- Stage 2：一个六线共同成因 study，负责把机制证据组织成统一的机制账本、类比结构和 `USDTA` 设计约束。

## Stage 1

当前保留的 Stage 1 artifact：

1. `artifacts/studies/20260410_224818_px4_real_generalization_ablation`
2. `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`
3. `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation`
4. `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix`

当前关键数字：

- PX4 baseline `accepted_run_count = 30`, `generalized_supported = 80`
- PX4 diagnostic `accepted_run_count = 48`, `generalized_supported = 111`
- ArduPilot baseline `accepted_run_count = 30`, `generalized_supported = 12`
- ArduPilot diagnostic `accepted_run_count = 48`, `generalized_supported = 12`

## Stage 2

当前 Stage 2 把六条机制线组织成六个带仿真器信息的机制代号：

- `PX-STC`: PX4 State Transport Continuation
- `PX-STD`: PX4 State Transport Differential
- `AP-DAB`: ArduPilot Direct Actuator Bundle
- `AP-HTM`: ArduPilot History Transport MixedMode
- `AP-HTS`: ArduPilot History Transport STABILIZE
- `AP-HTG`: ArduPilot History Transport GUIDED_NOGPS

当前 canonical Stage 2 study：

- `artifacts/studies/20260421_090255_stage2_six_line_common_cause_analysis`

新的 Stage 2 只回答三类问题：

- 哪些低维 `X` 子空间稳定映射到紧凑 `Y` bundle
- 哪些 `state / direct / history transport` 机制在不同 backend 与 regime 中复现
- 哪些边界真正由 leakage、conditioning 与 regime shift 主导

它直接导出 `USDTA` 的设计约束。

## 当前结论

- `Y ≈ fX (+ b)` 的 empirical validation 已成立。
- 六条机制线现在按统一代号组织。
- `PX-STC/PX-STD` 共同定义 PX4 的 state-transport 家族。
- `AP-DAB` 是 ArduPilot 的 direct-transport 实例。
- `AP-HTM/AP-HTS/AP-HTG` 共同定义 history-transport 家族，其中边界主要由 conditioning、mask collapse 和 regime split 决定。
- 当前 Stage 2 的目标是为统一算法 `USDTA` 提供设计指导。

## 阅读顺序

1. `README.md`
2. `docs/STAGE1_SUMMARY.md`
3. `docs/STAGE2_SUMMARY.md`
4. `artifacts/studies/20260421_090255_stage2_six_line_common_cause_analysis/reports/stage2_six_line_common_cause.md`

## 正式入口

Stage 1：

- `scripts/run_px4_generalization_full.sh`
- `scripts/run_ardupilot_generalization_full.sh`
- `scripts/visualize_fit_matrices.py`

Stage 2：

- `scripts/analyze_stage2_six_line_common_cause.py`

## 目录

- `artifacts/studies/`: 正式 study artifact
- `configs/`: Stage 1 retained config
- `docs/`: Stage 1/Stage 2 canonical summary
- `scripts/`: 当前正式入口
- `src/`: retained analysis code
- `tests/`: 保留后的最小回归集
