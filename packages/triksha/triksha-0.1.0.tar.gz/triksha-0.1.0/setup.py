#!/usr/bin/env python3
"""
Setup script for Triksha

This script allows you to install Triksha as a Python package and creates
convenient command-line entry points.

Usage:
  pip install -e .
  pip install triksha
"""
from setuptools import setup, find_packages
import os

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read long description from README
long_description = ""
if os.path.exists('README.md'):
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name="triksha",
    version="0.1.0",
    description="Advanced LLM Security Testing System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Triksha Team",
    author_email="info@triksha.ai",
    url="https://github.com/triksha-ai/triksha",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
        "Topic :: Software Development :: Testing",
    ],
    keywords="ai security testing llm red-teaming guardrails benchmark",
    entry_points={
        'console_scripts': [
            'triksha=triksha:main',
            'triksha-cli=triksha:main',
            'triksha-benchmark=triksha.cli.commands.benchmark.command:main',
            'triksha-train=triksha.cli.commands.training_commands:main',
        ],
    },
    package_data={
        'triksha': [
            'data/*',
            'datasets/*',
            'model_profiles/*',
            'cli/templates/*',
        ],
    },
)
