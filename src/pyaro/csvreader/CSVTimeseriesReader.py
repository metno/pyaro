import csv
import numpy as np
from pyaro.timeseries import Data, Flag, Reader, Station, Engine


class CSVTimeseriesReader(Reader):
    def __init__(
                self,
                filename,
                columns={
                    'variable': 0,
                    'station': 1,
                    'longitude': 2,
                    'latitude': 3,
                    'value': 4,
                    'units': 5,
                    'start_time': 6,
                    'end_time': 7
                    },
                variable_units={'SOx': 'Gg',
                                'NOx': 'Mg'},
                csvreader_kwargs={'delimiter': ","},
                filters=[]
                ):
        """open a new csv timeseries-reader

        :param filename_or_obj_or_url: path-like object to csv-file
        """
        self._filename = filename
        self._stations = {}
        self._data = {} # var -> {data-array}
        with open(self._filename, newline='') as csvfile:
            crd = csv.reader(csvfile, **csvreader_kwargs)
            for row in crd:
                variable = row[columns['variable']]
                value = float(row[columns['value']])
                station = row[columns['station']]
                lon = float(row[columns['longitude']])
                lat = float(row[columns['latitude']])
                start = np.datetime64(row[columns['start_time']])
                end = np.datetime64(row[columns['end_time']])
                if 'altitude' in columns:
                    alt = float(row[columns['altitude']])
                else:
                    alt = 0
                if 'units' in columns:
                    units = row[columns['units']]
                else:
                    units = variable_units[variable]

                if variable in self._data:
                    da = self._data[variable]
                    if da.units != units:
                        raise Exception(f"unit change from '{da.units}' to 'units'")
                else:
                    da = Data(variable, units)
                    self._data[variable] = da
                da.append(value, station, lat, lon, alt, start, end, Flag.VALID, np.nan)

    def data(self, varname) -> Data:
        return self._data[varname]

    def stations(self) -> dict[str, Station]:
        return self.stations

    def variables(self) -> list[str]:
        return self._data.keys()

    def close(self):
        pass

class CSVTimeseriesEngine(Engine):
    def open(self, filename, *args, **kwargs) -> CSVTimeseriesReader:
        return CSVTimeseriesReader(filename, *args, **kwargs)

    def args(self):
        return ("filename", "columns", "csvreader_kwargs", "variable_units", "filters")

    def description(self):
        return "Simple reader of csv-files using python csv-reader"

    def url(self):
        return "https://github.com/metno/pyaro"




if __name__ == "__main__":
    import os
    engine = CSVTimeseriesEngine()
    engine.url()
    engine.url
    engine.description()
    engine.args()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'testdata', 'csvReader_testdata.csv')
    with engine.open(file, filters=[]) as ts:
        for var in ts.variables():
            print(var, ts.data(var))
    pass
