#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from u import *
import re
from urllib import quote

class dslEntryPlugin( object ):
	"""
	абстрактный класс, определяет методы, которые нужно переопределить
	"""
	def __init__( self ):
		super( dslEntryPlugin, self ).__init__()
 		
	def preparse( self, t, s ):
		return t, s

	def postparse( self, t, s ):
		return t, s

	# 
	# css классы:
	#	p
	#	c
	#	sec
	#	com
	#	trn
	#	mN, где N ∈ (0..9)
	#
	simple_map = {
		u'b': ( u'<b>', u'</b>' ),
		u'u': ( u'<u>', u'</u>' ),
		u'i': ( u'<i>', u'</i>' ),
		u's': ( u'<s>', u'</s>' ),
		u'p': ( u'<span class="p">', u'</span>' ),
		u'c': ( u'<span class="c">', u'</span>' ), # без указания цвета
		u'*': ( u'<span class="sec">', u'</span>' ), # sec for SECondary
		u'ex': ( u'<em>', u'</em>' ),
		u'com': ( u'<span class="com">', u'</span>' ),
		u'trn': ( u'<span class="trn">', u'</span>' ),
		u'!trs': ( u'<noindex>', u'</noindex>' ),
		u'sub': ( u'<sub>', u'</sub>' ),
		u'sup': ( u'<sup>', u'</sup>' )
	}
	complex_map = {
		ur'^c (\w+)$': ( ur'<span style="color:\1">', u'</span>' ),
		ur'^(m\d)$': ( ur'<p class="\1">', u'</span>' )
	}

	# компиляция re при загрузке
	new_map = {}
	for key in complex_map:
		new_key = re.compile( key, re.UNICODE )
		val = complex_map[ key ]
		new_map[ new_key ] = val
	complex_map = new_map
	del new_map


	def tag_map( self, tag ):
		'''
		tag_map( '*' ) -> ( u'<span class="sec">', u'</span>' )

		найти html тег на замену dsl команде.

		возвращает tuple из двух элементов: для открывающего и закрывающего тегов.
		каждый из них может быть строкой (unicode) или функцией (lambda).
		если это функция, она должа принимать содержимое тега первым параметром и возвращать строку (unicode)
		пример:
			lambda inner: u'<a href="%s#">' % inner
		'''
		open, close = u'', u''

		# tag -- заголовоки тега. с аргументами, до скобки ]
		tag = u( tag )
		# inner -- содержание, необходимо для [url] и [ref]
		# inner = utf( inner )

		# из справки abbyy lingvo:
		#  Важно! Вложение зон индексации и команд форматирования текста одного типа недопустимо по правилам языка DSL.
		# что позволяет надеяться, что внутри тэга не будет его же самого

		if tag in dslEntryPlugin.simple_map.keys():
			return dslEntryPlugin.simple_map[ tag ]
		else:
			for key in dslEntryPlugin.complex_map:
				val = dslEntryPlugin.complex_map[ key ]
				open, close = val[0], val[1]
				_ = re.sub( key, open, tag )
				if _ != tag:
					# что-то заменилось
					return _, close
		# else:
		# url и ref -- тяжёлый случай
		if tag in ( u'url', u'ref' ):
			open = lambda inner: ur'<a href="{url}">'\
				.format(
					url = quote( utf( inner ))
				)
			return open, ur'</a>'

		# если дошли сюда -- значит тэг не верный
		raise Exception( "tag_map: что это такое ??? '%s'" % utf( tag ))

		# конец tag_map


if __name__ == '__main__':
	pl = dslEntryPlugin()

	tags = [
		'c green',
		'c skyblue',
		'm3',
		'url',
		'ref',
		'b',
		'u',
		'i',
		's',
		'p',
		'c',
		'*',
		'ex',
		'com',
		'trn',
		'!trs',
		'sub',
		'sup',
		'c aqua',
		'm10'
	]

	for tag in tags:
		_ = pl.tag_map( tag )
		if type( _[0] ) is type( lambda : None ):
			_0 = _[0]( u'mix 文化' )
		else:
			_0 = _[0]

		if type( _[1] ) is type( lambda : None ):
			_1 = _[1]( u'mix 文化' )
		else:
			_1 = _[1]

		print '%scontent%s'% ( _0, _1 )
	# pl.tag_map( tag )
