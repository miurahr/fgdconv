Developer information
=====================


Build environment
-----------------

Recommend to use `Virtualenv` to prepare python environment::

    $ virtualenv --python=python3.5 venv
    $ . venv/bin/activate
    $ pip install -rrequirements.txt -rrequirements-dev.txt
    $ pip wheel .


Test environment
----------------

JpGisGml2Gml project use `tox` for test.
It is recommended to use `pyenv` to install python versions::

    $ pyenv install 2.7.13
    $ pyenv install 3.4.6
    $ pyenv install 3.5.3
    $ pyenv install 3.6.0
    $ pyenv virtualenv 3.6.0 venv
    $ pyenv local venv 2.7.13 3.4.6 3.5.3 3.6.0
    $ sudo apt install libgdal-dev
    $ pip install -rrequirements.txt -rrequirements-dev.txt
    $ PYGDAL_VER=`gdal-config --version`.3 tox


Tested versions
---------------

* Python 2.7.13
* Python 3.4.6
* Python 3.5.3
* Python 3.6.0


Dependency System libraries
---------------------------

* libgdal-dev


Dependency python runtime libraries
-----------------------------------

* pygdal
* lxml

