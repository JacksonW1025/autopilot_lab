# Phase 2 Monitoring / Logging 复现说明

这份文档用于复现当前已经完成的 **Phase 2: Monitoring & Logging** 工作。

当前我判断 Phase 2 **已经完成**，因为 `/home/car/autopilot_lab/TODO.md` 中的 Phase 2 exit criteria 已满足：

- 在线 5 个标准 topic 都能稳定录制
- 每次 run 都能把 `.ulg` 绝对路径写入 `manifest.yaml`
- `notes.md` 能自动生成异常摘要
- recorder 不依赖 PlotJuggler 与 ULog CLI
- 已至少有一组 run 同时提供 ROS 证据、ULog 路径和主机性能快照

## 当前首选参考结果

推荐用下面两组 run 复现 Phase 2 的 logging 口径：

- attitude:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_075831_attitude_step_roll/`
- manual flight:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_093511_manual_step_roll/`

这两组都已经具备：

- 完整 `telemetry/*.csv`
- `manifest.yaml`
- `notes.md`
- `metrics.csv`
- `.ulg` 绝对路径
- 主机性能快照

## Phase 2 的标准观测量

当前 recorder 固定录制这 5 个标准 topic：

- `/fmu/out/vehicle_attitude`
- `/fmu/out/vehicle_local_position`
- `/fmu/out/vehicle_status`
- `/fmu/out/manual_control_setpoint`
- `/fmu/out/vehicle_control_mode`

另外会额外落盘：

- `telemetry/input_profile.csv`
- `telemetry/vehicle_status_events.csv`
- `telemetry/vehicle_control_mode_events.csv`

## 当前 artifact 结构

每次 run 的标准结构：

```text
/home/car/autopilot_lab/artifacts/px4/runs/<run_id>/
├── manifest.yaml
├── notes.md
├── metrics.csv
├── telemetry/
│   ├── input_profile.csv
│   ├── manual_control_setpoint.csv
│   ├── vehicle_attitude.csv
│   ├── vehicle_control_mode.csv
│   ├── vehicle_control_mode_events.csv
│   ├── vehicle_local_position.csv
│   ├── vehicle_status.csv
│   └── vehicle_status_events.csv
└── plots/
```

## 一次性构建

如果刚改过代码，先构建：

```bash
cd /home/car/autopilot_lab
source /opt/ros/humble/setup.bash
colcon build --packages-select fep_research --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
```

## 复现一组标准 Phase 2 run

先确认没有旧进程：

```bash
pgrep -af 'MicroXRCEAgent udp4 -p 8888|px4_sitl_default/bin/px4|gz sim|ros2 run fep_research experiment_runner'
```

然后准备 3 个终端。

### 终端 1：启动 Agent

```bash
source /opt/ros/humble/setup.bash
MicroXRCEAgent udp4 -p 8888
```

### 终端 2：启动 PX4 SITL

```bash
cd /home/car/PX4-Autopilot
make px4_sitl gz_x500
```

### 终端 3：source 工作空间

```bash
source /opt/ros/humble/setup.bash
source /home/car/autopilot_lab/install/setup.bash
```

建议先做真值检查：

```bash
ros2 topic list | rg '^/fmu/(in|out)/'
ros2 topic echo --once /fmu/out/vehicle_status
```

## 推荐复现实验顺序

### 1. attitude step roll

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/step_roll_010.yaml
```

### 2. manual flight roll

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_roll_040.yaml
```

## 每次 run 完成后看什么

### A. 看 recorder 是否真的录满 5 个 topic

```bash
LATEST_RUN="$(ls -dt /home/car/autopilot_lab/artifacts/px4/runs/* | head -n 1)"
find "${LATEST_RUN}/telemetry" -maxdepth 1 -type f | sort
```

应至少看到：

- `vehicle_attitude.csv`
- `vehicle_local_position.csv`
- `vehicle_status.csv`
- `manual_control_setpoint.csv`
- `vehicle_control_mode.csv`

### B. 看 manifest 是否写入 `.ulg` 绝对路径

```bash
sed -n '1,220p' "${LATEST_RUN}/manifest.yaml"
```

重点确认：

- `px4_log_path`
- `ros_topics_recorded`
- `anomaly_summary`

### C. 看 notes 是否自动写入异常摘要和主机性能快照

```bash
sed -n '1,260p' "${LATEST_RUN}/notes.md"
```

重点确认：

- `观察到的异常`
- `Recorder 摘要`
- `主机性能快照（开始前）`
- `主机性能快照（结束后）`
- `Timing 分析可用性`

### D. 看 metrics 是否落盘

```bash
cat "${LATEST_RUN}/metrics.csv"
```

## 我当前采用的验收口径

当前我把下面这些现象视为 Phase 2 已经打通：

- 5 个标准 topic 有持续 CSV
- `vehicle_status_events.csv` 与 `vehicle_control_mode_events.csv` 能生成
- `manifest.yaml` 中有 `.ulg` 绝对路径
- `notes.md` 中有异常摘要和主机性能快照
- 整个流程不依赖：
  - PlotJuggler
  - `ulog2csv`
  - `pyulog`

## 当前限制

- 当前很多 run 仍带 `clock_missing`
- 因此 Phase 2 已完成不代表 timing 结论可用
- 当前 Phase 2 完成的含义是：
  - logging / evidence pipeline 已稳定
  - 不是 `/clock` 问题已经解决

## 与其他 Phase 的边界

- Phase 1:
  - 关注输入链、profile 接口和单 run 闭环是否打通
- Phase 2:
  - 关注证据是否稳定落盘
- Phase 3:
  - 关注跨 run 汇总、frontier layering、nominal/windy 对比

对应复现文档：

- Phase 1:
  - `/home/car/autopilot_lab/PHASE1_ATTITUDE_REPRO.md`
  - `/home/car/autopilot_lab/PHASE1_MANUAL_REPRO.md`
- Phase 3:
  - `/home/car/autopilot_lab/PHASE3_ANALYSIS_REPRO.md`

## 实验结束后的收尾

在 Agent 和 PX4 终端按 `Ctrl-C` 即可。

最后确认没有残留进程：

```bash
pgrep -af 'MicroXRCEAgent udp4 -p 8888|px4_sitl_default/bin/px4|gz sim|ros2 run fep_research experiment_runner'
```
