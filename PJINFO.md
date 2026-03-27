# PJINFO.md (Project Information)

> 每次运行 Agent 必读；每次 work 完成后更新【自动】部分。  
> 当前仓库以 `autopilot_lab` 为准，旧 `px4_ws` 仅作冻结参考。

## 项目背景（【手动】）

- **核心目标**：基于 PX4 与 ArduPilot 两套飞控仿真链路，开展博士阶段关于 **Flight Envelope Protection (FEP)** 与 **Pilot-Induced Oscillation (PIO)** 的前期实验研究。
- **研究范围**：激进输入下的包线边界识别、失效前兆观测、sample-level identification，以及面向 Jetson 平台的后续安全监控与干预接口。
- **当前策略**：先建立共享研究层，再分别保留 `px4_ros2_backend` 与 `ardupilot_mavlink_backend`，避免把 ArduPilot 强行塞进 PX4 ROS 2 假设中。

## 硬件环境（【手动】）

- **计算平台**：NVIDIA Jetson AGX Orin 64G
- **性能模式**：MAXN (Mode 0) + Jetson Clocks
- **外部设备**：当前以 SITL 为主，实机链路后续单独规划

## 软件环境（【手动】）

- **操作系统**：Ubuntu 22.04 aarch64
- **NVMe 挂载点**：`/mnt/nvme`
- **主研究仓库**：`/home/car/autopilot_lab -> /mnt/nvme/autopilot_lab`
- **旧 PX4 工作区**：`/home/car/px4_ws`
- **PX4 固件仓库**：`/home/car/PX4-Autopilot -> /mnt/nvme/px4_work/PX4-Autopilot`
- **ArduPilot 固件仓库**：`/home/car/ardupilot -> /mnt/nvme/UAVFuzzing/ardupilot-home`
- **Micro XRCE-DDS Agent**：`/home/car/Micro-XRCE-DDS-Agent -> /mnt/nvme/px4_work/Micro-XRCE-DDS-Agent`
- **ROS 2**：Humble
- **Gazebo**：Harmonic `8.10.0`

## 项目结构（【自动】常更新）

- **关键路径**：
  - `~/autopilot_lab/`：当前主工作仓库
  - `~/autopilot_lab/src/`：并列包根目录
  - `~/autopilot_lab/reference/`：参考资料与阶段总结
  - `~/autopilot_lab/artifacts/px4/`：PX4 历史与新增结果
  - `~/autopilot_lab/artifacts/ardupilot/`：ArduPilot 结果
  - `~/PX4-Autopilot/`：PX4 固件树
  - `~/ardupilot/`：ArduPilot 固件树
- **主要包**：
  - `fep_core`：共享配置、路径、profile、artifact I/O
  - `px4_ros2_backend`：PX4 ROS 2 专用实现
  - `ardupilot_mavlink_backend`：ArduPilot MAVLink 专用实现
  - `fep_research`：兼容包，继续暴露既有 PX4 CLI
  - `px4_msgs` / `px4_ros_com`：PX4 官方消息与示例包

## 当前状态（【自动】每次 work 后更新）

- **仓库层面**：
  - [2026-03-26] 已新建独立 git 仓库 `autopilot_lab`
  - [2026-03-26] 已建立 `/home/car/autopilot_lab -> /mnt/nvme/autopilot_lab`
  - [2026-03-26] 旧 `/home/car/px4_ws` 已保留为冻结基线，不回写
  - [2026-03-26] `reference/` 与历史 PX4 artifacts 已迁入新仓
  - [2026-03-27] `artifacts/` 根目录下旧兼容软链接已移除，后续统一使用 `artifacts/px4/...` 与 `artifacts/ardupilot/...`
- **代码层面**：
  - [2026-03-26] 已抽出 `fep_core`
  - [2026-03-26] 已建立 `px4_ros2_backend`
  - [2026-03-26] 已建立 `ardupilot_mavlink_backend`
  - [2026-03-26] `fep_research` 已降为兼容层，继续保持 `ros2 run fep_research ...` 入口
  - [2026-03-26] 代码和文档中的旧工作区硬编码已清理到新路径口径
- **PX4 状态**：
  - [2026-03-26] PX4 历史 runs 已迁入 `artifacts/px4/runs/`，当前共 `249` 组目录
  - [2026-03-26] PX4 历史 analysis 已迁入 `artifacts/px4/analysis/`，当前共 `42` 组目录
  - [2026-03-26] PX4 历史 matrix 已迁入 `artifacts/px4/matrix/`，当前共 `9` 组目录
  - [2026-03-26] PX4 历史 identification 已迁入 `artifacts/px4/identification/`，当前共 `5` 组目录
  - [2026-03-26] 新仓 PX4 smoke 已跑通；代表性 run 为 `artifacts/px4/runs/20260326_225500_attitude_baseline_roll/`
- **ArduPilot 状态**：
  - [2026-03-26] 已打通 `sim_vehicle.py + pymavlink` 的最小实验闭环
  - [2026-03-26] 已实现 `ardupilot_experiment_runner`
  - [2026-03-26] 已实现 `ardupilot_matrix_runner`
  - [2026-03-26] 已实现 `ardupilot_log_backfill`
  - [2026-03-26] ArduPilot smoke 已跑通；代表性 run 为 `artifacts/ardupilot/runs/20260326_230029_attitude_baseline_roll/`
- **构建与环境**：
  - [2026-03-26] `colcon build --packages-up-to fep_core px4_ros2_backend fep_research ardupilot_mavlink_backend px4_msgs px4_ros_com` 已通过
  - [2026-03-26] 已新增 `scripts/autopilot_lab_env.sh` 用于统一 Python 依赖和 workspace 环境
  - [2026-03-26] ROS Humble 消息生成链当前要求用户态 `empy<4`
- **当前缺口**：
  - ArduPilot backend 目前只具备最小 run / matrix / backfill 能力，还没有 PX4 等价的 Phase 3 分析深度
  - ArduPilot 仍未对齐 PX4 的 ULog 级 failure attribution 与 identification
  - 双 backend 的严格对比实验还需要进一步统一指标口径

## 重要命令（【只增不删】）

### 统一环境

```bash
source /home/car/autopilot_lab/scripts/autopilot_lab_env.sh
```

### PX4

```bash
MicroXRCEAgent udp4 -p 8888
cd /home/car/PX4-Autopilot
make px4_sitl gz_x500
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/baseline_roll.yaml
```

### ArduPilot

```bash
ros2 run ardupilot_mavlink_backend ardupilot_experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/baseline_roll.yaml
```

### 验证命令是否已安装

```bash
ros2 run fep_research experiment_runner --help
ros2 run ardupilot_mavlink_backend ardupilot_experiment_runner --help
```

## 设计原则（【手动】）

- 优先保持 PX4 现有工作流稳定，再扩 ArduPilot
- 共享逻辑进入 `fep_core`，backend 专有逻辑不要回流污染共享层
- 没有充分证据时，不要把 PX4 的结论直接外推到 ArduPilot 或实机
- 代码和文档统一使用新仓库路径，不再引入 `px4_ws` 新依赖

## 其它注意事项（【手动】）

- 与用户交互时使用简体中文，专业名称保持英文
- 非必要不要使用 sudo
- 如果遇到连续失败，优先停下来汇报真实 blocker
