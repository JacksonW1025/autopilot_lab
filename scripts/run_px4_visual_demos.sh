#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORLD="default"
REPEAT=1

usage() {
  cat <<'EOF'
Usage: run_px4_visual_demos.sh [--world default] [--repeat 1]

Capture PX4 visual demo runs without feeding them into the authoritative analysis path.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --world) WORLD="$2"; shift ;;
    --repeat) REPEAT="$2"; shift ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

set +u
source /opt/ros/humble/setup.bash
source "${ROOT_DIR}/scripts/autopilot_lab_env.sh" >/dev/null
set -u

run_py() {
  local module_expr="$1"
  shift
  python3 -c "$module_expr" "$@"
}

if command -v ros2 >/dev/null 2>&1 && ros2 pkg prefix px4_ros2_backend >/dev/null 2>&1; then
  ros2 run px4_ros2_backend px4_linearity_matrix \
    --world "${WORLD}" \
    --pattern px4_visual_demo_offboard_roll_sweep_capture.yaml \
    --pattern px4_visual_demo_offboard_yaw_sweep_capture.yaml \
    --repeat "${REPEAT}"
else
  run_py 'from px4_ros2_backend.linearity_matrix import main; main()' \
    --world "${WORLD}" \
    --pattern px4_visual_demo_offboard_roll_sweep_capture.yaml \
    --pattern px4_visual_demo_offboard_yaw_sweep_capture.yaml \
    --repeat "${REPEAT}"
fi

