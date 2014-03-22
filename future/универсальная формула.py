#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pymorphy2
m = pymorphy2.MorphAnalyzer()

# согласование слова с количеством
word = u'предметов'
count = 3
agree = ( m.parse( m.parse( word )[ 0 ].normal_form )[ 0 ] ).make_agree_with_number( count ).word

print count, agree


# вывод всех форм слова
s = u'телефоном'
word = m.parse( s )[ 0 ]
forms = [ x.word for x in word.lexeme ]

for x in forms: print x
