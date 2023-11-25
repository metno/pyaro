

import abc

import numpy as np

from .Data import Data
from .Station import Station


class Filter(abc.ABC):
    """Base-class for all filters used from pyaro-Readers
    """

    def __init__(self, **kwargs):
        """empty initializer required for initializing a filter without restrictions"""
        return

    @abc.abstractmethod
    def args(self) -> dict:
        """retrieve the kwargs possible to retrieve a new object of this filter with filter restrictions

        :return: a dictionary possible to use as kwargs for the new method
        """
        return

    def new(self, **kwargs): # -> Self: requires python >= 3.11
        """retrieve a new Filter with restrictions set in kwargs

        :return: a Filter object with restrictions
        """
        return self.__class__(**kwargs)


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
        self._include = include
        self._exclude = exclude
        return

    def args(self):
        return {'reader_to_new': {}, 'include': [], 'exclude': []}

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
            newvar = self._reader_to_new.get(x, x)
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
        new_var = self._reader_to_new.get(variable, variable)
        return self.has_variable(new_var)

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

    def args(self):
        return {'include': [], 'exclude': []}

    def has_station(self, station) -> bool:
        if len(self._include) > 0:
            if not station in self._include:
                return False
        if station in self._exclude:
            return False
        return True

    def filter_stations(self, stations: dict[str, Station]) -> dict[str, Station]:
        return {s: v for s, v in stations.items() if self.has_station(s)}

class CountryFilter(StationReductionFilter):

    def __init__(self, include: [str]=[], exclude: [str]=[]):
        """Filter countries by ISO2 names (capitals!)

        :param include: countries to include, defaults to [], meaning all countries
        :param exclude: countries to exclude, defaults to [], meaning none
        """
        self._include = set(include)
        self._exclude = set(exclude)
        return

    def args(self):
        return {'include': [], 'exclude': []}

    def has_country(self, country) -> bool:
        if len(self._include) > 0:
            if not country in self._include:
                return False
        if country in self._exclude:
            return False
        return True

    def filter_stations(self, stations: dict[str, Station]) -> dict[str, Station]:
        return {s: v for s, v in stations.items() if self.has_country(v.country)}






