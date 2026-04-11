#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VEHICLE="ArduCopter"
FRAME="quad"
REPEAT=3
SKIP_SITL=0
SKIP_CAPTURE=0
MATRIX_DIR=""

usage() {
  cat <<'EOF'
Usage: run_ardupilot_guided_nogps_smoke.sh [--vehicle ArduCopter] [--frame quad] [--repeat 3]
                                           [--skip-sitl] [--skip-capture --matrix-dir DIR]
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

if [[ $SKIP_CAPTURE -eq 0 ]]; then
  MATRIX_ARGS=(
    --vehicle "${VEHICLE}"
    --frame "${FRAME}"
    --config "${ROOT_DIR}/configs/studies/ardupilot_real_nominal_guided_nogps_capture.yaml"
    --repeat "${REPEAT}"
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

ROOT_DIR="${ROOT_DIR}" MATRIX_DIR="${MATRIX_DIR}" python3 - <<'PY'
import os
from pathlib import Path

from linearity_core.io import read_rows_csv, write_json
from linearity_core.study_artifacts import build_guided_mode_smoke_payload, render_guided_mode_smoke_markdown

matrix_dir = Path(os.environ["MATRIX_DIR"]).expanduser().resolve()
runs_manifest = matrix_dir / "runs.csv"
rows = read_rows_csv(runs_manifest)
run_dirs = [Path(row["artifact_dir"]).expanduser().resolve() for row in rows if row.get("artifact_dir")]
payload = build_guided_mode_smoke_payload(run_dirs, target_mode="GUIDED_NOGPS", target_consecutive_runs=3)

reports_dir = matrix_dir / "reports"
summary_dir = matrix_dir / "summary"
reports_dir.mkdir(parents=True, exist_ok=True)
summary_dir.mkdir(parents=True, exist_ok=True)
(reports_dir / "guided_nogps_smoke.md").write_text(render_guided_mode_smoke_markdown(payload), encoding="utf-8")
write_json(summary_dir / "guided_nogps_smoke.json", payload)
print(f"guided_nogps_smoke_passed={str(bool(payload['passed'])).lower()}")
raise SystemExit(0 if payload["passed"] else 1)
PY
