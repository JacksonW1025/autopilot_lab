# fep_research

`fep_research` 现在只是兼容入口层，不再承载仓库的主要研究实现。

当前真正的默认主线是分层敏感性研究：

- `manual_whole_loop`
- `attitude_explicit`
- `rate_single_loop` 按需引入

本包继续保留旧的 `ros2 run fep_research ...` CLI 名称，避免现有脚本全部失效，但默认行为已经切到新的研究口径。

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

旧的 `baseline_* / step_* / pulse_* / sweep_* / manual_flight_*` 配置暂时保留，但应视为历史配置池，而不是新的默认实验口径。

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
