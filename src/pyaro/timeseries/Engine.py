import abc

class Engine(abc.ABC):
    """The engine is the 'singelton' generator object for databases of the engines type."""

    @abc.abstractmethod
    def open_timeseries(self, filename_or_obj_or_url, *, filters=None):
        """open-function of the timeseries, initializing the reader-object, i.e.
        equivalent to Reader(filename_or_object_or_url, *, filter)

        @return pyaro.timeseries.Reader
        """
        pass

    @property
    @abc.abstractmethod
    def timeseries_args(self) -> list[str]:
        """return a tuple of parameters to be passed to open_timeseries, including
        the mandatory filename_or_obj_or_url parameter.
        """
        return ['filename_or_obj_or_url']

    @property
    @abc.abstractmethod
    def description(self):
        """Get a descriptive string about this pyaro implementation.
        """
        pass

    @property
    @abc.abstractmethod
    def url(self):
        """Get a url about more information, docs of the datasource-engine.

        This should be the github-url or similar of the implementation.
        """
        pass




