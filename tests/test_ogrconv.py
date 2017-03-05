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

from unittest import TestCase
from io import open  # support python2.7
import os

from jpgisgml2gml.ogrconv import OgrConv


class OgrConvTestCase(TestCase):
    def setUp(self):
        self.here = os.path.dirname(__file__)

    def test_convert(self):
        out_f_name = os.path.join("/tmp", "BldA84_test.gml")
        in_f_name = os.path.join(self.here, 'BldA.gml')
        converter = OgrConv(4612, 4326)
        converter.convert(in_f_name, "GML", out_f_name, "GML")
        out_f = open(out_f_name, 'r', encoding="utf-8")
        out_text = out_f.read()
        with open(os.path.join(self.here, "BldA84.gml"), "r") as f:
            expected = f.read()
        assert out_text == expected
