#!/usr/bin/env python3
"""
Setup script for whisper-ssh package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read development requirements
dev_requirements = []
with open('requirements-dev.txt') as f:
    dev_requirements = f.read().splitlines()

setup(
    name="whisper-ssh",
    version="1.1.0",
    author="Josh Meesey",
    description="Whisper messages to remote Linux machines via SSH",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JdMasuta/whisper-ssh",
    project_urls={
        "Bug Tracker": "https://github.com/JdMasuta/whisper-ssh/issues",
        "Documentation": "https://github.com/JdMasuta/whisper-ssh#readme",
        "Source Code": "https://github.com/JdMasuta/whisper-ssh",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Communications",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "test": ["pytest>=6.0", "pytest-cov>=2.0"],
    },
    entry_points={
        "console_scripts": [
            "whisper-ssh=whisper_ssh.cli:main",
            "whisper=whisper_ssh.cli:main",  # Short alias
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="ssh notification remote desktop linux ubuntu notify-send whisper",
    platforms=["any"],
)