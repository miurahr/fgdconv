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
import tempfile

from fgdconv import fgd2ogr

from tests.xmlutil import assertXmlEqual


# Argparse mock
class MockArgs:
    def __init__(self):
        self.conv = False
        self.infile = None
        self.outfile = None
        self.format = "GML"


class Fgd2OgrTestCase(TestCase):
    def setUp(self):
        self.here = os.path.dirname(__file__)
        self.out_d_base = tempfile.mkdtemp()

    def test_main(self):
        # set argparser argument mock
        args = MockArgs()
        args.conv = False
        args.outfile = os.path.join(self.out_d_base, "BldA84_test.gml")
        args.format = "GML"

        # test main process according to Python version
        try:
            unicode  # python2.7
            args.infile = os.path.join(self.here, "data", "BldA.xml")
            fgd2ogr.process2(args)
        except NameError: # python3
            args.infile = open(os.path.join(self.here, "data", "BldA_source.xml"), "r")
            fgd2ogr.process(args)
            args.infile.close()

        # assertion
        with open(args.outfile, mode="r", encoding="utf-8") as f:
            out_text = f.read()
        with open(os.path.join(self.here, "data", "BldA_jgd2000.gml"), mode="r",
                  encoding="utf-8") as f:
            expected = f.read()
        assertXmlEqual(out_text, expected)

    def test_conv(self):
        # set argparser argument mock
        args = MockArgs()
        args.conv = True
        args.outfile = os.path.join(self.out_d_base,  "BldA84_test.gml")
        args.format = "GML"

        # test main process with conversion flag
        try:
            unicode  # python2.7
            args.infile = os.path.join(self.here, "data", "BldA_source.xml")
            fgd2ogr.process2(args)
        except NameError:
            args.infile = open(os.path.join(self.here, "data", "BldA_source.xml"), "r")
            fgd2ogr.process(args)
            args.infile.close()

        # assertion
        with open(args.outfile, mode="r", encoding="utf-8") as f:
            out_text = f.read()
        with open(os.path.join(self.here, "data", "BldA_wgs84.gml"), mode="r",
                  encoding="utf-8") as f:
            expected = f.read()
        assertXmlEqual(out_text, expected)
