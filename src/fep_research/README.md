# fep_research

面向 PX4 FEP Phase 1-3 的兼容 package。

当前仓库中真正的 PX4 ROS 2 实现已迁移到 `src/px4_ros2_backend/`，本包保留原有 `ros2 run fep_research ...` CLI 名称以兼容现有工作流、脚本和文档。

当前已实现：
- attitude 主链注入：`experiment_runner` + `attitude_injector`
- manual 输入链注入：`experiment_runner` + `manual_input_injector`
- 5 个标准 topic recorder：`telemetry_recorder`
- run artifacts 自动落盘：`manifest.yaml`、`notes.md`、`metrics.csv`、`telemetry/*.csv`
- attitude 基线与 step 配置
- attitude pulse / sweep 配置
- manual echo / flight / pulse / sweep 验证配置
- `analysis_runner` 跨 run 汇总：CSV + Markdown + SVG 图
- Gazebo `/clock` -> ROS `/clock` 本地 bridge：`gz_clock_bridge`
- ULog 解析与历史回填：`ulog_metrics` + `ulog_backfill`
- headless/fresh 扰动矩阵执行：`matrix_runner`

当前状态：
- `/clock` timing 口径已恢复到 `experiment_runner` / `matrix_runner`
- ULog 饱和指标已写入全部历史与新增 run 的 `metrics.csv`
- `windy` fresh matrix 已覆盖 `config/*.yaml` 的 40 组配置

## 目录

```text
src/fep_research/
├── README.md
├── package.xml
├── setup.py
├── setup.cfg
├── config/
│   ├── baseline_roll.yaml
│   ├── step_roll_010.yaml
│   ├── step_roll_015.yaml
│   ├── step_roll_020.yaml
│   ├── step_pitch_010.yaml
│   ├── step_pitch_015.yaml
│   ├── step_pitch_020.yaml
│   ├── pulse_roll_010.yaml
│   ├── pulse_roll_015.yaml
│   ├── pulse_roll_020.yaml
│   ├── pulse_pitch_010.yaml
│   ├── pulse_pitch_015.yaml
│   ├── pulse_pitch_020.yaml
│   ├── sweep_roll_010.yaml
│   ├── sweep_roll_015.yaml
│   ├── sweep_pitch_002.yaml
│   ├── sweep_pitch_005.yaml
│   ├── sweep_pitch_010.yaml
│   ├── manual_step_roll_020.yaml
│   ├── manual_step_throttle_020.yaml
│   ├── manual_flight_roll_020.yaml
│   ├── manual_flight_roll_040.yaml
│   ├── manual_flight_roll_060.yaml
│   ├── manual_flight_roll_080.yaml
│   ├── manual_flight_pulse_roll_040.yaml
│   ├── manual_flight_pulse_pitch_040.yaml
│   ├── manual_flight_sweep_roll_040.yaml
│   ├── manual_flight_sweep_pitch_040.yaml
│   ├── manual_flight_pitch_040.yaml
│   ├── manual_flight_pitch_060.yaml
│   ├── manual_flight_pitch_080.yaml
│   ├── manual_flight_yaw_040.yaml
│   ├── manual_flight_yaw_060.yaml
│   ├── manual_flight_yaw_080.yaml
│   ├── manual_flight_composite_moderate.yaml
│   ├── manual_flight_composite_aggressive.yaml
│   ├── manual_flight_composite_aggressive_t035.yaml
│   ├── manual_flight_throttle_030.yaml
│   ├── manual_flight_throttle_040.yaml
│   └── manual_flight_throttle_080.yaml
├── resource/
│   └── fep_research
└── fep_research/
    ├── __init__.py
    ├── gz_clock_bridge.py
    ├── matrix_runner.py
    ├── ulog_metrics.py
    ├── ulog_backfill.py
    ├── common.py
    ├── profiles.py
    ├── artifacts.py
    ├── metrics.py
    ├── attitude_injector.py
    ├── telemetry_recorder.py
    ├── experiment_runner.py
    ├── manual_input_injector.py
    └── analysis_runner.py
```

## 运行前置

1. `source /opt/ros/humble/setup.bash`
2. `source /home/car/autopilot_lab/install/setup.bash`
3. 单组实验可手动启动：
   - `MicroXRCEAgent udp4 -p 8888`
   - `cd /home/car/PX4-Autopilot && make px4_sitl gz_x500`
4. 若走 timing / headless 口径，推荐使用：
   - `gz sim -r -s /home/car/PX4-Autopilot/Tools/simulation/gz/worlds/default.sdf`
   - `PX4_GZ_STANDALONE=1 HEADLESS=1 make px4_sitl gz_x500`

`experiment_runner` 会在 ROS 侧 `/clock` 缺失时自动拉起 `gz_clock_bridge`。

## 构建

```bash
cd /home/car/autopilot_lab
colcon build --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo --symlink-install --packages-up-to fep_research
```

## attitude 复现

baseline:

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/baseline_roll.yaml
```

step:

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/step_roll_010.yaml
```

更多已验证 attitude 配置：

- `step_roll_020.yaml`
- `step_roll_015.yaml`
- `step_pitch_010.yaml`
- `step_pitch_015.yaml`
- `step_pitch_020.yaml`
- `pulse_roll_010.yaml`
- `pulse_roll_015.yaml`
- `pulse_roll_020.yaml`
- `pulse_pitch_010.yaml`
- `pulse_pitch_015.yaml`
- `pulse_pitch_020.yaml`
- `sweep_roll_010.yaml`
- `sweep_pitch_005.yaml`
- `sweep_pitch_010.yaml`

## manual echo 验证

当前 manual 链只验证：

- 输入：`/fmu/in/manual_control_input`
- 回显：`/fmu/out/manual_control_setpoint`

当前 manual run **不会**主动发送：

- arm
- offboard 切换
- takeoff
- land

所以飞机保持静止是当前阶段的预期行为，不算失败。

manual roll echo:

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_step_roll_020.yaml
```

manual throttle echo:

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_step_throttle_020.yaml
```

## manual flight 验证

`manual_mode=flight` 会先用 position offboard 起飞并悬停，再切到 `POSCTL + manual_control_input`，最后自动 `NAV_LAND`。

当前首个已通过的真实控制效果 run：

- `manual_flight_roll_040.yaml`
- artifact: `/home/car/autopilot_lab/artifacts/px4/runs/20260310_093511_manual_step_roll/`
- `status=completed`
- `response_delay_ms=7.651`
- `nav_state_change=0`
- `failsafe_event=0`
- step 窗口内 `max_xy_disp≈1.67 m`
- `manual_enabled=True`

复现命令：

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/manual_flight_roll_040.yaml
```

当前已补齐的 manual flight 配置：

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
- `manual_flight_pulse_roll_040.yaml`
- `manual_flight_pulse_pitch_040.yaml`
- `manual_flight_sweep_roll_040.yaml`
- `manual_flight_sweep_pitch_040.yaml`

## analysis 汇总

离线汇总当前 artifacts：

```bash
python3 -m fep_research.analysis_runner
```

或在已 source 的环境里：

```bash
ros2 run fep_research analysis_runner
```

查看 windy anchor：

```bash
ros2 run fep_research analysis_runner --world-filter windy
```

回填全部历史 run 的 ULog 指标：

```bash
ros2 run fep_research ulog_backfill
```

执行 full windy fresh matrix：

```bash
ros2 run fep_research matrix_runner --world windy --force-timing-required
```

执行 full nominal fresh matrix：

```bash
ros2 run fep_research matrix_runner --world default --force-timing-required
```

默认输出：

- `artifacts/px4/analysis/<timestamp>_phase3_nominal/summary.md`
- `artifacts/px4/analysis/<timestamp>_phase3_nominal/selected_runs.csv`
- `artifacts/px4/analysis/<timestamp>_phase3_nominal/nominal_completed_runs.csv`
- `artifacts/px4/analysis/<timestamp>_phase3_nominal/axis_layers.csv`
- `artifacts/px4/analysis/<timestamp>_phase3_nominal/plots/attitude_overview.svg`
- `artifacts/px4/analysis/<timestamp>_phase3_nominal/plots/manual_overview.svg`

说明：

- 选择逻辑默认按“激励场景”去重，而不是按完整 runtime 参数去重；同一场景若有多次 completed rerun，优先选择最新一组
- 默认 `--world-filter nominal`，避免 windy rerun 覆盖 nominal 数据集
- 需要看 windy anchor 时，显式传 `--world-filter windy`
- `matrix_runner` 现在支持 `default -> nominal` 的自动分析映射，因此 nominal fresh matrix 跑完后会直接生成 `phase3_nominal` 汇总
- `safe / degraded / invalid` 是第一版 operational layering，不等于最终论文结论
- 当前 plotting 直接输出 SVG，不依赖 GUI 或额外图形后端
- 当前 nominal 已完成一套 fresh/headless 的 timing-valid full matrix，最新汇总位于 `/home/car/autopilot_lab/artifacts/px4/analysis/20260313_043013_phase3_nominal/`
- 当前 windy 也已有 full fresh matrix，最新汇总位于 `/home/car/autopilot_lab/artifacts/px4/analysis/20260313_043013_phase3_windy/`
- 当前 `metrics.csv` / `manifest.yaml` / `notes.md` 已额外写入 `xy_radius` / `xy_displacement` 摘要，用于识别风场下的位置漂移与可能的地图边界污染
- 当前 `windy` run 默认启用起飞前 XY 半径 gate；若上一组 run 已把落点漂到远离原点的位置，新 run 会直接记 `prestart_xy_radius_excessive` 并停止在起飞前
- 最新 nominal fresh matrix 显示：
  - attitude `step/pulse roll/pitch` 目前 `0.10/0.15 -> safe`, `0.20 -> degraded`
  - `sweep pitch 0.02 -> safe`, `0.05/0.10 -> degraded`
  - `sweep roll 0.10 -> safe`, `0.15 -> degraded`
- 最新 windy fresh matrix 显示：
  - attitude `step/pulse roll/pitch` 目前基本全落在 `degraded`
  - `sweep pitch 0.10` 已进入 invalid frontier
  - ULog 机制统计可见 windy attitude 的 `clip_frac` 与 `max_unalloc_torque` 明显高于 nominal 与 manual

复现文档：

- Phase 1 单 run：
  - `/home/car/autopilot_lab/PHASE1_ATTITUDE_REPRO.md`
  - `/home/car/autopilot_lab/PHASE1_MANUAL_REPRO.md`
- Phase 2 logging：
  - `/home/car/autopilot_lab/PHASE2_REPRO.md`
- Phase 3 analysis / windy：
  - `/home/car/autopilot_lab/PHASE3_ANALYSIS_REPRO.md`

## 说明

- 第一版默认使用 body-angle + `thrust_body=[0.0, 0.0, hover_thrust]`
- `manual_mode=echo` 用于地面回显验证，飞机静止属于预期
- `manual_mode=flight` 用于验证 manual 对机体的真实控制效果
- `timing_required` 会决定是否把 `/clock` 缺失视为 blocker
- 做 `windy` anchor 时仍优先每组 fresh 重启 PX4/GZ；prestart gate 只是防止累计漂移污染后续 run 的下限保护
- 目前不自动复制 `.ulg`，只在 `manifest.yaml` 记录原始绝对路径
