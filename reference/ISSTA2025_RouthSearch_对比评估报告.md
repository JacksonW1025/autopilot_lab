# ISSTA 2025 RouthSearch 与当前工作对比评估报告

## 1. 结论先行

- 当前工作**没有根本走偏**，但必须重新收紧问题表述。更准确的说法不是“已经在识别飞控内部参数敏感度”，而是“已经在识别激进输入下，PX4 闭环中哪些信号、约束和控制层更早退化”。
- 你现在的实验平台已经能回答“**哪里先坏**”，但还不能严格回答“**哪一个飞控内部参数最敏感**”。
- 目前最关键的理论偏差有三个：
  - `manual` 链和 `attitude` 链不是同层输入，直接把两者当成同类“飞手输入”比较，会混入控制层级差异。
  - `attitude` 链带有 ROS 侧自写的简化高度保持，而 `manual` 链走的是 PX4 原生 `POSCTL` 位置控制，外环并不一致。
  - `manual` 链当前很多核心指标是拿输入回显 `manual_control_setpoint` 做对齐，而不是拿下游有效设定值或飞行器真实响应做对齐。
- “哪些参数对于激进输入更敏感”这一问题，当前仓库**只回答了一半**：
  - 已经开始识别敏感的**外部观测量**和**内部约束**，例如 `tracking_error`、`response_delay`、`clip_frac`、`max_unalloc_torque`、`torque_achieved`。
  - 但还没有严格识别敏感的**控制器参数**。
- PID 绝对没有过时，反而是当前工作里**必须显式纳入**的一组核心参数。至少要把它们作为受控常量冻结并报告；如果研究问题继续往“参数敏感度”推进，PID 与位置控制相关参数都应进入实验因素。

## 2. RouthSearch 原工作到底在研究什么

RouthSearch 的对象很明确：它研究的是**低层 PID 参数配置边界**，不是飞手激进输入边界。

从原仓库与中文解析看，RouthSearch 的核心对象是：

- 给定飞行模式，搜索 **P/I/D 三维参数空间中的 valid/invalid 边界**。
- 理论起点是 **Routh-Hurwitz 稳定性判据**。
- 工程上再用 **coordinate search** 修正理论边界与真实边界之间的偏移。
- 有效性由 mode-specific oracle 判定，而不是只看某一个单点误差。

对 PX4 而言，原工作实际搜索的就是速率环 PID。`hold_roll` 脚本直接改的是：

- `MC_ROLLRATE_P`
- `MC_ROLLRATE_I`
- `MC_ROLLRATE_D`

所以 RouthSearch 的核心命题是：

> 在既定飞行模式下，哪一组底层 PID 参数会让控制程序从“有效”跨到“无效”。

这和你当前工作的自然延伸关系是成立的，但它们不是同一个问题。

## 3. 当前仓库实际在研究什么

当前仓库更像是在研究：

> 在固定控制器配置下，不同激进输入和不同输入入口会如何推动 PX4 闭环更早进入退化区、约束区和失效区。

这和 README 里的表述基本一致，而且这个方向本身是合理的。但代码层面显示，你现在实际上在混合研究三件事：

1. **输入入口层级差异**
   - `manual` 链：`manual_control_input -> PX4 manual sticks -> POSCTL`
   - `attitude` 链：直接发 `vehicle_attitude_setpoint`
2. **闭环退化机理**
   - 例如 `actuator_motors` clipping、`control_allocator_status` 的 `unallocated_torque`
3. **第一阶段 sample-level surrogate identification**
   - 用 `y_{t+1} = a x_t + b y_t` 的一阶离散近似，对 `command_body / attitude_setpoint / rates_setpoint / torque_setpoint` 做 `x_t` schema compare

也就是说，当前工作已经超出“环境搭建”，但还没有进入严格的“内部参数敏感度辨识”。

## 4. 关键控制链复原

### 4.1 当前 `manual` 链并不是低层直接操纵

当前 `manual_input_injector.py` 在飞行模式下会：

- 先用 offboard 位置保持起飞
- 再切到 `NAVIGATION_STATE_POSCTL`
- 然后持续发布 `/fmu/in/manual_control_input`

而在 PX4 里，这条链并不是“摇杆直接打到姿态环”：

- `manual_control_setpoint` 先经过 expo/deadzone 处理
- `POSCTL` 下默认 `MPC_POS_MODE=4`
- 这会进入 `ManualAcceleration` 任务
- 摇杆先被映射为加速度/速度/位置设定，再进入位置控制器
- 之后才进入姿态控制、速率控制、控制分配和电机

因此，当前 `manual` 链本质上是：

`pilot stick -> input shaping -> manual acceleration task -> position/velocity PID -> attitude -> rate PID -> allocator -> motors`

### 4.2 当前 `attitude` 链也不是“纯 PX4 原生外环”

`attitude_injector.py` 直接发布 `/fmu/in/vehicle_attitude_setpoint`，这会进入 PX4 姿态控制器，再生成 `vehicle_rates_setpoint`，然后进入速率 PID。

但这里还有一个额外简化：

- 你在 ROS 侧写了一个轻量的 `_apply_altitude_hold()`
- 它用自定义 `altitude_hold_kp / altitude_hold_kd` 和 `hover_thrust` 去修正 `thrust_z`

因此，当前 `attitude` 链更准确地说是：

`ROS-side simplified altitude PD + PX4 attitude controller -> rate PID -> allocator -> motors`

这和 `manual` 链使用的 PX4 原生 `POSCTL` 外环不是同一个控制结构。

### 4.3 这意味着什么

这意味着当前“manual 比 attitude 更稳”的结论，当前只能解释为：

> 在你现在这套实验设置下，经由 PX4 内部 manual/position 控制律整形后的输入，比直接打入姿态设定点的输入，更晚触到底层饱和和分配约束。

这个结论本身成立，但它不是纯粹的“飞手输入更安全”结论，也不是“某个内部参数更敏感”结论。

## 5. 目前哪里过于简单

我认为当前仓库至少有六个地方还明显过于简化。

### 5.1 把不同控制层入口当成同类输入比较

这是当前最重要的问题。

- `manual` 链进入的是 `POSCTL` 下的 manual acceleration / position 外环
- `attitude` 链进入的是姿态设定点层

所以这不是“同一层输入的公平比较”，而是“不同控制深度入口的对比实验”。

这类实验可以做，但结论必须改口径。

### 5.2 `attitude` 链的高度保持过于工程化

当前 `attitude` 注入为了让实验可飞，引入了 ROS 侧的简化高度保持。这是合理的工程过渡，但理论上有两个问题：

- 它把一个自写 PD 外环叠在了 PX4 原生姿态控制之前；
- 它让 `attitude` 链和 `manual` 链在外环结构上更不一致。

如果后续继续拿这两条链直接推导“飞手控制敏感度”，理论支撑会偏弱。

### 5.3 `manual` 链的核心误差与延迟指标过于浅层

`metrics.py` 中，`manual` 链的 `tracking_error_peak` 和 `response_delay_ms` 主要是把命令与 `manual_control_setpoint` 回显对齐。

这意味着：

- 它测得更多是“输入是否被 PX4 接收到并回显”
- 不是“飞行器真实响应的延迟”
- 也不是“manual 经过内部控制律后，下游有效设定值的变化”

仓库通过 `experiment_runner.py` 又补了“是否真的观察到位移/姿态变化”的 anomaly gate，这让 `manual flight` 不至于完全失真；但用于跨 run 主汇总的很多指标，依然不是严格意义上的闭环响应指标。

### 5.4 当前的 `a/b` 模型还是 first-stage surrogate，不是参数因果辨识

`ab_fit_runner.py` 当前做的是：

- 一步离散时间拟合
- 状态只用 `[roll, pitch, p, q]`
- 输入只在 `command_body / attitude_setpoint / rates_setpoint / torque_setpoint` 四种 proxy 中比较

它已经足够支持一个结论：

> 在当前 nominal attitude dataset 中，`attitude_setpoint` 是更稳定的 `x_t` proxy。

但它还不能支持另一个更强的结论：

> `attitude_setpoint` 对激进输入“最敏感”。

因为这里比较的是 surrogate 输入定义的可拟合性，不是飞控内部参数本身的物理敏感度。

### 5.5 当前 recorder 对控制器内部状态记录不足

ROS 侧 recorder 目前只固定录了 5 个标准 topic：

- `vehicle_attitude`
- `vehicle_local_position`
- `vehicle_status`
- `manual_control_setpoint`
- `vehicle_control_mode`

这能支撑 run-level 证据链，但对“控制理论上的内部机理解释”还不够。像下面这些更关键的量，目前主要还依赖 ULog 离线抽取，而不是在线统一落盘：

- `vehicle_angular_velocity`
- `vehicle_rates_setpoint`
- `rate_ctrl_status`
- `vehicle_torque_setpoint`
- `vehicle_thrust_setpoint`
- `control_allocator_status`
- `actuator_motors`

### 5.6 当前 frontier / degraded 判定仍带明显 heuristic 色彩

`analysis_runner.py` 的 `safe / degraded / invalid` 是很有价值的工程标签，但目前还是 operational labeling：

- 一部分靠 anomaly
- 一部分靠误差/延迟阈值
- 一部分靠当前已完成前沿点

这足够支持阶段性分析，但还不足以直接上升为严格控制理论结论。

## 6. “哪些参数对激进输入更敏感”的理解是否符合预期

结论是：**部分符合，但概念上还没收严。**

### 6.1 当前已经做对的部分

当前仓库没有停留在“误差大了所以系统敏感”这种浅层表述，而是已经开始往内部机理推进：

- 关注 `clip_frac`
- 关注 `max_unalloc_torque`
- 关注 `torque_achieved`
- 在 windy 下进一步区分 active window 与 prefailsafe window

这一步是对的，因为它开始触到“激进输入如何把闭环推进到约束面”这一层。

### 6.2 当前还没做对的部分

但现在“参数”这个词用得偏宽了。当前真正识别出来的，更多是：

- **敏感观测量**：例如 tracking error、delay、xy drift
- **敏感约束**：例如 motor clipping、allocator unallocated torque
- **较稳定的输入 proxy**：例如 nominal attitude 数据里 `attitude_setpoint`

还不是：

- `MC_ROLLRATE_P` 比 `MC_ROLLRATE_D` 更敏感
- `MPC_XY_VEL_P_ACC` 比 `MPC_XY_MAN_EXPO` 更敏感
- 或者某个 PID/外环参数对边界移动的贡献排序

所以如果继续沿用“已经找到了敏感参数”的表述，会比当前证据走得更快。

### 6.3 当前证据真正支持的说法

当前证据更支持下面这句话：

> 在当前 PX4 配置和实验口径下，激进输入首先暴露的是某些观测量和约束的脆弱性；其中直接姿态入口比 manual/position 入口更早把系统推向底层饱和与分配限制，而 `attitude_setpoint` 只是当前 nominal attitude dataset 里最稳定的第一版 `x_t` proxy。

这句话是成立的。

## 7. PID 是否缺少必要考虑

结论是：**是的，当前工作对 PID 的考虑还不够，而且 PID 应该明确成为参数集合的一部分。**

原因有三层。

### 7.1 从 RouthSearch 的延续关系看，PID 不能消失

RouthSearch 的原问题就是低层 PID 边界。你现在把问题推进到激进输入，本来就是在问：

> 为什么在参数正确的前提下，系统仍可能在激进输入下越界。

这并不意味着 PID 可以忽略；恰恰相反，它意味着：

- 现在要研究的是“输入”与“PID/控制器参数”之间的相互作用
- 而不是用输入替代 PID

### 7.2 从 PX4 实际控制链看，PID 仍然直接决定是否进入约束区

PX4 的多旋翼速率控制仍然是明确的 PID + FF 结构，并带 anti-windup 与 integrator limit。

至少下面这组参数仍然是核心变量：

- `MC_ROLLRATE_P/I/D/K/FF`
- `MC_PITCHRATE_P/I/D/K/FF`
- `MC_YAWRATE_P/I/D/K/FF`
- `MC_RR_INT_LIM`
- `MC_PR_INT_LIM`
- `MC_YR_INT_LIM`

激进输入下，是否更早出现：

- 积分项堆积
- anti-windup 触发
- torque allocation 达不到
- 电机削顶

都和这些参数强相关。

### 7.3 只看 PID 也不够，还要把 manual/position 外环参数一起纳入

如果你的研究对象已经扩展到飞手输入，那么只盯住 rate PID 也不完整。因为 `manual` 链还显著受下面这些参数影响：

- `MPC_POS_MODE`
- `MPC_VEL_MANUAL`
- `MPC_VEL_MAN_SIDE`
- `MPC_VEL_MAN_BACK`
- `MPC_ACC_HOR`
- `MPC_ACC_HOR_MAX`
- `MPC_JERK_MAX`
- `MPC_HOLD_DZ`
- `MPC_XY_MAN_EXPO`
- `MPC_Z_MAN_EXPO`
- `MPC_YAW_EXPO`
- `MPC_XY_P`
- `MPC_Z_P`
- `MPC_XY_VEL_P/I/D_ACC`
- `MPC_Z_VEL_P/I/D_ACC`

所以更准确的说法应该是：

- 如果研究问题是“固定控制器下的 aggressive pilot input”，PID 和 `MPC_*` 至少要作为**冻结并报告的受控变量**。
- 如果研究问题是“哪些内部参数对 aggressive input 更敏感”，那 PID 和 `MPC_*` 就必须进入**解释变量和实验因素**。

## 8. 对当前方向的总体判断

### 8.1 没有走偏的部分

- 你确实在延续 RouthSearch，只是从“静态参数边界”推进到了“动态激进输入边界”。
- 你已经不再停留在 demo，而是做出了带 evidence chain 的实验平台。
- 你已经开始把 run-level 现象推进到 sample-level surrogate identification。
- 你已经在解释“为什么坏”，而不只是记录“坏没坏”。

### 8.2 有走偏风险的部分

走偏风险主要不在于实验本身，而在于研究命题表述：

- 如果继续把当前结果表述成“已找到敏感参数”，会走偏。
- 如果继续把 `manual` vs `attitude` 表述成“飞手输入 vs 飞手输入”的公平比较，也会走偏。

更稳妥的重新表述应该是：

> 当前工作研究的是，在不同控制入口与环境条件下，PX4 闭环如何被激进输入逐步推向包线边界，以及哪些约束和控制层更先失去裕度。

这一定义和现有代码、artifact、分析结果是对齐的。

## 9. 下一步开始前的补充建议

下面这些建议我认为不是“可选优化”，而是当前工作继续往前走之前最该补的部分。

### 9.1 先把研究问题拆成三个层次，不要混写

建议把后续工作明确拆成三类问题：

1. **输入入口敏感性**
   - 比较不同入口层级如何把系统更快推向约束
   - 例如 `manual`、`attitude`、`rates_setpoint`
2. **内部机理敏感性**
   - 比较哪些约束先成为瓶颈
   - 例如 clipping、unallocated torque、integrator buildup
3. **控制参数敏感性**
   - 比较哪些 PID / MPC 参数会显著移动边界

这三类问题都重要，但不能再混成一个“敏感参数”。

### 9.2 修正 `manual` 链指标定义

下一步不要再只用 `manual_control_setpoint` echo 作为 `manual` 主分析指标。至少要补成两层：

- 输入传播层：`command -> manual echo`
- 闭环效果层：`command -> downstream effective setpoint / actual state`

建议优先补的 `manual` 下游量：

- `vehicle_local_position_setpoint` 或等价位置/速度设定
- `vehicle_attitude_setpoint`
- `vehicle_rates_setpoint`
- `vehicle_torque_setpoint`

这样 `manual` 链和 `attitude` 链才能在“哪一层先坏”这个问题上真正可比。

### 9.3 处理 `attitude` 链的外环不一致问题

这里有两种合理路线，选一条就行，但要明确：

- 路线 A：保留当前 ROS 侧简化高度保持，但把它明确写成实验控制器的一部分，并报告其 `kp/kd/hover_thrust`
- 路线 B：尽量改成 PX4 原生外环一致的实验口径，减少 ROS 侧自写外环

如果目标是“飞手控制输入研究”，我更建议优先靠近路线 B。

### 9.4 把 PID 与 `MPC_*` 参数正式纳入实验设计

建议最小化地先做一版分层实验：

- 固定输入 profile
- 固定环境
- 只小范围改变 `MC_ROLLRATE_* / MC_PITCHRATE_*`
- 单独观察 frontier、clipping、allocator 和 uncertainty 的偏移

然后再补：

- `MPC_XY_VEL_P/I/D_ACC`
- `MPC_XY_MAN_EXPO`
- `MPC_ACC_HOR`
- `MPC_JERK_MAX`

这样你就能真正开始回答“哪些控制参数会改变 aggressive input boundary”。

### 9.5 扩充 recorder / dataset，而不是只继续扫更多幅值

我不建议下一步直接继续无脑扩 sweep/step 幅值矩阵。优先级更高的是先把证据链补齐：

- 录或抽取 `vehicle_angular_velocity`
- `vehicle_rates_setpoint`
- `rate_ctrl_status`
- `vehicle_torque_setpoint`
- `vehicle_thrust_setpoint`
- `control_allocator_status`
- `actuator_motors`

否则后面即使幅值扫得更多，理论解释仍会被“内部状态缺口”卡住。

### 9.6 重写当前最关键的一句结论

建议把当前阶段核心结论改写成下面这句，后续所有文档都按这个口径收：

> 当前仓库已经完成了从 RouthSearch 的静态 PID 边界问题向“动态激进输入下闭环包线边界问题”的过渡，但现阶段识别出的主要是敏感信号、敏感约束和不同控制入口的脆弱性；严格的控制参数敏感度排序仍需把 PID、`MPC_*` 参数和一致化控制层指标正式纳入实验设计。

## 10. 最终回答

对你最关心的四个问题，我的最终判断是：

- **方向是否走偏？**
  - 没有根本走偏，但当前表述比当前证据更超前，需要从“参数敏感度”收回到“控制层脆弱性与约束敏感性”。
- **是否有过于简单的地方？**
  - 有，而且主要集中在输入层级不一致、`attitude` 链外环自写、`manual` 链指标偏向输入回显、以及 recorder 对内部控制状态记录不足。
- **“哪些参数对激进输入更敏感”的理解是否符合预期？**
  - 部分符合。现在更接近“哪些信号和约束更敏感”，还不是“哪些控制器参数更敏感”。
- **PID 是否缺少必要考虑，是否也应属于参数的一部分？**
  - 是。PID 不仅要考虑，而且应成为当前工作正式参数集合的一部分；同时还应把 `MPC_*` 位置/手动整形参数一起纳入。

## 11. 主要证据来源

- 当前仓库：
  - `README.md`
  - `intro.md`
  - `reference/阶段工作总结与下一步研究计划.md`
  - `src/fep_research/fep_research/manual_input_injector.py`
  - `src/fep_research/fep_research/attitude_injector.py`
  - `src/fep_research/fep_research/metrics.py`
  - `src/fep_research/fep_research/telemetry_recorder.py`
  - `src/fep_research/fep_research/analysis_runner.py`
  - `src/fep_research/fep_research/identification_dataset_builder.py`
  - `src/fep_research/fep_research/ab_fit_runner.py`
  - `artifacts/px4/analysis/20260316_083659_phase3_nominal/summary.md`
  - `artifacts/px4/identification/20260316_083830_nominal_attitude_repeats/fit_20260316_083740/fit_summary.md`
  - `artifacts/px4/identification/20260316_083830_nominal_attitude_repeats/uncertainty_attitude_setpoint_20260316_083748/uncertainty_summary.md`
- RouthSearch 仓库：
  - `README.zh-CN.md`
  - `RouthSearch_完整中文翻译与细致解析.md`
  - `evaluation_script/hold_roll_roth/px4_hold_roll_routh_identify_bounder.sh`
  - `routh_search/px4/PX4Util.py`
  - `routh_search/px4/px4_hold_mode.py`
  - `routh_search/px4/px4_hold_mode_oracle.py`
- 本地 PX4 控制链源码：
  - `src/modules/flight_mode_manager/tasks/Utility/Sticks.cpp`
  - `src/modules/flight_mode_manager/FlightModeManager.cpp`
  - `src/modules/flight_mode_manager/tasks/ManualAcceleration/FlightTaskManualAcceleration.cpp`
  - `src/modules/flight_mode_manager/tasks/Utility/StickAccelerationXY.cpp`
  - `src/modules/mc_att_control/mc_att_control_main.cpp`
  - `src/modules/mc_rate_control/MulticopterRateControl.cpp`
  - `src/lib/rate_control/rate_control.cpp`
  - `src/modules/mc_rate_control/mc_rate_control_params.c`
  - `src/modules/mc_pos_control/PositionControl/PositionControl.cpp`
  - `src/modules/mc_pos_control/multicopter_position_control_gain_params.c`
  - `src/modules/mc_pos_control/multicopter_position_mode_params.c`
  - `src/modules/mc_pos_control/multicopter_autonomous_params.c`
