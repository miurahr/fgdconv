# -*- coding: utf-8 -*-
import os
from jpgisgml2gml.schema import Schema


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
        type = node.attrib.get("type")
        if type is None:
            return None

        typename = etree.QName(self.replace_ns(type)).localname
        return self.get_fgd_complex_type_sequence(typename)

    def get_fgd_complex_type_sequence(self, name):
        elements = []

        # get the base complexType define, sequence element list.
        node = self.find(".//xs:complexType[@name='" + name + "']" +
                         "/xs:complexContent/xs:extension")
        if node is not None and node.attrib.get("base") is not None:
            typename = etree.QName(self.replace_ns(node.attrib.get("base"))).localname
            elements.extend(self.get_fgd_complex_type_sequence(typename))

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
    xsdFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/FGD_GMLSchema.xsd')
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
