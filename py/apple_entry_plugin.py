#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
from dsl import dslEntryPlugin
from dsl.u import u, utf
from dsl import normalize
import string

digs = string.digits + string.lowercase


def int2base(x, base=10):
    if x < 0:
        sign = -1
    elif x == 0:
        return '0'
    else:
        sign = 1
    x *= sign
    digits = []
    while x:
        digits.append(digs[x % base])
        x /= base
    if sign < 0:
        digits.append('-')
    digits.reverse()
    return ''.join(digits)


def get_id_for_header():
    cnt = [0]

    def get_id_for_header(header):
        s = u'_%s' % int2base(cnt[0], 36)
        cnt[0] += 1
        return s

    return get_id_for_header


get_id_for_header = get_id_for_header()


class AppleEntryPlugin(dslEntryPlugin):
    def __init__(self):
        super(AppleEntryPlugin, self).__init__()
        self.title = u''

    def preparse():
        # замыкание, приватные статические переменные
        plain_replace_table = [
            (ur'[c][i][*][ex]', ur'[*][ex][i][c]'),  # защита от дураков
            (ur'[c][i][ex]', ur'[ex][i][c]'),
            (ur'[ex][*]', ur'[*][ex]'),
            (ur'[/*][/ex]', ur'[/ex][/*]'),
            (ur'[m2][ex]', ur'<div class="m2 e" d:priority="2">'),
            (ur'[m3][ex]', ur'<div class="m3 e" d:priority="2">'),
            (ur'[m4][ex]', ur'<div class="m4 e" d:priority="2">'),
            (ur'[m2][*][ex]', ur'<div class="m2 e" d:priority="2">'),
            (ur'[m3][*][ex]', ur'<div class="m3 e" d:priority="2">'),
            (ur'[m4][*][ex]', ur'<div class="m4 e" d:priority="2">'),
            (ur'[/ex][/*][/m]', ur'</div>'),
            (ur'[/ex][/m]', ur'</div>'),
            (ur'[*][ex]', ur'<div class="e" d:priority="2">'),
            (ur'[/ex][/*]', ur'</div>'),
            (ur'[*]', ur'<div d:priority="2">'),
            (ur'[/*]', ur'</div>')
        ]

        reg_sub_table = [
            (ur'(\D)(([2-9]|\d{2})\))', ur'\1\n\2')  # новая строка перед пунктами 1) 2) 3)
        ]

        # скомпилировать регулярки перед запуском
        reg_sub_table = map(lambda (r, s): (re.compile(r, re.UNICODE), s), reg_sub_table)

        def preparse(self, t, s):
            # запомнить для postparse
            self.title = normalize.full(t)
            self.title_short = normalize.short(t)

            for (old, new) in plain_replace_table:
                s = s.replace(old, new)
            for (reg, sub) in reg_sub_table:
                s = reg.sub(sub, s)
            return t, s

        return preparse

    preparse = preparse()

    def postparse():
        # замыкание, приватные статические переменные
        href_re = re.compile(ur'href="(.+?)"', re.UNICODE)

        def postparse(self, t, s):
            return \
                u'<d:entry id="{id}" d:title="{title}">{indx}{header}{content}</d:entry>'.format(
                    id=get_id_for_header(t),
                    title=self.title,
                    indx=u''.join([
                        ur'<d:index d:value="%s" d:title="%s"/>' % (value, title)
                        for (value, title) in list(self.indexes())
                        if value.strip() != u'' and title.strip() != u''
                    ]),
                    header=t,
                    content=href_re.sub(
                        lambda x:
                            x.group()
                            if x.groups()[0].startswith('http') else
                            ur'href="x-dictionary:d:%s"' % x.groups()[0],
                        s
                    )
                )
            # конец postparse
        return postparse
    postparse = postparse()

    def indexes(self):
        """
        indexes() -> list

        список индексов в формате:
        list(
            tuple(value, title),
            ...
        )
        """
        a = {(self.title, self.title)}
        a.add((self.title_short, self.title))
        return a

    def index(value, title):
        """
        # deprecated!

        index(value, title) -> u'<d:index …>'

        отставленна на всякий полезный случай
        """
        if value.strip() == u'' or \
           title.strip() == u'':
            return u''
        return ur'<d:index d:value="%s" d:title="%s"/>' % (value, title)
