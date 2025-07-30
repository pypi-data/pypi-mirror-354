"""
Setup configuration for flotorch-eval package.
"""

from setuptools import find_packages, setup

# Read base requirements
with open("requirements/base.txt") as f:
    base_requirements = [line.strip() for line in f if line.strip() and not line.startswith("-r")]

# Read agent evaluation requirements
with open("requirements/agent_eval.txt") as f:
    agent_eval_requirements = [
        line.strip() for line in f if line.strip() and not line.startswith("-r")
    ]

# Read development requirements
with open("requirements/dev.txt") as f:
    dev_requirements = [line.strip() for line in f if line.strip() and not line.startswith("-r")]

setup(
    name="flotorch-eval",
    version="0.2.1",
    description="A comprehensive evaluation framework for AI systems",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nanda Rajashekaruni",
    author_email="nanda@flotorch.ai",
    url="https://github.com/flotorch/flotorch-eval",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=base_requirements,
    extras_require={
        "agent": agent_eval_requirements,
        "dev": dev_requirements,
        "all": agent_eval_requirements + dev_requirements,
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
