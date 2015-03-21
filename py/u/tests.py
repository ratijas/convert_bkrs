# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from u import u, utf


class SimpleUnicodeTestCase(unittest.TestCase):
    def testString(self):
        self.assertEquals("string", str("string"))

    def testUnicode(self):
        self.assertEquals(u"string", unicode("string"))

    def testCoerce(self):
        self.assertEquals("string", u"string")


class ModuleUnicodeTestCase(unittest.TestCase):
    def setUp(self):
        self.richstr = '\xd0\xa1\xd1\x82\xd1\x80\xd0\xbe\xd0\xba\xd0\xb0'
        self.richuni = u'\u0421\u0442\u0440\u043e\u043a\u0430'

    def tearDown(self):
        pass

    # strict type check
    def assertTypeEquals(self, first, second):
        """assert not only equality of two values as defined by operator ==,
        but also check that both are of the same type().
        """
        self.assertEquals(first, second)
        self.assertEquals(type(first), type(second))

    # u.u
    def testUFromAsciiString(self):
        self.assertTypeEquals(u"string", u("string"))

    def testUFromRichString(self):
        self.assertTypeEquals(self.richuni, u(self.richstr))

    def testUFromAsciiUnicode(self):
        self.assertTypeEquals(u"string", u(u"string"))

    def testUFromRichUnicode(self):
        self.assertTypeEquals(self.richuni, u(self.richuni))

    def testUFromNumber(self):
        self.assertTypeEquals(u"14.5", u(14.5))

    def testUFromBool(self):
        self.assertTypeEquals(u"True", u(True))

    def testUFromCallable(self):
        l = lambda x: x**2
        self.assertTrue(u(l).startswith(u"<function <lambda> at 0x"))

    def testUFromCustom__str__(self):
        class C(object):

            def __init__(self, s):
                self.s = s

            def __str__(self):
                return self.s  # randomn rubbish
        self.assertTypeEquals(self.richuni, u(C(self.richstr)))

    def testUFromCustom__unicode__(self):
        class C(object):

            def __init__(self, s):
                self.s = s

            def __unicode__(self):
                return self.s
        self.assertTypeEquals(self.richuni, u(C(self.richuni)))

    # u.utf
    def testUtfFromAsciiString(self):
        s = utf("string")
        self.assertTypeEquals("string", s)
        self.assertTypeEquals(type("string"), type(s))

    def testUtfFromRichString(self):
        self.assertTypeEquals(self.richstr, utf(self.richstr))

    def testUtfFromAsciiUnicode(self):
        self.assertTypeEquals("string", utf(u"string"))

    def testUtfFromRichUnicode(self):
        self.assertTypeEquals(self.richstr, utf(self.richuni))

    def testUtfFromNumber(self):
        self.assertTypeEquals("14.5", utf(14.5))

    def testUtfFromBool(self):
        self.assertTypeEquals(("False"), utf(False))

    def testUtfFromCallable(self):
        def fn():
            pass
        fn.__name__ = self.richstr
        self.assertTrue(utf(fn).startswith(
            "<function %s at 0x" % self.richstr))

    def testUtfFromCustom__str__(self):
        class C(object):

            def __init__(self, s):
                self.s = s

            def __str__(self):
                return self.s
        self.assertTypeEquals(self.richstr, utf(C(self.richstr)))

    def testUtfFromCustom__unicode__(self):
        class C(object):

            def __init__(self, s):
                self.s = s

            def __unicode__(self):
                return self.s
        self.assertTypeEquals(self.richstr, utf(C(self.richuni)))

if __name__ == "__main__":
    unittest.main()
