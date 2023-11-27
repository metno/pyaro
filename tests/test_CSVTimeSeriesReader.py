import unittest
import os

import numpy as np
from pyaro.timeseries.Filter import StationFilter, CountryFilter
from pyaro.csvreader.CSVTimeseriesReader import CSVTimeseriesEngine
from pyaro.timeseries.Wrappers import VariableNameChangingReader


class TestCSVTimeSeriesReader(unittest.TestCase):
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'testdata', 'csvReader_testdata.csv')
    def test_init(self):
        engine = CSVTimeseriesEngine()
        self.assertEquals(engine.url(), "https://github.com/metno/pyaro")
        # just see that it doesn't fails
        engine.description()
        engine.args()
        with engine.open(self.file, filters=[]) as ts:
            count = 0
            for var in ts.variables():
                count += len(ts.data(var))
            self.assertEqual(count, 208)
            self.assertEqual(len(ts.stations()), 2)

        with engine.open(self.file, filters=[StationFilter(exclude=['station1'])]) as ts:
            for var in ts.variables():
                self.assertEqual(len(ts.data(var).slice(np.array([0,1,2]))), 3)
            self.assertEqual(len(ts.stations()), 1)


    # wrapper-test
    def test_wrappers(self):
        engine = CSVTimeseriesEngine()
        newsox = 'oxidised_sulphur'
        with VariableNameChangingReader(engine.open(self.file, filters=[]),
                                        {'SOx': newsox}) as ts:
            self.assertEqual(ts.data(newsox).variable, newsox)
        pass

if __name__ == "__main__":
    unittest.main()
