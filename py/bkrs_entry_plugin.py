#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from chinese_entry_plugin import ChineseEntryPlugin
from dsl.u import u, utf
import color
import re

class BkrsEntryPlugin( ChineseEntryPlugin ):
	"""тоже надо бы написать"""
	def __init__( self ):
		super( BkrsEntryPlugin, self ).__init__()

	def preparse( self, t, s ):
		t, s = super( BkrsEntryPlugin, self ).preparse( t, s )
		i = s.find( u'\n' )
		# сохранить пиньинь для индекса
		self.pinyin = s[ :i ].strip()
		return t, u'<div class="py">%s</div>%s' % ( self.pinyin, s[ i: ])

	def indexes( self ):
		'''
		...
		'''
		# type( a ) is set == True
		a = super( BkrsEntryPlugin, self ).indexes()

		# сокращение
		s = self.title

		# фича: ставишь точку в конце -> словарь ищет точное совпадение
		a = set([ ( i[ 0 ]+u'。', i[ 1 ] ) for i in a ])

		# вырезать всё, что не иероглиф
		s = re.sub( ur'[^\u4e00-\u9fff]', u'', s )
		a.add(( s, s ))

		# добавить индексы с подстановками 中国人, *人, 中*, 中国*, *国人
		# начинается на 中国
		# закачивается на *国
		# содержит *国*
		for x in xrange( 1, len( s )):
			part_end   = s[ x : ]
			a.add(( u'*%s' % part_end, self.title ))

			for y in xrange( 1, len( part_end )):
				# part_mid 	= part_end[ :y ]
				a.add(( u'*%s*' % part_end[ :y ], self.title ))

		# пиньинь
		if self.pinyin != u'_':
			# исходный, с диактрисами
			a.add(( self.pinyin+u'.', self.title ))

			# найти пиньинь, "выдрать" его значение из результатов, преобразовать всех в юникод
			py = map( u, [ x['value'] for x in color.search_for_pin_yin_in_string( self.pinyin )])
			# py -- список unicode строк со слогами пиньиня

			# с диактрисами, с пробелами по слогам
			a.add(( u' '.join( py )+u'.', self.title ))

			# с цифрами вместо тонов, с пробелами по слогам
			a.add(( u' '.join(
					map(
						# соеденить:
						lambda p: u'%s%d' % (
							# пиньинь без диактрисов
							color.plain_pin_yin( p ),
							# номер тона
							color.determineTone( p )
						),
						# для каждого из слогов
						py
					)
				) + u'.',
				self.title
			))

		# return jieguo, s
		return a
		# конец indexes
