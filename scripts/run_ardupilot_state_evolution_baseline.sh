#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VEHICLE="ArduCopter"
FRAME="quad"
MODE=""
STAGE="pilot"
ACCEPTED_TARGET=""
MAX_ATTEMPTS_PER_CONFIG=""
SKIP_SITL=0
SKIP_CAPTURE=0
MATRIX_DIR=""

usage() {
  cat <<'EOF'
Usage: run_ardupilot_state_evolution_baseline.sh --mode stabilize|guided_nogps [--stage pilot|full]
                                                 [--vehicle ArduCopter] [--frame quad]
                                                 [--accepted-target N] [--max-attempts-per-config N]
                                                 [--skip-sitl] [--skip-capture --matrix-dir DIR]

Run the Formal V2 ArduPilot mode-isolated state-evolution baseline.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode) MODE="$2"; shift ;;
    --stage) STAGE="$2"; shift ;;
    --vehicle) VEHICLE="$2"; shift ;;
    --frame) FRAME="$2"; shift ;;
    --accepted-target) ACCEPTED_TARGET="$2"; shift ;;
    --max-attempts-per-config) MAX_ATTEMPTS_PER_CONFIG="$2"; shift ;;
    --skip-sitl) SKIP_SITL=1 ;;
    --skip-capture) SKIP_CAPTURE=1 ;;
    --matrix-dir) MATRIX_DIR="$2"; shift ;;
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

case "${MODE}" in
  stabilize)
    BASE_CAPTURE="${ROOT_DIR}/configs/studies/ardupilot_real_nominal_stabilize_capture.yaml"
    MODE_UPPER="STABILIZE"
    ;;
  guided_nogps)
    BASE_CAPTURE="${ROOT_DIR}/configs/studies/ardupilot_real_nominal_guided_nogps_capture.yaml"
    MODE_UPPER="GUIDED_NOGPS"
    ;;
  *)
    echo "--mode must be stabilize or guided_nogps" >&2
    exit 2
    ;;
esac

case "${STAGE}" in
  pilot|full) ;;
  *)
    echo "--stage must be pilot or full" >&2
    exit 2
    ;;
esac

if [[ -z "${ACCEPTED_TARGET}" ]]; then
  if [[ "${STAGE}" == "pilot" ]]; then
    ACCEPTED_TARGET=8
  else
    ACCEPTED_TARGET=10
  fi
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

run_stage_check() {
  run_py 'from linearity_analysis.stage_checks import main; main()' "$@"
}

TMP_CONFIG_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_CONFIG_DIR}"' EXIT

GENERATED_CONFIGS="$(
  ROOT_DIR="${ROOT_DIR}" TMP_CONFIG_DIR="${TMP_CONFIG_DIR}" BASE_CAPTURE="${BASE_CAPTURE}" MODE="${MODE}" python3 - <<'PY'
import copy
import os
from pathlib import Path

import yaml

root = Path(os.environ["ROOT_DIR"])
out_dir = Path(os.environ["TMP_CONFIG_DIR"])
base_path = Path(os.environ["BASE_CAPTURE"])
mode_label = os.environ["MODE"]
payload = yaml.safe_load(base_path.read_text(encoding="utf-8"))
base_amplitude = float(payload["amplitude"])
base_seed = int(payload["seed"])
input_type = str(payload["input_type"]).strip().lower()
multi_broad_phases = {
    "roll": [0.0, 0.9, 1.8],
    "pitch": [0.4, 1.3, 2.2],
    "yaw": [0.7, 1.6, 2.5],
    "throttle": [1.1, 2.0, 2.9],
}
scenario_specs = [
    (
        "nominal",
        {
            "amplitude_scale": 1.0,
            "frequencies": {
                "roll": [0.13, 0.37, 0.71],
                "pitch": [0.17, 0.43, 0.89],
                "yaw": [0.11, 0.29, 0.61],
                "throttle": [0.19, 0.47, 0.97],
            },
            "throttle_scale": 1.0,
            "throttle_bias": 0.0,
            "manual_throttle_scale": 0.30,
            "manual_throttle_bias": 0.65,
        },
    ),
    (
        "dynamic",
        {
            "amplitude_scale": 1.35,
            "frequencies": {
                "roll": [0.23, 0.61, 1.07],
                "pitch": [0.27, 0.67, 1.19],
                "yaw": [0.19, 0.49, 0.91],
                "throttle": [0.31, 0.79, 1.33],
            },
            "throttle_scale": 1.0,
            "throttle_bias": 0.0,
            "manual_throttle_scale": 0.36,
            "manual_throttle_bias": 0.65,
        },
    ),
    (
        "throttle_biased",
        {
            "amplitude_scale": 1.0,
            "frequencies": {
                "roll": [0.13, 0.37, 0.71],
                "pitch": [0.17, 0.43, 0.89],
                "yaw": [0.11, 0.29, 0.61],
                "throttle": [0.19, 0.47, 0.97],
            },
            "throttle_scale": 1.2,
            "throttle_bias": 0.04,
            "manual_throttle_scale": 0.30,
            "manual_throttle_bias": 0.68,
        },
    ),
]

for scenario_index, (scenario_name, spec) in enumerate(scenario_specs):
    item = copy.deepcopy(payload)
    item["study_name"] = f"ardupilot_state_evolution_{mode_label}_{scenario_name}_baseline_capture"
    item["scenario"] = scenario_name
    item["config_profile"] = f"ardupilot_state_evolution_{mode_label}_{scenario_name}_baseline"
    item["seed"] = base_seed + scenario_index * 100
    item["profile_type"] = "multi_broad"
    item["perturbation_strategy"] = "generalization_multi_broad"
    item["amplitude"] = round(base_amplitude * float(spec["amplitude_scale"]), 6)
    extras = dict(item.get("extras", {}) or {})
    nominal_throttle = float(extras.get("throttle_amplitude", extras.get("thrust_delta", 0.12 if input_type == "manual" else 0.10)))
    extras["multi_broad_frequencies_hz"] = spec["frequencies"]
    extras["multi_broad_phases_rad"] = multi_broad_phases
    if input_type == "manual":
        extras["throttle_amplitude"] = round(nominal_throttle * float(spec["throttle_scale"]), 6)
        extras["ardupilot_manual_throttle_scale"] = float(spec["manual_throttle_scale"])
        extras["ardupilot_manual_throttle_bias"] = float(spec["manual_throttle_bias"])
    else:
        extras["thrust_delta"] = round(nominal_throttle * float(spec["throttle_scale"]), 6)
    if abs(float(spec.get("throttle_bias", 0.0))) > 0.0:
        extras["multi_broad_axis_bias"] = {"throttle": float(spec["throttle_bias"])}
    else:
        extras.pop("multi_broad_axis_bias", None)
    item["extras"] = extras
    output_path = out_dir / f"{item['study_name']}.yaml"
    output_path.write_text(yaml.safe_dump(item, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(output_path)
PY
)"

PLAN_PATH="${TMP_CONFIG_DIR}/ablation_plan.yaml"
ANALYSIS_CONFIG_PATH="${TMP_CONFIG_DIR}/analysis.yaml"
ROOT_DIR="${ROOT_DIR}" MODE="${MODE}" MODE_UPPER="${MODE_UPPER}" TMP_CONFIG_DIR="${TMP_CONFIG_DIR}" python3 - <<'PY'
import os
from pathlib import Path

import yaml

root = Path(os.environ["ROOT_DIR"])
tmp_dir = Path(os.environ["TMP_CONFIG_DIR"])
mode_label = os.environ["MODE"]
mode_upper = os.environ["MODE_UPPER"]
plan = yaml.safe_load((root / "configs/ablations/ardupilot_state_evolution_targeted_baseline.yaml").read_text(encoding="utf-8"))
plan["output_study_name"] = f"ardupilot_state_evolution_{mode_label}_baseline"
(tmp_dir / "ablation_plan.yaml").write_text(yaml.safe_dump(plan, sort_keys=False, allow_unicode=True), encoding="utf-8")
analysis = yaml.safe_load((root / "configs/studies/ardupilot_state_evolution_targeted_baseline_analysis.yaml").read_text(encoding="utf-8"))
analysis["study_name"] = f"ardupilot_state_evolution_{mode_label}_baseline_analysis"
analysis["flight_mode"] = mode_upper
analysis["config_profile"] = f"ardupilot_state_evolution_{mode_label}_baseline_analysis"
analysis["ablation_plan"] = str(tmp_dir / "ablation_plan.yaml")
(tmp_dir / "analysis.yaml").write_text(yaml.safe_dump(analysis, sort_keys=False, allow_unicode=True), encoding="utf-8")
PY

CONFIG_ARGS=()
CONFIG_NAMES=()
while IFS= read -r config_path; do
  [[ -n "${config_path}" ]] || continue
  CONFIG_ARGS+=(--config "${config_path}")
  CONFIG_NAMES+=(--config-name "$(basename "${config_path}")")
done <<< "${GENERATED_CONFIGS}"

if [[ $SKIP_CAPTURE -eq 0 ]]; then
  MATRIX_ARGS=(
    --vehicle "${VEHICLE}"
    --frame "${FRAME}"
    "${CONFIG_ARGS[@]}"
    --repeat 1
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
  ANALYSIS_OUTPUT="$(ros2 run linearity_analysis linearity_compare_schemas \
    --config "${ANALYSIS_CONFIG_PATH}" \
    --plan "${PLAN_PATH}" \
    --runs-manifest "${RUNS_MANIFEST}")"
else
  ANALYSIS_OUTPUT="$(run_py 'from linearity_analysis.linearity_compare_schemas import main; main()' \
    --config "${ANALYSIS_CONFIG_PATH}" \
    --plan "${PLAN_PATH}" \
    --runs-manifest "${RUNS_MANIFEST}")"
fi
printf '%s\n' "${ANALYSIS_OUTPUT}"

STUDY_DIR="$(printf '%s\n' "${ANALYSIS_OUTPUT}" | awk -F= '/^study_dir=/{print $2}' | tail -n 1)"
if [[ -z "${STUDY_DIR}" ]]; then
  echo "study_dir is required" >&2
  exit 1
fi

run_stage_check full-baseline \
  --matrix-dir "${MATRIX_DIR}" \
  --study-dir "${STUDY_DIR}" \
  "${CONFIG_NAMES[@]}" \
  --accepted-target "${ACCEPTED_TARGET}" \
  --required-path reports/scenario_generalization.md \
  --required-path summary/scenario_generalization.json \
  --required-path reports/scenario_holdout.md \
  --required-path summary/scenario_holdout.json \
  --required-path reports/state_evolution_audit.md \
  --required-path summary/state_evolution_audit.json \
  --required-path reports/sparsity_overlap.md \
  --required-path summary/sparsity_overlap.json

echo "matrix_dir=${MATRIX_DIR}"
echo "study_dir=${STUDY_DIR}"
