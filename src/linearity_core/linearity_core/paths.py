from __future__ import annotations

import os
from pathlib import Path


def _path_from_env(name: str, default: str) -> Path:
    return Path(os.environ.get(name, default)).expanduser()


WORKSPACE_ROOT = _path_from_env("AUTOPILOT_LAB_ROOT", "/home/car/autopilot_lab")
PX4_ROOT = _path_from_env("PX4_ROOT", "/home/car/PX4-Autopilot")
ARDUPILOT_ROOT = _path_from_env("ARDUPILOT_ROOT", "/home/car/ardupilot")

ARTIFACT_ROOT = WORKSPACE_ROOT / "artifacts"
RAW_ARTIFACT_ROOT = ARTIFACT_ROOT / "raw"
STUDY_ARTIFACT_ROOT = ARTIFACT_ROOT / "studies"

PX4_RAW_ROOT = RAW_ARTIFACT_ROOT / "px4"
ARDUPILOT_RAW_ROOT = RAW_ARTIFACT_ROOT / "ardupilot"
SYNTHETIC_RAW_ROOT = RAW_ARTIFACT_ROOT / "synthetic"

PX4_MATRIX_ROOT = ARTIFACT_ROOT / "px4_matrix"
ARDUPILOT_MATRIX_ROOT = ARTIFACT_ROOT / "ardupilot_matrix"

CONFIG_ROOT = WORKSPACE_ROOT / "configs" / "studies"
ABLATION_ROOT = WORKSPACE_ROOT / "configs" / "ablations"
DOCS_ROOT = WORKSPACE_ROOT / "docs"
SCRIPTS_ROOT = WORKSPACE_ROOT / "scripts"
LOCK_PATH = WORKSPACE_ROOT / "lab.lock.json"

PX4_LOG_ROOT = PX4_ROOT / "build/px4_sitl_default/rootfs/log"


def raw_root_for_backend(backend: str) -> Path:
    mapping = {
        "px4": PX4_RAW_ROOT,
        "ardupilot": ARDUPILOT_RAW_ROOT,
        "synthetic": SYNTHETIC_RAW_ROOT,
    }
    try:
        return mapping[backend]
    except KeyError as exc:
        raise ValueError(f"Unsupported backend: {backend}") from exc
