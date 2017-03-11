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
import sys
import tempfile
import xml

from fgdconv.ogr2ogr import Ogr2Ogr
from fgdconv.ogr2ogr import is_valid
from fgdconv.sax.fgd2gml_handler import Fgd2Gml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='conv', action='store_true',
                        help="Convert coordination from JGD2000 to WGS84")
    parser.add_argument('-f', dest='format', nargs='?',
                        default="ESRI Shapefile",
                        help="Output file format name" +
                             "(Default is ESRI Shapefile)." +
                             "Some possible values are:\n"+
                             '    -f "ESRI Shapefile"' +
                             '\n    -f "GML"')
    parser.add_argument('infile', type=argparse.FileType('r'),
                        help='FGD JPGIS(GML) v4 input file.')
    parser.add_argument('outfile', help='Output GML file. If not specified')
    args = parser.parse_args()
    process(args)


def process(args):
    format = "GML"  # default
    if args.format is not None:
        format = args.format
    if args.conv:
        if is_valid(format, args.outfile):
            gml = tempfile.NamedTemporaryFile()
            gml_f = gml.name
            gml.close()
            gml = open(gml_f, "wb")
            xml.sax.parse(args.infile, Fgd2Gml(gml))
            gml.close()
            converter = Ogr2Ogr(4612, 4326)
            converter.convert(gml_f, "GML", args.outfile, format)
            os.unlink(gml_f)
        else:
            # raise error
            pass
    else:
        if format == "GML":
            outfile = open(args.outfile, "wb")
            xml.sax.parse(args.infile, Fgd2Gml(outfile))
            outfile.close()
        else:
            if is_valid(format, args.outfile):
                converter = Ogr2Ogr(4612, 4612)
                gml = tempfile.NamedTemporaryFile()
                gml_f = gml.name
                gml.close()
                gml = open(gml_f, "wb")
                xml.sax.parse(args.infile, Fgd2Gml(gml))
                gml.close()
                converter.convert(gml_f, args.outfile)
                os.unlink(gml_f)
            else:
                # FIXME: raise error
                pass

# --------------------------------------------------
# Python 2.7 compatibility code
# --------------------------------------------------
def commandline_arg(bytestring):
    unicode_string = bytestring.decode(sys.getfilesystemencoding())
    return unicode_string


def main2():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='conv', action='store_true',
                        help='Convert coordination from JGD2000 to WGS84')
    parser.add_argument('-f', dest='format', nargs='?',
                        default="ESRI Shapefile",
                        help="Output file format name." +
                             "(Default is ESRI Shapefile)." +
                             "Some possible values are:\n"+
                             '    -f "ESRI Shapefile"' +
                             '\n    -f "GML"')
    parser.add_argument('infile', type=commandline_arg,
                        help='FGD JPGIS(GML) v4 input file.')
    parser.add_argument('outfile', type=commandline_arg,
                        help='Output GML file. If not specified')
    args = parser.parse_args()
    process2(args)


def process2(args):
    from io import open  # hack for python2.7
    in_f = open(args.infile, 'r')
    source = in_f.read().encode(encoding="utf-8")
    in_f.close()
    if args.conv:
        gml = tempfile.NamedTemporaryFile()
        gml_f = gml.name
        gml.close()
        gml = open(gml_f, "wb")
        xml.sax.parseString(source, Fgd2Gml(gml))
        gml.close()
        converter = Ogr2Ogr(4612, 4326)
        converter.convert(gml_f, "GML", args.outfile, args.format)
        os.unlink(gml_f)
    else:
        outfile = open(args.outfile, 'wb')
        xml.sax.parseString(source, Fgd2Gml(outfile))
        outfile.close()
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
