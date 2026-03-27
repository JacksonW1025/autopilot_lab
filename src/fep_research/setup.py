from setuptools import find_packages, setup


package_name = "fep_research"


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
    description="Compatibility CLI package for the layered sensitivity study platform.",
    license="Apache-2.0",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "attitude_injector = fep_research.attitude_injector:main",
            "telemetry_recorder = fep_research.telemetry_recorder:main",
            "experiment_runner = fep_research.experiment_runner:main",
            "manual_input_injector = fep_research.manual_input_injector:main",
            "analysis_runner = fep_research.analysis_runner:main",
            "gz_clock_bridge = fep_research.gz_clock_bridge:main",
            "matrix_runner = fep_research.matrix_runner:main",
            "ulog_backfill = fep_research.ulog_backfill:main",
            "identification_dataset_builder = fep_research.identification_dataset_builder:main",
            "ab_fit_runner = fep_research.ab_fit_runner:main",
            "ab_uncertainty_runner = fep_research.ab_uncertainty_runner:main",
        ],
    },
)
