# Phase 3 Analysis / Windy 复现说明

这份文档用于复现当前已经完成的 **Phase 3** 工作，范围包括：

- `analysis_runner` 的跨 run 汇总
- nominal / windy 两套 `summary + CSV + SVG`
- nominal / windy 两套 fresh/headless matrix
- `windy.sdf` 下的 attitude `pulse / sweep` anchor
- `windy.sdf` 下的 attitude `step / pulse / sweep` 边界收敛与解释
- ULog 饱和指标的机制化汇总

当前这批工作已经不再属于 Phase 1。

原因很直接：

- Phase 1 的退出条件是“输入链、profile 接口、artifact 落盘打通”
- 当前已经在做：
  - 跨 run 汇总
  - nominal / windy 对比
  - frontier layering
  - 扰动下的边界比较

这些都对应 `/home/car/autopilot_lab/TODO.md` 中的 **Phase 3: Sensitivity Analysis**。

Phase 1 的 baseline / step / manual 主链复现仍保留在：

- `/home/car/autopilot_lab/PHASE1_ATTITUDE_REPRO.md`
- `/home/car/autopilot_lab/PHASE1_MANUAL_REPRO.md`

## 当前首选参考结果

当前优先参考的 Phase 3 分析目录：

- nominal:
  - `/home/car/autopilot_lab/artifacts/px4/analysis/20260313_043013_phase3_nominal/`
- windy:
  - `/home/car/autopilot_lab/artifacts/px4/analysis/20260313_043013_phase3_windy/`

当前优先参考的 nominal fresh matrix：

- `/home/car/autopilot_lab/artifacts/px4/matrix/20260313_035624_default/`

当前 nominal 关键结果：

- 选中 run 共 `41` 组，其中 completed=`40`
- 已完成 run 中有 `39` 组 timing-valid，仅 `1` 组仍是早期 `clock_missing` legacy run
- attitude 当前 nominal 前沿：
  - `step roll/pitch 0.10/0.15 -> safe`
  - `step roll/pitch 0.20 -> degraded`
  - `pulse roll/pitch 0.10/0.15 -> safe`
  - `pulse roll/pitch 0.20 -> degraded`
  - `sweep pitch 0.02 -> safe`
  - `sweep pitch 0.05/0.10 -> degraded`
  - `sweep roll 0.10 -> safe`
  - `sweep roll 0.15 -> degraded`
- nominal 的 `ulog_mechanism_summary.csv` 可见：
  - attitude `median_clip_frac≈0.010`
  - attitude `median_max_unalloc_torque≈0.131`
  - manual `median_clip_frac≈0.000`
  - manual `median_max_unalloc_torque≈0.012`
- 因此 nominal 下虽然 attitude 主链仍整体可完成，但它比 manual 链更早触到执行器/控制分配约束

当前优先参考的 `windy` attitude anchor：

- `attitude pulse roll 0.10`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_052601_attitude_pulse_roll/`
- `attitude pulse roll 0.20`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_052706_attitude_pulse_roll/`
- `attitude sweep roll 0.10`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_052759_attitude_sweep_roll/`
- `attitude sweep pitch 0.10`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_052856_attitude_sweep_pitch/`

对应关键结果：

- `pulse roll 0.10`:
  - `status=completed`
  - `tracking_error_peak=0.198241`
  - `tracking_error_rms=0.079284`
  - `response_delay_ms=11.183`
- `pulse roll 0.20`:
  - `status=completed`
  - `tracking_error_peak=0.202775`
  - `tracking_error_rms=0.029930`
  - `response_delay_ms=62.269`
- `sweep roll 0.10`:
  - `status=completed`
  - `tracking_error_peak=0.173096`
  - `tracking_error_rms=0.076127`
  - `response_delay_ms=4.601`
- `sweep pitch 0.10`:
  - `status=invalid_runtime`
  - `tracking_error_peak=0.169572`
  - `tracking_error_rms=0.063970`
  - `response_delay_ms=2.782`
  - `failsafe_event=1`
  - `anomaly_summary=['clock_missing', 'land_timeout_force_disarm']`

当前额外可参考的 `windy` 流程验证 run：

- `fresh pass`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_063154_attitude_pulse_roll/`
  - `prestart_xy_radius_m=0.186`
  - `status=completed`
- `same-session blocked`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_063246_attitude_pulse_roll/`
  - `prestart_xy_radius_m=83.154`
  - `completion_reason=prestart_xy_gate_blocked`
- `fresh pass-through but later dynamic invalid`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_063336_attitude_pulse_roll/`
  - `prestart_xy_radius_m=0.172`
  - `prestart gate passed=yes`
  - 后续仍 `failsafe_event=1`

当前额外可参考的 `windy manual` fresh anchor：

- `manual pulse pitch 0.40`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_064512_manual_pulse_pitch/`
  - `status=completed`
  - `end_xy_radius_m=1.113`
- `manual sweep pitch 0.40`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_064626_manual_sweep_pitch/`
  - `status=completed`
  - `end_xy_radius_m=2.069`
- `manual step composite moderate`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_064746_manual_step_composite/`
  - `status=completed`
  - `end_xy_radius_m=1.71`

当前额外可参考的 `windy attitude sweep` frontier：

- `attitude sweep roll 0.15`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_065047_attitude_sweep_roll/`
  - `status=invalid_runtime`
  - `failsafe_event=1`
  - `end_xy_radius_m=135.362`
- `attitude sweep pitch 0.02`:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_065214_attitude_sweep_pitch/`
  - `status=invalid_runtime`
  - `failsafe_event=1`
  - `end_xy_radius_m=128.711`

## 已知限制

- nominal 最新已选集并不再是“全部 non-timing”：
  - nominal completed 中已有 `39` 组 timing-valid
  - windy completed 中已有 `36` 组 timing-valid
- 但 nominal 已选集里仍保留 `1` 组 legacy `clock_missing` manual composite run
- 因此做严格 timing 对比时，仍要把这组 legacy run 单独标出或补 rerun
- `safe / degraded / invalid` 只是第一版 operational layering
- 后续解释不能只看 layer，还要同时看：
  - `tracking_error_peak`
  - `failsafe_event`
  - `anomaly_summary`
  - `ulog_mechanism_summary.csv`

一个已经出现的典型例子是：

- `windy pulse roll 0.10` 虽暂记为 `safe`
- 但其 `tracking_error_peak≈0.198`
- 已明显高于 nominal `pulse roll 0.10`

## 相关代码与配置

关键代码：

- `/home/car/autopilot_lab/src/fep_research/fep_research/analysis_runner.py`
- `/home/car/autopilot_lab/src/fep_research/fep_research/experiment_runner.py`

本轮 `windy` attitude 配置：

- `/home/car/autopilot_lab/src/fep_research/config/pulse_roll_010.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/pulse_roll_020.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/sweep_roll_010.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/sweep_pitch_005.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/sweep_pitch_010.yaml`

## 一次性构建

如果刚改过代码，先构建：

```bash
cd /home/car/autopilot_lab
source /opt/ros/humble/setup.bash
colcon build --packages-select fep_research --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
```

## 仅复现 analysis 汇总

如果 artifacts 已经存在，只需要跑：

```bash
source /opt/ros/humble/setup.bash
source /home/car/autopilot_lab/install/setup.bash
ros2 run fep_research analysis_runner --world-filter nominal
ros2 run fep_research analysis_runner --world-filter windy
```

运行后会生成：

```text
/home/car/autopilot_lab/artifacts/px4/analysis/<timestamp>_phase3_nominal/
/home/car/autopilot_lab/artifacts/px4/analysis/<timestamp>_phase3_windy/
```

重点看：

- `summary.md`
- `selected_runs.csv`
- `axis_layers.csv`
- `ulog_mechanism_summary.csv`
- `plots/attitude_overview.svg`
- `plots/manual_overview.svg`

如果要直接重跑 full fresh matrix：

```bash
source /opt/ros/humble/setup.bash
source /home/car/autopilot_lab/install/setup.bash
ros2 run fep_research matrix_runner --world default --force-timing-required
ros2 run fep_research matrix_runner --world windy --force-timing-required
```

## 复现 windy attitude anchor

先确认没有旧进程残留：

```bash
pgrep -af 'MicroXRCEAgent udp4 -p 8888|px4_sitl_default/bin/px4|gz sim|ros2 run fep_research experiment_runner'
```

然后准备 3 个终端。

### 终端 1：启动 Agent

```bash
source /opt/ros/humble/setup.bash
MicroXRCEAgent udp4 -p 8888
```

### 终端 2：启动 PX4 SITL + windy world

```bash
cd /home/car/PX4-Autopilot
PX4_GZ_WORLD=windy make px4_sitl gz_x500
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

## 推荐复现实验顺序

### 1. step roll 0.10

```bash
PX4_GZ_WORLD=windy ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/step_roll_010.yaml
```

### 2. step roll 0.15

```bash
PX4_GZ_WORLD=windy ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/step_roll_015.yaml
```

### 3. step roll 0.20

```bash
PX4_GZ_WORLD=windy ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/step_roll_020.yaml
```

### 4. pulse roll 0.10

```bash
PX4_GZ_WORLD=windy ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/pulse_roll_010.yaml
```

### 5. pulse roll 0.15

```bash
PX4_GZ_WORLD=windy ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/pulse_roll_015.yaml
```

### 6. pulse roll 0.20

```bash
PX4_GZ_WORLD=windy ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/pulse_roll_020.yaml
```

### 7. step pitch 0.10

```bash
PX4_GZ_WORLD=windy ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/step_pitch_010.yaml
```

### 8. step pitch 0.20

```bash
PX4_GZ_WORLD=windy ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/step_pitch_020.yaml
```

### 9. pulse pitch 0.10

```bash
PX4_GZ_WORLD=windy ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/pulse_pitch_010.yaml
```

### 10. pulse pitch 0.20

```bash
PX4_GZ_WORLD=windy ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/pulse_pitch_020.yaml
```

### 11. step pitch 0.15

```bash
PX4_GZ_WORLD=windy ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/step_pitch_015.yaml
```

### 12. pulse pitch 0.15

```bash
PX4_GZ_WORLD=windy ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/pulse_pitch_015.yaml
```

## 一个关键注意点

启动 PX4 时传 `PX4_GZ_WORLD=windy` 还不够。

运行 `experiment_runner` 时也必须显式传：

```bash
PX4_GZ_WORLD=windy ros2 run fep_research experiment_runner --config ...
```

否则 run 虽然实际发生在 `windy.sdf`，但 `manifest.yaml` 里的 `sim_world` 可能会被写成 `unspecified`，后续会污染 `analysis_runner --world-filter nominal` 的结果。

## windy run 的执行口径

现在做 `windy` anchor 时，默认按这个顺序执行：

1. 优先每组 anchor fresh 重启 `MicroXRCEAgent + PX4/GZ`。
2. 如果同一会话内连续跑，`experiment_runner` 会在起飞前检查当前位置的 XY 半径。
3. 默认阈值是 `prestart_max_xy_radius_m=5.0`，超限就直接记 `prestart_xy_radius_excessive`，`completion_reason=prestart_xy_gate_blocked`，本次 run 不再起飞。
4. 如果起飞前 `vehicle_local_position.xy_valid` 还没 ready，会记 `prestart_xy_unavailable`，同样停止在起飞前。

这一步不是为了判定控制边界，而是为了防止“上一组 run 的漂移落点污染下一组 run”。

## 每次 run 完成后看什么

每次 run 都会生成：

```text
/home/car/autopilot_lab/artifacts/px4/runs/<run_id>/
```

快速检查命令：

```bash
LATEST_RUN="$(ls -dt /home/car/autopilot_lab/artifacts/px4/runs/* | head -n 1)"
echo "${LATEST_RUN}"
cat "${LATEST_RUN}/metrics.csv"
sed -n '1,220p' "${LATEST_RUN}/manifest.yaml"
tail -n 80 "${LATEST_RUN}/notes.md"
```

重点看这些字段：

- `status`
- `sim_world`
- `prestart_xy_gate`
- `tracking_error_peak`
- `response_delay_ms`
- `failsafe_event`
- `anomaly_summary`

现在还应额外看：

- `start_xy_radius_m`
- `end_xy_radius_m`
- `xy_radius_peak_m`
- `xy_displacement_peak_m`

如果 `anomaly_summary` 中出现：

- `xy_radius_excessive`
- `xy_displacement_excessive`
- `start_xy_radius_excessive`
- `prestart_xy_radius_excessive`

则说明该 run 很可能已经受到风场下的位置累积漂移或可视地图边界污染。

## 复现完 anchor 后刷新分析

```bash
source /opt/ros/humble/setup.bash
source /home/car/autopilot_lab/install/setup.bash
ros2 run fep_research analysis_runner --world-filter nominal
ros2 run fep_research analysis_runner --world-filter windy
```

## 我当前采用的判断口径

当前 `windy` 下，我主要看这些信号：

- 是否 `status=completed`
- 是否出现 `failsafe_event=1`
- `tracking_error_peak` 是否明显高于 nominal 对应点
- 是否出现 `land_timeout_force_disarm`
- summary 的 `Axis Layers` 是否开始出现 `invalid`

## 当前结论

- 当前这批交付已经满足 **Phase 3 exit criteria**
- `windy` 数据集已经覆盖 attitude `step / pulse / sweep` 首轮 profile
- fresh `windy` 下，attitude `step roll 0.10/0.15/0.20` 全部为 `degraded`，并伴随 `~68-72 m` 的单次 run 内 XY 漂移
- fresh `windy` 下，attitude `pulse roll 0.10` 可复现 `invalid_runtime + failsafe_event=1`；`0.15/0.20` 虽能完成，也都只能记为 `degraded`
- 当前 `windy + attitude step/pulse roll` 已经看不到可信 `safe` 点
- fresh `windy` 下，attitude `step pitch 0.10/0.15/0.20` 也都只落在 `degraded`
- fresh `windy` 下，attitude `pulse pitch` 当前表现为 `0.10/0.15 -> degraded`, `0.20 -> invalid_runtime + failsafe_event=1`
- `sweep roll 0.15` 已进入 invalid，`sweep pitch` 的 invalid frontier 已下压到 `0.02`
- 最新 `windy` analysis 在 `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_073506_phase3_windy/`
- 最新 nominal analysis 在 `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_074448_phase3_nominal/`
- `analysis_runner` 当前会在同一 scenario 内优先选择最新 completed rerun，避免旧 run 覆盖 fresh frontier

因此后续更合理的动作是：

- 若继续扩展，更合理的是做机制解释、ULog 饱和分析或 full windy matrix，而不是继续把当前 Phase 3 当作未完成
- `manual pitch / composite` 的首轮 `windy` anchor 已补齐，后续若继续扩 manual，更合理的是更激进幅值而不是重复当前 safe 点
- `/clock` 仍留在 timing / phase 结论阶段再处理

## Phase 3 完成判断

- 当前已满足 `/home/car/autopilot_lab/TODO.md` 中的 `Phase 3 exit criteria`
- 因此本阶段现在应视为 **Phase 3 completed**
- 后续若继续做 `/clock` timing 恢复、ULog 饱和解析或 full windy matrix，应视为扩展工作，而不是当前 Phase 3 blocker

## 实验结束后的收尾

在 Agent 和 PX4 终端按 `Ctrl-C` 即可。

最后再确认没有残留进程：

```bash
pgrep -af 'MicroXRCEAgent udp4 -p 8888|px4_sitl_default/bin/px4|gz sim|ros2 run fep_research experiment_runner'
```
