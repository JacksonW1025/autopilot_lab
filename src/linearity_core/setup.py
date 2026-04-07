from setuptools import find_packages, setup


package_name = "linearity_core"


setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        (f"share/{package_name}", ["package.xml"]),
    ],
    install_requires=["setuptools", "numpy", "PyYAML", "pymavlink"],
    zip_safe=True,
    maintainer="car",
    maintainer_email="1245080419@qq.com",
    description="Core configuration, dataset, fitting, and reporting helpers for global linearity studies.",
    license="Apache-2.0",
    extras_require={"test": ["pytest"]},
)
