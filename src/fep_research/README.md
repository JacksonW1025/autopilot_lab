# fep_research

`fep_research` 现在只是兼容入口层，不再承载仓库的主要研究实现。

当前真正的默认主线是分层敏感性研究：

- `manual_whole_loop`
- `attitude_explicit`
- `rate_single_loop`

本包继续保留旧的 `ros2 run fep_research ...` CLI 名称，避免现有脚本全部失效，但默认行为已经切到新的研究口径。

截至 `2026-03-30`，当前已确认：

- roll 三层 canonical smoke 已在双 backend 上真实跑通
- 本轮 12 个新 run 过滤后全部进入 accepted
- 详细状态、artifact 路径与当前边界统一见 `/home/car/autopilot_lab/docs/M1_STATUS.md`

当前更推荐直接使用 backend-native CLI：

- `ros2 run px4_ros2_backend px4_experiment_runner`
- `ros2 run px4_ros2_backend px4_matrix_runner`
- `ros2 run ardupilot_mavlink_backend ardupilot_experiment_runner`
- `ros2 run ardupilot_mavlink_backend ardupilot_matrix_runner`
- `ros2 run fep_core study_analysis_runner`

## 现在的入口含义

- `ros2 run fep_research experiment_runner`
  - 仍然运行 PX4 backend
- `ros2 run fep_research matrix_runner`
  - 仍然运行 PX4 matrix
- `ros2 run fep_research analysis_runner`
  - 已切换到新的跨 backend `study_analysis_runner`
  - 不再是旧的 PX4-only phase 汇总

## 默认配置

推荐直接使用新的分层配置：

- `config/layered_manual_roll_020.yaml`
- `config/layered_manual_roll_020_p120.yaml`
- `config/layered_attitude_roll_010.yaml`
- `config/layered_attitude_roll_010_p120.yaml`
- `config/layered_rate_roll_010.yaml`
- `config/layered_rate_roll_010_p120.yaml`

旧的 `baseline_* / step_* / pulse_* / sweep_* / manual_flight_*` 配置暂时保留，但应视为历史配置池，而不是新的默认实验口径。

说明：

- `rate_single_loop` 已进入 canonical roll smoke 并通过验收
- 研究扩展顺序仍是先补 pitch，再做 yaw/composite

## 常用命令

```bash
source /home/car/autopilot_lab/scripts/autopilot_lab_env.sh
```

PX4 manual：

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/layered_manual_roll_020.yaml
```

PX4 attitude：

```bash
ros2 run fep_research experiment_runner --config /home/car/autopilot_lab/src/fep_research/config/layered_attitude_roll_010.yaml
```

跨 backend 分层汇总：

```bash
ros2 run fep_research analysis_runner
```

最小 CI：

```bash
/home/car/autopilot_lab/scripts/ci_minimal.sh
```
