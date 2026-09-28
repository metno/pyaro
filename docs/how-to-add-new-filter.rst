.. _add_a_filter:

How to add a new filter
=======================

Filters allow a reader to reduce or transform the variables, stations, or
observations it exposes. The built-in filters are implemented in
``pyaro.timeseries.Filter``. A filter can be added to Pyaro when its
implementation is available to the reader package and the reader advertises
that it supports the filter.

Choose the filter base class
----------------------------

Start by choosing the base class that matches what the filter changes:

``Filter``
    Use this for a filter that changes variables, stations, or data directly.
    Override one or more of ``filter_variables``, ``filter_stations``, and
    ``filter_data``.

``DataIndexFilter``
    Use this when the filter selects observations from a :py:class:`~pyaro.timeseries.Data`
    object. Implement ``filter_data_idx`` and return an index accepted by
    :meth:`~pyaro.timeseries.Data.slice`. ``DataIndexFilter`` applies that
    index in its ``filter_data`` implementation, so the data filtering logic
    does not need to be duplicated.

``StationReductionFilter``
    Use this for a filter that removes stations and the corresponding
    observations. Implement ``filter_stations``; the base class derives the
    observation index from the remaining station names.

Always implement the methods ``__init__``, ``init_kwargs()``, and ``name()`` in addition
to the chosen base classes methods.

The base ``Filter`` methods return their input unchanged. This means a filter
only needs to implement the operations it actually supports. For example, a
filter that only removes variables should implement ``filter_variables`` and
leave station and data handling to the defaults.

Implement and register the filter
----------------------------------

Every concrete filter must provide:

* a constructor with sensible defaults;
* ``init_kwargs()``, returning the arguments needed to recreate the current
  filter;
* ``name()``, returning a unique factory name; and
* the relevant filtering method(s).

Use ``@registered_filter`` to add the filter to the process-wide filter
factory. Registration happens when the module containing the class is
imported.

The following example keeps observations whose quality value is between a
configured limit (this functionality is already available in the
``:py:class:`~pyaro.timeseries.Filter.DataRangeFilter` ``):

.. code-block:: python

    import numpy as np

    from pyaro.timeseries.Filter import DataIndexFilter, registered_filter


    @registered_filter
    class DataMinMaxFilter(DataIndexFilter):
        def __init__(self, minimum: float = 0.0, maximum: float = 1.0):
            self._minimum = minimum
            self._maximum = maximum

        def init_kwargs(self):
            return {"minimum": self._minimum, "maximum": self._maximum}

        def name(self):
            return "data_min_max"

        def filter_data_idx(self, data, stations, variables):
            return (np.asarray(data["quality"]) >= self._minimum) & (np.asarray(data["quality"]) <= self._maximum)

The concrete data access in ``filter_data_idx`` must follow the
:py:class:`~pyaro.timeseries.Data` implementation used by the reader. A
filter should raise a clear exception for invalid configuration rather than
silently returning a different result.

``name()`` is the public name used by the declarative filter syntax. It must
not collide with an existing filter name. The registration decorator raises
``FilterFactoryException`` when a duplicate name is registered.

Make the filter available to a reader
-------------------------------------

Readers based on :py:class:`~pyaro.timeseries.AutoFilterReaderEngine.AutoFilterReader`
must include the filter in ``supported_filters``. The default implementation
returns the built-in filters, so override it when adding a reader-specific
filter:

.. code-block:: python

    from pyaro.timeseries.AutoFilterReaderEngine import AutoFilterReader
    from pyaro.timeseries.Filter import filters


    class MyReader(AutoFilterReader):
        @classmethod
        def supported_filters(cls):
            supported = super().supported_filters()
            supported.append(filters.get("data_min_max"))
            return supported

        # Implement _unfiltered_data, _unfiltered_stations,
        # _unfiltered_variables, and close as usual.

The reader must call ``self._set_filters(filters)`` from its constructor.
``AutoFilterReader`` then applies the configured filters to
``variables()``, ``stations()``, and ``data()``. A filter supplied to a
reader but not listed by ``supported_filters`` raises
``UnknownFilterException``.

Readers that subclass :py:class:`~pyaro.timeseries.Reader` directly must
apply filters themselves and validate them against the reader's
``supported_filters`` contract. For most readers,
``AutoFilterReader`` is the preferred implementation because it keeps this
behaviour consistent.

Make the filter available to (most/all) Readers
----------------

To make a built-in filter available to every reader that uses
``AutoFilterReader``'s default implementation, add its factory name to the
comma-separated list returned by
``AutoFilterReader.supported_filters()`` in
``pyaro.timeseries.AutoFilterReaderEngine``. The filter must already be
registered with ``@registered_filter`` so that ``filters.get(name)`` can
instantiate it. All ``AutoFilterReader`` subclasses that do not override
``supported_filters()`` will then accept it.

Reader-specific subclasses may still override ``supported_filters()`` to
restrict or extend the list. If a reader overrides the method, add the new
filter explicitly there when that reader should support it.



Using the filter
----------------

After the module containing the filter has been imported, it can be created
programmatically:

.. code-block:: python

    quality_filter = filters.get("data_min_max", maximum=0.5)
    reader = engine.open("observations.csv", filters=[quality_filter])

It can also be created declaratively by passing the factory name and
constructor arguments:

.. code-block:: python

    reader = engine.open(
        "observations.csv",
        filters={"data_min_max": {"maximum": 0.5}},
    )

Multiple filters are applied in the order supplied. The declarative dictionary
form is converted to a list of filter objects by the reader, and each filter
must be supported by that reader.

Test the filter
---------------

Add focused tests for the filter's public behaviour. At minimum, test:

* the default and configured constructor arguments;
* ``name()`` and ``init_kwargs()``;
* inclusion and exclusion of the relevant variables, stations, or
  observations;
* boundary values and empty results; and
* use through both ``filters.get`` and a reader's ``filters`` argument.

Also run the repository test suite and build the documentation to catch
invalid cross-references or examples:

.. code-block:: console

    python -m unittest discover -s tests
    sphinx-build -b html docs docs/_build/html

If the filter is part of the public built-in API, add its class to the filter
list in ``docs/api.rst`` so that its API documentation is generated.
