#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
создание всех возможных вариантов для индекса

содержит только публичную одну функцию -- indexes()
'''

# ########################################################################## #
#                     !! внутри используется unicode !!                      #
#             !! для связи в внешним миром используется utf-8 !!             #
#                                                                            #
#                  вход в модуль: indexes()                                  #
#                  входные данные:                                           #
#                               <utf-8> s, reading                           #
#                  выходные данные:                                          #
#                               tuple ->                                     #
# ########################################################################## #

import re
import normalize
from rm_unicode import *
import color

try:
	import pymorphy2
	morphy = pymorphy2.MorphAnalyzer()
except:
	import sys
	print >>sys.stderr, '''
модуль 'pymorphy2' не установлен на этой машине.
ты можешь скачать его вот отсюда
http://pymorphy2.readthedocs.org/en/latest/
'''
	exit(1)

def _test_all_hz( s ):
	return all( u'\u4e00' <= c <= u'\u9fff' for c in s )

def _test_any_hz( s ):
	return any( u'\u4e00' <= c <= u'\u9fff' for c in s )

def _test_any_ru( s ):
	return any( u'а' <= c <= u'я' for c in s.lower())

def generate_hz_indexes( s, reading ):
	jieguo = set()
	s = re.sub( ur'[^\u4e00-\u9fff]', u'', s )	# вырезать всё, что не иероглиф
	jieguo.add( s )

	# добавить индексы с подстановками 中国人, *人, 中*, 中国*, *国人
	# начинается на 中国
	# закачивается на *国
	# содержит *国*
	for x in xrange( 1, len( s )):
		part_end   = s[ x : ]
		jieguo.add( u'*%s' % part_end )
		# print u'part_end: %s' % part_end
		for y in xrange( 1, len( part_end )):
			part_mid 	= part_end[ :y ]
			# print u'x: %d, y: %d, part_mid: %s' % ( x, y, part_mid )
			jieguo.add( u'*%s*' % part_mid )
	# пиньинь
	if reading != u'_':
		jieguo.add( reading )

		py = map( u, [ x['value'] for x in color.search_for_pin_yin_in_string( reading )])
		jieguo.add( u' '.join( py )) 		# с диактрисами

		jieguo.add( u' '.join(
				map( lambda p: u'%s%d' % (
					color.plain_pin_yin( p ),
					color.determineTone( p )
					),
				py )
			)
		)

	return jieguo, s


def generate_ru_indexes():
	not_ru_re = re.compile( u'[^-а-яА-ЯёЁ ]', re.UNICODE )

	def recursive( slova ):
		'''
		recursive( slova ) -> set
		slova -- list of list of word forms

		самое левое слово в очередь
		пример:
			полная ложка дёгтя
			ложка дёгтя
			дёгтя
			[]
		'''
		if len( slova ) < 1:
			return set()
		else:
			jieguo = set([])
			for i in range( len( slova )):
				s = slova[ i: ]
				jieguo.update( add_left_part( set(['']), s ))
			return jieguo

	def add_left_part( jieguo, slova ):
		'''
		самое правое слово в очередь

		полная ложка дёгтя
		полная ложка
		полная
		'''
		if len( slova ) < 1:
			return jieguo
		else:
			# добавить правое слова
			return add_right_part( add_left_part( jieguo, slova[ :-1 ] ), slova[ -1 ])

	def add_right_part( jieguo, sforms ):
		'''
		прилепить слово из sforms к каждому jieguo
		'''
		if len( sforms ) <= 0:
			return jieguo
		elif len( jieguo ) <= 0:
			return set( sforms )
		else:
			xin_jieguo = set()
			for j in jieguo:
				for form in sforms:
					xin_jieguo.add( form if j == u'' else u' '.join([ j, form ]) )
			return xin_jieguo
	
	def generate_ru_indexes( s ):
		'''
		generate_ru_indexes( slova ) -> set
		'''
		jieguo = set()

		s = u( normalize.brackets( s ))
		full = s

		if s.find( '[' ) is not -1:
			full = u( normalize.full( s ))
			jieguo.add( full )
			jieguo.add( u( normalize.short( s )))

		# выпилить всё нерусское
		s = u( normalize.spaces( re.sub( not_ru_re, u'', s )))
		words = s.split(' ')

		# индекс занимает слишком много места
		index_max = 1
		words_to_index = words[ :index_max ] if len( words ) > index_max else words

		slova = []

		for w in words_to_index:
			normal_form = morphy.parse( w )
			if len( normal_form ) > 0:
				normal_form = normal_form[0]
			else:
				break
			forms = set() # формы одного слова
			for x in normal_form.lexeme:
				forms.add( x.word )
			slova.append( forms )

		jieguo.update( recursive( slova ))

		if len( words ) > index_max:
			words = words[ index_max: ]
			xin_jieguo = set()
			for juzi in jieguo:
				l = [ juzi ]
				l.extend( words )
				xin_jieguo.add( u' '.join( l ))
			jieguo = xin_jieguo

		return jieguo, full

	return generate_ru_indexes, recursive, add_left_part, add_right_part
generate_ru_indexes, recursive, add_left_part, add_right_part = generate_ru_indexes()

	

def indexes( s, reading=None ):
	'''
	indexes( s[, reading ]) -> tuple, str

	список всех переборов с подстановками, комбинациями, склонениями,
	падежами и прочей красотой.
	при этом знаки препинания исключаются из всех вариантов, кроме
	одного -- полного исходного
	возвращаемое значение:
		- typle из всех возможных комбинаций
		- str: полный вариант фразы. utf-8
	'''
	# вход в модуль. дальше -- unicode
	s = u( s )
	reading = u( reading.strip() ) if reading else None
	full = s

	jieguo = set()

	if _test_any_hz( s ):
		# это китайский
		jieguo, full = generate_hz_indexes( s, reading )
		jieguo.add( s )	# добавить

	elif _test_any_ru( s ):
		# скорее всего, тут русский
		jieguo, full = generate_ru_indexes( s )
		jieguo.add( s )	# добавить

	else:
		jieguo.add( s )
		# еггог
		# raise Exception( u'indexes: тут какая-то борода: %s' % s )
	# где-то иногда добавляются пустые строки
	try:
		jieguo.remove( u'' )
	except:
		pass
	# выход из модуля. возврар в utf-8
	return tuple( map( utf, jieguo )), utf( full )


def main():
	# test
	w = [
		[ u'полный', u'полная' ],
		[ u'ложка', u'ложки', u'ложкой' ],
		[ u'дёгтя', u'дёготь' ]
	]

	l = add_left_part( w[ 0 ], w[ 1: ] )
	for i in l: print i

	print '-------------------'

	r, f = generate_ru_indexes( u'полная ложка дёгтя' )
	# r = recursive( w )
	for k in r:
		print k
	print '-------------------'
	print u'итого: %d' % len( r )

	print '----'

	s = '大开发者'
	p = 'ruǎnjiàn kāifāzhě'
	print s
	print '--------------------'
	for i in indexes( s, p )[0]: print i
	print '--------------------'

if __name__ == '__main__':
	main()