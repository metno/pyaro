import unittest
import os

import numpy as np
import pyaro
import pyaro.timeseries
from pyaro.timeseries.Wrappers import VariableNameChangingReader


class TestCSVTimeSeriesReader(unittest.TestCase):
    file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "testdata",
        "csvReader_testdata.csv",
    )

    def test_init(self):
        engine = pyaro.list_timeseries_engines()["csv_timeseries"]
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

    def test_data(self):
        engines = pyaro.list_timeseries_engines()
        with engines["csv_timeseries"].open(
            filename=self.file,
            filters=[pyaro.timeseries.filters.get("countries", include=["NO"])],
        ) as ts:
            for var in ts.variables():
                # stations
                ts.data(var).stations
                # start_times
                ts.data(var).start_times
                # stop_times
                ts.data(var).end_times
                # latitudes
                ts.data(var).latitudes
                # longitudes
                ts.data(var).longitudes
                # altitudes
                ts.data(var).altitudes
                # values
                ts.data(var).values
                # flags
                ts.data(var).flags
        self.assertTrue(True)

    def test_append_data(self):
        engines = pyaro.list_timeseries_engines()
        with engines["csv_timeseries"].open(
            filename=self.file,
            filters=[pyaro.timeseries.filters.get("countries", include=["NO"])],
        ) as ts:
            var = next(iter(ts.variables()))
            data = ts.data(var)
            old_size = len(data)
            rounds = 3
            for _ in range(rounds):
                data.append(
                    value=data.values,
                    station=data.stations,
                    start_time=data.start_times,
                    end_time=data.end_times,
                    latitude=data.latitudes,
                    longitude=data.longitudes,
                    altitude=data.altitudes,
                    flag=data.flags,
                    standard_deviation=data.standard_deviations,
                )
            self.assertEqual(
                (2**rounds) * old_size, len(data), "data append by array"
            )

    def test_stationfilter(self):
        engine = pyaro.list_timeseries_engines()["csv_timeseries"]
        sfilter = pyaro.timeseries.filters.get("stations", exclude=["station1"])
        with engine.open(self.file, filters=[sfilter]) as ts:
            count = 0
            for var in ts.variables():
                count += len(ts.data(var))
            self.assertEqual(count, 104)
            self.assertEqual(len(ts.stations()), 1)

    def test_boundingboxfilter_exception(self):
        with self.assertRaises(pyaro.timeseries.Filter.BoundingBoxException):
            pyaro.timeseries.filters.get("bounding_boxes", include=[(-90, 0, 90, 180)])

    def test_boundingboxfilter(self):
        engine = pyaro.list_timeseries_engines()["csv_timeseries"]
        sfilter = pyaro.timeseries.filters.get(
            "bounding_boxes", include=[(90, 180, -90, 0)]
        )
        self.assertEqual(sfilter.init_kwargs()["include"][0][3], 0)
        with engine.open(self.file, filters=[sfilter]) as ts:
            count = 0
            for var in ts.variables():
                count += len(ts.data(var))
            self.assertEqual(len(ts.stations()), 1)
            self.assertEqual(count, 104)
        sfilter = pyaro.timeseries.filters.get(
            "bounding_boxes", exclude=[(90, 0, -90, -180)]
        )
        self.assertEqual(sfilter.init_kwargs()["exclude"][0][3], -180)
        with engine.open(self.file, filters=[sfilter]) as ts:
            count = 0
            for var in ts.variables():
                count += len(ts.data(var))
            self.assertEqual(len(ts.stations()), 1)
            self.assertEqual(count, 104)

    def test_timebounds_exception(self):
        with self.assertRaises(pyaro.timeseries.Filter.TimeBoundsException):
            pyaro.timeseries.filters.get(
                "time_bounds",
                start_include=[("1903-01-01 00:00:00", "1901-12-31 23:59:59")],
            )

    def test_timebounds(self):
        engine = pyaro.list_timeseries_engines()["csv_timeseries"]
        tfilter = pyaro.timeseries.filters.get(
            "time_bounds",
            startend_include=[("1997-01-01 00:00:00", "1997-02-01 00:00:00")],
            end_exclude=[("1997-01-05 00:00:00", "1997-01-07 00:00:00")],
        )
        self.assertEqual(
            tfilter.init_kwargs()["startend_include"][0][1], "1997-02-01 00:00:00"
        )
        with engine.open(self.file, filters=[tfilter]) as ts:
            count = 0
            for var in ts.variables():
                count += len(ts.data(var))
            self.assertEqual(len(ts.stations()), 2)
            self.assertEqual(count, 112)

    def test_flagfilter(self):
        engine = pyaro.list_timeseries_engines()["csv_timeseries"]
        ffilter = pyaro.timeseries.filters.get(
            "flags",
            include=[
                pyaro.timeseries.Flag.VALID,
                pyaro.timeseries.Flag.BELOW_THRESHOLD,
            ],
        )
        self.assertEqual(
            ffilter.init_kwargs()["include"][0], pyaro.timeseries.Flag.VALID
        )
        with engine.open(self.file, filters=[ffilter]) as ts:
            count = 0
            for var in ts.variables():
                count += len(ts.data(var))
            self.assertEqual(len(ts.stations()), 2)
            self.assertEqual(count, 208)

        ffilter = pyaro.timeseries.filters.get(
            "flags", include=[pyaro.timeseries.Flag.INVALID]
        )
        with engine.open(self.file, filters=[ffilter]) as ts:
            count = 0
            for var in ts.variables():
                count += len(ts.data(var))
            self.assertEqual(len(ts.stations()), 2)
            self.assertEqual(count, 0)

    def test_wrappers(self):
        engine = pyaro.list_timeseries_engines()["csv_timeseries"]
        newsox = "oxidised_sulphur"
        with VariableNameChangingReader(
            engine.open(self.file, filters=[]), {"SOx": newsox}
        ) as ts:
            self.assertEqual(ts.data(newsox).variable, newsox)
        pass

    def test_variables_filter(self):
        engine = pyaro.list_timeseries_engines()["csv_timeseries"]
        newsox = "oxidised_sulphur"
        vfilter = pyaro.timeseries.filters.get(
            "variables", reader_to_new={"SOx": newsox}
        )
        with engine.open(self.file, filters=[vfilter]) as ts:
            self.assertEqual(ts.data(newsox).variable, newsox)
        pass

    def test_filterFactory(self):
        filters = pyaro.timeseries.filters.list()
        print(filters["variables"])
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
