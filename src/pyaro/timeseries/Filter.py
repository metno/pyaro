

import abc
import inspect

import numpy as np

from .Data import Data, Flag
from .Station import Station





class Filter(abc.ABC):
    """Base-class for all filters used from pyaro-Readers
    """

    def __init__(self, **kwargs):
        """constructor of Filters. All filters must have a default constructor without kwargs
        for an empty filter object"""
        return

    def args(self) -> list:
        """retrieve the kwargs possible to retrieve a new object of this filter with filter restrictions

        :return: a dictionary possible to use as kwargs for the new method
        """
        ba = inspect.signature(self.__class__.__init__).bind(0)
        ba.apply_defaults()
        args = ba.arguments
        args.pop('self')
        return args

    @abc.abstractmethod
    def init_kwargs(self) -> dict:
        """return the init kwargs"""


    @abc.abstractmethod
    def name(self) -> str:
        """Return a unique name for this filter

        :return: a string to be used by FilterFactory
        """

    def filter_data(self, data: Data, stations: [Station], variables: [str]) -> Data:
        """Filtering of data

        :param data: Data of e.g. a Reader.data(varname) call
        :param stations: List of stations, e.g. from a Reader.stations() call
        :param variables: variables, i.e. from a Reader.variables() call
        :return: a updated Data-object with this filter applied
        """
        return data

    def filter_stations(self, stations: dict[str, Station]) -> dict[str, Station]:
        """Filtering of stations list

        :param stations: List of stations, e.g. from a Reader.stations() call
        :return: dict of filtered stations
        """
        return stations

    def filter_variables(self, variables: [str]) -> [str]:
        """Filtering of variables

        :param variables: List of variables, e.g. from a Reader.variables() call
        :return: List of filtered variables.
        """
        return variables

    def __repr__(self):
        return f"{type(self).__name__}(**{self.init_kwargs()})"

class FilterFactoryException(Exception):
    pass

class FilterFactory():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FilterFactory, cls).__new__(cls)
            cls.instance._filters = {}
        return cls.instance

    def register(self, filter: Filter):
        """Register a new filter to the factory
        with a filter object (might be empty)

        :param filter: a filter implementation
        """
        if filter.name() in self._filters:
            raise FilterFactoryException(
                f"Cannot use {filter}: {filter.name()} already in use by {self.get(filter.name())}"
            )
        self._filters[filter.name()] = filter

    def get(self, name, **kwargs):
        """Get a filter by name. If kwargs are given, they will be send to the
        filters new method

        :param name: a filter-name
        :return: a filter, optionally initialized
        """
        filter = self._filters[name]
        return filter.__class__(**kwargs)

    def list(self):
        return self._filters.keys()

filters = FilterFactory()

class VariableNameFilter(Filter):
    """Filter to change variable-names and/or include/exclude variables"""

    def __init__(self, reader_to_new: dict[str, str]={}, include: [str]=[], exclude: [str]=[]):
        """Create a new variable name filter.

        :param reader_to_new: dictionary from readers-variable names to new variable-names,
            e.g. used in your project, defaults to {}
        :param include: list of variables to include only (new names if changed), defaults to []
            meaning keep all variables unless excluded.
        :param exclude: list of variables to exclude (new names if changed), defaults to []
        """
        self._reader_to_new = reader_to_new
        self._new_to_reader = {v: k for k, v in reader_to_new.items()}
        self._include = set(include)
        self._exclude = set(exclude)
        return

    def init_kwargs(self):
        return {"reader_to_new": self._reader_to_new,
                "include": list(self._include),
                "exclude": list(self._exclude)}

    def name(self):
        return "variables"

    def reader_varname(self, new_variable: str) -> str:
        """convert a new variable name to a reader-variable name

        :param new_variable: variable name after translation
        :return: variable name in the original reader
        """
        return self._new_to_reader.get(new_variable, new_variable)

    def new_varname(self, reader_variable: str) -> str:
        """convert a reader-variable to a new variable name

        :param reader_variable: variable as used in the reader
        :return: variable name after translation
        """
        return self._reader_to_new.get(reader_variable, reader_variable)

    def filter_data(self, data, stations, variables):
        """Translate data's variable"""
        data._set_variable(self._reader_to_new.get(data.variable, data.variable))
        return data

    def filter_variables(self, variables: [str]) -> [str]:
        """change variable name and reduce variables applying include and exclude parameters

        :param variables: variable names as in the reader
        :return: valid variable names in translated nomenclature
        """
        newlist = []
        for x in variables:
            newvar = self.new_varname(x)
            if self.has_variable(newvar):
                newlist.append(newvar)
        return newlist


    def has_variable(self, variable) -> bool:
        """check if a variable-name is in the list of variables applying include and exclude

        :param variable: variable name in translated, i.e. new scheme
        :return: True or False
        """
        if len(self._include) > 0:
            if not variable in self._include:
                return False
        if variable in self._exclude:
            return False
        return True

    def has_reader_variable(self, variable) -> bool:
        """Check if variable-name is in the list of variables applying include and exclude

        :param variable: variable as returned from the reader
        :return: True or False
        """
        new_var = self.new_varname(variable)
        return self.has_variable(new_var)

filters.register(VariableNameFilter())


class DataIndexFilter(Filter):
    """A abstract baseclass implementing filter_data by an abstract method
    filter_data_idx"""
    @abc.abstractmethod
    def filter_data_idx(self, data: Data, stations: dict[str, Station], variables: str):
        """Filter data to an index which can be applied to Data.slice(idx) later

        :return: a index for Data.slice(idx)
        """
        pass

    def filter_data(self, data: Data, stations: dict[str, Station], variables: str):
        idx = self.filter_data_idx(data, stations, variables)
        return data.slice(idx)


class StationReductionFilter(DataIndexFilter):
    """Abstract method for all filters, which work on reducing the number of stations only.

    The filtering of stations has to be implemented by subclasses, while filtering of data
    is already implemented.
    """
    @abc.abstractmethod
    def filter_stations(self, stations: dict[str, Station]) -> dict[str, Station]:
        pass

    def filter_data_idx(self, data: Data, stations: dict[str, Station], variables: str) -> Data:
        stat_names = self.filter_stations(stations).keys()
        dstations = data.stations
        stat_names = np.fromiter(stat_names, dtype=dstations.dtype)
        index = np.in1d(dstations, stat_names)
        return index


class StationFilter(StationReductionFilter):

    def __init__(self, include: [str]=[], exclude: [str]=[]):
        self._include = set(include)
        self._exclude = set(exclude)
        return

    def init_kwargs(self):
        return {"include": list(self._include),
                "exclude": list(self._exclude)}

    def name(self):
        return "stations"

    def has_station(self, station) -> bool:
        if len(self._include) > 0:
            if not station in self._include:
                return False
        if station in self._exclude:
            return False
        return True

    def filter_stations(self, stations: dict[str, Station]) -> dict[str, Station]:
        return {s: v for s, v in stations.items() if self.has_station(s)}

filters.register(StationFilter())



class CountryFilter(StationReductionFilter):

    def __init__(self, include: [str]=[], exclude: [str]=[]):
        """Filter countries by ISO2 names (capitals!)

        :param include: countries to include, defaults to [], meaning all countries
        :param exclude: countries to exclude, defaults to [], meaning none
        """
        self._include = set(include)
        self._exclude = set(exclude)
        return

    def init_kwargs(self):
        return {"include": list(self._include),
                "exclude": list(self._exclude)}

    def name(self):
        return "countries"

    def has_country(self, country) -> bool:
        if len(self._include) > 0:
            if not country in self._include:
                return False
        if country in self._exclude:
            return False
        return True

    def filter_stations(self, stations: dict[str, Station]) -> dict[str, Station]:
        return {s: v for s, v in stations.items() if self.has_country(v.country)}

filters.register(CountryFilter())


class FlagFilter(DataIndexFilter):

    def __init__(self, include: [Flag]=[], exclude: [Flag]=[]):
        """Filter data by Flags

        :param include: flags to include, defaults to [], meaning all flags
        :param exclude: flags to exclude, defaults to [], meaning none
        """
        self._include = set(include)
        if len(include) == 0:
            all_include = set([f for f in Flag])
        else:
            all_include = self._include
        self._exclude = set(exclude)
        self._valid = all_include.difference(self._exclude)
        return

    def name(self):
        return "flags"

    def init_kwargs(self):
        return {"include": list(self._include),
                "exclude": list(self._exclude)}


    def filter_data_idx(self, data: Data, stations: dict[str, Station], variables: str) -> Data:
        validflags = np.fromiter(self._valid, dtype=data.flags.dtype)
        index = np.in1d(data.flags.dtype, validflags)
        return index

filters.register(FlagFilter())


if __name__ == "__main__":
    for name, fil in filters._filters.items():
        assert(name == fil.name())
        print(name, fil.args())
        print(fil)
