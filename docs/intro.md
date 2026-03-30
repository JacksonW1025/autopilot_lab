# autopilot_lab 项目简介与当前实验状况

## 1. 当前状态

`autopilot_lab` 现在的主口径是 `Dual-Backend M1` 分层实验平台：

- backend：PX4 + ArduPilot
- 主能力：`manual_whole_loop`、`attitude_explicit`、`rate_single_loop`
- 主特征：bootstrap、doctor、fresh matrix、strict study analysis、legacy 隔离

截至 `2026-03-30`，当前已完成真实 M1 验收闭环：

- `doctor_lab.sh` 已 ready
- 双 backend canonical roll smoke 已真跑通过
- 本轮 12 个新 run 已全部进入 accepted
- 最小 CI `scripts/ci_minimal.sh` 已通过

当前权威状态页：

- `docs/M1_STATUS.md`

## 2. 新仓与旧仓关系

- 主开发仓：`/home/car/autopilot_lab -> /mnt/nvme/autopilot_lab`
- 旧冻结仓：`/home/car/px4_ws`

后续开发只在 `autopilot_lab` 上继续推进；`px4_ws` 保持冻结。

## 3. M1 已补齐的关键点

### 3.1 环境与入口

- 新增 `milestone.lock.json`
- 新增 `scripts/bootstrap_lab.sh`
- 新增 `scripts/doctor_lab.sh`
- 新增 `scripts/smoke_lab.sh`
- 新增 `scripts/ci_minimal.sh`
- 默认入口切到 backend-native CLI

### 3.2 运行与实验层

- PX4 `rate_single_loop` 已从占位分支补成可运行主能力
- ArduPilot matrix 已支持 `repeat`、`session_dir` 和 fresh session lifecycle
- PX4 / ArduPilot 的新 run 都写入统一里程碑元数据

### 3.3 汇总与可信性层

- `study_analysis_runner` 默认只接收当前里程碑 `accepted` runs
- 历史 runs 默认被标记为 `legacy`
- schema 不完整的新 runs 会被标为 `rejected`
- 新汇总默认输出 `accepted_runs.csv` 和 `rejected_runs.csv`

## 4. 当前可信结论

截至 `2026-03-30`，现在可以明确说：

- PX4 与 ArduPilot 都已经纳入同一套分层 study 口径
- `manual / attitude / rate` 三层都已在 roll canonical smoke 上完成双 backend 验证
- 主汇总默认不会再把旧 schema runs 静默混入当前结论
- 最新 smoke 的 12 个新 run 过滤后 `accepted=12`、`rejected=0`
- 全仓最新 study manifest 计数为 `accepted=39`、`legacy=253`、`rejected=20`，这是汇总口径，不是这轮 smoke 的失败数
- 当前环境已经达到一个可用于论文实验初步环境建设的里程碑

## 5. 仍需记住的边界

- 历史 artifacts 仍然存在，而且默认被隔离为 `legacy`
- M1 的 canonical smoke 只锁定 `roll` 轴
- 当前研究扩展顺序是先补 pitch，再做 yaw/composite
- `fep_research` 仍保留兼容入口，但不再是默认前门

## 6. 推荐使用方式

首次环境准备：

```bash
/home/car/autopilot_lab/scripts/bootstrap_lab.sh
/home/car/autopilot_lab/scripts/doctor_lab.sh
```

统一 smoke：

```bash
/home/car/autopilot_lab/scripts/smoke_lab.sh --backend all --repeat 1
```

最小 CI：

```bash
/home/car/autopilot_lab/scripts/ci_minimal.sh
```

严格汇总：

```bash
ros2 run fep_core study_analysis_runner
```
