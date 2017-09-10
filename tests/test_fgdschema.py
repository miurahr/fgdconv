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
from fgdconv.sax.fgdschema import FgdSchema

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
