#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''testing for color.py.'''

import sys
import unittest

sys.path.append('../')
import color

_baiwen = u'bǎiwén bùrú yījiàn // fāng’àn // fǎngán // xúniang'

class SearchPinYinTestCase(unittest.TestCase):
    def setUp(self):
        self._cmd = color.ranges_of_pinyin_in_string
    def tearDown(self):
        pass
    def testBaiwenBuruYijian(self):
        rs = self._cmd(_baiwen)
    def testRanges(self):
        ranges = self._cmd(u"Gōngzuò")
        expected = [(0, 4), (4, 3)]
        #self.failUnlessEqual(ranges, expected)
        
class ColorizeTestCase(unittest.TestCase):
    def testColorizeBaiwen(self):
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

class lowercase_remove_tones_TestCase(unittest.TestCase):
    def test_lowercase_string_by_rempoving_pinyin_tones(self):
        cmd = color.lowercase_string_by_removing_pinyin_tones
        s_list = [
            (u"À! Zhēn měi!", u"a! zhen mei!"),
            (_baiwen, u'baiwen buru yijian // fang’an // fangan // xuniang'),
            ("Nǐ lái háishi bù lái?", u"ni lai haishi bu lai?"),  # not unicode
            ]
        for with_tones, clean in s_list:
            self.failUnlessEqual(cmd(with_tones), clean)

if __name__ == '__main__':
    unittest.main()
