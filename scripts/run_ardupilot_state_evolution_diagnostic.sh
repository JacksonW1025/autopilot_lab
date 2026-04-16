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
Usage: run_ardupilot_state_evolution_diagnostic.sh --mode stabilize|guided_nogps [--stage pilot|full]
                                                   [--vehicle ArduCopter] [--frame quad]
                                                   [--accepted-target N] [--max-attempts-per-config N] [--skip-sitl]
                                                   [--skip-capture --matrix-dir DIR]

Run the Formal V2 ArduPilot mode-isolated state-evolution diagnostic matrix.
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
    AXIS_CAPTURE="${ROOT_DIR}/configs/studies/ardupilot_diagnostic_stabilize_axis_capture.yaml"
    THROTTLE_CAPTURE="${ROOT_DIR}/configs/studies/ardupilot_diagnostic_stabilize_throttle_capture.yaml"
    MODE_UPPER="STABILIZE"
    ;;
  guided_nogps)
    AXIS_CAPTURE="${ROOT_DIR}/configs/studies/ardupilot_diagnostic_guided_nogps_axis_capture.yaml"
    THROTTLE_CAPTURE="${ROOT_DIR}/configs/studies/ardupilot_diagnostic_guided_nogps_throttle_capture.yaml"
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
    ACCEPTED_TARGET=1
  else
    ACCEPTED_TARGET=2
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
  ROOT_DIR="${ROOT_DIR}" TMP_CONFIG_DIR="${TMP_CONFIG_DIR}" MODE="${MODE}" AXIS_CAPTURE="${AXIS_CAPTURE}" THROTTLE_CAPTURE="${THROTTLE_CAPTURE}" python3 - <<'PY'
import copy
import os
from pathlib import Path

import yaml

root = Path(os.environ["ROOT_DIR"])
out_dir = Path(os.environ["TMP_CONFIG_DIR"])
mode_label = os.environ["MODE"]
axis_payload = yaml.safe_load(Path(os.environ["AXIS_CAPTURE"]).read_text(encoding="utf-8"))
throttle_payload = yaml.safe_load(Path(os.environ["THROTTLE_CAPTURE"]).read_text(encoding="utf-8"))
axes = ("roll", "pitch", "yaw")
tiers = (("small", 0.5), ("medium", 1.0), ("large", 1.5))

base_amplitude = float(axis_payload["amplitude"])
base_seed = int(axis_payload["seed"])
input_type = str(axis_payload["input_type"]).strip().lower()
for axis_index, axis in enumerate(axes):
    for tier_index, (tier_name, factor) in enumerate(tiers):
        sweep_item = copy.deepcopy(axis_payload)
        sweep_item["study_name"] = f"ardupilot_state_evolution_{mode_label}_nominal_sweep_{axis}_{tier_name}"
        sweep_item["scenario"] = "nominal"
        sweep_item["config_profile"] = f"ardupilot_state_evolution_{mode_label}_nominal_sweep_{axis}_{tier_name}"
        sweep_item["seed"] = base_seed + axis_index * 100 + tier_index
        sweep_item["axis"] = axis
        sweep_item["amplitude"] = round(base_amplitude * factor, 6)
        sweep_item["profile_type"] = "sweep"
        sweep_item["perturbation_strategy"] = "generalization_diagnostic"
        sweep_item.setdefault("extras", {})
        sweep_item["extras"]["amplitude_tier"] = tier_name
        sweep_item["extras"]["profile_family"] = "sweep_control"
        output_path = out_dir / f"{sweep_item['study_name']}.yaml"
        output_path.write_text(yaml.safe_dump(sweep_item, sort_keys=False, allow_unicode=True), encoding="utf-8")
        print(output_path)

        random_item = copy.deepcopy(axis_payload)
        random_item["study_name"] = f"ardupilot_state_evolution_{mode_label}_dynamic_random_{axis}_{tier_name}"
        random_item["scenario"] = "dynamic"
        random_item["config_profile"] = f"ardupilot_state_evolution_{mode_label}_dynamic_random_{axis}_{tier_name}"
        random_item["seed"] = base_seed + 5000 + axis_index * 100 + tier_index
        random_item["axis"] = axis
        random_item["amplitude"] = round(base_amplitude * 1.35 * factor, 6)
        random_item["profile_type"] = "random"
        random_item["perturbation_strategy"] = "generalization_diagnostic"
        random_item.setdefault("extras", {})
        random_item["extras"]["amplitude_tier"] = tier_name
        random_item["extras"]["profile_family"] = "dynamic_random"
        random_item["extras"]["random_interval_s"] = 0.30
        if input_type == "manual":
            random_item["extras"]["ardupilot_manual_throttle_scale"] = 0.36
        output_path = out_dir / f"{random_item['study_name']}.yaml"
        output_path.write_text(yaml.safe_dump(random_item, sort_keys=False, allow_unicode=True), encoding="utf-8")
        print(output_path)

throttle_amplitude = float(throttle_payload["amplitude"])
throttle_seed = int(throttle_payload["seed"])
throttle_input_type = str(throttle_payload["input_type"]).strip().lower()
for tier_index, (tier_name, factor) in enumerate(tiers):
    item = copy.deepcopy(throttle_payload)
    item["study_name"] = f"ardupilot_state_evolution_{mode_label}_throttle_biased_alternating_throttle_{tier_name}"
    item["scenario"] = "throttle_biased"
    item["config_profile"] = f"ardupilot_state_evolution_{mode_label}_throttle_biased_alternating_throttle_{tier_name}"
    item["seed"] = throttle_seed + tier_index
    item["axis"] = "throttle"
    item["amplitude"] = round(throttle_amplitude * factor * 1.2, 6)
    item["bias"] = 0.04
    item["profile_type"] = "alternating_pulse_train"
    item["perturbation_strategy"] = "generalization_diagnostic"
    item.setdefault("extras", {})
    item["extras"]["amplitude_tier"] = tier_name
    item["extras"]["profile_family"] = "alternating_pulse_train"
    item["extras"]["pulse_count"] = 5
    item["extras"]["pulse_width_s"] = 0.35
    item["extras"]["pulse_gap_s"] = 0.65
    if throttle_input_type == "manual":
        item["extras"]["ardupilot_manual_throttle_bias"] = 0.68
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
plan = yaml.safe_load((root / "configs/ablations/ardupilot_state_evolution_targeted_diagnostic.yaml").read_text(encoding="utf-8"))
plan["output_study_name"] = f"ardupilot_state_evolution_{mode_label}_diagnostic"
(tmp_dir / "ablation_plan.yaml").write_text(yaml.safe_dump(plan, sort_keys=False, allow_unicode=True), encoding="utf-8")
analysis = yaml.safe_load((root / "configs/studies/ardupilot_state_evolution_targeted_diagnostic_analysis.yaml").read_text(encoding="utf-8"))
analysis["study_name"] = f"ardupilot_state_evolution_{mode_label}_diagnostic_analysis"
analysis["flight_mode"] = mode_upper
analysis["config_profile"] = f"ardupilot_state_evolution_{mode_label}_diagnostic_analysis"
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

run_stage_check matrix-targets --matrix-dir "${MATRIX_DIR}" "${CONFIG_NAMES[@]}" --accepted-target "${ACCEPTED_TARGET}"
run_stage_check diagnostic-artifact --study-dir "${STUDY_DIR}"
run_stage_check artifact-paths \
  --study-dir "${STUDY_DIR}" \
  --required-path reports/scenario_generalization.md \
  --required-path summary/scenario_generalization.json \
  --required-path reports/state_evolution_audit.md \
  --required-path summary/state_evolution_audit.json \
  --required-path reports/sparsity_overlap.md \
  --required-path summary/sparsity_overlap.json

echo "matrix_dir=${MATRIX_DIR}"
echo "study_dir=${STUDY_DIR}"
