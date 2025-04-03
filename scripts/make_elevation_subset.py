import xarray as xr


FILE_PATH = (
    "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/GTOPO30/merged/N.nc"
)

with xr.open_dataset(FILE_PATH) as ds:
    subset = ds.sel(lon=slice(-2, 10), lat=slice(57, 61))

    subset.to_netcdf("gtopo30_subset.nc")
