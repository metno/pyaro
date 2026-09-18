import unittest

import numpy as np

from pyaro.timeseries.Data import Flag
from pyaro.timeseries.DataStationIdStructured import DataStationIdStructured


class TestDataStationIdStructured(unittest.TestCase):
    def test_append_and_expose_data_and_station_fields(self):
        data = DataStationIdStructured(variable="vmro3", units="ppb")
        data.append(
            value=273.15,
            station="station-a",
            latitude=60.0,
            longitude=10.0,
            altitude=100.0,
            start_time=np.datetime64("2024-01-01T00:00:00"),
            end_time=np.datetime64("2024-01-01T01:00:00"),
            flag=Flag.INVALID,
            standard_deviation=0.5,
        )
        data.append(
            value=274.15,
            station="station-a",
            latitude=60.0,
            longitude=10.0,
            altitude=100.0,
            start_time=np.datetime64("2024-01-01T01:00:00"),
            end_time=np.datetime64("2024-01-01T02:00:00"),
        )

        self.assertEqual(len(data), 2)
        self.assertEqual(data.variable, "vmro3")
        self.assertEqual(data.units, "ppb")
        np.testing.assert_allclose(data.values, [273.15, 274.15])
        np.testing.assert_array_equal(data.stations, ["station-a", "station-a"])
        np.testing.assert_array_equal(data.station_ids, [0, 0])
        np.testing.assert_array_equal(data.latitudes, [60.0, 60.0])
        np.testing.assert_array_equal(data.longitudes, [10.0, 10.0])
        np.testing.assert_array_equal(data.altitudes, [100.0, 100.0])
        np.testing.assert_allclose(data["values"], [273.15, 274.15])
        np.testing.assert_array_equal(data["stations"], ["station-a", "station-a"])
        np.testing.assert_array_equal(data["station_ids"], [0, 0])
        np.testing.assert_array_equal(data["latitudes"], [60.0, 60.0])
        np.testing.assert_array_equal(data["longitudes"], [10.0, 10.0])
        np.testing.assert_array_equal(data["altitudes"], [100.0, 100.0])

        np.testing.assert_array_equal(
            data.start_times,
            np.array(
                ["2024-01-01T00:00:00", "2024-01-01T01:00:00"],
                dtype="datetime64[s]",
            ),
        )
        np.testing.assert_array_equal(data.flags, [Flag.INVALID, Flag.VALID])
        np.testing.assert_array_equal(data["stations"], data.stations)
        self.assertSetEqual(
            set(data.keys()),
            {
                "values",
                "station_ids",
                "start_times",
                "end_times",
                "flags",
                "standard_deviations",
                "stations",
                "latitudes",
                "longitudes",
                "altitudes",
            },
        )

    def test_array_append_deduplicates_stations_and_slice_preserves_metadata(self):
        data = DataStationIdStructured(variable="ozone", units="ug m-3")
        data.append(
            value=np.array([1.0, 2.0, 3.0]),
            station=np.array(["station-a", "station-b", "station-a"]),
            latitude=np.array([60.0, 61.0]),
            longitude=np.array([10.0, 11.0]),
            altitude=np.array([100.0, 110.0]),
            start_time=np.array(
                [
                    "2024-02-01T00:00:00",
                    "2024-02-01T01:00:00",
                    "2024-02-01T02:00:00",
                ],
                dtype="datetime64[s]",
            ),
            end_time=np.array(
                [
                    "2024-02-01T01:00:00",
                    "2024-02-01T02:00:00",
                    "2024-02-01T03:00:00",
                ],
                dtype="datetime64[s]",
            ),
            flag=np.array([Flag.VALID, Flag.INVALID, Flag.VALID]),
            standard_deviation=np.array([0.1, 0.2, 0.3]),
        )

        self.assertEqual(len(data), 3)
        np.testing.assert_array_equal(
            data.stations, ["station-a", "station-b", "station-a"]
        )
        np.testing.assert_array_equal(data.station_ids, [0, 1, 0])
        np.testing.assert_array_equal(data.latitudes, [60.0, 61.0, 60.0])
        np.testing.assert_array_equal(
            data.stations_by_ids([0, 1]), ["station-a", "station-b"]
        )

        sliced = data.slice([True, False, True])
        self.assertEqual(sliced.variable, "ozone")
        self.assertEqual(sliced.units, "ug m-3")
        np.testing.assert_array_equal(sliced.values, [1.0, 3.0])
        np.testing.assert_array_equal(sliced.stations, ["station-a", "station-a"])
