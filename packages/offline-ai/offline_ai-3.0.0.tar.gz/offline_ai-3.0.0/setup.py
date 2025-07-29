#!/usr/bin/env python3
"""
Setup script for offline-ai package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="offline-ai",
    version="3.0.0",
    author="AI Terminal Assistant",
    author_email="offline-ai@example.com",
    description="🤖 Локальный ИИ-ассистент для терминала с умной установкой без прав администратора",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ai-terminal/offline-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Terminals",
        "Topic :: Utilities",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "offline-ai=offline_ai.cli:main",
            "ai=offline_ai.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
