# -*- coding: utf-8 -*-
# Copyright (c) 2017 Hiroshi Miura
#               2014 mizutuu
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
#
# based on a script from
#     http://wiki.openstreetmap.org/wiki/Converting_OSM_to_GML
# modified to work with JPGIS(GML) V4.0 XSD by yoshida
# Work with JPGIS FGD GML V4.1 XSD

import os
from collections import deque
from itertools import islice
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import SubElement
from xml.sax.handler import ContentHandler

from fgdconv.sax import fgdschema


class Fgd2GmlHandler(ContentHandler):
    def __init__(self, file_path):
        ContentHandler.__init__(self)
        self.fh = open(file_path, 'wb')
        self.xsdFile = open(os.path.join(os.path.abspath(
                os.path.dirname(__file__)), 'data/FGD_GMLSchema.xsd'))
        self.schema = fgdschema.FgdSchema(self.xsdFile)
        self.featureId = None
        self.featureTag = None  # ex) 'WStrL', 'Cstline', etc...
        self.nodeElements = None
        self.currentStack = []
        self.current = None
        self.nodes = []
        self.tags = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.schema = None
        self.xsdFile.close()
        self.fh.close()

    def get_fgd_tags(self):
        return self.schema.get_fgd_element_names()

    def get_fgd_node_elements(self, name):
        self.nodeElements = self.schema.get_fgd_elements(name)

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

        # matched FGD node member name.
        # (case of WStrL element, 'loc', 'type', 'name', etc...)
        node = self.get_fgd_node_element(name)
        if node is None:
            return False

        return True

    def startDocument(self):
        self.tags = self.get_fgd_tags()
        self.nodeElements = None
        self.featureTag = None
        self.featureId = None
        self.currentStack = []
        self.current = None
        self.nodes = []
        self.fh.write(b'<?xml version="1.0" encoding="utf-8" ?>\n')
        self.fh.write(b'<ogr:FeatureCollection')
        self.fh.write(b' xmlns:xsi=')
        self.fh.write(b'"http://www.w3.org/2001/XMLSchema-instance"')
        self.fh.write(b' xsi:schemaLocation=""')
        self.fh.write(b' xmlns:ogr="http://ogr.maptools.org/"')
        self.fh.write(b' xmlns:gml="http://www.opengis.net/gml">\n')

    def endDocument(self):
        self.fh.write(b'</ogr:FeatureCollection>\n')

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
            new_element.text = self.split_content(content_list)
        for n in node['node']:
            self.rebuild_element(new_element, n)

    def split_content(self, content_list):
        return ' '.join([x[1] + "," + x[0]
                         for x in [x.split()
                                   for x in content_list if x != ""]])

    def generate_feature(self):
        feature_member = Element('gml:featureMember',)
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

            if node['type'] in {'gml:CurvePropertyType',
                                'gml:DiscreteCoverageType',
                                'gml:PointPropertyType',
                                'gml:SurfacePropertyType'}:
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

        ElementTree(feature_member).write(self.fh, encoding="UTF-8",
                                          xml_declaration=False)
        self.fh.write(b'\n')
