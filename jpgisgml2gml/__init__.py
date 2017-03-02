#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, xml
import argparse
from jpgisgml2gml.jpgisgml2gml import Fgd2Gml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('jpgis_file', help='JPGIS(GML) v4 file name.')
    parser.add_argument('-o', dest='output_file', help="output GML file.")
    args = parser.parse_args()
    out_f = open(args.output_file, "wb")
    in_fh = open(args.jpgis_file, "r")
    xsdFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/FGD_GMLSchema.xsd')
    fgdParser = Fgd2Gml(out_f, xsdFile)
    out_f.write(b'<?xml version="1.0" encoding="utf-8" ?>\n')
    out_f.write(b'<ogr:FeatureCollection\n')
    out_f.write(b'     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
    out_f.write(b'     xsi:schemaLocation=""\n')
    out_f.write(b'     xmlns:ogr="http://ogr.maptools.org/"\n')
    out_f.write(b'     xmlns:gml="http://www.opengis.net/gml">\n')
    xml.sax.parse(in_fh, fgdParser)
    out_f.write(b'</ogr:FeatureCollection>\n')
