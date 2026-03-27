#!/usr/bin/env bash
set -eo pipefail

export AUTOPILOT_LAB_ROOT="${AUTOPILOT_LAB_ROOT:-/home/car/autopilot_lab}"
export PX4_ROOT="${PX4_ROOT:-/home/car/PX4-Autopilot}"
export ARDUPILOT_ROOT="${ARDUPILOT_ROOT:-/home/car/ardupilot}"

python3 -m pip install --user --upgrade 'empy<4' pymavlink MAVProxy pyulog PyYAML numpy >/dev/null

set +u
source /opt/ros/humble/setup.bash
if [[ -f "${AUTOPILOT_LAB_ROOT}/install/setup.bash" ]]; then
  source "${AUTOPILOT_LAB_ROOT}/install/setup.bash"
fi
set -u

for pkg_lib in \
  "${AUTOPILOT_LAB_ROOT}/install/fep_research/lib/fep_research" \
  "${AUTOPILOT_LAB_ROOT}/install/ardupilot_mavlink_backend/lib/ardupilot_mavlink_backend"
do
  if [[ -d "${pkg_lib}" ]]; then
    export PATH="${pkg_lib}:${PATH}"
  fi
done

echo "AUTOPILOT_LAB_ROOT=${AUTOPILOT_LAB_ROOT}"
echo "PX4_ROOT=${PX4_ROOT}"
echo "ARDUPILOT_ROOT=${ARDUPILOT_ROOT}"
