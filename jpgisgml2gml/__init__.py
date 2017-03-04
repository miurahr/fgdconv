#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, xml
import argparse
from jpgisgml2gml.jpgisgml2gml import Fgd2Gml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help='JPGIS(GML) v4 input file.')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('wb'), defualt=sys.stdout,
                        help="Output GML file.")
    args = parser.parse_args()

    fgdParser = Fgd2Gml(args.outfile)
    xml.sax.parse(args.infile, fgdParser)
