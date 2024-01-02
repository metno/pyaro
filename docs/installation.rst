Installation
============

pyaro only needs explicit installation for pyaro developers, i.e. those who implement a new reader.
Users should install a implementation of pyaro like `pyaerocom-readers https://github.com/metno/pyaro-readers`.
User-installation is only required if only the example reader `csv-timeseries` is needed. 

As interface, pyaro has hardly any other dependencies except python and numpy.

You can install pyaerocom via pip or from source.

Via pip
^^^^^^^

This will install the latest pyaro and all its dependencies (numpy).

	# install pyaerocom on machines with numpy
	python -m pip install 'pyaro@git+https://github.com/metno/pyaro.git'


From source:

	# install pyaerocom on machines with numpy
    git clone https://github.com/metno/pyaro.git
    cd pyaro
	python -m pip install .

