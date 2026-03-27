# AGENTLOG.md

## 目标

把 `autopilot_lab` 从“PX4-only 激进输入实验仓”改造成“跨飞控的分层敏感性研究平台”，默认主线为：

- `manual_whole_loop`
- `attitude_explicit`
- `rate_single_loop` 按需引入

参考来源为 `~/RouthSearch` 的研究结构，而不是回退到旧的静态 PID 复现。

## 2026-03-27 本轮改造

### 1. 研究 schema 升级

- 扩展 `src/fep_core/fep_core/config.py`
- 新增字段：
  - `study_family`
  - `study_layer`
  - `study_role`
  - `oracle_profile`
  - `mode_under_test`
  - `parameter_group`
  - `parameter_set_name`
  - `parameter_overrides`
  - `controlled_parameters`
  - `input_contract`
  - `output_contract`
  - `attribution_boundary`
- 默认解析逻辑已支持：
  - `manual -> manual_whole_loop`
  - `attitude -> attitude_explicit`
  - `rate -> rate_single_loop`

### 2. 共享 study artifact

- `src/fep_core/fep_core/paths.py`
  - 新增 `STUDY_ARTIFACT_ROOT = artifacts/studies`
- `src/fep_core/fep_core/io.py`
  - 新增 `ensure_study_directories()`
- `src/fep_core/fep_core/study_analysis_runner.py`
  - 新增跨 backend study 汇总 CLI
  - 汇总输出：
    - `tables/merged_runs.csv`
    - `reports/summary.md`
    - `manifest.yaml`

### 3. 参数快照能力

- `src/fep_core/fep_core/mav_params.py`
  - 新增通用 MAVLink 参数工具：
    - `connect_mavlink`
    - `snapshot_parameters`
    - `set_parameters`
    - `close_mavlink`
- `src/fep_core/setup.py`
  - 增加 `pymavlink`
  - 增加 `study_analysis_runner` 入口

### 4. PX4 证据链升级

- `src/px4_ros2_backend/px4_ros2_backend/common.py`
  - 增补 attitude/rate/allocator/actuator 主题
- `src/px4_ros2_backend/px4_ros2_backend/telemetry_recorder.py`
  - 新增 CSV 落盘：
    - `vehicle_attitude_setpoint`
    - `vehicle_angular_velocity`
    - `vehicle_rates_setpoint`
    - `rate_ctrl_status`
    - `control_allocator_status`
    - `actuator_motors`
- `src/px4_ros2_backend/px4_ros2_backend/experiment_runner.py`
  - 已接入参数 `snapshot / apply / restore`
  - 已写入 `study` metadata
  - 已生成：
    - `oracle_valid`
    - `oracle_failure_reason`
    - `stress_class`
    - `mechanism_flags`
    - `rate_layer_recommended`
    - `rate_layer_reasons`
  - `rate_single_loop` 当前在 PX4 仍明确标记为条件层，不作为第一批默认 runner

### 5. ArduPilot 分层 runner 重写

- 完全替换 `src/ardupilot_mavlink_backend/ardupilot_mavlink_backend/experiment_runner.py`
- 默认支持：
  - `manual_whole_loop`
    - `GUIDED takeoff -> STABILIZE -> MANUAL_CONTROL -> LAND`
  - `attitude_explicit`
    - `GUIDED takeoff -> SET_ATTITUDE_TARGET -> LAND`
  - `rate_single_loop`
    - 已预留 body-rate 模式发送接口
- 已接入参数 `snapshot / apply / restore`
- 已写入 `study` metadata
- 已生成：
  - `oracle_valid`
  - `oracle_failure_reason`
  - `stress_class`
  - `mechanism_flags`
  - `rate_layer_recommended`

### 6. ArduPilot `.BIN` 离线解析

- 新增 `src/ardupilot_mavlink_backend/ardupilot_mavlink_backend/bin_log_metrics.py`
- 已支持解析并标准化导出：
  - `ATT`
  - `RATE`
  - `CTUN`
  - `MOTB`
  - `RCOU`
  - 可选 `PIDR / PIDP / PIDY`
- 已输出基础指标：
  - `tracking_error_peak`
  - `tracking_error_rms`
  - `response_delay_ms`
  - `rate_tracking_error_peak`
  - `rate_tracking_error_rms`
  - `clip_frac`
  - `thlimit_peak`
  - `max_motor_output`

### 7. 默认分析入口切换

- `src/fep_research/fep_research/analysis_runner.py`
  - 已不再转发到旧 PX4-only `analysis_runner`
  - 现在直接转发到 `fep_core.study_analysis_runner`
- `src/px4_ros2_backend/px4_ros2_backend/matrix_runner.py`
  - 自动汇总已切到新的 study 汇总

### 8. 新的分层配置

- 新增：
  - `src/fep_research/config/layered_manual_roll_020.yaml`
  - `src/fep_research/config/layered_manual_roll_020_p120.yaml`
  - `src/fep_research/config/layered_attitude_roll_010.yaml`
  - `src/fep_research/config/layered_attitude_roll_010_p120.yaml`
- 第一批参数组固定为 `roll_rate_pid`
- `P+20%` 采用：
  - PX4：`MC_ROLLRATE_P = 0.18`
  - ArduPilot：`ATC_RAT_RLL_P = 0.162`

### 9. 根文档替换

- 已重写：
  - `README.md`
  - `PJINFO.md`
  - `AGENTLOG.md`
- 顶层旧 Phase 文档已退出主入口，只保留在 `docs/`

## 验证

### 编译

已通过：

```bash
python3 -m compileall src/fep_core src/px4_ros2_backend src/ardupilot_mavlink_backend src/fep_research
```

### 配置与导入

已验证：

- 新分层配置可被 `RunConfig` 正确解析
- `study_metadata('px4')` / `study_metadata('ardupilot')` 能正确展开

### ArduPilot `.BIN` 解析

已用以下参考日志做离线验证：

- `/mnt/nvme/RouthSearch/routh_search/ardupilot/oracle_logs/base.BIN`

### Study 汇总

已成功生成新的 study artifact：

- `artifacts/studies/20260327_041108_layered_sensitivity/`

## 当前结论

- 仓库默认研究口径已经切到论文导向的分层主线
- 旧 PX4-only phase 叙事不再是默认入口
- `manual + attitude` 已成为并列主实验层
- `rate` 不再被默认忽略，但保持条件触发
- 当前仓库已经具备继续做 `roll_rate_pid` baseline / `P+20%` 对比的基础能力
