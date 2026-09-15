import pyaro.timeseries
import unittest
import os


class TestCSVTimeSeriesReader(unittest.TestCase):
    file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "testdata",
        "datadir",
        "csvReader_testdata.csv",
    )

    def test_conventions(self):
        engine = pyaro.list_timeseries_engines()["csv_timeseries"]
        with engine.open(self.file) as reader:
            conventions = reader.conventions()
            self.assertIsInstance(conventions, list)
            self.assertEqual(len(conventions), 1)
            for convention in conventions:
                self.assertIsInstance(convention, str)
                self.assertTrue(reader.convention_supported(convention))
                self.assertEqual(reader._convention_name(convention), "pyaerocom")
                self.assertGreaterEqual(reader._convention_version(convention)[0], 0)
                self.assertGreaterEqual(reader._convention_version(convention)[1], 0)

            self.assertTrue(reader.convention_supported("pyaerocom-0.0"))
            reader.close()
