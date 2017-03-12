FGDConv
=======

This is a converter program to convert from Fundamental Geospatial Data provided
by Geographic Information Authority of Japan(GSI) to GML.

国土地理院基盤地図情報`FGD`_ (Fundamental Geospatial Data) 基本項目 JPGIS(GML)
V4.0形式のデータをGMLに変換するコンバータである。


.. _FGD: http://www.gsi.go.jp/kiban/

Requirement
-----------

Python 2.7.13, Python 3.4 or later. Python 3.5 or later is recommended.
実行には Python 3.4 または Python 2.7.13 が必要である。
Python バージョン3.5以降が推奨される。


Basic usage
-----------

SYNOPSIS::

    fgdconv [-c][-f <format>] <Input FGD-GML filename>  <Output filename or directory name>
    fgdconv [-c] -f "GML" <Input FGD-GML filename> <Output GML filename ex. out.gml>
    fgdconv [-c] -f "ESRI Shapefile" <Input FGD-GML filename> <Output directory name ex. out>


DESCRIPTION

This utility convert Fundamental Geospatial Data to GML or other wellknown format.
このツールは、基盤地図情報基本項目XMLデータを著名なデータ形式に変換する。
GMLに変換するには、つぎのように実行する::

    $ fgdconv FG-GML-533946-AdmArea-20140701-0001.xml AdmArea.gml

-c オプションを指定すると、出力をWGS84の測量系に変換する::

    $ fgdconv -c FG-GML-533946-AdmArea-20140701-0001.xml AdmArea.gml

-f オプションで出力ファイル形式を指定できる::

    $ fgdconv -c -f "ESRI Shapefile" FG-GML-533946-AdmArea-20140701-0001.xml out

この例では、outディレクトリーが作成され、out.shpファイルが生成される。
現在のところ、"ESRI Shapefile"と"GML"が指定可能である。


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

