
import abc
from ._Data import Data
from ._Station import Station

class Reader(abc.ABC):

    @abc.abstractmethod
    def open_reader(self, filename_or_obj_or_url, *, filters=None):
        pass

    @property
    @abc.abstractmethod
    def open_parameters(self):
        """return a list of parameters to be passed to open_readers, including
        the mandatory filename_or_obj_or_url parameter.
        """
        return ['filename_or_obj_or_url']

    @abc.abstractmethod
    def data(self, varname) -> Data:
        pass

    @abc.abstractmethod
    def stations(self) -> dict[str, Station]:
        pass

    @abc.abstractmethod
    def get_variables(self, station=None) -> list[str]:
        pass


    @property
    @abc.abstractmethod
    def description(self):
        """Get a descriptive string about this pyaro.timeseries-reader.
        """
        pass

    @property
    @abc.abstractmethod
    def url(self):
        """Get a url about more information, docs of the datasource for this reader.

        This should be the github-url or similar of this reader.
        """
        pass
