from __future__ import annotations


COMMAND_COLUMNS = [
    "command_roll",
    "command_pitch",
    "command_yaw",
    "command_throttle",
]

STATE_COLUMNS = [
    "roll",
    "pitch",
    "yaw",
    "roll_rate",
    "pitch_rate",
    "yaw_rate",
    "position_x",
    "position_y",
    "position_z",
    "velocity_x",
    "velocity_y",
    "velocity_z",
    "altitude",
    "vertical_speed",
    "heading",
]

STATE_SUBSET_COLUMNS = [
    "roll",
    "pitch",
    "yaw",
    "roll_rate",
    "pitch_rate",
    "yaw_rate",
]

CONTROLLER_PARAM_PREFIX = "param_"
BACKEND_PREFIX = "backend_"
MODE_PREFIX = "mode_"
SCENARIO_PREFIX = "scenario_"
CONFIG_PROFILE_PREFIX = "config_profile_"

INTERNAL_COLUMNS = [
    "integrator_roll",
    "integrator_pitch",
    "integrator_yaw",
    "control_output_roll",
    "control_output_pitch",
    "control_output_yaw",
    "torque_achieved",
    "thrust_achieved",
    "saturation_ratio",
]

ACTUATOR_COLUMNS = [
    "actuator_1",
    "actuator_2",
    "actuator_3",
    "actuator_4",
]

TRACKING_ERROR_COLUMNS = [
    "tracking_error_roll",
    "tracking_error_pitch",
    "tracking_error_yaw",
    "tracking_error_rate_roll",
    "tracking_error_rate_pitch",
    "tracking_error_rate_yaw",
]

STABILITY_PROXY_COLUMNS = [
    "saturation_ratio",
    "control_effort_magnitude",
    "tracking_error_magnitude",
]

WINDOW_SUMMARY_BASE_COLUMNS = [
    "roll",
    "pitch",
    "yaw",
    "roll_rate",
    "pitch_rate",
    "yaw_rate",
    "altitude",
    "vertical_speed",
]

X_GROUPS = {
    "commands": COMMAND_COLUMNS,
    "state": STATE_COLUMNS,
    "controller_params": [],
    "backend_mode": [],
    "internal": INTERNAL_COLUMNS,
    "actuator_feedback": ACTUATOR_COLUMNS,
}

Y_GROUPS = {
    "raw_state": STATE_COLUMNS,
    "selected_state_subset": STATE_SUBSET_COLUMNS,
    "actuator": ACTUATOR_COLUMNS,
    "tracking_error": TRACKING_ERROR_COLUMNS,
    "stability_proxy": STABILITY_PROXY_COLUMNS,
    "window_summary_base": WINDOW_SUMMARY_BASE_COLUMNS,
}

STRICT_RAW_X_SCHEMAS = {
    "commands_only",
    "commands_plus_state",
    "commands_plus_state_history",
    "commands_plus_controller_params",
    "commands_plus_state_plus_params",
    "pooled_backend_mode_augmented",
    "full_augmented",
}
