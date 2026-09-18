import abc
import sys
from .Data import Data
from .Station import Station
from .Filter import Filter, filters


class Reader(abc.ABC):
    """Baseclass for timeseries. This can be used with a context manager"""

    @abc.abstractmethod
    def __init__(self, filename_or_obj_or_url, *, filters=None):
        """Initialize the reader.

        This function is usually called from the Engine's open function.
        All parameters should also be listed in the Engine's args function.

        :param filename_or_obj_or_url: location of database instance
        :param filters: list of filters, or dict of (name, kwargs) for FilterFactory
        """
        pass

    def metadata(self) -> dict[str, str]:
        """Metadata set by the datasource.

        The reader-implementation might add metadata depending on the data-source
        to this method. See github.com/pyaro/Metadata.md for more information.

        :return dictionary with different metadata
        """
        return dict()

    def conventions(self) -> list[str]:
        """List all conventions followed by this reader.

        :return: List of convention names.
        """
        if "conventions" in self.metadata():
            return self.metadata()["conventions"].lower().split(",")
        return ["pyaerocom-0.0"]

    @staticmethod
    def _convention_name(convention: str) -> str:
        """Extract the name part of a convention string.

        :param convention: Full convention string.
        :return: Name part of the convention.
        """
        return "".join(convention.lower().split("-")[0:-1])

    @staticmethod
    def _convention_version(convention: str) -> (int, int):
        """Extract the version part of a convention string.

        :param convention: Full convention string.
        :return: Tuple of (major, minor) version numbers.
        """
        version = convention.lower().split("-")[-1]
        version_mayor, version_minor = [int(x) for x in version.split(".")]
        return version_mayor, version_minor

    def convention_supported(self, convention) -> bool:
        """Check if a specific convention is supported by this reader.

        :param convention: Name of the convention to check.
        :return: True if the convention is supported, False otherwise.
        """
        name = self._convention_name(convention)
        version_mayor, version_minor = self._convention_version(convention)
        supported = False
        for conv in self.conventions():
            if self._convention_name(conv) == name:
                major, minor = self._convention_version(conv)
                if version_mayor == major and version_minor >= minor:
                    supported = True
                    break

        return supported

    @abc.abstractmethod
    def data(self, varname: str) -> Data:
        """Return all data for a variable

        :param varname: variable name as returned from variables
        :return: a data object
        """
        pass

    @abc.abstractmethod
    def stations(self) -> dict[str, Station]:
        """Dictionary of all stations available for this reader.

        :return: dictionary with station-id as returned from data to Station metadata.
        """
        pass

    @abc.abstractmethod
    def variables(self) -> list[str]:
        """List all variables available in this reader.

        The variable-names returned here should already be change if a
        VariableNameChanger is used.

        :return: List of variables names.
        """
        pass

    @abc.abstractmethod
    def close(self) -> None:
        """Cleanup code for the reader.

        This method will automatically be called when going out of context.
        Implement as dummy (pass) if no cleanup needed.
        """
        pass

    def __enter__(self):
        """Context managaer function

        :return: context-object
        """
        return self

    def __exit__(self, type, value, traceback):
        """Context manager function.

        The default implementation calls the close function.
        """
        self.close()
        return
