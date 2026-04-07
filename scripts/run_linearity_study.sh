#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: run_linearity_study.sh --config PATH [--skip-analysis]

Run one global-linearity study from raw capture through report generation.
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

if command -v ros2 >/dev/null 2>&1 && ros2 pkg prefix linearity_study >/dev/null 2>&1; then
  ros2 run linearity_study linearity_run_study "$@"
else
  python3 -c 'from linearity_study.linearity_run_study import main; main()' "$@"
fi
