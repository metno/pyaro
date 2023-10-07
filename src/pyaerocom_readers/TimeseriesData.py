

import numpy as np


class TimeseriesData():
    """Baseclass for data returned from a TimeseriesReader.

    This is the minimum set of columns required for a reader to return.
    A reader is welcome to return a self-implemented subclass of
    TimeseriesData.

    All TimeseriesData arrays are accessible as a dict or as property, e.g.
    ```
    td = TimeseriesData()
    print(td.values)
    print(td["values"])
    ```

    """

    def __init__(self) -> None:
        self._variable = ""
        self._units = ""
        self._data = {
            'values': np.zeros((0), 'f'),
            'stations': np.zeros((0), 'U'), # Unicode string
            'latitudes':  np.zeros((0), 'f'),
            'longitudes':np.zeros((0), 'f'),
            'altitudes':  np.zeros((0), 'f'),
            'start_times': np.zeros((0), 'M'), # M=datetime64
            'stop_times': np.zeros((0), 'M'),
            'flags': np.zeros((0), 'i4'),
            'standard_deviations': np.zeros((0), 'f')
        }
        pass

    def __len__(self) -> int:
        """Number of data-points"""
        return self._data["values"].size()

    def __getitem__(self, key):
        """access the data as a dict"""
        return self._data[key]

    def keys(self):
        """all available data-fields, excluding variable and units which are
        considered metadata"""
        return self._data.keys()


    def set_data(self, variable: str, units: str, data: dict[str, np.ndarray]):
        """Initialization code for the data.
        Only known data-fields will be read from data, i.e. it is not
        possible to extend TimeseriesData without subclassing.

        :param variable: variable name
        :param units: variable units
        :param data: dict with all numpy.ndarrays required for TimeseriesData
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
        for key in self.keys():
            self._data[key] = data[key]
        return

    @property
    def variable(self) -> str:
        """Variable name for all the data

        :return: variable name
        """
        return self._variable

    @property
    def unit(self) -> str:
        """Unit in CF-notation, the same unit applies to all values

        :return: Unit in CF-notation
        """

    @property
    def values(self) -> np.ndarray:
        """A 1-dimensional float array of values.

        :return: 1dim array of floats
        """
        return self._data["values"]

    @property
    def stations(self) -> np.ndarray:
        """A 1-dimensional array of station identifiers (strings, usually name)

        :return: 1dim array of strings
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
