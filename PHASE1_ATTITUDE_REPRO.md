# Phase 1 Attitude 实验复现说明

这份文档用于复现当前已经完成的 `attitude` 主链实验，包括：

- `baseline`
- `roll 0.10`
- `roll 0.20`
- `pitch 0.10`
- `pitch 0.20`

`manual_control_input` 的 ground echo 验证已经单独整理在：

- `/home/car/autopilot_lab/PHASE1_MANUAL_REPRO.md`

当前如果要复现 nominal/windy 汇总、`analysis_runner` 或 `windy` 下的 attitude `pulse/sweep` anchor，请改看：

- `/home/car/autopilot_lab/PHASE3_ANALYSIS_REPRO.md`

当前实现采用新的 hybrid takeoff 口径：

- 起飞阶段参考 `px4_ros_com/offboard_control.py`
- 先用 `position + trajectory_setpoint` 起飞并进入悬停
- 到达目标高度后，再切到 `attitude + vehicle_attitude_setpoint`
- attitude 阶段带轻量高度保持修正

旧的 fixed-thrust 直接起飞口径不再作为首选参考。

## 当前首选参考结果

以下 artifact 是当前优先参考的一组：

- baseline:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_075735_attitude_baseline_roll/`
- `roll 0.10`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_075831_attitude_step_roll/`
- `roll 0.20`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_075919_attitude_step_roll/`
- `pitch 0.10`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_080623_attitude_step_pitch/`
- `pitch 0.20`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_080711_attitude_step_pitch/`

对应的关键指标：

- baseline:
  - `status=completed`
  - `tracking_error_peak=0.039394`
  - `tracking_error_rms=0.007278`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `roll 0.10`:
  - `status=completed`
  - `response_delay_ms=83.828`
  - `tracking_error_peak=0.099726`
  - `tracking_error_rms` 见该 run 的 `metrics.csv`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `roll 0.20`:
  - `status=completed`
  - `response_delay_ms=93.598`
  - `tracking_error_peak=0.19995`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `pitch 0.10`:
  - `status=completed`
  - `response_delay_ms=69.776`
  - `tracking_error_peak=0.100126`
  - `tracking_error_rms=0.012211`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `pitch 0.20`:
  - `status=completed`
  - `response_delay_ms=74.32`
  - `tracking_error_peak=0.200077`
  - `tracking_error_rms=0.024676`
  - `nav_state_change=0`
  - `failsafe_event=0`

## 已知限制

- 当前这些 run 都带有 `clock_missing`
- 因此它们只适合 `functional / non-timing` 结论
- 不适合用于 `timing / phase / lockstep` 结论

## 相关配置文件

配置都在 `/home/car/autopilot_lab/src/fep_research/config/` 下：

- `baseline_roll.yaml`
- `step_roll_010.yaml`
- `step_roll_020.yaml`
- `step_pitch_010.yaml`
- `step_pitch_020.yaml`

## 一次性构建

如果你刚改过代码，先构建：

```bash
cd /home/car/autopilot_lab
source /opt/ros/humble/setup.bash
colcon build --packages-select fep_research --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
```

## 每次实验前的环境准备

先确认没有旧进程残留：

```bash
pgrep -af 'MicroXRCEAgent udp4 -p 8888|px4_sitl_default/bin/px4|gz sim|ros2 run fep_research experiment_runner'
```

正常情况下，这条命令不应输出旧进程。

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

建议先做一遍最小真值检查：

```bash
ros2 topic list | rg '^/fmu/(in|out)/'
ros2 topic echo --once /fmu/out/vehicle_status
```

至少应能看到这些 topic：

- `/fmu/in/offboard_control_mode`
- `/fmu/out/vehicle_attitude`
- `/fmu/out/vehicle_control_mode`
- `/fmu/out/vehicle_status`

## 推荐复现实验顺序

建议按下面顺序执行。前一组完成且无异常，再跑后一组。

### 1. baseline

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/baseline_roll.yaml
```

### 2. roll 0.10

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/step_roll_010.yaml
```

### 3. roll 0.20

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/step_roll_020.yaml
```

### 4. pitch 0.10

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/step_pitch_010.yaml
```

### 5. pitch 0.20

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/step_pitch_020.yaml
```

## 每次 run 完成后看什么

每次 run 都会自动生成目录：

```text
/home/car/autopilot_lab/artifacts/px4/runs/<run_id>/
```

重点看这几个文件：

- `manifest.yaml`
- `metrics.csv`
- `notes.md`
- `telemetry/vehicle_attitude.csv`
- `telemetry/vehicle_local_position.csv`
- `telemetry/input_profile.csv`

快速检查命令：

```bash
LATEST_RUN="$(ls -dt /home/car/autopilot_lab/artifacts/px4/runs/* | head -n 1)"
echo "${LATEST_RUN}"
cat "${LATEST_RUN}/metrics.csv"
sed -n '1,200p' "${LATEST_RUN}/manifest.yaml"
tail -n 60 "${LATEST_RUN}/notes.md"
```

## 我实际采用的放行标准

当前 `attitude` 实验继续推进时，我主要看这些条件：

- `status=completed`
- `nav_state_change=0`
- `failsafe_event=0`
- 没有明显的低空擦地、反弹或异常大姿态耦合
- `manifest.yaml` 中能记录到 `px4_log_path`

当前阶段不把 `/clock` 缺失当作 functional blocker。

## 当前不再优先参考的旧 run

下面这些是旧口径或已被新口径替代的 run，不建议再作为首选参考：

- `/home/car/autopilot_lab/artifacts/px4/runs/20260310_072035_attitude_step_roll/`
- `/home/car/autopilot_lab/artifacts/px4/runs/20260310_072151_attitude_step_pitch/`

原因：

- 这些 run 发生在 hybrid takeoff 重构之前
- 旧起飞策略更容易出现低空、贴地或低质量数据

## 实验结束后的收尾

如果你要结束本轮实验，直接在 Agent 和 PX4 的终端里按 `Ctrl-C` 即可。

可再检查一次是否还有残留进程：

```bash
pgrep -af 'MicroXRCEAgent udp4 -p 8888|px4_sitl_default/bin/px4|gz sim|ros2 run fep_research experiment_runner'
```

如果后续要继续 Phase 1，下一步应从 `manual_control_input` 主链开始，而不是继续放大 `roll/pitch` 幅值。
