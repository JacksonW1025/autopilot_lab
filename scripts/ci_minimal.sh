#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: ci_minimal.sh

Run the smoke-free M1 regression gate:
- python3 -m pytest -q tests
- python3 -m py_compile for Python files under src/, tests/, scripts/
- scripts/doctor_lab.sh --help
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

cd "${ROOT_DIR}"

python3 -m pytest -q tests

mapfile -t PY_FILES < <(find src tests scripts -type f -name '*.py' | sort)
if [[ ${#PY_FILES[@]} -gt 0 ]]; then
  python3 -m py_compile "${PY_FILES[@]}"
fi

scripts/doctor_lab.sh --help >/dev/null
echo "ci_status=passed"
