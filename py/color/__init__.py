#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''searching for pinyin and wrap it with HTML.

module provides some useful functions for working with Chinese pinyin,
"phonetic system for transcribing the Mandarin pronunciations of
Chinese characters into the Latin alphabet" (c) wikipedia.

modify given DOM by replacing children text nodes containing pinyin with
wrapper element:
``colorize_DOM``

undo colorize:
``uncolorize_DOM``

detect and wrap pinyin with HTML in plain text string:
``colorized_HTML_string_from_string``

do the same, but returns a wrapper -- DOM element:
``colorized_HTML_element_from_string``

searching for pinyin in string of text:
``ranges_of_pinyin_in_string``

finding out what tone has some pinyin word:
``determine_tone``

remove tones (diacritics) from pinyin string:
``lowercase_string_by_removing_pinyin_tones``

constants:

PINYIN_LIST -- specially sorted list of all possible pinyin words.

PINYIN_WRAPPER_CLASS -- default class used by ``[un]colorize_DOM``.
'''

import re
from u import u, utf

__all__ = [
    'ignore_link_and_input_node_filter',
    'colorize_DOM',
    'uncolorize_DOM',
    'colorized_HTML_string_from_string',
    'colorized_HTML_element_from_string',
    'ranges_of_pinyin_in_string',
    'determine_tone',
    'lowercase_string_by_removing_pinyin_tones',
    'PINYIN_LIST',
    'PINYIN_WRAPPER_CLASS',
    'TONES_CLASSES',
    ]

PINYIN_LIST = u'zhuang,shuang,chuang,zhuan,zhuai,zhong,zheng,zhang,xiong,xiang,shuan,shuai,sheng,shang,qiong,qiang,niang,liang,kuang,jiong,jiang,huang,guang,chuan,chuai,chong,cheng,chang,zuan,zong,zhuo,zhun,zhui,zhua,zhou,zhen,zhei,zhao,zhan,zhai,zeng,zang,yuan,yong,ying,yang,xuan,xing,xiao,xian,weng,wang,tuan,tong,ting,tiao,tian,teng,tang,suan,song,shuo,shun,shui,shua,shou,shen,shei,shao,shan,shai,seng,sang,ruan,rong,reng,rang,quan,qing,qiao,qian,ping,piao,pian,peng,pang,nüe,nuan,nong,ning,niao,nian,neng,nang,ming,miao,mian,meng,mang,lüe,luan,long,ling,liao,lian,leng,lang,kuan,kuai,kong,keng,kang,juan,jing,jiao,jian,huan,huai,hong,heng,hang,guan,guai,gong,geng,gang,feng,fang,duan,dong,ding,diao,dian,deng,dang,cuan,cong,chuo,chun,chui,chua,chou,chen,chao,chan,chai,ceng,cang,bing,biao,bian,beng,bang,zuo,zun,zui,zou,zhu,zhi,zhe,zha,zen,zei,zao,zan,zai,yun,yue,you,yin,yao,yan,xun,xue,xiu,xin,xie,xia,wen,wei,wan,wai,tuo,tun,tui,tou,tie,tao,tan,tai,suo,sun,sui,sou,shu,shi,she,sha,sen,sei,sao,san,sai,ruo,run,rui,rua,rou,ren,rao,ran,qun,que,qiu,qin,qie,qia,pou,pin,pie,pen,pei,pao,pan,pai,nü,nuo,nou,niu,nin,nie,nen,nei,nao,nan,nai,mou,miu,min,mie,men,mei,mao,man,mai,lü,luo,lun,lou,liu,lin,lie,lia,lei,lao,lan,lai,kuo,kun,kui,kua,kou,ken,kei,kao,kan,kai,jun,jue,jiu,jin,jie,jia,huo,hun,hui,hua,hou,hen,hei,hao,han,hai,guo,gun,gui,gua,gou,gen,gei,gao,gan,gai,fou,fen,fei,fan,duo,dun,dui,dou,diu,die,dia,den,dei,dao,dan,dai,cuo,cun,cui,cou,chu,chi,che,cha,cen,cao,can,cai,bin,bie,ben,bei,bao,ban,bai,ang,zu,zi,ze,za,yu,yo,yi,ye,ya,xu,xi,wu,wo,wa,tu,ti,te,ta,su,si,se,sa,ru,ri,re,qu,qi,pu,po,pi,pa,ou,nu,ni,ng,ne,na,mu,mo,mi,me,ma,lu,li,le,la,ku,ke,ka,ju,ji,hu,he,ha,gu,ge,ga,fu,fo,fa,er,en,ei,du,di,de,da,cu,ci,ce,ca,bu,bo,bi,ba,ao,an,ai,o,n,m,e,a,r'.split(',')
# sorted by length, so first look up the longest variant.

PINYIN_WRAPPER_CLASS = u'pinYinWrapper'

TONES_CLASSES = (u"t0", u"t1", u"t2", u"t3", u"t4")


def ignore_link_and_input_node_filter(node):
    import lxml.etree as ET
    if node.tag.lower() in ("a", "input"):
        return False
    return True


def colorize_DOM(root_node,
                 node_filter=ignore_link_and_input_node_filter,
                 pinyin_wrapper_class=PINYIN_WRAPPER_CLASS,
                 tones_classes=TONES_CLASSES):
    '''colorize_DOM(root_node, node_filter, pinyin_wrapper_class, tones_classes) --> None

    modify given DOM in place.  using ``etree``.
    detect and colorize pinyin in text nodes of *root_node* and its
    child nodes ignoring nodes for which *node_filter* returns False.
    text nodes will be replaced with <span> wrapper whose class
    attribute is *pinyin_wrapper_class*.
    wrapper will contain only text nodes and <span>s with one of
    *tones_classes* accordingly to the tone of containing pinyin.

    parameters:
        root_node -- instance of ``etree``.
        node_filter -- callable.
            parameters:
                node -- instance of ``etree``.
            return value:
                True to allow function to look up for pinyin inside
                node itself or its child nodes, otherwise False.
                its useful to deny colorizing of <a> or other elements
                that should have their own colors by design.
        pinyin_wrapper_class -- class for wrapper <span>
        tones_classes -- 5-tuple of class names for <span> inside
            wrapper.  element with index [0] will be used for zero
            tone, [1] for first and so on.

    return value:
        None
    '''
    if node_filter is None:
        node_filter = lambda: True
    # loop instead recursion
    node_stack = [root_node]
    for child in node_stack[-1]:
        if node_filter(child):
            pass



def uncolorize_DOM(root_node, pinyin_wrapper_class=PINYIN_WRAPPER_CLASS):
    '''uncolorize_DOM(root_node, pinyin_wrapper_class) --> None

    opposite to ``colorize_DOM``.  replace back wrappers (nodes with
    class equal to *pinyin_wrapper_class*) with contained text.
    '''
    pass


def colorized_HTML_string_from_string(
        string,
        pinyin_wrapper_class=PINYIN_WRAPPER_CLASS,
        tones_classes=TONES_CLASSES):
    '''colorized_HTML_string_from_string(string[, pinyin_wrapper_class][, tones_classes]) --> unicode

    !! replacing obsolete ``colorize_pin_yin``.

    detect and wrap pinyin with HTML in plain text *string*.  if no
    pinyin found, string won't be modified and no wrapper applied.

    return value:
        string represents one HTML element <span> whose class is
        *pinyin_wrapper_class*.  it contains child text nodes and
        inner <span>s with classes set according to contained pinyin
        tone.  these classes can be specified by *tone_classes*
        argument.
        returns *string* if no pinyin found or all tones are zero.
    '''
    string = u(string)
    ranges = ranges_of_pinyin_in_string(string)
    if not ranges:
        return string

    words = map(lambda r: r._slice(string), ranges)
    tones = map(determine_tone, words)
    if not any(tones):
        return string  # all tones are zero, probably it is not pinyin.

    # do a colorize work here
    prev_end = 0
    result = u'<span class="%s">' % pinyin_wrapper_class
    for range, word, tone in zip(ranges, words, tones):
        result += string[prev_end:range.location]
        # colorize one word
        result += u'<span class="{}">{}</span>'.format(
                   tones_classes[tone], word)
        prev_end = range.location + range.length
    result += string[prev_end:] + u"</span>"
    return result


def colorized_HTML_element_from_string(
        string,
        pinyin_wrapper_class=PINYIN_WRAPPER_CLASS,
        tones_classes=TONES_CLASSES):
    '''colorized_HTML_element_from_string(string[, pinyin_wrapper_class][, tones_classes]) --> etree.Element or *string*

    same as ``colorized_HTML_string_from_string``, but returns an
    ``etree.Element``.
    '''
    string = u(string)
    ranges = ranges_of_pinyin_in_string(string)
    if not ranges:
        return string

    # do a colorize work here
    words = map(lambda r: r._slice(string), ranges)
    tones = map(determine_tone, words)
    if not any(tones):
        return string  # all tones are zero, probably it is not pinyin.

    import lxml.etree as ET
    prev_end = 0
    wrapper = ET.Element("span")
    wrapper.set("class", pinyin_wrapper_class)
    wrapper.text = string[:ranges[0].location]
    for i, range in enumerate(ranges):
        word = range._slice(string)
        span = ET.SubElement(wrapper, "span")
        span.set("class", tones_classes[determine_tone(word)])
        span.text = word
        if len(ranges) > i + 1:
            span.tail = string[range.location + range.length:ranges[i+1].location]
    return wrapper


# ---- static vars
_diacritics = (
    (u'āáǎăà',    u'a'),
    (u'ēéěè',     u'e'),
    (u'ōóǒò',     u'o'),
    (u'ūúǔùǖǘǚǜ', u'u'),
    (u'īíǐì',     u'i')
)

def lowercase_string_by_removing_pinyin_tones(s):
    '''lowercase_string_by_removing_pinyin_tones(string) --> unicode

    simplify / plainize chinese pinyin by converting it to lower case and
    removing diacritics from letters 'a', 'e', 'o', 'u', i'.
    '''
    s = u(s).lower()
    for diacrs, normal in _diacritics:
        for diacr in diacrs:
            s = s.replace(diacr, normal)
    return s



# ---- static vars
_t1 = u"āēūǖīō"
_t2 = u"áéúǘíó"
_t3 = u"ǎăěǔǚǐǒ"
_t4 = u"àèùǜìò"

def determine_tone(pinyin):
    '''determine_tone(string) --> {0..4}

    detect tone of given pinyin word.
    return value:
        int from 0 up to 4, where 0 means that tone undetermined.
    '''
    pinyin = u(pinyin)
    for letter in pinyin:
        if letter in _t1:
            return 1
        if letter in _t2:
            return 2
        if letter in _t3:
            return 3
        if letter in _t4:
            return 4
    # not found, fall-back to  zero
    return 0


# ---- static vars
from collections import namedtuple
_range = namedtuple("_range", ("location", "length"))
def _slice(self, obj):
    return obj[self.location : self.location + self.length]
_range._slice = _slice

def ranges_of_pinyin_in_string(s):
    '''ranges_of_pinyin_in_string(string) --> list<_range>

    !! replacing obsolete ``search_for_pin_yin_in_string``.

    searches for pinyin in given string *s*.  *s* must be either
    unicode string or utf-8 encoded ``str``, or anything else that
    can be converted by ``u`` function.

    return value:
        list of ranges of pinyin,
        where ``_range`` is 2-namedtuple of (location, length).
        list can be empty.
    '''
    result = []

    # the trick of replacing 'v' is that 'v' does not exists in pinyin,
    # but still returns *True* on str.islower()
    plain_s = lowercase_string_by_removing_pinyin_tones(s).replace(u'v', u' ')
    plain_s_len = len(plain_s)

    char_p = 0  # scan through whole string, skipping len(found) chars.
    while char_p < plain_s_len:
        # scan for next nearest beginning of pinyin word,
        # e.g for small(1) latin char [a-z].
        # (1) small because after ``lowercase_...`` no caps left.
        if not plain_s[char_p].islower():
            char_p += 1
            continue
        # now char_p pointing at lowercase letter

        # try to match string to pinyin from the list.  remember that list is
        # sorted by length.
        for word in PINYIN_LIST:
            word_len = len(word)

            if plain_s[char_p : char_p + word_len] == word:
                # rule of apostrophe in pinyin:
                #   "'" must be before 'a', 'e' and 'o'.
                #
                # if next letter exactly 'a', 'e' or 'o',
                #   do a rollback by one letter and check, if such word exists.
                #
                # remember that a pinyin never begins with 'i' or 'u',
                #   and 'v' already replaced with space before the loop.
                if char_p + word_len + 1 < plain_s_len and\
                    plain_s[char_p + word_len] in 'aoeiu':

                    shorten_word = word[:-1]

                    if shorten_word in PINYIN_LIST:
                        word = shorten_word
                        word_len = len(word)
                    #else:
                        # then our rollback failed,
                        # there should be an error in pinyin,
                        # but we'll try hard to save the situation.
                        # let's leave non-shorten word and be happy
                # *word* keeps the word we found.
                break
        else:
            # loop exited normally, means word not matches pinyin
            # but the letter is latin.  so we need to skip all subsequence
            # latins.  and spaces also.
            while char_p < plain_s_len and not plain_s[char_p].isspace():
                char_p += 1
            while char_p < plain_s_len and plain_s[char_p].isspace():
                char_p += 1
            word = None

        # add word if there's one.
        if word:
            result.append(_range(char_p, word_len))
            char_p += word_len
        # else:
            # means that a letter is latin, but pinyin not found.
            # skipping already done on for's *else* branch.

    return result


def colorize(s):
    '''colorize(s) --> unicode

    !! obsoleted by ``colorize_DOM``.  use that one instead.
    '''
    raise NotImplementedError(
        "obsoleted by ``colorize_DOM``.  use that one instead.")


def search_for_pin_yin_in_string(s):
    '''search_for_pin_yin_in_string(s) --> list

    !! obsoleted by ``ranges_of_pinyin_in_string``.  use that one instead.
    '''
    raise NotImplementedError(
        "obsoleted by ``ranges_of_pinyin_in_string``.  use that one instead.")


def colorize_pin_yin(text, pin_yin_pairs):
    '''colorize_pin_yin(text, pin_yin_pairs) --> str

    !! obsoleted by ``colorized_HTML_string_from_string`` and
    ``colorized_HTML_element_from_string``.  use one of those instead.
    '''
    raise NotImplementedError(
        "obsoleted by ``colorized_HTML_string_from_string`` and "
        "``colorized_HTML_element_from_string``.  use one of those instead.")
