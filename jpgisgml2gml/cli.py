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

from io import open
import argparse
import os
import sys
import tempfile
import xml

from jpgisgml2gml.fgd2gml import Fgd2Gml
from jpgisgml2gml.ogrconv import OgrConv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='conv', action='store_true',
                        help="Convert coordination from JGD2000 to WGS84")
    parser.add_argument('infile', type=argparse.FileType('r'),
                        help='JPGIS(GML) v4 input file.')
    parser.add_argument('outfile', help='Output GML file. If not specified')
    args = parser.parse_args()
    process(args)


def process(args):
    if args.conv:
        gml = tempfile.NamedTemporaryFile()
        gml_f = gml.name
        gml.close()
        gml = open(gml_f, "wb")
        converter = OgrConv(4612, 4326)
        xml.sax.parse(args.infile, Fgd2Gml(gml))
        gml.close()
        converter.convert(gml_f, "GML", args.outfile, "GML")
        os.unlink(gml_f)
    else:
        outfile = open(args.outfile, "wb")
        xml.sax.parse(args.infile, Fgd2Gml(outfile))


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
    parser.add_argument('infile', type=commandline_arg,
                        help='JPGIS(GML) v4 input file.')
    parser.add_argument('outfile', type=commandline_arg,
                        help='Output GML file. If not specified')
    args = parser.parse_args()
    process2(args)


def process2(args):
    source = open(args.infile, 'r').read()
    if args.conv:
        gml = tempfile.NamedTemporaryFile()
        gml_f = gml.name
        gml.close()
        gml = open(gml_f, "w")
        xml.sax.parseString(source, Fgd2Gml(gml))
        gml.close()
        converter = OgrConv(4612, 4326)
        converter.convert(gml_f, "GML", args.outfile, "GML")
        os.unlink(gml_f)
    else:
        outfile = open(args.outfile, 'w')
        xml.sax.parseString(source, Fgd2Gml(outfile))
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
