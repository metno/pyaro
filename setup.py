#!/usr/bin/env python3

from setuptools import setup
import os

setup(
    name="pyaro",
    version="0.0.0",
    description="Base Repository for all pyaro, the pyaerocom reader objects",
    author="Heiko Klein, Daniel Heinesen",
    author_email="Heiko.Klein@met.no",
    url="https://github.com/metno/pyaro",
    packages=["pyaro", "pyaro.timeseries", "pyaro.csvreader"],
    package_dir={
        "pyaro": "src/pyaro",
        "pyaro.timeseries": "src/pyaro/timeseries",
        "pyaro.csvreader": "src/pyaro/csvreader"
    },
    package_data={},
    scripts=[],
    entry_points={
        "pyaro.timeseries": ["csv_timeseries=pyaro.csvreader:CSVTimeseriesEngine"]
    }
)
