from .Reader import Reader
from .Data import Data
from contextlib import contextmanager


class VariableNameChangingReader(Reader):
    """A pyaro.timeseries.Reader wrapper taking a real Reader implementation and
    changing variable names in the original reader. Example:

        with VariableNameChangingReader(pyaro.open_timeseries(file, filters=[]),
                                        {'SOx': 'oxidised_sulphur'}) as ts:
            for var in ts.variables():
                print(var, ts.data(var))
                # oxidised_sulphur oxidised_sulphur, Gg, [( 0. ...

    """

    def __init__(self, reader: Reader, reader_to_new: dict[str, str], **kwargs,):
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

    def data(self, varname):
        """Get the data from the reader with one of the new variable names.

        :param varname: new variable name
        :return: data with new variable name
        """
        data = self.reader.data(self._new_to_reader.get(varname, varname))
        data._set_variable(varname)
        return data

    def metadata(self):
        """Get the metadata from the reader
        NOT changing the variable name to the newly given ones for the moment

        :return: metadata from the original reader class
        """
        metadata = self._reader.metadata()
        return metadata

    def stations(self):
        return self._reader.stations()

    def variables(self):
        """Variables with new variable names

        :return: iterator of new variables names
        """
        return [self._reader_to_new.get(x, x) for x in self._reader.variables()]

    def close(self):
        self._reader.close()

    @contextmanager
    def read(self,):
        """define read method. All needed parameters should be put into self
        by the __init__ method

        This function is usually called after the Engine's open function.'
        """
        with self._reader.read() as ts:
            yield self
        # return self._reader.read()


