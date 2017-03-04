from unittest import TestCase
from io import open  # support python2.7
import os
import tempfile
import xml

from jpgisgml2gml import fgd2gml


class JpgisGml2GmlTestCase(TestCase):
    def setUp(self):
        self.here = os.path.dirname(__file__)

    def test_convert(self):
        out_f = tempfile.TemporaryFile()
        in_f = open(os.path.join(self.here, 'BldA.xml'), "r")
        fgd_parser = fgd2gml.Fgd2Gml(out_f)
        try:
            unicode  # python2.7
            in_buf = in_f.read().encode(encoding="utf-8")
            xml.sax.parseString(in_buf, fgd_parser)
        except NameError:
            # python3
            xml.sax.parse(in_f, fgd_parser)
        out_f.seek(0)
        out_text = out_f.read().decode("utf-8")
        with open(os.path.join(self.here, "expected.xml"), "r") as f:
            expected = f.read()
        assert out_text == expected
