# Backend Compare

## Baseline
- `PX4`: accepted_runs=30/30; stability=stable; best_combo=full_augmented | next_raw_state | ols_affine | stratified
- `ArduPilot`: accepted_runs=30/30; stability=unknown; best_combo=commands_plus_state_history | selected_state_subset | ols_affine | pooled
- both_baselines_stable: `false`

## Diagnostic Gate
- `PX4` attitude: accepted=OFFBOARD_ATTITUDE pitch, OFFBOARD_ATTITUDE roll, OFFBOARD_ATTITUDE yaw, POSCTL pitch, POSCTL roll, POSCTL yaw; rejected=none
- `ArduPilot` attitude: accepted=GUIDED_NOGPS pitch, GUIDED_NOGPS roll, GUIDED_NOGPS yaw, STABILIZE pitch, STABILIZE roll, STABILIZE yaw; rejected=none
- `PX4` throttle_boundary: `mixed`; reasons=active_phase_missing, experiment_not_started, experiment_truncated_before_expected_active_samples, failsafe_during_experiment, insufficient_active_nonzero_command_samples
- `ArduPilot` throttle_boundary: `none`; reasons=none
- throttle_boundary_consistent: `false`

## Scenario Generalization
- `PX4` baseline: generalized_supported=80; supported_but_local=40; not_generalized=96; representative=full_augmented | next_raw_state | ols_affine | stratified
- `PX4` diagnostic: generalized_supported=111; supported_but_local=15; not_generalized=90; representative=full_augmented | next_raw_state | ols_affine | stratified
- `ArduPilot` baseline: generalized_supported=12; supported_but_local=0; not_generalized=204; representative=commands_only | actuator_response | ridge_affine | pooled
- `ArduPilot` diagnostic: generalized_supported=12; supported_but_local=0; not_generalized=204; representative=commands_only | actuator_response | ridge_affine | pooled
- generalization_difference_driver: `both_support_cross_scenario_linearity_but_px4_is_broader`

## Conclusion
- difference_driver: `baseline_stability_unresolved`
- 当前差异更像 baseline 还不够稳，暂时不适合把 backend 差异当作主解释。 两边都已给出跨 scenario 的正面线性证据，但 PX4 的 generalized-supported 组合明显更多。