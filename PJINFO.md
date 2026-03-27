# PJINFO.md

> 每次 Agent work 前先读本文件；完成后只更新“当前状态”和“最近变更”。

## 项目背景

- 核心目标：围绕 FEP / PIO 前期研究，建立可用于论文实验的多飞控分层敏感性平台
- 研究对象：PX4 与 ArduPilot 两套 SITL 控制链
- 当前主线：`manual_whole_loop + attitude_explicit`
- 条件层：`rate_single_loop`
- 参考方法来源：`~/RouthSearch`
  - 借鉴 `mode-specific task`
  - 借鉴 `offline oracle`
  - 借鉴 `valid/invalid boundary`
  - 借鉴 `parameter factor`
  - 不把当前仓库改回纯 PID 边界复现仓

## 环境基线

- 计算平台：Jetson AGX Orin 64G
- 操作系统：Ubuntu 22.04 aarch64
- ROS：Humble
- Gazebo：Harmonic
- 主仓库：`/home/car/autopilot_lab -> /mnt/nvme/autopilot_lab`
- PX4 固件：`/home/car/PX4-Autopilot`
- ArduPilot 固件：`/home/car/ardupilot`
- RouthSearch 参考路径：`~/RouthSearch`

## 当前默认研究口径

### `manual_whole_loop`

- 目标：评估飞手激进输入下的整机闭环响应敏感度
- PX4：`manual -> POSCTL`
- ArduPilot：`MANUAL_CONTROL -> STABILIZE`
- 输入：`roll / pitch / yaw / throttle`
- 输出：姿态、位置、模式变化、执行器约束
- 主标签：`oracle_valid`
- 归因边界：只说明整机闭环，不直接归因到 `attitude / rate`

### `attitude_explicit`

- 目标：分析 `attitude setpoint -> actual attitude` 的参数敏感度
- PX4：显式 offboard attitude
- ArduPilot：`GUIDED + SET_ATTITUDE_TARGET`
- 输入：attitude setpoint + controlled thrust
- 输出：actual attitude，必要时加 actual rates
- 主标签：`oracle_valid`
- 归因边界：只说明 attitude 层及其以下控制链

### `rate_single_loop`

- 当前不是第一批默认实验
- 引入条件：
  - attitude 层差异无法由输入映射或 altitude hold 解释
  - 研究参数本身就是 rate PID
  - 论文需要更强归因证据

## 目录与接口

- 共享层：`src/fep_core`
- PX4 backend：`src/px4_ros2_backend`
- ArduPilot backend：`src/ardupilot_mavlink_backend`
- 兼容入口：`src/fep_research`
- 归档文档：`docs/`
- Study 汇总输出：`artifacts/studies/`

## 当前默认配置

- manual baseline：`src/fep_research/config/layered_manual_roll_020.yaml`
- manual `P+20%`：`src/fep_research/config/layered_manual_roll_020_p120.yaml`
- attitude baseline：`src/fep_research/config/layered_attitude_roll_010.yaml`
- attitude `P+20%`：`src/fep_research/config/layered_attitude_roll_010_p120.yaml`

## 当前状态

- [2026-03-27] 根文档默认口径已从 PX4-only phase 流水线切到分层敏感性研究平台
- [2026-03-27] `fep_core.config` 已加入 `study_* / oracle / parameter / attribution` schema
- [2026-03-27] `fep_core` 已加入 study artifact 目录和跨 backend `study_analysis_runner`
- [2026-03-27] PX4 telemetry recorder 已补 attitude 层证据链：
  - `vehicle_attitude_setpoint`
  - `vehicle_rates_setpoint`
  - `vehicle_angular_velocity`
  - `rate_ctrl_status`
  - `control_allocator_status`
  - `actuator_motors`
- [2026-03-27] PX4 `experiment_runner` 已接入：
  - 参数 `snapshot / apply / restore`
  - `oracle_valid / oracle_failure_reason`
  - `stress_class`
  - `mechanism_flags`
  - `rate_layer_recommended`
- [2026-03-27] ArduPilot `experiment_runner` 已从最小 smoke runner 改成分层 runner
- [2026-03-27] ArduPilot 已补 `.BIN` 离线解析：
  - `ATT`
  - `RATE`
  - `CTUN`
  - `MOTB`
  - `RCOU`
- [2026-03-27] `ros2 run fep_research analysis_runner` 已切到新的分层 study 汇总
- [2026-03-27] 旧顶层 Phase 文档已退出主入口，现仅保留在 `docs/`

## 最近变更

- 新增 `artifacts/studies/<timestamp>_layered_sensitivity/`
- 新增分层配置：
  - `layered_manual_roll_020.yaml`
  - `layered_manual_roll_020_p120.yaml`
  - `layered_attitude_roll_010.yaml`
  - `layered_attitude_roll_010_p120.yaml`
- 新增 ArduPilot `.BIN` 指标提取模块：
  - `src/ardupilot_mavlink_backend/ardupilot_mavlink_backend/bin_log_metrics.py`

## 常用命令

先加载环境：

```bash
source /home/car/autopilot_lab/scripts/autopilot_lab_env.sh
```

PX4 manual：

```bash
MicroXRCEAgent udp4 -p 8888
cd /home/car/PX4-Autopilot
make px4_sitl gz_x500
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/layered_manual_roll_020.yaml
```

PX4 attitude：

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/layered_attitude_roll_010.yaml
```

ArduPilot manual：

```bash
ros2 run ardupilot_mavlink_backend ardupilot_experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/layered_manual_roll_020.yaml
```

ArduPilot attitude：

```bash
ros2 run ardupilot_mavlink_backend ardupilot_experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/layered_attitude_roll_010.yaml
```

跨 backend study 汇总：

```bash
ros2 run fep_research analysis_runner
```

## 注意事项

- 所有文档和交互统一使用简体中文
- `~/RouthSearch` 是旧 ISSTA 工作的唯一参考代码口径
- 如需系统级操作，可以使用 `sudo`
- 旧 `px4_ws` 与旧 Phase 文档不再作为默认开发入口
