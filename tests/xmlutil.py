# Copyright (c) 2015 Ian Bicking and FormEncode Contributors
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
#
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from __future__ import print_function
import sys
try:
    import doctest
    doctest.OutputChecker
except (AttributeError, ImportError):  # Python < 2.4
    import util.doctest24 as doctest
try:
    import xml.etree.ElementTree as ET
except ImportError:
    import elementtree.ElementTree as ET


def assertXmlEqual(s1, s2):
    try:
        unicode
        py2 = True
    except NameError:
        py2 = False

    # file like object
    if hasattr(s1, 'read'):
        if py2:
            x1 = ET.fromstring(s1.read().encode('utf-8'))
            x2 = ET.fromstring(s2.read().encode('utf-8'))
        else:
            x1 = ET.parse(s1).getroot()
            x2 = ET.parse(s2).getroot()
        if not xml_compare(x1, x2, errprint):
            raise AssertionError
        return

    # str/unicode
    if py2:
        x1 = ET.fromstring(s1.encode('utf-8'))
        x2 = ET.fromstring(s2.encode('utf-8'))
    else:
        x1 = ET.fromstring(s1)
        x2 = ET.fromstring(s2)
    if not xml_compare(x1, x2, errprint):
        raise AssertionError


def errprint(s):
    print(s, file=sys.stderr)


def xml_compare(x1, x2, reporter=None):
    if x1.tag != x2.tag:
        if reporter:
            reporter('Tags do not match: %s and %s' % (x1.tag, x2.tag))
        return False
    for name, value in x1.attrib.items():
        if x2.attrib.get(name) != value:
            if reporter:
                reporter('Attributes do not match: %s=%r, %s=%r'
                         % (name, value, name, x2.attrib.get(name)))
            return False
    for name in x2.attrib:
        if name not in x1.attrib:
            if reporter:
                reporter('x2 has an attribute x1 is missing: %s'
                         % name)
            return False
    if not text_compare(x1.text, x2.text):
        if reporter:
            reporter('text: %r != %r' % (x1.text, x2.text))
        return False
    if not text_compare(x1.tail, x2.tail):
        if reporter:
            reporter('tail: %r != %r' % (x1.tail, x2.tail))
        return False
    cl1 = x1.getchildren()
    cl2 = x2.getchildren()
    if len(cl1) != len(cl2):
        if reporter:
            reporter('children length differs, %i != %i'
                     % (len(cl1), len(cl2)))
        return False
    i = 0
    for c1, c2 in zip(cl1, cl2):
        i += 1
        if not xml_compare(c1, c2, reporter=reporter):
            if reporter:
                reporter('children %i do not match: %s'
                         % (i, c1.tag))
            return False
    return True


def text_compare(t1, t2):
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()


def make_xml(s):
    return ET.XML('<xml>%s</xml>' % s)
