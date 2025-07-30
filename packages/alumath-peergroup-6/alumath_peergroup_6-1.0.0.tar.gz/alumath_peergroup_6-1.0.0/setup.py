"""
Setup script for alumath_peergroup_6 package.
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_file(filename):
    with open(filename, "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return []

setup(
    name="alumath_peergroup_6",
    version="1.0.0",
    author="Peergroup 6",
    author_email="peergroup6@example.com",
    description="A Python library for matrix multiplication with support for different dimensions",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/peergroup6/alumath_peergroup_6",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    keywords="matrix multiplication linear algebra mathematics",
    license="MIT",
    license_files=("LICENSE"),
    project_urls={
        "Bug Reports": "https://github.com/peergroup6/alumath_peergroup_6/issues",
        "Source": "https://github.com/peergroup6/alumath_peergroup_6",
        "Documentation": "https://github.com/peergroup6/alumath_peergroup_6/wiki",
    },
)
