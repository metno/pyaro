import abc
from .Data import Data
from .Station import Station

class Reader(abc.ABC):
    """Baseclass for timeseries. This can be used with a context manager"""

    @abc.abstractmethod
    def __init__(self, filename_or_obj_or_url, *, filters=None):
        pass

    @abc.abstractmethod
    def data(self, varname) -> Data:
        pass

    @abc.abstractmethod
    def stations(self) -> dict[str, Station]:
        pass

    @abc.abstractmethod
    def variables(self, station=None) -> list[str]:
        pass

    @abc.abstractmethod
    def close() -> None:
        """Cleanup code for the reader.

        This method will automatically be called when going out of context.
        Implement as dummy (pass) if no cleanup needed.
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
