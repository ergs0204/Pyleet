from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="pyleet",
    version="0.2.0",
    description="Run and test your LeetCode Python solutions locally",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="ergs0204",
    author_email="ergs0204@gmail.com",
    url="https://github.com/ergs0204/pyleet",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "pyleet=pyleet.__main__:main",  # Adjust to your CLI entry
        ]
    },
    include_package_data=True,
)
