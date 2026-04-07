# Experiment Protocol

## 主流程

1. 选定 study scope
2. 配置 backend、mode、scenario、采样率、repeat、seed
3. 选择 `x_schema` 与 `y_schema`
4. 执行 raw run 采集
5. 构建 prepared sample table
6. 拟合全局线性/仿射模型
7. 估计稀疏性与稳定性
8. 生成报告并比较 schema

## 推荐研究顺序

1. 先跑 `commands_only`
2. 再跑 `commands_plus_state`
3. 再加入 `history`
4. 再测试 `pooled_backend_mode_augmented`
5. 最后在明确需要时尝试 `full_augmented` 或 `feature_mapped_linear`

## 支持的激励策略

- 单变量 sweep
- 两变量组合 sweep
- 随机组合探索
- 小扰动实验
- broad exploration
- 参数扫描

## pooled 与 stratified

- `pooled`
  - 混合 backend / mode / scenario 一起拟合
- `stratified`
  - 每个分层单独拟合
- `compare_both`
  - 同时输出两者并比较

## 结论口径

每个 study 至少给出：

- `f`
- `b`
- 稀疏 mask
- `R² / MSE / MAE`
- residual statistics
- condition number / singular values
- coefficient stability
- backend/mode consistency
- top influential connections

并明确判断：

- `supported`
- `partial`
- `unsupported`
