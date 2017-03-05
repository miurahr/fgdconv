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
import sys
import tempfile
import xml

import jpgisgml2gml
import jgd2k2wgs84

# detect python2 or python3
try:
    unicode
    py3 = False
except NameError:
    py3 = True


def commandline_arg(bytestring):
    unicode_string = bytestring.decode(sys.getfilesystemencoding())
    return unicode_string


def get_parser():
    inhelp = 'JPGIS(GML) v4 input file.'
    outhelp = "Output GML file. If not specified"
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='conv', action='store_true',
                        help="Convert coordination from JGD2000 to WGS84")
    if py3:
        parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                            default=sys.stdin, help=inhelp)
        parser.add_argument('outfile', nargs='?', help=outhelp)
    else:
        parser.add_argument('infile', nargs='?', type=commandline_arg,
                            help=inhelp)
        parser.add_argument('outfile', nargs='?', type=commandline_arg,
                            help=outhelp)
    return parser


def get_outfile_object(args):
    if args.outfile is not None:
        return open(args.outfile, 'wb')
    else:
        return sys.stdout


def infile(args):
    if py3:
        return args.infile
    else:
        if args.infile_name is not None:
            return open(args.infile, 'rb')
        else:
            return sys.stdin


def main():
    parser = get_parser()
    args = parser.parse_args()
    conv = args.conv
    flag_stdout = False

    if conv:
        gml = tempfile.NamedTemporaryFile()
        gml_f = gml.name
        if args.outfile is None:
            gml84 = tempfile.NamedTemporaryFile()
            gml84_f = gml84.name
            gml84.close()
            flag_stdout = True
        else:
            gml84_f = args.outfile
    else:
        gml = get_outfile_object(args)

    fgd_parser = jpgisgml2gml.Fgd2Gml(gml)
    if py3:
        xml.sax.parse(infile(args), fgd_parser)
    else:
        # Python2.7 will got encoding error with xml.sax.parse()
        # so reading source XML explicitly.
        source = infile(args).read().decode(encoding="UTF-8")
        xml.sax.parseString(source, fgd_parser)
    if conv:
        converter = jgd2k2wgs84.Jgd2k2Gml()
        converter.prepare(gml_f, gml84_f)
        converter.convert()
        converter.close()
        if flag_stdout:
            fin = open(gml84_f, 'r')
            for line in fin:
                print(line.strip())
            fin.close()


if __name__ == '__main__':
    exit(main())
