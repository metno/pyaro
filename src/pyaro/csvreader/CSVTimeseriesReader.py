import csv
import numpy as np
from pyaro.timeseries import Data, Reader, Station, Engine

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
                csvreader_kwargs={'delimiter': ","},
                variable_units={'SOx': 'Gg'},
                filters=[]
                ):
        """open a new csv timeseries-reader

        :param filename_or_obj_or_url: path-like object to csv-file
        """
        self._filename = filename
        self._stations = {}
        self._data = {} # var -> station -> {}
        with open(self._filename, newline='') as csvfile:
            crd = csv.reader(csvfile, **csvreader_kwargs)
            for row in crd:
                variable = row[columns['variable']]
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
                    unit = row[columns['units']]
                else:
                    units = ""



    def data(self, varname) -> Data:
        return Data()

    def stations(self) -> dict[str, Station]:
        return self.stations

    def variables(self) -> list[str]:
        return []

    def close(self):
        pass

class CSVTimeseriesEngine(Engine):
    def open_timeseries(self, filename, *args, **kwargs) -> CSVTimeseriesReader:
        return CSVTimeseriesReader(filename, *args, **kwargs)

    def timeseries_args(self):
        return ("filename", "columns", "csvreader_kwargs", "variable_units", "filters")

    def description(self):
        return "Simple reader of csv-files using python csv-reader"

    def url(self):
        return "https://github.com/metno/pyaro"




if __name__ == "__main__":
    import os
    engine = CSVTimeseriesEngine()
    engine.url()
    engine.description()
    engine.timeseries_args()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'testdata', 'csvReader_testdata.csv')
    with engine.open_timeseries(file, filters=[]) as ts:
        ts.data("x")
    pass
