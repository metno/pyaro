.. _add_a_reader:

How to add a new reader
------------------------

Adding a new reader for read support to pyaerocom does not require
to integrate any code in PyAerocom; all you need to do is:

- Create a class that inherits from :py:class:`~pyaro.timeseries.Reader` and
  :py:class:`~pyaro.timeseries.Engine`
  and implements the methods, see :ref:`RST backend_entrypoint`

- Declare the Engine-class as an external plugin in your ``setup.py``, see :ref:`RST reader_registration`

If you also want to support lazy loading and dask see :ref:`RST lazy_loading`.


You can see what backends are currently available in your working environment
with :py:class:`~pyaro.list_timeseries_readers()`.

.. _RST backend_entrypoint:

TimeseriesEngine/Reader subclassing
+++++++++++++++++++++++++++++++++++

Your ``TimeseriesReader`` sub-class is the primary interface with PyAerocom, and
it should implement the following attributes and methods:

- the ``__init__`` method (mandatory)
- the ``data`` method (mandatory)
- the ``stations`` method (mandatory)
- the ``variables`` method (mandatory)
- the ``close`` method (optional, if needed)

The entry-point to your ``Reader`` is a ``Engine``, which also needs implementation:

- the ``open`` method, instantiating the ``Reader`` (mandatory)
- the ``args`` readonly attribute (mandatory, a list of arguments which can be given to open)
- the ``supported_filters`` readonly attribute (mandatory, a list of filters)
- the ``description`` readonly attribute (optional)
- the ``url`` readonly attribute (optional) (reference to repository)

This is what a ``TimeseriesReader`` subclass should look like:

.. code-block:: python

    from pyaro.timeseries import Data, Reader, Station, Engine


    class MyTimeseriesReader(Reader):
        def __init__(
            self,
            filename_or_obj_or_url,
            *,
            filters=None,
            # other backend specific keyword arguments
            # `chunks` and `cache` DO NOT go here, they are handled by xarray
        ):
            ...


        def data(self, varname):
            ...

        def stations(self):
            ...

        def variables(self):
            ...

    class MyTimeseriesEngine(Engine)
        def open(self, filename_or_obj_or_url, *args, **kwargs):
            return MyTimeseriesReader(filename_or_obj_or_url, *args, **kwargs)

        def args(self):
            open_parameters = ["filename_or_obj", "filters"]
            return open_parameters

        def supported_filters(self):
            return ["CountryFilter", "FlagFilter"]

        def description(self):
            return "Engine fro MyTimeseries files."

        def url(self):
            return "https://link_to/your_backend/documentation"

``Reader`` subclass methods and attributes are detailed in the following.

.. _RST Engine.open or Reader.__init__:
^^^^^^^^^^^^

The backend-Engine ``open`` shall implement reading from location, the variables
decoding and it shall instantiate the output PyAerocom class :py:class:`~pyaro.Data`.

The following is an example of the high level processing steps:

.. code-block:: python

    def open(
        self,
        filename_or_obj_or_url,
        *,
        filters
    ):
        return tsr



The input of ``open`` method are one argument
(``filename_or_obj_or_url``) and one keyword argument (``drop_variables``):

- ``filename_or_obj_or_url``: can be any object but usually it is a string containing a path or an instance of
  :py:class:`pathlib.Path` or an url.
- ``filters``: can be `None` or an iterable containing filters to be (optionally) applied when reading the data.


Your reader can also take as input a set of backend-specific keyword
arguments. All these keyword arguments can be passed to
:py:func:`~pyaro.timeseries.Engine.open` grouped either via the ``backend_kwargs``
parameter or explicitly using the syntax ``**kwargs``.


.. _RST Engine.args:

Engine.args
^^^^^^^^^^^^^^^^^^^^^^^

``Engine.args`` is the list of backend ``open`` arguments.


.. _RST properties:

Engine.description and Engine.url
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``description`` is used to provide a short text description of the backend.
``url`` is used to include a link to the backend's documentation or code.

These attributes are surfaced when a user prints :py:class:`~pyaro.timeseries.backends`.
If ``description`` or ``url`` are not defined, an empty string is returned.


.. _RST backend_registration:

How to register a reader (backend)
+++++++++++++++++++++++++

Define a new entrypoint in your ``setup.py`` (or ``setup.cfg``) with:

- group: ``pyaro.timeseries``
- name: the name to be passed to :py:meth:`~pyaro.timeseries`  as ``engine``
- object reference: the reference of the Engine-class that you have implemented.

You can declare the entrypoint in ``setup.py`` using the following syntax:

.. code-block::

    setuptools.setup(
        entry_points={
            "pyaro.timeseries": ["my_timeseries_reader=my_package.my_module:MyTimeseriesEngine"],
        },
    )

in ``setup.cfg``:

.. code-block:: cfg

    [options.entry_points]
    pyaro.timeseries =
        my_timeseries_reader = my_package.my_module:MyTimeseriesEngine


See https://packaging.python.org/specifications/entry-points/#data-model
for more information

If you are using `Poetry <https://python-poetry.org/>`_ for your build system, you can accomplish the same thing using "plugins".
In this case you would need to add the following to your ``pyproject.toml`` file:

.. code-block:: toml

    [tool.poetry.plugins."pyaro.timeseries"]
    "my_timesereiesreader" = "my_package.my_module:MyTimeseriesEngine"

See https://python-poetry.org/docs/pyproject/#plugins for more information on Poetry plugins.

.. _RST lazy_loading:

How to support lazy loading
+++++++++++++++++++++++++++

TimeseriesReaders are by design lazy loading, i.e. data can be loaded when the ``data`` method is called
(if supported by the implementation).


