==========
Change Log
==========

All notable changes to this project will be documented in this file.

`Unreleased`_
=============

Added
-----
* test: CI test with AppVeyor for windows, Tavis-CI on Linux.
* test: Record test coverage on coveralls.
* test: Python gdal binary for test on windows.
* test: Add test script.
* test: Add coverage test.

Changed
-------
* Update FGD schema to V4.1
* Sax handler constructor accept an output file path instead of file object.
* Refactoring main method.
* Refactoring test.

Fixed
-----
* Add copyright for test utility xml_compare.
* Add license of FGD schema file.
* Load schema file with explicit UTF-8 encoding.


`v0.3.0`_
=========

Added
-----
* Support Shapefile output and defualt format is GML.

Changed
-------
* Introduce fgdconv/sax package directory and
  rename fgd2gml.py to fgd2gml_handler.py
* Classname change from ogrconv to ogr2ogr.
* Classname change from cli to fgd2ogr.

Fixed
-----
* Make test data clean against FGD license.


`v0.2.0`_
=========

Added
-----
* Support conversion from JGD2000 to WGS84 coordination.
* Documentation with Sphinx document processor.

Changed
-------
* Not support STDIN and STDOUT for command line.
* Rename project 'fgdconv' means FGD converter,
  now FGD: fundamental geospatial data.

`v0.1.0`_
=========

Added
-----
* Add build scripts.
* Add test cases.
* Add commandline help message.
* Add Pip requirements.txt

Changed
-------
* Introduce package jpgisgml2gml.
* Accept Commandline argument.
* Documentation with ReST format.

Fixed
-----
* PEP8 warnings.
* Support both Python3 (>=3.4) and Python 2 (=2.7.x)
* Workaround known bug for build bdist_wininst on Linux

v0.0.1
======

* Original initial work.

.. _Unreleased: https://github.com/miurahr/fgdconv/compare/v0.3.0...HEAD
.. _v0.3.0: https://github.com/miurahr/fgdconv/compare/v0.2.0...v0.3.0
.. _v0.2.0: https://github.com/miurahr/fgdconv/compare/v0.1.0...v0.2.0
.. _v0.1.0: https://github.com/miurahr/fgdconv/compare/v0.0.1...v0.1.0
