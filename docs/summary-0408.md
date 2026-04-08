# 2026-04-08 PX4 实验仓库分析报告

本报告基于以下权威产物整理：

- `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/reports/summary.md`
- `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/reports/schema_comparison.md`
- `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/summary/study_summary.json`
- `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/fits/...`
- `docs/STAGE_REPORT_2026-04-07.md`
- `docs/RESEARCH_GOAL.md`
- `README.md`
- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/XY_SCHEMA_GUIDE.md`
- `src/linearity_core/linearity_core/fit.py`
- `src/linearity_core/linearity_core/report.py`

当前默认研究 scope 为：

- backend: `px4`
- airframe: `gz_x500`
- world: `default`
- scenario: `nominal`
- modes: `POSCTL` 与 `OFFBOARD_ATTITUDE`

## 先给结论

- 当前最优 schema 是 `commands_plus_state_history x next_raw_state | ols_affine | pooled`。
- 它的 `median_test_r2 = 0.9726`，`median_test_mse = 0.000046`，`median_test_mae = 0.003960`。
- 但仓库给它的判定仍然是 `partial`，不是 `supported`。核心原因不是精度不够，而是条件数过高：`effective_condition_number ≈ 1,259,416`，超过仓库 `supported` 判定阈值 `1e6`。
- 如果追求“更稀疏、更稳定”的版本，同一组 `X/Y` 下的 `ridge_affine` 是最佳折中：`median_test_r2 = 0.9600`，`sparsity_ratio = 0.9825`。
- 因而当前最合理的回答是：在这个很窄的 PX4 scope 下，存在一个“预测力很强”的全局仿射近似；但它还不是一个物理意义干净、数值条件良好、可被称为“完美解释飞行行为”的全局线性定律。

## 1. 核心结论与最佳特征组合

### 1.1 当前系统找到的 best schema

来自 `summary.md` 与 `schema_comparison.md` 的直接结论：

| 项目 | 结果 |
| --- | --- |
| best linear schema | `commands_plus_state_history x next_raw_state | ols_affine | pooled` |
| best sparse/stable schema | `commands_plus_state_history x next_raw_state | ridge_affine | pooled` |
| best Y definition | `next_raw_state` |
| median test R2 | `0.9726` |
| median test MSE | `0.000046` |
| median test MAE | `0.003960` |
| support | `partial` |
| coefficient stability | `1.0000` |
| effective condition number | `1259416.2092` |

### 1.2 为什么这个组合表现最好

这个结果好，不是因为“历史状态特别神奇”，而是因为它同时满足了三个条件：

1. `X` 里终于有了足够的状态上下文。
   只有 command 的 `commands_only` 基本无法解释下一步响应；一旦把当前状态并入 `X`，性能是断崖式跃升。

2. `Y` 选成了最容易被线性近似的目标。
   在本次 broad ablation 里，`next_raw_state` 明显优于 `actuator_response`、`delta_state`、`future_state_horizon` 等其他目标定义。

3. `history` 只提供了小幅但稳定的增益。
   `commands_plus_state_history` 比 `commands_plus_state` 略强，说明最近几步的滞后项有帮助，但不是决定性因素。

### 1.3 为什么不是 `full_augmented`

`full_augmented x next_raw_state | lasso_affine | pooled` 也能做到 `R2 = 0.8755`，但仍显著落后于 `commands_plus_state_history x next_raw_state` 的 `0.9726`。这意味着：

- 加入更多 internal / actuator / one-hot 特征，并没有自动变得更可线性解释；
- 反而更容易把异质性、共线性和 alias 一起带进来；
- “更多特征”在这个实验里不是胜利条件，关键是“是否刚好覆盖了决定下一步状态所需的最小上下文”。

## 2. 变量消融分析

### 2.1 仓库汇总里给出的官方 step-up

`summary.md` 直接给出了两个 X 侧增益：

| 升级路径 | 汇总中的 R2 提升 |
| --- | --- |
| `commands_only -> commands_plus_state` | `+1.0442` |
| `commands_plus_state -> commands_plus_state_history` | `+0.0064` |

这里要注意：这两个数值来自仓库自动汇总逻辑，比较的是“每个 X schema 自己的最佳结果”，不一定是完全同一个 `Y/model` 口径。

### 2.2 固定到同一个目标 `Y = next_raw_state` 后再看

如果把比较口径固定到你最关心的“预测无人机下一步原始状态”，结论更明显：

| 模型 | `commands_only -> commands_plus_state` | `commands_plus_state -> history` |
| --- | ---: | ---: |
| `ols_affine` | `-120.0332 -> 0.9545`，提升 `+120.9877` | `0.9545 -> 0.9726`，提升 `+0.0181` |
| `ridge_affine` | `-119.7585 -> 0.9595`，提升 `+120.7180` | `0.9595 -> 0.9600`，提升 `+0.0005` |
| `lasso_affine` | `-119.8793 -> 0.9663`，提升 `+120.8456` | `0.9663 -> 0.9672`，提升 `+0.0009` |

### 2.3 这说明了什么

- “当前状态”是必须的。没有状态时，线性模型几乎完全崩溃。
- “历史状态”不是必须条件，但有边际价值。
- 更精确地说：对“下一步响应”这个任务，PX4 在当前 scope 下更接近一个“以当前状态为主、少量历史补充”的近 Markov 系统，而不是一个强依赖长历史的系统。

因此，对你的问题“历史状态必要吗”，我的直接回答是：

- 对达到“可用的高精度预测”，不是必要条件，因为 `commands_plus_state x next_raw_state` 已经有 `R2 ≈ 0.9545 ~ 0.9663`。
- 对把结果再往上推一小步，或者吸收一部分控制链的滞后与未显式建模的动态，历史状态是有帮助的。
- 所以更准确的表述是：“历史状态有益，但不是主导因素；主导因素是把当前状态纳入 `X`。”

## 3. 矩阵的数学性质：稀疏性与稳定性

### 3.1 先回答“f 是否稀疏”

这里要区分两层含义：

1. 如果按 `matrix_f.csv` 的“数值上是否恰好等于 0”来理解：
   `ols_affine` 的系数矩阵并不稀疏，数值上基本是稠密的。

2. 如果按仓库自己的“稳定非零连接”定义来理解：
   仓库会把 repeated fit / bootstrap 后稳定出现的连接写到 `sparsity_mask.csv` 里。按这个定义，最佳 OLS 结果是“中等偏强的稀疏”，最佳 ridge 结果则是“极强稀疏”。

因此，更严谨的回答是：

- `best predictive` 的 `f` 在数值层面偏稠密；
- 但在仓库定义的稳定支持集意义下，`f` 具有明显稀疏性；
- 若你强调“可解释稀疏结构”，`ridge_affine` 比 `ols_affine` 更像稀疏映射。

### 3.2 维度与总体统计

最佳 `X/Y` 组合下：

- `matrix_f.csv` 形状为 `76 x 15`
- 行数 `76` 表示 X 侧共有 76 个输入特征
- 列数 `15` 表示 Y 侧共有 15 个未来原始状态输出

这 76 个输入来自：

- 当前 command 4 个
- 当前 state 15 个
- `lag_1` 19 个
- `lag_2` 19 个
- `lag_3` 19 个

对应的 15 个输出为：

1. `future_state_roll`
2. `future_state_pitch`
3. `future_state_yaw`
4. `future_state_roll_rate`
5. `future_state_pitch_rate`
6. `future_state_yaw_rate`
7. `future_state_position_x`
8. `future_state_position_y`
9. `future_state_position_z`
10. `future_state_velocity_x`
11. `future_state_velocity_y`
12. `future_state_velocity_z`
13. `future_state_altitude`
14. `future_state_vertical_speed`
15. `future_state_heading`

### 3.3 稀疏统计

| 模型 | 矩阵形状 | 稳定非零数 | 总连接数 | sparsity ratio | median test R2 |
| --- | --- | ---: | ---: | ---: | ---: |
| `ols_affine` | `76 x 15` | `324` | `1140` | `0.7158` | `0.9726` |
| `ridge_affine` | `76 x 15` | `20` | `1140` | `0.9825` | `0.9600` |

这说明：

- OLS 为了追求最高预测精度，保留了较大的稳定支持集；
- ridge 用更强的正则化把映射压缩到了极少数连接上，只付出了约 `0.0126` 的 `R2` 损失。

### 3.4 结构特征

从 `sparsity_mask.csv` 可以看出两个鲜明现象：

- OLS 的稳定连接高度集中在 command 与 command-history 上，尤其是四个当前控制量和多个 lag command。
- ridge 的稳定连接几乎塌缩到了垂向运动相关变量：
  - `position_z`
  - `altitude`
  - `velocity_z`
  - `vertical_speed`
  - 及其 lag 项

这意味着：

- 如果只问“能不能预测”，OLS 会尽量利用更多输入通道；
- 如果只问“有没有特别稳定的骨架关系”，ridge 认为真正稳固的部分主要是垂向运动学相关通道。

### 3.5 完整矩阵形状可视化

说明：

- 下面不是 `matrix_f.csv` 的实数系数热图，而是 `sparsity_mask.csv` 的完整 ASCII 可视化。
- `█` 表示该输入到该输出的连接被判定为“稳定非零”。
- `·` 表示该连接未进入稳定支持集。
- 右侧数字是该行在 15 个输出上的稳定非零个数。

列编号：

```text
01=future_state_roll
02=future_state_pitch
03=future_state_yaw
04=future_state_roll_rate
05=future_state_pitch_rate
06=future_state_yaw_rate
07=future_state_position_x
08=future_state_position_y
09=future_state_position_z
10=future_state_velocity_x
11=future_state_velocity_y
12=future_state_velocity_z
13=future_state_altitude
14=future_state_vertical_speed
15=future_state_heading
```

`commands_plus_state_history x next_raw_state | ols_affine | pooled`

```text
command_roll             ███████████████ 15
command_pitch            ███████████████ 15
command_yaw              ███████████████ 15
command_throttle         ███████████████ 15
roll                     ···············  0
pitch                    ···············  0
yaw                      ···········█·█·  2
roll_rate                ···············  0
pitch_rate               ···············  0
yaw_rate                 ···············  0
position_x               ···█··█····█·█·  4
position_y               ·······█·······  1
position_z               ······█·█··███·  5
velocity_x               ····█····█·█·█·  4
velocity_y               ···········█·█·  2
velocity_z               ···········█·█·  2
altitude                 ······█·█··███·  5
vertical_speed           ···········█·█·  2
heading                  ···········█·█·  2
command_roll__lag_1      █·█████████████ 14
command_pitch__lag_1     ███████████████ 15
command_yaw__lag_1       ███████████████ 15
command_throttle__lag_1  ███████████████ 15
roll__lag_1              ···············  0
pitch__lag_1             ···········█·█·  2
yaw__lag_1               ···········█·█·  2
roll_rate__lag_1         ···············  0
pitch_rate__lag_1        ···············  0
yaw_rate__lag_1          ···██··········  2
position_x__lag_1        ····█·█····█·█·  4
position_y__lag_1        ···············  0
position_z__lag_1        ········█··███·  4
velocity_x__lag_1        ···········█·█·  2
velocity_y__lag_1        ···········█·█·  2
velocity_z__lag_1        ···········█·█·  2
altitude__lag_1          ········█··███·  4
vertical_speed__lag_1    ···········█·█·  2
heading__lag_1           ···········█·█·  2
command_roll__lag_2      ███████████████ 15
command_pitch__lag_2     ███████████████ 15
command_yaw__lag_2       ███████████████ 15
command_throttle__lag_2  ███████████████ 15
roll__lag_2              ···············  0
pitch__lag_2             ···········█·█·  2
yaw__lag_2               ···············  0
roll_rate__lag_2         ···············  0
pitch_rate__lag_2        ···············  0
yaw_rate__lag_2          ····█··········  1
position_x__lag_2        ···██··········  2
position_y__lag_2        ···██······█·█·  4
position_z__lag_2        ········█··███·  4
velocity_x__lag_2        ···██··········  2
velocity_y__lag_2        ···············  0
velocity_z__lag_2        ···············  0
altitude__lag_2          ········█··███·  4
vertical_speed__lag_2    ···············  0
heading__lag_2           ···············  0
command_roll__lag_3      ███████████████ 15
command_pitch__lag_3     ███████████████ 15
command_yaw__lag_3       ███████████████ 15
command_throttle__lag_3  ·██████████████ 14
roll__lag_3              ···············  0
pitch__lag_3             ···············  0
yaw__lag_3               ···············  0
roll_rate__lag_3         ···············  0
pitch_rate__lag_3        ···············  0
yaw_rate__lag_3          ···············  0
position_x__lag_3        ···········█·█·  2
position_y__lag_3        ···········█·█·  2
position_z__lag_3        ···········█·█·  2
velocity_x__lag_3        ···········█·█·  2
velocity_y__lag_3        ···············  0
velocity_z__lag_3        ···············  0
altitude__lag_3          ···········█·█·  2
vertical_speed__lag_3    ···············  0
heading__lag_3           ···············  0
```

`commands_plus_state_history x next_raw_state | ridge_affine | pooled`

```text
command_roll             ···············  0
command_pitch            ···············  0
command_yaw              ···············  0
command_throttle         ···············  0
roll                     ···············  0
pitch                    ···············  0
yaw                      ···············  0
roll_rate                ···············  0
pitch_rate               ···············  0
yaw_rate                 ···············  0
position_x               ···············  0
position_y               ···············  0
position_z               ········█···█··  2
velocity_x               ···············  0
velocity_y               ···············  0
velocity_z               ···········█·█·  2
altitude                 ········█···█··  2
vertical_speed           ···········█·█·  2
heading                  ···············  0
command_roll__lag_1      ···············  0
command_pitch__lag_1     ···············  0
command_yaw__lag_1       ···············  0
command_throttle__lag_1  ···············  0
roll__lag_1              ···············  0
pitch__lag_1             ···············  0
yaw__lag_1               ···············  0
roll_rate__lag_1         ···············  0
pitch_rate__lag_1        ···············  0
yaw_rate__lag_1          ···············  0
position_x__lag_1        ···············  0
position_y__lag_1        ···············  0
position_z__lag_1        ········█···█··  2
velocity_x__lag_1        ···············  0
velocity_y__lag_1        ···············  0
velocity_z__lag_1        ···············  0
altitude__lag_1          ········█···█··  2
vertical_speed__lag_1    ···············  0
heading__lag_1           ···············  0
command_roll__lag_2      ···············  0
command_pitch__lag_2     ···············  0
command_yaw__lag_2       ···············  0
command_throttle__lag_2  ···············  0
roll__lag_2              ···············  0
pitch__lag_2             ···············  0
yaw__lag_2               ···············  0
roll_rate__lag_2         ···············  0
pitch_rate__lag_2        ···············  0
yaw_rate__lag_2          ···············  0
position_x__lag_2        ···············  0
position_y__lag_2        ···············  0
position_z__lag_2        ········█···█··  2
velocity_x__lag_2        ···············  0
velocity_y__lag_2        ···············  0
velocity_z__lag_2        ···············  0
altitude__lag_2          ········█···█··  2
vertical_speed__lag_2    ···············  0
heading__lag_2           ···············  0
command_roll__lag_3      ···············  0
command_pitch__lag_3     ···············  0
command_yaw__lag_3       ···············  0
command_throttle__lag_3  ···············  0
roll__lag_3              ···············  0
pitch__lag_3             ···············  0
yaw__lag_3               ···············  0
roll_rate__lag_3         ···············  0
pitch_rate__lag_3        ···············  0
yaw_rate__lag_3          ···············  0
position_x__lag_3        ···············  0
position_y__lag_3        ···············  0
position_z__lag_3        ········█···█··  2
velocity_x__lag_3        ···············  0
velocity_y__lag_3        ···············  0
velocity_z__lag_3        ···············  0
altitude__lag_3          ········█···█··  2
vertical_speed__lag_3    ···············  0
heading__lag_3           ···············  0
```

### 3.6 条件数为什么这么高，它暗示了什么

`summary.md` 给出的 conditioning 信息是：

- `raw_condition_number = inf`
- `effective_condition_number ≈ 1259416.2092`
- 被 conditioning 剪掉的典型特征包括：
  - `altitude` 及其 history
  - `vertical_speed` 及其 history
  - 若干 `command_throttle` history alias

这背后的数学含义是：

1. 原始特征矩阵存在精确共线性。
   仓库源码里明确把 `altitude` 视作 `position_z` 的 alias，把 `vertical_speed` 视作 `velocity_z` 的 alias。`raw_condition_number = inf` 正是在说：不做处理时，`X` 的列空间里有完全重复或线性相关的方向。

2. 即使做了 alias / one-hot baseline / rank pruning，问题仍然“几乎奇异”。
   `1.259e6` 不是普通意义上的“大一点”，而是已经大到说明最小奇异值非常小，系数求解对微小扰动高度敏感。

3. 这会削弱单个系数的物理可解释性。
   也就是说：
   - 预测可以很好；
   - 但某一个具体系数的正负号和数值大小，不一定能稳当地对应“真实物理因果强度”；
   - 不同但近似等价的系数组合，可能给出非常接近的预测结果。

4. 这也是为什么最佳结果只能算 `partial`。
   按仓库 `classify_support` 的规则，`R2 >= 0.70`、`stability >= 0.60` 且 `condition_number <= 1e6` 才能算 `supported`。当前 best 虽然精度高、稳定性也高，但 conditioning 没过线。

5. 对现实物理意义的暗示是：
   当前 fitted `f` 更像一个“窄实验范围内好用的预测算子”，而不是一个可以直接当作全局物理定律解释的、唯一可识别的控制映射。

顺便强调一点：`coefficient_stability = 1.0000` 并不和高条件数矛盾。前者是在当前 split/bootstrap 与阈值规则下，统计上看“被选中的系数比较稳定”；后者是在说这个线性反问题本身仍然接近不可识别。

## 4. 预测目标的差异：Y-side schema 对比

### 4.1 哪个更容易被线性公式拟合

结论非常明确：

- `next_raw_state` 明显更容易被线性模型拟合。
- `actuator_response` 在当前真实 PX4 scope 下几乎不能被这个全局线性框架有效解释。

### 4.2 直接数据依据

先看“每个 Y schema 的最佳结果”：

| Y schema | 最佳 X/model | median test R2 |
| --- | --- | ---: |
| `next_raw_state` | `commands_plus_state_history | ols_affine` | `0.9726` |
| `future_state_horizon` | `commands_plus_state_history | lasso_affine` | `0.6627` |
| `selected_state_subset` | `commands_plus_state_history | lasso_affine` | `0.4997` |
| `delta_state` | `commands_plus_state_history | lasso_affine` | `-0.0169` |
| `actuator_response` | `commands_plus_state | ridge_affine` | `-0.4104` |

只看你点名的两类：

| Y schema | 最佳 R2 | 结论 |
| --- | ---: | --- |
| `next_raw_state` | `0.9726` | 强可拟合 |
| `actuator_response` | `-0.4104` | 不可拟合 |

两者最佳结果的直接差值是：

- `0.9726 - (-0.4104) = 1.3830`

再看同一个 X 下的对比，结论也一致：

| X schema | `next_raw_state` 最佳 R2 | `actuator_response` 最佳 R2 | 差值 |
| --- | ---: | ---: | ---: |
| `commands_plus_state` | `0.9663` | `-0.4104` | `+1.3767` |
| `commands_plus_state_history` | `0.9726` | `-0.4834` | `+1.4560` |

### 4.3 为什么会这样

一个合理解释是：

- `next_raw_state` 是更接近系统外显运动学结果的量，已经把底层执行器、姿态环、分配器、模式逻辑、饱和等内部复杂性“积分”进去了；
- `actuator_response` 更贴近底层控制链，受隐藏状态、内部控制器、混控与限幅逻辑影响更大；
- 当前 `X` 虽然已经有 command、state 和 history，但仍不足以把底层 actuator 响应压缩成一个固定的全局线性映射。

所以，在这个实验里：

- “预测无人机下一步原始状态”可以被高精度线性近似；
- “预测底层执行器响应”不行。

## 5. 对默认研究问题的直接回答

`docs/RESEARCH_GOAL.md` 的默认问题是：

> 在给定 study scope 下，是否存在一个固定的全局线性或仿射映射 `Y ≈ fX (+ b)`，可以较好解释 UAV 的输入-响应关系？

结合 `docs/STAGE_REPORT_2026-04-07.md` 与本次权威 study，我的直接回答是：

### 5.1 是否存在固定的全局线性或仿射映射 `Y ≈ fX + b`

有，但只是在“精心选择的 X/Y 定义”下，且只能算部分成立。

更具体地说：

- 若把问题定义为 `commands_plus_state_history -> next_raw_state`，则确实存在一个固定的 pooled 仿射近似，且预测效果很强：`median_test_r2 = 0.9726`。
- 但这个结论只对当前 very narrow scope 成立：
  - PX4
  - `gz_x500`
  - `POSCTL` 与 `OFFBOARD_ATTITUDE`
  - `nominal`
  - pooled 主报告

### 5.2 线性模型足以完美解释它的飞行行为吗

不够。

理由有五个：

1. 仓库自己都把 best result 判成 `partial`，不是 `supported`。
2. `effective_condition_number ≈ 1.259e6` 太高，说明映射虽然能预测，但不够稳健、不够可识别。
3. `actuator_response`、`delta_state` 等 Y 定义并没有被同一套全局线性假设解释好。
4. `commands_only` 完全失败，说明单靠“输入命令 -> 响应”这一层抽象并不成立，必须把当前状态作为上下文带进去。
5. 最佳结果也不是零误差：`MSE = 0.000046`、`MAE = 0.003960`，因此离“完美解释”还有距离。

因此，最准确的结论是：

> 在当前 PX4 `gz_x500`、`POSCTL` 与 `OFFBOARD_ATTITUDE` 的 study scope 下，存在一个对 `next_raw_state` 很有效的全局仿射近似；但它不是一个对所有响应定义都成立、数值上也足够健康、并且能完美解释飞行行为的统一线性定律。

## 6. 给不了解仓库的人：目录结构、关键文件与建议阅读路径

### 6.1 顶层目录结构

```text
autopilot_lab/
├── README.md
├── AGENTLOG.md
├── PJINFO.md
├── artifacts/
│   ├── px4_matrix/
│   ├── raw/
│   └── studies/
├── configs/
│   ├── ablations/
│   └── studies/
├── doc/
├── docs/
├── scripts/
├── src/
│   ├── ardupilot_mavlink_backend/
│   ├── linearity_analysis/
│   ├── linearity_core/
│   ├── linearity_study/
│   ├── px4_msgs/
│   ├── px4_ros2_backend/
│   └── px4_ros_com/
└── tests/
```

### 6.2 关键目录解释

| 路径 | 作用 |
| --- | --- |
| `README.md` | 仓库总体说明、当前权威实验、快速入口 |
| `docs/RESEARCH_GOAL.md` | 默认研究问题，定义“到底在验证什么” |
| `docs/STAGE_REPORT_2026-04-07.md` | 当前阶段 scope、权威 artifacts、当前最重要结论 |
| `docs/XY_SCHEMA_GUIDE.md` | `X-schema` / `Y-schema` 的具体语义 |
| `docs/EXPERIMENT_PROTOCOL.md` | 实验主流程与推荐研究顺序 |
| `configs/ablations/` | broad ablation 的计划矩阵 |
| `configs/studies/` | 单项 study 配置 |
| `scripts/` | 环境检查、运行主实验、重跑 broad ablation 的脚本入口 |
| `src/linearity_core/` | schema 构造、拟合、条件数与报告核心逻辑 |
| `src/linearity_analysis/` | schema 比较、聚合与 study 输出 |
| `src/linearity_study/` | 主实验执行入口 |
| `artifacts/raw/` | 原始 PX4 / synthetic 采集结果 |
| `artifacts/studies/` | prepared 数据、拟合结果、报告与总结 |
| `tests/` | 回归测试、artifact smoke、conditioning 与 schema 注册测试 |

### 6.3 当前权威 study 的结构

```text
artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/
├── manifest.yaml
├── prepared/
│   ├── sample_table.csv
│   └── schema_inventory.yaml
├── fits/
│   └── <x_schema>__<y_schema>__pooled/
│       └── <model>/
│           ├── matrix_f.csv
│           ├── bias_b.csv
│           ├── sparsity_mask.csv
│           ├── metrics.json
│           └── residuals.csv
├── reports/
│   ├── summary.md
│   └── schema_comparison.md
└── summary/
    └── study_summary.json
```

### 6.4 每个关键文件怎么看

| 文件 | 建议看法 |
| --- | --- |
| `prepared/sample_table.csv` | 真实训练表，确认每一行样本都有哪些列 |
| `prepared/schema_inventory.yaml` | 看 run 数、row 数、数据质量、可用字段和 feature inventory |
| `reports/summary.md` | 看最终口径的“标准答案” |
| `reports/schema_comparison.md` | 看所有 schema 的排序与指标差异 |
| `summary/study_summary.json` | 结构化结果，适合做二次分析或写自动报告 |
| `fits/.../matrix_f.csv` | 真正的线性映射矩阵 `f` |
| `fits/.../bias_b.csv` | 偏置项 `b` |
| `fits/.../sparsity_mask.csv` | 稀疏支持集，比直接看 `matrix_f` 更适合看结构 |
| `fits/.../metrics.json` | 完整指标、特征名、输出名、top influential、conditioning 信息 |
| `fits/.../residuals.csv` | 看误差分布、异常样本与分模式表现 |

### 6.5 按实验流程的建议阅读顺序

如果一个人完全不了解这个代码仓，我建议按下面顺序看：

1. `docs/RESEARCH_GOAL.md`
   先搞清楚仓库不是做控制器设计，而是在验证“是否存在固定全局线性/仿射映射”。

2. `docs/STAGE_REPORT_2026-04-07.md`
   确认当前唯一有效 scope、权威 raw run、权威 study 与现阶段结论。

3. `artifacts/studies/.../reports/summary.md`
   先拿到结论，不要一上来就扎进源码。

4. `artifacts/studies/.../reports/schema_comparison.md`
   再看为什么这个结论成立，哪些 schema 赢，哪些 schema 输。

5. `artifacts/studies/.../prepared/schema_inventory.yaml`
   看这次 study 实际用了哪些 run、多少样本、缺失率如何、哪些特征真的可用。

6. 选一个重点组合去看 `fits/.../matrix_f.csv`、`bias_b.csv`、`sparsity_mask.csv`
   推荐先看：
   - `commands_plus_state_history__next_raw_state__pooled/ols_affine`
   - `commands_plus_state_history__next_raw_state__pooled/ridge_affine`

7. 再回到 `docs/XY_SCHEMA_GUIDE.md`
   结合拟合结果理解 `commands_only`、`commands_plus_state`、`history`、`next_raw_state`、`actuator_response` 的具体含义。

8. 最后才看源码
   推荐顺序：
   - `src/linearity_core/linearity_core/fit.py`
   - `src/linearity_core/linearity_core/report.py`
   - `src/linearity_analysis/`

9. 如果要复现实验，再去看：
   - `configs/ablations/px4_real_broad_ablation_balanced.yaml`
   - `scripts/run_px4_broad_ablation.sh`

### 6.6 一个最省时间的“理解仓库”最短路径

如果只有 15 分钟，我建议只看这 6 个文件：

1. `docs/RESEARCH_GOAL.md`
2. `docs/STAGE_REPORT_2026-04-07.md`
3. `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/reports/summary.md`
4. `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/reports/schema_comparison.md`
5. `artifacts/studies/20260407_031229_px4_real_broad_ablation_balanced/prepared/schema_inventory.yaml`
6. `src/linearity_core/linearity_core/fit.py`

## 最终结论

用一句话压缩整份报告：

> 当前仓库已经证明：在 PX4 `gz_x500`、`POSCTL/OFFBOARD_ATTITUDE`、`nominal` 的窄 scope 内，只要把“当前状态”放进输入，下一步原始状态可以被一个固定的全局仿射模型高精度近似；但这个模型仍然数值病态、对某些 Y 定义失败，因此它是“强预测近似”，不是“完美线性真相”。

## 阶段性问题回答（2026-04-08）

### A. 本轮对话实际完成了什么

这一轮对话主要把“当前 PX4 实验到底在做什么、数据是怎么组织的、为什么你一开始看不到明显动作、后续如何保证每次实验都能看见 Gazebo 可视化”这几件事彻底厘清了。

首先，已经把 `prepared/sample_table.csv` 的含义讲清楚了：它不是原始飞控日志，而是全局线性研究使用的统一训练底表。它把 `input_trace.csv` 与姿态、角速度、位置、执行器、控制状态等 topic 对齐后，整理成“一行一个监督样本”的宽表，然后再由不同的 `X-schema / Y-schema` 从中切列形成真正的 `X` 和 `Y`。相关逻辑在 `docs/DATA_SCHEMA.md`、`src/linearity_core/linearity_core/dataset.py` 和 `src/linearity_core/linearity_core/schemas.py`。

其次，已经解释了 `OLS / Ridge / Lasso` 的差异：`OLS` 是普通最小二乘，追求误差最小；`Ridge` 加 `L2` 正则，主要解决病态和共线性；`Lasso` 加 `L1` 正则，更偏向产生稀疏系数。它们在当前 PX4 结果中的角色也比较清楚：`OLS` 给到最高精度，`Ridge` 给到更强的稳定与稀疏倾向，`Lasso` 介于两者之间。

再次，已经把“仿真时飞机做什么动作是由谁指定的”讲清楚了。动作不是手动临时写死，而是由 study config 中的 `input_type / axis / profile_type / amplitude / duration / extras` 等字段定义，再由 `ExcitationGenerator` 生成时序命令，最后由 PX4 backend 的 injector 实际注入。

### B. 本轮排查出的关键问题

你最开始看到“只有起飞、没有后续明显动作”，不是观察问题，而是第一次 raw run 根本没有进入动作段。检查 `artifacts/raw/px4/20260408_020028_px4_manual_broad_composite_r1/manifest.yaml` 与 `telemetry/input_trace.csv` 后可以确认：

- `experiment_start_time_ns = null`
- 存在 `takeoff_clearance_timeout`
- `phase` 只有 `warmup_position` 和 `takeoff_position_hold`
- `command_roll / pitch / yaw / throttle` 全程为 `0`

也就是说，那一轮只完成了起飞保持，没有开始真正的 `broad/composite` 扰动。

为此，已经修正了 PX4 注入器的起飞完成判定逻辑，使其不再只依赖单一的局部坐标 `z` 收敛，而是允许“达到目标高度”或“达到有效离地间隙”二者之一即可视为进入动作段。修改位置：

- `src/px4_ros2_backend/px4_ros2_backend/manual_input_injector.py`
- `src/px4_ros2_backend/px4_ros2_backend/attitude_injector.py`

修正后重新跑的 `artifacts/raw/px4/20260408_020617_px4_manual_broad_composite_r1` 已经确认进入了 `broad_active` 段，说明动作注入链路本身是通的。

### C. 为了“看得见”，本轮新增了两类高可见度演示

为了让 Gazebo 窗口中的动作更明显，本轮没有直接修改正式研究配置，而是单独增加了视觉演示配置。

第一类是大幅 `roll sweep` 演示：

- 配置：`configs/studies/px4_visual_demo_offboard_roll_sweep_capture.yaml`
- run：`artifacts/raw/px4/20260408_022211_px4_attitude_sweep_roll_r1`

这轮的特点是姿态滚转明显，视觉效果强，但横向漂移也更大，因此更适合确认“系统确实在动”，不太适合强调“原地保持”。

第二类是大幅 `yaw sweep` 演示：

- 配置：`configs/studies/px4_visual_demo_offboard_yaw_sweep_capture.yaml`
- run：`artifacts/raw/px4/20260408_022647_px4_attitude_sweep_yaw_r1`
- 重放 run：`artifacts/raw/px4/20260408_022855_px4_attitude_sweep_yaw_r1`

这轮的特点是：

- `command_yaw` 约为 `-0.9 ~ 0.9`
- `roll / pitch` 保持很小
- 视觉上更接近“机头左右摆动”
- 横移比 `roll sweep` 小，更适合演示

因此，如果后续只是为了给人看动作过程，`yaw sweep` 比 `roll sweep` 更合适。

### D. 后续“每次实验都默认带可视化窗口”已经接通

这轮已经把 PX4 的默认实验入口改成“只要有显示环境，就默认起带 GUI 的 Gazebo”，而不是默认 headless。当前已经接通的入口有：

- `src/px4_ros2_backend/px4_ros2_backend/matrix_runner.py`
- `src/linearity_study/linearity_study/linearity_run_study.py`
- `src/px4_ros2_backend/px4_ros2_backend/experiment_runner.py`

因此，后续无论是：

- 跑 PX4 broad ablation
- 跑单个 study
- 跑单次 raw capture

都会优先弹出 Gazebo 窗口，方便观察。只有显式设置 `AUTOPILOT_LAB_HEADLESS=1` 时才会退回无窗口模式。

### E. 在引入 ArduPilot 之前，PX4 还缺什么

如果问题只是“PX4 当前能不能给出第一阶段研究结论”，答案是可以。当前权威报告已经足以支持一个明确口径：

- 在 `gz_x500 + POSCTL/OFFBOARD_ATTITUDE + nominal` 的当前 scope 下
- 固定全局仿射模型对 `next_raw_state` 可以给出很强的预测近似
- 但这种近似仍然数值病态，不能被解释为完美、全局、稳定、物理可解释的线性真相

但如果问题是“PX4 现在能不能直接作为引入 ArduPilot 前的稳定基线”，答案是还不够。

在引入 ArduPilot 之前，PX4 至少还建议补以下几类内容：

1. 更多 fresh repeats

当前权威主报告本质上仍接近“每个 mode 一条主 run”的口径。对于真正的 backend 对照基线，这个统计支撑偏弱。建议：

- `POSCTL` 至少补到 `3-5` 个 repeats
- `OFFBOARD_ATTITUDE` 至少补到 `3-5` 个 repeats

重点观察：

- `median_test_r2`
- `effective_condition_number`
- `sparsity_mask`
- `support` 是否稳定

2. 单轴动作输入

当前正式主报告以 `broad + composite` 为主，这适合覆盖更广状态空间，但不利于诊断“是哪一类控制通道最先破坏全局线性假设”。建议补：

- `roll` 单轴 sweep
- `pitch` 单轴 sweep
- `yaw` 单轴 sweep
- `throttle` 单轴 sweep 或 pulse

这些实验不一定都要进入权威主报告，但至少应该形成一套 PX4-only 诊断集。

3. 幅度分层

当前结论更多描述的是“小到中等扰动下”的线性可近似性。为了更严肃地回答“全局线性到底能撑多远”，建议同一 mode 下补：

- small amplitude
- medium amplitude
- large amplitude

看线性结论在何处开始明显恶化。

4. pooled vs stratified 对照

当前权威主结论主要是 pooled 口径，而 `docs/STAGE_REPORT_2026-04-07.md` 也已经明确把 stratified 对照列为下一步。这一页在 ArduPilot 引入前最好补齐，否则 backend 对比时会缺少一个重要维度。

5. raw run 验收门槛

这轮实际已经暴露出一个重要事实：流程成功不等于动作真正有效。建议在 PX4 raw run 层加入硬验收条件，例如：

- 必须进入 active phase
- 必须存在足够多非零命令样本
- 不能在动作段开始前就失败
- failsafe 导致动作段被截断时应标记为不合格研究 run

6. 演示配置与研究配置分层

像 `roll/yaw visual demo` 这类配置很适合观察，但不应该混入正式 broad ablation 研究口径。建议保留两套明确边界：

- `demo-only`
- `authoritative research`

### F. 是否需要预留 ArduPilot 相关代码区域

需要，但不需要为此再做一层很重的新抽象。

从当前仓库结构看，ArduPilot backend 已经有独立区域：

- `src/ardupilot_mavlink_backend/ardupilot_mavlink_backend/`

因此，现在真正需要“预留”的，不是再新建一堆空文件或空模块，而是把跨 backend 的契约压实。更具体地说，应该重点保证这些东西一致：

- `prepared sample table` 的 canonical 列口径
- `manifest` 的结构
- `data_quality` 的结构
- raw run 的验收标准
- `X/Y schema` 的切列规则与命名

换句话说，真正需要预留的是“接口契约区”，而不是“提前铺很多 ArduPilot 占位代码”。

当前更合理的策略是：

- 继续保留 PX4 和 ArduPilot 各自独立的 backend runner / capture / session 实现
- 把分析层和 prepared table 层的统一口径固定住
- 等 PX4 基线稳定后，再把同一套实验矩阵移植到 ArduPilot

### G. 当前阶段的判断

到目前为止，PX4 已经足够支撑第一阶段主结论，但还不足以作为一个非常稳固的、可直接与 ArduPilot 做强对照的最终基线。

更准确地说，当前状态应理解为：

- 研究链路已通
- 结论已形成
- 可视化与演示已补上
- 但 PX4-only 基线仍需要做重复轮次、动作覆盖和验收强化

只有把这些补齐之后，再引入 ArduPilot，才更容易区分：

- 是 backend 差异导致结论变化
- 还是 PX4 基线本身就还不够稳

### H. TODO

- 给 `POSCTL` 和 `OFFBOARD_ATTITUDE` 各补 `3-5` 个 fresh repeats。
- 增加 PX4-only 单轴动作实验：`roll / pitch / yaw / throttle`。
- 增加 PX4-only 幅度分层实验：`small / medium / large`。
- 产出一页正式的 `pooled vs stratified` PX4 对照报告。
- 在 raw run 层增加硬验收门：`active phase`、非零命令样本数、动作前失败检测、failsafe 截断检测。
- 明确区分 `visual demo configs` 与 `authoritative research configs`。
- 固定跨 backend 的 `prepared table / manifest / data_quality / schema naming` 契约。
- 在 PX4 基线稳定后，再把同一套实验矩阵迁移到 ArduPilot。
