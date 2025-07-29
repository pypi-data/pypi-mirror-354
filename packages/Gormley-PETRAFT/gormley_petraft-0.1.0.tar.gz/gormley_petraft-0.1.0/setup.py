from setuptools import setup, find_packages

setup(
    name="Gormley_PETRAFT",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "openpyxl",  # If you're saving .xlsx
        # Add anything else your code depends on
    ],
    entry_points={
        "console_scripts": [
            "petraft-runner=runner:main",  # If using runner.py
        ],
    },
    author="Your Name",
    description="Automated ATRP recipe generator for PET-RAFT synthesis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
)
