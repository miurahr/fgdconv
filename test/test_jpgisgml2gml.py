from unittest import TestCase
from nose.tools import ok_, eq_

import os

class JpgisGml2GmlTestCase(TestCase):
    def setUp(self):
        self.xsdFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/FGD_GMLSchema.xsd')

