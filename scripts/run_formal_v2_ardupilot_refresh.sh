#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="${ROOT_DIR}/docs"
GENERALIZATION_MAX_ATTEMPTS=12
TARGETED_MAX_ATTEMPTS=12
PRUNE_OUTPUT_DIR="${ROOT_DIR}/metadata/artifact_prune/formal_v2"
APPLY_PRUNE=0

usage() {
  cat <<'EOF'
Usage: run_formal_v2_ardupilot_refresh.sh [--generalization-max-attempts N] [--targeted-max-attempts N]
                                          [--docs-dir DIR] [--prune-output-dir DIR] [--apply-prune]
                                          [extra args forwarded to capture scripts]

Runs the approved Formal V2 refresh workflow:
1. reuse latest PX4 generalization full studies
2. rerun ArduPilot generalization full
3. rerun ArduPilot targeted state-evolution validation line
4. rebuild compare + milestone docs
5. refresh curated heatmaps
6. generate prune manifests
7. optionally apply prune
EOF
}

FORWARDED_ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --generalization-max-attempts) GENERALIZATION_MAX_ATTEMPTS="$2"; shift ;;
    --targeted-max-attempts) TARGETED_MAX_ATTEMPTS="$2"; shift ;;
    --docs-dir) DOCS_DIR="$2"; shift ;;
    --prune-output-dir) PRUNE_OUTPUT_DIR="$2"; shift ;;
    --apply-prune) APPLY_PRUNE=1 ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      FORWARDED_ARGS+=("$1")
      ;;
  esac
  shift
done

run_py() {
  local module_expr="$1"
  shift
  python3 -c "$module_expr" "$@"
}

set +u
source /opt/ros/humble/setup.bash
source "${ROOT_DIR}/scripts/autopilot_lab_env.sh" >/dev/null
set -u

latest_study_dir() {
  run_py 'from linearity_analysis.stage_checks import latest_study_dir_by_name; import sys; study = latest_study_dir_by_name(sys.argv[1]); print(study if study else "")' "$1"
}

require_study_dir() {
  local study_name="$1"
  local study_dir
  study_dir="$(latest_study_dir "${study_name}")"
  if [[ -z "${study_dir}" ]]; then
    echo "missing required study: ${study_name}" >&2
    exit 1
  fi
  printf '%s\n' "${study_dir}"
}

PX4_BASELINE_DIR="$(require_study_dir "px4_real_generalization_ablation")"
PX4_DIAGNOSTIC_DIR="$(require_study_dir "px4_generalization_diagnostic_matrix")"

ARDUPILOT_FULL_OUTPUT="$(bash "${ROOT_DIR}/scripts/run_ardupilot_generalization_full.sh" --max-attempts-per-config "${GENERALIZATION_MAX_ATTEMPTS}" "${FORWARDED_ARGS[@]}")"
printf '%s\n' "${ARDUPILOT_FULL_OUTPUT}"
ARDUPILOT_BASELINE_DIR="$(require_study_dir "ardupilot_real_generalization_ablation")"
ARDUPILOT_DIAGNOSTIC_DIR="$(require_study_dir "ardupilot_generalization_diagnostic_matrix")"

TARGETED_OUTPUT="$(bash "${ROOT_DIR}/scripts/run_ardupilot_state_evolution_validation_full.sh" --max-attempts-per-config "${TARGETED_MAX_ATTEMPTS}" "${FORWARDED_ARGS[@]}")"
printf '%s\n' "${TARGETED_OUTPUT}"
VALIDATION_DIR="$(require_study_dir "ardupilot_state_evolution_validation")"

MILESTONE_OUTPUT="$(
  run_py 'from linearity_analysis.milestone_report import main; main()' \
    --px4-baseline "${PX4_BASELINE_DIR}" \
    --ardupilot-baseline "${ARDUPILOT_BASELINE_DIR}" \
    --px4-diagnostic "${PX4_DIAGNOSTIC_DIR}" \
    --ardupilot-diagnostic "${ARDUPILOT_DIAGNOSTIC_DIR}" \
    --state-evolution-validation "${VALIDATION_DIR}" \
    --docs-dir "${DOCS_DIR}"
)"
printf '%s\n' "${MILESTONE_OUTPUT}"

COMPARE_DIR="$(printf '%s\n' "${MILESTONE_OUTPUT}" | awk -F= '/^compare_dir=/{print $2}' | tail -n 1)"
if [[ -z "${COMPARE_DIR}" ]]; then
  COMPARE_DIR="$(require_study_dir "px4_vs_ardupilot_compare")"
fi

python3 "${ROOT_DIR}/scripts/refresh_formal_v2_heatmaps.py" \
  "${PX4_BASELINE_DIR}" \
  "${PX4_DIAGNOSTIC_DIR}" \
  "${ARDUPILOT_BASELINE_DIR}" \
  "${ARDUPILOT_DIAGNOSTIC_DIR}" \
  "${VALIDATION_DIR}"

python3 "${ROOT_DIR}/scripts/refresh_formal_v2_static_docs.py" \
  "${PX4_BASELINE_DIR}" \
  "${PX4_DIAGNOSTIC_DIR}" \
  "${ARDUPILOT_BASELINE_DIR}" \
  "${ARDUPILOT_DIAGNOSTIC_DIR}" \
  "${VALIDATION_DIR}"

PRUNE_ARGS=(--output-dir "${PRUNE_OUTPUT_DIR}")
if [[ ${APPLY_PRUNE} -eq 1 ]]; then
  PRUNE_ARGS+=(--apply)
fi
python3 "${ROOT_DIR}/scripts/prune_artifacts.py" "${PRUNE_ARGS[@]}"

echo "px4_baseline_dir=${PX4_BASELINE_DIR}"
echo "px4_diagnostic_dir=${PX4_DIAGNOSTIC_DIR}"
echo "ardupilot_baseline_dir=${ARDUPILOT_BASELINE_DIR}"
echo "ardupilot_diagnostic_dir=${ARDUPILOT_DIAGNOSTIC_DIR}"
echo "validation_dir=${VALIDATION_DIR}"
echo "compare_dir=${COMPARE_DIR}"
echo "docs_dir=${DOCS_DIR}"
echo "prune_output_dir=${PRUNE_OUTPUT_DIR}"
