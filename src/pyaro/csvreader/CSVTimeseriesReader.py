import csv
import numpy as np
from pyaro.timeseries import Data, Reader, Station

class CSVTimeseriesReader(Reader):
    def open_reader(self,
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
                    filters=[]):
        """open a new csv timeseries-reader

        :param filename_or_obj_or_url: path-like object to csv-file
        """
        self.filename = filename
        self.stations = {}
        self.data = {} # var -> station -> {}
        with open(self.filename, newline='') as csvfile:
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



    def open_parameters(self):
        return ["filename_or_obj_or_url", "columns", "csvreader_kwargs", "variable_units", "filters"]

    def get_data(self, varname, *, filters=None) -> pyaro.TimeseriesData:
        return pyaro.TimeseriesData()

    def stations(self) -> dict[str, pyaro.TimeseriesStation]:
        return self.stations


    def description(self):
        return "Simple reader of csv-files using python csv-reader"

    def url(self):
        return f"https://github.com/metno/pyaerocom-readers"


if __name__ == "__main__":
    # test-code

