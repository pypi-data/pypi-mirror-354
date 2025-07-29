"""Package configuration for the QEPPI-community distribution.

This file originates from the `ohuelab/QEPPI` project and is updated for the
community-maintained version.
"""

import os
from glob import glob
from setuptools import setup

# read version
exec(open("QEPPI/version.py").read())

# long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="QEPPIcommunity",
    version=__version__,
    author="Jianmin Wang",
    author_email="drugai@gmail.com",
    description="Community-Maintained Version of Calculation module of QEPPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AspirinCode/QEPPI-community",
    license="MIT",
    packages=["QEPPI"],
    python_requires=">=3.8",
    install_requires=[
        "rdkit>=2025.3.2",
        "numpy>=1.19.5",
        "pandas>=1.1.5",
    ],
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)