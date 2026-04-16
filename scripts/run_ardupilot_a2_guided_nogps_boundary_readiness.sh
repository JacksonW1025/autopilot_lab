#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VEHICLE="ArduCopter"
FRAME="quad"
SKIP_SITL=0
SKIP_CAPTURE=0
MATRIX_DIR=""
OUTPUT_ROOT=""
SCENARIOS=""
ACCEPTED_TARGET=5
MAX_ATTEMPTS_PER_CONFIG=10

usage() {
  cat <<'EOF'
Usage: run_ardupilot_a2_guided_nogps_boundary_readiness.sh [--vehicle ArduCopter] [--frame quad]
                                                           [--skip-sitl] [--skip-capture --matrix-dir DIR]
                                                           [--output-root DIR]
                                                           [--scenarios nominal,throttle_biased]

Run the narrow ArduPilot A2 GUIDED_NOGPS boundary-readiness regime scout.
- fixed scope: GUIDED_NOGPS only, throttle only, pulse_train only
- fixed matrix: nominal/throttle_biased x micro/probe/confirm
- fixed capture policy: repeat=1, accepted-target=5, max-attempts-per-config=10
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --vehicle) VEHICLE="$2"; shift ;;
    --frame) FRAME="$2"; shift ;;
    --skip-sitl) SKIP_SITL=1 ;;
    --skip-capture) SKIP_CAPTURE=1 ;;
    --matrix-dir) MATRIX_DIR="$2"; shift ;;
    --output-root) OUTPUT_ROOT="$2"; shift ;;
    --scenarios) SCENARIOS="$2"; shift ;;
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

TMP_CONFIG_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_CONFIG_DIR}"' EXIT

GENERATED_CONFIGS="$(
  ROOT_DIR="${ROOT_DIR}" TMP_CONFIG_DIR="${TMP_CONFIG_DIR}" SCENARIOS="${SCENARIOS}" python3 - <<'PY'
import copy
import os
from pathlib import Path

import yaml

root = Path(os.environ["ROOT_DIR"])
out_dir = Path(os.environ["TMP_CONFIG_DIR"])
scenario_filter_raw = os.environ.get("SCENARIOS", "").strip()
scenario_filter = {item.strip() for item in scenario_filter_raw.split(",") if item.strip()}
base_path = root / "configs/studies/ardupilot_diagnostic_guided_nogps_throttle_capture.yaml"
payload = yaml.safe_load(base_path.read_text(encoding="utf-8"))
base_seed = int(payload["seed"])
specs = [
    ("nominal", "micro", 0.02, 0.0, 5, 0.35, 0.95),
    ("nominal", "probe", 0.05, 0.0, 5, 0.35, 0.95),
    ("nominal", "confirm", 0.10, 0.0, 5, 0.35, 0.95),
    ("throttle_biased", "micro", 0.02, 0.04, 5, 0.35, 0.95),
    ("throttle_biased", "probe", 0.05, 0.04, 5, 0.35, 0.95),
    ("throttle_biased", "confirm", 0.10, 0.04, 5, 0.35, 0.95),
]

for index, (scenario, tier, amplitude, bias, pulse_count, pulse_width_s, pulse_gap_s) in enumerate(specs):
    if scenario_filter and scenario not in scenario_filter:
        continue
    item = copy.deepcopy(payload)
    item["study_name"] = f"ardupilot_a2_guided_nogps_boundary_readiness_{scenario}_{tier}"
    item["scenario"] = scenario
    item["config_profile"] = f"ardupilot_a2_guided_nogps_boundary_readiness_{scenario}_{tier}"
    item["seed"] = base_seed + index
    item["axis"] = "throttle"
    item["profile_type"] = "pulse_train"
    item["amplitude"] = amplitude
    item["bias"] = bias
    item["perturbation_strategy"] = "a2_boundary_regime_scout_v1"
    item.setdefault("extras", {})
    item["extras"]["amplitude_tier"] = tier
    item["extras"]["readiness_scenario"] = scenario
    item["extras"]["profile_family"] = "pulse_train"
    item["extras"]["readiness_protocol_version"] = "v4_guided_nogps"
    item["extras"]["pulse_count"] = pulse_count
    item["extras"]["pulse_width_s"] = pulse_width_s
    item["extras"]["pulse_gap_s"] = pulse_gap_s
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
    "${CONFIG_ARGS[@]}"
    --repeat 1
    --accepted-target "${ACCEPTED_TARGET}"
    --max-attempts-per-config "${MAX_ATTEMPTS_PER_CONFIG}"
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
ANALYSIS_ARGS=(--runs-manifest "${RUNS_MANIFEST}")
if [[ -n "${OUTPUT_ROOT}" ]]; then
  ANALYSIS_ARGS+=(--output-root "${OUTPUT_ROOT}")
fi

ANALYSIS_OUTPUT="$(run_py 'from linearity_analysis.ardupilot_a2_boundary_readiness import main; main()' "${ANALYSIS_ARGS[@]}")"
printf '%s\n' "${ANALYSIS_OUTPUT}"

STUDY_DIR="$(printf '%s\n' "${ANALYSIS_OUTPUT}" | awk -F= '/^study_dir=/{print $2}' | tail -n 1)"
if [[ -z "${STUDY_DIR}" ]]; then
  echo "study_dir is required" >&2
  exit 1
fi
