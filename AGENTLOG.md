# AGENTLOG.md

## 目标

围绕 `Y ≈ fX (+ b)` 构建一个可持续推进的无人机全局线性研究平台。当前唯一正式主线是：

- 采集真实或仿真 raw run
- 在统一 `X / Y schema` 下构造样本
- 拟合全局线性/仿射矩阵 `f`
- 用稀疏性、稳定性、泛化表现判断该 `f` 是否可接受
- 用 PX4 与 ArduPilot 的相似性增强结论，而不是把研究写成 backend 竞赛

## 2026-04-06

- 建立 `linearity_core / linearity_study / linearity_analysis` 三层结构
- 统一 study config、sample table、fit artifact、study summary 的输出口径
- 建立基础 synthetic smoke 与测试集

## 2026-04-07

- 固定 PX4 正式 scope：`gz_x500/default + nominal + POSCTL/OFFBOARD_ATTITUDE`
- 建立 PX4 真实 capture、analysis、broad ablation 链路
- PX4 raw capture 支持 `ROS 直录 + ULog 缺口回填`
- 条件数诊断拆分为 `raw_condition_number` 与 `effective_condition_number`

## 2026-04-09

### 仓库主线收敛

- 删除旧阶段报告、旧 generic/public study configs
- 删除旧的 backendless 入口与 smoke 入口
- README / PJINFO / lab.lock 统一改到当前正式实验主线

### Artifact 与契约冻结

- 冻结 raw/study contract：`manifest`、`data_quality.acceptance`、prepared sample table 身份列、X/Y schema naming 跨 backend 对齐
- 新增稳定输出：
  - `reports/baseline_stability.md`
  - `reports/diagnostic_gate.md`
  - `reports/matrix_gallery.md`
- supported 组合现在会自动生成 `matrix_heatmap_abs.png` 与 `matrix_heatmap_signed.png`

### ArduPilot 正式接入

- ArduPilot 可视化默认改为 best-effort `MAVProxy --console --map`
- `GUIDED_ATTITUDE` 统一改名为 `GUIDED_NOGPS`
- 新增 `GUIDED_NOGPS` smoke、`STABILIZE` partial baseline、`STABILIZE` throttle diagnostic、contract audit、formal compare 链路

### PX4 live 修复

- 定位 PX4 POSCTL live blocker：OFFBOARD setpoint 会因时基问题出现秒级断流
- 注入器 timer 改为显式 `SYSTEM_TIME`
- 修复后最小 POSCTL smoke 恢复 accepted，`input_trace` 最大间隔回到约 `0.0558s`
- 修复后 PX4 authoritative baseline raw capture 已重新达到：
  - `POSCTL = 5 accepted`
  - `OFFBOARD_ATTITUDE = 5 accepted`

## 2026-04-11

### Generalization Full 收口

- 完成 PX4 generalization full：
  - baseline
  - diagnostic
- 完成 ArduPilot generalization full：
  - baseline
  - diagnostic
- canonical compare 已切到 latest generalization full 四个 study
- 当前正式主文档与附录已全部刷新到 generalization 线

## 当前重点

- 保持 canonical artifact、README、PJINFO 与 docs 同步
- 优先清理 superseded artifact 与临时日志，保持仓库精简
- 后续如果继续扩实验，优先读透 generalized-supported 组合的 `matrix_f` 热力图，而不是盲目继续扩 schema
