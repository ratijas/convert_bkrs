#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''testing for color.py.'''

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import color

_baiwen = u'bǎiwén bùrú yījiàn // fāng’àn // fǎngán // xúniang'
_2_baiwen = u'2 bǎiwén'
_3_nongmingong = u'3 nóngmíngōng'
_4_kou_anshang = u'4 kǒu’ànshàng'
_5_kouanshang = u'5 kǒuànshàng'
_6_fengongsi = u'6 fēngōngsī'
_7_aiyo = u'7 āiyō'
_8_shenme = u'8 shénme'
_9_fadia = u'9 fādiǎ'
_10_zhiding = u'10 zhǐdìng'
_11_yi1_yi4 = u'11 yī; yì'
_12_nanguo_langxingoufei_er_eryide = u'12 nánguò // lángxīngǒufèi // èr’ěryīde'


class ignore_link_and_input_node_filter_TestCase(unittest.TestCase):
    def setUp(self):
        import lxml.etree as ET
        self.ET = ET
        self.cmd = color.ignore_link_and_input_node_filter
    def test_link_tag(self):
        link = self.ET.fromstring("""<A HREF='http://bkrs.info/slovo.php?ch=仁'>仁</A>""")
        self.assertFalse(self.cmd(link))
    def test_input_tag(self):
        input = self.ET.fromstring("""<input name="ch" size="20" value="100500" type="hidden" />""")
        self.assertFalse(self.cmd(input))
    def test_other(self):
        tag = self.ET.fromstring("""<div class="py">rén<img class="pointer" src="images/player/negative_small/playup.png" /></div>""")
        self.assertTrue(self.cmd(tag))


class colorize_uncolorize_DOM_TestCase(unittest.TestCase):
    def setUp(self):
        import lxml.etree as ET
        self.ET = ET


class colorized_HTML_string_TestCase(unittest.TestCase):
    def test_pairs(self):
        cmd = color.colorized_HTML_string_from_string
        self.failUnlessEqual(cmd(_baiwen),
            u'<span class="pinYinWrapper"><span class="t3">bǎi</span><span class="t2">wén</span> <span class="t4">bù</span><span class="t2">rú</span> <span class="t1">yī</span><span class="t4">jiàn</span> // <span class="t1">fāng</span>’<span class="t4">àn</span> // <span class="t3">fǎn</span><span class="t2">gán</span> // <span class="t2">xú</span><span class="t0">niang</span></span>')
        self.failUnlessEqual(cmd(_2_baiwen),
            u'<span class="pinYinWrapper">2 <span class="t3">bǎi</span><span class="t2">wén</span></span>')
        self.failUnlessEqual(cmd(_3_nongmingong),
            u'<span class="pinYinWrapper">3 <span class="t2">nóng</span><span class="t2">mín</span><span class="t1">gōng</span></span>')
        self.failUnlessEqual(cmd(_4_kou_anshang),
            u'<span class="pinYinWrapper">4 <span class="t3">kǒu</span>’<span class="t4">àn</span><span class="t4">shàng</span></span>')
        self.failUnlessEqual(cmd(_5_kouanshang),
            u'<span class="pinYinWrapper">5 <span class="t3">kǒu</span><span class="t4">àn</span><span class="t4">shàng</span></span>')
        self.failUnlessEqual(cmd(_6_fengongsi),
            u'<span class="pinYinWrapper">6 <span class="t1">fēn</span><span class="t1">gōng</span><span class="t1">sī</span></span>')
        self.failUnlessEqual(cmd(_7_aiyo),
            u'<span class="pinYinWrapper">7 <span class="t1">āi</span><span class="t1">yō</span></span>')
        self.failUnlessEqual(cmd(_8_shenme),
            u'<span class="pinYinWrapper">8 <span class="t2">shén</span><span class="t0">me</span></span>')
        self.failUnlessEqual(cmd(_9_fadia),
            u'<span class="pinYinWrapper">9 <span class="t1">fā</span><span class="t3">diǎ</span></span>')
        self.failUnlessEqual(cmd(_10_zhiding),
            u'<span class="pinYinWrapper">10 <span class="t3">zhǐ</span><span class="t4">dìng</span></span>')
        self.failUnlessEqual(cmd(_11_yi1_yi4),
            u'<span class="pinYinWrapper">11 <span class="t1">yī</span>; <span class="t4">yì</span></span>')
        self.failUnlessEqual(cmd(_12_nanguo_langxingoufei_er_eryide),
            u'<span class="pinYinWrapper">12 <span class="t2">nán</span><span class="t4">guò</span> // <span class="t2">láng</span><span class="t1">xīn</span><span class="t3">gǒu</span><span class="t4">fèi</span> // <span class="t4">èr</span>’<span class="t3">ěr</span><span class="t1">yī</span><span class="t0">de</span></span>')


class colorized_HTML_element_TestCase(unittest.TestCase):
    def should_be(self, text):
        return self.ET.tostring(
                self.ET.XML(color.colorized_HTML_string_from_string(text)), encoding='unicode')
    def cmd(self, text):
        return self.ET.tostring(color.colorized_HTML_element_from_string(text), encoding='unicode')
    def setUp(self):
        import lxml.etree as ET
        self.ET = ET
    def test_pairs(self):
        for x in [_baiwen,
                  _2_baiwen,
                  _3_nongmingong,
                  _4_kou_anshang,
                  _5_kouanshang,
                  _6_fengongsi,
                  _7_aiyo,
                  _8_shenme,
                  _9_fadia,
                  _10_zhiding,
                  _11_yi1_yi4,
                  _12_nanguo_langxingoufei_er_eryide]:
            self.assertEqual(self.cmd(x), self.should_be(x))


class ranges_of_pinyin_in_string_TestCase(unittest.TestCase):
    def setUp(self):
        self._cmd = color.ranges_of_pinyin_in_string
    def test_one_word(self):
        self.failUnlessEqual(self._cmd(u"bǎi"), [(0, 3)])
        self.failUnlessEqual(self._cmd(u" jiàn."), [(1, 4)])
        self.failUnlessEqual(self._cmd(u"...-niang, ..."), [(4, 5)])
    def test_two_words(self):
        ranges = self._cmd(u"Gōngzuò")
        self.failUnlessEqual(ranges, [(0, 4), (4, 3)])
    def test_baiwen_buru_yijian(self):
        ranges = self._cmd(_baiwen)
        self.failUnlessEqual(ranges, [(0,3), (3,3), (7,2), (9,2), (12,2),
            (14,4), (22,4), (27,2), (33,3), (36,3), (43,2), (45,5)])


class determine_tone_TestCase(unittest.TestCase):
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
    def testNonPinyin(self):
        self.failUnlessEqual(0, color.determine_tone('бурда'))
    def testMixedPinyin(self):
        self.failUnlessEqual(3, color.determine_tone('bǎiwén'))


class utilities_TestCase(unittest.TestCase):
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
