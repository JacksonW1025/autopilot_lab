# TODO.md

## 用途

这不是泛化 roadmap，而是面向后续 Agent 的 **PX4 FEP 阶段 1-3 执行手册**。目标是把后续工作固定为一条可复现、可审计、可逐步推进的实验流水线，用来回答下面两个核心问题：

1. 激进输入下，系统里哪些变量最先失真。
2. 系统从线性控制区进入危险包线边界的条件是什么。

## 非目标

- 第一版不修改 PX4 固件。
- 第一版不实现最终 FEP 保护器。
- 当前阶段不自行发散设计 FEP 方案；若导师后续给出保护策略方向，本仓库先负责把 `a x_t + b y_t = y_{t+1}` 的参数级敏感度证据准备出来。
- 第一版不直接产出论文级最终结论。
- 第一版不使用 `/fmu/in/actuator_motors` 直注入作为主实验路径，避免绕过控制层导致研究问题偏移。

## 当前可信基线

以下事实已经在当前机器上核过，后续工作默认以这些事实为准，而不是以旧文档的表述为准。

- 平台：Jetson AGX Orin 64G，Ubuntu 22.04 aarch64。
- 仿真链路：PX4 v1.15 SITL + ROS 2 Humble + Gazebo Harmonic。
- Gazebo 现状：当前机器仅保留 Harmonic；`gz sim --versions` 返回 `8.10.0`。
- PX4 SITL 核验脚本：`/home/car/run_fep_sim.sh`。
- 工作区当前仅有两个现成 package：
  - `src/px4_msgs`
  - `src/px4_ros_com`
- 当前工作区已有自定义研究 package `src/fep_research`，首版统一入口为 `ros2 run fep_research experiment_runner --config <yaml>`。
- PX4 Python offboard 参考实现位于：
  - `/home/car/autopilot_lab/src/px4_ros_com/src/examples/offboard_py/offboard_control.py`
- uXRCE-DDS 当前真实接口中：
  - 姿态主链输入：`/fmu/in/offboard_control_mode` + `/fmu/in/vehicle_attitude_setpoint`
  - 手动并行链输入：`/fmu/in/manual_control_input`
  - 不是 `/fmu/in/manual_control_setpoint`
- PX4 ULog 当前真实落点：
  - `/home/car/PX4-Autopilot/build/px4_sitl_default/rootfs/log/`
  - 不要写成 `~/PX4-Autopilot/log/`
- `2026-03-10` 复核：fresh `MicroXRCEAgent udp4 -p 8888` + `make px4_sitl gz_x500` 下，TODO 指定的 `/fmu/in` 与 `/fmu/out` topics 可见，但 `/clock` 未出现；当前 baseline/step 结果只能作为非 timing run 采信。
- 当前机器没有以下工具：
  - `PlotJuggler`
  - `ulog2csv`
  - `pyulog`
- 因此第一版统一采用“脚本优先，GUI 可选”的监控策略。

## 关键风险与防坑约束

### 风险 1：Sim-to-Real Gap

- Phase 1-3 产出的边界结论，统一表述为“基于当前仿真动力学与当前扰动设置的实验边界”，不要直接写成实机绝对安全边界。
- 当前 PX4 GZ world 中，`default.sdf` 与 `lawn.sdf` 的风场默认关闭；不要把“无风 world 下的边界”误写为“广义鲁棒边界”。
- 在名义边界跑通后，必须补一轮扰动鲁棒性重跑。第一选择是 `Tools/simulation/gz/worlds/windy.sdf`；如果 world 切换方式当次未打通，就在 artifacts 和结论中明确标记“仅无风名义条件有效”。

### 风险 2：线性模型局部有效、非线性区会崩溃

- 把导师给出的 `y_{t+1} = a x_t + b y_t` 只当作局部线性解释工具，不当作全工况真实模型。
- Phase 3 的目标不只是拟合线性区，还必须显式圈出“模型开始失真”和“非线性崩溃/奇点”区间。
- 后续任何分析脚本都不要把所有 aggressive data 强行塞进同一个线性拟合。

### 风险 3：Jetson Orin + ROS2 可能出现性能假象

- 后续自定义 package 的默认构建方式改为 `RelWithDebInfo`，不要继续沿用无显式 build type 的 `colcon build`。
- 每次用于时延分析的 run，必须额外记录主机侧性能快照，否则不能把观测到的延迟直接解释成物理极限。
- 如果出现 `/clock` 正常但 `Load Average` 异常飙升、节点明显卡顿、executor 堵塞，就把该 run 标为“系统负载污染”，不能用来下物理论断。

### 风险 4：Timing 结论依赖 lockstep 严格成立

- 时延、相位差、敏感延迟相关结论只允许建立在标准 lockstep SITL run 上。
- 统一使用 `make px4_sitl gz_x500` 作为 timing 分析入口，不使用 `px4_sitl_nolockstep`。
- 任何出现 `/clock` 冻结、回退、长时间停滞或明显跳变的 run，都直接标记为 timing invalid。

## 每次开工前必读

每次正式开始任何新实现前，先读下面三份文档，再决定是否继续：

1. `/home/car/autopilot_lab/PJINFO.md`
2. `/home/car/autopilot_lab/AGENTLOG.md`
3. `/home/car/autopilot_lab/reference/阶段工作总结与下一步研究计划.md`

## 执行硬规则

- 任何 `sudo`、安装新软件、修改系统配置的动作，都先向用户确认。
- 任何新增 package，默认补一个简短 `README.md`，解释用途、入口脚本和运行方式。
- 任何新增代码，默认加简洁中文注释，重点解释非显然逻辑。
- 单点问题最多自主尝试 3 次，仍未打通就向用户报告 blocker。
- 任何实验先做 live truth-check，再开始写研究代码。
- 任何 run 都必须生成完整 artifacts；没有 artifacts 的 run 视为无效。
- 任何阶段的完成判据没有满足，就不要进入下一阶段。

## Phase 0: Preflight & Truth Check

### 0.1 环境 source

每次新终端都先执行：

```bash
source /opt/ros/humble/setup.bash
source /home/car/autopilot_lab/install/setup.bash
```

### 0.2 逐项核验命令

#### Check A: Gazebo 版本

```bash
gz sim --versions
```

通过条件：

- 输出版本为 `8.10.0`
- 没有出现 `command not found`

#### Check B: Micro XRCE-DDS Agent 可执行

```bash
command -v MicroXRCEAgent
MicroXRCEAgent --help >/dev/null
```

通过条件：

- `MicroXRCEAgent` 在 `PATH` 中
- `--help` 至少能输出 usage；若返回码非 0 但 usage 正常且 agent 可启动，也按通过处理

#### Check C: 一键闭环核验

```bash
bash /home/car/run_fep_sim.sh
```

通过条件：

- `/clock` 上线
- `/clock` 时间推进
- `/fmu/out/vehicle_status` 可见
- 脚本最终打印 `Ready for Research (FEP)`

补充说明：

- `Check C` 主要用于 timing / sim-time 环境复核。
- 如果 `Check C` 仅因为 `/clock` 缺失而失败，但 `Check D` 已确认 PX4 SITL、XRCE-DDS 和核心 `/fmu/in|out` topics 正常，则仍允许继续 Phase 1 的 functional baseline / step run。
- 这类 run 必须在 `manifest.yaml` / `notes.md` 中明确标记 `clock_missing` 或 `timing invalid`，且结论只能用于功能性与误差观察，不能用于 timing 结论。

#### Check D: 手工 live truth-check

终端 1：

```bash
MicroXRCEAgent udp4 -p 8888
```

终端 2：

```bash
cd /home/car/PX4-Autopilot
make px4_sitl gz_x500
```

终端 3：

```bash
source /opt/ros/humble/setup.bash
source /home/car/autopilot_lab/install/setup.bash
ros2 topic list | rg '^/fmu/(in|out)/'
```

至少确认下列 topic 真实存在：

- `/fmu/in/offboard_control_mode`
- `/fmu/in/vehicle_attitude_setpoint`
- `/fmu/in/manual_control_input`
- `/fmu/out/vehicle_attitude`
- `/fmu/out/vehicle_local_position`
- `/fmu/out/vehicle_status`
- `/fmu/out/manual_control_setpoint`
- `/fmu/out/vehicle_control_mode`

通过条件：

- Gazebo 模型成功加载
- PX4 SITL 无明显启动错误
- 上述 topic 可见

### 0.3 当前工具缺口与 fallback

当前机器没有 `PlotJuggler` 与 `ulog2csv/pyulog`。这不是 Phase 0 的失败条件。

第一版 fallback 规则：

- 在线趋势观察：用自写 Python recorder 保存 ROS topic 片段，不依赖 GUI。
- 离线 ULog：先记录 `.ulg` 绝对路径，不阻塞输入生成链路开发。
- 若进入 Phase 3 时仍缺 ULog 解析器，则先完成 ROS 侧误差/延迟分析，并把 ULog 饱和指标标记为 `pending_ulog_parse`。

### 0.4 Lockstep 与 timing 门禁

时延/相位差类 run 统一遵守：

- 只用标准入口：

```bash
cd /home/car/PX4-Autopilot
make px4_sitl gz_x500
```

- 禁止使用 `px4_sitl_nolockstep`
- 禁止在 `/clock` 出现冻结、回退、长时间停滞时继续采信该 run

Timing 通过条件：

- `/clock` 单调推进
- `run_fep_sim.sh` 的时钟推进检查可复现通过
- SITL 未出现需要人工恢复的长时间卡顿

补充规则：

- `/clock` 是 timing-sensitive run 的硬门禁，不是 Phase 1 functional run 的硬门禁。
- 对当前 `attitude baseline / step` 首轮实验：
  - 若核心 FMU topics、ULog 和 artifact 落盘正常，即使 `/clock` 缺失，也允许继续执行
  - 但该 run 必须显式标记为 `non-timing`
- 只有当目标变成“时延、相位差、lockstep 有效性、sim-time 对齐结论”时，`/clock` 才重新成为必须通过的 gate。

### 0.5 主机性能快照

每个准备用于时延分析的 run，开始前和结束后都执行：

```bash
uptime
cat /proc/loadavg
```

记录要求：

- 把输出写入 `notes.md`
- 若 load 异常飙升但 topic 时间关系明显异常，则把该 run 标记为 `host_load_contaminated`

## 工作区落盘约定

### 目录约定

后续研究代码和结果统一落在以下位置：

```text
/home/car/autopilot_lab/
├── src/fep_research/
└── artifacts/
    └── runs/<run_id>/
```

第一版 `src/fep_research` 统一采用 Python-first 结构，至少包含：

```text
src/fep_research/
├── README.md
├── package.xml
├── resource/
├── setup.py
└── fep_research/
    ├── __init__.py
    ├── attitude_injector.py
    ├── manual_input_injector.py
    ├── telemetry_recorder.py
    ├── experiment_runner.py
    └── analysis_runner.py
```

后续自定义 package 的默认构建命令固定为：

```bash
cd /home/car/autopilot_lab
colcon build --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo --symlink-install --packages-up-to fep_research
```

### run_id 约定

统一使用以下格式：

```text
YYYYMMDD_HHMMSS_<chain>_<profile>_<axis>
```

示例：

```text
20260310_153000_attitude_step_roll
20260310_160500_manual_sweep_pitch
```

### 每次 run 的产物格式

每个 run 都必须生成：

```text
artifacts/runs/<run_id>/
├── manifest.yaml
├── notes.md
├── metrics.csv
├── telemetry/
│   ├── vehicle_attitude.csv
│   ├── vehicle_local_position.csv
│   ├── vehicle_status.csv
│   ├── manual_control_setpoint.csv
│   └── vehicle_control_mode.csv
└── plots/
```

`manifest.yaml` 必填字段：

- `run_id`
- `phase`
- `input_chain`
- `input_topic`
- `profile_type`
- `profile_params`
- `start_time`
- `end_time`
- `status`
- `px4_log_path`
- `ros_topics_recorded`
- `anomaly_summary`

`notes.md` 必填内容：

- 本次 run 的目的
- 操作人/Agent
- 观察到的异常
- 是否建议放大下一轮激励
- 主机性能快照（`uptime` + `/proc/loadavg`）
- 本次 run 是否可用于 timing 分析

`metrics.csv` 第一版至少包含这些列：

- `run_id`
- `input_chain`
- `profile_type`
- `axis`
- `input_peak`
- `input_rate_peak`
- `tracking_error_peak`
- `tracking_error_rms`
- `response_delay_ms`
- `nav_state_change`
- `failsafe_event`
- `ulog_saturation_metric`
- `ulog_parse_status`

### ULog 记录规则

- 不自动复制 `.ulg` 二进制文件。
- 只在 `manifest.yaml` 中记录原始 `.ulg` 的绝对路径。
- 查找 `.ulg` 的标准方法：
  - run 开始前记录一次 `rootfs/log/` 下的文件列表
  - run 结束后再次扫描
  - 选新增文件；若没有新增文件，则选最近修改时间最新的 `.ulg`

## Phase 1: Aggressive Input Generation

### 目标

建立两条可复现输入链，并统一支持 `step`、`sweep`、`pulse` 三类激励 profile。

### 总体策略

- 主链先做姿态注入链。
- 并行保留手动输入链，但不允许它拖慢主链闭环。
- 任何激励都先从保守幅值开始，再逐步放大。

### 1A. 姿态主链

主链固定为：

- `/fmu/in/offboard_control_mode`
- `/fmu/in/vehicle_attitude_setpoint`

辅助控制沿用 `px4_ros_com` Python offboard example 的模式：

- heartbeat
- arm
- mode switch
- 定时器驱动发布

实现要求：

- `attitude_injector.py` 必须复用 `offboard_control.py` 的结构，不从零设计控制节奏。
- `OffboardControlMode` 中默认开启 `attitude=True`。
- `VehicleAttitudeSetpoint` 必须显式填写：
  - `timestamp`
  - `roll_body` / `pitch_body` / `yaw_body` 或 `q_d`
  - `thrust_body`
- 第一版默认先用 body-angle + `thrust_body` 路线，不先做 quaternion-only 抽象。
- 初始 hover thrust 采用保守默认值，先从 `thrust_body=[0.0, 0.0, -0.5]` 起步，再依据 baseline 调整。

### 1B. 手动并行链

并行链固定为：

- `/fmu/in/manual_control_input`

不是：

- `/fmu/in/manual_control_setpoint`

实现要求：

- `manual_input_injector.py` 直接发布 `px4_msgs/msg/ManualControlSetpoint`
- 至少填充以下字段：
  - `timestamp`
  - `timestamp_sample`
  - `valid=True`
  - `data_source=SOURCE_MAVLINK_0`
  - `roll`
  - `pitch`
  - `yaw`
  - `throttle`
- 所有 stick 输入都保持在消息定义允许范围 `[-1, 1]`

并行链的可靠性规则：

- 先验证 `/fmu/out/manual_control_setpoint` 能真实回显输入，再做 aggressive profile。
- 如果手动链不能独立完成稳定起飞或模式切换，不要卡住整体工作。
- 此时允许先用姿态主链完成起飞/悬停验证，再单独验证手动链输入可达性。

### 1C. 统一 profile 接口

两条链都必须支持统一 profile schema：

- `profile_type`: `step | sweep | pulse`
- `axis`: `roll | pitch | yaw | throttle | composite`
- `amplitude`
- `bias`
- `start_after_s`
- `duration_s`
- `sample_rate_hz`

第一版默认 profile 梯度：

- attitude step: `0.10 -> 0.20 -> 0.35 -> 0.50 rad`
- manual step: `0.20 -> 0.40 -> 0.60 -> 0.80`
- pulse width: `0.20 s`
- sweep frequency: `0.20 -> 2.00 Hz`

推进规则：

- 上一档 run artifacts 完整且没有失控级异常，才允许进入下一档。
- 出现 mode 掉线、failsafe、SITL crash、ULog 丢失，立即停止放大。

### 1D. Phase 1 exit criteria

满足以下条件才算完成：

- `src/fep_research` package 建立完成
- 姿态主链至少成功执行 1 个 baseline + 1 个 step run
- 手动并行链至少验证过输入可达性
- `step`、`sweep`、`pulse` 三类 profile 的接口都已实现
- 每次 run 都能生成完整 artifacts

## Phase 2: Monitoring & Logging

### 目标

把每次激励输入、系统响应、日志位置和异常摘要稳定记录下来，为后续敏感度分析提供证据。

### 在线主观测量

第一版只把下面这些 topic 作为标准在线观测量：

- `/fmu/out/vehicle_attitude`
- `/fmu/out/vehicle_local_position`
- `/fmu/out/vehicle_status`
- `/fmu/out/manual_control_setpoint`
- `/fmu/out/vehicle_control_mode`

### 关键事实

`ActuatorMotors` 在当前 DDS 映射中不是在线输出观测量，因此：

- 电机饱和判断不能只靠在线 ROS 订阅
- 电机饱和判断以 ULog 为主数据源
- ROS topic 只承担在线趋势观察与快速 sanity check

### Recorder 默认实现

默认实现 `telemetry_recorder.py`，不要先上 `ros2 bag`。

Recorder 要求：

- 按固定 topic 各自落 CSV
- 每条记录保留 ROS 接收时间戳
- 对 `vehicle_status` 和 `vehicle_control_mode` 额外记录状态变化事件
- 在 run 结束时输出摘要到 `notes.md`

### 每次 run 需要保存的三类证据

#### 证据 A: 输入 profile

必须写入：

- `run_id`
- `profile_type`
- `profile_params`
- `input_topic`
- `start_time`
- `end_time`

#### 证据 B: ROS 侧关键 topic 片段

至少保存：

- 姿态响应
- 位置响应
- 模式状态
- 控制模式状态
- 手动链回显状态

#### 证据 C: ULog 路径与异常摘要

至少写入：

- `.ulg` 绝对路径
- 本次 run 是否成功找到 `.ulg`
- 是否发生模式异常
- 是否发生 topic 中断
- 是否发生 crash / restart

### 工具缺口的处理顺序

第一版处理顺序固定如下：

1. 先保证 ROS recorder 稳定可用
2. 再保证 `.ulg` 路径自动发现稳定可用
3. 最后在获得用户许可后补 ULog 解析工具

不要反过来做。

### Timing 结论的额外证据

如果某个 run 要被用于“延迟”“相位差”“通信瓶颈”结论，必须额外同时满足：

- `notes.md` 中有主机性能快照
- `/clock` 没有异常
- run 不是 `host_load_contaminated`

否则该 run 只能用于功能性观察，不能用于 timing 结论。

### Phase 2 exit criteria

满足以下条件才算完成：

- 在线 5 个标准 topic 都能稳定录制
- 每次 run 都能把 `.ulg` 绝对路径写入 manifest
- `notes.md` 能自动生成异常摘要
- recorder 不依赖 PlotJuggler 与 ULog CLI 就能完成基本采集
- 至少有一组 run 能同时提供 ROS 证据、ULog 路径和主机性能快照

## Phase 3: Sensitivity Analysis

### 目标

把 Phase 1 和 Phase 2 产物转成可比对的指标与图表，形成第一版线性区/非线性失效区判断。

### 最小指标集

第一版固定计算以下指标：

- 输入幅值 `input_peak`
- 输入变化率 `input_rate_peak`
- 姿态跟踪误差峰值 `tracking_error_peak`
- 姿态跟踪误差均方根 `tracking_error_rms`
- 响应延迟 `response_delay_ms`
- 模式切换事件 `nav_state_change`
- failsafe 或异常退出事件 `failsafe_event`
- ULog 饱和相关指标 `ulog_saturation_metric`

如果当前没有 ULog 解析器：

- `ulog_saturation_metric` 写 `pending_ulog_parse`
- `ulog_parse_status` 写 `missing_parser`
- 不阻塞 ROS 侧误差/延迟分析

### 指标计算默认口径

- 姿态主链误差：以输入 setpoint 与 `/fmu/out/vehicle_attitude` 的姿态差为准
- 手动并行链误差：以手动输入幅值与实际姿态变化趋势的对应关系为准
- 响应延迟：默认取输入第一次越过 10% 峰值，到实际响应幅值第一次越过阈值的时间差；若 10% 阈值未命中，可回退到 5% 峰值或 `0.002` 的最小阈值
- 模式异常：`VehicleStatus` 或 `VehicleControlMode` 出现非预期切换
- 线性模型只在局部区间解释数据；必须显式标记线性区与非线性失效区，禁止把全量数据做单一线性解释

### 固定实验顺序

严格按下面顺序推进：

1. `baseline`
2. `single-axis step`
3. `single-axis sweep`
4. `multi-axis aggressive case`

只有前一类实验 artifacts 完整、指标可计算，才进入下一类。

### 每一类实验的最低要求

#### baseline

- 无激进输入，仅保持稳定悬停或稳定受控状态
- 记录基础噪声、基础误差、基础模式状态

#### single-axis step

- 先 roll，再 pitch
- yaw 作为次优先项，放在 roll/pitch 打通后
- 每轴按预设梯度逐步放大

#### single-axis sweep

- 先低频，再高频
- 每次 sweep 只改一个主变量，避免一次引入多个自由度

#### multi-axis aggressive case

- 只在 single-axis 系列已经稳定产出指标后执行
- 第一版只做有限组合，不做组合爆炸

### 固定产出物

每组实验最终至少产出：

- 实验表格
- 误差曲线
- 延迟曲线
- 第一版线性区判断
- 第一版危险边界判断
- 下一轮实验参数建议

### 鲁棒性补充要求

在 nominal 条件下得到第一版边界后，补做一轮扰动重跑：

- 优先针对“最后一个安全点”和“第一个明显失效点”重跑
- 优先尝试切换到 `Tools/simulation/gz/worlds/windy.sdf`
- 如果 world 切换路径未在当次工作中打通，则在结论里明确声明“当前仅覆盖无风名义条件”

建议把图统一输出到：

```text
artifacts/runs/<run_id>/plots/
```

### Phase 3 exit criteria

满足以下条件才算完成：

- baseline、single-axis step、single-axis sweep、multi-axis aggressive case 都至少各有一组有效 run
- `metrics.csv` 列稳定、口径一致
- 至少能画出误差和延迟曲线
- 能给出第一版“线性区 / 非线性失效区”判断
- 能说明当前结论是在“无风 nominal”还是“已补扰动重跑”的条件下成立

## Phase 3.5: `a/b` 参数级敏感度辨识

### 目标

当前阶段的重点不是先做 FEP 方案，而是先把导师给出的局部线性视角真正落到可辨识的数据问题上：

```text
y_{t+1} = a x_t + b y_t
```

这里沿用导师记号：

- `a`：输入通道对下一时刻状态的有效影响
- `b`：当前状态对下一时刻状态的状态转移影响

本阶段要回答的不是“哪条 run 更差”，而是：

1. 在当前 hover-local 工况下，哪些 `a` / `b` 项对激进输入最敏感。
2. 这些项在 nominal 与 windy、低幅值与前沿幅值之间如何变化。
3. 什么时候局部线性模型本身开始失真，不能再继续拿 `a/b` 做解释。

### 当前进展

- [2026-03-16] `identification_dataset_builder` 已落地：
  - 最新数据集位于 `/home/car/autopilot_lab/artifacts/px4/identification/20260316_073813_nominal_attitude/`
  - 当前已导出 `18` 个 nominal timing-valid attitude runs、`7322` 条 sample-level rows
- [2026-03-16] `ab_fit_runner` 已落地：
  - 最新拟合目录位于 `/mnt/nvme/px4_work/px4_ws/artifacts/identification/20260316_073813_nominal_attitude/fit_20260316_075341/`
  - 当前已完成 `command_body / attitude_setpoint / rates_setpoint / torque_setpoint` 四类 `x_t` schema compare
- [2026-03-16] 第一版 nominal schema 选择已有初步结论：
  - `attitude_setpoint` 当前是最稳的 `x_t` 定义，`mean_loo_rmse=0.01265`、`mean_rollout_rmse=0.01917`
  - `rates_setpoint` 次之，`command_body` 虽然 one-step 误差尚可，但 rollout 发散，当前不能直接作为正式 `a`
- [2026-03-16] nominal repeat matrix 已完成：
  - `/home/car/autopilot_lab/artifacts/px4/matrix/20260316_080737_default/` 已完成 `step/pulse × roll/pitch × 0.05/0.10/0.15 × repeat=3`
  - 结果为 `36/36 completed`，说明这 12 个 operating points 在 fresh nominal + timing-valid 条件下具有很强的执行稳定性
- [2026-03-16] repeat-inclusive dataset / fit / uncertainty 已打通：
  - repeat 数据集位于 `/mnt/nvme/px4_work/px4_ws/artifacts/identification/20260316_083830_nominal_attitude_repeats/`，包含 `36` 个 runs、`13374` 条 samples
  - repeat 条件下的 schema compare 仍显示 `attitude_setpoint` 最稳：`mean_loo_rmse=0.00988`、`mean_rollout_rmse=0.02020`
  - uncertainty 目录位于 `/mnt/nvme/px4_work/px4_ws/artifacts/identification/20260316_083830_nominal_attitude_repeats/uncertainty_attitude_setpoint_20260316_083748/`
  - 当前各 operating point 的 pooled `mean_rollout_rmse` 约为 `0.0135 ~ 0.0213`，run-to-run `std_run_rollout_rmse` 约为 `0.00025 ~ 0.00468`

### 建议的阶段收口点

- 当前建议把这一版收口为 `Phase 3.5-v1: nominal schema freeze + repeat uncertainty`
- 这版的完成标志已经满足：
  - nominal clean set 已冻结
  - 第一版正式 `x_t` 已冻结为 `attitude_setpoint`
  - fixed operating point repeats 已完成并形成 uncertainty artifact
  - first-pass schema compare 与 validation 已形成
- 这版不必再等：
  - `effective input proxy` 对照拟合
  - `windy` coefficient validation
  - 跨环境 sensitivity shift compare
- 上面三项更适合作为下一版 `Phase 3.5-v2`，否则阶段边界会继续被拖模糊

### 当前还欠缺哪些关键条件

#### 缺口 1：`x_t / y_t / y_{t+1}` 还没有被正式冻结

当前 pipeline 更偏向边界分析，尚未把参数辨识对象固定下来。还缺：

- 第一版到底辨识哪一类局部模型：
  - attitude hover-local
  - manual hover-local
  - 含位置状态
  - 还是纯姿态/角速度状态
- `x_t` 到底取：
  - command profile
  - manual stick
  - 还是 allocator/actuator 之后的有效输入
- `y_t` 到底取：
  - 欧拉角
  - 角速度
  - 姿态 + 角速度联合状态
  - 还是再加位置/速度状态

如果这一步不先冻结，后面任何 `a/b` 结果都只是“看起来像辨识”，不是可复现的研究对象。

#### 缺口 2：当前缺少 identification-ready 的逐样本数据集

现在稳定产出的是：

- run-level `metrics.csv`
- `summary.md`
- selected/frontier CSV
- ULog 饱和与 attribution 摘要

这些足够回答边界和机理问题，但还不够直接做 `a/b` 拟合。当前仍缺：

- 固定采样周期的 `x_t, y_t, y_{t+1}` 表
- active window / recovery window / prefailsafe window 的逐样本切片
- command / state / ULog internal signals 的统一时间轴
- 用于 train / validate / repeat compare 的标准 dataset 目录

换句话说，当前“分析单位”还是 run，不是 sample。

#### 缺口 3：当前 recorder 的时序变量覆盖不足

目前 ROS recorder 固定录的是：

- `vehicle_attitude`
- `vehicle_local_position`
- `vehicle_status`
- `manual_control_setpoint`
- `vehicle_control_mode`

这足以做 boundary analysis，但对 `a/b` 辨识还不够。当前仍缺的关键时序变量包括：

- `vehicle_angular_velocity` 或等价角速度时序
- `vehicle_rates_setpoint`
- `vehicle_attitude_setpoint` 的统一对齐版本
- `actuator_motors`
- `control_allocator_status`
- 若 PX4 当前 ULog 中可用，则还应考虑 torque / thrust setpoint 相关量

没有这些变量，就很难把“命令输入”“飞控内部有效输入”“最终状态响应”区分开。

#### 缺口 4：当前没有把“commanded input”与“effective input”分开

对 `a x_t + b y_t = y_{t+1}` 来说，最大的陷阱是把 `x_t` 简单等同于 ROS 侧下发命令。

但在当前实验里，已经明确出现：

- motor clipping
- torque allocation limit
- thrust / torque achieved 下滑
- prefailsafe 阶段约束恶化

这意味着：

- command 并不等于真正进入飞行器动力学的有效输入
- aggressive 区和 windy 区尤其如此

如果不把 `x_t` 至少拆成 `commanded input` 与 `effective input proxy` 两层，那么 `a` 的物理含义会严重混淆。

#### 缺口 5：当前数据仍以“边界探索”为主，而不是“可辨识激励设计”为主

目前 step / pulse / sweep 很适合找 frontier，但不一定适合参数辨识。当前还缺：

- 局部线性区内的 persistently exciting 激励
- 低幅值、单轴、正负对称、可重复的辨识序列
- 更适合辨识的 PRBS / multi-sine / short orthogonal pulse 设计

否则很容易出现：

- 数据足够说明“会退化”
- 但不足以稳定估计某个 `a_{ij}` 或 `b_{ij}`

#### 缺口 6：当前 nominal 与 windy 的使用边界不同

当前 nominal 已洗净并统一 timing 口径，这是做第一阶段 `a/b` 辨识的基础。

但 windy 还存在：

- 少量历史 non-timing selected run
- 明显 `xy` 漂移污染
- failed / prefailsafe 主导的后段异常

因此当前还不能直接把 nominal 和 windy 混在一起拟合同一个 `a/b` 模型。更合理的是：

- 先在 nominal timing-valid run 上做第一版局部辨识
- 再把 windy 作为外扰/失配验证集
- 必要时再升级成 `a x_t + b y_t + w_t`

#### 缺口 7：当前还没有 repeat-based 的参数不确定性估计

当前 repeat matrix 已经能说明边界概率，但还没有说明：

- 同一工况下估计出的 `a/b` 系数方差多大
- 系数对 run-to-run 漂移有多敏感
- 系数变化是统计显著，还是只是噪声

所以现在还缺：

- 每个 operating point 的 repeated identification set
- coefficient confidence interval
- coefficient stability check

#### 缺口 8：当前没有固定的辨识评价标准

即使现在开始拟合，也还缺统一的 acceptance criteria。至少需要固定：

- one-step prediction RMSE
- multi-step rollout divergence
- coefficient sign / magnitude stability
- 不同 repeat 之间的 coefficient dispersion
- 与简单 baseline 模型相比的增益

没有这些指标，就无法判断“这个 `a/b` 拟合到底是不是可信”。

### 建议的第一阶段辨识范围

为了控制问题规模，第一阶段建议只做：

- `world = nominal`
- `timing-valid only`
- `attitude chain only`
- `hover-local only`
- 先不把位置状态并入主模型

建议第一版候选状态向量：

- `y_t = [roll, pitch, p, q]`

建议第一版候选输入向量：

- `x_t = [roll_cmd, pitch_cmd]`

原因很简单：

- 这组变量最贴近当前已有的 attitude 主链实验
- 能最大限度避开 windy 的位置污染
- 先做 roll/pitch attitude-local model，比一开始把 yaw / throttle / position 全塞进模型稳得多

manual 链不要和 attitude 链混做一个总模型。若后续要比较，应做：

- attitude-local `a/b`
- manual-local `a/b`

两套独立结果，再比较谁更敏感。

### 建议执行顺序

1. **先冻结模型对象**
   明确第一版只研究哪条链、哪个状态向量、哪个输入向量、哪个 operating point。

2. **补 identification-ready dataset builder**
   把 command profile、telemetry 和 ULog internal channels 对齐，输出固定采样率的 sample-level dataset。

3. **先补 recorder / ULog 变量覆盖**
   优先补角速度、rates setpoint、allocator、actuator 相关量；不要只拿 run summary 直接做辨识。

4. **补 phase segmentation 与 lag alignment**
   明确 warmup / active / recovery / prefailsafe，不允许把整段 run 混成一个拟合窗口。

5. **先做 nominal 局部模型，再谈 windy**
   windy 当前更适合拿来做模型失配与扰动验证，不适合直接作为第一版 `a/b` 主训练集。

6. **先做单轴局部辨识，再扩到双轴**
   roll-only、pitch-only 分开确认后，再进入联合状态模型。

7. **先做 one-step 预测，再做 sensitivity compare**
   模型自己先能稳定预测，才有资格谈“哪个参数更敏感”。

### 建议新增产物

当进入本阶段时，建议固定新增以下产物：

- `artifacts/px4/identification/<session>/dataset/`
- `artifacts/px4/identification/<session>/fit_summary.md`
- `artifacts/px4/identification/<session>/ab_coefficients.csv`
- `artifacts/px4/identification/<session>/ab_sensitivity.csv`
- `artifacts/px4/identification/<session>/validation_metrics.csv`

其中：

- `ab_coefficients.csv` 存每个 operating point 的 `a/b` 系数
- `ab_sensitivity.csv` 存不同环境/幅值下的系数变化量与排序
- `validation_metrics.csv` 存 RMSE、rollout error、repeat dispersion

### 当前不建议做的事

- 不要把 nominal + windy + failed run 混成一个总模型
- 不要把 active window 和 prefailsafe window 混成一个拟合窗口
- 不要直接用 frontier / invalid 数据去反推线性区 `a/b`
- 不要把 attitude 与 manual 链混成同一组系数
- 不要在没有 repeat 和 validation 的情况下宣称“某个参数最敏感”

### 本阶段完成判据

只有同时满足下面条件，才算真正进入了 `a/b` 参数级敏感度辨识：

- 已冻结第一版 `x_t / y_t / y_{t+1}` 定义
- 已能稳定导出 sample-level identification dataset
- 已有 nominal timing-valid 的 clean training set
- 已有至少一组 repeat-based validation set
- 已能输出可复现的 `a/b` 系数表和 validation 指标表
- 已能明确说明哪些系数变化来自：
  - 输入幅值变化
  - 环境变化
  - 污染/失效阶段变化

## 推荐执行顺序

为了降低返工，后续工作按下面顺序执行：

1. 先建 `src/fep_research` package 与 `README.md`
2. 先复用 `offboard_control.py`，打通姿态主链
3. 再做 `telemetry_recorder.py`
4. 再做 run artifact 目录和 manifest 自动写入
5. 再补手动并行链输入与回显验证
6. 再做 Phase 3 脚本化分析

不要一开始就做复杂分析器或 GUI 集成。

## 每次 work 完成后的收尾动作

每次完成一个有效 work session，都执行下面动作：

1. 更新 `/home/car/autopilot_lab/AGENTLOG.md`
2. 更新 `/home/car/autopilot_lab/PJINFO.md` 的【自动】段
3. 更新本文件的完成状态、下一个动作和 blocker
4. 确认本次新增 artifacts 路径已写入记录

## 2026-03-10 Work Session 状态

### 已完成

- `fep_research` 已按标准 `ament_python` package 配置修正，当前可正常 `ros2 run`
- attitude injector / profile / recorder / artifact 落盘主链已打通
- 有效 baseline run：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_064014_attitude_baseline_roll/`
- 有效 step run：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_064245_attitude_step_roll/`
- fresh baseline run：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_070244_attitude_baseline_roll/`
- fresh step run：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_071545_attitude_step_roll/`
- fresh `roll 0.20` run：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_072035_attitude_step_roll/`
- fresh `pitch 0.10` run：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_072151_attitude_step_pitch/`
- hybrid takeoff 重验证 baseline run：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_075735_attitude_baseline_roll/`
- hybrid takeoff 重验证 `roll 0.10` run：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_075831_attitude_step_roll/`
- hybrid takeoff 重验证 `roll 0.20` run：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_075919_attitude_step_roll/`
- baseline 当前结果：
  - `status=completed`
  - `nav_state_change=0`
  - `failsafe_event=0`
- step 当前结果：
  - `status=completed`
  - roll `0.10`：旧 run `response_delay_ms=2492.316`；重验证 run `response_delay_ms=83.828`
  - roll `0.20`：旧 run `response_delay_ms=1345.141`；重验证 run `response_delay_ms=93.598`
  - pitch `0.10`：`input_peak=0.1`，`response_delay_ms=1033.769`
  - `nav_state_change=0`
  - `failsafe_event=0`
  - `anomaly_summary=['clock_missing']`

### 下一个动作

- 在 hybrid takeoff 口径下补跑 `pitch 0.10 / 0.20 rad`，形成与 roll 对称的一组 attitude 数据
- 开始手动链可达性验证
- 单独排查 `/clock` 为什么在 fresh `gz_x500` run 下缺失，恢复 timing 口径

### 当前 blocker

- 当前没有阻塞 Phase 1 functional baseline / step 的 blocker
- `/clock` 在 fresh lockstep SITL run 下仍未出现，但它只阻塞 timing 结论，不阻塞当前功能性实验推进

## 当前待办清单

- [x] 建立 `src/fep_research` Python package
- [x] 复用 `offboard_control.py` 实现姿态主链 injector
- [x] 实现统一 profile schema
- [x] 实现 `telemetry_recorder.py`
- [x] 实现 run artifact 自动落盘
- [x] 验证 `/fmu/in/manual_control_input` 到 `/fmu/out/manual_control_setpoint` 的手动链可达性
- [x] 验证 `manual_control_input` 对机体的真实控制效果（`manual_mode=flight` / `roll 0.40`）
- [x] 建立第一版分析脚本与 `metrics.csv` 输出
- [x] 在 `AGENTLOG.md` / `PJINFO.md` 中持续同步真实进展

## 当前 blocker 记录

- [x] `/clock` 已通过本地 `gz_clock_bridge` 在 fresh/headless SITL 口径下恢复，可在 `experiment_runner` / `matrix_runner` 中自动拉起
- [x] 当前机器无 `PlotJuggler` 不再视为 blocker（recorder / analysis 已脱离其依赖）
- [x] `pyulog` 已就位，历史与新增 run 的 `ulog_saturation_metric` 已全部回填
- [x] `manual pitch / yaw / throttle` 的空中 flight 验证
- [x] 扰动 world / 风场重跑链路已实测打通

## 2026-03-10 补充记录（fresh preflight + baseline rerun）

### 新增有效产物

- fresh baseline run：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_070244_attitude_baseline_roll/`
- 本次 baseline 结果：
  - `status=completed`
  - `nav_state_change=0`
  - `failsafe_event=0`
  - `response_delay_ms=nan`
  - `anomaly_summary=['clock_missing']`

### 本次未继续的动作

- `0.10 rad` step 本次未重跑
- 原因是当时按旧门禁把 `/clock` 误当成了 functional step 的前置条件

### 对 `/clock` blocker 的最新收窄结果

- fresh `MicroXRCEAgent udp4 -p 8888` + `make px4_sitl gz_x500` 下：
  - TODO 指定的 8 个 `/fmu/in|out` topics 仍全部可见
  - ROS 2 中 `/clock` 默认不可见
- `gz topic -l` 显示 Gazebo 侧存在：
  - `/clock`
  - `/world/default/clock`
- 桥接尝试结果：
  - `ros_gz_bridge parameter_bridge /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock` 会持续打印 `Unknown message type [8] / [9]`
  - `ros_gz_bridge parameter_bridge /world/default/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock` 能建立 bridge，Gazebo 侧也能看到 subscriber
  - 但 ROS 侧 `/world/default/clock` 仍未收到实际 `Clock` 消息

### 下一个最小动作

- 先按 non-timing 口径继续 `step_roll_010.yaml`
- 再单独排查 `ros_gz_bridge` 对 `Clock` 的运行时异常，恢复 timing 口径

## 2026-03-10 补充记录（functional gate 调整 + fresh step rerun）

### 调整结果

- `/clock` 已从“Phase 1 functional run blocker”调整为“timing blocker”
- 当前 `baseline / step` 允许在 `clock_missing` 标记下继续执行
- 但所有 timing / phase / lockstep 结论仍必须等 `/clock` 真正可用后再采信

### 代码修正

- `fep_research.common.read_clock_topic_available()` 已改为真正读取 `/clock` 消息，不再只看 `topic list`
- `experiment_runner` 的 timing 判定已改为：
  - 先确认能收到 `/clock`
  - 再确认 `/clock` 在推进
- 因此后续 `notes.md` 中的 `Timing 分析可用性` 不会再被假阳性 topic 误判

### 新增有效产物

- fresh corrected step run：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_071545_attitude_step_roll/`

### 本次 fresh step 结果

- `status=completed`
- `input_peak=0.1`
- `response_delay_ms=2492.316`
- `nav_state_change=0`
- `failsafe_event=0`
- `anomaly_summary=['clock_missing']`
- `Timing 分析可用性 = no`

### 当前结论

- 现在已经没有必要继续让 `/clock` 阻塞当前 baseline / step 主实验
- 但 `/clock` 仍值得后续单独排查，因为它直接影响 timing 结论的可信度

## 2026-03-10 补充记录（roll 0.20 + pitch 0.10）

### 新增有效产物

- `roll 0.20`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_072035_attitude_step_roll/`
- `pitch 0.10`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_072151_attitude_step_pitch/`

### 本次结果

- `roll 0.20`：
  - `status=completed`
  - `input_peak=0.2`
  - `response_delay_ms=1345.141`
  - `tracking_error_peak=0.228273`
  - `tracking_error_rms=0.08127`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `pitch 0.10`：
  - `status=completed`
  - `input_peak=0.1`
  - `response_delay_ms=1033.769`
  - `tracking_error_peak=0.27559`
  - `tracking_error_rms=0.053984`
  - `nav_state_change=0`
  - `failsafe_event=0`

### 观察

- attitude 主链在 `roll 0.20` 与 `pitch 0.10` 下都未出现 mode 掉线或 failsafe
- 两个 run 都仍带有 `clock_missing`，因此依旧只按 non-timing 口径采信
- `pitch 0.10` 的 `tracking_error_peak` 明显高于 `roll 0.10`，后续建议补一档 `pitch 0.20` 再比较轴间差异

## 2026-03-10 补充记录（hybrid takeoff + roll 主链重验证）

### 触发原因

- 用户在 Gazebo 中观察到旧 `roll 0.20` 存在低空贴地、前翻接地后反弹
- 复核 telemetry 后确认旧 fixed-thrust 起飞/保持策略会生成低质量 run，因此旧 `roll 0.20` 不再作为首选参考

### 本次实现修正

- `attitude_injector.py` 起飞阶段已改为参考 `px4_ros_com/offboard_control.py` 的 `trajectory_setpoint` 位置控制
- warmup / takeoff 期间发布：
  - `/fmu/in/offboard_control_mode` with `position=True`
  - `/fmu/in/trajectory_setpoint`
- 达到目标高度并稳定后再切换到：
  - `/fmu/in/offboard_control_mode` with `attitude=True`
  - `/fmu/in/vehicle_attitude_setpoint`
- attitude 阶段新增轻量高度保持修正：
  - 以 `hover_thrust` 为基准
  - 用本地 `z` / `vz` 做 thrust 微调

### 本次新增有效产物

- baseline：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_075735_attitude_baseline_roll/`
- `roll 0.10`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_075831_attitude_step_roll/`
- `roll 0.20`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_075919_attitude_step_roll/`

### 本次结果

- baseline：
  - `status=completed`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `roll 0.10`：
  - `status=completed`
  - `input_peak=0.1`
  - `response_delay_ms=83.828`
  - `tracking_error_peak=0.099726`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `roll 0.20`：
  - `status=completed`
  - `input_peak=0.2`
  - `response_delay_ms=93.598`
  - `tracking_error_peak=0.19995`
  - `nav_state_change=0`
  - `failsafe_event=0`

### 当前结论

- 旧 `roll 0.20` 的低空贴地/反弹问题已被新的 hybrid takeoff 流程消掉
- 新 `roll 0.20` run 的 step 期间：
  - 最大 roll 约 `12.20 deg`
  - pitch 耦合仅约 `0.05 deg`
- 当前更合理的下一步是继续补 `pitch` 轴，而不是继续回头调起飞推力

## 2026-03-10 补充记录（hybrid takeoff + pitch 主链重验证）

### 本次新增配置

- `pitch 0.20`：
  - `/home/car/autopilot_lab/src/fep_research/config/step_pitch_020.yaml`

### 本次新增有效产物

- `pitch 0.10`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_080623_attitude_step_pitch/`
- `pitch 0.20`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_080711_attitude_step_pitch/`

### 本次结果

- `pitch 0.10`：
  - `status=completed`
  - `input_peak=0.1`
  - `response_delay_ms=69.776`
  - `tracking_error_peak=0.100126`
  - `tracking_error_rms=0.012211`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `pitch 0.20`：
  - `status=completed`
  - `input_peak=0.2`
  - `response_delay_ms=74.32`
  - `tracking_error_peak=0.200077`
  - `tracking_error_rms=0.024676`
  - `nav_state_change=0`
  - `failsafe_event=0`

### 观察

- 两个 `pitch` run 都仍带有 `anomaly_summary=['clock_missing']`，因此继续只按 non-timing 口径采信
- 两个 `pitch` run 都未出现 mode 掉线或 failsafe
- `pitch 0.10` 的 step 期间：
  - 最大 pitch 约 `5.66 deg`
  - roll 耦合仅约 `0.07 deg`
  - local `z` 约维持在 `-1.56 m ~ -1.48 m`
- `pitch 0.20` 的 step 期间：
  - 最大 pitch 约 `11.29 deg`
  - roll 耦合仅约 `0.06 deg`
  - local `z` 约维持在 `-1.07 m ~ -0.96 m`
- 至此 `roll 0.10 / 0.20` 与 `pitch 0.10 / 0.20` 已全部按 hybrid takeoff 口径完成重验证

### 下一步

- 开始验证 `manual_control_input` 主链
- `/clock` 继续只作为 timing / phase / lockstep 结论的专项 blocker

## 2026-03-10 补充记录（manual_control_input echo 验证）

### 本次实现边界

- 当前 manual 主链只验证：
  - `/fmu/in/manual_control_input`
  - `/fmu/out/manual_control_setpoint`
- 本次 run 不发送 arm / offboard / takeoff / land
- 因此实验期间飞机保持静止属于预期行为，不视为失败

### 本次新增配置

- `manual roll 0.20`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_step_roll_020.yaml`
- `manual throttle 0.20`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_step_throttle_020.yaml`

### 本次新增有效产物

- `manual roll 0.20`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_091844_manual_step_roll/`
- `manual throttle 0.20`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_091935_manual_step_throttle/`

### 本次结果

- `manual roll 0.20`：
  - `status=completed`
  - `input_peak=0.2`
  - `response_delay_ms=2.328`
  - `tracking_error_peak=0.0`
  - `tracking_error_rms=0.0`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual throttle 0.20`：
  - `status=completed`
  - `input_peak=0.2`
  - `response_delay_ms=2.826`
  - `tracking_error_peak=0.0`
  - `tracking_error_rms=0.0`
  - `nav_state_change=0`
  - `failsafe_event=0`

### 观察

- 两个 manual run 都仍带有 `anomaly_summary=['clock_missing']`，因此继续只按 non-timing 口径采信
- `/fmu/out/manual_control_setpoint` 已真实回显输入
- 两个 run 的回显 `data_source` 都为 `2`，即 `SOURCE_MAVLINK_0`
- `manual roll 0.20` 的回显峰值约为 `0.2`
- `manual throttle 0.20` 的回显峰值约为 `0.2`
- 当前这组 run 只能说明 manual 输入链路可达，不能说明 manual 已具备稳定飞行控制能力

### 下一步

- 若继续做地面 echo 验证，可补 `manual pitch / yaw`
- `manual 对机体的真实控制效果` 这一步已切换到 `manual_mode=flight` 完成首轮验证；后续应补 `pitch / yaw / throttle` 的空中 flight 验证

## 2026-03-10 补充记录（manual_control_input flight 验证）

### 本次实现方式

- `manual_mode=flight` 采用两段式流程：
  - 先参考 `px4_ros_com/offboard_control.py` 用 `position offboard + trajectory_setpoint` 起飞并悬停
  - 再切到 `POSCTL + manual_control_input`
- 本次 flight run 结束后自动 `NAV_LAND`

### 本次新增配置

- `manual flight roll 0.20`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_roll_020.yaml`
- `manual flight roll 0.40`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_roll_040.yaml`

### 本次新增有效产物

- `manual flight roll 0.40`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_093511_manual_step_roll/`

### 本次结果

- `manual flight roll 0.40`：
  - `status=completed`
  - `input_peak=0.4`
  - `response_delay_ms=7.651`
  - `nav_state_change=0`
  - `failsafe_event=0`

### telemetry 复核

- `vehicle_control_mode.csv` 可见 `flag_control_manual_enabled=True`
- `vehicle_status.csv` 可见 `nav_state=2 (POSCTL)`
- step 窗口内：
  - `max_xy_disp≈1.666858 m`
  - `max_abs_dz≈0.046167 m`
  - `max_roll_deg≈3.393`
  - `max_pitch_deg≈0.503`
- 当前可确认 manual 输入已经对机体运动产生真实影响，而不只是 echo

### 当前结论

- `manual_control_input` 已完成从“链路可达性验证”到“真实机体控制效果验证”的第一步收敛
- 当前这组 run 仍带有 `anomaly_summary=['clock_missing']`，因此继续只按 non-timing 口径采信
- 下一步更合理的是补齐其余主轴的 flight 验证，或开始进入更高幅值 / 更长 duration 的 manual 试验

## 2026-03-11 补充记录（manual pitch / yaw / throttle flight 验证）

### 本次新增配置

- `manual flight pitch 0.40`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_pitch_040.yaml`
- `manual flight yaw 0.40`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_yaw_040.yaml`
- `manual flight throttle 0.30`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_throttle_030.yaml`

### 本次新增有效产物

- `manual flight pitch 0.40`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_015041_manual_step_pitch/`
- `manual flight yaw 0.40`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_015137_manual_step_yaw/`
- `manual flight throttle 0.30`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_015241_manual_step_throttle/`

### 本次结果

- `manual flight pitch 0.40`：
  - `status=completed`
  - `response_delay_ms=2.675`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight yaw 0.40`：
  - `status=completed`
  - `response_delay_ms=1.653`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight throttle 0.30`：
  - `status=completed`
  - `response_delay_ms=10.712`
  - `nav_state_change=0`
  - `failsafe_event=0`

### telemetry 复核

- 三组 run 的 `vehicle_control_mode.csv` 均可见 `flag_control_manual_enabled=True`
- 三组 run 的 `vehicle_status.csv` 均可见 `nav_state=2 (POSCTL)`
- `manual flight pitch 0.40`：
  - `max_xy_disp≈1.489452 m`
  - `max_pitch_deg≈2.951`
- `manual flight yaw 0.40`：
  - `max_yaw_delta≈1.000160 rad`
  - `max_yaw_delta≈57.305 deg`
- `manual flight throttle 0.30`：
  - `max_abs_dz≈0.689530 m`
  - `z` 从约 `-1.476495 m` 到 `-2.168089 m`

### 当前结论

- 至此 `manual roll / pitch / yaw / throttle` 四个主轴都已完成首轮空中 real-effect validation
- 三组新增 run 仍带有 `anomaly_summary=['clock_missing']`，因此继续只按 non-timing 口径采信
- 下一步更合理的是进入更高幅值 / 更长 duration / composite manual profile，或补自动化分析摘要

## 2026-03-11 补充记录（manual 更高幅值 / 更长 duration）

### 本次新增配置

- `manual flight roll 0.60 / 4s`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_roll_060.yaml`
- `manual flight pitch 0.60 / 4s`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_pitch_060.yaml`
- `manual flight yaw 0.60 / 4s`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_yaw_060.yaml`
- `manual flight throttle 0.40 / 4s`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_throttle_040.yaml`

### 本次新增有效产物

- `manual flight roll 0.60 / 4s`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_025216_manual_step_roll/`
- `manual flight pitch 0.60 / 4s`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_025321_manual_step_pitch/`
- `manual flight yaw 0.60 / 4s`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_025417_manual_step_yaw/`
- `manual flight throttle 0.40 / 4s`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_025523_manual_step_throttle/`

### 本次结果

- `manual flight roll 0.60 / 4s`：
  - `status=completed`
  - `response_delay_ms=6.348`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight pitch 0.60 / 4s`：
  - `status=completed`
  - `response_delay_ms=12.919`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight yaw 0.60 / 4s`：
  - `status=completed`
  - `response_delay_ms=2.771`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight throttle 0.40 / 4s`：
  - `status=completed`
  - `response_delay_ms=5.676`
  - `nav_state_change=0`
  - `failsafe_event=0`

### telemetry 复核

- 四组 run 均可见 `flag_control_manual_enabled=True`
- 四组 run 均可见 `nav_state=2 (POSCTL)`
- `roll 0.60 / 4s`：
  - `max_xy_disp≈5.721606 m`
  - `max_roll_deg≈8.343`
- `pitch 0.60 / 4s`：
  - `max_xy_disp≈5.762712 m`
  - `max_pitch_deg≈7.832`
- `yaw 0.60 / 4s`：
  - `max_yaw_delta≈2.972098 rad`
  - `max_yaw_delta≈170.289 deg`
- `throttle 0.40 / 4s`：
  - `max_abs_dz≈1.499212 m`
  - `z` 从约 `-0.849481 m` 到 `-2.348693 m`

### 当前结论

- 当前 `manual flight` 在更高幅值 / 更长 duration 下仍未触发 `failsafe` 或 `nav_state_change`
- 这一轮仍全部带有 `anomaly_summary=['clock_missing']`，因此继续只按 non-timing 口径采信
- 下一步若继续放大，更合理的是进入 `0.80` 或 `composite`，但不应在同一工作段再继续无门槛加码

## 2026-03-11 补充记录（manual `0.80 / 4s` 单轴梯度）

### 本次新增配置

- `manual flight roll 0.80 / 4s`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_roll_080.yaml`
- `manual flight pitch 0.80 / 4s`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_pitch_080.yaml`
- `manual flight yaw 0.80 / 4s`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_yaw_080.yaml`
- `manual flight throttle 0.80 / 4s`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_throttle_080.yaml`

### 本次新增有效产物

- `manual flight roll 0.80 / 4s`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_032107_manual_step_roll/`
- `manual flight pitch 0.80 / 4s`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_032211_manual_step_pitch/`
- `manual flight yaw 0.80 / 4s`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_032310_manual_step_yaw/`
- `manual flight throttle 0.80 / 4s`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_032406_manual_step_throttle/`

### 本次结果

- `manual flight roll 0.80 / 4s`：
  - `status=completed`
  - `response_delay_ms=5.567`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight pitch 0.80 / 4s`：
  - `status=completed`
  - `response_delay_ms=2.839`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight yaw 0.80 / 4s`：
  - `status=completed`
  - `response_delay_ms=2.755`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight throttle 0.80 / 4s`：
  - `status=completed`
  - `response_delay_ms=4.645`
  - `nav_state_change=0`
  - `failsafe_event=0`

### telemetry 复核

- 四组 run 均可见 `flag_control_manual_enabled=True`
- 四组 run 均可见 `nav_state=2 (POSCTL)`
- `roll 0.80 / 4s`：
  - `max_xy_disp≈10.719555 m`
  - `max_roll_deg≈15.737`
- `pitch 0.80 / 4s`：
  - `max_xy_disp≈10.558043 m`
  - `max_pitch_deg≈15.230`
- `yaw 0.80 / 4s`：
  - `max_yaw_delta≈3.138149 rad`
  - `max_yaw_delta≈179.803 deg`
- `throttle 0.80 / 4s`：
  - `max_abs_dz≈5.234878 m`
  - `z` 从约 `-1.894797 m` 到 `-7.129675 m`

### 当前结论

- `manual 0.80 / 4s` 单轴梯度四组都已跑通，且仍未触发 `failsafe` 或 `nav_state_change`
- 但 `yaw 0.80 / 4s` 已接近 `180 deg`，`throttle 0.80 / 4s` 的 vertical excursion 已超过 `5 m`，说明当前已进入非常激进的包线边缘
- 本轮 run 仍全部带有 `anomaly_summary=['clock_missing']`，因此继续只按 non-timing 口径采信
- 下一步若继续推进，更合理的是 `composite` profile 或固定幅值下拉长 `duration`

## 2026-03-11 补充记录（manual composite profile）

### 代码修正

- `profiles.py` 已修正 `composite` 输出逻辑：
  - 只在 active phase 输出非零 stick
  - `roll/pitch/yaw/throttle` 分量统一由 `profile_value` 缩放
- `experiment_runner.py` 已补 `composite` 的 post-run gate：
  - 同时检查 `XY`、`yaw`、`z` 三类响应
- `metrics.py` 已补 `composite` 的聚合指标口径：
  - `input_peak` / `input_rate_peak` / `tracking_error_*` / `response_delay_ms` 都按多通道聚合

### 本次新增配置

- `manual flight composite moderate`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_composite_moderate.yaml`
- `manual flight composite aggressive`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_composite_aggressive.yaml`
- `manual flight composite aggressive t035`：
  - `/home/car/autopilot_lab/src/fep_research/config/manual_flight_composite_aggressive_t035.yaml`

### 本次新增有效产物

- `manual flight composite moderate`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_033558_manual_step_composite/`
- `manual flight composite aggressive t035`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_033822_manual_step_composite/`

### 本次无效产物

- `manual flight composite aggressive`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_033654_manual_step_composite/`
  - `status=invalid_runtime`
  - 原因：`manual_composite_z_not_observed`

### 本次结果

- `manual flight composite moderate`：
  - `status=completed`
  - `input_peak=0.25`
  - `response_delay_ms=4.977`
  - `nav_state_change=0`
  - `failsafe_event=0`
- `manual flight composite aggressive t035`：
  - `status=completed`
  - `input_peak=0.4`
  - `response_delay_ms=4.724`
  - `nav_state_change=0`
  - `failsafe_event=0`

### telemetry 复核

- `manual flight composite moderate`：
  - `max_xy_disp≈1.300192 m`
  - `max_abs_dz≈0.294022 m`
  - `max_yaw_delta≈0.447868 rad`
  - `max_yaw_delta≈25.661 deg`
- `manual flight composite aggressive`（无效 run）：
  - `max_xy_disp≈3.186113 m`
  - `max_abs_dz≈0.060398 m`
  - `max_yaw_delta≈0.648339 rad`
  - `max_yaw_delta≈37.147 deg`
- `manual flight composite aggressive t035`：
  - `max_xy_disp≈3.139198 m`
  - `max_abs_dz≈1.492419 m`
  - `max_yaw_delta≈0.595984 rad`
  - `max_yaw_delta≈34.147 deg`

### 当前结论

- `manual composite` 已打通：当前至少已有一组 `moderate` 和一组 `aggressive t035` 的有效 run
- 第一版 `aggressive` 失败不是因为 mode 掉线或 failsafe，而是因为 `throttle=0.20` 在组合输入下没能产生足够 `z` 响应
- 当前更合理的下一步是固定 `composite` 幅值后拉长 `duration`，或引入 `pulse / sweep` 风格的多通道 profile

## 2026-03-11 补充记录（analysis_runner + attitude pulse/sweep + windy anchor）

### 代码修正

- `analysis_runner.py` 已从占位入口改为真实分析器，当前支持：
  - 按激励场景去重
  - `--world-filter nominal|windy|all`
  - 输出 `summary.md`、`selected_runs.csv`、`nominal_completed_runs.csv`、`axis_layers.csv` 与 `plots/*.svg`
- `experiment_runner.py` 已把 `sim_world` 写入 `manifest.yaml` / `notes.md`
- `README.md` 已补 `analysis_runner` 用法与 world filter 说明

### 本次新增配置

- `/home/car/autopilot_lab/src/fep_research/config/pulse_roll_010.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/pulse_roll_020.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/sweep_roll_010.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/sweep_pitch_010.yaml`

### 本次新增 nominal artifacts

- `pulse roll 0.10`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_044939_attitude_pulse_roll/`
- `pulse roll 0.20`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_045019_attitude_pulse_roll/`
- `sweep roll 0.10`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_045059_attitude_sweep_roll/`
- `sweep pitch 0.10`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_045153_attitude_sweep_pitch/`

### nominal 关键结果

- `pulse roll 0.10`：
  - `status=completed`
  - `tracking_error_peak=0.100003`
  - `response_delay_ms=89.471`
- `pulse roll 0.20`：
  - `status=completed`
  - `tracking_error_peak=0.200138`
  - `response_delay_ms=85.010`
- `sweep roll 0.10`：
  - `status=completed`
  - `tracking_error_peak=0.156932`
  - `tracking_error_rms=0.045859`
  - `response_delay_ms=194.073`
- `sweep pitch 0.10`：
  - `status=completed`
  - `tracking_error_peak=0.136987`
  - `tracking_error_rms=0.039033`
  - `response_delay_ms=97.442`

### 第一版 analysis 产物

- nominal:
  - `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_045919_phase3_nominal/`
- windy:
  - `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_045919_phase3_windy/`

### nominal 当前结论

- `world_filter=nominal` 下共选中 27 组 run，其中 completed=25
- attitude `step/roll 0.20`、`step/pitch 0.20`、`pulse/roll 0.20` 当前都已进入 `degraded`
- attitude `sweep roll 0.10` 与 `sweep pitch 0.10` 当前暂仍处于 `safe`
- manual 单轴 `0.80` 与 composite `0.40` 当前仍是 nominal 探索前沿

### 本次新增 windy anchor artifacts

- `attitude step roll 0.10`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_045447_attitude_step_roll/`
- `attitude step roll 0.20`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_045535_attitude_step_roll/`
- `manual flight roll 0.80`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_045617_manual_step_roll/`
- `manual flight composite aggressive t035`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_045705_manual_step_composite/`

### windy 关键结果

- `attitude step roll 0.10`：
  - `status=invalid_runtime`
  - `failsafe_event=1`
  - `tracking_error_peak=0.245886`
- `attitude step roll 0.20`：
  - `status=completed`
  - `anomaly_summary=['clock_missing', 'land_timeout_force_disarm']`
- `manual flight roll 0.80`：
  - `status=invalid_runtime`
  - `takeoff_clearance_timeout`
  - `manual_window_missing`
- `manual flight composite aggressive t035`：
  - `status=invalid_runtime`
  - `takeoff_clearance_timeout`
  - `manual_window_missing`

### 当前结论

- 第一版 analysis_runner 已经把现有 nominal run 变成了可比对的表和图，不再只是零散 artifacts
- 当前 nominal/no-wind 与 windy 结果已经明显分叉；nominal 边界不能直接当作扰动鲁棒边界
- 下一步更合理的是：
  - 继续补 manual `pulse / sweep`
  - 再扩 `windy` 下的少量 sweep / pulse anchor
  - `/clock` 仍留在 timing 结论阶段再处理

## 2026-03-11 补充记录（manual pulse/sweep + windy 对应 anchor）

### 代码修正

- `experiment_runner.py` 已把 manual flight 的有效实验窗口判定从只识别 `step_active` 改为同时识别：
  - `step_active`
  - `pulse_active`
  - `sweep_active`
- 新增无效原因：
  - `manual_profile_window_missing`
- 这样 manual `pulse / sweep` 不再因为 profile 名称不匹配而被误判为窗口缺失

### 本次新增配置

- `/home/car/autopilot_lab/src/fep_research/config/manual_flight_pulse_roll_040.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/manual_flight_pulse_pitch_040.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/manual_flight_sweep_roll_040.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/manual_flight_sweep_pitch_040.yaml`

### 配置门禁修正

- 首轮 `manual pulse roll 0.40` 曾出现两次无效尝试：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_050855_manual_pulse_roll/`
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_050949_manual_pulse_roll/`
- 复核后确认短 pulse 在有效窗口内仍有真实位移，但量级只有约 `0.029 m`
- 因此已把 pulse 配置修正为：
  - `pulse_width_s=0.50`
  - `manual_motion_min_displacement_m=0.02`
- 该修正的含义是：manual `pulse` 不再沿用适合长 step 的旧位移门禁

### 本次新增 nominal artifacts

- `manual pulse roll 0.40`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_051051_manual_pulse_roll/`
- `manual pulse pitch 0.40`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_051131_manual_pulse_pitch/`
- `manual sweep roll 0.40`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_051213_manual_sweep_roll/`
- `manual sweep pitch 0.40`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_051256_manual_sweep_pitch/`

### nominal 关键结果

- `manual pulse roll 0.40`：
  - `status=completed`
  - `input_peak=0.4`
  - `response_delay_ms=7.664`
- `manual pulse pitch 0.40`：
  - `status=completed`
  - `input_peak=0.4`
  - `response_delay_ms=1.327`
- `manual sweep roll 0.40`：
  - `status=completed`
  - `input_peak=0.399999`
  - `response_delay_ms=5.637`
- `manual sweep pitch 0.40`：
  - `status=completed`
  - `input_peak=0.4`
  - `response_delay_ms=7.153`

### 本次新增 windy anchor artifacts

- `manual pulse roll 0.40`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_051414_manual_pulse_roll/`
- `manual sweep roll 0.40`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_051502_manual_sweep_roll/`

### windy 关键结果

- `manual pulse roll 0.40`：
  - `status=completed`
  - `input_peak=0.4`
  - `response_delay_ms=3.096`
- `manual sweep roll 0.40`：
  - `status=completed`
  - `input_peak=0.399988`
  - `response_delay_ms=10.123`

### 最新分析产物

- nominal:
  - `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_051702_phase3_nominal/`
- windy:
  - `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_051702_phase3_windy/`

### 当前结论

- nominal 数据集现在已覆盖：
  - attitude `baseline / step / pulse / sweep`
  - manual `step / pulse / sweep`
- manual `pulse/sweep` 已不再只是待补项，而是已进入第一版 nominal summary
- `windy` 下 manual `pulse/sweep roll 0.40` 可以完成，但 `step roll 0.80` 与 `composite aggressive t035` 仍会在有效实验窗口前失败
- 因此当前扰动结论已经明显表现为：
  - 不是“manual 一律更鲁棒”
  - 而是“风场影响与 profile、起飞阶段稳定性和窗口进入条件强相关”
- 当前全部已完成 run 仍带 `clock_missing`；以上结论继续只适用于 functional / non-timing

### 下一步

- 优先补 `windy` 下的 attitude `pulse / sweep` anchor
- 再决定是否补更多 manual `pitch` / `composite` 扰动点
- `/clock` 继续留到 timing / phase 结论阶段再处理

## 2026-03-11 补充记录（windy attitude pulse/sweep anchor）

### 运行修正

- `20260311_052601_attitude_pulse_roll` 实际运行在 `windy.sdf`
- 仅因启动 `experiment_runner` 时没有显式传入 `PX4_GZ_WORLD=windy`，导致 `manifest.yaml` 里的 `sim_world` 初始写成 `unspecified`
- 该 run 的 `manifest.yaml` / `notes.md` 已补正为 `windy`
- 这一步很重要，因为 `analysis_runner` 的 world filtering 完全依赖 `manifest.yaml`

### 本次新增 windy artifacts

- `attitude pulse roll 0.10`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_052601_attitude_pulse_roll/`
- `attitude pulse roll 0.20`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_052706_attitude_pulse_roll/`
- `attitude sweep roll 0.10`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_052759_attitude_sweep_roll/`
- `attitude sweep pitch 0.10`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_052856_attitude_sweep_pitch/`

### windy 关键结果

- `attitude pulse roll 0.10`：
  - `status=completed`
  - `tracking_error_peak=0.198241`
  - `tracking_error_rms=0.079284`
  - `response_delay_ms=11.183`
- `attitude pulse roll 0.20`：
  - `status=completed`
  - `tracking_error_peak=0.202775`
  - `tracking_error_rms=0.029930`
  - `response_delay_ms=62.269`
- `attitude sweep roll 0.10`：
  - `status=completed`
  - `tracking_error_peak=0.173096`
  - `tracking_error_rms=0.076127`
  - `response_delay_ms=4.601`
- `attitude sweep pitch 0.10`：
  - `status=invalid_runtime`
  - `tracking_error_peak=0.169572`
  - `tracking_error_rms=0.063970`
  - `response_delay_ms=2.782`
  - `failsafe_event=1`
  - `anomaly_summary=['clock_missing', 'land_timeout_force_disarm']`

### 最新分析产物

- nominal:
  - `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_053059_phase3_nominal/`
- windy:
  - `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_053059_phase3_windy/`

### 最新 windy analysis 结论

- 当前 `world_filter=windy` 下已选 run 共 `10` 组，其中 completed=`6`
- `attitude:pulse` 与 `attitude:sweep` 已不再是 windy 数据集的 profile 缺口
- 当前 windy attitude layering 为：
  - `step/roll 0.20 -> degraded`
  - `pulse/roll 0.10 -> safe`
  - `pulse/roll 0.20 -> degraded`
  - `sweep/roll 0.10 -> safe`
  - `sweep/pitch 0.10 -> invalid`

### 解释注意事项

- `safe / degraded / invalid` 仍只是第一版 operational layering
- `windy pulse roll 0.10` 虽被标成 `safe`，但其 `tracking_error_peak≈0.198` 已明显高于 nominal `pulse roll 0.10`
- 因此后续写结论时不能只引用 layer，还必须同时引用：
  - 绝对误差
  - 是否出现 `failsafe_event`
  - 是否出现 `land_timeout_force_disarm`

### 当前结论

- 当前 `windy` 数据集已经覆盖 attitude `step / pulse / sweep` 首轮 profile
- 但动态包线已开始表现出 profile 依赖：
  - `pulse roll 0.10/0.20` 可以完成，但误差显著抬升
  - `sweep roll 0.10` 可以完成
  - `sweep pitch 0.10` 已出现 `invalid_runtime`
- 因此下一轮 windy 扰动研究应优先考虑：
  - 更系统的 `attitude sweep` 轴向补点
  - manual `pitch/composite` 扰动点
  - 最后才是 timing / `/clock`

## 2026-03-11 补充记录（阶段归属 + Phase 3 REPRO）

### 阶段判断

- 当前主工作已不是 Phase 1
- 当前更准确的表述是：
  - `Phase 3 completed`
- 判断依据：
  - 现在的主工作已经从“输入链打通与单 run 验证”
  - 转向“跨 run analysis、nominal/windy 对比、frontier layering 与扰动解释”
- 这些都对应本文件中的：
  - `## Phase 3: Sensitivity Analysis`

### 新增复现文档

- 已新增：
  - `/home/car/autopilot_lab/PHASE3_ANALYSIS_REPRO.md`

### 当前复现入口约定

- Phase 1 主链与单 run 复现：
  - `/home/car/autopilot_lab/PHASE1_ATTITUDE_REPRO.md`
  - `/home/car/autopilot_lab/PHASE1_MANUAL_REPRO.md`
- Phase 3 analysis / windy 复现：
  - `/home/car/autopilot_lab/PHASE3_ANALYSIS_REPRO.md`

### 当前要求

- 后续如果继续做：
  - `analysis_runner`
  - nominal / windy summary 刷新
  - windy anchor rerun
- 默认按 Phase 3 work 记录，不再混写成 Phase 1

## 2026-03-11 补充记录（Phase 3 完成复核）

### 结论

- 当前判断：
  - `Phase 3 已完成`

### 对照 exit criteria 的复核结果

- 已满足本文件 `Phase 3 exit criteria`：
  - baseline、single-axis step、single-axis sweep、multi-axis aggressive case 均已有至少一组有效 run
  - `metrics.csv` 已稳定落盘，nominal / windy 口径一致
  - `analysis_runner` 已稳定输出误差/延迟表和 `plots/*.svg`
  - nominal / windy summary 已给出第一版 `safe / degraded / invalid` layering
  - 当前结论已明确区分 nominal 与 windy，不再混写成单一边界

### 当前正式参考分析目录

- nominal：
  - `/home/car/autopilot_lab/artifacts/px4/analysis/20260313_031312_phase3_nominal/`
- windy：
  - `/home/car/autopilot_lab/artifacts/px4/analysis/20260313_031312_phase3_windy/`

### 说明

- `Phase 3 已完成` 指的是首版 sensitivity analysis 与 frontier layering 已收口
- `/clock` timing、ULog 解析与 full windy matrix 已在 `2026-03-13` 收口；nominal 历史 run 仍保持 non-timing 口径，不会 retroactive 变成 timing-valid

## 2026-03-11 补充记录（Phase 2 完成 + REPRO）

### 结论

- 当前判断：
  - `Phase 2 已完成`

### 判断依据

- 已满足本文件 `Phase 2 exit criteria`：
  - 在线 5 个标准 topic 都能稳定录制
  - 每次 run 都能把 `.ulg` 绝对路径写入 manifest
  - `notes.md` 能自动生成异常摘要
  - recorder 不依赖 PlotJuggler 与 ULog CLI
  - 至少已有一组 run 同时提供 ROS 证据、ULog 路径和主机性能快照

### 代表性参考 run

- attitude:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_075831_attitude_step_roll/`
- manual:
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260310_093511_manual_step_roll/`

### 新增复现文档

- `/home/car/autopilot_lab/PHASE2_REPRO.md`

### 当前复现入口约定

- Phase 1:
  - `/home/car/autopilot_lab/PHASE1_ATTITUDE_REPRO.md`
  - `/home/car/autopilot_lab/PHASE1_MANUAL_REPRO.md`
- Phase 2:
  - `/home/car/autopilot_lab/PHASE2_REPRO.md`
- Phase 3:
  - `/home/car/autopilot_lab/PHASE3_ANALYSIS_REPRO.md`

## 2026-03-11 补充记录（windy position drift / boundary contamination）

### 新增配置

- `/home/car/autopilot_lab/src/fep_research/config/sweep_pitch_005.yaml`

### 新增代码口径

- `metrics.csv` 已新增：
  - `start_xy_radius_m`
  - `end_xy_radius_m`
  - `xy_radius_peak_m`
  - `xy_displacement_peak_m`
- `manifest.yaml` 已新增：
  - `xy_motion_summary`
- `notes.md` 已新增：
  - `## XY 运动摘要`
- `windy` 下若位置漂移过大，当前会自动追加 anomaly：
  - `start_xy_radius_excessive`
  - `xy_radius_excessive`
  - `xy_displacement_excessive`

### 本次新增 windy artifacts

- `attitude sweep pitch 0.10` repeat：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_055849_attitude_sweep_pitch/`
- `attitude sweep pitch 0.05`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_060004_attitude_sweep_pitch/`
- `attitude pulse roll 0.10` fresh with xy anomaly instrumentation：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_060642_attitude_pulse_roll/`

### 关键结果

- `repeat sweep pitch 0.10`：
  - 再次 `status=invalid_runtime`
  - `failsafe_event=1`
- `sweep pitch 0.05`：
  - 仍为 `status=invalid_runtime`
  - `failsafe_event=1`
  - `anomaly_summary=['clock_missing', 'land_timeout_force_disarm']`
- `fresh pulse roll 0.10`：
  - `status=completed`
  - `start_xy_radius_m=0.137`
  - `end_xy_radius_m=62.7`
  - `xy_radius_peak_m=62.7`
  - `xy_displacement_peak_m=62.65`
  - `anomaly_summary` 已新增 `xy_radius_excessive` 与 `xy_displacement_excessive`

### 方法学结论

- `windy sweep pitch` 的失效已经不是单次偶发；当前在 `0.10` 与 `0.05` 两档都可复现
- `windy` 下 attitude run 会出现显著水平漂移；即使输入幅值不大，也可能在单次 run 内漂到可视地面范围之外
- 同一仿真会话里连续做多组 `windy` attitude run，会把上一组的落点漂移带到下一组，导致后续 run 不是从原点附近重新开始
- 因此当前部分 `windy` invalid 不能简单解释为纯控制律边界，还必须考虑：
  - 风场导致的位置漂移
  - 可视地图边界污染
  - run-to-run 的起点累积漂移

### 最新分析产物

- `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_060937_phase3_windy/`

### 当前要求

- 后续若继续做 `windy` 边界图谱，更稳妥的流程应是：
  - 每组 anchor fresh 重启 PX4/GZ
  - 或至少在起飞前加入位置半径 gate
  - 并把 `xy_*_excessive` 视为环境污染信号，而不是只当普通 anomaly

## 2026-03-11 补充记录（windy prestart gate）

### 新增代码口径

- `telemetry_recorder.py` 已新增 `latest_row()`，用于在 recorder ready 后读取最新 `vehicle_local_position`
- `experiment_runner.py` 已新增 `windy` 起飞前 XY 半径 gate：
  - 默认只在 `sim_world=windy` 时启用
  - 默认阈值 `prestart_max_xy_radius_m=5.0`
  - 默认等待 `prestart_xy_gate_timeout_s=2.0`
- gate 若失败，当前会：
  - 追加 `prestart_xy_radius_excessive` 或 `prestart_xy_unavailable`
  - 写入 `manifest.yaml: prestart_xy_gate`
  - 在 `notes.md` 新增 `## 起飞前位置 Gate`
  - 停止在起飞前，不再执行 `injector.start_run()`
- `analysis_runner.py` 已把 `prestart_xy_radius_excessive` 纳入 windy 污染提示，不再只看 `xy_*_excessive`

### 方法学更新

- `windy` 实验流程现在不再允许“从明显漂移后的落点继续起飞”而不留痕迹
- fresh 重启仍是首选；prestart gate 只是防止 run-to-run 累积漂移污染的下限保护
- 因此后续如果看到：
  - `completion_reason=prestart_xy_gate_blocked`
  - `anomaly_summary` 含 `prestart_xy_radius_excessive`
- 应直接重启 PX4/GZ，而不是把该 run 当成新的动态边界点

## 2026-03-11 补充记录（windy prestart gate 实跑验证）

### 本次新增 windy artifacts

- fresh run：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_063154_attitude_pulse_roll/`
- same-session rerun：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_063246_attitude_pulse_roll/`
- fresh rerun：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_063336_attitude_pulse_roll/`

### 验证结果

- `20260311_063154_attitude_pulse_roll`：
  - `prestart_xy_radius_m=0.186`
  - `prestart gate passed=yes`
  - `status=completed`
  - 但单次 run 内仍漂到 `end_xy_radius_m=65.727`
- `20260311_063246_attitude_pulse_roll`：
  - 与上一组处于同一 `windy` 会话
  - `prestart_xy_radius_m=83.154`
  - `completion_reason=prestart_xy_gate_blocked`
  - `anomaly_summary=['clock_missing', 'prestart_xy_radius_excessive']`
  - 本次 run 未起飞，`XY 运动摘要=unavailable`
- `20260311_063336_attitude_pulse_roll`：
  - fresh 重启后 `prestart_xy_radius_m=0.172`
  - `prestart gate passed=yes`
  - 说明 gate 没有误伤 fresh 会话
  - 但后续仍 `status=invalid_runtime` 且 `failsafe_event=1`，这属于动态/扰动问题，不属于 gate 误判

### 最新分析产物

- `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_063445_phase3_windy/`

### 结论

- 现在已经有直接证据证明：
  - 同一 `windy` 会话内的第二组 run 会因为起点半径过大被 gate 拦下
  - fresh 会话里的同配置 run 不会被 gate 误伤
- 因而后续 `windy` invalid 必须先区分：
  - `prestart_xy_gate_blocked` 这类流程污染阻断
  - 真正进入实验窗口后的动态失效

## 2026-03-11 补充记录（windy manual pitch/composite anchor）

### 本次新增 windy artifacts

- `manual pulse pitch 0.40`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_064512_manual_pulse_pitch/`
- `manual sweep pitch 0.40`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_064626_manual_sweep_pitch/`
- `manual step composite moderate`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_064746_manual_step_composite/`

### 关键结果

- `manual pulse pitch 0.40`：
  - `status=completed`
  - `response_delay_ms=6.001`
  - `end_xy_radius_m=1.113`
  - `anomaly_summary=['clock_missing']`
- `manual sweep pitch 0.40`：
  - `status=completed`
  - `response_delay_ms=6.054`
  - `end_xy_radius_m=2.069`
  - `anomaly_summary=['clock_missing']`
- `manual step composite moderate`：
  - `status=completed`
  - `input_peak=0.25`
  - `response_delay_ms=4.557`
  - `end_xy_radius_m=1.71`
  - `anomaly_summary=['clock_missing']`

### 方法学结论

- 在 fresh `windy` 会话下，manual `pitch` 与 `composite moderate` 首轮 anchor 都能稳定完成
- 与 attitude `pulse/sweep` 相比，这些 manual run 的水平漂移显著更小，当前都在 `~1-2 m` 量级
- 因此当前 `windy` 下的分叉已经更清楚：
  - attitude chain 的主要风险在单次 run 内的大幅漂移与动态失效
  - manual `pitch/composite` 首轮点当前仍更接近 safe operational 区

### 最新分析产物

- `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_064839_phase3_windy/`

### 下一步

- 若继续按 TODO 收敛 `windy` 边界，更合理的是补更系统的 `attitude sweep` 点
- manual 方向若继续扩，应优先更激进的 `pitch/composite` 幅值，而不是重复当前 safe anchor

## 2026-03-11 补充记录（windy attitude sweep frontier 收敛）

### 新增配置

- `/home/car/autopilot_lab/src/fep_research/config/sweep_roll_015.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/sweep_pitch_002.yaml`

### 本次新增 windy artifacts

- `attitude sweep roll 0.15`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_065047_attitude_sweep_roll/`
- `attitude sweep pitch 0.02`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_065214_attitude_sweep_pitch/`

### 关键结果

- `attitude sweep roll 0.15`：
  - fresh 起步 `prestart_xy_radius_m=0.214`
  - `status=invalid_runtime`
  - `failsafe_event=1`
  - `end_xy_radius_m=135.362`
- `attitude sweep pitch 0.02`：
  - fresh 起步 `prestart_xy_radius_m=0.072`
  - `status=invalid_runtime`
  - `failsafe_event=1`
  - `end_xy_radius_m=128.711`

### 最新分析产物

- `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_065319_phase3_windy/`

### 收敛后的 frontier

- 当前 `windy` 下：
  - `attitude sweep roll` 的 safe/invalid 分界已从 `0.10 -> safe`、`0.15 -> invalid` 收到更窄区间
  - `attitude sweep pitch` 的 invalid frontier 已下压到 `0.02`
- 这说明当前问题已经不是“只有较大 sweep 幅值会坏”，而是 `windy + attitude sweep` 在非常保守幅值下也会出现大幅水平漂移和 failsafe

### 下一步

- 当前更合理的后续动作不再是继续盲目加更多 `sweep` 幅值
- 应转向：
  - 复核 `windy` 下 attitude `step/pulse` 的更细分边界
  - 或开始调查为什么 `attitude sweep` 会在保守幅值下也触发大幅 XY 漂移 / 轴间耦合失效

## 2026-03-11 补充记录（windy attitude step/pulse roll frontier 收敛）

### 新增配置

- `/home/car/autopilot_lab/src/fep_research/config/step_roll_015.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/pulse_roll_015.yaml`

### 本次新增 windy artifacts

- `attitude step roll 0.10` fresh rerun：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_070756_attitude_step_roll/`
- `attitude step roll 0.15`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_070934_attitude_step_roll/`
- `attitude step roll 0.20` fresh rerun：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_071030_attitude_step_roll/`
- `attitude pulse roll 0.10` fresh rerun：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_071122_attitude_pulse_roll/`
- `attitude pulse roll 0.15`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_071302_attitude_pulse_roll/`
- `attitude pulse roll 0.20` fresh rerun：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_071400_attitude_pulse_roll/`

### 关键结果

- `step roll 0.10`：
  - `status=completed`
  - `tracking_error_peak=0.218768`
  - `response_delay_ms=2.898`
  - `end_xy_radius_m=68.485`
- `step roll 0.15`：
  - `status=completed`
  - `tracking_error_peak=0.217005`
  - `response_delay_ms=7.158`
  - `end_xy_radius_m=72.003`
- `step roll 0.20`：
  - `status=completed`
  - `tracking_error_peak=0.203601`
  - `response_delay_ms=47.045`
  - `end_xy_radius_m=71.351`
- `pulse roll 0.10`：
  - `status=invalid_runtime`
  - `tracking_error_peak=0.102791`
  - `failsafe_event=1`
  - `end_xy_radius_m=66.513`
- `pulse roll 0.15`：
  - `status=completed`
  - `tracking_error_peak=0.249681`
  - `response_delay_ms=3.268`
  - `end_xy_radius_m=66.514`
- `pulse roll 0.20`：
  - `status=completed`
  - `tracking_error_peak=0.202546`
  - `response_delay_ms=1.519`
  - `end_xy_radius_m=62.888`

### 最新分析产物

- `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_071658_phase3_windy/`

### 方法学结论

- 在 fresh `windy` 会话下，attitude `step roll 0.10/0.15/0.20` 全部能完成，但全部伴随 `~68-72 m` 的单次 run 内大幅 XY 漂移，因此当前都应解释为 `degraded` 而不是 `safe`
- attitude `pulse roll` 在 fresh `windy` 下仍表现出不稳定：`0.10` 可复现 `invalid_runtime + failsafe_event=1`，而 `0.15/0.20` 虽能完成，但也都带显著漂移与抬升误差
- 当前 `windy + attitude step/pulse roll` 的核心问题已经不再只是“某个幅值是否失效”，而是整个 profile 家族在很小幅值下都缺乏可信 `safe` 区
- `analysis_runner.py` 已修正 scenario selection 排序：同一激励场景下现在优先选“最新 completed run”，不再让旧的低异常 run 静默覆盖最新 rerun

### 下一步

- 若继续按 TODO 收敛 `windy` 边界，更合理的是补 attitude `step/pulse pitch` 首轮 anchor
- 若要解释机制，则应开始复核为什么 `windy + attitude` 在无 XY hold 下会把 `step/pulse/sweep` 全部推入大幅漂移区

## 2026-03-11 补充记录（windy attitude step/pulse pitch 首轮 anchor）

### 新增配置

- `/home/car/autopilot_lab/src/fep_research/config/pulse_pitch_010.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/pulse_pitch_020.yaml`

### 本次新增 windy artifacts

- `attitude step pitch 0.10`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_072424_attitude_step_pitch/`
- `attitude step pitch 0.20`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_072520_attitude_step_pitch/`
- `attitude pulse pitch 0.10`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_072613_attitude_pulse_pitch/`
- `attitude pulse pitch 0.20`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_072708_attitude_pulse_pitch/`

### 关键结果

- `step pitch 0.10`：
  - `status=completed`
  - `tracking_error_peak=0.193484`
  - `response_delay_ms=7.089`
  - `end_xy_radius_m=61.681`
- `step pitch 0.20`：
  - `status=completed`
  - `tracking_error_peak=0.198577`
  - `response_delay_ms=66.092`
  - `end_xy_radius_m=59.828`
- `pulse pitch 0.10`：
  - `status=completed`
  - `tracking_error_peak=0.255793`
  - `response_delay_ms=5.196`
  - `end_xy_radius_m=59.758`
- `pulse pitch 0.20`：
  - `status=invalid_runtime`
  - `tracking_error_peak=0.198937`
  - `failsafe_event=1`
  - `end_xy_radius_m=60.357`

### 最新分析产物

- `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_072821_phase3_windy/`

### 方法学结论

- fresh `windy` 下，attitude `step pitch 0.10/0.20` 都只能归到 `degraded`，而且都伴随 `~60 m` 的单次 run 内 XY 漂移与 `land_timeout_force_disarm`
- attitude `pulse pitch` 的边界更陡：`0.10 -> degraded`，`0.20 -> invalid_runtime + failsafe_event=1`
- 现在 `windy + attitude` 的分叉已经更清楚：
  - `step/pulse roll` 基本全落在 `degraded`
  - `step pitch` 也没有可信 `safe` 点
  - `pulse pitch 0.20` 已经进入 invalid frontier

### 下一步

- 若继续按 TODO 收敛 `windy` 边界，更合理的是补 `step/pulse pitch` 的更细分中间点
- 若更关注机制，则应开始解释为什么 `windy + attitude pitch` 也会稳定触发大幅 XY 漂移与长延迟

## 2026-03-11 补充记录（windy attitude step/pulse pitch 中间点）

### 新增配置

- `/home/car/autopilot_lab/src/fep_research/config/step_pitch_015.yaml`
- `/home/car/autopilot_lab/src/fep_research/config/pulse_pitch_015.yaml`

### 本次新增 windy artifacts

- `attitude step pitch 0.15`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_073316_attitude_step_pitch/`
- `attitude pulse pitch 0.15`：
  - `/home/car/autopilot_lab/artifacts/px4/runs/20260311_073412_attitude_pulse_pitch/`

### 关键结果

- `step pitch 0.15`：
  - `status=completed`
  - `tracking_error_peak=0.224164`
  - `response_delay_ms=1.058`
  - `end_xy_radius_m=58.744`
- `pulse pitch 0.15`：
  - `status=completed`
  - `tracking_error_peak=0.287873`
  - `response_delay_ms=11.555`
  - `end_xy_radius_m=63.422`

### 最新分析产物

- `/home/car/autopilot_lab/artifacts/px4/analysis/20260311_073506_phase3_windy/`

### 方法学结论

- fresh `windy` 下，attitude `step pitch` 现在已经形成 `0.10/0.15/0.20` 全部 `degraded` 的连续带，没有出现可信 `safe` 点，也还没有新的 invalid 点
- attitude `pulse pitch` 的边界现在更完整：`0.10/0.15 -> degraded`，`0.20 -> invalid`
- `pulse pitch 0.15` 的 `tracking_error_peak=0.287873` 已高于 `0.10` 与 `0.20`，说明当前解释不能只看幅值大小，还要把 profile 内动态响应异常一起写进去

### 下一步

- 若继续按 TODO 收敛 `windy` 边界，更合理的是转向 `step/pulse roll` 的更细分中间点之外的机制解释，或开始查 `pitch` 轴为何全段都只落在 `degraded`

## 2026-03-13 补充记录（`/clock` timing + ULog 解析 + full windy matrix）

### 本次新增实现

- `experiment_runner` 已支持在 `/clock` 缺失时自动拉起本地 `gz_clock_bridge`
- 新增 `ulog_metrics.py` / `ulog_backfill.py`，将 ULog 饱和指标回填到 `metrics.csv`
- 新增 `matrix_runner.py`，按 fresh/headless 口径批量执行 `windy` 全量矩阵

### 本次新增产物

- fresh `windy` matrix：
  - `/home/car/autopilot_lab/artifacts/px4/matrix/20260313_023647_windy/`
- 最新 nominal analysis：
  - `/home/car/autopilot_lab/artifacts/px4/analysis/20260313_031312_phase3_nominal/`
- 最新 windy analysis：
  - `/home/car/autopilot_lab/artifacts/px4/analysis/20260313_031312_phase3_windy/`

### 关键结果

- full `windy` fresh matrix 已覆盖 `config/*.yaml` 的 `40` 组配置
- 该矩阵的原始执行结果为：
  - `completed=35`
  - `failed=5`
  - 全部 `40` 组 run 的 `ulog_parse_status=parsed`
  - `39` 组 run 的 `notes.md` 标记 `Timing 分析可用性 = yes`
- 最新 `windy` summary 已按新口径刷新：
  - `selected runs=40`
  - `completed=38`
  - `non-timing=2`
  - `invalid_timing=1`
- 最新 `nominal` summary 也已刷新，继续明确保留其 historical non-timing 身份，不与 fresh `windy` timing-valid run 混写

### 当前结论

- `/clock` timing、ULog 解析与 full windy matrix 三项扩展工作已完成
- 当前剩余工作不再是“链路是否缺失”，而是：
  - 是否继续补更细分的 `windy` 幅值点
  - 是否开始解释 `windy + attitude` 下普遍出现的 XY 漂移与 frontier 机制
