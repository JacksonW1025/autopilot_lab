#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ANCHOR_DEEP_DIVE=""
IN_DEPTH_ANALYSIS=""
A2_PAIR_TARGET=""
A1_TARGETED_REPRODUCTION=""
OUTPUT_DIR=""

usage() {
  cat <<'EOF'
Usage: run_formal_v2_next_phase_decision.sh [--anchor-deep-dive DIR] [--in-depth-analysis DIR] [--a2-pair-target DIR] [--a1-targeted-reproduction DIR] [--output-dir DIR]

Build the thin Formal V2 next-phase decision layer from latest or explicit derived artifacts.
- auto-discovers the latest anchor deep dive, in-depth analysis, A2 pair-target readiness, and A1 targeted reproduction artifacts
- keeps bucket-first ranking and does not recompute canonical formal conclusions
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --anchor-deep-dive) ANCHOR_DEEP_DIVE="$2"; shift ;;
    --in-depth-analysis) IN_DEPTH_ANALYSIS="$2"; shift ;;
    --a2-pair-target) A2_PAIR_TARGET="$2"; shift ;;
    --a1-targeted-reproduction) A1_TARGETED_REPRODUCTION="$2"; shift ;;
    --output-dir) OUTPUT_DIR="$2"; shift ;;
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

ARGS=()
if [[ -n "${ANCHOR_DEEP_DIVE}" ]]; then
  ARGS+=(--anchor-deep-dive "${ANCHOR_DEEP_DIVE}")
fi
if [[ -n "${IN_DEPTH_ANALYSIS}" ]]; then
  ARGS+=(--in-depth-analysis "${IN_DEPTH_ANALYSIS}")
fi
if [[ -n "${A2_PAIR_TARGET}" ]]; then
  ARGS+=(--a2-pair-target "${A2_PAIR_TARGET}")
fi
if [[ -n "${A1_TARGETED_REPRODUCTION}" ]]; then
  ARGS+=(--a1-targeted-reproduction "${A1_TARGETED_REPRODUCTION}")
fi
if [[ -n "${OUTPUT_DIR}" ]]; then
  ARGS+=(--output-dir "${OUTPUT_DIR}")
fi

ANALYSIS_OUTPUT="$(python3 "${ROOT_DIR}/scripts/analyze_formal_v2_next_phase_decision.py" "${ARGS[@]}")"
printf '%s\n' "${ANALYSIS_OUTPUT}"

STUDY_DIR="$(printf '%s\n' "${ANALYSIS_OUTPUT}" | awk -F= '/^study_dir=/{print $2}' | tail -n 1)"
if [[ -z "${STUDY_DIR}" ]]; then
  echo "study_dir is required" >&2
  exit 1
fi
