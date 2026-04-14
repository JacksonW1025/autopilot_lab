#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

set +u
source /opt/ros/humble/setup.bash
source "${ROOT_DIR}/scripts/autopilot_lab_env.sh" >/dev/null
set -u

run_py() {
  local module_expr="$1"
  shift
  python3 -c "$module_expr" "$@"
}

extract_study_dir() {
  awk -F= '/^study_dir=/{print $2}' | tail -n 1
}

STABILIZE_BASELINE_OUTPUT="$(bash "${ROOT_DIR}/scripts/run_ardupilot_state_evolution_baseline.sh" --mode stabilize --stage full "$@")"
printf '%s\n' "${STABILIZE_BASELINE_OUTPUT}"
STABILIZE_BASELINE_DIR="$(printf '%s\n' "${STABILIZE_BASELINE_OUTPUT}" | extract_study_dir)"

STABILIZE_DIAGNOSTIC_OUTPUT="$(bash "${ROOT_DIR}/scripts/run_ardupilot_state_evolution_diagnostic.sh" --mode stabilize --stage full "$@")"
printf '%s\n' "${STABILIZE_DIAGNOSTIC_OUTPUT}"
STABILIZE_DIAGNOSTIC_DIR="$(printf '%s\n' "${STABILIZE_DIAGNOSTIC_OUTPUT}" | extract_study_dir)"

GUIDED_BASELINE_OUTPUT="$(bash "${ROOT_DIR}/scripts/run_ardupilot_state_evolution_baseline.sh" --mode guided_nogps --stage full "$@")"
printf '%s\n' "${GUIDED_BASELINE_OUTPUT}"
GUIDED_BASELINE_DIR="$(printf '%s\n' "${GUIDED_BASELINE_OUTPUT}" | extract_study_dir)"

GUIDED_DIAGNOSTIC_OUTPUT="$(bash "${ROOT_DIR}/scripts/run_ardupilot_state_evolution_diagnostic.sh" --mode guided_nogps --stage full "$@")"
printf '%s\n' "${GUIDED_DIAGNOSTIC_OUTPUT}"
GUIDED_DIAGNOSTIC_DIR="$(printf '%s\n' "${GUIDED_DIAGNOSTIC_OUTPUT}" | extract_study_dir)"

VALIDATION_OUTPUT="$(
  run_py 'from linearity_analysis.ardupilot_state_evolution_validation import main; main()' \
    --stabilize-baseline "${STABILIZE_BASELINE_DIR}" \
    --stabilize-diagnostic "${STABILIZE_DIAGNOSTIC_DIR}" \
    --guided-baseline "${GUIDED_BASELINE_DIR}" \
    --guided-diagnostic "${GUIDED_DIAGNOSTIC_DIR}"
)"
printf '%s\n' "${VALIDATION_OUTPUT}"
VALIDATION_DIR="$(printf '%s\n' "${VALIDATION_OUTPUT}" | extract_study_dir)"

echo "validation_dir=${VALIDATION_DIR}"
