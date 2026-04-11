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
            "linearity_compare_schemas = linearity_analysis.linearity_compare_schemas:main",
            "linearity_contract_audit = linearity_analysis.contract_audit:main",
            "linearity_matrix_gallery = linearity_analysis.matrix_gallery:main",
            "linearity_milestone_report = linearity_analysis.milestone_report:main",
            "linearity_prune_artifacts = linearity_analysis.prune_artifacts:main",
            "linearity_stage_checks = linearity_analysis.stage_checks:main",
        ],
    },
)
