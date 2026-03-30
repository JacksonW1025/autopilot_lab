from __future__ import annotations

import os
from pathlib import Path


def _path_from_env(name: str, default: str) -> Path:
    return Path(os.environ.get(name, default)).expanduser()


WORKSPACE_ROOT = _path_from_env("AUTOPILOT_LAB_ROOT", "/home/car/autopilot_lab")
PX4_ROOT = _path_from_env("PX4_ROOT", "/home/car/PX4-Autopilot")
ARDUPILOT_ROOT = _path_from_env("ARDUPILOT_ROOT", "/home/car/ardupilot")

ARTIFACT_ROOT = WORKSPACE_ROOT / "artifacts"
PX4_ARTIFACT_ROOT = ARTIFACT_ROOT / "px4"
ARDUPILOT_ARTIFACT_ROOT = ARTIFACT_ROOT / "ardupilot"
STUDY_ARTIFACT_ROOT = ARTIFACT_ROOT / "studies"

PX4_RUNS_ROOT = PX4_ARTIFACT_ROOT / "runs"
PX4_ANALYSIS_ROOT = PX4_ARTIFACT_ROOT / "analysis"
PX4_MATRIX_ROOT = PX4_ARTIFACT_ROOT / "matrix"
PX4_IDENTIFICATION_ROOT = PX4_ARTIFACT_ROOT / "identification"
PX4_LOG_ROOT = PX4_ROOT / "build/px4_sitl_default/rootfs/log"

ARDUPILOT_RUNS_ROOT = ARDUPILOT_ARTIFACT_ROOT / "runs"
ARDUPILOT_ANALYSIS_ROOT = ARDUPILOT_ARTIFACT_ROOT / "analysis"
ARDUPILOT_MATRIX_ROOT = ARDUPILOT_ARTIFACT_ROOT / "matrix"
ARDUPILOT_IDENTIFICATION_ROOT = ARDUPILOT_ARTIFACT_ROOT / "identification"
ARDUPILOT_LOG_ROOT = ARDUPILOT_ARTIFACT_ROOT / "logs"
ARDUPILOT_BIN_LOG_ROOT = ARDUPILOT_LOG_ROOT / "bin"
ARDUPILOT_TLOG_ROOT = ARDUPILOT_LOG_ROOT / "tlog"

CONFIG_ROOT = WORKSPACE_ROOT / "src/fep_research/config"
REFERENCE_ROOT = WORKSPACE_ROOT / "reference"
SCRIPTS_ROOT = WORKSPACE_ROOT / "scripts"
MILESTONE_LOCK_PATH = WORKSPACE_ROOT / "milestone.lock.json"


def runs_root_for_backend(backend: str) -> Path:
    mapping = {
        "px4": PX4_RUNS_ROOT,
        "px4_ros2": PX4_RUNS_ROOT,
        "ardupilot": ARDUPILOT_RUNS_ROOT,
        "ardupilot_mavlink": ARDUPILOT_RUNS_ROOT,
    }
    try:
        return mapping[backend]
    except KeyError as exc:
        raise ValueError(f"Unsupported backend: {backend}") from exc
