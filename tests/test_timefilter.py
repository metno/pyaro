from datetime import datetime

from pyaro.timeseries.Filter import TimeBoundsFilter


def test_timemax():
    bounds = TimeBoundsFilter(start_include=[("2023-01-01 00:00:00", "2024-01-01 00:00:00")])

    envelope = bounds.envelope()
    assert envelope[0] == datetime.fromisoformat("2023-01-01 00:00:00")
    assert envelope[1] == datetime.fromisoformat("2024-01-01 00:00:00")
