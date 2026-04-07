#!/usr/bin/env bash
set -eo pipefail

export AUTOPILOT_LAB_ROOT="${AUTOPILOT_LAB_ROOT:-/home/car/autopilot_lab}"
export PX4_ROOT="${PX4_ROOT:-/home/car/PX4-Autopilot}"
export ARDUPILOT_ROOT="${ARDUPILOT_ROOT:-/home/car/ardupilot}"

set +u
source /opt/ros/humble/setup.bash
if [[ -f "${AUTOPILOT_LAB_ROOT}/install/setup.bash" ]]; then
  source "${AUTOPILOT_LAB_ROOT}/install/setup.bash"
fi
set -u

for pkg_src in \
  "${AUTOPILOT_LAB_ROOT}/src/linearity_core" \
  "${AUTOPILOT_LAB_ROOT}/src/linearity_analysis" \
  "${AUTOPILOT_LAB_ROOT}/src/linearity_study" \
  "${AUTOPILOT_LAB_ROOT}/src/px4_ros2_backend" \
  "${AUTOPILOT_LAB_ROOT}/src/ardupilot_mavlink_backend"
do
  case ":${PYTHONPATH:-}:" in
    *":${pkg_src}:"*) ;;
    *) export PYTHONPATH="${pkg_src}${PYTHONPATH:+:${PYTHONPATH}}" ;;
  esac
done

for pkg_lib in \
  "${AUTOPILOT_LAB_ROOT}/install/linearity_core/lib/linearity_core" \
  "${AUTOPILOT_LAB_ROOT}/install/linearity_analysis/lib/linearity_analysis" \
  "${AUTOPILOT_LAB_ROOT}/install/linearity_study/lib/linearity_study" \
  "${AUTOPILOT_LAB_ROOT}/install/px4_ros2_backend/lib/px4_ros2_backend" \
  "${AUTOPILOT_LAB_ROOT}/install/ardupilot_mavlink_backend/lib/ardupilot_mavlink_backend"
do
  if [[ -d "${pkg_lib}" ]]; then
    export PATH="${pkg_lib}:${PATH}"
  fi
done
