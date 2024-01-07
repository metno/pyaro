***************************
pyaro - Airquality Reader-interface for Observations
***************************

Website of pyaro, the Python library that solves the mystery of reading airquality measurement databases. (Pronounciation as in French: Poirot)

About
============

Pyaro is an interface which uses a simple access pattern to different air-pollution databases.
The goal of pyro was threefold.

    1. A simple interface for different types of air-pollution databases
    2. A programatic interface to these databases easily usable by large applications like `PyAerocom <https://pyaerocom.readthedocs.io>`_
    3. Easy extension for air-pollution database providers or programmers giving the users (1. or 2.) direct access
       their databases without the need of a new API.

A few existing implementations of pyaro can be found at `pyaerocom-readers <https://github.com/metno/pyaro-readers>`_ .

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   index
   installation
   tutorials/index
   reader-design
   timeseries_data
   api
   how-to-add-new-reader
   genindex

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
