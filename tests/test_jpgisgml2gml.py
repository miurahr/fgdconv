from unittest import TestCase
import jpgisgml2gml

import os
import tempfile
import xml

class JpgisGml2GmlTestCase(TestCase):
    def test_convert(self):
        out_f = tempfile.TemporaryFile()
        in_f = open(os.path.join(os.path.dirname(__file__), 'BldA.xml'), "r")
        fgd_parser = jpgisgml2gml.Fgd2Gml(out_f)
        xml.sax.parse(in_f, fgd_parser)
        out_f.seek(0)
        out_text = out_f.read().decode("utf-8")
        expected = """<?xml version="1.0" encoding="utf-8" ?>
<ogr:FeatureCollection
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation=""
     xmlns:ogr="http://ogr.maptools.org/"
     xmlns:gml="http://www.opengis.net/gml">
<gml:featureMember><ogr:BldA fid="20161209-50295-12846-s-11705"><ogr:id>K17_5026512840_298334</ogr:id><ogr:fid>20161209-50295-12846-s-11705</ogr:fid><ogr:lfSpanFr>2016-12-09</ogr:lfSpanFr><ogr:devDate>2016-12-10</ogr:devDate><ogr:orgGILvl>2500</ogr:orgGILvl><ogr:area><ogr:geometryProperty><gml:Surface srsName="EPSG:4612"><gml:patches><gml:PolygonPatch><gml:exterior><gml:Ring><gml:curveMember><gml:Curve><gml:segments><gml:LineStringSegment><gml:posList>139.708789472,35.688618 139.708817722,35.6886725 139.708758306,35.688693 139.708730056,35.6886385 139.708789472,35.688618</gml:posList></gml:LineStringSegment></gml:segments></gml:Curve></gml:curveMember></gml:Ring></gml:exterior></gml:PolygonPatch></gml:patches></gml:Surface></ogr:geometryProperty></ogr:area><ogr:type>堅ろう建物</ogr:type></ogr:BldA></gml:featureMember>
<gml:featureMember><ogr:BldA fid="20161209-50292-12867-s-23910"><ogr:id>K17_5026512840_298335</ogr:id><ogr:fid>20161209-50292-12867-s-23910</ogr:fid><ogr:lfSpanFr>2016-12-09</ogr:lfSpanFr><ogr:devDate>2016-12-10</ogr:devDate><ogr:orgGILvl>2500</ogr:orgGILvl><ogr:area><ogr:geometryProperty><gml:Surface srsName="EPSG:4612"><gml:patches><gml:PolygonPatch><gml:exterior><gml:Ring><gml:curveMember><gml:Curve><gml:segments><gml:LineStringSegment><gml:posList>139.701679834,35.744088831 139.701730582,35.744089067 139.701730017,35.744164240 139.701679268,35.744164094 139.701679834,35.744088831</gml:posList></gml:LineStringSegment></gml:segments></gml:Curve></gml:curveMember></gml:Ring></gml:exterior></gml:PolygonPatch></gml:patches></gml:Surface></ogr:geometryProperty></ogr:area><ogr:type>普通建物</ogr:type></ogr:BldA></gml:featureMember>
<gml:featureMember><ogr:BldA fid="20161209-50295-12840-s-15265"><ogr:id>K17_5026512840_298336</ogr:id><ogr:fid>20161209-50295-12840-s-15265</ogr:fid><ogr:lfSpanFr>2016-12-09</ogr:lfSpanFr><ogr:devDate>2016-12-10</ogr:devDate><ogr:orgGILvl>2500</ogr:orgGILvl><ogr:area><ogr:geometryProperty><gml:Surface srsName="EPSG:4612"><gml:patches><gml:PolygonPatch><gml:exterior><gml:Ring><gml:curveMember><gml:Curve><gml:segments><gml:LineStringSegment><gml:posList>139.712064556,35.673476611 139.712109194,35.673514944 139.712057361,35.673555667 139.712012417,35.673517194 139.712064556,35.673476611</gml:posList></gml:LineStringSegment></gml:segments></gml:Curve></gml:curveMember></gml:Ring></gml:exterior></gml:PolygonPatch></gml:patches></gml:Surface></ogr:geometryProperty></ogr:area><ogr:type>普通建物</ogr:type></ogr:BldA></gml:featureMember>
</ogr:FeatureCollection>
"""
        assert out_text == expected
