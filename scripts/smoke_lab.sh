#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_PATH="${ROOT_DIR}/milestone.lock.json"
BACKEND="all"
REPEAT=1
PX4_WORLD="default"
SKIP_DOCTOR=0

usage() {
  cat <<'EOF'
Usage: smoke_lab.sh [--backend all|px4|ardupilot] [--repeat N] [--px4-world WORLD] [--skip-doctor]

Run the canonical Dual-Backend M1 smoke suite and finish with strict study analysis.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --backend)
      BACKEND="$2"
      shift
      ;;
    --repeat)
      REPEAT="$2"
      shift
      ;;
    --px4-world)
      PX4_WORLD="$2"
      shift
      ;;
    --skip-doctor)
      SKIP_DOCTOR=1
      ;;
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

json_value() {
  local expr="$1"
  python3 - "$LOCK_PATH" "$expr" <<'PY'
import json
import sys

path, expr = sys.argv[1], sys.argv[2]
payload = json.load(open(path, "r", encoding="utf-8"))
value = payload
for part in expr.split("."):
    if not part:
        continue
    value = value[part]
if isinstance(value, list):
    for item in value:
        print(item)
else:
    print(value)
PY
}

if [[ $SKIP_DOCTOR -eq 0 ]]; then
  "${ROOT_DIR}/scripts/doctor_lab.sh"
fi

set +u
source /opt/ros/humble/setup.bash
source "${ROOT_DIR}/scripts/autopilot_lab_env.sh"
set -u

mapfile -t CANONICAL_CONFIGS < <(json_value canonical_smoke_configs)
declare -a PATTERNS=()
for config_path in "${CANONICAL_CONFIGS[@]}"; do
  PATTERNS+=("--pattern" "$(basename "$config_path")")
done

if [[ "$BACKEND" == "all" || "$BACKEND" == "px4" ]]; then
  ros2 run px4_ros2_backend px4_matrix_runner --world "$PX4_WORLD" --repeat "$REPEAT" "${PATTERNS[@]}"
fi

if [[ "$BACKEND" == "all" || "$BACKEND" == "ardupilot" ]]; then
  ros2 run ardupilot_mavlink_backend ardupilot_matrix_runner --repeat "$REPEAT" "${PATTERNS[@]}"
fi

ros2 run fep_core study_analysis_runner
echo "smoke_status=completed"
