from copy import deepcopy
import functools
import sys
import warnings

from importlib_metadata import EntryPoints, entry_points
from .TimeseriesReader import TimeseriesReader

def build_timeseries_readers(entrypoints: EntryPoints) -> dict[str, TimeseriesReader]:
    backend_entrypoints: dict[str, type[TimeseriesReader]] = {}
    backend_entrypoints = {}
    for entrypoint in entrypoints:
        name = entrypoint.name
        if name in backend_entrypoints:
            return
        try:
            backend = entrypoint.load()
            backend_entrypoints[name] = backend()
        except Exception as ex:
            warnings.warn(f"Engine {name!r} loading failed:\n{ex}", RuntimeWarning)
    return backend_entrypoints


@functools.lru_cache(maxsize=1)
def list_timeseries_readers() -> dict[str, TimeseriesReader]:
    """
    Return a dictionary of available timeseries_readers and their objects.

    Returns
    -------
    dictionary

    Notes
    -----
    This function lives in the backends namespace (``engs=pyar.list_timeseries_readers()``).
    More information about each reader is available via the TimeseriesReader obj.url() and
    obj.description()

    # New selection mechanism introduced with Python 3.10. See GH6514.
    """
    if sys.version_info >= (3, 10):
        entrypoints = entry_points(group="pyaerocom_readers.timeseries_readers")
    else:
        entrypoints = entry_points().get("pyaerocom_readers.timeseries_readers", [])
    return build_timeseries_readers(entrypoints)


def get_timeseries_reader(name):
    return deepcopy(list_timeseries_readers()[name])

def open_timeseries_reader(name, *args, **kwargs) -> TimeseriesReader:
    """open a timeseries reader directly, sending args and kwargs
    directly to the TimeseriesReader.open_reader() function

    :param name: the name of the entrypoint as key in list_timeseries_readers
    :return: an implementation-object of a TimeseriesReader openend to a location
    """
    obj = get_timeseries_reader(name)
    obj.open_reader(args, kwargs)
    return obj
