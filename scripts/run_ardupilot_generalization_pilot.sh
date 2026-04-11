#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"${ROOT_DIR}/scripts/run_ardupilot_generalization_baseline.sh" --stage pilot "$@"
"${ROOT_DIR}/scripts/run_ardupilot_generalization_diagnostic.sh" --stage pilot "$@"
