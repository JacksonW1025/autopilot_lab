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

run_stage_check() {
  run_py 'from linearity_analysis.stage_checks import main; main()' "$@"
}

PX4_OUTPUT="$("${ROOT_DIR}/scripts/run_px4_broad_ablation.sh" --accepted-target 5 "$@")"
printf '%s\n' "${PX4_OUTPUT}"

MATRIX_DIR="$(printf '%s\n' "${PX4_OUTPUT}" | awk -F= '/^matrix_dir=/{print $2}' | tail -n 1)"
STUDY_DIR="$(printf '%s\n' "${PX4_OUTPUT}" | awk -F= '/^study_dir=/{print $2}' | tail -n 1)"

if [[ -z "${MATRIX_DIR}" || -z "${STUDY_DIR}" ]]; then
  echo "matrix_dir and study_dir are required" >&2
  exit 1
fi

run_stage_check full-baseline \
  --matrix-dir "${MATRIX_DIR}" \
  --study-dir "${STUDY_DIR}" \
  --config-name px4_real_nominal_posctl_capture.yaml \
  --config-name px4_real_nominal_offboard_attitude_capture.yaml \
  --accepted-target 5
