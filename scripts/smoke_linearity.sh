#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_PATH="${ROOT_DIR}/lab.lock.json"
SKIP_DOCTOR=0

usage() {
  cat <<'EOF'
Usage: smoke_linearity.sh [--skip-doctor]

Run the default backendless global-linearity smoke and generate a report.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

if [[ "${1:-}" == "--skip-doctor" ]]; then
  SKIP_DOCTOR=1
fi

json_value() {
  local expr="$1"
  python3 - "$LOCK_PATH" "$expr" <<'PY'
import json
import sys

path, expr = sys.argv[1], sys.argv[2]
payload = json.load(open(path, "r", encoding="utf-8"))
value = payload
for part in expr.split("."):
    if not part:
        continue
    value = value[part]
if isinstance(value, list):
    for item in value:
        print(item)
else:
    print(value)
PY
}

if [[ $SKIP_DOCTOR -eq 0 ]]; then
  "${ROOT_DIR}/scripts/doctor_lab.sh"
fi

set +u
source "${ROOT_DIR}/scripts/autopilot_lab_env.sh" >/dev/null
set -u

SMOKE_CONFIG="${ROOT_DIR}/$(json_value default_smoke_config)"
if command -v ros2 >/dev/null 2>&1 && ros2 pkg prefix linearity_study >/dev/null 2>&1; then
  ros2 run linearity_study linearity_run_study --config "${SMOKE_CONFIG}"
else
  python3 -c 'from linearity_study.linearity_run_study import main; main()' --config "${SMOKE_CONFIG}"
fi
echo "smoke_status=completed"
