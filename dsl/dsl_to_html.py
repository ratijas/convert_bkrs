#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from u import u, utf

def dsl_to_html( text ):
	return step2( step1( u( text ).strip() ))


# шаг 1
# преобразовать dsl в html с помощью str.replace и re.sub

import re

def step1():
	plain_replace_table = [
		( ur'\[', ur'&#91;' ),
		( ur'\]', ur'&#93;' ),
		# ( u'\n', u'<br/>' ),
		( u'[b]', u'<b>' ),
		( u'[/b]', u'</b>' ),
		( u'[c][i]', u'[i][c]' ),
		( u'[/i][/c]', u'[/c][/i]' ),
		( u'[i]', u'<i>' ),
		( u'[/i]', u'</i>' ),
		( u'[c]', u'<span class="green">' ),
		( u'[/c]', u'</span>' ),
		( u'[e]', u'[ex]' ),
		( u'[/e]', u'[/ex]' ),
		( u'[ex]', u'<div class="e">' ),
		( u'[/ex]', u'</div>' ),
		( u'[/m]', u'</div>' ),
		( u'[*]', u'<div class="sec">' ),
		( u'[/*]', u'</div>' ),
		( u'[p]', u'<i class="green">' ),
		( u'[/p]', u'</i>' ),
		( u'[com]', u'<div class="com">' ),
		( u'[/com]', u'</div>' ),
		( u'[trn]', u'<div class="trn">' ),
		( u'[/trn]', u'</div>' ),
		( u'[!trs]', u'<noindex>' ),
		( u'[/!trs]', u'</noindex>' ),
		( u'[sub]', u'<sub>' ),
		( u'[/sub]', u'</sub>' ),
		( u'[sup]', u'<sup>' ),
		( u'[/sup]', u'</sup>' )
	]
	reg_sub_table = [
		( ur'\[c (.+?)\]',	ur'<span style="color=\1">' ),
		( ur'- \[ref\](.+?)\[\/ref\]',	ur'<div class="m2">- [ref]\1[/ref]</div>' ),
		( ur'\[ref\](.+?)\[\/ref\]',	ur'<a href="\1">\1</a>' ),
		( ur'\[url\](.+?)\[\/url\]',	ur'<a href="\1">\1</a>' ),
		( ur'\[m(\d)\]',	ur'<div class="m\1">' )
	]

	# скомпилировать регулярки перед запуском
	reg_sub_table = map( lambda (r, s): ( re.compile( r, re.UNICODE ), s ), reg_sub_table )

	def step1( text ):
		for old, new in plain_replace_table:
			text = text.replace( old, new )
		for old, new in reg_sub_table:
			text = re.sub( old, new, text )
		return text
	return step1
step1 = step1()


# шаг 2
# сделать наш html “правильным” на все 100%
# с помощью парсера

from lxml import etree
from io import StringIO

def step2():
	# нужна оболочка, например <body>, или <z>
	# без костыля xmlns будет ошибка парсера
	body_start, body_end = u'<z xmlns:d="d">', u'</z>'

	def step2( text ):
		# обернуть
		text = u'%s%s%s' % ( body_start, text.replace( u'&', u'&amp;' ), body_end )

		# создать парсер
		parser = etree.XMLParser( recover=True, encoding="ascii" )

		# попарсить дерево
		tree = etree.parse( StringIO( u( text.encode( 'ascii', 'xmlcharrefreplace' ))), parser )

		# будет не совсем красиво, зато ничего не сломается
		els = tree.xpath('span/div') + tree.xpath('i/div') + tree.xpath('b/div')
		for el in els:
		    el.tag = 'span'

		# распечатать в unicode, иначе -- куча багов
		text = etree.tostring( tree, encoding='unicode', xml_declaration=False )

		# вырезать оболочку <body>...</body>
		text = text.strip()[ len( body_start ) : -len( body_end ) ]

		return text
	return step2
step2 = step2()
