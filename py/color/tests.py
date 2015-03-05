#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''testing for color.py'''

import sys
import unittest

sys.path.append('../')
import color

class SearchPinYinTestCase(unittest.TestCase):
    def setUp(self):
        self.s = u'bǎiwén bùrú yījiàn // fāng’àn // fǎngán // xúniang'
    def tearDown(self):
        pass
    def testBaiwenBuruYijian(self):
        r = color.search_for_pin_yin_in_string(self.s)
        
class ColorizeTestCase(unittest.TestCase):
    def testBasics(self):
        baiwen = u'bǎiwén'
        expected = u'<span class="t3">bǎi</span><span class="t2">wén</span>'
        self.failUnlessEqual(color.colorize(baiwen), expected)
    


class determineToneTestCase(unittest.TestCase):
    def testFristTone(self):
        self.failUnlessEqual(1, color.determine_tone('fāng'))
        self.failUnlessEqual(1, color.determine_tone('yī'))
    def testSecondTone(self):
        self.failUnlessEqual(2, color.determine_tone('gán'))
        self.failUnlessEqual(2, color.determine_tone('xún'))
    def testThirdTone(self):
        self.failUnlessEqual(3, color.determine_tone('fǎn'))
        self.failUnlessEqual(3, color.determine_tone('lǚ'))
    def testFourthTone(self, ):
        self.failUnlessEqual(4, color.determine_tone('àn'))
        self.failUnlessEqual(4, color.determine_tone('dìnggòu'))
    def testZeroTone(self):
        self.failUnlessEqual(0, color.determine_tone('de'))
        self.failUnlessEqual(0, color.determine_tone('ning'))
    def testNonPinYin(self):
        self.failUnlessEqual(0, color.determine_tone('бурда'))
    
    


def main():
	s = u'bǎiwén bùrú yījiàn // fāng’àn // fǎngán // xúniang'
	print u'изначально: "%s"' % s
	r = search_for_pin_yin_in_string( s )
	print u'search_for_pin_yin_in_string() ->'
	for e in r:
		print u'\t' u'start: %d,' u'\t' u'value: %s' % \
			( e[ 'start' ], u( e[ 'value' ]))

	print u'colorize\n----'

	s2 = colorize( s )
	print u'type is', type( s2 )
	print s2

if __name__ == '__main__':
    unittest.main()
