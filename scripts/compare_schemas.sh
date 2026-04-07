#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: compare_schemas.sh --config PATH --plan PATH [--run-dir DIR ... | --study-dir DIR]

Compare multiple X/Y schema combinations on one or more raw runs.
EOF
}

set +u
source /opt/ros/humble/setup.bash
source "${ROOT_DIR}/scripts/autopilot_lab_env.sh" >/dev/null
set -u

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" || $# -eq 0 ]]; then
  usage
  exit 0
fi

if command -v ros2 >/dev/null 2>&1 && ros2 pkg prefix linearity_analysis >/dev/null 2>&1; then
  ros2 run linearity_analysis linearity_compare_schemas "$@"
else
  python3 -c 'from linearity_analysis.linearity_compare_schemas import main; main()' "$@"
fi
