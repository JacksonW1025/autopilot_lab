# autopilot_lab

`autopilot_lab` 是一个围绕无人机输入到响应关系的研究仓库。仓库当前只保留一条中心叙事：

`sparsity hypothesis -> empirical validation -> in-depth analysis -> novel attack algorithm -> evaluation`

这里的核心对象是矩阵 `f`。项目把它看作输入到响应的稀疏导数矩阵，并围绕这张矩阵回答两个问题：

1. 这类固定线性映射是否真实存在。
2. 这类映射里哪些稀疏结构足够稳定，能够支撑后续攻击算法。

## 当前仓库保留了什么

仓库当前只保留三类内容：

- 能直接证明 stage 1 和 stage 2 结论的 study artifact
- 能把 stage 2 insight 推进到 A2 算法与评估的脚本和源码
- 能帮助快速进入项目状态的三份总结文档

当前阅读入口：

1. [docs/STAGE1_SUMMARY.md](docs/STAGE1_SUMMARY.md)
2. [docs/STAGE2_SUMMARY.md](docs/STAGE2_SUMMARY.md)
3. [docs/REMATCH.md](docs/REMATCH.md)

## 五个阶段现在分别做了什么

### 1. Sparsity Hypothesis

项目的理论起点是：`f` 不是任意稠密矩阵，真正有解释力的结构会表现为稀疏、稳定、低维的导数模式。这个假设决定了后续所有实验的判读方式。

### 2. Empirical Validation

这一阶段使用 PX4 与 ArduPilot 两套 backend，在统一 `X/Y` 口径下验证固定线性映射是否存在，并检查它是否能跨 `nominal / dynamic / throttle_biased` 三种场景成立。当前保留的主证据是四个 generalization study。

### 3. In-Depth Analysis

这一阶段不再停留在“能拟合”，而是继续追问“什么结构可信，什么结构只是高分假象”。当前保留的主证据是 mode-isolated state-evolution study、anchor deep dive 和 in-depth synthesis。

### 4. Novel Attack Algorithm

这一阶段把 stage 2 的结构结论收敛成一个可执行的攻击目标。当前仓库保留的是 A2 主线，目标已经锁定为：

- `GUIDED_NOGPS`
- `pair_imbalance_12_vs_34`
- `12_gt_34`

### 5. Evaluation

这一阶段对 A2 做 bounded repeatability 与 live evaluation。当前保留的结论是：full-window baseline 被排除，penultimate-window confirm protocol 形成了受边界约束的正面执行证据，widened pulse family 仍然处于边界之外。

## 当前结论的最短版本

- `Y ≈ fX (+ b)` 已经得到正面 empirical validation。
- PX4 的稳定结构偏向 state-dominated 的短时传播。
- ArduPilot 的稳定结构偏向 commands-only 的低维 direct-control。
- A2 是当前最适合继续推进的攻击主线。
- 当前 evaluation claim 只覆盖经过审查的 penultimate-window confirm protocol。

## 目录结构

```text
autopilot_lab/
├── AGENT.md
├── README.md
├── artifacts/
│   └── studies/
├── configs/
├── docs/
│   ├── STAGE1_SUMMARY.md
│   ├── STAGE2_SUMMARY.md
│   └── REMATCH.md
├── scripts/
├── src/
└── tests/
```

目录说明：

- `artifacts/studies/`：正式证据目录。每个 study 都是一个可直接引用的阶段证据。
- `configs/`：实验与分析配置。
- `scripts/`：正式实验入口。
- `src/`：拟合、分析、backend runner 和 A2 评估逻辑。
- `tests/`：保留后的最小回归集。

## 推荐阅读顺序

如果只想快速理解仓库状态，按下面顺序阅读：

1. [docs/STAGE1_SUMMARY.md](docs/STAGE1_SUMMARY.md)
2. [docs/STAGE2_SUMMARY.md](docs/STAGE2_SUMMARY.md)
3. [docs/REMATCH.md](docs/REMATCH.md)

如果要直接看 artifact：

1. `artifacts/studies/20260410_224818_px4_real_generalization_ablation`
2. `artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`
3. `artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation`
4. `artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix`
5. `artifacts/studies/20260413_134505_ardupilot_state_evolution_validation`
6. `artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive`
7. `artifacts/studies/20260414_064902_formal_v2_in_depth_analysis`
8. `artifacts/studies/20260417_001924_151397_ardupilot_a2_target_scout`
9. `artifacts/studies/20260417_001925_356349_ardupilot_a2_pair_target_readiness`
10. `artifacts/studies/20260417_122519_536215_ardupilot_a2_pair_target_bounded_repeatability_campaign`
11. `artifacts/studies/20260417_122644_564567_ardupilot_a2_pair_target_bounded_repeatability_campaign`
12. `artifacts/studies/20260417_122621_661226_ardupilot_a2_pair_target_live_evaluation`
13. `artifacts/studies/20260417_122622_852971_ardupilot_a2_pair_target_live_evaluation`
14. `artifacts/studies/20260417_122623_985857_ardupilot_a2_pair_target_live_evaluation`
15. `artifacts/studies/20260417_122625_153113_ardupilot_a2_pair_target_live_evaluation`
16. `artifacts/studies/20260417_122626_326415_ardupilot_a2_pair_target_live_evaluation`
17. `artifacts/studies/20260417_122627_505610_ardupilot_a2_pair_target_live_evaluation`

## 正式入口

Stage 1:

- `scripts/run_px4_generalization_full.sh`
- `scripts/run_ardupilot_generalization_full.sh`

Stage 2:

- `scripts/run_ardupilot_state_evolution_validation_full.sh`
- `scripts/analyze_anchor_deep_dive.py`
- `scripts/analyze_formal_v2_in_depth.py`

A2:

- `scripts/run_ardupilot_a2_target_scout.sh`
- `scripts/run_ardupilot_a2_guided_nogps_pair_target_readiness.sh`
- `scripts/run_ardupilot_a2_pair_target_algorithm_evaluation.sh`
- `scripts/run_ardupilot_a2_pair_target_bounded_repeatability_campaign.sh`
- `scripts/run_ardupilot_a2_pair_target_live_evaluation.sh`
- `scripts/run_ardupilot_a2_pair_target_live_campaign.sh`
