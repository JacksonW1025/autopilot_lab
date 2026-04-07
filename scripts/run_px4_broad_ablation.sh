#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORLD="default"
REPEAT=1
SKIP_CAPTURE=0
MATRIX_DIR=""
ANALYSIS_CONFIG="${ROOT_DIR}/configs/studies/px4_real_nominal_broad_ablation_analysis.yaml"
ABLATION_PLAN="${ROOT_DIR}/configs/ablations/px4_real_broad_ablation.yaml"

usage() {
  cat <<'EOF'
Usage: run_px4_broad_ablation.sh [--world default] [--repeat 1] [--skip-capture --matrix-dir DIR]
                                  [--analysis-config PATH] [--plan PATH]

Run the first real PX4 broad-ablation report:
  1. fresh PX4 raw capture for POSCTL and OFFBOARD_ATTITUDE
  2. compare multiple X/Y schema combinations
  3. generate a study report under artifacts/studies/
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --world) WORLD="$2"; shift ;;
    --repeat) REPEAT="$2"; shift ;;
    --skip-capture) SKIP_CAPTURE=1 ;;
    --matrix-dir) MATRIX_DIR="$2"; shift ;;
    --analysis-config) ANALYSIS_CONFIG="$2"; shift ;;
    --plan) ABLATION_PLAN="$2"; shift ;;
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

if [[ $SKIP_CAPTURE -eq 0 ]]; then
  if command -v ros2 >/dev/null 2>&1 && ros2 pkg prefix px4_ros2_backend >/dev/null 2>&1; then
    MATRIX_OUTPUT="$(ros2 run px4_ros2_backend px4_linearity_matrix \
      --world "${WORLD}" \
      --pattern px4_real_nominal_posctl_capture.yaml \
      --pattern px4_real_nominal_offboard_attitude_capture.yaml \
      --repeat "${REPEAT}")"
  else
    MATRIX_OUTPUT="$(run_py 'from px4_ros2_backend.linearity_matrix import main; main()' \
      --world "${WORLD}" \
      --pattern px4_real_nominal_posctl_capture.yaml \
      --pattern px4_real_nominal_offboard_attitude_capture.yaml \
      --repeat "${REPEAT}")"
  fi
  printf '%s\n' "${MATRIX_OUTPUT}"
  MATRIX_DIR="$(printf '%s\n' "${MATRIX_OUTPUT}" | awk -F= '/^matrix_dir=/{print $2}' | tail -n 1)"
fi

if [[ -z "${MATRIX_DIR}" ]]; then
  echo "matrix_dir is required" >&2
  exit 1
fi

RUNS_MANIFEST="${MATRIX_DIR}/runs.csv"

if command -v ros2 >/dev/null 2>&1 && ros2 pkg prefix linearity_analysis >/dev/null 2>&1; then
  ros2 run linearity_analysis linearity_compare_schemas \
    --config "${ANALYSIS_CONFIG}" \
    --plan "${ABLATION_PLAN}" \
    --runs-manifest "${RUNS_MANIFEST}"
else
  run_py 'from linearity_analysis.linearity_compare_schemas import main; main()' \
    --config "${ANALYSIS_CONFIG}" \
    --plan "${ABLATION_PLAN}" \
    --runs-manifest "${RUNS_MANIFEST}"
fi
