# 统一 Schema 口径下全局线性 `f` 的里程碑报告

## 这项研究到底在问什么

这项研究要回答的问题很直接：

如果我们把飞行器在某一时刻看到的输入记成 `X`，把稍后想预测的结果记成 `Y`，那么是否存在一个固定不变的映射 `f`，让大量数据都近似满足：

`Y ≈ fX (+ b)`

这里可以把它理解成：

- `X` 是“现在手里有什么信息”，例如命令、姿态、角速度、位置、速度，或者这些量的短历史。
- `Y` 是“接下来会发生什么”，例如下一时刻状态、状态子集、未来短窗响应，或执行器响应。
- `f` 是一张固定矩阵。如果同一张矩阵在很多不同飞行片段上都能工作，而且不是靠偶然凑出来的，我们就说这里有可接受的线性证据。

这份报告刻意不把重点放在“PX4 和 ArduPilot 谁更好”上。真正的重点是：在统一的数据口径和统一的分析口径下，线性关系本身是否站得住。

## 为什么要同时跑 PX4 和 ArduPilot

如果只在一个飞控上得到结论，最大的风险是：我们看到的不是“飞行控制问题本身的结构”，而只是某一个软件实现的习惯。

所以这次实验做了两件约束很强的事：

- 两个 backend 使用同一套 `X` 定义、`Y` 定义、模型族和报告结构。
- 两个 backend 的 raw 数据都经过同一口径的质量门槛，只有通过门槛的 run 才能进入正式分析。

这样一来，如果两个 backend 表现相似，这不是坏事，反而是好事。它说明“线性关系”更像问题本身的性质，而不是某一个 backend 的偶然产物。

## 当前正式实验状态

这轮正式实验已经全部完成，不再是进行中状态：

- PX4 generalization full baseline：done。
- PX4 generalization full diagnostic：done。
- ArduPilot generalization full baseline：done。
- ArduPilot generalization full diagnostic：done。

这意味着现在已经可以直接回答两类问题：

1. 线性关系 `Y ≈ fX (+ b)` 本身是否成立。
2. 这个关系在 `nominal / dynamic / throttle_biased` 三档状态下是否还能站得住。

Formal V2 现在有两条同级正式线：

- generalization full 四-study 线，负责回答“线性关系总体是否存在，以及能否跨 scenario 成立”。
- ArduPilot mode-isolated targeted line，负责回答“state-evolution 在不混 mode 时能否形成成熟正结论，否则能否成熟地下负结论”；当前 overall_status=`mode_isolated_state_evolution_still_inconclusive`。

## 这次正式做了哪些实验

正式实验分成四份 study：

- PX4 baseline：`30/30 accepted`，覆盖 `POSCTL` 与 `OFFBOARD_ATTITUDE`，并同时覆盖三档 scenario。
- PX4 diagnostic：姿态轴全部 accepted，throttle boundary=`mixed`。
- ArduPilot baseline：`30/30 accepted`，覆盖 `STABILIZE` 与 `GUIDED_NOGPS`，并同时覆盖三档 scenario。
- ArduPilot diagnostic：姿态轴全部 accepted，throttle boundary=`none`。

## 现在已经能说清楚的结论

### 1. 可以正式把“线性关系存在”作为正面结论

- PX4 baseline 的代表性 supported 组合是 `full_augmented | next_raw_state | ols_affine | stratified`，当前 best combo 是 `full_augmented | next_raw_state | ols_affine | stratified`，`median_test_r2=0.9995`。
- ArduPilot baseline 的最稳 supported anchor 是 `commands_only | actuator_response | ridge_affine | pooled`，它说明 ArduPilot 这边也不是“没有线性”，而是最稳的证据更集中在命令到响应的映射上。
- 两边合计都已经出现了跨 scenario 的 generalized-supported 组合：PX4 共 `191` 个，ArduPilot 共 `24` 个。

这足以支持一个谨慎但明确的判断：在当前实验包线内，固定线性/仿射映射 `f` 不是空想，它确实在大量真实仿真数据上重复出现。

### 2. 这轮 generalization full 比旧 broad baseline 更有说服力

旧的 20260409 broad baseline 主要回答“线性证据是否存在”。

这轮 generalization full 则进一步回答“换一组状态、换一类动作，这个映射还在不在”。

- PX4 baseline `generalized_supported=80`，diagnostic `generalized_supported=111`。
- ArduPilot baseline `generalized_supported=12`，diagnostic `generalized_supported=12`。
- 当前 compare 的 generalization 判断是：`both_support_cross_scenario_linearity_but_px4_is_broader`。

这意味着现在的主结论已经不只是“某个 nominal 条件下能拟合”，而是“同一类线性结构在更宽一点的局部飞行包线里仍然反复出现”。

### 3. PX4 的 generalized-supported 证据更宽、更接近状态演化主线

- PX4 当前 baseline 图册里的 supported 组合数是 `120`。
- PX4 baseline 的代表性 generalized-supported 组合是 `full_augmented | next_raw_state | ols_affine | stratified`。
- PX4 diagnostic 的代表性 generalized-supported 组合是 `full_augmented | next_raw_state | ols_affine | stratified`。
- PX4 baseline 的跨场景解释结论是：当前 study 里已经出现跨 scenario 仍然保持 supported 的组合，f 更像常见映射而不是单一 operating-point 拟合。

这说明 PX4 不是只有一两组幸运组合高分，而是在状态演化相关的 `X/Y` 定义上已经形成较成片的跨场景正面证据。

### 4. ArduPilot 也已经出现 generalized-supported 证据，但范围更窄

- ArduPilot 当前 baseline 图册里的 supported 组合数是 `12`。
- ArduPilot baseline 的代表性 generalized-supported 组合是 `commands_only | actuator_response | ridge_affine | pooled`。
- ArduPilot diagnostic 的代表性 generalized-supported 组合是 `commands_only | actuator_response | ridge_affine | pooled`。
- ArduPilot baseline 的最优高分组合是 `commands_plus_state_history | selected_state_subset | ols_affine | pooled`，`median_test_r2=1.0000`，但它仍然不是最稳的 supported 主结论。
- state-evolution audit 的直接结论是：厚化 baseline 没有改变 ArduPilot 当前明确 supported 的主集合，state-evolution 路径的主阻塞仍然是 condition_number/mixed，而不是单纯 R2 不够。

这说明 ArduPilot 不是没有跨场景线性证据，而是目前更稳的证据主要集中在较简单的命令驱动路径上。高分的 state-evolution 组合仍然要同时面对条件数和稳定性问题。

### 4b. mode-isolated targeted line 正在回答更窄但更关键的问题

- STABILIZE targeted status=`inconclusive`，结论：该 mode 当前还没有成熟正结论，也还没满足成熟负结论的稳定性条件。
- GUIDED_NOGPS targeted status=`inconclusive`，结论：该 mode 当前还没有成熟正结论，也还没满足成熟负结论的稳定性条件。
- targeted aggregate artifact: `../artifacts/studies/20260413_134505_ardupilot_state_evolution_validation`
- STABILIZE targeted baseline: `../artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline`
- STABILIZE targeted diagnostic: `../artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic`
- GUIDED_NOGPS targeted baseline: `../artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline`
- GUIDED_NOGPS targeted diagnostic: `../artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic`

这条线不是 supplementary。它和 generalization full 一样，都是 Formal V2 的正式输入，只是回答的问题更聚焦于 ArduPilot state-evolution 本身。

### 5. 两个 backend 的相似性仍然在增强主结论，但不能说得过满

- 两边都已经完成 full baseline 与 full diagnostic。
- 两边 diagnostic 的姿态轴都能稳定 accepted。
- ArduPilot 当前 throttle boundary=`none`；PX4 当前 throttle boundary=`mixed`，说明扩展动作后的 throttle 边界并不完全对称。
- 两边都出现了跨 scenario generalized-supported 组合。

这说明实验不是依赖某一个 backend 的偶然成功，而是已经在统一 schema 和统一数据契约下，反复看到了同类线性结构。只是当我们开始扩大动作和状态包线时，backend 间的边界差异也开始显形了。

## 现在还不能说得过头的地方

- compare 的 gate/stability 主判断仍然是 `baseline_stability_unresolved`。
- ArduPilot baseline stability 当前状态仍是 `unknown`，不是完全锁死不变的状态。

所以当前还不适合把“backend 差异已经被完全解释清楚”当成主标题。更稳妥的说法是：

1. 线性关系存在，这一点已经可以正式汇报。
2. 线性关系在多 scenario 下仍然成立，这一点也已经有正面证据。
3. PX4 的 generalized-supported 范围更宽，但 ArduPilot 的相对收窄，还不能被过度简化成最终 backend 输赢结论。

## 历史阶段结论怎么处理

20260409 那一轮 broad baseline / diagnostic 和准备性 artifact 不再进入 Formal V2 正式口径。

当前正式结论的主输入，已经切换为 generalization full 四个 study、targeted validation 和新的 compare artifact。

## 下一步建议

下一步不需要再扩很多新 schema。更值钱的是把已经出现的 `f` 矩阵读透：

1. 系统阅读 generalized-supported 组合的 `matrix_f` 热力图，区分哪些结构是真正的物理映射，哪些只是状态延续。
2. 若还要继续比较 backend 差异，优先做稳定性复查，不要先扩 schema 空间。
3. 若要把 backend 差异升格成更强结论，需要先继续压实 ArduPilot state-evolution 路径的稳定性。

## 这次里程碑的一句话总结

在统一 schema 和统一数据契约下，`Y ≈ fX (+ b)` 已经不只是一个局部拟合假设，而是一个在 PX4 和 ArduPilot 上都能拿到跨 scenario 正面证据的正式结论。当前 PX4 的 generalized-supported 证据更宽，ArduPilot 的证据更窄但仍然真实存在，因此现在适合把“线性存在且可一定程度泛化”作为正式里程碑，而不是把“backend 胜负”作为主标题。

## Artifact 路径

- PX4 baseline: `../artifacts/studies/20260410_224818_px4_real_generalization_ablation`
- ArduPilot baseline: `../artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation`
- PX4 diagnostic: `../artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`
- ArduPilot diagnostic: `../artifacts/studies/20260413_091420_ardupilot_generalization_diagnostic_matrix`
- final compare: `../artifacts/studies/20260413_134755_px4_vs_ardupilot_compare`
- state-evolution audit: `../artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/reports/state_evolution_audit.md`
- targeted validation: `../artifacts/studies/20260413_134505_ardupilot_state_evolution_validation`
- STABILIZE targeted baseline: `../artifacts/studies/20260413_115811_ardupilot_state_evolution_stabilize_baseline`
- STABILIZE targeted diagnostic: `../artifacts/studies/20260413_122521_ardupilot_state_evolution_stabilize_diagnostic`
- GUIDED_NOGPS targeted baseline: `../artifacts/studies/20260413_124654_ardupilot_state_evolution_guided_nogps_baseline`
- GUIDED_NOGPS targeted diagnostic: `../artifacts/studies/20260413_132622_ardupilot_state_evolution_guided_nogps_diagnostic`