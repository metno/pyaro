import functools
import sys
import warnings

from importlib_metadata import EntryPoints, entry_points
from .TimeSeriesReader import TimeSeriesReader

def build_timeseries_readers(entrypoints: EntryPoints) -> dict[str, TimeSeriesReader]:
    backend_entrypoints: dict[str, type[TimeSeriesReader]] = {}
    backend_entrypoints = {}
    for entrypoint in entrypoints:
        name = entrypoint.name
        if name in backend_entrypoints:
            return
        try:
            backend = entrypoint.load()
            backend_entrypoints[name] = backend
        except Exception as ex:
            warnings.warn(f"Engine {name!r} loading failed:\n{ex}", RuntimeWarning)
    return backend_entrypoints


@functools.lru_cache(maxsize=1)
def list_timeseries_readers() -> dict[str, TimeSeriesReader]:
    """
    Return a dictionary of available timeseries_readers and their objects.

    Returns
    -------
    dictionary

    Notes
    -----
    This function lives in the backends namespace (``engs=pyare.list_timeseries_readers()``).
    More information about each reader is available via the TimeSeriesReader obj.url() and
    obj.description()

    # New selection mechanism introduced with Python 3.10. See GH6514.
    """
    if sys.version_info >= (3, 10):
        entrypoints = entry_points(group="pyaerocom-readers.timeseries_readers")
    else:
        entrypoints = entry_points().get("xarray.backends", [])
    return build_timeseries_readers(entrypoints)


