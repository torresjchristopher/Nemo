from setuptools import setup, find_packages
import os

setup(
    name="nemo",
    version="1.0.0",
    description="Project Nemo - Master Synthesis Engine for Real-Time Intention Prediction",
    author="Christopher Torres",
    packages=[
        'nemo',
        'nemo.core',
        'nemo.systems',
    ],
    package_data={
        'nemo': ['systems/task-screen-simulator/*.py'],
    },
    install_requires=[
        "click==8.1.7",
        "rich==13.7.0",
        "numpy==1.24.3",
        "requests==2.31.0",
        "packaging==23.2",
    ],
    entry_points={
        "console_scripts": [
            "nemo=nemo.core.cli:cli",
        ],
    },
    python_requires=">=3.8",
)
