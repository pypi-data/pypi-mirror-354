#!/usr/bin/env python
"""Setup script for NuroMind package"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nuromind",
    version="0.0.1",
    author="Ziyuan Huang",
    author_email="ziyuan.huang2@umassmed.edu",
    description="A neuroscience ML library for Alzheimer's disease research with microbiome integration and LLM capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/melhzy/nuromind",
    project_urls={
        "Bug Tracker": "https://github.com/melhzy/nuromind/issues",
        "Documentation": "https://github.com/melhzy/nuromind",
        "Source Code": "https://github.com/melhzy/nuromind",
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "datasets>=2.14.0",
        "huggingface-hub>=0.16.0",
        "openai>=1.0.0",
        "langchain>=0.1.0",
        "chromadb>=0.4.0",
        "monai>=1.3.0",
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.12.0",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
        "viz": [
            "plotly>=5.0.0",
            "bokeh>=3.0.0",
        ],
        "bio": [
            "biopython>=1.79",
            "scikit-bio>=0.5.7",
        ],
        "microbiome": [
            "biom-format>=2.1.12",
            "unifrac>=1.1",
        ],
    },
    keywords="neuroscience alzheimer microbiome machine-learning deep-learning",
    include_package_data=True,
    zip_safe=False,
)