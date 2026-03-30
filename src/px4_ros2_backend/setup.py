from setuptools import find_packages, setup


package_name = "px4_ros2_backend"


setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        (f"share/{package_name}", ["package.xml"]),
    ],
    install_requires=["setuptools", "numpy", "PyYAML", "pyulog"],
    zip_safe=True,
    maintainer="car",
    maintainer_email="1245080419@qq.com",
    description="PX4 ROS 2 backend for autopilot_lab.",
    license="Apache-2.0",
    extras_require={"test": ["pytest"]},
    entry_points={
        "console_scripts": [
            "px4_experiment_runner = px4_ros2_backend.experiment_runner:main",
            "px4_matrix_runner = px4_ros2_backend.matrix_runner:main",
            "px4_rate_injector = px4_ros2_backend.rate_injector:main",
            "px4_analysis_runner = px4_ros2_backend.analysis_runner:main",
        ],
    },
)
