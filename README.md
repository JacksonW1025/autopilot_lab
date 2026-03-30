# autopilot_lab

`autopilot_lab` 现在的默认状态是 `Dual-Backend M1` 分层实验平台。

- backend：PX4 + ArduPilot
- 主能力：`manual_whole_loop`、`attitude_explicit`、`rate_single_loop`
- 默认目标：可 bootstrap、可 doctor、可 fresh 批跑、可 strict 汇总

## M1 口径

- 当前里程碑：`dual_backend_m1`
- schema 版本：`2`
- capability：`manual_attitude_rate`
- 默认主汇总聚焦当前里程碑的 `accepted` runs
- 历史 runs 默认按 `legacy` 隔离，不进入主 summary

## 当前已验证状态

截至 `2026-03-30`，当前已经确认：

- `scripts/doctor_lab.sh` 返回 `status=ready`
- 已真实执行 `/home/car/autopilot_lab/scripts/smoke_lab.sh --backend all --repeat 1`
- 双 backend 的 6 组 canonical roll smoke 共 12 个新 run 全部进入 `accepted_runs.csv`
- `scripts/ci_minimal.sh` 已通过

精确的 artifact 路径、计数口径与当前边界统一见：

- `docs/M1_STATUS.md`

## 仓库结构

```text
autopilot_lab/
├── artifacts/
│   ├── ardupilot/
│   ├── px4/
│   └── studies/
├── docs/
├── scripts/
├── milestone.lock.json
└── src/
    ├── fep_core/
    ├── px4_ros2_backend/
    ├── ardupilot_mavlink_backend/
    ├── fep_research/
    ├── px4_msgs/
    └── px4_ros_com/
```

## 环境准备

首次环境准备：

```bash
/home/car/autopilot_lab/scripts/bootstrap_lab.sh
```

环境体检：

```bash
/home/car/autopilot_lab/scripts/doctor_lab.sh
```

最小 CI：

```bash
/home/car/autopilot_lab/scripts/ci_minimal.sh
```

只加载环境时：

```bash
source /home/car/autopilot_lab/scripts/autopilot_lab_env.sh
```

## 默认入口

PX4 单次实验：

```bash
ros2 run px4_ros2_backend px4_experiment_runner \
  --config /home/car/autopilot_lab/src/fep_research/config/layered_attitude_roll_010.yaml
```

PX4 matrix：

```bash
ros2 run px4_ros2_backend px4_matrix_runner \
  --world default \
  --pattern layered_manual_roll_020.yaml \
  --pattern layered_manual_roll_020_p120.yaml \
  --pattern layered_attitude_roll_010.yaml \
  --pattern layered_attitude_roll_010_p120.yaml \
  --pattern layered_rate_roll_010.yaml \
  --pattern layered_rate_roll_010_p120.yaml
```

ArduPilot 单次实验：

```bash
ros2 run ardupilot_mavlink_backend ardupilot_experiment_runner \
  --config /home/car/autopilot_lab/src/fep_research/config/layered_attitude_roll_010.yaml
```

ArduPilot matrix：

```bash
ros2 run ardupilot_mavlink_backend ardupilot_matrix_runner \
  --pattern layered_manual_roll_020.yaml \
  --pattern layered_manual_roll_020_p120.yaml \
  --pattern layered_attitude_roll_010.yaml \
  --pattern layered_attitude_roll_010_p120.yaml \
  --pattern layered_rate_roll_010.yaml \
  --pattern layered_rate_roll_010_p120.yaml
```

严格汇总：

```bash
ros2 run fep_core study_analysis_runner
```

显式纳入 legacy：

```bash
ros2 run fep_core study_analysis_runner --include-legacy
```

单独校验 artifacts：

```bash
ros2 run fep_core study_validate
```

## Canonical Smoke

M1 固定 6 组 canonical smoke：

- `layered_manual_roll_020.yaml`
- `layered_manual_roll_020_p120.yaml`
- `layered_attitude_roll_010.yaml`
- `layered_attitude_roll_010_p120.yaml`
- `layered_rate_roll_010.yaml`
- `layered_rate_roll_010_p120.yaml`

统一 smoke 入口：

```bash
/home/car/autopilot_lab/scripts/smoke_lab.sh --backend all --repeat 1
```

## Legacy 策略

- 缺 `schema_version` 或 `milestone_id` 的历史 runs 会被标成 `legacy`
- `legacy` 默认不进入 `accepted_runs.csv`
- 主 summary 默认只基于当前里程碑 `accepted` runs
- 本轮新 smoke run 过滤后没有 rejected，但全仓 `rejected_runs.csv` 当前并不为空
- 历史 artifacts 不删除、不自动迁移、不静默混入主结论

## 当前实现状态

- `manual_whole_loop`
  - PX4 / ArduPilot 都可运行
- `attitude_explicit`
  - PX4 / ArduPilot 都可运行
- `rate_single_loop`
  - 已进入 canonical roll smoke 并在 PX4 / ArduPilot 双 backend 上通过
  - 研究归因上仍按条件层使用，不把它写成 pitch/yaw/composite 已完成
- strict study analysis
  - 默认过滤 legacy 和 schema 不完整 runs
  - 全仓 `rejected_runs.csv` 可能包含旧 `legacy` 或未进入 accepted 的历史行
- backend-native CLI
  - 已作为默认入口保留
- `fep_research`
  - 继续保留兼容 shim，不再是默认 front door

## M1 验收标准

M1 完成的最低标准是：

- `bootstrap_lab.sh` 能完成依赖与构建
- `doctor_lab.sh` 返回 `status=ready`
- 双 backend 都能 fresh 跑完 6 组 canonical smoke
- 每个新 run 都带完整 `schema_version/milestone_id/capability_level`
- 默认 summary 不再出现空 `study_layer`
- PX4 不再产出 `rate_layer_not_implemented`

## 当前已达成结果

截至 `2026-03-30`，当前已达成：

- `/home/car/autopilot_lab/scripts/smoke_lab.sh --backend all --repeat 1` 已真实跑通
- 最新两份 matrix 各 6 行，全部 `status=completed`、`exit_code=0`
- 本轮 12 个新 run 过滤后为 `accepted=12`、`rejected=0`
- backend 分布为 `px4_ros2=6`、`ardupilot_mavlink=6`
- layer 分布为 `manual_whole_loop=4`、`attitude_explicit=4`、`rate_single_loop=4`
- 最新 study manifest 的全局计数是 `accepted=39`、`legacy=253`、`rejected=20`
- 上述全局计数不是“本轮 smoke 失败”，它是当前里程碑下的全仓汇总口径
- `scripts/ci_minimal.sh` 已通过
- 当前扩展顺序保持为：先补 pitch，再做 yaw/composite
