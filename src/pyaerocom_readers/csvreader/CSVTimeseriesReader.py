import numpy as np
import pyaerocom_readers as pyaro

class CSVTimeseriesReader(pyaro.TimeseriesReader):
    def open_reader(self, filename_or_obj_or_url):
        """_summary_

        :param filename_or_obj_or_url: path-like object to csv-file
        """
        pass

    def open_parameters(self):
        return ["filename_or_obj_or_url"]

    def get_data(self, varname, *, filters=None) -> pyaro.TimeseriesData:
        return pyaro.TimeseriesData()


    def description(self):
        return "Simple reader of csv-files using python csv-reader"

    def url(self):
        return "https://github.com/metno/pyaerocom-readers"
