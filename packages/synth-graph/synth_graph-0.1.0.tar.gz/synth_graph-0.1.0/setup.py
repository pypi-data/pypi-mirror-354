"""
Setup configuration for synth-graph package
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="synth-graph",
    version="0.1.0",
    author="Synth AI",
    author_email="team@synth.ai",
    description="Modern graph orchestration library for building stateful, multi-actor applications with LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/synth-ai/synth-graph",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "networkx>=3.0",
        "pydantic>=2.0",
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"],
    },
)