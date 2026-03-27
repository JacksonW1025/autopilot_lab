# autopilot_lab 部署与迁移日志

## 概述

- **目标平台**: Jetson AGX Orin 64G
- **操作系统**: Ubuntu 22.04 aarch64
- **主工作仓库**: `/home/car/autopilot_lab -> /mnt/nvme/autopilot_lab`
- **PX4 固件仓库**: `/home/car/PX4-Autopilot -> /mnt/nvme/px4_work/PX4-Autopilot`
- **ArduPilot 固件仓库**: `/home/car/ardupilot -> /mnt/nvme/UAVFuzzing/ardupilot-home`
- **旧 PX4 工作区**: `/home/car/px4_ws`，保留为冻结基线
- **最后更新**: `2026-03-27`

## 基础环境

### 存储布局

- NVMe 挂载点: `/mnt/nvme`
- 主研究仓: `/mnt/nvme/autopilot_lab`
- PX4 固件: `/mnt/nvme/px4_work/PX4-Autopilot`
- ArduPilot 固件: `/mnt/nvme/UAVFuzzing/ardupilot-home`

### 已验证组件

- Gazebo Harmonic `8.10.0`
- ROS 2 Humble
- `ros-humble-ros-gz`
- PX4 Autopilot `v1.15`
- Micro XRCE-DDS Agent
- ArduPilot SITL + `sim_vehicle.py`

## 2026-03-08 基础环境搭建

- 完成 ROS 2 Humble、Gazebo Harmonic、PX4 v1.15、Micro XRCE-DDS Agent 的安装与编译
- 完成 NVMe 挂载与工作目录迁移
- 验证 `MicroXRCEAgent`、PX4 SITL 与 Gazebo GUI 可正常运行

## 2026-03-10 至 2026-03-16 PX4 研究流水线

- 建立 `fep_research` 研究包和 `TODO.md`
- 打通 attitude / manual 两条输入链
- 固化 Phase 1-3 artifact 结构
- 完成 nominal / windy 汇总分析与 identification 数据导出
- 形成 PX4 历史 artifacts 基线：
  - `runs`: 249
  - `analysis`: 42
  - `matrix`: 9
  - `identification`: 5

## 2026-03-26 至 2026-03-27 双 backend 迁移

### 目录与仓库调整

- 新建独立 git 仓库 `/mnt/nvme/autopilot_lab`
- 建立软链接 `/home/car/autopilot_lab -> /mnt/nvme/autopilot_lab`
- 旧 `/home/car/px4_ws` 保留，不回写
- `reference/` 和历史 PX4 artifacts 完整迁入新仓
- `artifacts/` 统一改为：
  - `artifacts/px4/`
  - `artifacts/ardupilot/`
- 根目录下旧兼容软链接已移除

### 代码结构调整

- 新增 `src/fep_core`
  - 共享配置、路径、profile、artifact I/O
- 新增 `src/px4_ros2_backend`
  - PX4 ROS 2 专用实现
- 新增 `src/ardupilot_mavlink_backend`
  - ArduPilot MAVLink 专用实现
- 保留 `src/fep_research`
  - 兼容层，继续暴露 PX4 既有 CLI
- 保留顶层 `src/px4_msgs` 与 `src/px4_ros_com` submodule

### 构建与运行修正

- 新增 `scripts/autopilot_lab_env.sh`
  - 安装用户态 Python 依赖
  - source `/opt/ros/humble/setup.bash`
  - source `install/setup.bash`
- 处理 ROS Humble 与 `empy` 的兼容问题
  - 当前采用 `empy<4`
- 清除代码和文档中的旧工作区硬编码
  - `/home/car/px4_ws`
  - `/mnt/nvme/px4_work/px4_ws`

## 验证记录

### 构建验证

- `python3 -m compileall` 通过
- `colcon build --packages-up-to fep_core px4_ros2_backend fep_research ardupilot_mavlink_backend px4_msgs px4_ros_com` 通过

### PX4 smoke

- 命令:
  - `ros2 run fep_research matrix_runner --world default --pattern baseline_roll.yaml`
- 结果:
  - 新仓 PX4 run 已成功落盘
  - 代表性产物:
    - `artifacts/px4/runs/20260326_225500_attitude_baseline_roll/`

### ArduPilot smoke

- 命令:
  - `ros2 run ardupilot_mavlink_backend ardupilot_experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/baseline_roll.yaml`
- 结果:
  - 能启动外部 `/home/car/ardupilot` 的 SITL
  - 能通过 `pymavlink` 建立连接并落盘遥测
  - 代表性产物:
    - `artifacts/ardupilot/runs/20260326_230029_attitude_baseline_roll/`

## 当前使用方式

先 source 环境：

```bash
source /home/car/autopilot_lab/scripts/autopilot_lab_env.sh
```

PX4：

```bash
MicroXRCEAgent udp4 -p 8888
cd /home/car/PX4-Autopilot
make px4_sitl gz_x500
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/baseline_roll.yaml
```

ArduPilot：

```bash
ros2 run ardupilot_mavlink_backend ardupilot_experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/baseline_roll.yaml
```

## 当前注意事项

- `src/fep_research` 现在是兼容层，不是主要实现位置
- PX4 日志仍保留在 `/home/car/PX4-Autopilot/build/px4_sitl_default/rootfs/log/`
- ArduPilot backend 当前只实现了最小实验闭环，还没有 PX4 等价的完整分析深度
- 后续所有新工作都应以 `autopilot_lab` 为准，不再以 `px4_ws` 为准
