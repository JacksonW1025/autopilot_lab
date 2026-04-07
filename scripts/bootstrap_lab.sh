#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_PATH="${ROOT_DIR}/lab.lock.json"
DRY_RUN=0
SKIP_SYSTEM_DEPS=0
SKIP_PYTHON_DEPS=0
SKIP_BUILD=0

usage() {
  cat <<'EOF'
Usage: bootstrap_lab.sh [--dry-run] [--skip-system-deps] [--skip-python-deps] [--skip-build]

Bootstrap the global linearity study environment:
  1. validate external repositories
  2. initialize submodules
  3. install system and Python dependencies
  4. build the workspace
  5. validate linearity study CLIs
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --skip-system-deps) SKIP_SYSTEM_DEPS=1 ;;
    --skip-python-deps) SKIP_PYTHON_DEPS=1 ;;
    --skip-build) SKIP_BUILD=1 ;;
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

run_cmd() {
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] $*"
    return 0
  fi
  echo "+ $*"
  "$@"
}

AUTOPILOT_LAB_ROOT="${AUTOPILOT_LAB_ROOT:-$(json_value external_roots.AUTOPILOT_LAB_ROOT)}"
PX4_ROOT="${PX4_ROOT:-$(json_value external_roots.PX4_ROOT)}"
ARDUPILOT_ROOT="${ARDUPILOT_ROOT:-$(json_value external_roots.ARDUPILOT_ROOT)}"

for required_path in "$AUTOPILOT_LAB_ROOT" "$PX4_ROOT" "$ARDUPILOT_ROOT"; do
  if [[ ! -d "$required_path" ]]; then
    echo "missing required path: $required_path" >&2
    exit 1
  fi
done

cd "$ROOT_DIR"
run_cmd git submodule update --init --recursive

if [[ $SKIP_SYSTEM_DEPS -eq 0 ]]; then
  run_cmd sudo apt-get update
  run_cmd sudo apt-get install -y python3-pip python3-colcon-common-extensions python3-vcstool
fi

if [[ $SKIP_PYTHON_DEPS -eq 0 ]]; then
  mapfile -t PIP_MODULES < <(json_value python_pip_modules)
  if [[ ${#PIP_MODULES[@]} -gt 0 ]]; then
    run_cmd python3 -m pip install --user --upgrade "${PIP_MODULES[@]}"
  fi
fi

if [[ $SKIP_BUILD -eq 0 ]]; then
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] source /opt/ros/humble/setup.bash && colcon build --symlink-install"
  else
    set +u
    source /opt/ros/humble/setup.bash
    set -u
    echo "+ colcon build --symlink-install"
    colcon build --symlink-install
  fi
fi

if [[ $DRY_RUN -eq 1 ]]; then
  echo "[dry-run] validate linearity study CLIs after build"
  exit 0
fi

set +u
source "${AUTOPILOT_LAB_ROOT}/scripts/autopilot_lab_env.sh" >/dev/null
set -u

mapfile -t BACKEND_CLIS < <(json_value backend_clis)
for cli in "${BACKEND_CLIS[@]}"; do
  if ! command -v "$cli" >/dev/null 2>&1; then
    echo "missing backend CLI after bootstrap: $cli" >&2
    exit 1
  fi
done

echo "bootstrap_status=ready"
