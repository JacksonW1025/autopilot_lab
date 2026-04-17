from setuptools import find_packages, setup


package_name = "linearity_analysis"


setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        (f"share/{package_name}", ["package.xml"]),
    ],
    install_requires=["setuptools", "numpy", "PyYAML", "matplotlib"],
    zip_safe=True,
    maintainer="car",
    maintainer_email="1245080419@qq.com",
    description="Analysis CLIs for autopilot_lab global linearity studies.",
    license="Apache-2.0",
    extras_require={"test": ["pytest"]},
    entry_points={
        "console_scripts": [
            "linearity_analyze = linearity_analysis.linearity_analyze:main",
            "linearity_ardupilot_a2_pair_target_algorithm_evaluation = linearity_analysis.ardupilot_a2_pair_target_algorithm_evaluation:main",
            "linearity_ardupilot_a2_pair_target_live_campaign = linearity_analysis.ardupilot_a2_pair_target_live_campaign:main",
            "linearity_ardupilot_a2_pair_target_live_evaluation = linearity_analysis.ardupilot_a2_pair_target_live_evaluation:main",
            "linearity_ardupilot_a2_guided_nogps_pair_pipeline = linearity_analysis.ardupilot_a2_guided_nogps_pair_pipeline:main",
            "linearity_ardupilot_a2_boundary_readiness = linearity_analysis.ardupilot_a2_boundary_readiness:main",
            "linearity_ardupilot_a2_pair_target_readiness = linearity_analysis.ardupilot_a2_pair_target_readiness:main",
            "linearity_ardupilot_a2_target_scout = linearity_analysis.ardupilot_a2_target_scout:main",
            "linearity_compare_schemas = linearity_analysis.linearity_compare_schemas:main",
            "linearity_contract_audit = linearity_analysis.contract_audit:main",
            "linearity_ardupilot_a2_readiness = linearity_analysis.ardupilot_a2_readiness:main",
            "linearity_matrix_gallery = linearity_analysis.matrix_gallery:main",
            "linearity_milestone_report = linearity_analysis.milestone_report:main",
            "linearity_prune_artifacts = linearity_analysis.prune_artifacts:main",
            "linearity_px4_a1_family_readiness = linearity_analysis.px4_a1_family_readiness:main",
            "linearity_px4_a1_roll_pitch_targeted_reproduction = linearity_analysis.px4_a1_roll_pitch_targeted_reproduction:main",
            "linearity_px4_a1_target_scout = linearity_analysis.px4_a1_target_scout:main",
            "linearity_stage_checks = linearity_analysis.stage_checks:main",
        ],
    },
)
