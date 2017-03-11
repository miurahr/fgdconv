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
import tempfile
import xml
from io import open  # support python2.7
from unittest import TestCase

from fgdconv.sax import fgd2gml_handler

from tests.xmlutil import assertXmlEqual


class Fgd2GmlHandlerTestCase(TestCase):
    def setUp(self):
        self.here = os.path.dirname(__file__)

    def test_sax_fgd2gml_handler(self):
        out_f = tempfile.TemporaryFile()
        in_f = open(os.path.join(self.here, 'data', 'BldA_source.xml'), "r")
        fgd_parser = fgd2gml_handler.Fgd2Gml(out_f)
        try:
            unicode  # python2.7
            in_buf = in_f.read().encode(encoding="utf-8")
            xml.sax.parseString(in_buf, fgd_parser)
        except NameError:
            # python3
            xml.sax.parse(in_f, fgd_parser)
        in_f.close()
        out_f.seek(0)
        out_text = out_f.read().decode("utf-8")
        out_f.close()
        with open(os.path.join(self.here, 'data', "BldA_jgd2000.gml"), "r") as f:
            expected = f.read()
        assertXmlEqual(out_text, expected)