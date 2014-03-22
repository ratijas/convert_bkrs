# -*- coding: UTF-8 -*-
u'''
модуль normalize

удалить пробелы в начале, в конце, а также заменить смежные пробелы на один
'''

import re
from rm_unicode import u, utf

try:
	from unidecode import unidecode
except:
	import sys
	print >>sys.stderr, '''
модуль 'unidecode' не установлен на этой машине.
ты можешь скачать его с оффициального сайта питона
https://pypi.python.org/packages/source/U/Unidecode/Unidecode-0.04.14.tar.gz
'''
	exit(1)


def spaces():
	# глобальная переменная, только для ф-ции spaces
	space_re = re.compile( ur'( |\t){2,}', re.UNICODE )

	def spaces( s ):
		'''
		обрезать пробелы внале и вконце, заменить повторяющиеся пробелы и табуляции на один пробел
		'''
		return utf( re.sub( space_re, u' ', u( s ).strip() ))
	return spaces
spaces = spaces()

def brackets():
	re_sub = (
		(
			re.compile( ur'( *)\{( *)\\\[( *)', re.UNICODE ),		# { \[
			ur'\1\2\3['
		),
		(
			re.compile( ur'( *)\\\]( *)\}( *)', re.UNICODE ),		# \] }
			ur']\1\2\3'
		),
		(
			re.compile( ur'( *)\{( *)\(( *)\}( *)', re.UNICODE ),	# { ( }
			ur'\1\2\3\4['
		),
		(
			re.compile( ur'( *)\{( *)\)( *)\}( *)', re.UNICODE ),	# { ) }
			ur']\1\2\3\4' 
		),
		(
			re.compile( ur'( *)\{( *)\(( *)', re.UNICODE ),			# { (
			ur'\1\2\3['
		),
		(
			re.compile( ur'( *)\)( *)\}( *)', re.UNICODE ),			# ) }
			ur']\1\2\3'
		),
		(
			re.compile( ur'( *)\{( *)', re.UNICODE ),				# {
			ur'\1\2['
		),
		(
			re.compile( ur'( *)\}( *)', re.UNICODE ),				# }
			ur']\1\2'
		),
		(
			re.compile( ur'{.*?}', re.UNICODE ),
			ur''
		)
	)

	def brackets( s ):
		r'''
		замена всех вариантов скобок на квадратные []

		заменяются такие комбинации:
			{ \[ ... \] }
			{ ( } ... { ) }
			{ ( ... ) }
			{ ... }
		'''
		s = u( s )
		if s.find( u'{' ) is not -1:		# -1 значит не найденно
			for exp, sub in re_sub:
				s = re.sub( exp, sub, s )
		return utf( spaces( s ))
	return brackets
brackets = brackets()


def full( s ):
	'''
	full( 'seq[uence]' ) -> 'sequence'

	длинный вариант строки с квадратными скобками
	'''
	return utf( u( s ).replace( '[', '' ).replace( ']', '' ))


def short():
	del_brackets_re = re.compile( ur'\[.*?\]', re.UNICODE )

	def short( s ):
		'''
		short( 'seq[uence]' ) -> 'seq'

		короткий вариант строки с квадратными скобками
		'''
		return utf( spaces( re.sub( del_brackets_re, u'', u( s ))))
	return short
short = short()

def id():
	non_id_re = re.compile( r'[^a-zA-Z0-9_]' )

	def id( s ):
		s = u( s )
		s = unidecode( s )
		s = u( s )
		s = s.strip()
		s = brackets( s )
		s = full( s )
		s = s.lower()
		s = spaces( s )
		s = s.replace( ' ', '_' )
		s = re.sub( non_id_re, '_', s )
		s = utf( s )
		return s
	return id
id = id()

if __name__ == '__main__':
	s = u' попытка 	{(}to{)}   test  这个 '
	print s, '\t\t id() \t\t', id( s )

	r = ur'{(}высоко{)} поднять знамя чего-либо'
	print r, '\t\t brackets() \t\t', brackets( r )

	t = ur'в {(}самый {)}разгар'
	print t, '\t\t full() \t\t', full( brackets( t ))

	h = ur'по{ чьему-либо} адресу'
	print h, '\t\t short() \t\t', short( brackets( h ))

	d = ur'быть {\[находиться, содержаться\] }под стражей'
	print d, '\t\t brackets() \t\t', brackets( d )