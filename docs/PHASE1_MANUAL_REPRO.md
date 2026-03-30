# Phase 1 Manual 实验复现说明

> Archived: 这是旧 PX4-only Phase 文档，不再代表 `Dual-Backend M1` 的默认入口或默认结论。
>
> 当前权威状态看：`/home/car/autopilot_lab/docs/M1_STATUS.md`
>
> 当前默认入口看：`/home/car/autopilot_lab/README.md` 与 `/home/car/autopilot_lab/docs/intro.md`

这份文档用于复现当前已经完成的 `manual_control_input` 基础链路验证，以及已打通的 manual flight 验证。

当前验证目标只有一条：

- 输入：`/fmu/in/manual_control_input`
- 回显：`/fmu/out/manual_control_setpoint`

`manual_mode=echo` 这一步**不是** manual 飞行实验。

它不会主动执行：

- arm
- offboard 切换
- takeoff
- land

所以实验期间飞机保持静止，是当前阶段的预期行为。

## 当前首选参考结果

- `manual roll 0.20`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_091844_manual_step_roll/`
- `manual throttle 0.20`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_091935_manual_step_throttle/`
- `manual flight roll 0.40`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_093511_manual_step_roll/`
- `manual flight pitch 0.40`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_015041_manual_step_pitch/`
- `manual flight yaw 0.40`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_015137_manual_step_yaw/`
- `manual flight throttle 0.30`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_015241_manual_step_throttle/`
- `manual flight roll 0.60 / 4s`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_025216_manual_step_roll/`
- `manual flight pitch 0.60 / 4s`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_025321_manual_step_pitch/`
- `manual flight yaw 0.60 / 4s`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_025417_manual_step_yaw/`
- `manual flight throttle 0.40 / 4s`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_025523_manual_step_throttle/`
- `manual flight roll 0.80 / 4s`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_032107_manual_step_roll/`
- `manual flight pitch 0.80 / 4s`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_032211_manual_step_pitch/`
- `manual flight yaw 0.80 / 4s`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_032310_manual_step_yaw/`
- `manual flight throttle 0.80 / 4s`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_032406_manual_step_throttle/`
- `manual flight composite moderate`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_033558_manual_step_composite/`
- `manual flight composite aggressive (z gate failed)`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_033654_manual_step_composite/`
- `manual flight composite aggressive t035`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_033822_manual_step_composite/`

关键结果：

- `manual roll 0.20`:
  - `status=completed`
  - `input_peak=0.2`
  - `response_delay_ms=2.328`
  - `tracking_error_peak=0.0`
  - `tracking_error_rms=0.0`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual throttle 0.20`:
  - `status=completed`
  - `input_peak=0.2`
  - `response_delay_ms=2.826`
  - `tracking_error_peak=0.0`
  - `tracking_error_rms=0.0`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight roll 0.40`:
  - `status=completed`
  - `input_peak=0.4`
  - `response_delay_ms=7.651`
  - `tracking_error_peak=0.0`
  - `tracking_error_rms=0.0`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight pitch 0.40`:
  - `status=completed`
  - `input_peak=0.4`
  - `response_delay_ms=2.675`
  - `tracking_error_peak=0.0`
  - `tracking_error_rms=0.0`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight yaw 0.40`:
  - `status=completed`
  - `input_peak=0.4`
  - `response_delay_ms=1.653`
  - `tracking_error_peak=0.0`
  - `tracking_error_rms=0.0`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight throttle 0.30`:
  - `status=completed`
  - `input_peak=0.3`
  - `response_delay_ms=10.712`
  - `tracking_error_peak=0.0`
  - `tracking_error_rms=0.0`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight roll 0.60 / 4s`:
  - `status=completed`
  - `input_peak=0.6`
  - `response_delay_ms=6.348`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight pitch 0.60 / 4s`:
  - `status=completed`
  - `input_peak=0.6`
  - `response_delay_ms=12.919`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight yaw 0.60 / 4s`:
  - `status=completed`
  - `input_peak=0.6`
  - `response_delay_ms=2.771`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight throttle 0.40 / 4s`:
  - `status=completed`
  - `input_peak=0.4`
  - `response_delay_ms=5.676`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight roll 0.80 / 4s`:
  - `status=completed`
  - `input_peak=0.8`
  - `response_delay_ms=5.567`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight pitch 0.80 / 4s`:
  - `status=completed`
  - `input_peak=0.8`
  - `response_delay_ms=2.839`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight yaw 0.80 / 4s`:
  - `status=completed`
  - `input_peak=0.8`
  - `response_delay_ms=2.755`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight throttle 0.80 / 4s`:
  - `status=completed`
  - `input_peak=0.8`
  - `response_delay_ms=4.645`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight composite moderate`:
  - `status=completed`
  - `input_peak=0.25`
  - `response_delay_ms=4.977`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight composite aggressive (z gate failed)`:
  - `status=invalid_runtime`
  - `input_peak=0.4`
  - `response_delay_ms=5.877`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight composite aggressive t035`:
  - `status=completed`
  - `input_peak=0.4`
  - `response_delay_ms=4.724`
  - `nav_state_change=0`
  - `failsafe_event=0`

回显特征：

- 两组 run 的 `/fmu/out/manual_control_setpoint` 都真实收到输入
- `data_source=2`，即 `SOURCE_MAVLINK_0`
- `roll` 或 `throttle` 的回显峰值都达到约 `0.2`

真实控制效果特征：

- `manual flight roll 0.40` 在 step 窗口内切到了 `POSCTL + manual enabled`
- telemetry 复核可见 `max_xy_disp≈1.67 m`
- 同一窗口内 `max_roll_deg≈3.39`
- `manual flight pitch 0.40` 的 step 窗口 `max_xy_disp≈1.49 m`
- `manual flight yaw 0.40` 的 step 窗口 `max_yaw_delta≈1.00 rad / 57.3 deg`
- `manual flight throttle 0.30` 的 step 窗口 `max_abs_dz≈0.69 m`
- `manual flight roll 0.60 / 4s` 的 step 窗口 `max_xy_disp≈5.72 m`
- `manual flight pitch 0.60 / 4s` 的 step 窗口 `max_xy_disp≈5.76 m`
- `manual flight yaw 0.60 / 4s` 的 step 窗口 `max_yaw_delta≈2.97 rad / 170.3 deg`
- `manual flight throttle 0.40 / 4s` 的 step 窗口 `max_abs_dz≈1.50 m`
- `manual flight roll 0.80 / 4s` 的 step 窗口 `max_xy_disp≈10.72 m`
- `manual flight pitch 0.80 / 4s` 的 step 窗口 `max_xy_disp≈10.56 m`
- `manual flight yaw 0.80 / 4s` 的 step 窗口 `max_yaw_delta≈3.14 rad / 179.8 deg`
- `manual flight throttle 0.80 / 4s` 的 step 窗口 `max_abs_dz≈5.23 m`
- `manual flight composite moderate` 的 step 窗口：
  - `max_xy_disp≈1.30 m`
  - `max_abs_dz≈0.29 m`
  - `max_yaw_delta≈0.45 rad / 25.7 deg`
- `manual flight composite aggressive (t=0.20)` 的 step 窗口：
  - `max_xy_disp≈3.19 m`
  - `max_abs_dz≈0.06 m`
  - `max_yaw_delta≈0.65 rad / 37.1 deg`
- `manual flight composite aggressive t035` 的 step 窗口：
  - `max_xy_disp≈3.14 m`
  - `max_abs_dz≈1.49 m`
  - `max_yaw_delta≈0.60 rad / 34.1 deg`
- 这说明 manual 输入已经不只是 echo，而是对机体运动产生了真实影响

## 已知限制

- 当前 run 都带有 `clock_missing`
- 所以仍然只适合 `functional / non-timing` 结论
- echo run 只能说明 manual 输入链路可达
- 当前已完成 `roll / pitch / yaw / throttle` 的首轮空中 manual flight 验证

## 配置文件

配置位于 `/home/car/autopilot_lab/src/fep_research/config/`：

- `manual_step_roll_020.yaml`
- `manual_step_throttle_020.yaml`
- `manual_flight_roll_020.yaml`
- `manual_flight_roll_040.yaml`
- `manual_flight_pitch_040.yaml`
- `manual_flight_yaw_040.yaml`
- `manual_flight_throttle_030.yaml`
- `manual_flight_roll_060.yaml`
- `manual_flight_pitch_060.yaml`
- `manual_flight_yaw_060.yaml`
- `manual_flight_throttle_040.yaml`
- `manual_flight_roll_080.yaml`
- `manual_flight_pitch_080.yaml`
- `manual_flight_yaw_080.yaml`
- `manual_flight_throttle_080.yaml`
- `manual_flight_composite_moderate.yaml`
- `manual_flight_composite_aggressive.yaml`
- `manual_flight_composite_aggressive_t035.yaml`

## 一次性构建

如果刚改过代码，先构建：

```bash
cd /home/car/autopilot_lab
source /opt/ros/humble/setup.bash
colcon build --packages-select fep_research --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
```

## 每次实验前的环境准备

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

建议先做最小真值检查：

```bash
ros2 topic list | rg '^/fmu/(in|out)/'
ros2 topic echo --once /fmu/out/vehicle_status
```

至少确认这些 topic 可见：

- `/fmu/in/manual_control_input`
- `/fmu/out/manual_control_setpoint`
- `/fmu/out/vehicle_status`

## 推荐复现实验顺序

### 1. manual roll 0.20

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_step_roll_020.yaml
```

### 2. manual throttle 0.20

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_step_throttle_020.yaml
```

### 3. manual flight roll 0.40

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_roll_040.yaml
```

### 4. manual flight pitch 0.40

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_pitch_040.yaml
```

### 5. manual flight yaw 0.40

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_yaw_040.yaml
```

### 6. manual flight throttle 0.30

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_throttle_030.yaml
```

### 7. manual flight roll 0.60 / 4s

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_roll_060.yaml
```

### 8. manual flight pitch 0.60 / 4s

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_pitch_060.yaml
```

### 9. manual flight yaw 0.60 / 4s

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_yaw_060.yaml
```

### 10. manual flight throttle 0.40 / 4s

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_throttle_040.yaml
```

### 11. manual flight roll 0.80 / 4s

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_roll_080.yaml
```

### 12. manual flight pitch 0.80 / 4s

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_pitch_080.yaml
```

### 13. manual flight yaw 0.80 / 4s

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_yaw_080.yaml
```

### 14. manual flight throttle 0.80 / 4s

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_throttle_080.yaml
```

### 15. manual flight composite moderate

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_composite_moderate.yaml
```

### 16. manual flight composite aggressive

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_composite_aggressive.yaml
```

### 17. manual flight composite aggressive t035

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_composite_aggressive_t035.yaml
```

## 每次 run 完成后看什么

每次 run 会生成：

```text
/home/car/autopilot_lab/artifacts/px4/runs/<run_id>/
```

重点看：

- `manifest.yaml`
- `metrics.csv`
- `notes.md`
- `telemetry/manual_control_setpoint.csv`
- `telemetry/input_profile.csv`
- `telemetry/vehicle_local_position.csv`
- `telemetry/vehicle_control_mode.csv`

快速检查：

```bash
LATEST_RUN="$(ls -dt /home/car/autopilot_lab/artifacts/px4/runs/* | head -n 1)"
echo "${LATEST_RUN}"
cat "${LATEST_RUN}/metrics.csv"
sed -n '1,200p' "${LATEST_RUN}/manifest.yaml"
tail -n 60 "${LATEST_RUN}/notes.md"
```

如果要直接看 manual 回显峰值：

```bash
python3 - <<'PY'
import csv
from pathlib import Path
run = Path("REPLACE_WITH_RUN_DIR")
rows = list(csv.DictReader((run / "telemetry" / "manual_control_setpoint.csv").open()))
for axis in ("roll", "pitch", "yaw", "throttle"):
    values = [float(r[axis]) for r in rows]
    print(axis, min(values), max(values))
print("data_source", sorted({r["data_source"] for r in rows}))
PY
```

如果要直接复核 manual flight 是否真的让机体移动：

```bash
python3 - <<'PY'
import csv
import math
from pathlib import Path
run = Path("REPLACE_WITH_RUN_DIR")
profile_rows = list(csv.DictReader((run / "telemetry" / "input_profile.csv").open()))
active_ns = [int(r["publish_time_ns"]) for r in profile_rows if r["phase"] == "step_active" or abs(float(r["profile_value"])) > 1e-6]
start_ns = min(active_ns)
end_ns = max(active_ns)
pos_rows = [
    r for r in csv.DictReader((run / "telemetry" / "vehicle_local_position.csv").open())
    if start_ns <= int(r["received_time_ns"]) <= end_ns
]
x0 = float(pos_rows[0]["x"])
y0 = float(pos_rows[0]["y"])
max_xy = max(
    math.hypot(float(r["x"]) - x0, float(r["y"]) - y0)
    for r in pos_rows
)
print("max_xy_disp_m", round(max_xy, 6))
PY
```

## 当前放行标准

当前 manual echo 验证继续推进时，我主要看这些条件：

- `status=completed`
- `nav_state_change=0`
- `failsafe_event=0`
- `manual_control_setpoint.csv` 里有真实样本
- 样本中的 `data_source=2`
- 目标轴的回显峰值达到配置幅值附近

当前 manual flight 验证继续推进时，我额外看这些条件：

- `status=completed`
- `nav_state_change=0`
- `failsafe_event=0`
- `vehicle_control_mode.csv` 中出现 `flag_control_manual_enabled=True`
- `vehicle_status.csv` 中出现 `nav_state=2 (POSCTL)`
- step 窗口里能观察到真实机体位移或姿态变化

## 历史后续方向

当前 manual 主链已经完成：

- ground echo 验证
- `roll / pitch / yaw / throttle` 的首轮空中真实控制效果验证
- 更高幅值 / 更长 duration 的第二轮验证：`roll / pitch / yaw = 0.60 / 4s`，`throttle = 0.40 / 4s`
- `0.80 / 4s` 的单轴梯度验证
- `composite` profile：`moderate` 已通过，`aggressive t035` 已通过

按当时的 Phase 1 语境，如果要更进一步，应做下面二选一之一：

- 做 `composite` profile，或把 `duration` 再拉长到 `5-6s`
- 在保持当前 hybrid takeoff 的前提下提高 manual 分析指标，补自动位移/姿态摘要

按 `2026-03-30` 的当前主线，这里已经是历史后续方向；现在的研究扩展顺序以 `/home/car/autopilot_lab/docs/M1_STATUS.md` 为准：先补 pitch，再做 yaw/composite。
