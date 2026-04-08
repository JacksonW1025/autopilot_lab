# 2026-04-09 实验仓库现状说明

这份文档是写给“不想先啃完 `X schema / Y schema / pooled / stratified` 才能看懂仓库”的读者的。

如果你只想先看一句话，当前最准确的总结是：

- 这个仓库已经把 PX4 的第一阶段实验链路跑通了。
- 当前最稳的正式结论是：在 `gz_x500 + nominal + POSCTL/OFFBOARD_ATTITUDE` 这个范围里，用“当前控制命令 + 当前状态 + 少量历史”去预测“下一拍状态”，可以得到非常强的线性近似。
- 但这不等于“PX4 飞行控制本质上就是一个简单、完美、稳定、全局的线性系统”。
- 现在已经可以把 PX4 当成一个成形的研究对象，但还不建议马上把它当作和 ArduPilot 做强对照时的最终无争议基线。

## 1. 这个仓库里现在有什么

先用最直白的话说，仓库里现在主要有 5 类东西。

### 1.1 `src/`: 真正干活的代码

主要模块包括：

- [linearity_core](/home/car/autopilot_lab/src/linearity_core/linearity_core)
  - 负责数据准备、特征构造、拟合、研究契约、数据质量检查。
- [linearity_analysis](/home/car/autopilot_lab/src/linearity_analysis/linearity_analysis)
  - 负责把准备好的样本做批量分析，输出 `summary.md`、`study_summary.json`、`matrix_f.csv` 等结果。
- [linearity_study](/home/car/autopilot_lab/src/linearity_study/linearity_study)
  - 负责把多条 raw run 组织成 study。
- [px4_ros2_backend](/home/car/autopilot_lab/src/px4_ros2_backend/px4_ros2_backend)
  - PX4 的采集、运行、session、验收逻辑。
- [ardupilot_mavlink_backend](/home/car/autopilot_lab/src/ardupilot_mavlink_backend/ardupilot_mavlink_backend)
  - ArduPilot 预留 backend 区域，目前代码区域已经存在，但还没有进入正式对照阶段。

### 1.2 `configs/`: 实验配置

- [configs/studies](/home/car/autopilot_lab/configs/studies)
  - 定义“抓哪些数据、按什么方式跑分析”。
- [configs/ablations](/home/car/autopilot_lab/configs/ablations)
  - 定义“比较哪些输入组合、哪些输出定义、哪些模型、哪些 pooling 方式”。

你可以把它理解为：

- `src/` 是发动机。
- `configs/` 是实验说明书。

### 1.3 `scripts/`: 一键执行入口

当前最重要的脚本有：

- [run_px4_authoritative_baseline.sh](/home/car/autopilot_lab/scripts/run_px4_authoritative_baseline.sh)
  - 跑当前正式 PX4 baseline。
- [run_px4_diagnostic_matrix.sh](/home/car/autopilot_lab/scripts/run_px4_diagnostic_matrix.sh)
  - 跑 PX4-only 单轴和幅度分层诊断集。
- [run_px4_visual_demos.sh](/home/car/autopilot_lab/scripts/run_px4_visual_demos.sh)
  - 跑演示型配置，不属于正式研究口径。
- [visualize_fit_matrices.py](/home/car/autopilot_lab/scripts/visualize_fit_matrices.py)
  - 把最值得看的系数矩阵画成热力图，方便直观看稀疏性和强弱分布。

### 1.4 `artifacts/`: 实验产物

这是现在最重要的目录，因为实验有没有跑出来，最终都体现在这里。

- [artifacts/raw](/home/car/autopilot_lab/artifacts/raw)
  - 每一次单独飞行或单次采集的原始产物。
- [artifacts/studies](/home/car/autopilot_lab/artifacts/studies)
  - 把多条 raw run 聚合后形成的研究结果。
- [artifacts/px4_matrix](/home/car/autopilot_lab/artifacts/px4_matrix)
  - matrix 层调度记录，记录一轮批量 capture 运行了哪些任务。

### 1.5 `docs/`: 研究说明和阶段结论

当前比较关键的文档有：

- [STAGE_REPORT_2026-04-08.md](/home/car/autopilot_lab/docs/STAGE_REPORT_2026-04-08.md)
  - 当前正式阶段报告。
- [XY_SCHEMA_GUIDE.md](/home/car/autopilot_lab/docs/XY_SCHEMA_GUIDE.md)
  - X/Y schema 技术说明。
- [DATA_SCHEMA.md](/home/car/autopilot_lab/docs/DATA_SCHEMA.md)
  - 数据产物结构说明。
- [summary-0408.md](/home/car/autopilot_lab/docs/summary-0408.md)
  - 更早一轮总结，但它还是偏 schema 视角。

另外还有：

- `build/`
- `install/`
- `log/`

这些主要是 ROS2/colcon 的构建与日志产物，不是研究结论本身。

## 2. 现在实验进行到什么状态

### 2.1 当前正式 baseline 已经重建完成

当前正式的 PX4 authoritative baseline 是：

- backend: `px4`
- 机型: `gz_x500`
- world: `default`
- scenario: `nominal`
- mode: `POSCTL` 和 `OFFBOARD_ATTITUDE`

它对应的正式 study 是：

- [20260408_062436_px4_real_broad_ablation](/home/car/autopilot_lab/artifacts/studies/20260408_062436_px4_real_broad_ablation)

这份 study 的 accepted-only 状态已经满足正式口径：

- `run_count = 6`
- `accepted_run_count = 6`
- `rejected_run_count = 0`
- `POSCTL = 3 accepted`
- `OFFBOARD_ATTITUDE = 3 accepted`

也就是说，当前正式结论不是基于“随便抓到的几次 run”，而是基于一组通过研究验收门的 accepted-only 数据。

### 2.2 PX4-only 诊断集也已经跑过

诊断 study 是：

- [20260408_074744_px4_diagnostic_axis_matrix_balanced](/home/car/autopilot_lab/artifacts/studies/20260408_074744_px4_diagnostic_axis_matrix_balanced)

它的作用不是给正式主结论排名，而是回答：

- 哪个控制轴更容易破坏实验验收条件？
- 哪个动作幅度一上来就不稳定？

这轮诊断的结果很清楚：

- `roll / pitch / yaw` 在两个 mode 下、三档幅度下都能 accepted
- `throttle` 在两个 mode 下、三档幅度下全部被拒收
- 主要拒收原因是 `insufficient_active_nonzero_command_samples`

简化理解就是：

- 姿态相关通道目前是“研究上比较干净”的
- throttle 通道目前最容易先出问题

### 2.3 ArduPilot 代码区域已经在仓库里，但还没开始正式对照

仓库里已经有：

- [ardupilot_mavlink_backend](/home/car/autopilot_lab/src/ardupilot_mavlink_backend/ardupilot_mavlink_backend)

但当前正式研究状态仍然是：

- PX4 baseline 已经建立
- ArduPilot 还没有进入“同一实验矩阵、同一统计口径”的正式比较阶段

换句话说：

- 现在仓库不是“只做 PX4”
- 但正式研究进度目前还是“PX4 先打地基，ArduPilot 之后接进来”

## 3. 先解释这些最容易看不懂的词

这一节尽量不用术语压你。

### 3.1 什么是 raw run

一次 raw run，可以理解成“一次具体实验飞行/仿真采集”。

它会落在：

- [artifacts/raw](/home/car/autopilot_lab/artifacts/raw)

每条 run 里通常会有：

- `manifest.yaml`
- `telemetry/*.csv`
- `logs/`
- `metadata/`

你可以把 raw run 理解成“单次实验原件”。

### 3.2 什么是 study

study 不是单次 run，而是把多条 run 放在一起做统一分析。

它会落在：

- [artifacts/studies](/home/car/autopilot_lab/artifacts/studies)

你可以把它理解成“研究报告文件夹”。

一份 study 里通常会有：

- `prepared/sample_table.csv`
- `prepared/schema_inventory.yaml`
- `reports/summary.md`
- `summary/study_summary.json`
- `fits/...`

### 3.3 什么是 accepted-only

这轮仓库已经明确区分两件事：

- capture 是否跑完
- 这条 run 是否合格到可以进入正式研究

所以现在一条 run 就算技术上“采到了文件”，也不一定能算合格研究数据。

accepted-only 的意思是：

- 只让通过研究验收门的 run 进入正式分析

当前会重点检查的东西包括：

- 实验是否真的开始了
- 是否真的进入动作段
- 动作段里是否有足够多非零控制命令
- 是否在动作期间 failsafe
- 是否缺关键 topic

### 3.4 什么是 authoritative、diagnostic、demo

这三个词不是一个意思。

- `authoritative_research`
  - 正式研究口径，用来写主结论。
- `diagnostic_research`
  - 诊断口径，用来找问题边界，不直接当作主结论。
- `demo_only`
  - 主要用于观察和展示，不进入正式结论。

简单说：

- authoritative 是“正式证据”
- diagnostic 是“问题定位工具”
- demo 是“演示”

### 3.5 什么是 X schema

把它理解成：

- “我给模型看哪些输入信息”

这里的 `X` 不是神秘数学黑话，它就是输入。

比如：

- `commands_only`
  - 只给模型看 4 个控制命令：`roll / pitch / yaw / throttle`
- `commands_plus_state`
  - 除了控制命令，再给当前状态
- `commands_plus_state_history`
  - 在 `command + 当前状态` 的基础上，再把最近几拍历史也给进去
- `full_augmented`
  - 再加入 mode、config_profile、控制器内部量、执行器反馈等更多上下文

所以你可以把 X schema 直接理解成：

- “输入打包方案”

### 3.6 什么是 Y schema

同理，`Y` 就是模型要去预测的目标。

常见的几种：

- `next_raw_state`
  - 预测下一拍状态本身
- `delta_state`
  - 预测“下一拍减当前拍”的变化量
- `future_state_horizon`
  - 预测更远一点未来的状态
- `actuator_response`
  - 预测执行器层面的响应

所以你可以把 Y schema 理解成：

- “输出定义方式”

### 3.7 什么是 `next_raw_state`

这是当前最关键的一个词。

它的意思不是“无限久以后的未来”，而是：

- 用当前这一拍的信息，预测下一拍的原始状态

这里的“状态”通常包括：

- 姿态角 `roll / pitch / yaw`
- 角速度
- 位置
- 速度
- 高度
- 垂向速度
- heading

### 3.8 什么是 `commands_plus_state_history`

这只是一个很长的名字，但意思其实很简单：

- 控制命令
- 当前状态
- 再加上最近几拍的历史状态和历史命令

可以把它理解成：

- “给模型更多上下文，让它更像知道系统刚刚发生了什么”

### 3.9 什么是 `full_augmented`

这是更大的输入包。

在 `commands + state + history` 之外，还会加一些额外上下文，例如：

- 当前 mode
- config_profile
- 控制器内部量
- actuator 反馈

所以 `full_augmented` 的核心意思就是：

- “尽量把系统上下文多给一点”

### 3.10 什么是 pooled 和 stratified

这两个词非常容易把人劝退，其实意思不复杂。

- `pooled`
  - 把不同 mode 的数据合在一起，训练一个统一模型
- `stratified`
  - 先按条件分开，再分别拟合

在当前 study 里，主要就是：

- pooled: 把 `POSCTL` 和 `OFFBOARD_ATTITUDE` 合在一起看
- stratified: 分 mode 看

你可以把它理解成：

- pooled 在问：“一个统一公式能不能同时解释两种 mode？”
- stratified 在问：“分开看时，各自是不是更整齐？”

### 3.11 什么是 `ols_affine`

它表示：

- 用最普通的线性回归去拟合
- 但允许有一个偏置项 `b`

所以模型形式更像：

```text
Y ≈ X · F + b
```

其中：

- `X` 是输入
- `Y` 是输出
- `F` 是系数矩阵
- `b` 是偏置

“affine” 可以理解成：

- “线性部分 + 常数偏移”

### 3.12 什么是 `matrix_f.csv`

这是每次拟合后最直观的核心产物之一。

它就是上面公式里的 `F`。

如果矩阵大小是 `93 x 15`，意思就是：

- 一共有 93 个输入特征
- 一共有 15 个输出分量

矩阵里的每一个格子，都可以粗略理解成：

- 某个输入特征，对某个输出分量的线性影响权重

### 3.13 什么是 `R²`

它是“拟合效果有多好”的一个常见指标。

简单理解：

- 越接近 `1` 越好
- 如果接近 `0`，说明模型几乎没解释力
- 如果是很大的负数，说明模型几乎完全跑偏

当前你看到 `0.9994`、`0.9996` 这种值，说明：

- 预测近似非常强

但注意：

- `R²` 很高，不自动等于“模型物理上干净”
- 也不自动等于“这个公式全局稳定”

### 3.14 什么是 condition number

这是这类报告里最容易被忽略、但实际上很关键的指标。

它粗略表示：

- 这个线性问题在数值上是否病态
- 系数是不是对微小扰动特别敏感

你可以把它理解成：

- `R²` 回答“能不能拟合得很好”
- `condition number` 回答“这个好结果是不是脆得厉害”

所以当前报告里一个很重要的现实是：

- `R²` 很高
- 但 condition number 仍然很大

这就是为什么我们不能把现在的结果说成“完美、稳固、物理可解释的线性真相”。

### 3.15 什么是 support = supported / partial

这是仓库对结果可靠性的内部标签。

可以简单理解为：

- `supported`
  - 结果比较稳，至少没那么明显踩到病态红线
- `partial`
  - 结果有价值，但还带明显保留意见

当前最强的 pooled 结果，虽然 `R²` 最高，但仍然只是 `partial`。

这恰恰说明：

- 仓库现在没有只迷信高分数

## 4. 当前最重要的实验结果是什么

### 4.1 当前最强的线性关系是什么

如果只看“谁的分数最高”，当前最强的是：

- `full_augmented -> next_raw_state | pooled | ols_affine`

可以把它翻译成一句人话：

- 给模型看很多上下文，包括命令、当前状态、部分历史、mode、配置和一些内部量
- 然后让它预测下一拍状态
- 这件事在线性近似上效果最好

它当前的关键数字是：

- `median_test_r2 = 0.9996`
- `effective_condition_number = 1039336.3683`
- `support = partial`

这意味着：

- 它“非常能拟合”
- 但它“数值上还是偏病态”

### 4.2 如果不想要太重的输入包，最值得看的关系是什么

如果你希望结果既强，又尽量接近一个“更朴素的基线”，当前更值得看的组合是：

- `commands_plus_state_history -> next_raw_state | pooled | ols_affine`

翻译成人话就是：

- 用控制命令 + 当前状态 + 少量历史
- 去预测下一拍状态

它的关键数字是：

- `median_test_r2 = 0.9994`
- `effective_condition_number = 996260.5635`
- `support = supported`

这也是为什么现在更适合对外讲的主结论是：

- “当前控制命令 + 当前状态 + 少量历史”到“下一拍状态”之间存在很强的线性近似

而不是：

- “某个特别大的、包含很多内部量的大模型一定就是唯一正确答案”

### 4.3 当前最重要的 Y 结论是什么

当前最稳定的结论不是某个 X，而是某个 Y。

现在最清楚的结论是：

- `next_raw_state` 是当前最好预测、也最适合作为主输出定义的 Y schema

这说明当前问题更像是在做：

- “一步预测”

而不是：

- “直接解释长期未来”
- “直接解释执行器细节”

### 4.4 pooled 和 stratified 目前怎么理解

当前 study 说明：

- `pooled` 给出了最高的绝对 `R²`
- `stratified` 并没有推翻主结论
- 它只是提醒我们：把 mode 混在一起和分开看，最优组合不完全一样

所以现在最合理的说法是：

- “一个统一模型大体能成立”
- 但“mode 差异仍然真实存在”

### 4.5 throttle 的信号是什么

当前 diagnostic matrix 给出的最清楚结论是：

- `roll / pitch / yaw` 三个姿态相关通道都比较干净
- `throttle` 最先系统性出问题

注意，这里“出问题”不是说飞机一定飞坏了，而是说：

- 在当前研究验收规则下，throttle 更容易拿不到足够合格的动作样本

研究意义上，它说明：

- 当前全局线性假设最先失稳的地方，很可能就在 throttle 相关通道

## 5. 那两个最值得看的矩阵到底是什么

这部分专门回答“矩阵大概长什么样”。

### 5.1 第一张：`full_augmented -> next_raw_state`

当前最强总体矩阵对应：

- `X = full_augmented`
- `Y = next_raw_state`

它的矩阵大小大约是：

- `93 x 15`

意思是：

- 93 行输入特征
- 15 列未来状态输出

输出列主要就是：

- 未来的姿态角
- 未来的角速度
- 未来的位置
- 未来的速度
- 未来的高度
- 未来的垂向速度
- 未来的 heading

热力图已经生成在：

- [full abs heatmap](/home/car/autopilot_lab/artifacts/studies/20260408_062436_px4_real_broad_ablation/fits/full_augmented__next_raw_state__pooled/ols_affine/matrix_heatmap_abs.png)
- [full signed heatmap](/home/car/autopilot_lab/artifacts/studies/20260408_062436_px4_real_broad_ablation/fits/full_augmented__next_raw_state__pooled/ols_affine/matrix_heatmap_signed.png)

怎么看：

- 颜色越深，表示这个输入和这个输出之间的线性权重越强
- 大片很浅，表示很多连接很弱
- 有成块的深色区域，表示某一组输入会集中影响某一组输出

### 5.2 第二张：`commands_plus_state_history -> next_raw_state`

当前更稳、更适合拿来讲“基线”的矩阵对应：

- `X = commands_plus_state_history`
- `Y = next_raw_state`

它的矩阵大小大约是：

- `76 x 15`

和第一张相比，它少掉了一些 mode/internal/actuator 扩展特征，更接近：

- 命令
- 当前状态
- 最近几拍历史

热力图在：

- [history abs heatmap](/home/car/autopilot_lab/artifacts/studies/20260408_062436_px4_real_broad_ablation/fits/commands_plus_state_history__next_raw_state__pooled/ols_affine/matrix_heatmap_abs.png)
- [history signed heatmap](/home/car/autopilot_lab/artifacts/studies/20260408_062436_px4_real_broad_ablation/fits/commands_plus_state_history__next_raw_state__pooled/ols_affine/matrix_heatmap_signed.png)

如果你只想看“一个比较像线性动力学近似”的图，我更建议先看这一组。

## 6. 当前的初步结论

把所有结果压缩成最少的话，当前可以得出这些初步结论。

### 6.1 已经可以说“第一阶段主结论成立”

在当前 scope 下，已经可以稳定地说：

- PX4 的 `next_raw_state` 可以被固定全局仿射模型很好地近似预测

### 6.2 但这仍然不是“飞控真相被线性系统完全揭示”

因为当前同时还看到：

- 最优组合的 condition number 仍然很高
- 最强结果不全是 `supported`
- pooled 和 stratified 之间仍存在结构差异
- throttle 通道在诊断里最先暴露问题

所以现在更准确的表达是：

- “有很强的线性近似”

而不是：

- “系统本质上就是一个干净稳定的全局线性模型”

### 6.3 当前更像是一个“强一步预测模型”

现有结果最支持的故事是：

- 当前命令 + 当前状态 + 少量历史
- 可以非常好地预测下一拍状态

它更像一个“一步动力学近似”，而不是一个一口气解释所有控制层细节的万能模型。

## 7. 下一步 TODO

当前最合理的下一步，不是再写一堆抽象层，而是继续把研究边界压实。

### 7.1 先把 PX4 baseline 再做厚一点

- 给 `POSCTL` 和 `OFFBOARD_ATTITUDE` 从 `3 repeats` 继续补到 `5 repeats`
- 继续观察：
  - `median_test_r2`
  - `effective_condition_number`
  - `support`
  - `sparsity_mask`
  - 最优组合是否稳定

### 7.2 单独处理 throttle

- 针对 throttle 单独设计更合适的动作注入方式
- 重点排查为什么会反复出现：
  - `insufficient_active_nonzero_command_samples`
- 不要把 throttle 和姿态轴继续混在同一层诊断叙事里

### 7.3 把 PX4-only 诊断结论写成更短、更直接的一页

现在 diagnostic 结果已经很清楚，但还偏散落在 artifact 里。

建议补一页单独说明：

- 哪些轴 accepted
- 哪些轴 rejected
- 哪些幅度开始出现问题
- 这说明了什么

### 7.4 在引入 ArduPilot 之前，冻结跨 backend 契约

重点不是再铺很多新代码，而是确保这些东西以后都按同一口径产出：

- `manifest`
- `data_quality`
- `research_acceptance`
- `prepared sample table`
- `X/Y schema naming`

### 7.5 然后再把同一实验矩阵迁移到 ArduPilot

顺序最好是：

1. PX4 baseline 再厚一点
2. throttle 诊断再清楚一点
3. 契约冻结
4. 同一实验矩阵迁到 ArduPilot

这样到时候如果结论变了，才比较容易判断：

- 是 backend 差异造成的
- 还是 PX4 baseline 本来就还不够稳

## 8. 如果你现在只想知道“下一步先看什么”

我建议按这个顺序看：

1. [STAGE_REPORT_2026-04-08.md](/home/car/autopilot_lab/docs/STAGE_REPORT_2026-04-08.md)
2. [authoritative study summary](/home/car/autopilot_lab/artifacts/studies/20260408_062436_px4_real_broad_ablation/reports/summary.md)
3. [authoritative schema inventory](/home/car/autopilot_lab/artifacts/studies/20260408_062436_px4_real_broad_ablation/prepared/schema_inventory.yaml)
4. 两组矩阵热力图
5. [diagnostic schema inventory](/home/car/autopilot_lab/artifacts/studies/20260408_074744_px4_diagnostic_axis_matrix_balanced/prepared/schema_inventory.yaml)

如果你只想用一套最简单的话复述给别人，可以直接说：

- 这个仓库已经把 PX4 的 accepted-only 正式 baseline 做出来了。
- 现在最强的线性关系，是“命令和当前状态去预测下一拍状态”。
- 结果分数非常高，但数值条件还不够漂亮，所以不能把它吹成完美线性真相。
- throttle 是当前最先暴露问题的控制轴。
- 下一步应该是在保持同一契约的前提下，把 PX4 baseline 再做厚一点，然后再迁移到 ArduPilot。
