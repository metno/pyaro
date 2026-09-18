import numpy as np

from .Data import Data, DynamicRecArray, Flag


class DataStationIdStructured(Data):
    """An implementation of Data using numpy Structured Arrays and keeping stations as a separate field.

    This is the minimum set of columns required for a reader to return.
    A reader is welcome to return a self-implemented subclass of
    Data.

    stations is U64, so it is at least 256 bytes long, which is much larger than the rest (38 bytes).
    For long timeseries, e.g. years of hourly data, this might be too much. Keeping station
    information separate from time-step data can save memory.

    The current approach stores a timestep in 30 bytes, and each station in 76 bytes, reducing
    memory consumption for long time-series to about 10% compared to NpStructuredData with 310 bytes
    per measurement.

    Data can be added by rows with the append method, or a completed numpy.StructuredArray
    can be submitted using set_data.

    :note: Available since 0.3.0

    """

    _dtype = [
        ("values", "f"),
        ("station_ids", "i4"),
        ("start_times", "datetime64[s]"),
        ("end_times", "datetime64[s]"),
        ("flags", "i2"),
        ("standard_deviations", "f"),
    ]

    _dtype_station = [
        ("stations", "U64"),
        ("latitudes", "f"),
        ("longitudes", "f"),
        ("altitudes", "f"),
    ]

    def __init__(self, variable: str = "", units: str = "") -> None:
        self._variable = variable
        self._units = units
        self._data = DynamicRecArray(self._dtype)
        self._station_data = DynamicRecArray(self._dtype_station)
        self._station_dict = (
            dict()
        )  # mapping from station name to station index in _station_data

    def __len__(self) -> int:
        """Number of data-points"""
        return len(self._data)

    def __getitem__(self, key):
        """access the data as a dict"""
        # check if key is a tuple or list
        if isinstance(key, (tuple, list)):
            raise KeyError(
                f"Tuple or list keys are not supported by {self.__class__.__name__}"
            )
        if key in self._data.keys():
            return self._data.data[key]
        elif key in self._station_data.keys():
            return self._station_data.data[self._data.data["station_ids"]][key]
        else:
            raise KeyError(f"Key {key} not found in data or station data")

    def unique_by_keys(self, keys: tuple | list) -> np.array:
        """Return the indices of unique rows based on the specified keys
        :param keys: tuple or list of keys to consider for uniqueness
        :return: numpy array of indices of unique rows
        """
        # use dict for ordered keys
        data_keys = dict()
        for key in keys:
            if key in self._data.keys():
                data_keys[key] = 1
            elif key in self._station_data.keys():
                data_keys["station_ids"] = 1
            else:
                raise KeyError(f"Key {key} not found in data or station data")
        return np.unique(self._data.data[list(data_keys.keys())], return_index=True)[1]

    def keys(self):
        """all available data-fields, excluding variable and units which are
        considered metadata"""
        return self._data.keys() + self._station_data.keys()

    def append(
        self,
        value,
        station,
        latitude,
        longitude,
        altitude,
        start_time,
        end_time,
        flag=Flag.VALID,
        standard_deviation=np.nan,
    ):
        """append with a new data-row, or numpy arrays

        :param value
        :param station
        :param latitude
        :param longitude
        :param altitude
        :param start_time
        :param end_time
        :param flag: defaults to Flag.VALID
        :param standard_deviation: defaults to np.nan
        """
        if type(value).__module__ == np.__name__:  # numpy array handling
            # get a index to unique stations
            station_ids = np.zeros_like(station, dtype=int)
            # loop over all stations and add them if new or set the known ids
            unique_stations = np.unique(station)
            for i, unique_station in enumerate(unique_stations):
                if unique_station not in self._station_dict:
                    station_index = len(self._station_data)
                    self._station_data.append(
                        (
                            unique_station,
                            latitude[i],
                            longitude[i],
                            altitude[i],
                        )
                    )
                    self._station_dict[unique_station] = station_index
                else:
                    station_index = self._station_dict[unique_station]
                station_ids[station == unique_station] = station_index
            # append the data-section, but with station_ids only
            self._data.append_array(
                values=value,
                station_ids=station_ids,
                start_times=start_time,
                end_times=end_time,
                flags=flag,
                standard_deviations=standard_deviation,
            )
        else:
            # below add single values
            if len(station) > 64:
                raise Exception(f"station name too long, max 64char: {station}")
            #        x = np.array([(value, station, latitude, longitude, altitude, start_time, end_time, flag, standard_deviation)],
            #                    dtype=self._dtype)
            if not station in self._station_dict:
                # add new station to _station_data and update _station_dict
                station_index = len(self._station_data)
                self._station_data.append(
                    (
                        station,
                        latitude,
                        longitude,
                        altitude,
                    )
                )
                self._station_dict[station] = station_index
            else:
                station_index = self._station_dict[station]

            self._data.append(
                (
                    value,
                    station_index,
                    start_time,
                    end_time,
                    flag,
                    standard_deviation,
                )
            )
        return

    def set_data(
        self,
        variable: str,
        units: str,
        data: np.array,
        station_data: np.array,
        station_dict: dict,
    ):
        """Initialization code for the data.
        Only known data-fields will be read from data, i.e. it is not
        possible to extend TimeseriesData without subclassing.

        :param variable: variable name
        :param units: variable units
        :param data: a numpy structured array with all fields (see append)
        :param station_data: a numpy structured array with all station fields
        :param station_dict: a dictionary mapping station names to indices
        :raises KeyError: on missing field
        :raises Exception: if not all data-ndarrays have same size
        :raises Exception: if not all data-fields are ndarrays
        """
        for key in self._data.data.dtype.names:
            if key not in data.dtype.names:
                raise KeyError(f"{key} not in data: {data.dtype}")
            if not isinstance(data[key], (np.ndarray, np.generic)):
                raise Exception(f"data[{key}] is not a numpy.ndarray")
            if len(data[key]) != len(data["values"]):
                raise Exception(f"values and {key} not of same size")
        for key in station_data.dtype.names:
            if key not in self._station_data.data.dtype.names:
                raise KeyError(f"{key} not in station_data: {station_data.dtype}")
            if not isinstance(station_data[key], (np.ndarray, np.generic)):
                raise Exception(f"station_data[{key}] is not a numpy.ndarray")
        self._variable = variable
        self._units = units
        self._data.set_data(data)
        self._station_data.set_data(station_data)
        self._station_dict = station_dict
        return

    def slice(self, index):
        newData = DataStationIdStructured()
        newData.set_data(
            self.variable,
            self.units,
            self._data.data[index],
            self._station_data.data,
            self._station_dict,
        )
        return newData

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
        return self._data.data["values"]

    @property
    def stations(self) -> np.ndarray:
        """A 1-dimensional array of station identifiers (strings, usually name)

        :return: 1dim array of strings, max-length 64-chars
        """
        return self.stations_by_ids(self.station_ids)

    def stations_by_ids(self, station_ids):
        station_ids = np.asarray(station_ids)

        return self._station_data.data[station_ids]["stations"]

    @property
    def station_ids(self) -> np.ndarray:
        """A 1-dimensional array of station ids.

        :return: 1dim array of integers
        """
        return self._data.data["station_ids"]

    @property
    def latitudes(self) -> np.ndarray:
        """A 1-dimensional array of latitudes (float)

        :return: 1dim array of floats
        """
        return self._station_data.data[self.station_ids]["latitudes"]

    @property
    def longitudes(self) -> np.ndarray:
        """A 1-dimensional array of longitudes (float)

        :return: 1dim array of floats
        """
        return self._station_data.data[self.station_ids]["longitudes"]

    @property
    def altitudes(self) -> np.ndarray:
        """A 1-dimensional array of altitudes (float)

        :return: 1dim array of floats
        """
        return self._station_data.data[self.station_ids]["altitudes"]

    @property
    def start_times(self) -> np.ndarray:
        """A 1-dimensional array of int64 datetimes indicating the start
        of the measurement

        :return: 1dim array of datetime64
        """
        return self._data.data["start_times"]

    @property
    def end_times(self) -> np.ndarray:
        """A 1-dimensional array of int64 datetimes indicating the end
        of the measurement

        :return: 1dim array of datetime64
        """
        return self._data.data["end_times"]

    @property
    def flags(self) -> np.ndarray:
        """A 1-dimensional array of flags as defined in pyaro

        :return: 1dim array of ints
        """
        return self._data.data["flags"]

    @property
    def standard_deviations(self) -> np.ndarray:
        """A 1-dimensional array of stdevs. NaNs describe
        not available stdev per measurement

        :return: 1dim array of floats
        """
        return self._data.data["standard_deviations"]

    def __str__(self):
        return f"{self.variable}, {self.units}, {self._data.data}, {self._station_data.data}"
