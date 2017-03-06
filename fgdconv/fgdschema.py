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

import os
import lxml.etree
import xml.etree.ElementTree as ET

try:
    dict.iteritems
except AttributeError:
    # Python 3
    def iteritems(d):
        return iter(d.items())
else:
    # Python 2
    def iteritems(d):
        return d.iteritems()


class Schema:
    def __init__(self, schemafile):
        self.root = ET.parse(schemafile)

    @staticmethod
    def replace_ns(path):
        SCHEMA_SPACE = {
            "fgd:": "{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}",
            "gml:": "{http://www.opengis.net/gml/3.2}",
            "xlink:": "{http://www.w3.org/1999/xlink}",
            "xs:": "{http://www.w3.org/2001/XMLSchema}"
        }
        for k, v in iteritems(SCHEMA_SPACE):
            path = path.replace(k, v)
        return path

    def findall(self, path):
        return self.root.findall(self.replace_ns(path))

    def find(self, path):
        return self.root.find(self.replace_ns(path))

    @staticmethod
    def names_of(nodes):
        return [node.get("name") for node in nodes]

    def get_types(self, t_name):
        return self.names_of(self.findall(t_name))

    def get_simple_types(self):
        return self.get_types("xs:simpleType")

    def get_complex_types(self):
        return self.get_types("xs:complexType")

    def get_elements_of_attribute(self, attribute):
        return self.names_of(self.findall(".//xs:element/xs:complexType/xs:"
                                          + attribute + "/../.."))

    def get_element_attributes(self, name):
        node = self.find(".//xs:element[@name='" + name + "']")
        if node is None:
            node = self.find(".//xs:complexType[@name='" + name + "']")

        if node is None:
            return None
        else:
            return node.attrib


class FgdSchema(Schema):
    def __init__(self, schemafile):
        Schema.__init__(self, schemafile)

    def get_fgd_element_names(self):
        names = []
        node = self.findall("./xs:element")
        for e in node:
            if e.attrib.get("name") is not None:
                names.append(e.attrib.get("name"))
        names.remove("Dataset")
        return names

    def get_fgd_element_attributes(self, name):
        attributes = []
        elements = self.get_fgd_elements(name)
        if elements is not None:
            for v in elements:
                attributes.append(v['name'])
        return attributes

    def get_fgd_element(self, name, tag):
        elements = self.get_fgd_elements(name)
        if elements is not None:
            for element in elements:
                if element['name'] == tag:
                    return element
        return None

    def get_fgd_elements(self, name):
        node = self.find(".//xs:element[@name='" + name + "']")

        # get the complexType in sequence elements
        type_node = node.attrib.get("type")
        if type_node is None:
            return None

        typename = lxml.etree.QName(self.replace_ns(type_node)).localname
        return self.get_fgd_complex_type_sequence(typename)

    def get_fgd_complex_type_sequence(self, name):
        elements = []

        # get the base complexType define, sequence element list.
        node = self.find(".//xs:complexType[@name='" + name + "']" +
                         "/xs:complexContent/xs:extension")
        if node is not None and node.attrib.get("base") is not None:
            base = node.attrib.get("base")
            tname = lxml.etree.QName(self.replace_ns(base)).localname
            elements.extend(self.get_fgd_complex_type_sequence(tname))

        # get the sequence element list.
        node = self.find(".//xs:complexType[@name='" + name + "']" +
                         "/xs:complexContent/xs:extension/xs:sequence")
        if node is None:
            return elements

        for v in node:
            if len(v.attrib) > 0:
                elements.append(v.attrib)

        return elements


if __name__ == '__main__':
    xsdFile = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'data/FGD_GMLSchema.xsd')
    with open(xsdFile) as f:
        schema = FgdSchema(f)
        element_names = schema.get_fgd_element_names()
        print(element_names)
        print(schema.get_fgd_element_attributes("WStrL"))
        print(schema.get_fgd_element("WStrL", "loc"))
        print(schema.get_fgd_elements("WStrL"))
        # print all types.
        for e in element_names:
            elements = schema.get_fgd_elements(e)
            for i in elements:
                print(i['type'].encode('utf_8'))
