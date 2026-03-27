# autopilot_lab

`autopilot_lab` 现在的默认定位不再是“PX4-only 激励演示仓”，而是一个面向论文研究的分层敏感性实验平台。

通俗地说，旧工作主要是在 PX4 里打激进输入，看系统哪里先坏、哪些约束先顶满；现在仓库要进一步回答的是：在不同控制层、不同参数组下，系统从 `valid` 到 `invalid` 的边界怎么移动，以及这个变化应该归因到哪一层。

这次改造参考了 `~/RouthSearch` 的方法结构，而不是直接回退到旧的 PID 论文复现。当前显式吸收的核心概念有：

- `mode-specific task`
- `offline oracle`
- `valid/invalid boundary`
- `parameter factor`

因此，仓库主线已经改成：

- `manual_whole_loop`
  - 评估飞手激进输入下的整机闭环响应敏感度
- `attitude_explicit`
  - 单独分析 `attitude setpoint -> actual attitude` 的参数敏感度
- `rate_single_loop`
  - 不是默认主线，但已经有统一 schema、触发条件和 artifact 位置；当姿态层归因不够强时再补进来

## 当前默认研究口径

### 1. `manual_whole_loop`

- 研究问题：飞手等价输入进入飞控后，整机闭环在哪个输入档位开始从 `valid` 走向 `invalid`
- PX4：`manual -> POSCTL`
- ArduPilot：`MANUAL_CONTROL -> STABILIZE`
- 输入：`roll / pitch / yaw / throttle`
- 输出：姿态、位置、模式变化、执行器约束
- 主指标：`oracle_valid`、tracking error、response delay、XY/Z drift、failsafe、saturation onset
- 归因边界：只用于整机 `pilot-input sensitivity`，不直接归因到 `attitude` 或 `rate` 单层参数

### 2. `attitude_explicit`

- 研究问题：去掉 manual mapping 后，`attitude setpoint -> actual attitude` 的跟踪与失稳边界如何随参数改变
- PX4：显式 offboard attitude setpoint
- ArduPilot：`GUIDED + SET_ATTITUDE_TARGET`
- 输入：`roll / pitch / yaw attitude setpoint` 与受控 `thrust`
- 输出：actual attitude，必要时辅以 actual rates
- 主指标：`oracle_valid`、attitude tracking error peak/rms、overshoot、settling、phase lag、clip/saturation
- 归因边界：只归因到 `attitude` 输入层及其以下控制链，不混入 manual shaping

### 3. `rate_single_loop`

- 当前不是第一批默认实验
- 但不再被默认忽略
- 只有满足以下条件时才正式补做：
  - 姿态层已经观察到显著差异，但这些差异无法由输入映射、altitude hold 或 manual shaping 解释
  - 当前研究因素本身就是 `MC_ROLLRATE_* / MC_PITCHRATE_* / ATC_RAT_RLL_* / ATC_RAT_PIT_*`
  - 论文归因需要更强证据，需要显式拆开 `attitude outer loop` 与 `rate inner loop`

## 仓库结构

```text
autopilot_lab/
├── artifacts/
│   ├── ardupilot/
│   ├── px4/
│   └── studies/
├── docs/
│   └── legacy PX4 phase documents
├── reference/
├── scripts/
└── src/
    ├── ardupilot_mavlink_backend/
    ├── fep_core/
    ├── fep_research/
    ├── px4_msgs/
    ├── px4_ros_com/
    └── px4_ros2_backend/
```

关键点：

- `fep_core`
  - 共享 schema、profile、artifact I/O、study analysis、参数快照工具
- `px4_ros2_backend`
  - PX4 专用 runner、injector、ULog 解析
- `ardupilot_mavlink_backend`
  - ArduPilot 专用 runner、MAVLink 注入、`.BIN` 解析
- `fep_research`
  - 兼容入口层，但默认 `analysis_runner` 已切到新的分层 study 汇总
- `docs/`
  - 旧 PX4-only Phase 文档归档区，不再代表当前主线

## 现在真正会输出什么

每个 run 都会落下新的研究元信息，而不再只保留旧的 phase 风格结果：

- `study_layer`
- `study_role`
- `mode_under_test`
- `parameter_group`
- `parameter_set_name`
- `parameter_snapshot_before`
- `parameter_snapshot_after`
- `oracle_valid`
- `oracle_failure_reason`
- `stress_class`
- `mechanism_flags`
- `rate_layer_recommended`
- `rate_layer_reasons`

跨 backend 汇总统一写到：

- `artifacts/studies/<timestamp>_layered_sensitivity/`

其中至少包括：

- `tables/merged_runs.csv`
- `reports/summary.md`
- `manifest.yaml`

## 默认实验配置

第一批默认配置已经切到分层主线，并显式支持 `roll_rate_pid` 的 `baseline / P+20%`：

- `src/fep_research/config/layered_manual_roll_020.yaml`
- `src/fep_research/config/layered_manual_roll_020_p120.yaml`
- `src/fep_research/config/layered_attitude_roll_010.yaml`
- `src/fep_research/config/layered_attitude_roll_010_p120.yaml`

当前 `P+20%` 使用：

- PX4：`MC_ROLLRATE_P = 0.18`
- ArduPilot：`ATC_RAT_RLL_P = 0.162`

## 使用方式

先加载环境：

```bash
source /home/car/autopilot_lab/scripts/autopilot_lab_env.sh
```

### PX4 manual 主线

```bash
MicroXRCEAgent udp4 -p 8888
cd /home/car/PX4-Autopilot
make px4_sitl gz_x500

ros2 run fep_research experiment_runner \
  --config /home/car/autopilot_lab/src/fep_research/config/layered_manual_roll_020.yaml
```

### PX4 attitude 主线

```bash
ros2 run fep_research experiment_runner \
  --config /home/car/autopilot_lab/src/fep_research/config/layered_attitude_roll_010.yaml
```

### ArduPilot manual 主线

```bash
ros2 run ardupilot_mavlink_backend ardupilot_experiment_runner \
  --config /home/car/autopilot_lab/src/fep_research/config/layered_manual_roll_020.yaml
```

### ArduPilot attitude 主线

```bash
ros2 run ardupilot_mavlink_backend ardupilot_experiment_runner \
  --config /home/car/autopilot_lab/src/fep_research/config/layered_attitude_roll_010.yaml
```

### 新的默认汇总

```bash
ros2 run fep_research analysis_runner
```

这条命令现在不再调用旧的 PX4-only `analysis_runner`，而是直接汇总 PX4 与 ArduPilot 的分层研究 run。

## 当前实现状态

- 已完成统一研究 schema：
  - `study_family`
  - `study_layer`
  - `study_role`
  - `oracle_profile`
  - `mode_under_test`
  - `parameter_group`
  - `parameter_set_name`
  - `parameter_overrides`
  - `controlled_parameters`
  - `input_contract`
  - `output_contract`
  - `attribution_boundary`
- PX4 runner 已支持：
  - 参数 `snapshot / apply / restore`
  - `oracle_valid`
  - `stress_class`
  - `mechanism_flags`
  - `rate layer` 触发建议
  - attitude 层证据链回填：`vehicle_attitude_setpoint / vehicle_rates_setpoint / vehicle_angular_velocity / rate_ctrl_status / control_allocator_status / actuator_motors`
- ArduPilot runner 已支持：
  - `manual_whole_loop`
  - `attitude_explicit`
  - 参数 `snapshot / apply / restore`
  - `.BIN` 离线解析
  - 标准化导出：`ATT / RATE / CTUN / MOTB / RCOU`
  - `oracle_valid`
  - `stress_class`
  - `mechanism_flags`
- `rate_single_loop`
  - schema 与触发条件已接入
  - ArduPilot body-rate 入口已预留
  - PX4 仍保留为条件层，当前不会作为第一批默认实验

## 归档说明

- 顶层旧 Phase 文档已经退出主入口
- 它们现在只保留在 `docs/`
- 如果你看到 `PHASE1_* / PHASE2_* / PHASE3_*`，应把它们当成旧 PX4-only 归档材料，而不是当前仓库的默认研究口径
