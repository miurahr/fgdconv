#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, xml
from jpgisgml2gml import Fgd2Gml


def main():
    xsdFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'schema/FGD_GMLSchema.xsd')
    fgdParser = Fgd2Gml(sys.stdout, xsdFile)
    print '<?xml version="1.0" encoding="utf-8" ?>'
    print '<ogr:FeatureCollection'
    print '     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
    print '     xsi:schemaLocation=""'
    print '     xmlns:ogr="http://ogr.maptools.org/"'
    print '     xmlns:gml="http://www.opengis.net/gml">'

    xml.sax.parse(sys.stdin, fgdParser)

    print '</ogr:FeatureCollection>'