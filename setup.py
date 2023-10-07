#!/usr/bin/env python3

from setuptools import setup
import os

setup(
    name="pyaerocom_readers",
    version="0.0.0",
    description="Base Repository for all pyaerocom_readers",
    author="Heiko Klein, Daniel Heinesen",
    author_email="Heiko.Klein@met.no",
    url="https://github.com/metno/pyaerocom-readers",
    packages=["pyaerocom_readers", "pyaerocom_readers.csvreader"],
    package_dir={
        "pyaerocom_readers": "src/pyaerocom_readers",
        "pyaerocom_readers.csvreader": "src/pyaerocom_readers/csvreader"
    },
    package_data={},
    scripts=[],
    entry_points={
        "pyaerocom_readers.timeseries_readers": ["csv_timeseries=pyaerocom_readers.csvreader:CSVTimeseriesReader"]
    }
)
