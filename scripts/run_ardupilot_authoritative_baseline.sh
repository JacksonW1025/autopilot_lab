#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ACCEPTED_TARGET=5
FORWARD_ARGS=()

usage() {
  cat <<'EOF'
Usage: run_ardupilot_authoritative_baseline.sh [--accepted-target 5] [--max-attempts-per-config N]
                                               [--vehicle ArduCopter] [--frame quad] [--repeat 1]
                                               [--skip-sitl] [--skip-capture --matrix-dir DIR]
                                               [--analysis-config PATH] [--plan PATH]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --accepted-target)
      ACCEPTED_TARGET="$2"
      shift 2
      ;;
    --vehicle|--frame|--repeat|--max-attempts-per-config|--matrix-dir|--analysis-config|--plan)
      FORWARD_ARGS+=("$1" "$2")
      shift 2
      ;;
    --skip-sitl|--skip-capture)
      FORWARD_ARGS+=("$1")
      shift
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

run_stage_check() {
  run_py 'from linearity_analysis.stage_checks import main; main()' "$@"
}

run_stage_check full-prereq

BASELINE_OUTPUT="$("${ROOT_DIR}/scripts/run_ardupilot_broad_ablation.sh" --accepted-target "${ACCEPTED_TARGET}" "${FORWARD_ARGS[@]}")"
printf '%s\n' "${BASELINE_OUTPUT}"

MATRIX_DIR="$(printf '%s\n' "${BASELINE_OUTPUT}" | awk -F= '/^matrix_dir=/{print $2}' | tail -n 1)"
STUDY_DIR="$(printf '%s\n' "${BASELINE_OUTPUT}" | awk -F= '/^study_dir=/{print $2}' | tail -n 1)"

if [[ -z "${MATRIX_DIR}" || -z "${STUDY_DIR}" ]]; then
  echo "matrix_dir and study_dir are required" >&2
  exit 1
fi

run_stage_check full-baseline \
  --matrix-dir "${MATRIX_DIR}" \
  --study-dir "${STUDY_DIR}" \
  --config-name ardupilot_real_nominal_stabilize_capture.yaml \
  --config-name ardupilot_real_nominal_guided_nogps_capture.yaml \
  --accepted-target "${ACCEPTED_TARGET}" \
  --required-path reports/state_evolution_audit.md \
  --required-path summary/state_evolution_audit.json

REFRESH_OUTPUT="$(run_py 'from linearity_analysis.milestone_report import main; main()' --ardupilot-baseline "${STUDY_DIR}")"
printf '%s\n' "${REFRESH_OUTPUT}"
