import xarray as xr

# Script which extracts only the first time point and topography value from the emep topography
# file to reduce data for the tests.
data = xr.open_dataset("/lustre/storeB/project/fou/kl/emep/Auxiliary/topography.nc")

start_time = data["time"][0]

data = data.sel(time=slice(start_time))

data = data["topography"]


data.to_netcdf("tests/testdata/datadir_elevation/topography.nc")