#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORLD="default"
STAGE="pilot"
SKIP_CAPTURE=0
MATRIX_DIR=""
ANALYSIS_CONFIG="${ROOT_DIR}/configs/studies/px4_generalization_diagnostic_matrix_analysis.yaml"
ABLATION_PLAN="${ROOT_DIR}/configs/ablations/px4_generalization_diagnostic_matrix.yaml"

usage() {
  cat <<'EOF'
Usage: run_px4_generalization_diagnostic.sh [--stage pilot|full] [--world default]
                                            [--skip-capture --matrix-dir DIR]
                                            [--analysis-config PATH] [--plan PATH]

Run the PX4 generalization diagnostic matrix.
- pilot: nominal sweep controls + alternating throttle on nominal/throttle_biased
- full: pilot set plus dynamic random attitude injections
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --stage) STAGE="$2"; shift ;;
    --world) WORLD="$2"; shift ;;
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

case "${STAGE}" in
  pilot|full) ;;
  *)
    echo "--stage must be pilot or full" >&2
    exit 2
    ;;
esac

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
  ROOT_DIR="${ROOT_DIR}" TMP_CONFIG_DIR="${TMP_CONFIG_DIR}" STAGE="${STAGE}" python3 - <<'PY'
import copy
import os
from pathlib import Path

import yaml

root = Path(os.environ["ROOT_DIR"])
out_dir = Path(os.environ["TMP_CONFIG_DIR"])
stage = os.environ["STAGE"]
axis_paths = [
    root / "configs/studies/px4_diagnostic_posctl_axis_capture.yaml",
    root / "configs/studies/px4_diagnostic_offboard_attitude_axis_capture.yaml",
]
throttle_paths = [
    root / "configs/studies/px4_diagnostic_posctl_throttle_capture.yaml",
    root / "configs/studies/px4_diagnostic_offboard_attitude_throttle_capture.yaml",
]
axes = ("roll", "pitch", "yaw")
tiers = (("small", 0.5), ("medium", 1.0), ("large", 1.5))

for base_index, base_path in enumerate(axis_paths):
    payload = yaml.safe_load(base_path.read_text(encoding="utf-8"))
    base_amplitude = float(payload["amplitude"])
    base_seed = int(payload["seed"])
    mode_label = str(payload["flight_mode"]).strip().lower()
    for axis_index, axis in enumerate(axes):
        for tier_index, (tier_name, factor) in enumerate(tiers):
            sweep_item = copy.deepcopy(payload)
            sweep_item["study_name"] = f"px4_generalization_{mode_label}_nominal_sweep_{axis}_{tier_name}"
            sweep_item["scenario"] = "nominal"
            sweep_item["config_profile"] = f"px4_generalization_{mode_label}_nominal_sweep_{axis}_{tier_name}"
            sweep_item["seed"] = base_seed + base_index * 1000 + axis_index * 100 + tier_index
            sweep_item["axis"] = axis
            sweep_item["amplitude"] = round(base_amplitude * factor, 6)
            sweep_item["profile_type"] = "sweep"
            sweep_item["perturbation_strategy"] = "generalization_diagnostic"
            sweep_item.setdefault("extras", {})
            sweep_item["extras"]["amplitude_tier"] = tier_name
            sweep_item["extras"]["amplitude_factor"] = factor
            sweep_item["extras"]["profile_family"] = "sweep_control"
            output_path = out_dir / f"{sweep_item['study_name']}.yaml"
            output_path.write_text(yaml.safe_dump(sweep_item, sort_keys=False, allow_unicode=True), encoding="utf-8")
            print(output_path)

            if stage != "full":
                continue
            random_item = copy.deepcopy(payload)
            random_item["study_name"] = f"px4_generalization_{mode_label}_dynamic_random_{axis}_{tier_name}"
            random_item["scenario"] = "dynamic"
            random_item["config_profile"] = f"px4_generalization_{mode_label}_dynamic_random_{axis}_{tier_name}"
            random_item["seed"] = base_seed + 5000 + base_index * 1000 + axis_index * 100 + tier_index
            random_item["axis"] = axis
            random_item["amplitude"] = round(base_amplitude * 1.35 * factor, 6)
            random_item["profile_type"] = "random"
            random_item["perturbation_strategy"] = "generalization_diagnostic"
            random_item["takeoff_altitude_m"] = 2.0
            random_item["min_profile_clearance_m"] = 0.40
            random_item.setdefault("extras", {})
            random_item["extras"]["amplitude_tier"] = tier_name
            random_item["extras"]["amplitude_factor"] = factor
            random_item["extras"]["profile_family"] = "dynamic_random"
            random_item["extras"]["random_interval_s"] = 0.30
            output_path = out_dir / f"{random_item['study_name']}.yaml"
            output_path.write_text(yaml.safe_dump(random_item, sort_keys=False, allow_unicode=True), encoding="utf-8")
            print(output_path)

for base_index, base_path in enumerate(throttle_paths):
    payload = yaml.safe_load(base_path.read_text(encoding="utf-8"))
    base_amplitude = float(payload["amplitude"])
    base_seed = int(payload["seed"])
    mode_label = str(payload["flight_mode"]).strip().lower()
    for scenario_index, scenario_name in enumerate(("nominal", "throttle_biased")):
        for tier_index, (tier_name, factor) in enumerate(tiers):
            item = copy.deepcopy(payload)
            item["study_name"] = f"px4_generalization_{mode_label}_{scenario_name}_alternating_throttle_{tier_name}"
            item["scenario"] = scenario_name
            item["config_profile"] = f"px4_generalization_{mode_label}_{scenario_name}_alternating_throttle_{tier_name}"
            item["seed"] = base_seed + base_index * 1000 + scenario_index * 100 + tier_index
            item["axis"] = "throttle"
            amplitude_scale = 1.2 if scenario_name == "throttle_biased" else 1.0
            item["amplitude"] = round(base_amplitude * factor * amplitude_scale, 6)
            item["bias"] = 0.04 if scenario_name == "throttle_biased" else 0.0
            item["profile_type"] = "alternating_pulse_train"
            item["perturbation_strategy"] = "generalization_diagnostic"
            item.setdefault("extras", {})
            item["extras"]["amplitude_tier"] = tier_name
            item["extras"]["amplitude_factor"] = factor
            item["extras"]["profile_family"] = "alternating_pulse_train"
            item["extras"]["pulse_count"] = 5
            item["extras"]["pulse_width_s"] = 0.35
            item["extras"]["pulse_gap_s"] = 0.65
            output_path = out_dir / f"{item['study_name']}.yaml"
            output_path.write_text(yaml.safe_dump(item, sort_keys=False, allow_unicode=True), encoding="utf-8")
            print(output_path)
PY
)"

CONFIG_ARGS=()
CONFIG_NAMES=()
while IFS= read -r config_path; do
  [[ -n "${config_path}" ]] || continue
  CONFIG_ARGS+=(--config "${config_path}")
  CONFIG_NAMES+=(--config-name "$(basename "${config_path}")")
done <<< "${GENERATED_CONFIGS}"

if [[ ${#CONFIG_NAMES[@]} -eq 0 ]]; then
  echo "No diagnostic configs were generated" >&2
  exit 1
fi

if [[ $SKIP_CAPTURE -eq 0 ]]; then
  MATRIX_ARGS=(
    --world "${WORLD}"
    "${CONFIG_ARGS[@]}"
    --repeat 1
    --accepted-target 1
  )
  if command -v ros2 >/dev/null 2>&1 && ros2 pkg prefix px4_ros2_backend >/dev/null 2>&1; then
    MATRIX_OUTPUT="$(ros2 run px4_ros2_backend px4_linearity_matrix "${MATRIX_ARGS[@]}")"
  else
    MATRIX_OUTPUT="$(run_py 'from px4_ros2_backend.linearity_matrix import main; main()' "${MATRIX_ARGS[@]}")"
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

run_stage_check matrix-targets --matrix-dir "${MATRIX_DIR}" "${CONFIG_NAMES[@]}" --accepted-target 1
run_stage_check diagnostic-artifact --study-dir "${STUDY_DIR}"
run_stage_check artifact-paths \
  --study-dir "${STUDY_DIR}" \
  --required-path reports/scenario_generalization.md \
  --required-path summary/scenario_generalization.json

echo "matrix_dir=${MATRIX_DIR}"
echo "study_dir=${STUDY_DIR}"
