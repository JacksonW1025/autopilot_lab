# Dual-Backend M1 状态快照（截至 2026-03-30）

这份文档是当前 `Dual-Backend M1` 已验证状态的单一事实源。主入口文档只做摘要；涉及本轮真实 smoke、artifacts、accepted/rejected 计数与最小 CI 时，以本页为准。

## 当前结论

- `scripts/doctor_lab.sh` 已返回 `status=ready`
- 已真实执行 `/home/car/autopilot_lab/scripts/smoke_lab.sh --backend all --repeat 1`
- roll 三层 canonical smoke 已在 PX4 与 ArduPilot 双 backend 上跑通
- 本轮新产生的 12 个 run 过滤后全部进入 `accepted_runs.csv`，没有任何一个落入 `rejected_runs.csv`
- `scripts/ci_minimal.sh` 已通过
- 当前扩展顺序固定为：先补 pitch，再做 yaw/composite

## 本轮真实执行

执行命令：

```bash
/home/car/autopilot_lab/scripts/smoke_lab.sh --backend all --repeat 1
```

M1 固定 6 组 canonical 配置：

- `layered_manual_roll_020.yaml`
- `layered_manual_roll_020_p120.yaml`
- `layered_attitude_roll_010.yaml`
- `layered_attitude_roll_010_p120.yaml`
- `layered_rate_roll_010.yaml`
- `layered_rate_roll_010_p120.yaml`

## 最新产物位置

最新 matrix：

- PX4：`/home/car/autopilot_lab/artifacts/px4/matrix/20260330_022930_default/runs.csv`
- ArduPilot：`/home/car/autopilot_lab/artifacts/ardupilot/matrix/20260330_023431_ardupilot/runs.csv`

最新 study：

- `manifest.yaml`：`/home/car/autopilot_lab/artifacts/studies/20260330_023843_layered_sensitivity/manifest.yaml`
- `accepted_runs.csv`：`/home/car/autopilot_lab/artifacts/studies/20260330_023843_layered_sensitivity/tables/accepted_runs.csv`
- `rejected_runs.csv`：`/home/car/autopilot_lab/artifacts/studies/20260330_023843_layered_sensitivity/tables/rejected_runs.csv`

## 本轮 12 个新 run 的验收结果

本轮新 run 以两份 matrix `runs.csv` 中的 `artifact_dir` 为事实来源，再通过各自 `artifact_dir/manifest.yaml` 反查 `run_id`。

- PX4 matrix：6 行，全部 `status=completed`、`exit_code=0`
- ArduPilot matrix：6 行，全部 `status=completed`、`exit_code=0`
- 新 run 总数：12
- 过滤到这 12 个新 run 后：
  - `accepted=12`
  - `rejected=0`
- backend 分布：
  - `px4_ros2=6`
  - `ardupilot_mavlink=6`
- study layer 分布：
  - `manual_whole_loop=4`
  - `attitude_explicit=4`
  - `rate_single_loop=4`

## Study 全局计数说明

最新 study manifest 是当前里程碑口径下的全仓汇总，不是只统计这次 smoke 的 12 个新 run：

- `accepted_row_count=39`
- `legacy_row_count=253`
- `rejected_row_count=20`

这不表示“本轮 smoke 有 20 个失败 run”。它表示当前 `dual_backend_m1` 汇总时，全仓范围内仍存在历史 `legacy` 与未进入 accepted 的旧行。判断这轮 smoke 是否通过，必须以本页上面的“本轮 12 个新 run 过滤结果”为准。

## Manifest 完整性

本轮 12 个新 run 的 `manifest.yaml` 已核对通过：

- 顶层字段带齐：
  - `schema_version=2`
  - `milestone_id=dual_backend_m1`
  - `capability_level=manual_attitude_rate`
  - `study`
  - `parameter_snapshot_before`
  - `parameter_snapshot_after`
- `study` block 已带齐：
  - `study_family`
  - `study_layer`
  - `study_role`
  - `oracle_profile`
  - `mode_under_test`
  - `parameter_group`
  - `parameter_set_name`
  - `controlled_parameters`
  - `input_contract`
  - `output_contract`
  - `attribution_boundary`

## 最小 CI

最小 smoke-free 回归门已经落地并通过：

```bash
/home/car/autopilot_lab/scripts/ci_minimal.sh
```

脚本固定执行三项：

- `python3 -m pytest -q tests`
- 对 `src/`、`tests/`、`scripts/` 下所有 `.py` 做 `python3 -m py_compile`
- `scripts/doctor_lab.sh --help`

## 当前边界与下一步

- 当前已验证范围是 roll 三层双 backend，不提前把 pitch、yaw、composite 写成已完成
- `rate_single_loop` 已进入 canonical roll smoke 并通过，但在研究归因上仍是条件层
- 下一步顺序固定为：
  - 先补 pitch
  - 再做 yaw/composite
