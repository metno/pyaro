from .Reader import Reader
from .Data import Data


class VariableNameChangingReaderData(Data):
    def __init__(self, data: Data, varname: str):
        self._data = data
        self._variable = varname

    def keys(self):
        return self._data.keys()

    def slice(self, index):
        return VariableNameChangingReaderData(self._data.slice(index), self._variable)

    def __len__(self) -> int:
        return len(self._data)

    @property
    def variable(self) -> str:
        return self._variable

    @property
    def units(self) -> str:
        return self._data.units

    @property
    def values(self):
        return self._data.values

    @property
    def stations(self):
        return self._data.stations

    @property
    def latitudes(self):
        return self._data.latitudes

    @property
    def longitudes(self):
        return self._data.altitudes

    @property
    def altitudes(self):
        return self._data.altitudes

    @property
    def start_times(self):
        return self._data.start_times

    @property
    def end_times(self):
        return self._data.end_times

    @property
    def flags(self):
        return self._data.flags

    @property
    def standard_deviations(self):
        return self._data.standard_deviations


class VariableNameChangingReader(Reader):
    """A pyaro.timeseries.Reader wrapper taking a real Reader implementation and
    changing variable names in the original reader. Example:

        with VariableNameChangingReader(pyaro.open_timeseries(file, filters=[]),
                                        {'SOx': 'oxidised_sulphur'}) as ts:
            for var in ts.variables():
                print(var, ts.data(var))
                # oxidised_sulphur oxidised_sulphur, Gg, [( 0. ...

    """

    def __init__(self, reader: Reader, reader_to_new: dict[str, str]):
        """Initialize the variable name changes of Reader

        :param reader: The Reader instance to change variable names on
        :param reader_to_new: dictionary translating readers variable names to
            new names
        """
        self._reader = reader
        self._reader_to_new = reader_to_new
        self._new_to_reader = {v: k for k, v in reader_to_new.items()}

        return

    @property
    def reader(self):
        """Return the original reader

        :return: original reader without modifications, see __init__
        """
        return self._reader

    def data(self, varname) -> Data:
        """Get the data from the reader with one of the new variable names.

        :param varname: new variable name
        :return: data with new variable name
        """
        data = self.reader.data(self._new_to_reader.get(varname, varname))
        return VariableNameChangingReaderData(data, varname)

    def stations(self):
        return self._reader.stations()

    def metadata(self):
        return self._reader.metadata()

    def variables(self):
        """Variables with new variable names

        :return: iterator of new variables names
        """
        return [self._reader_to_new.get(x, x) for x in self._reader.variables()]

    def close(self):
        self._reader.close()
