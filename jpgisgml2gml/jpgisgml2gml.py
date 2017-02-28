# -*- coding: utf-8 -*-
# based on a script from http://wiki.openstreetmap.org/wiki/Converting_OSM_to_GML
# modified to work with JPGIS(GML) V4.0 XSD by yoshida

import os, sys, re, xml.sax
from xml.sax.handler import ContentHandler
from xml.etree.ElementTree import Element, SubElement, ElementTree
from fgdschema import FgdSchema
from itertools import islice
from collections import deque


class Fgd2Gml(ContentHandler):
    def __init__(self, fh, xsdFile):
        ContentHandler.__init__(self)
        self.fh = fh
        self.xsdFile = xsdFile
        self.featureId = None
        self.featureTag = None
        self.nodeElements = None
        self.currentStack = []
        self.current = None
        self.nodes = []
        self.tags = None

    def get_fgd_tags(self):
        with open(self.xsdFile) as f:
            schema = FgdSchema(f)
            return schema.get_fgd_element_names()

    def get_fgd_node_elements(self, name):
        with open(self.xsdFile) as f:
            schema = FgdSchema(f)
            self.nodeElements = schema.get_fgd_elements(name)

    def get_fgd_node_element(self, name):
        for element in self.nodeElements:
            if element['name'] == name:
                return element
        return None

    def get_fgd_node_element_type(self, name):
        element = self.get_fgd_node_element(name)
        if element is None:
            return None
        return element['type']

    def is_fgd_tag(self, name):
        # matched FGD element name. ('WStrL', 'Cstline', etc...)
        if name in self.tags:
            return True
        return False

    def is_fgd_node_name(self, name):
        if self.featureTag is None:
            return False
        if self.nodeElements is None:
            self.get_fgd_node_elements(self.featureTag)

        # matched FGD node member name. (case of WStrL element, 'loc', 'type', 'name', etc...)
        node = self.get_fgd_node_element(name)
        if node is None:
            return False

        return True

    def startDocument(self):
        self.tags = self.get_fgd_tags()
        self.nodeElements = None
        self.featureTag = None  # ex) 'WStrL', 'Cstline', etc...
        self.featureId = None

        self.currentStack = []
        self.current = None

        self.nodes = []

    def characters(self, data):
        if self.current is not None:
            self.currentStack[-1]['text'] += data

    def startElement(self, name, attr):
        if self.is_fgd_tag(name):
            # find new FGD tag.
            self.featureTag = name
            self.featureId = attr["gml:id"]
        elif self.is_fgd_node_name(name):
            # find new FGD node tag.
            type = self.get_fgd_node_element_type(name)
            self.current = {
                'name': name,  # ex) 'fid', 'lfSpanFr', ...
                'type': type,  # ex) 'xs:string', 'gml:TimeInstantType', ...
                'isgml': type[0:4] == 'gml:',
                'text': "",
                'node': []
            }
            self.currentStack.append(self.current)
        # print "S:", name, self.getFGDNodeElement(name)["type"]

        elif self.current is not None and self.current['isgml']:
            # find new tag, in FGD node.
            new_node = {
                'name': name,
                'text': "",
                'node': []
            }
            self.currentStack[-1]['node'].append(new_node)
            self.currentStack.append(new_node)

    def endElement(self, name):
        if self.current is not None and self.current['name'] == name:
            # find end FGD node tag.
            self.nodes.append(self.current)
            self.currentStack = []
            self.current = None
        # print "E:", name

        elif self.current is not None and self.current['isgml']:
            # find end tag, in FGD node.
            self.currentStack.pop()

        if name in self.tags and self.featureTag == name:
            # find end FGD tag.
            self.generate_feature()

            self.featureId = None
            self.currentStack = []
            self.current = None
            self.nodes = []

    def rebuild_element(self, parent_element, node):
        new_element = SubElement(parent_element, node['name'])
        new_element.text = node['text'].strip()

        if node['name'] in {'gml:pos', 'gml:posList'}:
            # convert the lat/lon -> lon/lat.
            content_list = new_element.text.split("\n")
            new_element.text = ' '.join([x[1] + "," + x[0] for x in [x.split() for x in content_list if x != ""]])

        for n in node['node']:
            self.rebuild_element(new_element, n)

    def generate_feature(self):
        feature_member = Element('gml:featureMember')
        feature = SubElement(feature_member, 'ogr:' + self.featureTag)
        # set the fid.
        for node in self.nodes:
            if node['name'] == 'fid':
                feature.attrib['fid'] = node['text'].strip()

        # generate the id node.
        SubElement(feature, "ogr:id").text = self.featureId

        # generate the child nodes.
        for node in self.nodes:
            new_element = SubElement(feature, 'ogr:' + node['name'])
            new_element.text = node['text'].strip()

            if node['type'] in {'gml:CurvePropertyType', 'gml:DiscreteCoverageType',
                                'gml:PointPropertyType', 'gml:SurfacePropertyType'}:
                geom_element = SubElement(new_element, 'ogr:geometryProperty')
                geom_element.text = node['text'].strip()
                for n in node['node']:
                    self.rebuild_element(geom_element, n)

                # set the 'srsName' in child node.
                iter = geom_element.iter("*")
                gml_element = next(islice(iter, 1, None), None)
                gml_element.attrib['srsName'] = 'EPSG:4612'

            elif node['type'] == 'gml:TimeInstantType':
                last_element = deque(node['node'], maxlen=1).pop()
                new_element.text = last_element['text'].strip()

        ElementTree(feature_member).write(self.fh, 'utf-8')
        self.fh.write("\n")


if __name__ == "__main__":
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
