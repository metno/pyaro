# pyaro - Metadata

Pyaro offers free-form metadata fields/dictionaries for
[`Reader.metadata()`](src/pyaro/timeseries/Reader.py) and the optional field in
[`pyaro.timeseries.Station.metadata`](src/pyaro/timeseries/Station.py).

## Reader metadata

## Conventions

The reader is allowed to support several conventions of metadata. Conventions are case-insensitive alphanumeric titles, and can be comma-separated. Conventions exist because different user-groups might use pyaro with different terms. Conventions can be numbered semantically with mayor.minor versions. minor version updates are backward compatible, Mayor version can be incompatible

One can check if a convention is supported with
[`Reader.convention_supported()`](src/pyaro/timeseries/Reader.py). The available
conventions are returned by [`Reader.conventions()`](src/pyaro/timeseries/Reader.py):

```python
with engines['csv_timeseries'].open(
    filename=TEST_FILE,
    ) as ts:
    print(f"Conventions: {ts.conventions()}")
    if ts.convention_supported("pyaerocom-0.0"):
        print ts.metadata["revision"]
```

## General metadata for all conventions

|field | | default | comment |
|--------|-----|-----|-------------|
|revision| required | 0 | free-form revision, usually datestamp or combination of datestamps, should be alphabetically increasing for newer revisions |
|conventions| required (assume pyaerocom-0.0 when not specified) | the version of metadata conventions this reader follows |

## Station Metadata

### pyaerocom-0.0, default

|field | | default if given | comment|
|--------|-----|-----|-------------|
| long_name | optional |  | not used? |
| country | optional |   | ISO2 code |
| url | optional | | |
|station_type|optional| |rural/urban/...|
|display_name|optional| | non-unique nice display name of stations|
|description|optional|  |free-form human readable description about station|


### forbidden fields

The following fields are currently planned for futuren internal use of pyaro
and should not be used:
|field |comment|
|--------|-------------|
|_pyaro | might be an additional dictionary for internal usage |
|station| unique name of the station |
|latitude| avoid duplicate with data-section |
|longitude | avoid duplicate with data-section |
| altitude | avoid duplicate with data-section |
