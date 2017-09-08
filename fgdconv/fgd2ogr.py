#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Hiroshi Miura
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import os
import platform
import xml

from fgdconv.ogr2ogr import Ogr2Ogr
from fgdconv.ogr2ogr import is_valid
from fgdconv.sax.fgd2gml_handler import Fgd2GmlHandler
import fgdconv.utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='conv', action='store_true',
                        help="Convert coordination from JGD2000 to WGS84")
    parser.add_argument('-f', dest='format', nargs='?',
                        default="GML",
                        help="Output file format name" +
                             "(Default is ESRI Shapefile)." +
                             "Some possible values are:\n" +
                             '    -f "ESRI Shapefile"' +
                             '\n    -f "GML"')
    parser.add_argument('infile', type=argparse.FileType('r'),
                        help='FGD JPGIS(GML) v4 input file.')
    parser.add_argument('outfile', help='Output GML file. If not specified')
    args = parser.parse_args()
    try:
        process(args)
    except ValueError as err:
        print(err.args)
        return 1
    return 0


def process(args):
    if args.conv:
        if is_valid(args.format, args.outfile):
            gml_f = fgdconv.utils.get_temp_filename()
            with Fgd2GmlHandler(gml_f) as h:
                if platform.system() == 'Windows':
                    xml.sax.parse(args.infile, h)
                else:
                    with open(args.infile, 'r') as in_f:
                            source = in_f.read().encode(encoding="utf-8")
                            xml.sax.parseString(source, h)
            converter = Ogr2Ogr(4612, 4326)
            converter.convert(gml_f, "GML", args.outfile, args.format)
            os.unlink(gml_f)
        else:
            raise ValueError("Format is invalid")
    else:
        if args.format == "GML":
            with Fgd2GmlHandler(args.outfile) as h:
                if platform.system() == 'Windows':
                    xml.sax.parse(args.infile, h)
                else:
                    with open(args.infile, 'r') as in_f:
                            source = in_f.read().encode(encoding="utf-8")
                            xml.sax.parseString(source, h)
        else:
            if is_valid(args.format, args.outfile):
                converter = Ogr2Ogr(4612, 4612)
                gml_f = fgdconv.utils.get_temp_filename()
                with Fgd2GmlHandler(gml_f) as h:
                    xml.sax.parse(args.infile, h)
                converter.convert(gml_f, "GML", args.outfile, args.format)
                os.unlink(gml_f)
            else:
                raise ValueError("Format is invalid")


# --------------------------------------------------
# Python 2.7 compatibility code
# --------------------------------------------------
def main2():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='conv', action='store_true',
                        help='Convert coordination from JGD2000 to WGS84')
    parser.add_argument('-f', dest='format', nargs='?',
                        default="GML",
                        help="Output file format name." +
                             "(Default is ESRI Shapefile)." +
                             "Some possible values are:\n" +
                             '    -f "ESRI Shapefile"' +
                             '\n    -f "GML"')
    parser.add_argument('infile', type=fgdconv.utils.commandline_arg,
                        help='FGD JPGIS(GML) v4 input file.')
    parser.add_argument('outfile', type=fgdconv.utils.commandline_arg,
                        help='Output GML file. If not specified')
    args = parser.parse_args()
    try:
        process2(args)
    except ValueError as err:
        print(err.args)
        return 1
    return 0


def process2(args):
    from io import open  # hack for python2.7
    if args.conv:
        if is_valid(args.format, args.outfile):
            gml_f = fgdconv.utils.get_temp_filename()
            with Fgd2GmlHandler(gml_f) as h:
                xml.sax.parse(args.infile, h)
            converter = Ogr2Ogr(4612, 4326)
            converter.convert(gml_f, "GML", args.outfile, args.format)
            os.unlink(gml_f)
        else:
            raise ValueError("Format is invalid")
    else:
        if args.format == "GML":
            with Fgd2GmlHandler(args.outfile) as h:
                with open(args.infile, 'r') as in_f:
                        source = in_f.read().encode(encoding="utf-8")
                        xml.sax.parseString(source, h)
        else:
            if is_valid(args.format, args.outfile):
                converter = Ogr2Ogr(4612, 4612)
                gml_f = fgdconv.utils.get_temp_filename()
                with Fgd2GmlHandler(gml_f) as h:
                    xml.sax.parse(args.infile, h)
                converter.convert(gml_f, "GML", args.outfile, args.format)
                os.unlink(gml_f)
            else:
                raise ValueError("Format is invalid")
# --------------------------------------------------
# End of Python 2.7 compatibility code
# --------------------------------------------------


if __name__ == '__main__':
    # detect python2 or python3
    try:
        unicode
        exit(main2())
    except NameError:
        exit(main())
