#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "0.0.1"

setup(
    name="exsce-floorplan",
    version=version,
    author="Samuel Parra",
    description="Python realization of metamodels for indoor environment",
    long_description=long_description,
    long_description_content_type="text/markdown",

    python_requires=">=3.6",
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    package_data={
        # textx grammar files
        '': ['*.tx']
    },
    install_requires=[
        'textx',
        'textX-jinja',
        'numpy',
        'shapely',
        'matplotlib'
    ],
    entry_points={
        # textx language registration
        'textx_languages': [
            'exsce-floorplan-dsl = exsce_floorplan.registration:floorplan_lang',
            'exsce-variation-dsl = exsce_floorplan.registration:variation_lang'
        ],
        'textx_generators' : [
            'variation-to-floorplan = exsce_floorplan.registration:variation_floorplan_gen',
        ],
    },
)
