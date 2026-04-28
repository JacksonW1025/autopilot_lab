# USDTA 时序稀疏攻击算法 Stage1–4 实验计划

---

## 0. 总体定位

本文档定义一条完整的 USDTA 攻击算法实验线。整条实验线以“可控输入到未来风险输出的稀疏时序响应”为核心对象，将攻击问题建模为一个带有状态/模式选择、时序延迟补偿、不确定性约束、稀疏预算分配和滚动反馈修正的闭环规划问题。

整体流程分为四个阶段：

```text
Stage1: 时序响应建模与攻击可用导数估计
Stage2: 攻击机制编译与时序攻击原语构造
Stage3: USDTA 攻击规划器设计与实现
Stage4: 闭环攻击执行、诊断与版本固化
```

四个阶段之间的关系如下：

```text
授权飞行/仿真数据
  -> Stage1: J[h, tau] 时序响应模型与局部导数集合
  -> Stage2: mechanism ledger + attack primitives
  -> Stage3: sparse temporal robust planner
  -> Stage4: closed-loop attack execution + failure update
  -> 回写 Stage1/2 的模型置信度和适用边界
```

本文档关注攻击算法自身，不把重点放在外部叙事或展示性包装上。每个阶段必须产生可供下一阶段直接调用的机器可读 artifact。

---

## 1. 攻击算法总目标

USDTA 的核心目标是：在给定授权测试环境、当前飞行状态、攻击权限、扰动预算和目标风险函数的条件下，自动选择少量可控输入通道，并规划一段满足约束的时序扰动序列，使未来风险输出按照指定目标方向或放大目标发生变化。

算法不应输出简单的单步扰动方向：

```text
channel + sign + epsilon
```

而应输出时序攻击计划：

```text
attack_plan = {
  selected_mechanisms,
  selected_channels,
  attack_start_offsets,
  durations,
  sign_schedules,
  amplitude_schedule,
  expected_response_profile,
  fallback_rules
}
```

核心建模对象为：

\[
J_r[h, \tau] = \frac{\partial y_{t+h}}{\partial u_{t-\tau}} \mid r
\]

其中：

- `u`：攻击者在当前 threat model 下可控或可扰动的输入，例如 high-level setpoint、velocity command、attitude command、rate command、thrust command、actuator command。
- `y`：未来风险输出或目标输出，例如 tracking error、altitude deviation、attitude error、lateral error、safety margin residual、actuator stress、recovery error。
- `h`：未来预测 horizon。
- `tau`：输入历史 lag。
- `r`：当前飞行 regime，例如 hover、trajectory tracking、turn、transition、disturbance、near-saturation。

攻击规划形式为：

\[
\max_{\delta u_{t:t+T}}
\operatorname{RiskGain}(\delta u; \Phi, \mathcal{J}_r)
- \lambda_E C_E(\delta u)
- \lambda_R C_R(\delta u)
- \lambda_P C_P(\delta u)
\]

subject to:

```text
||delta_u||_inf <= eps_inf
||delta_u||_2 <= eps_2
active_channels(delta_u) <= k_channel
active_blocks(delta_u) <= k_block
TV(delta_u) <= eps_rate
spectral_cost(delta_u) <= eps_spectral
plausibility_cost(delta_u) <= eps_plausibility
support(delta_u) subset actionable_stable_support
```

其中：

- `RiskGain`：目标风险收益。
- `Phi`：攻击目标函数。
- `J_r`：当前 regime 下的导数张量或导数 ensemble。
- `C_E`：能量成本。
- `C_R`：扰动变化率成本。
- `C_P`：command plausibility 成本。
- `T`：规划长度。

---

## 2. 全局实验接口约定

### 2.1 Threat model 接口

所有阶段都必须显式声明当前实验使用的攻击权限。权限不是自然语言标签，而是机器可读 contract。

```yaml
threat_model:
  name: T1_high_level_setpoint
  writable_channels:
    - position_setpoint_x
    - position_setpoint_y
    - altitude_setpoint
    - yaw_setpoint
  readable_channels:
    - position
    - velocity
    - attitude
    - tracking_error
    - flight_mode
  forbidden_channels:
    - estimator_internal_state
    - pid_integral_state
    - motor_output_direct
  max_update_rate_hz: 10
  requires_mode_feedback: true
  requires_state_feedback: true
  online_observation_delay_steps: 1
```

推荐至少支持三类权限：

```text
T1: high-level setpoint / command perturbation
T2: mid-level controller input perturbation
T3: low-level actuator / mixer command perturbation, only for upper-bound or isolated bench simulation
```

Stage3 规划器只能使用 `writable_channels` 生成扰动，只能使用 `readable_channels` 更新在线置信度。任何不可写输入不得进入攻击 support。

### 2.2 风险输出接口

风险输出必须统一为 `risk_output` 对象。

```yaml
risk_outputs:
  tracking_error:
    channels: [ex, ey, ez, evx, evy, evz]
    objective_family: amplification
    default_weight: [1, 1, 1.5, 0.5, 0.5, 0.7]
  safety_margin:
    channels: [altitude_margin, lateral_margin, attitude_margin]
    objective_family: margin_reduction
  actuator_stress:
    channels: [motor_saturation_ratio, control_effort]
    objective_family: stress
  recovery:
    channels: [overshoot, settling_error, recovery_time_proxy]
    objective_family: recovery_degradation
```

### 2.3 扰动预算接口

扰动预算需要同时约束幅度、能量、通道数量、速率、频域特征和可执行性。

```yaml
budget:
  eps_inf:
    altitude_setpoint: 0.05
    velocity_setpoint: 0.04
    yaw_setpoint: 0.03
  eps_l2_total: 1.0
  max_active_channels: 2
  max_active_blocks: 3
  max_duration_steps: 30
  total_variation_limit: 0.35
  spectral_energy_limit: 0.40
  plausibility_percentile_limit: 0.95
  warmup_steps_before_attack: 20
  cooldown_steps_after_attack: 20
```

### 2.4 飞行 regime 接口

Regime 是攻击算法选择局部导数和机制原语的关键变量。

```yaml
regime_features:
  - flight_mode
  - speed_norm
  - altitude_error
  - attitude_error_norm
  - tracking_error_norm
  - control_effort
  - actuator_margin
  - disturbance_flag
  - trajectory_curvature

regimes:
  hover_low_dynamic:
    speed_norm_max: 0.5
    tracking_error_max: 0.2
  trajectory_tracking:
    speed_norm_min: 0.5
    trajectory_curvature_max: 0.3
  turn_or_curved_path:
    trajectory_curvature_min: 0.3
  transition:
    mode_change_recent_steps: 20
  high_workload:
    control_effort_min: 0.7
  near_saturation:
    actuator_margin_max: 0.15
```

Stage1 可以训练 regime-specific 导数模型。Stage3 在线时根据 `o_t` 选择当前 regime。

---

# Stage1: 时序响应建模与攻击可用导数估计

## 3. Stage1 目标

Stage1 的目标是为攻击规划器生成可调用的时序响应模型。它不是简单预测下一状态，而是估计在给定 regime 下，攻击者可控输入扰动对未来风险输出的多步响应：

\[
\Delta y_{t+1:t+H} \approx \sum_{\tau=0}^{L} J_r[h, \tau] \Delta u_{t-\tau}
\]

Stage1 的产物不是单个回归分数，而是：

```text
DerivativeTensorBundle = {
  J_ensemble,
  local_regime_models,
  support_probabilities,
  sign_statistics,
  impulse_response_profiles,
  finite_difference_checks,
  validity_ranges,
  normalization_metadata
}
```

## 4. Stage1 输入数据设计

### 4.1 数据源

所有 Stage1 数据必须来自授权环境：

```text
simulation_rollouts
isolated_testbench_rollouts
safe_enclosed_flight_rollouts, optional
```

每条 rollout 应包含：

```text
run_id
timestamp
flight_mode
mission_phase
state vector s_t
command vector u_t
controller input vector c_t, if accessible
actuator vector a_t, if accessible
tracking target r_t
risk outputs y_t
safety margins m_t
disturbance labels d_t
environment metadata
seed / controller config / stack version
```

### 4.2 采样与对齐

Stage1 需要先做统一时间对齐：

```text
resample_rate_hz: 20 or 50
max_clock_skew_steps: 1
interpolation: zero_order_hold for commands, linear for states
mode_transition_buffer_steps: 5-20
```

对齐后构造：

```text
u_window = [u_{t-L}, ..., u_t]
y_horizon = [y_{t+1}, ..., y_{t+H}]
state_context = s_t or compressed context z_t
regime_label = r_t
```

### 4.3 推荐 horizon 与 lag

初始配置：

```yaml
history_lag_L: [0, 3, 5, 10]
prediction_horizon_H: [5, 10, 20, 40]
planning_horizon_T: 10-30
```

如果控制频率为 20Hz：

```text
H=20 roughly corresponds to 1 second
L=5 roughly corresponds to 0.25 second history
```

不同飞控栈和控制频率必须记录换算关系。

## 5. Stage1 模型族

Stage1 不应只训练一个全局线性模型。推荐使用如下模型族，并最终将它们编译成统一 `J_ensemble`。

### 5.1 Global ridge temporal model

用于获取稳定的全局响应上界：

\[
y_{t+h} = b_h + \sum_{\tau=0}^{L} J[h, \tau] u_{t-\tau} + \epsilon
\]

特点：

```text
优点: 稳定、易实现、适合 baseline derivative
缺点: 不稀疏、不区分 regime
```

输出：

```text
J_global_ridge[h, tau, output, input]
```

### 5.2 Sparse temporal elastic-net model

用于发现稀疏 support：

\[
\min_J ||Y - XJ||_2^2 + \alpha ||J||_1 + \beta ||J||_2^2
\]

建议使用 multi-task 形式，让多个 horizon 或多个相关 output 共享输入 support。

输出：

```text
J_sparse_enet
support_mask
support_probabilities_by_bootstrap
```

### 5.3 Group sparse channel model

不要只在单个 coefficient 层面稀疏。攻击算法更关心“哪个输入通道值得攻击”。建议用 group sparsity：

```text
group = one input channel across all horizons, lags, and selected outputs
```

目标：

\[
\min_J ||Y - XJ||_2^2 + \lambda \sum_g ||J_g||_2
\]

输出：

```text
channel_level_support
mechanism_candidate_groups
```

### 5.4 Smooth temporal response model

飞控响应曲线通常不应在相邻 horizon 间剧烈跳变。加入平滑项：

\[
\lambda_s \sum_h ||J[h+1] - J[h]||_2^2
\]

输出更稳定的 impulse response：

```text
J_smooth
response_peak
response_duration
sign_flip_points
```

### 5.5 Low-rank temporal basis model

将时序响应表示为少量 basis：

\[
J[h, \tau] = \sum_{k=1}^{K} A_k B_k[h, \tau]
\]

推荐 basis：

```text
immediate_step
single_delayed_peak
slow_decay
oscillatory_response
delayed_accumulation
```

优点：减少参数量，直接生成攻击 timing 建议。

### 5.6 Regime-specific local model

按飞行 regime 训练局部导数：

```text
J_hover
J_tracking
J_turn
J_transition
J_high_workload
J_near_saturation
```

如果数据不足，可以使用加权平均：

\[
J_{local}(o_t) = \sum_r w_r(o_t) J_r
\]

其中：

```text
w_r(o_t) = softmax(-distance(features(o_t), center_r) / temperature)
```

### 5.7 Finite-difference response sampler

在仿真环境中，对通过初筛的 input channel 做局部扰动采样：

```text
base rollout: u
plus rollout: u + epsilon e_i over selected block
minus rollout: u - epsilon e_i over selected block
```

计算：

\[
FD_i[h] = \frac{y^+_{t+h} - y^-_{t+h}}{2\epsilon}
\]

FD 不要求覆盖所有通道，只要求覆盖候选攻击机制和边界机制。

## 6. Stage1 训练流程

### 6.1 数据预处理

```text
1. Load rollouts.
2. Align timestamps.
3. Normalize commands and outputs using train-only statistics.
4. Label regime.
5. Build command history windows.
6. Build future risk output horizon labels.
7. Remove invalid windows:
   - missing command
   - invalid mode
   - failsafe event before attack window
   - unstable simulator reset
   - actuator hard saturation, unless the regime is near_saturation
```

### 6.2 分割策略

Stage1 的模型必须能支持攻击规划，因此 split 以 rollout 和 regime 为单位：

```text
train_rollouts
validation_rollouts
heldout_regime_rollouts
heldout_disturbance_rollouts
```

禁止把同一连续时间段随机打散后同时放进训练和测试。

### 6.3 训练顺序

推荐训练顺序：

```text
Step 1: Train global ridge temporal model.
Step 2: Train sparse elastic-net temporal model.
Step 3: Train group sparse channel model.
Step 4: Train regime-specific local models.
Step 5: Build derivative ensemble.
Step 6: Estimate support probabilities and sign statistics.
Step 7: Run FD checks for top mechanism candidates.
Step 8: Export DerivativeTensorBundle.
```

## 7. Stage1 模型选择指标

Stage1 模型不是按预测分数单独排名，而是按攻击可用性综合排名。

### 7.1 预测适配指标

```text
horizon_weighted_nrmse
risk_output_r2
residual_autocorrelation
local_linearity_error
```

### 7.2 攻击可用指标

```text
command_to_risk_gain
active_controllable_channel_count
support_probability
sign_consistency
temporal_peak_clarity
regime_coverage
finite_difference_alignment
```

### 7.3 局部有效性指标

```text
valid_epsilon_range
valid_regime_range
saturation_exclusion_rate
mode_switch_exclusion_rate
response_delay_variance
```

### 7.4 推荐综合选择分数

\[
ModelScore =
\frac{
Gain_{cmd\rightarrow risk}
\cdot SupportStability
\cdot SignConsistency
\cdot FDMatch
\cdot RegimeCoverage
}{
PredictionError + Uncertainty + DelayVariance + \epsilon
}
\]

该分数仅用于选择 Stage2 输入模型，不直接用于最终攻击。

## 8. Stage1 输出产物

推荐目录：

```text
artifacts/stage1_temporal_response_modeling/
  configs/
    threat_model.yaml
    risk_outputs.yaml
    regime_definition.yaml
    derivative_estimator.yaml
    horizon_lag_grid.yaml
  models/
    J_global_ridge.npz
    J_sparse_enet.npz
    J_group_sparse.npz
    J_smooth_temporal.npz
    J_regime_ensemble.npz
  tables/
    model_scores.csv
    support_probabilities.csv
    sign_statistics.csv
    finite_difference_summary.csv
    local_validity_ranges.csv
    regime_model_coverage.csv
  reports/
    STAGE1_MODELING_SUMMARY.md
    DERIVATIVE_TENSOR_BUNDLE.md
    FINITE_DIFFERENCE_RESPONSE_REPORT.md
    REGIME_LOCAL_MODEL_REPORT.md
  schemas/
    derivative_tensor_bundle.schema.json
```

`derivative_tensor_bundle.schema.json` 推荐格式：

```json
{
  "bundle_id": "stage1_YYYYMMDD_stack_scenario",
  "input_channels": ["altitude_setpoint", "yaw_setpoint"],
  "output_channels": ["altitude_error", "lateral_error"],
  "horizons": [1, 2, 3, 4, 5, 10, 20],
  "lags": [0, 1, 2, 3, 4, 5],
  "regimes": ["hover_low_dynamic", "trajectory_tracking"],
  "ensemble_members": 32,
  "normalization": "train_only_zscore",
  "tensor_shape": "member x regime x horizon x lag x output x input"
}
```

## 9. Stage1 进入 Stage2 的条件

至少满足：

```text
1. 存在 A2/A3 可控输入通道的非零稳定响应。
2. 至少一个风险输出族具备清晰 horizon response。
3. 主候选机制的 sign consistency >= 0.70。
4. 主候选机制的 FD sign match >= 0.60。
5. 主候选机制有明确 valid_regime 或 valid_context。
6. 导数模型可以导出为统一 J_ensemble 接口。
```

如果不满足，Stage2 不应生成攻击原语，只应回到 Stage1 补充数据或改动 threat model。

---

# Stage2: 攻击机制编译与时序攻击原语构造

## 10. Stage2 目标

Stage2 的目标是把 Stage1 的导数张量转化为攻击规划器可以直接调用的攻击机制原语。Stage2 不输出“哪个系数最大”，而输出：

```text
在某个 flight regime 下，某个可控输入通道经过某种时序扰动形状，预计会在某个 horizon 对某个风险输出产生何种方向、强度、持续时间和不确定性。
```

Stage2 的核心产物：

```text
MechanismLedger
AttackPrimitiveLibrary
RegimeMechanismIndex
MechanismCompatibilityGraph
UncertaintySet
```

## 11. MechanismLedger 设计

### 11.1 基本字段

每条 mechanism 对应一个可解释的 input-output temporal response。

```yaml
mechanism_id: M_ALT_CMD_TO_ALT_ERR_HOVER_001
input_channel: altitude_setpoint
input_type: high_level_setpoint
output_channel: altitude_error
output_type: tracking_error
objective_family: amplification
valid_regime: hover_low_dynamic
threat_models: [T1_high_level_setpoint, T2_mid_level_input]
actionability_level: A3
```

### 11.2 时序字段

```yaml
horizon_profile:
  peak_horizon: 8
  peak_lag: 0
  response_duration_steps: 6
  response_start_horizon: 3
  response_end_horizon: 14
  sign_schedule: [+,+,+,+,+,+,-,-]
  sign_flip_horizon: 15
  cumulative_gain: 0.82
  positive_gain: 0.78
  negative_compensation_gain: 0.12
```

### 11.3 稳定性与不确定性字段

```yaml
statistics:
  mean_gain: 0.41
  std_gain: 0.08
  support_probability: 0.86
  sign_consistency: 0.91
  fd_sign_match: 0.82
  fd_magnitude_ratio: 0.74
  delay_std_steps: 1.3
  regime_coverage: 0.65
  local_validity_eps_min: 0.005
  local_validity_eps_max: 0.050
```

### 11.4 约束与风险字段

```yaml
constraints:
  max_safe_amplitude: 0.04
  preferred_amplitude_range: [0.01, 0.03]
  max_duration_steps: 12
  forbidden_regimes: [landing_transition, failsafe, unknown_mode]
  saturation_sensitive: true
  requires_mode_feedback: true
  requires_state_feedback: true

failure_guards:
  reject_if_sign_mismatch_count_ge: 2
  reject_if_delay_error_gt_steps: 5
  reject_if_actuator_margin_lt: 0.10
  reject_if_mode_changed_recent_steps: 10
```

## 12. AttackPrimitiveLibrary 设计

Mechanism 是响应关系；Attack Primitive 是可执行时序扰动模板。

### 12.1 Primitive 数据结构

```yaml
primitive_id: P_M_ALT_CMD_TO_ALT_ERR_HOVER_001_PULSE
mechanism_id: M_ALT_CMD_TO_ALT_ERR_HOVER_001
input_channel: altitude_setpoint
waveform_family: smooth_pulse
start_offset_steps: -8
duration_steps: 6
amplitude_variable: a
sign_schedule: [+,+,+,+,+,0]
expected_peak_horizon: 8
expected_output: altitude_error
expected_target_gain_lcb: 0.31
budget_cost_estimate: 0.18
plausibility_cost_estimate: 0.09
```

### 12.2 支持的 waveform family

#### A. Constant block

```text
delta_u[t:t+d] = a
```

适合慢响应或积分型响应。

#### B. Smooth pulse

```text
delta_u[t:t+d] = a * hann_window(d)
```

适合降低 rate cost 和 frequency detectability。

#### C. Ramp

```text
delta_u[t+i] = a * i / d
```

适合高层 setpoint 攻击，保持 command plausibility。

#### D. Delayed pulse train

```text
several short pulses aligned with response peak
```

适合有明确 delay profile 的机制。

#### E. Sign-scheduled block

```text
delta_u follows sign_schedule to avoid future compensation
```

适合 response sign 会翻转的机制。

### 12.3 Primitive 生成规则

对每个 mechanism，生成候选 primitive：

```text
1. 根据 peak_horizon 计算 lead_time。
2. 根据 response_duration_steps 生成 duration candidates。
3. 根据 sign_schedule 生成扰动符号。
4. 根据 local_validity_eps_range 生成 amplitude bounds。
5. 根据 preferred waveform family 生成 waveform candidates。
6. 计算每个 primitive 的 robust target gain、budget cost、plausibility cost。
```

推荐默认：

```yaml
lead_time_candidates:
  - peak_horizon - 2
  - peak_horizon
  - peak_horizon + 2

duration_candidates:
  - min(3, response_duration)
  - response_duration
  - min(2 * response_duration, max_duration)

waveforms:
  - smooth_pulse
  - constant_block
  - ramp
```

## 13. Objective-aware attack utility

Stage2 不能只按 mechanism 的导数强度排序。必须根据当前攻击目标计算 utility。

### 13.1 放大型目标

例如增大 tracking error：

\[
Utility(p) = \frac{LCB[\sum_h w_h ||R_p[h]||_Q]}{Cost(p) + \epsilon}
\]

其中 `R_p[h]` 是 primitive p 的预测响应。

### 13.2 定向 steering 目标

例如把 altitude error 推向正方向：

\[
Utility(p) = \frac{LCB[\sum_h w_h c^T R_p[h]]}{Cost(p) + \epsilon}
\]

如果 `c^T R_p[h]` 为负，则该 primitive 对该目标不可用。

### 13.3 安全余量目标

例如降低 safety margin：

\[
Utility(p) = \frac{LCB[\sum_h w_h \max(0, -\Delta margin_p[h])]}{Cost(p) + \epsilon}
\]

### 13.4 恢复退化目标

例如增加 recovery time：

```text
Utility = delayed_error_gain + overshoot_gain - early_compensation_penalty
```

### 13.5 Utility 中的惩罚项

```text
Cost(p) =
  alpha_E * energy_cost
+ alpha_R * rate_cost
+ alpha_P * plausibility_cost
+ alpha_U * uncertainty_cost
+ alpha_C * compensation_penalty
```

补偿惩罚用于避免短期攻击后被控制器快速反向恢复：

\[
compensation\_penalty = \sum_{h > h_{target}} \max(0, -c^T R_p[h])
\]

## 14. 不确定性集合编译

Stage2 必须把 Stage1 的 ensemble 编译成 planner 可用的不确定性集合。

### 14.1 Ensemble form

```text
U_m = {J_m^1, J_m^2, ..., J_m^K}
```

每个 `J_m^k` 是同一 mechanism 在 bootstrap、scenario、seed 或 local regime 下的一个候选响应。

### 14.2 LCB gain

\[
LCB(p) = mean(G_p) - \beta \cdot std(G_p)
\]

推荐：

```yaml
beta:
  lite: 0.5
  robust: 1.0
  conservative: 1.5
```

### 14.3 Worst-case gain

\[
Worst(p) = \min_k G_p^k
\]

适合高安全约束场景，但可能过于保守。

### 14.4 Quantile gain

\[
Q_{0.2}(p) = 20th percentile of G_p
\]

推荐作为默认 robust score，比 worst-case 稳定。

## 15. Mechanism compatibility graph

攻击 planner 需要知道哪些 primitive 可以共同使用、哪些会冲突。

### 15.1 冲突类型

```text
same_channel_rate_conflict:
  两个 primitive 使用同一 channel，且时间重叠导致 rate 超限。

opposite_target_conflict:
  两个 primitive 对同一 target output 方向相反。

compensation_conflict:
  一个 primitive 的 delayed response 抵消另一个 primitive 的目标响应。

budget_conflict:
  两个 primitive 合用后超过 L2 或 active block 限制。

regime_conflict:
  两个 primitive 适用 regime 不一致。
```

### 15.2 协同类型

```text
same_target_synergy:
  两个 primitive 对同一目标方向同号增强。

multi_axis_synergy:
  一个 primitive 增加 lateral error，另一个降低 recovery speed。

timing_synergy:
  两个 primitive 的 peak horizon 错开，形成持续风险窗口。
```

### 15.3 图结构

```json
{
  "nodes": ["primitive_id"],
  "edges": [
    {
      "p1": "P_001",
      "p2": "P_002",
      "type": "same_target_synergy",
      "weight": 0.15
    },
    {
      "p1": "P_003",
      "p2": "P_004",
      "type": "same_channel_rate_conflict",
      "weight": -1.0
    }
  ]
}
```

## 16. Stage2 输出产物

```text
artifacts/stage2_mechanism_compiler/
  configs/
    mechanism_gate.yaml
    primitive_generation.yaml
    objective_utility.yaml
    uncertainty_compile.yaml
  tables/
    mechanism_ledger.csv
    attack_primitives.csv
    primitive_utility_by_objective.csv
    mechanism_validity_by_regime.csv
    compatibility_edges.csv
  models/
    uncertainty_sets.pkl
    regime_mechanism_index.json
    primitive_library.json
    compatibility_graph.json
  reports/
    STAGE2_MECHANISM_LEDGER.md
    ATTACK_PRIMITIVE_LIBRARY.md
    OBJECTIVE_UTILITY_REPORT.md
    REGIME_MECHANISM_INDEX.md
    UNCERTAINTY_SET_REPORT.md
  schemas/
    mechanism_ledger.schema.json
    attack_primitive.schema.json
```

## 17. Stage2 进入 Stage3 的条件

至少满足：

```text
1. 每个主 objective 至少有 3 个可执行 primitive。
2. 每个主 threat model 至少有 1 个非空 stable support。
3. 每个 primitive 都有 amplitude bound、duration、lead_time、expected response。
4. 每个 primitive 都能计算 objective-aware utility。
5. 每个 primitive 都能计算 LCB 或 quantile robust gain。
6. compatibility graph 可用于规划器避免明显冲突。
```

---

# Stage3: USDTA 攻击规划器设计与实现

## 18. Stage3 目标

Stage3 实现真正的攻击算法。它读取 Stage2 的 primitive library 和 Stage1 的导数 ensemble，在每个控制窗口内生成扰动计划。

Stage3 的核心不是“选最大机制”，而是：

```text
当前状态下，针对当前目标，在预算约束内选择一组兼容的时序攻击 primitive，
并求解它们的幅度和时间组合，使 robust target gain 最大化。
```

## 19. Planner 输入输出

### 19.1 输入

```yaml
planner_input:
  timestamp: t
  observation: o_t
  threat_model: T1_high_level_setpoint
  objective:
    family: tracking_error_amplification
    target_outputs: [altitude_error, vertical_velocity_error]
    horizon_weights: [0.1, 0.2, 0.5, 1.0, 1.0]
    direction: null
  budget: budget.yaml
  primitive_library: primitive_library.json
  regime_index: regime_mechanism_index.json
  uncertainty_sets: uncertainty_sets.pkl
  compatibility_graph: compatibility_graph.json
  online_state: planner_state.json
```

### 19.2 输出

```yaml
planner_output:
  selected_primitives:
    - primitive_id: P_M_ALT_001_PULSE
      channel: altitude_setpoint
      start_step: 0
      duration_steps: 6
      amplitude: 0.025
      waveform: smooth_pulse
      expected_peak_horizon: 8
  delta_u_plan:
    shape: T x num_writable_channels
  expected_response:
    target_gain_lcb: 0.31
    target_gain_mean: 0.42
    expected_peak_error_step: 8
  constraints:
    eps_inf_used: 0.025
    l2_used: 0.17
    active_channels: 1
    tv_used: 0.08
    plausibility_score: 0.12
  fallback:
    monitor_outputs: [altitude_error]
    abort_if_mode_change: true
    downweight_if_sign_mismatch: true
```

## 20. Planner 主流程

```text
1. Regime inference
2. Candidate primitive retrieval
3. Objective-aware utility recomputation
4. Robust sparse support allocation
5. Constrained amplitude optimization
6. Plan validation and safety guards
7. Apply first block or first step
8. Observe response
9. Online confidence update
10. Re-plan
```

## 21. Step 1: Regime inference

根据当前 observation 选择 regime：

```python
regime_probs = regime_classifier(o_t)
active_regimes = top_regimes(regime_probs, threshold=0.2)
```

如果 regime 不确定：

```text
1. 使用多个 regime 的 primitive union。
2. 对每个 primitive 的 utility 乘以 regime probability。
3. 提高 uncertainty penalty。
4. 禁用 near-boundary primitives。
```

Regime-aware gain：

\[
G(p|o_t) = \sum_r P(r|o_t) G(p|r)
\]

## 22. Step 2: Candidate primitive retrieval

筛选条件：

```text
primitive.threat_models contains current threat_model
primitive.valid_regime compatible with active_regimes
primitive.input_channel in writable_channels
primitive.output_channel in objective.target_outputs or objective.related_outputs
primitive.local_validity_range covers budget amplitude
primitive.failure_guards not triggered
```

伪代码：

```python
candidates = []
for p in primitive_library:
    if not threat_model_allows(p):
        continue
    if not regime_compatible(p, active_regimes):
        continue
    if not objective_compatible(p, objective):
        continue
    if guard_triggered(p, observation, online_state):
        continue
    candidates.append(p)
```

## 23. Step 3: Objective-aware utility recomputation

Stage2 的 utility 是离线预估。Stage3 必须根据当前目标和状态重新计算。

### 23.1 当前目标权重

例如 tracking error 放大：

```python
error_now = compute_tracking_error(o_t)
Q = build_error_weight(error_now, objective)
```

如果目标是放大当前已有误差：

\[
c_t = \frac{e_t}{||e_t|| + \epsilon}
\]

则 directional gain：

\[
G_p = \sum_h w_h c_t^T R_p[h]
\]

### 23.2 Robust gain

对 ensemble 响应计算：

```python
gains = [objective_gain(response_k, objective, o_t) for response_k in p.responses]
mean_gain = mean(gains)
std_gain = std(gains)
lcb_gain = mean_gain - beta * std_gain
q_gain = quantile(gains, q=0.2)
```

默认使用：

```text
robust_gain = min(lcb_gain, q_gain) if conservative
robust_gain = q_gain if default
robust_gain = lcb_gain if fast
```

### 23.3 当前 utility

\[
U_t(p) =
\frac{RobustGain_t(p) + SynergyBonus_t(p)}
{EnergyCost(p) + RateCost(p) + PlausibilityCost(p) + CompensationPenalty(p) + \epsilon}
\]

## 24. Step 4: Robust sparse support allocation

推荐使用 greedy marginal allocation，而不是一开始求解全维非凸问题。

### 24.1 规划对象

规划器选择的是 primitive block：

```text
block = (primitive_id, start_step, duration, waveform, amplitude_variable)
```

支持集合：

```text
S = {block_1, ..., block_k}
```

### 24.2 Greedy allocation

伪代码：

```python
S = []
remaining_budget = B
while len(S) < max_active_blocks:
    best_block = None
    best_gain = -inf

    for p in candidates:
        if conflicts_with_existing(p, S, compatibility_graph):
            continue
        if violates_budget_lower_bound(p, remaining_budget):
            continue

        marginal_gain = robust_marginal_gain(p, S, objective, uncertainty_set)
        marginal_cost = estimated_cost(p)
        utility = marginal_gain / (marginal_cost + eps)

        if utility > best_gain:
            best_gain = utility
            best_block = p

    if best_block is None or best_gain < min_utility_threshold:
        break

    S.append(best_block)
    remaining_budget = update_budget(remaining_budget, best_block)
```

### 24.3 Marginal gain

不能简单相加，因为不同 primitive 可能抵消或协同。

\[
MG(p|S) = RobustGain(S \cup \{p\}) - RobustGain(S)
\]

其中：

```text
RobustGain(S) = quantile_k(Phi(sum responses of primitives in S))
```

### 24.4 多样性约束

为避免所有 budget 都分给一个高不确定通道：

```text
max_blocks_per_channel <= 2
max_total_duration_per_channel <= threshold
min_time_gap_if_same_channel >= gap
optional: encourage multi-output coverage
```

## 25. Step 5: Constrained amplitude optimization

选定 support 后，再优化幅度。设选中 `K` 个 primitive，幅度向量为：

\[
a = [a_1, ..., a_K]
\]

扰动计划：

\[
\delta u = W a
\]

其中 `W` 是 waveform/design matrix。

### 25.1 线性目标近似

若 objective 是定向线性目标：

\[
\max_a \quad g^T a - \lambda a^T R a
\]

subject to:

```text
A_inf a <= eps_inf
||W a||_2 <= eps_2
TV(Wa) <= eps_rate
plausibility(Wa) <= eps_plausibility
a_min <= a <= a_max
```

### 25.2 放大目标近似

若 objective 是误差范数放大：

\[
\max_a \quad ||e_0 + G a||_Q^2 - ||e_0||_Q^2 - \lambda ||a||_2^2
\]

可用 projected gradient ascent 或 coordinate ascent。

### 25.3 推荐默认解法

默认实现顺序：

```text
1. closed-form sign amplitude initialization
2. coordinate ascent with projection
3. projected gradient refinement
4. final budget projection
```

伪代码：

```python
a = initialize_amplitudes(S, objective)
for iter in range(max_iter):
    grad = compute_robust_objective_gradient(a, S, objective)
    a = a + step_size * grad
    a = project_box(a, a_min, a_max)
    a = project_budget(W @ a, budget)
    if objective_improvement < tol:
        break
```

### 25.4 Projection 顺序

推荐：

```text
1. box constraint per amplitude
2. per-channel L_inf
3. total L2 energy
4. total variation / rate
5. spectral constraint
6. plausibility envelope
```

如果 projection 导致目标收益为负，则放弃该 plan。

## 26. Step 6: Plan validation and guards

执行前必须检查：

```text
1. planned channels all writable
2. no forbidden regime active
3. expected robust_gain > min_gain
4. predicted compensation penalty < max_compensation
5. budget constraints satisfied
6. plausibility score satisfied
7. mode has been stable for min_mode_stable_steps
8. no hard safety abort flag
```

Plan 状态：

```text
ACCEPT
REJECT_LOW_GAIN
REJECT_BUDGET
REJECT_UNCERTAINTY
REJECT_REGIME
REJECT_GUARD
REJECT_PLAUSIBILITY
```

如果 reject，planner 应 fallback：

```text
fallback 1: reduce amplitude
fallback 2: shorten duration
fallback 3: switch to lower-risk primitive
fallback 4: no attack for this window
```

## 27. Step 7: Receding-horizon execution

不建议一次性执行完整长计划。默认执行：

```text
apply first step, or first short block of K_apply steps
observe response
re-plan
```

推荐配置：

```yaml
planning_horizon_T: 20
apply_horizon_K: 2
replan_interval_steps: 2
response_monitor_horizon: 10
```

如果系统更新频率太低，可以：

```text
planning_horizon_T: 10
apply_horizon_K: 1
```

## 28. Step 8: Online response monitor

执行后比较预测响应和实际响应。

### 28.1 观测响应

```text
observed_delta_y[h] = y_attack[t+h] - y_baseline_estimate[t+h]
```

如果没有并行 baseline，可使用短期局部预测：

```text
baseline_estimate = no_attack_predictor(o_t)
```

### 28.2 观测指标

```text
observed_gain
predicted_gain
response_ratio = observed_gain / (predicted_gain + eps)
sign_match
delay_error = observed_peak_horizon - predicted_peak_horizon
residual_norm
compensation_observed
```

### 28.3 置信度更新

对每个 mechanism 维护：

```text
confidence_m
gain_scale_m
delay_shift_m
sign_reliability_m
recent_failure_count_m
```

更新：

\[
confidence_{m,t+1} = \alpha confidence_{m,t} + (1-\alpha) match\_score_{m,t}
\]

其中：

```text
match_score =
  w1 * sign_match
+ w2 * clipped(response_ratio)
+ w3 * exp(-abs(delay_error) / tau_delay)
- w4 * compensation_observed
```

默认：

```yaml
alpha: 0.8
w_sign: 0.35
w_gain: 0.30
w_delay: 0.25
w_compensation: 0.10
```

### 28.4 Delay correction

如果连续观测到响应晚到：

```text
delay_shift_m += 1
```

如果响应早到：

```text
delay_shift_m -= 1
```

Stage3 下一轮生成 primitive 时调整：

```text
adjusted_start_offset = original_start_offset - delay_shift_m
```

### 28.5 Sign mismatch 处理

如果 `sign_mismatch_count >= threshold`：

```text
1. 下调该 mechanism confidence。
2. 从本次 episode 的 candidate pool 中移除。
3. 标记需要 Stage2 回看该 regime 的 sign stability。
```

## 29. Planner 版本定义

### 29.1 USDTA-core-static

```text
regime-aware: yes
primitive-based: yes
robust gain: no, use mean gain
online adaptation: no
amplitude optimization: simple coordinate
```

用途：验证 primitive-based attack 是否能工作。

### 29.2 USDTA-core-robust

```text
regime-aware: yes
primitive-based: yes
robust gain: quantile or LCB
online adaptation: no
amplitude optimization: coordinate + projection
```

用途：验证不确定性建模是否提升稳定性。

### 29.3 USDTA-core-rh

```text
regime-aware: yes
primitive-based: yes
robust gain: quantile or LCB
online adaptation: confidence + delay correction
amplitude optimization: coordinate + projection
```

用途：验证滚动规划和反馈修正。

### 29.4 USDTA-core-full

```text
regime-aware soft mixture
compatibility graph
robust sparse allocation
projected amplitude optimization
online gain/delay/sign correction
plausibility-aware constraints
```

用途：作为最终攻击算法实现。

## 30. Stage3 代码结构建议

```text
src/usdta/
  __init__.py
  data_contracts.py
  threat_model.py
  objectives.py
  regime.py
  tensors.py
  mechanisms.py
  primitives.py
  uncertainty.py
  compatibility.py
  planner/
    candidate_selector.py
    utility.py
    greedy_allocator.py
    amplitude_optimizer.py
    constraints.py
    validator.py
    receding_horizon.py
    online_adapter.py
  runtime/
    attack_session.py
    observation_buffer.py
    response_monitor.py
    safety_guards.py
  baselines/
    top_coefficient.py
    gradient_sign.py
    sparse_random.py
    bounded_noise.py
    pulse_chirp.py
    oracle_j.py
  evaluation/
    replay_eval.py
    sim_eval.py
    metrics.py
    diagnostics.py
```

## 31. Stage3 单元测试

### 31.1 Contract tests

```text
test_threat_model_filters_unwritable_channels
test_primitive_schema_loads
test_budget_projection_never_exceeds_limits
test_planner_output_shape
```

### 31.2 Algorithm tests

```text
test_greedy_allocator_increases_robust_gain
test_amplitude_optimizer_respects_linf_l2_tv
test_conflict_graph_blocks_conflicting_primitives
test_regime_mixture_weights_sum_to_one
test_delay_correction_shifts_start_offset
```

### 31.3 Synthetic recovery tests

构造已知线性系统：

```text
y[t+h] = J_true[h] delta_u[t]
```

验证：

```text
estimated plan chooses correct channel
estimated plan chooses correct lead time
estimated plan chooses correct sign
observed response matches predicted response
online adapter corrects injected delay mismatch
```

## 32. Stage3 输出产物

```text
artifacts/stage3_usdta_planner/
  configs/
    planner_core_static.yaml
    planner_core_robust.yaml
    planner_core_rh.yaml
    planner_core_full.yaml
    objective_configs.yaml
    budget_configs.yaml
  specs/
    planner_input.schema.json
    planner_output.schema.json
    online_state.schema.json
  reports/
    STAGE3_PLANNER_SPEC.md
    OBJECTIVE_DEFINITIONS.md
    CONSTRAINTS_AND_PROJECTIONS.md
    ONLINE_ADAPTER_SPEC.md
    IMPLEMENTATION_TEST_REPORT.md
  logs/
    unit_test_results.json
    synthetic_recovery_results.json
```

## 33. Stage3 进入 Stage4 的条件

至少满足：

```text
1. Planner 可以在离线 replay 中输出合法 plan。
2. 所有 plan 都满足 threat model 和 budget constraints。
3. Synthetic known-J 测试中能恢复正确 channel、timing 和 sign。
4. Online adapter 能修正人为注入的 gain scale、delay shift、sign mismatch。
5. 至少一个主 objective 的 planner 输出 expected robust gain > 0。
6. Baseline 实现与 USDTA 使用同一 budget interface。
```

---

# Stage4: 闭环攻击执行、诊断与版本固化

## 34. Stage4 目标

Stage4 的目标是让攻击算法在闭环环境中运行，记录预测响应与实际响应之间的差异，诊断失败原因，并把结果回写到模型、机制和 planner 版本中。

Stage4 不是只输出成功率，而是要形成完整闭环：

```text
planner_prediction
  -> attack_execution
  -> observed_response
  -> response_diagnostics
  -> mechanism confidence update
  -> planner version decision
```

## 35. Stage4 执行模式

### 35.1 Offline replay mode

使用历史日志，不实际改变系统，用于测试 planner 的合法性和预期收益。

```text
input: logged o_t, J_bundle, primitives
output: planned delta_u, expected_gain, constraint usage
```

用途：

```text
1. 检查 planner 是否频繁输出非法扰动。
2. 检查不同 objective 下选择的 primitive 是否合理。
3. 检查 budget 使用率和 plan diversity。
```

### 35.2 Counterfactual simulation mode

在仿真中执行攻击扰动，获取闭环响应。

```text
base rollout
attack rollout
paired seeds
same mission
same disturbance
```

用途：

```text
1. 获取真实 closed-loop response。
2. 更新 gain/delay/sign confidence。
3. 评估 receding-horizon 是否改善失配。
```

### 35.3 Isolated testbench mode

仅在隔离测试台或安全飞行围栏内执行，且必须启用安全 guard。

```text
hard abort conditions
max envelope boundary
manual override
low-amplitude first pass
```

该模式不作为默认执行模式。

## 36. Stage4 攻击 session 协议

每个 attack session 包含：

```yaml
session_id: S_YYYYMMDD_001
stack: px4_or_ardupilot
scenario: trajectory_tracking
regime_sequence: [hover, tracking, turn]
threat_model: T1_high_level_setpoint
objective: tracking_error_amplification
planner_variant: USDTA-core-rh
budget_profile: low_medium
seed: 123
base_rollout_id: R_base_001
attack_rollout_id: R_attack_001
```

每个 session 运行流程：

```text
1. Initialize environment and seed.
2. Run warmup without attack.
3. At eligible window, call planner.
4. Validate plan.
5. Apply first block.
6. Monitor response.
7. Re-plan until attack window ends.
8. Run cooldown.
9. Compute paired metrics.
10. Save trace and diagnostics.
```

## 37. 攻击窗口选择

攻击窗口不应随意选择。推荐三种窗口：

### 37.1 Regime-triggered window

当系统进入某个 regime 后触发：

```text
enter trajectory_tracking and stable for 20 steps
```

### 37.2 Error-triggered window

当已有误差处于某个范围时触发：

```text
tracking_error between low and medium
```

过低误差可能没有放大空间，过高误差可能触发保护或饱和。

### 37.3 Mission-phase window

在固定任务阶段触发：

```text
after takeoff
before waypoint transition
during curved path
before recovery segment
```

每个窗口必须记录：

```text
window_start
window_end
pre_attack_regime
pre_attack_error
actuator_margin
mode_stability
eligible_mechanisms
```

## 38. Stage4 指标

### 38.1 算法收益指标

```text
realized_target_gain
predicted_target_gain
robust_gain_lcb
prediction_to_realization_ratio
budget_efficiency = realized_gain / used_budget
channel_efficiency = realized_gain / active_channel_count
time_to_peak_error
attack_effect_duration
```

### 38.2 闭环响应指标

```text
peak_tracking_error
integrated_tracking_error
safety_margin_reduction
actuator_stress_delta
recovery_time_delta
overshoot_delta
settling_delay_delta
```

### 38.3 规划质量指标

```text
plan_acceptance_rate
plan_rejection_reason_counts
constraint_usage_ratio
primitive_diversity
regime_match_rate
online_replan_count
confidence_update_magnitude
delay_correction_count
```

### 38.4 响应匹配指标

```text
sign_match_rate
gain_ratio
peak_horizon_error
response_shape_cosine
compensation_observed
residual_norm
```

### 38.5 成本与可执行性指标

```text
eps_inf_used
l2_used
total_variation_used
spectral_cost
plausibility_cost
command_percentile_score
active_channels
active_blocks
```

## 39. 内部对照算法

Stage4 应保留若干内部对照，用于定位 USDTA 的算法问题。

### 39.1 top-coefficient

```text
选择 |J| 最大的可控 edge，按固定 sign 施加扰动。
```

作用：判断 USDTA 的时序 primitive 和 utility allocation 是否确实有价值。

### 39.2 gradient-sign

```text
delta = eps * sign(J^T target_gradient)
```

作用：判断 USDTA 是否比单步梯度方向更好。

### 39.3 sparse-random

```text
随机选择相同数量 channel 和 block，在相同 budget 下施加扰动。
```

作用：判断 support selection 是否有效。

### 39.4 pulse/chirp

```text
使用简单 pulse 或 chirp waveform，预算相同。
```

作用：判断 USDTA 的 delay-aware scheduling 是否优于通用频率覆盖。

### 39.5 oracle-J

```text
使用测试 regime 的真实/后验 J 进行规划。
```

作用：区分模型迁移失败和 planner 本身失败。

### 39.6 black-box shooting

```text
在仿真中随机采样 N 个扰动计划，选择观察到收益最高者。
```

作用：判断 USDTA 是否接近同预算搜索上界。

## 40. Stage4 消融版本

消融不是展示用，而是诊断算法模块。

```text
A0: static coefficient only
A1: + primitive timing
A2: + objective-aware utility
A3: + robust LCB gain
A4: + compatibility graph
A5: + constrained amplitude optimization
A6: + regime-aware selection
A7: + online confidence update
A8: + delay correction
A9: + plausibility constraint
```

每个消融输出：

```text
realized_gain
prediction_ratio
budget_efficiency
failure_reason_distribution
```

## 41. Failure taxonomy

### F1: no eligible primitive

当前 regime、objective 和 threat model 下没有可执行原语。

处理：

```text
Stage2 增加该 regime 的机制，或降低 objective 覆盖要求。
```

### F2: low predicted gain

有 primitive，但 robust gain 太低。

处理：

```text
检查 Stage1 导数是否弱；考虑调整目标输出或攻击窗口。
```

### F3: sign mismatch

实际响应方向与预测相反。

处理：

```text
立即下调 mechanism confidence；必要时禁用该 regime 下的 mechanism。
```

### F4: delay mismatch

实际 peak horizon 与预测差距过大。

处理：

```text
更新 delay_shift；重新生成 start offset。
```

### F5: gain overestimated

预测收益明显大于实际收益。

处理：

```text
提高 uncertainty penalty；更新 gain_scale。
```

### F6: controller compensation

短期攻击成功，但随后控制器快速恢复或反向补偿。

处理：

```text
提高 compensation_penalty；缩短或重排 sign schedule。
```

### F7: budget projection collapse

优化出的计划在 projection 后收益消失。

处理：

```text
调整 primitive amplitude range，或改用更低 rate-cost waveform。
```

### F8: regime misclassification

planner 使用了错误 regime 的机制。

处理：

```text
更新 regime classifier；使用 soft mixture 而非 hard label。
```

### F9: baseline coverage advantage

通用 pulse/chirp 或 random 由于覆盖更多频率/通道而更强。

处理：

```text
增加 timing diversity，允许多 primitive staggered schedule。
```

### F10: safety guard rejection

计划被安全 guard 拒绝。

处理：

```text
降低 amplitude；缩短 duration；重新选择低风险 primitive。
```

## 42. Stage4 数据记录格式

### 42.1 Attack trace

```json
{
  "session_id": "S_001",
  "step": 120,
  "observation_summary": {
    "regime": "trajectory_tracking",
    "tracking_error_norm": 0.12,
    "actuator_margin": 0.45
  },
  "planner_variant": "USDTA-core-rh",
  "selected_primitives": ["P_001", "P_017"],
  "delta_u": [[0.0, 0.02, 0.0], [0.0, 0.018, 0.0]],
  "expected_gain": 0.31,
  "expected_peak_horizon": 8,
  "budget_used": {
    "l2": 0.14,
    "linf": 0.02,
    "tv": 0.05
  },
  "guards": {
    "mode_stable": true,
    "plausibility_ok": true
  }
}
```

### 42.2 Response trace

```json
{
  "session_id": "S_001",
  "primitive_id": "P_001",
  "observed_gain": 0.24,
  "predicted_gain": 0.31,
  "gain_ratio": 0.77,
  "sign_match": true,
  "predicted_peak_horizon": 8,
  "observed_peak_horizon": 10,
  "delay_error": 2,
  "response_shape_cosine": 0.68,
  "compensation_observed": 0.12,
  "confidence_before": 0.84,
  "confidence_after": 0.79
}
```

### 42.3 Episode summary

```json
{
  "session_id": "S_001",
  "method": "USDTA-core-rh",
  "objective": "tracking_error_amplification",
  "realized_target_gain": 0.42,
  "budget_efficiency": 2.8,
  "prediction_to_realization_ratio": 0.74,
  "plan_acceptance_rate": 0.92,
  "failure_reasons": [],
  "online_updates": {
    "confidence_updates": 4,
    "delay_corrections": 2,
    "mechanisms_disabled": 0
  }
}
```

## 43. Stage4 固化准则

一个 planner variant 可以进入稳定版本，需满足：

```text
1. 合法 plan 输出率 >= 95%。
2. 预算违规率 = 0。
3. 在 synthetic known-J 环境中 channel/timing/sign 恢复率 >= 90%。
4. 在 closed-loop simulation 中 realized_gain 的中位数为正。
5. prediction_to_realization_ratio 在主要 regime 中不长期低于 0.3。
6. sign mismatch rate 不超过预设阈值。
7. failure taxonomy 中没有单一系统性失败超过 50%。
8. online adapter 不引入震荡式反复切换。
```

## 44. Stage4 输出产物

```text
artifacts/stage4_closed_loop_attack/
  configs/
    session_grid.yaml
    attack_windows.yaml
    planner_variants.yaml
    baseline_variants.yaml
  traces/
    attack_traces.jsonl
    response_traces.jsonl
    online_state_traces.jsonl
  tables/
    episode_summary.csv
    prediction_realization.csv
    failure_taxonomy.csv
    primitive_performance.csv
    regime_performance.csv
    ablation_performance.csv
  reports/
    STAGE4_CLOSED_LOOP_SUMMARY.md
    ATTACK_SESSION_REPORT.md
    PREDICTION_REALIZATION_REPORT.md
    FAILURE_DIAGNOSIS_REPORT.md
    PLANNER_VERSION_DECISION.md
  models/
    updated_mechanism_confidence.json
    updated_delay_corrections.json
    disabled_mechanisms.json
```

---

# 45. Stage1–4 端到端执行路线

## 45.1 第一轮：最小闭环

目标：确认完整链路可跑通。

```text
Stage1:
  1 stack
  2 regimes: hover, trajectory_tracking
  2 objectives: tracking_error, altitude_error
  command-only + command-history
  H <= 20, L <= 5

Stage2:
  生成 5-15 个 mechanism
  每个 mechanism 生成 2-3 个 primitive

Stage3:
  实现 USDTA-core-static
  实现 top-coefficient 和 gradient-sign 内部对照

Stage4:
  offline replay + counterfactual simulation
  10-20 sessions
```

通过条件：

```text
planner 合法输出稳定
至少一个 objective 有正 realized gain
prediction_to_realization_ratio 不为随机
```

## 45.2 第二轮：鲁棒规划

目标：加入不确定性和预算分配。

```text
Stage1:
  bootstrap J ensemble
  regime-specific J
  FD checks for top mechanisms

Stage2:
  LCB / quantile gain
  compatibility graph

Stage3:
  USDTA-core-robust
  greedy sparse allocation
  amplitude optimization

Stage4:
  paired simulation sessions
  ablations A0-A5
```

通过条件：

```text
robust variant 的 failure variance 低于 static variant
预算效率高于 simple coefficient baseline
```

## 45.3 第三轮：滚动闭环

目标：解决闭环失配。

```text
Stage1:
  更新 local validity ranges
  增加 transition / turn / disturbance regime

Stage2:
  增加 delay_shift metadata
  增加 failure guards

Stage3:
  USDTA-core-rh
  online confidence update
  delay correction

Stage4:
  full attack sessions with re-planning
  response monitor
  online update logs
```

通过条件：

```text
online adapter 能减少 delay mismatch 或 sign mismatch 的持续时间
rh variant 相比 robust static 在主要 regime 中 realized gain 更稳定
```

## 45.4 第四轮：完整算法固化

目标：形成可复现实验包。

```text
Stage1:
  多 regime、多 scenario、必要时多 stack

Stage2:
  完整 mechanism ledger
  primitive library
  compatibility graph

Stage3:
  USDTA-core-full
  baseline and ablation implementations

Stage4:
  session grid
  failure taxonomy
  version decision
```

通过条件：

```text
核心 planner 接口稳定
artifact 可复跑
主要 failure 已有处理规则
最终版本参数固定
```

---

# 46. 配置文件模板

## 46.1 derivative_estimator.yaml

```yaml
estimator:
  horizons: [1, 2, 3, 5, 8, 10, 15, 20]
  lags: [0, 1, 2, 3, 5]
  models:
    - ridge_temporal
    - elastic_net_temporal
    - group_sparse
    - smooth_temporal
    - regime_local
  regularization:
    ridge_alpha: [0.1, 1.0, 10.0]
    l1_ratio: [0.2, 0.5, 0.8]
    temporal_smooth_lambda: [0.0, 0.1, 1.0]
  bootstrap_members: 32
  normalization: train_only_zscore
  split: rollout_holdout
```

## 46.2 mechanism_gate.yaml

```yaml
gates:
  min_actionability: A2
  min_support_probability: 0.60
  min_sign_consistency: 0.70
  min_fd_sign_match: 0.60
  max_delay_std_steps: 5
  max_uncertainty_ratio: 2.0
  require_valid_regime: true
  allow_near_saturation: false
```

## 46.3 primitive_generation.yaml

```yaml
primitive_generation:
  waveform_families:
    - smooth_pulse
    - constant_block
    - ramp
    - sign_scheduled_block
  lead_time_offsets: [-2, 0, 2]
  duration_multipliers: [0.5, 1.0, 1.5]
  min_duration_steps: 2
  max_duration_steps: 20
  amplitude_grid: [0.25, 0.5, 0.75, 1.0]
  use_local_validity_bounds: true
```

## 46.4 planner_core_full.yaml

```yaml
planner:
  variant: USDTA-core-full
  planning_horizon_T: 20
  apply_horizon_K: 2
  replan_interval_steps: 2
  robust_gain_mode: quantile
  robust_quantile: 0.20
  lcb_beta: 1.0
  greedy:
    max_active_blocks: 3
    max_blocks_per_channel: 2
    min_utility_threshold: 0.01
  optimizer:
    method: coordinate_then_projected_gradient
    max_iter: 50
    step_size: 0.05
    tolerance: 1.0e-4
  online_adapter:
    enabled: true
    alpha: 0.80
    sign_mismatch_disable_threshold: 2
    delay_shift_max_steps: 5
  guards:
    require_mode_stable_steps: 10
    min_actuator_margin: 0.10
    reject_unknown_regime: true
```

## 46.5 objective_tracking.yaml

```yaml
objective:
  name: tracking_error_amplification
  family: amplification
  target_outputs:
    - position_error_x
    - position_error_y
    - altitude_error
    - velocity_error_x
    - velocity_error_y
    - vertical_velocity_error
  horizon_weights:
    type: delayed_peak
    peak_horizon: 10
    width: 6
  norm: weighted_l2
  weights:
    position_error_x: 1.0
    position_error_y: 1.0
    altitude_error: 1.5
    velocity_error_x: 0.5
    velocity_error_y: 0.5
    vertical_velocity_error: 0.7
  compensation_penalty:
    enabled: true
    post_target_horizon_start: 15
    weight: 0.3
```

---

# 47. 关键实现细节

## 47.1 Normalization

所有导数模型训练必须使用 train-only normalization。Planner 执行时需要将扰动从 normalized 空间映射回 command 空间。

```text
delta_u_raw = delta_u_normalized * command_std_train
```

预算应在 raw command 空间检查，导数响应可在 normalized 空间计算。

## 47.2 Horizon alignment

每个 primitive 必须明确：

```text
planner time t
attack application time t + start_step
expected response time t + expected_peak_horizon
objective measurement window
```

禁止把 `expected_peak_horizon` 和 `start_offset` 混用。

## 47.3 Multi-output objective aggregation

多输出目标不要简单求和 raw units。应统一标准化：

```text
normalized_output = output / output_scale
```

`output_scale` 可以来自：

```text
train standard deviation
safety margin scale
mission tolerance
```

## 47.4 Rate constraint

若控制接口不允许突变，必须启用 TV 约束：

\[
TV(\delta u) = \sum_t ||\delta u_t - \delta u_{t-1}||_1
\]

Ramp 和 smooth pulse 默认优先于 step。

## 47.5 Plausibility model

建立简单 command plausibility 模型：

```text
nominal command distribution by regime
command rate distribution by regime
command spectrum distribution by regime
```

planner 惩罚：

```text
plausibility_cost = max(0, percentile_score(delta_u) - threshold)
```

## 47.6 Safety guard

所有闭环攻击执行必须经过 guard：

```text
if unauthorized_environment: reject
if unknown_mode: reject
if actuator_margin below threshold: reject or downgrade
if hard safety flag: abort
if output envelope too close to boundary: stop attack
```

Guard 不是 planner 的收益项，而是硬条件。

## 47.7 Oracle-J diagnostic

Oracle-J 不进入正式攻击算法，只用于诊断：

```text
if oracle-J succeeds but USDTA fails:
  model transfer / mechanism selection failure
if oracle-J also fails:
  objective or budget not feasible
```

## 47.8 Episode-level rollback

如果在线过程中出现连续 mismatch：

```text
sign mismatch >= threshold
or gain ratio < min_gain_ratio for N windows
or delay error > max_delay_error for N windows
```

则：

```text
1. stop current primitive
2. lower amplitude
3. switch primitive
4. or no attack
```

---

# 48. 最小可实现代码路径

推荐优先实现如下最小路径：

```text
1. Stage1: ridge_temporal + elastic_net_temporal
2. Stage2: mechanism_ledger + smooth_pulse primitive
3. Stage3: USDTA-core-static
4. Stage4: offline replay
5. Stage3: add greedy allocation
6. Stage4: counterfactual simulation
7. Stage3: add robust quantile gain
8. Stage3: add online confidence update
9. Stage4: full session traces
```

最小闭环不需要一开始实现所有 waveform、所有 objective、所有 threat model。优先选：

```text
Threat model: T1 or T2
Objective: tracking_error_amplification
Regime: hover + trajectory_tracking
Waveform: smooth_pulse + constant_block
Planner: greedy + coordinate amplitude
Online: confidence update + delay correction
```

---

# 49. 最终交付物清单

完整实验线应产生：

```text
docs/usdta_stage1_4_algorithm_plan.md

configs/usdta/
  threat_model.yaml
  risk_outputs.yaml
  regime_definition.yaml
  derivative_estimator.yaml
  mechanism_gate.yaml
  primitive_generation.yaml
  planner_core_full.yaml
  objective_tracking.yaml
  budget.yaml

src/usdta/
  tensors.py
  mechanisms.py
  primitives.py
  objectives.py
  uncertainty.py
  planner/
  runtime/
  baselines/
  evaluation/

artifacts/
  stage1_temporal_response_modeling/
  stage2_mechanism_compiler/
  stage3_usdta_planner/
  stage4_closed_loop_attack/
```

---

# 50. 执行检查清单

## Stage1 checklist

- [ ] 已定义 threat model 的 writable/readable channels。
- [ ] 已定义 risk output 和 objective family。
- [ ] 已完成时间对齐和 train-only normalization。
- [ ] 已训练 global、sparse、group、regime-specific 响应模型。
- [ ] 已导出 J ensemble。
- [ ] 已估计 support probability 和 sign consistency。
- [ ] 已对主候选通道做 finite-difference response check。
- [ ] 已给出 local validity epsilon range。
- [ ] 已导出 DerivativeTensorBundle。

## Stage2 checklist

- [ ] 已生成 MechanismLedger。
- [ ] 每个 mechanism 都有 valid_regime、actionability、horizon_profile。
- [ ] 每个 mechanism 都有 uncertainty 和 failure guard。
- [ ] 已生成 AttackPrimitiveLibrary。
- [ ] 每个 primitive 都有 lead_time、duration、waveform、amplitude bound。
- [ ] 已计算 objective-aware utility。
- [ ] 已生成 compatibility graph。
- [ ] 已生成 regime mechanism index。

## Stage3 checklist

- [ ] Planner 只能使用 writable channels。
- [ ] Planner 能根据 observation 选择 regime。
- [ ] Candidate selector 能过滤不合法 primitive。
- [ ] Utility 依赖当前 objective，而不是固定 coefficient。
- [ ] Greedy allocator 能计算 marginal robust gain。
- [ ] Amplitude optimizer 满足 L∞、L2、L0、TV、spectral 和 plausibility 约束。
- [ ] Plan validator 能拒绝低收益或高风险计划。
- [ ] Online adapter 能更新 confidence、gain scale、delay shift 和 sign reliability。
- [ ] Baselines 使用同一 budget interface。

## Stage4 checklist

- [ ] 已实现 offline replay。
- [ ] 已实现 paired counterfactual simulation。
- [ ] 每个 session 都保存 attack trace 和 response trace。
- [ ] 已计算 prediction-to-realization ratio。
- [ ] 已记录 failure taxonomy。
- [ ] 已输出 primitive-level performance。
- [ ] 已输出 regime-level performance。
- [ ] 已输出 planner variant decision。
- [ ] 已将在线更新回写到 mechanism confidence artifact。

---

# 51. 核心设计原则

1. **机制先于扰动。** 先确定当前 regime 下哪些可控输入对目标风险输出有稳定时序响应，再生成扰动。
2. **目标决定 support。** 机制强不代表适合当前目标；support selection 必须依赖 objective。
3. **时序决定效果。** 响应峰值、持续时间和符号翻转决定攻击开始时间、持续时间和 sign schedule。
4. **预算是规划的一部分。** L∞、L2、L0、rate、spectral、plausibility 不是评估后检查项，而是优化约束。
5. **不确定性进入决策。** 选择 robust lower-bound 或 quantile gain，而不是只看 mean gain。
6. **闭环需要反馈。** 实际 response 与预测 response 的差异必须更新 confidence、delay 和 sign。
7. **失败要可回写。** 每次失败都应能定位到 model、mechanism、primitive、planner 或 environment。
8. **所有接口机器可读。** Stage1–4 之间通过 schema、csv/json/npz/pkl artifact 连接，避免手工解释。

---

## 附录 A: USDTA-core-full 伪代码

```python
def usdta_core_full_step(o_t, objective, budget, online_state):
    # 1. Infer regime
    regime_probs = regime_classifier(o_t)
    active_regimes = select_active_regimes(regime_probs)

    # 2. Retrieve candidates
    candidates = []
    for p in primitive_library:
        if not threat_model_allows(p):
            continue
        if not regime_compatible(p, active_regimes):
            continue
        if not objective_compatible(p, objective):
            continue
        if guard_triggered(p, o_t, online_state):
            continue
        candidates.append(p)

    # 3. Recompute utility
    scored = []
    for p in candidates:
        responses = predict_ensemble_response(p, o_t, active_regimes, online_state)
        gains = [objective_gain(r, objective, o_t) for r in responses]
        robust_gain = quantile(gains, q=0.2)
        cost = estimate_cost(p, budget, o_t)
        comp = compensation_penalty(responses, objective)
        confidence = online_state.confidence.get(p.mechanism_id, 1.0)
        utility = confidence * robust_gain / (cost + comp + 1e-8)
        scored.append((p, utility, robust_gain, cost))

    # 4. Greedy allocation
    selected = []
    remaining_budget = budget.copy()
    while len(selected) < budget.max_active_blocks:
        best = None
        best_u = -float("inf")
        for p, _, _, _ in scored:
            if p in selected:
                continue
            if conflicts(p, selected, compatibility_graph):
                continue
            if violates_min_budget(p, remaining_budget):
                continue
            mg = robust_marginal_gain(p, selected, objective, o_t)
            c = estimate_cost(p, remaining_budget, o_t)
            u = mg / (c + 1e-8)
            if u > best_u:
                best = p
                best_u = u
        if best is None or best_u < planner_config.min_utility_threshold:
            break
        selected.append(best)
        remaining_budget = reserve_budget(best, remaining_budget)

    # 5. Optimize amplitudes
    if not selected:
        return no_attack_plan(reason="NO_ELIGIBLE_PRIMITIVE")

    W = build_waveform_matrix(selected)
    a0 = initialize_amplitudes(selected, objective, o_t)
    a = optimize_amplitudes(
        a0=a0,
        W=W,
        selected=selected,
        objective=objective,
        budget=budget,
        constraints=planner_constraints,
    )

    delta_plan = W @ a
    delta_plan = project_all_constraints(delta_plan, budget)

    # 6. Validate
    validation = validate_plan(delta_plan, selected, objective, budget, o_t)
    if not validation.accept:
        return fallback_plan(validation.reason, selected, budget)

    # 7. Return first block for receding horizon execution
    return PlannerOutput(
        selected_primitives=selected,
        delta_u_plan=delta_plan,
        delta_u_apply=delta_plan[:planner_config.apply_horizon_K],
        expected_response=validation.expected_response,
        constraints=validation.constraint_usage,
        fallback=build_fallback_rules(selected),
    )
```

## 附录 B: Online adapter 伪代码

```python
def update_online_state(online_state, executed_plan, observed_trace):
    for p in executed_plan.selected_primitives:
        pred = executed_plan.expected_response[p.primitive_id]
        obs = extract_observed_response(observed_trace, p)

        sign_match = compute_sign_match(pred, obs)
        gain_ratio = obs.gain / (pred.gain + 1e-8)
        delay_error = obs.peak_horizon - pred.peak_horizon
        shape_match = cosine(pred.response_curve, obs.response_curve)
        compensation = compute_compensation(obs)

        match_score = (
            0.35 * float(sign_match)
            + 0.30 * clip(gain_ratio, 0.0, 1.5) / 1.5
            + 0.25 * exp(-abs(delay_error) / 5.0)
            + 0.10 * max(0.0, shape_match)
            - 0.10 * compensation
        )

        m = p.mechanism_id
        old_conf = online_state.confidence.get(m, 1.0)
        online_state.confidence[m] = 0.8 * old_conf + 0.2 * match_score

        if abs(delay_error) >= 2:
            old_shift = online_state.delay_shift.get(m, 0)
            online_state.delay_shift[m] = clip(old_shift + sign(delay_error), -5, 5)

        if not sign_match:
            online_state.sign_mismatch_count[m] += 1
        else:
            online_state.sign_mismatch_count[m] = 0

        if online_state.sign_mismatch_count[m] >= 2:
            online_state.disabled_mechanisms.add(m)

    return online_state
```

## 附录 C: 推荐 artifact 命名

```text
stage1_<date>_<stack>_<scenario>_temporal_response/
stage2_<date>_<stack>_<scenario>_mechanism_compile/
stage3_<date>_usdta_core_<variant>_planner/
stage4_<date>_<stack>_<scenario>_<variant>_closed_loop/
```

## 附录 D: 快速启动命令模板

```bash
python scripts/usdta/run_stage1_temporal_response.py \
  --config configs/usdta/derivative_estimator.yaml \
  --threat-model configs/usdta/threat_model.yaml \
  --risk-outputs configs/usdta/risk_outputs.yaml \
  --out artifacts/stage1_temporal_response_modeling

python scripts/usdta/compile_stage2_mechanisms.py \
  --bundle artifacts/stage1_temporal_response_modeling/models/J_regime_ensemble.npz \
  --gate configs/usdta/mechanism_gate.yaml \
  --primitive-config configs/usdta/primitive_generation.yaml \
  --out artifacts/stage2_mechanism_compiler

python scripts/usdta/run_stage3_planner_replay.py \
  --planner configs/usdta/planner_core_full.yaml \
  --objective configs/usdta/objective_tracking.yaml \
  --primitives artifacts/stage2_mechanism_compiler/models/primitive_library.json \
  --out artifacts/stage3_usdta_planner

python scripts/usdta/run_stage4_closed_loop_eval.py \
  --sessions configs/usdta/session_grid.yaml \
  --planner configs/usdta/planner_core_full.yaml \
  --out artifacts/stage4_closed_loop_attack
```

---

# 结语

这条 Stage1–4 实验线把 USDTA 定义为一个完整的时序稀疏攻击规划系统：Stage1 估计可控输入到未来风险输出的局部时序导数，Stage2 将导数响应编译为带有 regime、delay、uncertainty 和 guard 的攻击原语，Stage3 在当前目标和预算下进行鲁棒稀疏时序规划，Stage4 在闭环环境中执行、监控、诊断并回写机制置信度。

最终形成的算法不依赖单个大系数，也不依赖固定扰动模板，而是根据当前飞行状态、目标风险函数和模型不确定性动态选择攻击机制、扰动时序和幅度分配。
