API
========

Documentation of the core API of pyaro.

Classes
------------

Pyaro - Plugins
^^^^^^^^^^^^

.. automodule:: pyaro
   :members: list_timeseries_engines, open_timeseries, timeseries_data_to_pd
   :undoc-members:
   :imported-members:


Timeseries - User API
^^^^^^^^^^^^

.. automodule:: pyaro.timeseries
   :members: filters, Data, Station, Flag
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
