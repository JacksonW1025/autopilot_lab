# Diagnostic Gate

## Attitude Axes
- `OFFBOARD_ATTITUDE pitch`: small: 2A/0R, medium: 2A/0R, large: 2A/0R; first_problem_tier=none
- `OFFBOARD_ATTITUDE roll`: small: 2A/0R, medium: 2A/0R, large: 2A/0R; first_problem_tier=none
- `OFFBOARD_ATTITUDE yaw`: small: 2A/0R, medium: 2A/0R, large: 2A/0R; first_problem_tier=none
- `POSCTL pitch`: small: 2A/0R, medium: 2A/0R, large: 2A/0R; first_problem_tier=none
- `POSCTL roll`: small: 2A/0R, medium: 2A/0R, large: 2A/0R; first_problem_tier=none
- `POSCTL yaw`: small: 2A/0R, medium: 2A/0R, large: 2A/0R; first_problem_tier=none

## Throttle
- `OFFBOARD_ATTITUDE throttle`: small: 2A/0R, medium: 2A/1R, large: 2A/0R; first_problem_tier=medium; reasons=active_phase_missing, experiment_not_started, insufficient_active_nonzero_command_samples
- `POSCTL throttle`: small: 2A/0R, medium: 2A/0R, large: 2A/1R; first_problem_tier=large; reasons=experiment_truncated_before_expected_active_samples, failsafe_during_experiment

## Conclusion
- 姿态轴在当前诊断矩阵内保持 accepted；throttle 是最早系统性出问题的通道。