#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VEHICLE="ArduCopter"
FRAME="quad"
REPEAT=1
ACCEPTED_TARGET=0
MAX_ATTEMPTS_PER_CONFIG=""
SKIP_SITL=0
MATRIX_DIR=""
ANALYSIS_CONFIG="${ROOT_DIR}/configs/studies/ardupilot_real_nominal_broad_ablation_analysis.yaml"
ABLATION_PLAN="${ROOT_DIR}/configs/ablations/ardupilot_real_broad_ablation.yaml"

usage() {
  cat <<'EOF'
Usage: run_ardupilot_broad_ablation.sh [--vehicle ArduCopter] [--frame quad] [--repeat 1]
                                       [--accepted-target 0] [--max-attempts-per-config N]
                                       [--skip-sitl] [--skip-capture --matrix-dir DIR]
                                       [--analysis-config PATH] [--plan PATH]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --vehicle) VEHICLE="$2"; shift ;;
    --frame) FRAME="$2"; shift ;;
    --repeat) REPEAT="$2"; shift ;;
    --accepted-target) ACCEPTED_TARGET="$2"; shift ;;
    --max-attempts-per-config) MAX_ATTEMPTS_PER_CONFIG="$2"; shift ;;
    --skip-sitl) SKIP_SITL=1 ;;
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

SKIP_CAPTURE="${SKIP_CAPTURE:-0}"

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
  MATRIX_ARGS=(
    --vehicle "${VEHICLE}"
    --frame "${FRAME}"
    --pattern ardupilot_real_nominal_stabilize_capture.yaml
    --pattern ardupilot_real_nominal_guided_nogps_capture.yaml
    --repeat "${REPEAT}"
    --accepted-target "${ACCEPTED_TARGET}"
  )
  if [[ $SKIP_SITL -eq 1 ]]; then
    MATRIX_ARGS+=(--skip-sitl)
  fi
  if [[ -n "${MAX_ATTEMPTS_PER_CONFIG}" ]]; then
    MATRIX_ARGS+=(--max-attempts-per-config "${MAX_ATTEMPTS_PER_CONFIG}")
  fi
  if command -v ros2 >/dev/null 2>&1 && ros2 pkg prefix ardupilot_mavlink_backend >/dev/null 2>&1; then
    MATRIX_OUTPUT="$(ros2 run ardupilot_mavlink_backend ardupilot_linearity_matrix "${MATRIX_ARGS[@]}")"
  else
    MATRIX_OUTPUT="$(run_py 'from ardupilot_mavlink_backend.linearity_matrix import main; main()' "${MATRIX_ARGS[@]}")"
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
