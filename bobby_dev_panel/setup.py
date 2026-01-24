"""
Setup script for Bobby Dev Panel
"""

from setuptools import setup, find_packages

setup(
    name="bobby-dev-panel",
    version="1.0.0",
    description="Device diagnostics and control panel for Android devices",
    author="Bobby's Workshop",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "bobby-dev-panel=bobby.cli:cli_main",
            "bobby=bobby.cli:cli_main",
        ],
    },
)
