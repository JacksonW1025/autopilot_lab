from __future__ import annotations

import math

from linearity_core.config import StudyConfig
from linearity_core.excitation import ExcitationGenerator


def _base_payload() -> dict:
    return {
        "study_name": "generalization_profile",
        "backend": "synthetic",
        "flight_mode": "POSCTL",
        "scenario": "nominal",
        "config_profile": "generalization_profile",
        "seed": 17,
        "repeat_count": 1,
        "sampling_rate_hz": 20.0,
        "x_schema": "commands_only",
        "y_schema": "delta_state",
        "model": ["ols_affine"],
        "input_type": "manual",
        "axis": "composite",
        "amplitude": 0.18,
        "bias": 0.0,
        "start_after_s": 1.0,
        "duration_s": 6.0,
        "hold_s": 1.0,
        "hover_thrust": -0.69,
    }


def test_multi_broad_generates_decorrelated_composite_targets() -> None:
    config = StudyConfig.from_dict(
        {
            **_base_payload(),
            "profile_type": "multi_broad",
            "extras": {
                "roll_amplitude": 1.0,
                "pitch_amplitude": 0.8,
                "yaw_amplitude": 0.4,
                "throttle_amplitude": 0.12,
                "multi_broad_frequencies_hz": {
                    "roll": [0.13, 0.37, 0.71],
                    "pitch": [0.17, 0.43, 0.89],
                    "yaw": [0.11, 0.29, 0.61],
                    "throttle": [0.19, 0.47, 0.97],
                },
                "multi_broad_phases_rad": {
                    "roll": [0.0, 0.9, 1.8],
                    "pitch": [0.4, 1.3, 2.2],
                    "yaw": [0.7, 1.6, 2.5],
                    "throttle": [1.1, 2.0, 2.9],
                },
            },
        }
    )
    generator = ExcitationGenerator(config)
    early_profile, early_roll, early_pitch, early_yaw, early_throttle, early_phase = generator.manual_targets_at(1.5)
    later_profile, later_roll, later_pitch, later_yaw, later_throttle, later_phase = generator.manual_targets_at(2.1)
    assert early_phase == "multi_broad_active"
    assert later_phase == "multi_broad_active"
    assert not math.isclose(early_roll, early_pitch)
    assert not math.isclose(early_roll, early_yaw)
    assert not math.isclose(early_throttle, later_throttle)
    assert not math.isclose(early_profile, later_profile)
    samples = [generator.manual_targets_at(elapsed_s) for elapsed_s in (1.2, 1.8, 2.4, 3.0, 3.6, 4.2, 4.8, 5.4)]
    roll_values = [item[1] for item in samples]
    pitch_values = [item[2] for item in samples]
    assert min(roll_values) < 0.0 < max(roll_values) or min(pitch_values) < 0.0 < max(pitch_values)


def test_alternating_pulse_train_flips_signs_in_order() -> None:
    config = StudyConfig.from_dict(
        {
            **_base_payload(),
            "profile_type": "alternating_pulse_train",
            "axis": "throttle",
            "amplitude": 0.2,
            "extras": {
                "pulse_count": 5,
                "pulse_width_s": 0.35,
                "pulse_gap_s": 0.65,
            },
        }
    )
    generator = ExcitationGenerator(config)
    observed = []
    for elapsed_s in (1.05, 2.05, 3.05, 4.05, 5.05):
        value, phase = generator.profile_value_at(elapsed_s)
        observed.append((round(value, 6), phase))
    assert [phase for _value, phase in observed] == [
        "alternating_pulse_active_pos",
        "alternating_pulse_active_neg",
        "alternating_pulse_active_pos",
        "alternating_pulse_active_neg",
        "alternating_pulse_active_pos",
    ]
    assert [value for value, _phase in observed] == [0.2, -0.2, 0.2, -0.2, 0.2]
