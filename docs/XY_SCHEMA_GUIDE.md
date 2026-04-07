# X/Y Schema Guide

## X Schema

PX4 真实 raw run 默认采用“两级数据源”：

- 第一优先级：ROS/DDS 直录到 `telemetry/*.csv`
- 第二优先级：若整 topic 缺失，则从 `.ulg` 回填同名 CSV

因此 `full_augmented`、`tracking_error_response`、`actuator_response` 所依赖的 rate / actuator / internal signal 在 PX4 上不再要求 DDS 必须显式导出，只要 `.ulg` 中存在且时间基准可校准，就能进入后续 analysis。

平台内置这些 `X-schema`：

- `commands_only`
  - 只用 `command_roll/pitch/yaw/throttle`
- `commands_plus_state`
  - 在 command 基础上加入当前状态
- `commands_plus_state_history`
  - 在 command + state 基础上展开历史 lag
- `commands_plus_controller_params`
  - 把 run-level 参数广播为输入
- `commands_plus_state_plus_params`
  - command + state + 参数
- `pooled_backend_mode_augmented`
  - command + state + backend/mode/scenario/config_profile one-hot
- `full_augmented`
  - 再加入 internal signal 和 actuator feedback
- `feature_mapped_linear`
  - 在基础输入上做 clipped / squared / backend-gated feature map

### include / exclude groups

`x_include_groups` 和 `x_exclude_groups` 可进一步控制：

- `commands`
- `state`
- `controller_params`
- `backend_mode`
- `internal`
- `actuator_feedback`

## Y Schema

平台内置这些 `Y-schema`：

- `next_raw_state`
- `delta_state`
- `selected_state_subset`
  - `output_semantics: future_state` 时，对应 `future_state_<subset>`
  - `output_semantics: delta_state` 时，对应 `delta_state_<subset>`
  - `output_semantics: current_raw_state/raw_state` 时，才表示当前状态子空间
- `future_state_horizon`
- `actuator_response`
- `tracking_error_response`
- `window_summary_response`
- `stability_proxy_response`

### include / exclude groups

`y_include_groups` 和 `y_exclude_groups` 支持：

- `raw_state`
- `selected_state_subset`
- `actuator`
- `tracking_error`

## 严格 raw linear 与 feature-mapped linear

`feature_mapped_linear` 仍然使用线性拟合器，但拟合对象已经不是原始物理量本身，而是工程化特征空间。报告会显式标出它不属于 strict raw linear。

## Identifiability 规则

- sample-level varying feature 才能直接参与系数估计
- run-level covariate 只有在 study 中真的变化时才有识别意义
- 完全不变化的列会在拟合前自动剔除，并写入 `schema_inventory.yaml`
- pooled 模式会广播变化过的 run-level covariate
- stratified 模式按 `backend / mode / scenario / config_profile` 等条件拆分拟合
