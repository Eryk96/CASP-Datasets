#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

setup(
    name="casp",
    version="1.0",
    description="Extracts CASP data from predictioncenter and loads it into a file store to be used for machine learning",
    author="Erik Nicolas Kiehl",
    author_email="erik.kiehl@hotmail.dk",
    packages=find_packages(),
    entry_points={"console_scripts": ["casp=casp.cli:cli"]},
)