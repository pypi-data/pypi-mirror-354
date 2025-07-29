#!/usr/bin/env python3
from setuptools import setup, find_packages
import os

# Read version from __init__.py
def get_version():
    with open("src/xmemo/__init__.py") as fp:
        for line in fp:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    raise RuntimeError("Unable to find version string.")

version_string = get_version()

# Read README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xmemo",
    version=version_string,
    author="sairin1202",
    author_email="sairin1202@github.com",
    description="A Python package for recording agent memory and reflection from conversations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sairin1202/Xmemo",
    project_urls={
        "Bug Reports": "https://github.com/sairin1202/Xmemo/issues",
        "Source": "https://github.com/sairin1202/Xmemo",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "openai": ["openai>=1.0.0"],
        "claude": ["anthropic>=0.21.0"],
        "integrations": ["openai>=1.0.0", "anthropic>=0.21.0"],
        "all": ["openai>=1.0.0", "anthropic>=0.21.0"],
    },
    keywords=["ai", "agent", "memory", "reflection", "conversation"],
) 