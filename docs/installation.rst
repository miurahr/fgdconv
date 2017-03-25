Installation
============

Fgdconv is distributed in several package format.
Here is a list of package formats.

* source tar.gz distribution
* linux tar.gz binary distribution
* wheel package
* windows binary installer
* rpm binary and source package for linux
* dump of repository

Dependency installattion
------------------------

Fgdconv is a program written by Python language.
It is necessary to install Python language environment on your
Operating System used.
Fgdconv also depends OSGeo's GDAL library and its python binding.
Please install GDAL before install Fgdconv.

Windows
^^^^^^^

There are several way to install Python on Windows.
Our recommend is an official binary distribution from python.org
https://www.python.org/downloads/windows/

You can get GDAL and its Python binding from
http://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
as in Wheel binary format for Windows.

RHEL/CentOS/Fedora/OpenSUSE
^^^^^^^^^^^^^^^^^^^^^^^^^^^

GDAL is distributed as in an official package.
You can install a GDAL package by

    $ yum install gdal-devel

Please watch a version of GDAL whether it is 1.9.2, 2.0.2 or 2.1.3..
depend on your platform.

Then install python bindings.

    $ pip install wheel
    $ pip install pygdal==1.9.2

where version number is depend on your GDAL version.

Debian/Ubuntu/Mint
^^^^^^^^^^^^^^^^^^

GDAL is distributed as in an official package.
You can install a GDAL package by

    $ apt install libgdal1-dev

TPlease watch a version of GDAL whether it is 1.9.2, 2.0.2 or 2.1.3..
depend on your platform.

Then install python bindings.

    $ pip install wheel
    $ pip install pygdal==2.1.3

where version number is depend on your GDAL version.


Arch/Gentoo
^^^^^^^^^^^

TBD.


Install other dependency
------------------------

It is also necessary some dependencies for Fgdconv.
Install it with wheel.

    $ pip install -rrequirements.txt

If you are willing to join a development effort, please run

    $ pip install -rrequirements.txt -rrequirements-dev.txt


Install from wheel
------------------

It is recommend to use with virtualenv environment for POSIX system (e.g. Linux, MacOSX).

    $ pip install https://github.com/miurahr/fgdconv/releases/download/v0.3.0/fgdconv-0.3.0-py2.py3-none-any.whl


