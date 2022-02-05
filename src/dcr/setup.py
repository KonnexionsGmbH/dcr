"""Ensures the full and correct installation."""

from setuptools import find_packages
from setuptools import setup

entry_points = (
    {
        "console_scripts": [
            "dcr=dcr.cli:main",
        ],
    },
)
setup(
    author="Konnexions GmbH",
    author_email="info@konnexions.ch",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: Konnexions Public License (KX-PL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
    ],
    description="DCR - Document Content Recognition",
    keywords="dcr",
    license=" Konnexions Public License (KX-PL)",
    name="dcr",
    package_dir={"": "src/dcr"},
    packages=find_packages(include=["dcr", "dcr.*"]),
    python_requires=">=3.10",
    url="https://konnexionsgmbh.github.io/dcr/",
    version="0.5.0",
    zip_safe=False,
)
test_requirements = [
    "pytest",
]
test_suite = ("tests",)
