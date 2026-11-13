import unittest

from pyaro.timeseries.Filter import (
    BoundingBoxException,
    ProjectedBoundingBoxFilter,
)
from pyaro.timeseries.Station import Station


class TestProjectedBoundingBoxFilter(unittest.TestCase):
    projection_lcc = (
        "+proj=lcc +lat_1=63.3 +lat_2=63.3 +lat_0=63.3 +lon_0=15 "
        "+x_0=0 +y_0=0 +R=6371000 +units=m +no_defs"
    )

    @staticmethod
    def station(station, longitude, latitude):
        return Station(
            fields={
                "station": station,
                "latitude": latitude,
                "longitude": longitude,
                "altitude": 0.0,
                "long_name": station,
                "country": "",
                "url": "",
            }
        )

    def stations(self):
        return {
            "center": self.station("center", longitude=15.0, latitude=63.3),
            "outside": self.station("outside", longitude=15.1, latitude=63.4),
        }

    def test_identity_projection(self):
        bbox_filter = ProjectedBoundingBoxFilter(
            include=[(63.35, 15.05, 63.25, 14.95)],
            projection="EPSG:4326",
        )

        self.assertEqual(
            set(bbox_filter.filter_stations(self.stations())),
            {"center"},
        )

    def test_epsg3035_projection(self):
        bbox_filter = ProjectedBoundingBoxFilter(
            include=[(4480000.0, 4575000.0, 4470000.0, 4565000.0)],
            projection="EPSG:3035",
        )

        self.assertEqual(
            set(bbox_filter.filter_stations(self.stations())),
            {"center"},
        )

    def test_lambert_conformal_conic_projection(self):
        bbox_filter = ProjectedBoundingBoxFilter(
            include=[(1000.0, 1000.0, -1000.0, -1000.0)],
            projection=self.projection_lcc,
        )

        self.assertEqual(
            set(bbox_filter.filter_stations(self.stations())),
            {"center"},
        )

    def test_init_kwargs_preserve_projection(self):
        bbox_filter = ProjectedBoundingBoxFilter(
            include=[(1000.0, 1000.0, -1000.0, -1000.0)],
            projection=self.projection_lcc,
        )

        reconstructed = ProjectedBoundingBoxFilter(**bbox_filter.init_kwargs())

        self.assertEqual(reconstructed.init_kwargs(), bbox_filter.init_kwargs())
        self.assertEqual(
            set(reconstructed.filter_stations(self.stations())),
            {"center"},
        )

    def test_projected_bounding_box_validation(self):
        with self.assertRaises(BoundingBoxException):
            ProjectedBoundingBoxFilter(include=[(1.0, 2.0, 3.0)])

        with self.assertRaises(BoundingBoxException):
            ProjectedBoundingBoxFilter(include=[(1.0, 2.0, 3.0, 4.0)])

        # Projected coordinates may be far outside geographic degree ranges.
        ProjectedBoundingBoxFilter(
            include=[(4480000.0, 4575000.0, 4470000.0, 4565000.0)],
            projection="EPSG:3035",
        )


if __name__ == "__main__":
    unittest.main()
