#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
модуль-декоратор, направленный упрощение создания словаря с помощью модуля rm_xml

предоставленные здесь функции являются оболочкой для вызова ряда функций из rm_xml
'''

from rm_xml import *
import normalize
import re
import sys		# sys.stderr

stack = []
'стек вложеных тегов по мере разбора строка bb-кода'

def dictionary_open():
	'''
	<d:dictionary ...> открывающий тег
	'''
	return '\n<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">'

def dictionary_close():
	'''
	</d:dictionary> закрывающий тег
	'''
	return '\n</d:dictionary>'

id_set = set()
'идентификатор не должен регистрироваться дважды'

def make_id( s, only_get=False ):
	'''
	создать идентификатор и проследить, чтобы он не повторялся
	'''
	id = normalize.id( s )

	if not check_id( id ):
		raise Exception( 'make_id: невозможно создать валидный id (%s)' % id )

	if not only_get:
		h = hash( id )
		if h in id_set:
			raise Exception( 'make_id: идентификатор "%s" уже зарегистрирован' % id )
		id_set.add( h )
	return id

def entry( title ):
	id = make_id( title )
	full = normalize.full( normalize.brackets( title ))

	en = xml_node( 'd', 'entry', attr=(
		xml_attr( '', 'id', id ),
		xml_attr( 'd', 'title', full )
	))

	en.add_child( *index( title ))

	en.add_child( header( full ))

	return en

def _index( value, title=None ):
	'''
	создать индекс для конкретных title, value
	'''
	if title is None:
		title = value
	return xml_node( 'd', 'index', True, attr=(
		xml_attr( 'd', 'value', value ),
		xml_attr( 'd', 'title', title )
		)
	)

def index( s ):
	'''
	index( title ) -> list

	создать индексы для всех возможных вариантов
	возвращает список из xml_node
	'''
	indexes = []

	s = normalize.brackets( s )
	if s.find( '[' ) is not -1:
		full = normalize.full( s )
		short = normalize.short( s )
		
		indexes.append( _index( value=full ))
		indexes.append( _index( value=short, title=full ))
	else:
		indexes.append( _index( value=s ))
	return indexes


def generate_el( name ):
	if name[0] == 'm':
		if len( name ) == 2:
			return paragraph( int( name[1] ))
		else:
			return paragraph()
	elif name == 'p' or name == 'c':
		return mark()
	elif name == 'div':
		return div()
	elif name == 'i':
		return italic()
	elif name == 'b':
		return bold()
	elif name == '*':
		return span()
	elif name == 'ex':
		return example()
	elif name == 'ref':
		# end_ptr = s.find( '[' )
		# if end_ptr == -1:
		# 	print >>sys.stderr, '<-- generate_el: тег a не закрыт -->'
		return link( '#' )
	elif name == 'br':
		return br()
	elif name in ( 'ol', 'ul', 'li' ):
		return xml_node( name=name )
	elif name in ( 'table', 'tr', 'td' ):
		return xml_node( name=name )
	else:
		raise Exception( 'generate_el: неизвестный тег (%s)' % name )


token_type_string  = 0
token_type_tag_open = 1
token_type_tag_close = 2

def gettoken( s ):
	'''
	gettoken( s ) -> tuple

	разбор строки с bb-кодом на токены. возвращает первый токен в строке: тег или текст.
	возвращаемое зночение:
		tuple( int type, string value, int length )
	type -- тип токена. возможные значения:
		0 -- строка 			'..'
		1 -- открывающий тег 	'[..]'
		2 -- закрывающий тег 	'[/..]'
	value -- значение токена. для тегов скобки и обратные слеши убираются. 'm1', 'ref'
	length -- исходная длинна токена в символах. особенно актуально для тегов
	'''
	type = 0
	value = None
	length = 0

	if s[0] == '[':
		tag_end_ptr = s.find( ']' )		# конец имени тега, не скобки
		if tag_end_ptr == -1:
			raise Exception( 'gettoken: тег не закрыт (%s)' % s )

		length = tag_end_ptr + 1 		# преобразование указателя в длинну

		space_ptr = s.find( ' ', 2, tag_end_ptr )
		if space_ptr != -1:				# на случай всяких там [c black]
			tag_end_ptr = space_ptr

		if s[ 1 ] == '/':
			type 	= token_type_tag_close
			value 	= s[ 2 : tag_end_ptr ]
		else:
			type 	= token_type_tag_open
			value 	= s[ 1 : tag_end_ptr ]
	else:
		type 	= token_type_string
		tag_begin_ptr = s.find( '[' )
		if tag_begin_ptr == -1:
			value = s
		else:
			value = s[ : tag_begin_ptr ]
		length = len( value )

	return type, value, length


def parse( s ):
	'''
	parse( s ) -> list

	парсер bb-кода. для разбора bb-кода передать только строку с кодом.
	возвращает list из xml_node
	'''

	stack_xml 	= []			# стек xml. последний элемент -- текущая ветка
	stack_bb 	= []

	ptr 	= 0
	slen 	= len( s )
	result 	= []
	curnode = result

	while ptr < slen:
		ttype, tval, tlen = gettoken( s[ ptr : ])

		if ttype == token_type_string:
			curnode.append( xml_text( tval ))

		elif ttype == token_type_tag_open:
			if tval.startswith( 'm' ):
				tval = 'm'			# тег абзаца m1..m9 закрывается тегом [/m]
			el = generate_el( tval )
			curnode.append( el )
			
			if tval == 'ref':
				curnode.append( br())

			if not el.single:
				stack_bb.append( tval )
				stack_xml.append( el )
				curnode = el

		elif ttype == token_type_tag_close:
			if len( stack_bb ) > 0 and ( stack_bb[ -1 ] in ( tval, 'c' )): # часто глюки на [c]
				stack_bb.pop()
				stack_xml.pop()

				if len( stack_xml ) > 0:
					curnode = stack_xml[ -1 ]
				else:
					curnode = result
		ptr += tlen

	return result


_digits_and_bracket_re = re.compile( r'(\D)(([2-9]|\d{2})\))' )

def content( s ):
	'''
	content ( s ) -> list

	отформатировать bb-код в xhtml
	возвращает список из xml_node
	'''
	# &#91;     Left square bracket
	# &#93;     Right square bracket

	s = s.replace( r'\[', r'&#91;' ).replace( r'\]', r'&#93;' )		# обезопасить нарочно \[эскейпнутые\] квадратные скобки
	s = s.replace( r'<',  r'&#60;' ).replace( r'>',  r'&#62;' )		# убрать <треугольные скобки>
	s = re.sub( _digits_and_bracket_re, r'\1[br]\2', s )			# переносы строк перед пунктами списка

	return parse( s )


def header( s=None ):
	'''
	создать заголовок статьи
	'''
	x = xml_node( name='h1' )
	if s:
		x.add_child( *content( s ))
	return x


def paragraph( level=0 ):
	'''
	создать из m1 .. m9 параграф текста <p class="m1 .. m9">...</p>
	'''
	if 0 <= level <= 9:
		v = 'm%d' % level
		return xml_node( name='span', attr=( xml_attr( name='class', value=v ), ))
	else:
		raise Exception( 'paragraph: слишком большой уровень (%d)' % level )



def example():
	'''
	создать тег примера <span class="ex">...</span> с приоритетом "1"
	'''
	return xml_node(
		name = 'span',
		attr = (
			xml_attr( name='class', value='e' ),
			xml_attr( prefix='d', name='priority', value='2' )
		)
	)


def link( ln ):
	'''
	создать тег гиперссылки <a href="..."> (на самом деле <span class='ln')
	'''
	return xml_node( name='span', attr=( xml_attr( name='class', value='ln' ), ))


def italic():
	'''
	создать курсивный текст <i>...</i>
	'''
	return xml_node( name='i' )


def bold():
	'''
	создать полужирный текст <b>...</b>
	'''
	return xml_node( name='b' )

def span():
	'''
	создать чистый span
	'''
	return xml_node( name='span' )

def div():
	'''
	создать чистый div
	'''
	return xml_node( name='div' )

def br():
	'''
	создать перенос строки br
	'''
	return xml_node( name='br', single=True )

def mark():
	return xml_node( name='span', attr=( xml_attr( name='class', value='c' ), ))

if __name__ == '__main__':

	s4 = r'[m1]string [i]italic[/i][/m]'

	print '__main__: s4 = %s' % s4
	print 'длинна s4 = %d' % len( s4 )
	for x in parse( s4 ):
		print x
