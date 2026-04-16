#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNS_MANIFEST=""
OUTPUT_ROOT=""

usage() {
  cat <<'EOF'
Usage: run_ardupilot_a2_target_scout.sh --runs-manifest PATH [--output-root DIR]

Run the ArduPilot A2 target-scout analysis on an existing matrix manifest.
- fixed scope: analysis-only, no new capture
- fixed inputs: telemetry/input_trace.csv + telemetry/bin_rcou.csv
- fixed targets: collective floor state, pair imbalance, single-actuator floor state
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --runs-manifest) RUNS_MANIFEST="$2"; shift ;;
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

if [[ -z "${RUNS_MANIFEST}" ]]; then
  echo "--runs-manifest is required" >&2
  exit 1
fi

set +u
source /opt/ros/humble/setup.bash
source "${ROOT_DIR}/scripts/autopilot_lab_env.sh" >/dev/null
set -u

run_py() {
  local module_expr="$1"
  shift
  python3 -c "$module_expr" "$@"
}

ANALYSIS_ARGS=(--runs-manifest "${RUNS_MANIFEST}")
if [[ -n "${OUTPUT_ROOT}" ]]; then
  ANALYSIS_ARGS+=(--output-root "${OUTPUT_ROOT}")
fi

ANALYSIS_OUTPUT="$(run_py 'from linearity_analysis.ardupilot_a2_target_scout import main; main()' "${ANALYSIS_ARGS[@]}")"
printf '%s\n' "${ANALYSIS_OUTPUT}"

STUDY_DIR="$(printf '%s\n' "${ANALYSIS_OUTPUT}" | awk -F= '/^study_dir=/{print $2}' | tail -n 1)"
if [[ -z "${STUDY_DIR}" ]]; then
  echo "study_dir is required" >&2
  exit 1
fi
