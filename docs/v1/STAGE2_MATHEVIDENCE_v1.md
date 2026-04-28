# Stage 2 Mathematical Evidence

## 目的

本文记录 Stage 2 in-depth 分析的数学依据，回答两个问题：

- 六条机制线为什么可以被放在一起做共同成因分析。
- Stage 2 的结论到底是哪些“硬证据”支持出来的，哪些部分属于进一步的研究推断。

这里的核心思想不是比较“谁最好”，而是把六条线都写进同一个数学框架，再比较它们的共同结构与共同边界。

## 基础模型

Stage 2 的底层都建立在同一个局部线性或仿射模型上：

\[
Y \approx XW + b
\]

其中：

- `X`：输入矩阵。
- `Y`：输出矩阵。
- `W`：输入到输出的系数矩阵。
- `b`：偏置项。

在实现里，`X` 会先标准化，再做 `ols_affine` 或 `ridge_affine` 拟合，最后恢复成原始坐标下的 `coef` 与 `bias`。对应实现位于：

- `src/linearity_core/linearity_core/fit.py`
- 关键函数：`_fit_single_model(...)`、`fit_schema_combo(...)`

## Support 与 Generalization 的硬判据

Stage 2 不会把任意高分拟合都当成可靠结构。仓库里“supported”的判据是明确的：

- 中位测试 `R² >= 0.70`
- 系数稳定性 `>= 0.60`
- 条件数 `<= 1e6`

也就是说，一条线至少要同时满足：

- 拟合效果足够强；
- 多次重采样后系数不要大幅漂移；
- 数值条件不能病态到无法稳定解释。

这些判据定义在：

- `src/linearity_core/linearity_core/report.py`
- 关键函数：`classify_support(...)`

跨场景“真的泛化”还要额外满足：

- `scenario_consistency >= 0.60`
- 每个预期场景子组的 `R² >= 0.70`

其中：

\[
\text{scenario\_consistency} = \frac{\min R^2_{\text{scenario}}}{\max R^2_{\text{scenario}}}
\]

这一步的作用是排除“只在某一个局部工况里好看”的线。对应实现位于：

- `src/linearity_core/linearity_core/study_artifacts.py`
- 关键函数：`_scenario_generalization_status(...)`

## Stage 2 真的在比较什么

Stage 2 把六条机制线都压缩成四组可计算描述符，而不是只看一个分数。

### 1. 支持集几何

这组量回答：“有效作用到底集中在哪里？”

- `support_nonzero_count`：稳定稀疏掩码里有多少个非零位置。
- `row_dominance`：

\[
\text{row\_dominance} = \frac{\max_i \sum_j |W_{ij}|}{\sum_{i,j}|W_{ij}|}
\]

它衡量是不是“几乎由一条输入方向主导”。

- `effective_support_size`：

\[
\text{effective\_support\_size} = \frac{(\sum_i r_i)^2}{\sum_i r_i^2}, \quad r_i=\sum_j |W_{ij}|
\]

它不是简单地数非零位置，而是看质量真正分散在多少行上。

- `mask_jaccard`：基线与诊断阶段稀疏掩码的重叠度。

### 2. 目标束几何

这组量回答：“输出是不是集中打在一小组相关目标上？”

先定义每个输出列的总质量：

\[
c_j = \sum_i |W_{ij}|
\]

然后取质量最大的前三个输出，得到目标束。

- `target_bundle_compactness`：

\[
\text{compactness} = \frac{\sum_{j \in \text{Top-3}} c_j}{\sum_j c_j}
\]

越大说明输出越集中。

- `off_target_leakage = 1 - compactness`

这表示外溢程度，也就是本来只想推动目标响应，却有多少质量泄到了非目标输出上。

### 3. 传递核画像

这组量回答：“影响主要从哪里来？”

输入被分成五类：

- `command`：控制指令
- `state_current`：当前状态
- `history`：历史滞后项
- `mode_covariate`：模式或后端协变量
- `other`：其他项

然后计算每一类对总质量 \(|W|\) 的贡献比例：

\[
\text{share(block)} = \frac{\sum_{i \in \text{block}, j}|W_{ij}|}{\sum_{i,j}|W_{ij}|}
\]

这一步决定一条线更像：

- 状态传递
- 直接传递
- 历史传递

### 4. 边界与稳健性指标

这组量回答：“这条线为什么难，或者为什么可靠？”

- `effective_condition_number`

\[
\kappa_{\text{eff}} = \frac{\sigma_{\max}}{\sigma_{\min}}
\]

这里不是直接对原始矩阵算条件数，而是先删除精确别名列、one-hot 基线列，再保留线性独立列后再算。这样做是为了避免把“形式上重复编码”误当成真正的病态。

- `raw_top_edge_jaccard`：基线和诊断阶段最强若干条边是否重合。
- `scenario_consistency`：跨场景稳定性。

## 六条机制线的关键数值证据

下面列出最关键的数值，作为后续结论的直接依据。

### AP-DAB

- `R²` 约为 `0.998`
- 有效条件数约为 `1.04 ~ 1.51`
- 稳定支持集非零数 `4`
- `row_dominance ≈ 0.99`
- `effective_support_size ≈ 1.01`
- 目标束紧度约 `0.75`
- 外溢约 `0.25`
- `command_share = 1.0`

这说明它几乎就是“一条控制方向推动一组执行器响应”，而且数值稳定、结构重复、直接性很强。

### PX-STC / PX-STD

- `PX-STC` 的 `R²` 约为 `0.999`
- `PX-STD` 的 `R²` 约为 `0.75 ~ 0.81`
- 两者有效条件数都在 `10^3` 量级
- 掩码重叠度约 `0.61 ~ 0.63`
- 目标束在基线和诊断阶段保持一致
- `command_share` 只有约 `0.09`
- `state_current_share + history_share` 合计约 `0.84 ~ 0.85`

这说明它们不是“控制直接打输出”，而是当前状态和历史状态共同把影响往后传。

### AP-HTM / AP-HTG

- `R² = 1.0`
- 有效条件数在 `10^9` 量级
- 目标束紧度约 `0.5`
- 外溢约 `0.5`
- `history_share ≈ 0.75`

这说明线性结构本身并没有消失，但它们数值极不稳定，而且目标外溢很大，所以“可拟合”不等于“可稳定利用”。

### AP-HTS

- `baseline R² = 1.0`
- `diagnostic R² ≈ 0.913`
- 有效条件数从约 `2.18e6` 降到约 `1848`
- 稳定掩码非零数为 `0`
- 目标束紧度高达 `0.994 ~ 0.998`
- 外溢极低

这说明它不是没有结构，而是到了一个边界区：原始质量仍然强烈集中在某些输出上，但稳定稀疏支持集已经抓不住它。

## Stage 2 三个核心结论的数学依据

### 结论一：六条线都更像低维方向映射，而不是任意高维拟合

数学依据是：

- 每条线都能写成同一个 \(Y \approx XW+b\) 模型；
- 质量不是均匀铺满整个矩阵，而是存在明显集中；
- `AP-DAB` 展示了最极端的低维结构：`support_nonzero_count = 4`，`row_dominance ≈ 0.99`；
- `PX-STC/PX-STD` 虽然更分布式，但目标束在不同阶段保持稳定；
- `AP-HTS/AP-HTG` 即使稳定掩码已经退化，原始拟合仍然能保持高 `R²`，说明结构还在。

因此，Stage 2 不把这些线理解成“随便拟合出的高维噪声”，而是理解成少数关键输入方向推动一组相关输出的方向映射。

### 结论二：六条线可以归成三类传递机制

数学依据是输入质量分布：

- `AP-DAB`：`command_share = 1.0`，典型直接传递。
- `PX-STC/PX-STD`：`command_share` 很低，而 `state_current_share + history_share` 很高，说明它们是状态主导的传播。
- `AP-HTM/AP-HTS/AP-HTG`：历史项占主导，说明它们依赖过去一段时间的信息。

所以这三类机制不是人工命名，而是从输入块质量分布中归纳出来的。

### 结论三：真正的边界来自外溢、病态条件数和模式变化，而不是线性结构消失

数学依据是：

- `AP-HTM/AP-HTG` 的 `R²` 仍然等于 `1.0`，但条件数达到 `10^9`，说明“能拟合”与“能稳定利用”是两回事；
- 这两条线的目标束紧度只有 `0.5`，也就是一半质量都泄到了非目标响应上；
- `AP-HTS` 的稳定掩码已经空了，但高 `R²` 和极高目标束紧度仍然存在，说明它更像“边界塌缩”，而不是“结构消失”；
- `PX-STC/PX-STD` 与 `AP-DAB` 在跨阶段仍保有一定支持重叠和场景一致性，所以可以视为更稳的机制证据。

因此，Stage 2 的核心判断不是“有的线有结构，有的线没结构”，而是：

- 结构大多仍在；
- 但有些线会被外溢、数值病态或模式切换卡住。

## 哪些是硬证据，哪些是研究推断

### 硬证据

下面这些量是直接计算出来的：

- `R²`
- 有效条件数
- 系数稳定性
- 稀疏掩码与非零计数
- `row_dominance`
- `effective_support_size`
- `target_bundle_compactness`
- `off_target_leakage`
- `mask_jaccard`
- `raw_top_edge_jaccard`
- 输入块质量分布

### 研究推断

下面这些不是数学定理，而是基于上述证据做出的机制归纳：

- `PX-STC/PX-STD` 属于 state-transport 家族
- `AP-DAB` 属于 direct-transport
- `AP-HTM/AP-HTS/AP-HTG` 属于 history-transport
- 后续统一算法应同时支持这三类机制
- 算法中必须显式处理外溢和条件数问题

也就是说，Stage 2 的“家族划分”和 `USDTA` 设计启示，属于研究解释；但这些解释是建立在一整套可复现的矩阵描述符之上的。

## 对攻击算法设计的直接启示

从这些数学证据可以直接推出四条设计要求：

- 目标不应定义成单一输出，而应定义成一组相关输出的目标束。
- 算法必须能在状态传递、直接传递、历史传递三种机制之间切换。
- 算法必须内生地惩罚外溢，而不是事后再解释副作用。
- 算法必须内生地约束条件数，否则高拟合分数没有意义。

## 实现对应

如果需要把本文和仓库代码一一对应，主要看下面四个文件：

- `src/linearity_core/linearity_core/fit.py`
- `src/linearity_core/linearity_core/report.py`
- `src/linearity_core/linearity_core/study_artifacts.py`
- `src/linearity_analysis/linearity_analysis/stage2_six_line_common_cause.py`

其中：

- 拟合、条件数、稳定性：`fit.py`
- support 判据：`report.py`
- generalized 判据：`study_artifacts.py`
- Stage 2 四组描述符与六线聚合：`stage2_six_line_common_cause.py`
