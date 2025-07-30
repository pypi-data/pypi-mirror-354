"""
Setup file for the alumath_kheoml package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="alumath_kheoml",
    version="0.1.0",
    author="Group 4",
    author_email="your.email@example.com",
    description="A matrix operations library developed at African Leadership University",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oreste-abizera/ALU-BSE-MathML-PCA-Assignment-group4",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research"
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.0",
    ],
)
