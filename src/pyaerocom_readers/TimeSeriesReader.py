
import abc

class TimeSeriesReader(abc.ABC):

    @abc.abstractmethod
    def open_reader(filename_or_obj_or_url, *, filters=None):
        pass

    @property
    @abc.abstractmethod
    def open_parameters():
        """return a list of parameters to be passed to open_readers, including
        the mandatory filename_or_obj_or_url parameter.
        """
        return ['filename_or_obj_or_url']

    @abc.abstractmethod
    def get_data(varname, *, filters=None):
        pass

    @property
    @abc.abstractmethod
    def description(self):
        """Get a descriptive string about this timeseries-reader.
        """
        pass

    @property
    @abc.abstractmethod
    def url(self):
        """Get a url about more information, docs of the datasource for this reader.

        This should be the github-url or similar of this reader.
        """
        pass
