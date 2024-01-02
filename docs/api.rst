API
========

Documentation of the core API of pyaro.

Classes
------------

.. autosummary::
   :toctree: generated

   pyaro.timeseries

Pyaro - Plugins
^^^^^^^^^^^^

.. autofunction:: pyaro.list_timeseries_engines
.. autofunction:: pyaro.open_timeseries
.. autofunction:: pyaro.timeseries_data_to_pd


Timeseries - User API
^^^^^^^^^^^^

.. autoclass:: pyaro.timeseries.Data
   :members: 
   :undoc-members:
.. autoclass:: pyaro.timeseries.Station
   :members: 
   :undoc-members:
.. autoclass:: pyaro.timeseries.Flag
   :members: 
   :undoc-members:
.. automodule:: pyaro.timeseries.filters
   :members: 
   :undoc-members:
   :imported-members:


Timeseries - Dev API
^^^^^^^^^^^

.. automodule:: pyaro.timeseries
   :members: Engine, Reader, NpStructuredData
   :undoc-members:
   :imported-members:

.. automodule:: pyaro.timeseries.AutoFilterReaderEngine
   :imported-members:


csvreader for timeseries
^^^^^^^^^^^^

A simple implementation of a timeseries reader based on csv-files.

.. automodule:: pyaro.csvreader
   :members: CSVTimeseriesReader
   :undoc-members:
   :imported-members:
