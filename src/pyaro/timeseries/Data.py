
import abc
from enum import IntEnum, unique
import numpy as np

@unique
class Flag(IntEnum):
    """Flag of measurement data.

    :param IntEnum: all flags are simple integers
    """
    VALID = 0
    INVALID = 1
    BELOW_THRESHOLD = 2


class Data(abc.ABC):
    """Baseclass for data returned from a pyaro.timeseries.Reader.

    This is the minimum set of columns required for a reader to return.
    A reader is welcome to return a self-implemented subclass of
    Data.

    All Data arrays are accessible as a dict or as property, e.g.
    ```
    td = Data()
    print(td.values)
    print(td["values"])
    ```

    """
    _dtype = [
            ('values', 'f'),
            ('stations', 'U64'),
            ('latitudes', 'f'),
            ('longitudes', 'f'),
            ('altitudes', 'f'),
            ('start_times', 'datetime64[s]'),
            ('stop_times', 'datetime64[s]'),
            ('flags', 'i2'),
            ('standard_deviations', 'f'),
        ]



    def __init__(self, variable, units) -> None:
        self._variable = variable
        self._units = units

    def _set_variable(self, variable: str) -> None:
        """Friend method to set the variable name

        This is the setter function for variable. It should only be called by
        friend-classes like VariableNameChanger.

        :param variable: variable-name
        """
        self._variable = variable

    @abc.abstractmethod
    def keys(self):
        """all available data-fields, excluding variable and units which are
        considered metadata"""
        return {}.keys()

    @property
    @abc.abstractmethod
    def variable(self) -> str:
        """Variable name for all the data

        :return: variable name
        """
        return self._variable

    @property
    @abc.abstractmethod
    def units(self) -> str:
        """Units in CF-notation, the same unit applies to all values

        :return: Units in CF-notation
        """
        return self._units

    @property
    @abc.abstractmethod
    def values(self) -> np.ndarray:
        """A 1-dimensional float array of values.

        :return: 1dim array of floats
        """
        return

    @property
    @abc.abstractmethod
    def stations(self) -> np.ndarray:
        """A 1-dimensional array of station identifiers (strings, usually name)

        :return: 1dim array of strings, max-length 64-chars
        """
        return

    @property
    @abc.abstractmethod
    def latitudes(self) -> np.ndarray:
        """A 1-dimensional array of latitudes (float)

        :return: 1dim array of floats
        """
        return

    @property
    @abc.abstractmethod
    def longitudes(self) -> np.ndarray:
        """A 1-dimensional array of longitudes (float)

        :return: 1dim array of floats
        """
        return

    @property
    @abc.abstractmethod
    def altitude(self) -> np.ndarray:
        """A 1-dimensional array of altitudes (float)

        :return: 1dim array of floats
        """
        return

    @property
    @abc.abstractmethod
    def start_times(self) -> np.ndarray:
        """A 1-dimensional array of int64 datetimes indicating the start
        of the measurement

        :return: 1dim array of datetime64
        """
        return

    @property
    @abc.abstractmethod
    def end_times(self) -> np.ndarray:
        """A 1-dimensional array of int64 datetimes indicating the end
        of the measurement

        :return: 1dim array of datetime64
        """
        return

    @property
    @abc.abstractmethod
    def flags(self) -> np.ndarray:
        """A 1-dimensional array of flags as defined in pyaro

        :return: 1dim array of ints
        """
        return

    @property
    @abc.abstractmethod
    def standard_deviations(self) -> np.ndarray:
        """A 1-dimensional array of stdevs. NaNs describe
        not available stdev per measurement

        :return: 1dim array of floats
        """
        return



class NpStructuredData(Data):
    """An implementation of Data using numpy Structured Arrays.

    This is the minimum set of columns required for a reader to return.
    A reader is welcome to return a self-implemented subclass of
    Data.

    Data can be added by rows with the append method, or a completed numpy.StructuredArray
    can be submitted using set_data.

    """
    _dtype = [
            ('values', 'f'),
            ('stations', 'U64'),
            ('latitudes', 'f'),
            ('longitudes', 'f'),
            ('altitudes', 'f'),
            ('start_times', 'datetime64[s]'),
            ('stop_times', 'datetime64[s]'),
            ('flags', 'i2'),
            ('standard_deviations', 'f'),
        ]



    def __init__(self, variable, units) -> None:
        self._variable = variable
        self._units = units
        self._data = np.zeros([], dtype=self._dtype)


    def __len__(self) -> int:
        """Number of data-points"""
        return self._data["values"].size

    def __getitem__(self, key):
        """access the data as a dict"""
        return self._data[key]

    def keys(self):
        """all available data-fields, excluding variable and units which are
        considered metadata"""
        return self._data.keys()

    def append(self, value, station, latitude, longitude, altitude, start_time, stop_time, flag=Flag.VALID, standard_deviation=np.nan):
        """append with a new data-row

        :param value
        :param station
        :param latitude
        :param longitude
        :param altitude
        :param start_time
        :param stop_time
        :param flag: defaults to Flag.VALID
        :param standard_deviation: defaults to np.nan
        """
        if len(station) > 64:
            raise Exception(f"station name too long, max 64char: {station}")
        x = np.array([(value, station, latitude, longitude, altitude, start_time, stop_time, flag, standard_deviation)],
                    dtype=self._dtype)
        self._data = np.append(self._data, x)
        return


    def set_data(self, variable: str, units: str, data: np.array):
        """Initialization code for the data.
        Only known data-fields will be read from data, i.e. it is not
        possible to extend TimeseriesData without subclassing.

        :param variable: variable name
        :param units: variable units
        :param data: a numpy structured array with all fields (see append)
        :raises KeyError: on missing field
        :raises Exception: if not all data-ndarrays have same size
        :raises Exception: if not all data-fields are ndarrays
        """
        for key in self.keys():
            if not key in data:
                raise KeyError(f"{key} not in data")
            if not isinstance(data[key], (np.ndarray, np.generic)):
                raise Exception(f"data[{key}] is not a numpy.ndarray")
            if data[key].size() != data["values"].size():
                raise Exception(f"values and {key} not of same size")
        self._variable = variable
        self._units = units
        self._data = data
        return

    @property
    def variable(self) -> str:
        """Variable name for all the data

        :return: variable name
        """
        return self._variable

    @property
    def units(self) -> str:
        """Units in CF-notation, the same unit applies to all values

        :return: Units in CF-notation
        """
        return self._units

    @property
    def values(self) -> np.ndarray:
        """A 1-dimensional float array of values.

        :return: 1dim array of floats
        """
        return self._data["values"]

    @property
    def stations(self) -> np.ndarray:
        """A 1-dimensional array of station identifiers (strings, usually name)

        :return: 1dim array of strings, max-length 64-chars
        """
        return self._data["stations"]

    @property
    def latitudes(self) -> np.ndarray:
        """A 1-dimensional array of latitudes (float)

        :return: 1dim array of floats
        """
        return self._data["latitudes"]

    @property
    def longitudes(self) -> np.ndarray:
        """A 1-dimensional array of longitudes (float)

        :return: 1dim array of floats
        """
        return self._data["longitudes"]

    @property
    def altitude(self) -> np.ndarray:
        """A 1-dimensional array of altitudes (float)

        :return: 1dim array of floats
        """
        return self._data["altitudes"]

    @property
    def start_times(self) -> np.ndarray:
        """A 1-dimensional array of int64 datetimes indicating the start
        of the measurement

        :return: 1dim array of datetime64
        """
        return self._data["start_times"]

    @property
    def end_times(self) -> np.ndarray:
        """A 1-dimensional array of int64 datetimes indicating the end
        of the measurement

        :return: 1dim array of datetime64
        """
        return self._data["end_times"]

    @property
    def flags(self) -> np.ndarray:
        """A 1-dimensional array of flags as defined in pyaro

        :return: 1dim array of ints
        """
        return self._data["flags"]

    @property
    def standard_deviations(self) -> np.ndarray:
        """A 1-dimensional array of stdevs. NaNs describe
        not available stdev per measurement

        :return: 1dim array of floats
        """
        return self._data["standard_deviations"]


    def __str__(self):
        return f"{self.variable}, {self.units}, {self._data}"


