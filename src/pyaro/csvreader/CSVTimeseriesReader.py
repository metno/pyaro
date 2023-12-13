import csv
import numpy as np
from pyaro.timeseries import Data, NpStructuredData, Flag, Station
import pyaro.timeseries.AutoFilterReaderEngine


class CSVTimeseriesReader(pyaro.timeseries.AutoFilterReaderEngine.AutoFilterReader):
    def __init__(
        self,
        filename,
        columns={
            "variable": 0,
            "station": 1,
            "longitude": 2,
            "latitude": 3,
            "value": 4,
            "units": 5,
            "start_time": 6,
            "end_time": 7,
        },
        variable_units={"SOx": "Gg", "NOx": "Mg"},
        csvreader_kwargs={"delimiter": ","},
        filters=[],
    ):
        """open a new csv timeseries-reader

        :param filename_or_obj_or_url: path-like object to csv-file
        """
        self._filename = filename
        self._stations = {}
        self._data = {}  # var -> {data-array}
        self._set_filters(filters)
        with open(self._filename, newline="") as csvfile:
            crd = csv.reader(csvfile, **csvreader_kwargs)
            for row in crd:
                variable = row[columns["variable"]]
                value = float(row[columns["value"]])
                station = row[columns["station"]]
                lon = float(row[columns["longitude"]])
                lat = float(row[columns["latitude"]])
                start = np.datetime64(row[columns["start_time"]])
                end = np.datetime64(row[columns["end_time"]])
                if "altitude" in columns:
                    alt = float(row[columns["altitude"]])
                else:
                    alt = 0
                if "units" in columns:
                    units = row[columns["units"]]
                else:
                    units = variable_units[variable]

                if variable in self._data:
                    da = self._data[variable]
                    if da.units != units:
                        raise Exception(f"unit change from '{da.units}' to 'units'")
                else:
                    da = NpStructuredData(variable, units)
                    self._data[variable] = da
                da.append(value, station, lat, lon, alt, start, end, Flag.VALID, np.nan)
                if not station in self._stations:
                    self._stations[station] = Station(
                        {
                            "station": station,
                            "longitude": lon,
                            "latitude": lat,
                            "altitude": 0,
                            "country": "NO",
                            "url": "",
                            "long_name": station,
                        }
                    )

    def _unfiltered_data(self, varname) -> Data:
        return self._data[varname]

    def _unfiltered_stations(self) -> dict[str, Station]:
        return self._stations

    def _unfiltered_variables(self) -> list[str]:
        return self._data.keys()

    def close(self):
        pass


class CSVTimeseriesEngine(pyaro.timeseries.AutoFilterReaderEngine.AutoFilterEngine):
    def reader_class(self):
        return CSVTimeseriesReader

    def open(self, filename, *args, **kwargs) -> CSVTimeseriesReader:
        return self.reader_class()(filename, *args, **kwargs)

    def description(self):
        return "Simple reader of csv-files using python csv-reader"

    def url(self):
        return "https://github.com/metno/pyaro"
