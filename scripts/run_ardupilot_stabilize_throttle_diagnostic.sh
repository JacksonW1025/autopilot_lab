#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VEHICLE="ArduCopter"
FRAME="quad"
REPEAT=3
SKIP_SITL=0
SKIP_CAPTURE=0
MATRIX_DIR=""
ANALYSIS_CONFIG="${ROOT_DIR}/configs/studies/ardupilot_diagnostic_stabilize_throttle_analysis.yaml"
ABLATION_PLAN="${ROOT_DIR}/configs/ablations/ardupilot_diagnostic_stabilize_throttle.yaml"

usage() {
  cat <<'EOF'
Usage: run_ardupilot_stabilize_throttle_diagnostic.sh [--vehicle ArduCopter] [--frame quad] [--repeat 3]
                                                      [--skip-sitl] [--skip-capture --matrix-dir DIR]
                                                      [--analysis-config PATH] [--plan PATH]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --vehicle) VEHICLE="$2"; shift ;;
    --frame) FRAME="$2"; shift ;;
    --repeat) REPEAT="$2"; shift ;;
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

TMP_CONFIG_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_CONFIG_DIR}"' EXIT

GENERATED_CONFIGS="$(
  ROOT_DIR="${ROOT_DIR}" TMP_CONFIG_DIR="${TMP_CONFIG_DIR}" python3 - <<'PY'
import copy
import os
from pathlib import Path

import yaml

root = Path(os.environ["ROOT_DIR"])
out_dir = Path(os.environ["TMP_CONFIG_DIR"])
base_path = root / "configs/studies/ardupilot_diagnostic_stabilize_throttle_capture.yaml"
tiers = (("small", 0.5), ("medium", 1.0), ("large", 1.5))

payload = yaml.safe_load(base_path.read_text(encoding="utf-8"))
base_amplitude = float(payload["amplitude"])
base_study_name = str(payload["study_name"])
base_profile = str(payload["config_profile"])
base_seed = int(payload["seed"])
for tier_index, (label, factor) in enumerate(tiers):
    item = copy.deepcopy(payload)
    item["axis"] = "throttle"
    item["amplitude"] = round(base_amplitude * factor, 6)
    item["study_name"] = f"{base_study_name}__{label}"
    item["config_profile"] = f"{base_profile}__{label}"
    item["seed"] = base_seed + tier_index
    item.setdefault("extras", {})
    item["extras"]["amplitude_tier"] = label
    item["extras"]["amplitude_factor"] = factor
    output_path = out_dir / f"{item['study_name']}.yaml"
    output_path.write_text(yaml.safe_dump(item, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(output_path)
PY
)"

CONFIG_ARGS=()
while IFS= read -r config_path; do
  [[ -n "${config_path}" ]] || continue
  CONFIG_ARGS+=(--config "${config_path}")
done <<< "${GENERATED_CONFIGS}"

if [[ $SKIP_CAPTURE -eq 0 ]]; then
  MATRIX_ARGS=(
    --vehicle "${VEHICLE}"
    --frame "${FRAME}"
    --repeat "${REPEAT}"
    "${CONFIG_ARGS[@]}"
  )
  if [[ $SKIP_SITL -eq 1 ]]; then
    MATRIX_ARGS+=(--skip-sitl)
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
  ANALYSIS_OUTPUT="$(ros2 run linearity_analysis linearity_compare_schemas \
    --config "${ANALYSIS_CONFIG}" \
    --plan "${ABLATION_PLAN}" \
    --runs-manifest "${RUNS_MANIFEST}")"
else
  ANALYSIS_OUTPUT="$(run_py 'from linearity_analysis.linearity_compare_schemas import main; main()' \
    --config "${ANALYSIS_CONFIG}" \
    --plan "${ABLATION_PLAN}" \
    --runs-manifest "${RUNS_MANIFEST}")"
fi
printf '%s\n' "${ANALYSIS_OUTPUT}"

STUDY_DIR="$(printf '%s\n' "${ANALYSIS_OUTPUT}" | awk -F= '/^study_dir=/{print $2}' | tail -n 1)"
if [[ -z "${STUDY_DIR}" ]]; then
  echo "study_dir is required" >&2
  exit 1
fi

run_stage_check diagnostic --study-dir "${STUDY_DIR}"
