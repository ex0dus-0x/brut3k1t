#!/usr/bin/env python3
"""
setup.py

    Installs brute as CLI application locally.

"""

import os
import setuptools

NAME = "brute"
VERSION = "4.0"

REPO = "https://github.com/ex0dus-0x/brute"
DESC = "brute is a security-oriented framework for bruteforce/credential-stuffing attacks"

# Main setup method
setuptools.setup(
    name = NAME,
    version = VERSION,
    author = "ex0dus",
    description = DESC,
    license = "MIT",
    url=REPO,
    download_url="{}/archive/v{}".format(REPO, VERSION),
    packages = setuptools.find_packages(),
    entry_points = {
        "console_scripts": [
            "brute=brute.__main__:main"
        ],
    },
    install_requires=[
        "mechanize",
        "paramiko",
        "selenium",
        "xmpppy",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: End Users/Desktop",
        "Environment :: Console",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ]
)
