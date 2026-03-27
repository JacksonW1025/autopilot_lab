# autopilot_lab

`autopilot_lab` 是当前的主研究仓库，用于承载 Flight Envelope Protection / PIO 前期实验。它把原先 PX4-only 的 `px4_ws` 工作区拆成了“共享研究层 + 两个 backend”：

- `px4_ros2_backend`
  - 保留原有 PX4 + ROS 2 + Gazebo 实验链路
- `ardupilot_mavlink_backend`
  - 新增 ArduPilot SITL + MAVLink 实验链路
- `fep_core`
  - 承载共享配置、profile、路径和 artifact 读写
- `fep_research`
  - 兼容包，继续暴露原有 `ros2 run fep_research ...` 入口

新仓库路径固定为：

- `/home/car/autopilot_lab -> /mnt/nvme/autopilot_lab`

旧 `/home/car/px4_ws` 保留为冻结基线，不再作为后续主开发仓。

## 当前状态

截至 `2026-03-27`，仓库已经完成以下迁移与验证：

- PX4 历史研究代码已迁入，并拆分为 `fep_core`、`px4_ros2_backend`、`fep_research`
- `reference/` 已整体迁入新仓
- 历史 PX4 artifacts 已迁入 `artifacts/px4/`
- ArduPilot MAVLink backend 已完成最小可运行闭环
- `colcon build` 已在新仓通过
- PX4 smoke 已跑通
- ArduPilot smoke 已跑通

当前 artifact 规模：

- `artifacts/px4/runs/`: `249`
- `artifacts/px4/analysis/`: `42`
- `artifacts/px4/matrix/`: `9`
- `artifacts/px4/identification/`: `5`
- `artifacts/ardupilot/runs/`: `4`

`artifacts/` 根目录下旧的兼容软链接已经移除；后续统一直接使用 `artifacts/px4/...` 与 `artifacts/ardupilot/...`。

## 工作区布局

```text
autopilot_lab/
├── artifacts/
│   ├── ardupilot/
│   └── px4/
├── reference/
├── scripts/
│   └── autopilot_lab_env.sh
└── src/
    ├── ardupilot_mavlink_backend/
    ├── fep_core/
    ├── fep_research/
    ├── px4_msgs/
    ├── px4_ros_com/
    └── px4_ros2_backend/
```

关键约定：

- `src/fep_core`
  - 后端无关逻辑
- `src/px4_ros2_backend`
  - PX4 专用实现
- `src/ardupilot_mavlink_backend`
  - ArduPilot 专用实现
- `src/fep_research`
  - 兼容入口，保证既有 PX4 命令不变

## 快速使用

先准备环境：

```bash
source /home/car/autopilot_lab/scripts/autopilot_lab_env.sh
```

PX4 工作流仍沿用原先方式：

```bash
MicroXRCEAgent udp4 -p 8888
cd /home/car/PX4-Autopilot
make px4_sitl gz_x500

ros2 run fep_research experiment_runner \
  --config /home/car/autopilot_lab/src/fep_research/config/baseline_roll.yaml
```

ArduPilot backend 默认通过外部 `/home/car/ardupilot` 启动 SITL：

```bash
ros2 run ardupilot_mavlink_backend ardupilot_experiment_runner \
  --config /home/car/autopilot_lab/src/fep_research/config/baseline_roll.yaml
```

如果只想检查命令是否安装成功：

```bash
ros2 run fep_research experiment_runner --help
ros2 run ardupilot_mavlink_backend ardupilot_experiment_runner --help
```

## 研究范围

当前仓库还不是最终保护器实现，而是一套科研实验平台。它主要回答两个问题：

1. 激进输入下，哪些观测量最先失真。
2. 系统从线性控制区走向危险包线边界时，边界如何出现、收缩和迁移。

PX4 侧已经形成从输入注入、在线观测、artifact 落盘到跨 run 分析和 identification 的 Phase 1-3 闭环。ArduPilot 侧目前的目标是先建立可比较的最小实验闭环，而不是立即复制 PX4 全量分析栈。

## 重点入口

- `TODO.md`
  - 当前阶段执行手册和门禁
- `PJINFO.md`
  - 项目背景、环境基线、当前状态
- `intro.md`
  - 面向导师/新读者的当前阶段说明
- `AGENTLOG.md`
  - 环境部署、迁移与验证日志
- `PHASE1_ATTITUDE_REPRO.md`
  - PX4 attitude 主链复现
- `PHASE1_MANUAL_REPRO.md`
  - PX4 manual 主链复现
- `PHASE2_REPRO.md`
  - PX4 监测与落盘流程
- `PHASE3_ANALYSIS_REPRO.md`
  - PX4 nominal / windy 汇总与边界分析

## 代表性产物

- PX4 nominal analysis:
  - `artifacts/px4/analysis/20260316_083659_phase3_nominal/`
- PX4 windy analysis:
  - `artifacts/px4/analysis/20260316_070303_phase3_windy/`
- PX4 identification:
  - `artifacts/px4/identification/20260316_083830_nominal_attitude_repeats/`
- PX4 新仓 smoke run:
  - `artifacts/px4/runs/20260326_225500_attitude_baseline_roll/`
- ArduPilot 新仓 smoke run:
  - `artifacts/ardupilot/runs/20260326_230029_attitude_baseline_roll/`

## 说明

- `src/fep_research` 现在是兼容层，不再承载主要实现。
- PX4 日志仍保留在 `/home/car/PX4-Autopilot/build/px4_sitl_default/rootfs/log/`。
- ArduPilot 固件仓仍保留在 `/home/car/ardupilot/`，不并入本 git 仓库。
- `scripts/autopilot_lab_env.sh` 会补齐构建和运行所需的 Python 依赖，并 source ROS 2 与本工作区环境。
