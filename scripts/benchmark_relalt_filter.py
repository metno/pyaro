import pyaro
import csv
import time
import random
import os

# Generate test-data
if not os.path.exists("tmp_data.csv"):
    with open("tmp_data.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        variable = "NOx"
        unit = "Gg"
        for i in range(75000):
            name = f"station{i}"
            lat = random.uniform(30.05, 81.95)
            lon = random.uniform(-29.95, 89.95)
            value = random.uniform(0, 1)
            altitude = random.randrange(0, 1000)
            start_time = "1997-01-01 00:00:00"
            end_time = "1997-01-02 00:00:00"


            writer.writerow((variable, name, lat, lon, value, unit, start_time, end_time, altitude))

# Benchmark
engines = pyaro.list_timeseries_engines()
with engines["csv_timeseries"].open(
    filename="tmp_data.csv",
    filters=[pyaro.timeseries.filters.get("relaltitude", topo_file = "../tests/testdata/datadir_elevation/topography.nc", rdiff=90)],
    columns={
        "variable": 0,
        "station": 1,
        "longitude": 2,
        "latitude": 3,
        "value": 4,
        "units": 5,
        "start_time": 6,
        "end_time": 7,
        "altitude": 8,
        "country": "NO",
        "standard_deviation": "NaN",
        "flag": "0",
    }) as ts:
    start_time = time.perf_counter()
    ts.stations()
    end_time = time.perf_counter()


print(f"Total time: {end_time-start_time:.3f} seconds")
