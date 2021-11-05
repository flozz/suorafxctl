#!/usr/bin/env python
# encoding: UTF-8

import os
from setuptools import setup

long_description = ""

try:
    if os.path.isfile("README.rst"):
        long_description = open("README.rst", "r").read()
except Exception as error:
    print("Unable to read the README file: " + str(error))

setup(
    name="suorafxctl",
    version="1.0.0",
    description="Configure Roccat Suora FX keyboards on Linux",
    url="https://github.com/flozz/suorafxctl",
    license="WTFPL",
    long_description=long_description,
    author="Fabien LOISON",
    keywords="roccat suora suorafx keyboard",
    platforms=["Linux"],
    py_modules=["suorafxctl"],
    install_requires=[
        "libusb1>=2.0.0",
        "setuptools",
    ],
    extras_require={
        "dev": [
            "nox",
            "flake8",
            "black",
        ],
    },
    entry_points={
        "console_scripts": [
            "suorafxctl = suorafxctl:main",
        ]
    },
)
