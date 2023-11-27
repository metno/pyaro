import unittest
import os

import numpy as np
import pyaro
from pyaro.timeseries.Filter import StationFilter, CountryFilter
from pyaro.timeseries.Wrappers import VariableNameChangingReader


class TestCSVTimeSeriesReader(unittest.TestCase):
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'testdata', 'csvReader_testdata.csv')
    def test_init(self):
        engine = pyaro.list_timeseries_engines()['csv_timeseries']
        self.assertEqual(engine.url(), "https://github.com/metno/pyaro")
        # just see that it doesn't fails
        engine.description()
        engine.args()
        with engine.open(self.file, filters=[]) as ts:
            count = 0
            for var in ts.variables():
                count += len(ts.data(var))
            self.assertEqual(count, 208)
            self.assertEqual(len(ts.stations()), 2)

    def test_stationfilter(self):
        engine = pyaro.list_timeseries_engines()['csv_timeseries']
        with engine.open(self.file, filters=[StationFilter(exclude=['station1'])]) as ts:
            count = 0
            for var in ts.variables():
                count += len(ts.data(var))
            self.assertEqual(count, 104)
            self.assertEqual(len(ts.stations()), 1)

    def test_wrappers(self):
        engine = pyaro.list_timeseries_engines()['csv_timeseries']
        newsox = 'oxidised_sulphur'
        with VariableNameChangingReader(engine.open(self.file, filters=[]),
                                        {'SOx': newsox}) as ts:
            self.assertEqual(ts.data(newsox).variable, newsox)
        pass

if __name__ == "__main__":
    unittest.main()
