#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASELINE_STUDY=""
DIAGNOSTIC_STUDY=""
OUTPUT_ROOT=""

usage() {
  cat <<'EOF'
Usage: run_px4_a1_target_scout.sh [--baseline-study DIR] [--diagnostic-study DIR] [--output-root DIR]

Run the PX4 A1 target-scout analysis on canonical or user-provided study artifacts.
- fixed combo: full_augmented -> next_raw_state | ols_affine | stratified
- fixed scope: family scouting only, no new capture
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --baseline-study) BASELINE_STUDY="$2"; shift ;;
    --diagnostic-study) DIAGNOSTIC_STUDY="$2"; shift ;;
    --output-root) OUTPUT_ROOT="$2"; shift ;;
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

ARGS=()
if [[ -n "${BASELINE_STUDY}" ]]; then
  ARGS+=(--baseline-study "${BASELINE_STUDY}")
fi
if [[ -n "${DIAGNOSTIC_STUDY}" ]]; then
  ARGS+=(--diagnostic-study "${DIAGNOSTIC_STUDY}")
fi
if [[ -n "${OUTPUT_ROOT}" ]]; then
  ARGS+=(--output-root "${OUTPUT_ROOT}")
fi

ANALYSIS_OUTPUT="$(run_py 'from linearity_analysis.px4_a1_target_scout import main; main()' "${ARGS[@]}")"
printf '%s\n' "${ANALYSIS_OUTPUT}"

STUDY_DIR="$(printf '%s\n' "${ANALYSIS_OUTPUT}" | awk -F= '/^study_dir=/{print $2}' | tail -n 1)"
if [[ -z "${STUDY_DIR}" ]]; then
  echo "study_dir is required" >&2
  exit 1
fi
