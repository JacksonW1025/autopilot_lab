from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for package_root in (
    ROOT / "src" / "linearity_core",
    ROOT / "src" / "linearity_analysis",
    ROOT / "src" / "linearity_study",
    ROOT / "src" / "px4_ros2_backend",
    ROOT / "src" / "ardupilot_mavlink_backend",
):
    sys.path.insert(0, str(package_root))
