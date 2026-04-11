#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VEHICLE="ArduCopter"
FRAME="quad"
REPEAT=1
INCLUDE_GUIDED_NOGPS=0

usage() {
  cat <<'EOF'
Usage: run_ardupilot_visual_demos.sh [--vehicle ArduCopter] [--frame quad] [--repeat 1] [--include-guided-nogps]

Capture ArduPilot visual demo runs without feeding them into the authoritative analysis path.
By default, the ArduPilot backend will open MAVProxy GUI windows when a desktop display is available.
Set AUTOPILOT_LAB_HEADLESS=1 to suppress GUI windows.
By default only the stable STABILIZE visual demo is run. Add --include-guided-nogps to also try GUIDED_NOGPS.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --vehicle) VEHICLE="$2"; shift ;;
    --frame) FRAME="$2"; shift ;;
    --repeat) REPEAT="$2"; shift ;;
    --include-guided-nogps) INCLUDE_GUIDED_NOGPS=1 ;;
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

CONFIG_ARGS=(
  --config "${ROOT_DIR}/configs/studies/ardupilot_real_nominal_stabilize_capture.yaml"
)
if [[ "${INCLUDE_GUIDED_NOGPS}" -eq 1 ]]; then
  CONFIG_ARGS+=(--config "${ROOT_DIR}/configs/studies/ardupilot_real_nominal_guided_nogps_capture.yaml")
fi

if command -v ros2 >/dev/null 2>&1 && ros2 pkg prefix ardupilot_mavlink_backend >/dev/null 2>&1; then
  ros2 run ardupilot_mavlink_backend ardupilot_linearity_matrix \
    --vehicle "${VEHICLE}" \
    --frame "${FRAME}" \
    "${CONFIG_ARGS[@]}" \
    --repeat "${REPEAT}"
else
  run_py 'from ardupilot_mavlink_backend.linearity_matrix import main; main()' \
    --vehicle "${VEHICLE}" \
    --frame "${FRAME}" \
    "${CONFIG_ARGS[@]}" \
    --repeat "${REPEAT}"
fi
