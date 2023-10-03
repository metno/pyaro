.. _add_a_reader:

How to add a new reader
------------------------

Adding a new reader for read support to pyaerocom does not require
to integrate any code in PyAerocom; all you need to do is:

- Create a class that inherits from PyAerocom :py:class:`~pyaerocom_readers.TimeseriesReader` or ProfileReader
  and implements the method ``open_dataset`` see :ref:`RST backend_entrypoint`

- Declare this class as an external plugin in your ``setup.py``, see :ref:`RST reader_registration`

If you also want to support lazy loading and dask see :ref:`RST lazy_loading`.


You can see what backends are currently available in your working environment
with :py:class:`~pyaerocom_readers.list_timeseries_readers()`.

.. _RST backend_entrypoint:

TimeseriesReader subclassing
+++++++++++++++++++++++++++++

Your ``TimeseriesReader`` sub-class is the primary interface with PyAerocom, and
it should implement the following attributes and methods:

- the ``open_reader`` method (mandatory)
- the ``open_parameters`` attribute (optional)
- the ``description`` attribute (optional)
- the ```get_data`` method (mandatory)
- the ``url`` attribute (optional).

This is what a ``TimeseriesReader`` subclass should look like:

.. code-block:: python

    from pyaerocom_readers import TimeseriesReader


    class MyTimeseriesReader(TimeseriesReader):
        def open_reader(
            self,
            filename_or_obj_or_url,
            *,
            filters=None,
            # other backend specific keyword arguments
            # `chunks` and `cache` DO NOT go here, they are handled by xarray
        ):
            return my_open_dataset(filename_or_obj_or_url, drop_variables=drop_variables)

        open_parameters = ["filename_or_obj", "filters"]

        def get_data(TBD)

        description = "Use .my_database files in PyAerocom"

        url = "https://link_to/your_backend/documentation"

``TimeseriesReader`` subclass methods and attributes are detailed in the following.

.. _RST open_dataset:

open_network
^^^^^^^^^^^^

The backend ``open_reader`` shall implement reading from location, the variables
decoding and it shall instantiate the output PyAerocom class :py:class:`~pyaerocom.TimeseriesData` (TBD).

The following is an example of the high level processing steps:

.. code-block:: python

    def open_reader(
        self,
        filename_or_obj_or_url,
        *,
        filters
    ):
        return tsr



The input of ``open_reader`` method are one argument
(``filename_or_obj_or_url``) and one keyword argument (``drop_variables``):

- ``filename_or_obj_or_url``: can be any object but usually it is a string containing a path or an instance of
  :py:class:`pathlib.Path` or an url.
- ``filters``: can be `None` or an iterable containing filters to be (optionally) applied when reading the data.


Your reader can also take as input a set of backend-specific keyword
arguments. All these keyword arguments can be passed to
:py:func:`~pyaerocom-reader.open_reader` grouped either via the ``backend_kwargs``
parameter or explicitly using the syntax ``**kwargs``.


.. _RST open_parameters:

open_parameters
^^^^^^^^^^^^^^^^^^^^^^^

``open_parameters`` is the list of backend ``open_reader`` parameters.
It is not a mandatory parameter, and if the backend does not provide it
explicitly, pyaerocom_readers creates a list of them automatically by inspecting the
backend signature.



.. _RST properties:

description and url
^^^^^^^^^^^^^^^^^^^^

``description`` is used to provide a short text description of the backend.
``url`` is used to include a link to the backend's documentation or code.

These attributes are surfaced when a user prints :py:class:`~pyaercom-readers.timeseries-backends`.
If ``description`` or ``url`` are not defined, an empty string is returned.


.. _RST backend_registration:

How to register a reader (backend)
+++++++++++++++++++++++++

Define a new entrypoint in your ``setup.py`` (or ``setup.cfg``) with:

- group: ``pyaerocom_readers.timeseries_readers``
- name: the name to be passed to :py:meth:`~pyaerocom_readers.open_reader`  as ``engine``
- object reference: the reference of the class that you have implemented.

You can declare the entrypoint in ``setup.py`` using the following syntax:

.. code-block::

    setuptools.setup(
        entry_points={
            "pyaerocom_readers.timeseries_readers": ["my_timeseries_reader=my_package.my_module:MyTimeseriesReaderClass"],
        },
    )

in ``setup.cfg``:

.. code-block:: cfg

    [options.entry_points]
    pyaercom-readers.timeseries_readers =
        my_timeseriesreader = my_package.my_module:MyTimeseriesReaderClass


See https://packaging.python.org/specifications/entry-points/#data-model
for more information

If you are using `Poetry <https://python-poetry.org/>`_ for your build system, you can accomplish the same thing using "plugins". In this case you would need to add the following to your ``pyproject.toml`` file:

.. code-block:: toml

    [tool.poetry.plugins."pyaerocom_readers.timeseries_readers"]
    "my_timesereiesreader" = "my_package.my_module:MyTimeseriesReaderClass"

See https://python-poetry.org/docs/pyproject/#plugins for more information on Poetry plugins.

.. _RST lazy_loading:

How to support lazy loading
+++++++++++++++++++++++++++

TimeseriesReaders are by design lazy loading, i.e. data is loaded when the ``get_data`` method is called.


