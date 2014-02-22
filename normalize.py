# -*- coding: UTF-8 -*-
'''
модуль normalize

удалить пробелы в начале, в конце, а также заменить смежные пробелы на один
'''

import re

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

# глобальная переменная, только для ф-ции spaces
_space_re = re.compile( '( |\t){2,}' )

def spaces( s ):
	'''
	обрезать пробелы внале и вконце, заменить повторяющиеся пробелы и табуляции на один пробел
	'''
	return re.sub( _space_re, ' ', s.strip())


_re_sub = (
	(
		re.compile( r'( *)\{( *)\\\[( *)' ),		# { \[
		r'\1\2\3['
	),
	(
		re.compile( r'( *)\\\]( *)\}( *)' ),		# \] }
		r']\1\2\3'
	),
	(
		re.compile( r'( *)\{( *)\(( *)\}( *)' ),	# { ( }
		r'\1\2\3\4['
	),
	(
		re.compile( r'( *)\{( *)\)( *)\}( *)' ),	# { ) }
		r']\1\2\3\4' 
	),
	(
		re.compile( r'( *)\{( *)\(( *)' ),			# { (
		r'\1\2\3['
	),
	(
		re.compile( r'( *)\)( *)\}( *)' ),			# ) }
		r']\1\2\3'
	),
	(
		re.compile( r'( *)\{( *)' ),				# {
		r'\1\2['
	),
	(
		re.compile( r'( *)\}( *)' ),				# }
		r']\1\2'
	),
	(
		re.compile( r'{.*?}' ),
		r''
	)
)

def brackets( s ):
	'''
	замена всех вариантов скобок на квадратные []

	заменяются такие комбинации:
		{ \[ ... \] }
		{ ( } ... { ) }
		{ ( ... ) }
		{ ... }
	'''
	if s.find( '{' ) is not -1:		# -1 значит не найденно
		for exp, sub in _re_sub:
			s = re.sub( exp, sub, s )
	return spaces( s )

def full( s ):
	'''
	full( 'seq[uence]' ) -> 'sequence'

	длинный вариант строки с квадратными скобками
	'''
	return s.replace( '[', '' ).replace( ']', '' )


_del_brackets_re = re.compile( r'\[.*?\]' )

def short( s ):
	'''
	short( 'seq[uence]' ) -> 'seq'

	короткий вариант строки с квадратными скобками
	'''
	return spaces( re.sub( _del_brackets_re, '', s ))

_non_id_re = re.compile( r'[^a-zA-Z0-9_]' )

def id( s ):
	s = unicode( s, 'UTF-8' )
	s = unidecode( s )
	s = s.strip()
	s = full( brackets( s ))
	s = s.lower()
	s = spaces( s ).replace( ' ', '_' )
	s = re.sub( _non_id_re, '_', s )

	return s


if __name__ == '__main__':
	s = ' попытка 	{(}to{)}   test  这个 '
	print s, 'id()', id( s )

	r = r'{(}высоко{)} поднять знамя чего-либо'
	print r, 'brackets()', brackets( r )

	t = r'в {(}самый {)}разгар'
	print t, 'full()', full( brackets( t ))

	h = r'по{ чьему-либо} адресу'
	print h, 'short()', short( brackets( h ))

	d = r'быть {\[находиться, содержаться\] }под стражей'
	print d, 'brackets()', brackets( d )