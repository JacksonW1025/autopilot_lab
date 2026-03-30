#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_PATH="${ROOT_DIR}/milestone.lock.json"

usage() {
  cat <<'EOF'
Usage: doctor_lab.sh

Check the Dual-Backend M1 environment and report ready/not_ready with remediation hints.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
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

AUTOPILOT_LAB_ROOT="${AUTOPILOT_LAB_ROOT:-$(json_value external_roots.AUTOPILOT_LAB_ROOT)}"
PX4_ROOT="${PX4_ROOT:-$(json_value external_roots.PX4_ROOT)}"
ARDUPILOT_ROOT="${ARDUPILOT_ROOT:-$(json_value external_roots.ARDUPILOT_ROOT)}"

declare -a FAILURES=()

record_failure() {
  FAILURES+=("$1")
}

mapfile -t SYSTEM_COMMANDS < <(json_value system_commands)
for command_name in "${SYSTEM_COMMANDS[@]}"; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    record_failure "missing command: $command_name | remediation: install or add it to PATH"
  fi
done

mapfile -t PYTHON_MODULES < <(json_value python_modules)
for module_name in "${PYTHON_MODULES[@]}"; do
  import_name="$module_name"
  case "$module_name" in
    PyYAML) import_name="yaml" ;;
    pyulog) import_name="pyulog" ;;
  esac
  if ! python3 - "$import_name" <<'PY' >/dev/null 2>&1
import importlib
import sys
importlib.import_module(sys.argv[1])
PY
  then
    record_failure "missing python module: $module_name | remediation: run scripts/bootstrap_lab.sh"
  fi
done

for required_path in "$AUTOPILOT_LAB_ROOT" "$PX4_ROOT" "$ARDUPILOT_ROOT"; do
  if [[ ! -d "$required_path" ]]; then
    record_failure "missing path: $required_path | remediation: clone or mount the expected repository"
  fi
done

if [[ -d "$PX4_ROOT/.git" ]]; then
  current_px4="$(git -C "$PX4_ROOT" rev-parse HEAD 2>/dev/null || true)"
  expected_px4="$(json_value external_revisions.px4)"
  if [[ -n "$current_px4" && "$current_px4" != "$expected_px4" ]]; then
    record_failure "PX4 revision mismatch: $current_px4 != $expected_px4 | remediation: git -C $PX4_ROOT checkout $expected_px4"
  fi
fi

if [[ -d "$ARDUPILOT_ROOT/.git" ]]; then
  current_ardupilot="$(git -C "$ARDUPILOT_ROOT" rev-parse HEAD 2>/dev/null || true)"
  expected_ardupilot="$(json_value external_revisions.ardupilot)"
  if [[ -n "$current_ardupilot" && "$current_ardupilot" != "$expected_ardupilot" ]]; then
    record_failure "ArduPilot revision mismatch: $current_ardupilot != $expected_ardupilot | remediation: git -C $ARDUPILOT_ROOT checkout $expected_ardupilot"
  fi
fi

for config_path in $(json_value canonical_smoke_configs); do
  if [[ ! -f "${ROOT_DIR}/${config_path}" ]]; then
    record_failure "missing canonical config: ${ROOT_DIR}/${config_path} | remediation: restore the config file"
  fi
done

if [[ ! -f "${AUTOPILOT_LAB_ROOT}/install/setup.bash" ]]; then
  record_failure "missing workspace overlay: ${AUTOPILOT_LAB_ROOT}/install/setup.bash | remediation: run scripts/bootstrap_lab.sh"
else
  set +u
  source "${AUTOPILOT_LAB_ROOT}/scripts/autopilot_lab_env.sh" >/dev/null
  set -u
  mapfile -t BACKEND_CLIS < <(json_value backend_clis)
  for cli in "${BACKEND_CLIS[@]}"; do
    if ! command -v "$cli" >/dev/null 2>&1; then
      record_failure "missing backend CLI: $cli | remediation: rebuild the workspace with scripts/bootstrap_lab.sh"
    fi
  done
fi

if [[ ${#FAILURES[@]} -eq 0 ]]; then
  echo "status=ready"
  echo "milestone=$(json_value milestone_id)"
  exit 0
fi

echo "status=not_ready"
echo "milestone=$(json_value milestone_id)"
for failure in "${FAILURES[@]}"; do
  echo "- ${failure}"
done
exit 1
