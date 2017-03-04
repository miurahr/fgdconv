JPGISGML2Gml
===============

This is a converter program to convert from Fundamental Geospatial Data provided
by Geographic Information Authority of Japan(GSI) to GML.

国土地理院 `基盤地図情報`_ 基本項目 JPGIS(GML) V4.0形式のデータをGMLに変換するコンバータです。

.. _基盤地図情報: http://www.gsi.go.jp/kiban/

Requirement
-----------

Python 2.7.13, Python 3.4 or later. Python 3.5 or later is recommended.
実行には Python 3.4 または Python 2.7.13 が必要です。 Python バージョン3.5以降が推奨されます。

Tested versions
^^^^^^^^^^^^^^^

* Python 2.7.13
* Python 3.4.6
* Python 3.5.3
* Python 3.6.0


Basic usage
-----------

SYNOPSIS::

    jpgisgml2gml [<Input FGD-GML filename>  [<Output GML filename>]]

Convert Fundamental Geospatial Data to GML.
基盤地図情報基本項目XMLデータを、GMLに変換する::

    $ jpgisgml2gml FG-GML-533946-AdmArea-20140701-0001.xml AdmArea.gml

Convert GML to Shapefile GMLを、Shapeに変換する::

    $ ogr2ogr -f "ESRI Shapefile" -lco "ENCODING=UTF-8" AdmArea AdmArea.gml


License and copyright
---------------------

::

    The MIT License (MIT)

    Copyright (c) 2017 Hiroshi Miura
                  2014 mizutuu

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

