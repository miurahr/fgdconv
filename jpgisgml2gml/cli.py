#!/usr/bin/env python
# -*- coding: utf-8 -*-
from io import open
import sys
import xml
import argparse
import jpgisgml2gml


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
    if py3:
        parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                            default=sys.stdin, help=inhelp)
        parser.add_argument('outfile', nargs='?', type=argparse.FileType('wb'),
                            defualt=sys.stdout, help=outhelp)
    else:
        parser.add_argument('infile', nargs='?', type=commandline_arg,
                            help=inhelp)
        parser.add_argument('outfile', nargs='?', type=commandline_arg,
                            help=outhelp)
    return parser


def outfile(args):
    if py3:
        return args.outfile
    else:
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
    fgd_parser = jpgisgml2gml.Fgd2Gml(outfile(args))
    if py3:
        xml.sax.parse(infile(args), fgd_parser)
    else:
        # Python2.7 will got encoding error with xml.sax.parse()
        # so reading source XML explicitly.
        source = infile(args).read().decode(encoding="UTF-8")
        xml.sax.parseString(source, fgd_parser)


if __name__ == '__main__':
    exit(main())
