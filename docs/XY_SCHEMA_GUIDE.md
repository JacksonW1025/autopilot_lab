# X/Y Schema Guide

## 先怎么读当前正式结果

如果你现在要读最新结果，不要再从 20260409 的 broad baseline 开始。

当前推荐顺序是：

1. PX4 generalization full baseline
   - `../artifacts/studies/20260410_224818_px4_real_generalization_ablation`
2. PX4 generalization full diagnostic
   - `../artifacts/studies/20260411_021910_px4_generalization_diagnostic_matrix`
3. ArduPilot generalization full baseline
   - `../artifacts/studies/20260411_095055_ardupilot_real_generalization_ablation`
4. ArduPilot generalization full diagnostic
   - `../artifacts/studies/20260411_105433_ardupilot_generalization_diagnostic_matrix`

理由很简单：这四个 study 已经把“线性是否存在”和“它是否跨 scenario 仍然成立”两件事一起回答了。

## 当前最值得先看的代表性组合

### PX4：状态演化主线

当前最有代表性的 PX4 组合是：

- `full_augmented -> next_raw_state | ols_affine | stratified`

它是 current generalization full baseline 中的代表性 generalized-supported 结果，路径在：

- `../artifacts/studies/20260410_224818_px4_real_generalization_ablation/fits/full_augmented__next_raw_state__stratified/ols_affine/`

为什么先看它：

- 它直接回答“当前输入和状态，能否线性预测下一时刻状态”；
- 它不是只在单一 scenario 下高分，而是在 `nominal / dynamic / throttle_biased` 下都站得住；
- 它更接近“状态演化映射”本身，而不是只解释执行器响应。

### ArduPilot：当前最稳的跨场景主结构

当前最有代表性的 ArduPilot 组合是：

- `commands_only -> actuator_response | ridge_affine | pooled`

路径在：

- `../artifacts/studies/20260411_095055_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/`

为什么先看它：

- 它是当前 ArduPilot 最稳的 generalized-supported 主结构；
- 它说明 ArduPilot 不是“没有线性”，而是当前最稳的线性证据更集中在命令到响应的映射层；
- 这也是为什么当前 broad conclusion 不能被简单写成“ArduPilot 不支持线性”。

## X Schema 怎么理解

平台内置这些主要 `X-schema`：

- `commands_only`
  - 只用 `command_roll / pitch / yaw / throttle`
- `commands_plus_state`
  - command + 当前状态
- `commands_plus_state_history`
  - command + 当前状态 + 历史 lag
- `pooled_backend_mode_augmented`
  - command + state + backend/mode one-hot
- `full_augmented`
  - 再加入 internal signal 和 actuator feedback
- `feature_mapped_linear`
  - 仍然用线性拟合器，但输入已经变成工程化特征空间

### 当前怎么用这些 X Schema

- 如果你在看“状态演化是否线性”，先看 `commands_plus_state_history` 和 `full_augmented`。
- 如果你在看“命令到响应的直接路径是否线性”，先看 `commands_only`。
- 如果你在看 generalization study，不要把 `scenario_` one-hot 当成当前正式主解释。
  这条线想验证的是“同一个 `f` 是否跨 scenario 站得住”，不是让模型直接记住 scenario 标签。

## Y Schema 怎么理解

平台内置这些主要 `Y-schema`：

- `next_raw_state`
- `delta_state`
- `selected_state_subset`
- `future_state_horizon`
- `actuator_response`
- `window_summary_response`

### 当前怎么用这些 Y Schema

- `next_raw_state`
  最接近“状态下一步会变成什么”。
- `selected_state_subset`
  更像压缩版状态演化问题，便于先看主变量。
- `future_state_horizon`
  看短时未来窗口是否仍能被同一个线性结构解释。
- `actuator_response`
  看命令是否能稳定映射到执行器层响应。

## 当前推荐的阅读方法

1. 先看 `summary.md`
   - 它告诉你 best combo、support 和整体排序。
2. 再看 `scenario_generalization.md`
   - 它告诉你这个 combo 是 `generalized_supported`、`supported_but_local` 还是 `not_generalized`。
3. 再看 `matrix_f.csv` 和热力图
   - 这一步才是真正看“哪些输入连到了哪些输出”。
4. 如果遇到高 `R2` 但 support 仍然不高的组合，再去看：
   - `effective_condition_number`
   - `coefficient_stability`
   - ArduPilot 的 `state_evolution_audit.md`

## 当前最重要的阅读边界

- `feature_mapped_linear` 仍然是线性拟合器，但它不属于 strict raw linear；它更像“经过工程化特征变换后的线性”。
- `best_result` 不一定等于“最稳的正式结论”。
  有时 best result 只是高分，但 supported anchor 才是当前真正站稳的证据。
- 对 ArduPilot 尤其要注意：
  高 `R2` 不等于已经得到稳定 state-evolution 结论，必须把条件数和稳定性一起看。
