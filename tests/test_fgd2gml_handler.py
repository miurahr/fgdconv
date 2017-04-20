# -*- coding: utf-8 -*-
# Copyright (c) 2017 Hiroshi Miura
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
import xml
from io import open  # support python2.7
from unittest import TestCase

from fgdconv.sax import fgd2gml_handler
import fgdconv.utils

from tests.xmlutil import assertXmlEqual


class Fgd2GmlHandlerTestCase(TestCase):
    def setUp(self):
        self.here = os.path.dirname(__file__)
        # detect python version
        try:
            unicode  # python2.7
            self.py2 = True
        except NameError:
            # python3
            self.py2 = False

    def test_sax_fgd2gml_handler(self):
        out_f_name = fgdconv.utils.get_temp_filename()
        # run converter
        with open(os.path.join(self.here, 'data', 'BldA_source.xml'),
                  "r", encoding="utf-8") as in_f:
            with fgd2gml_handler.Fgd2GmlHandler(out_f_name) as fgd_parser:
                if self.py2:
                    in_buf = in_f.read().encode(encoding='utf-8')
                    xml.sax.parseString(in_buf, fgd_parser)
                else:
                    xml.sax.parse(in_f, fgd_parser)
        # check result
        with open(out_f_name, "r") as out_f:
            with open(os.path.join(self.here, 'data', "BldA_jgd2000.gml"),
                      "r", encoding="utf-8") as expected:
                assertXmlEqual(out_f, expected)
