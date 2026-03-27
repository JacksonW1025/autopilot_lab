# autopilot_lab 项目简介与当前实验状况

## 1. 文档目的

本文面向第一次接触当前仓库的老师或协作者，回答三件事：

1. `autopilot_lab` 现在到底是什么。
2. 它和旧 `px4_ws` 的关系是什么。
3. 目前哪些结论已经稳定，哪些还只是新 backend 的起步状态。

## 2. 一句话概括当前状态

`autopilot_lab` 是新的主研究仓库。它保留了原来 PX4 + ROS 2 的完整实验链路，同时新增了 ArduPilot + MAVLink backend，并把共享逻辑抽到了 `fep_core`。

也就是说，当前阶段的重点不是“把两套飞控完全做成同一套代码”，而是先把研究平台从单一 PX4 工作区提升为可容纳两个 backend 的统一实验仓库。

## 3. 为什么要从 `px4_ws` 迁到 `autopilot_lab`

旧 `px4_ws` 的问题不在于功能不够，而在于结构已经明显偏向 PX4 ROS 2：

- 研究逻辑、PX4 topic 接口、artifact 路径和 CLI 都混在同一个包里
- 历史分析代码默认假设底层一定是 PX4 ULog
- 文档、目录和运行方式也默认这是一个单 backend 的 ROS 2 工作区

如果继续在旧结构上硬接 ArduPilot，后果会很直接：

- 共享研究逻辑和 PX4 接口逻辑无法分离
- ArduPilot 明明不依赖 ROS 2 runtime，却会被迫伪装成 PX4 风格节点
- 后续做 cross-backend 对比时，artifact 与 manifest 的口径会越来越乱

因此现在采用的新结构是：

- `src/fep_core`
  - 后端无关层
- `src/px4_ros2_backend`
  - PX4 ROS 2 实现
- `src/ardupilot_mavlink_backend`
  - ArduPilot MAVLink 实现
- `src/fep_research`
  - PX4 兼容入口层

## 4. 旧仓和新仓的关系

- 新仓：
  - `/home/car/autopilot_lab -> /mnt/nvme/autopilot_lab`
- 旧仓：
  - `/home/car/px4_ws`

当前策略很明确：

- 旧仓保留，不回写，不反向同步
- 新仓作为后续主开发仓
- PX4 历史代码、`reference/` 和历史 PX4 artifacts 都已经迁入新仓

这意味着后续如果继续做 PX4，只在 `autopilot_lab` 上推进；`px4_ws` 只作为冻结基线存在。

## 5. 当前已经完成了什么

### 5.1 PX4 侧

PX4 侧原有能力已经保留：

- `ros2 run fep_research ...` 的入口保持兼容
- Phase 1-3 代码已经迁入并可在新仓编译
- 历史 `runs / analysis / matrix / identification` 已迁到 `artifacts/px4/`
- 新仓下已完成一次 PX4 smoke run 验证

因此，PX4 当前不是“准备迁移”，而是“已经迁完并能继续跑”。

### 5.2 ArduPilot 侧

ArduPilot 目前处于“最小闭环已建立”的状态：

- backend 位于 `src/ardupilot_mavlink_backend`
- 通过外部 `/home/car/ardupilot` 启动 SITL
- 通过 `pymavlink` 建立连接、接收心跳、记录遥测并落盘
- 已能写出 `manifest.yaml`、`metrics.csv`、`telemetry/*.csv`
- 已能记录 `ardupilot_tlog_path` 与 `ardupilot_bin_log_path`

但需要明确：

- 这还不是 PX4 Phase 3 等价实现
- 这还没有 ArduPilot 版的完整 failure attribution / identification
- 当前只能说 ArduPilot backend 已经具备后续扩展所需的基础闭环

## 6. 当前哪些结论是可信的

截至 `2026-03-27`，当前可以明确说：

- PX4 侧的研究流水线已经在新仓保持可用
- 旧 PX4 历史结果已经完成迁移，且目录口径稳定在 `artifacts/px4/...`
- `fep_research` 兼容层已经保住现有 PX4 ROS 2 节点入口
- ArduPilot backend 已经能完成最小 run 并生成标准化 artifacts

当前还不能夸大说：

- ArduPilot 已经和 PX4 在分析深度上完全对齐
- 两个 backend 已经可以直接做严格的一一对比结论
- 新 backend 已经完成针对 FEP 研究问题的完整统计与机理解释

## 7. 当前 artifact 口径

现在统一只使用下面两棵目录：

- `artifacts/px4/`
- `artifacts/ardupilot/`

其中：

- `artifacts/px4/`
  - 保存历史和后续 PX4 run、analysis、matrix、identification
- `artifacts/ardupilot/`
  - 保存 ArduPilot run、matrix 和后续回填结果

旧 `artifacts/runs` 这类兼容软链接已经移除，避免后续路径继续混乱。

## 8. 当前最值得记住的结论

如果只看当前阶段最核心的一点，可以概括为：

这个项目已经从“PX4 单 backend 的 ROS 2 工作区”升级成了“保留 PX4 兼容性、并为 ArduPilot 留出正式接入口的双 backend 研究仓库”。

换句话说，当前最大的进展不是多跑了几组仿真，而是把后续两套飞控并行研究的代码组织和数据组织先搭稳了。
