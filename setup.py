"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks

Movie Recommender Setup Script

This script is used to package and distribute the Movie Recommender project.
It contains information about the project, including its name, version, authors,
description, and other relevant details, to facilitate distribution and installation.

For more information about the PopcornPicks project, visit:
https://github.com/CSC-510-G55/PopcornPicks
"""

import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CSC-510-G55",  # Replace with your own username
    version="1.0.0",
    author="Balaji, Bhushan, Cyril",
    author_email="popcornpicksse24@gmail.com@gmail.com",
    description="A movie recommendation engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CSC-510-G55/PopcornPicks",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
