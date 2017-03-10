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
import shutil
import tempfile

from fgdconv.ogrconv import OgrConv
from tests.xmlutil import xml_compare_s


class OgrConvTestCase(TestCase):
    def setUp(self):
        self.here = os.path.dirname(__file__)
        self.out_d_base = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.out_d_base)
        pass

    def test_constructor(self):
        converter = OgrConv(4612, 4612)
        assert converter is not None

    def test_convert_gml(self):
        # resources
        in_f_name = os.path.join(self.here, 'data', 'BldA_jgd2000.gml')
        out_f_name = os.path.join(self.out_d_base, "BldA84_test.gml")
        # test body
        converter = OgrConv(4612, 4326)
        converter.convert(in_f_name, "GML", out_f_name, "GML")
        # assertion
        with open(out_f_name, 'r', encoding="utf-8") as f:
            out_text = f.read()
        with open(os.path.join(self.here, "data",
                               "BldA_wgs84.gml"), "r", encoding="utf-8") as f:
            expected = f.read()
        assert xml_compare_s(out_text, expected)


    def test_convert_shapefile(self):
        # resources
        in_f_name = os.path.join(self.here, "data", 'BldA_jgd2000.gml')
        test_f_name = "BldA84_test.shp"
        out_d_name = os.path.join(self.out_d_base, "BldA84_test", )
        # test body
        converter = OgrConv(4612, 4326)
        converter.convert(in_f_name, "GML", out_d_name, "ESRI Shapefile")
        assert os.path.exists(os.path.join(out_d_name, test_f_name))
