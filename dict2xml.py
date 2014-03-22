#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
модуль-декоратор, направленный упрощение создания словаря с помощью модуля rm_xml

предоставленные здесь функции являются оболочкой для вызова ряда функций из rm_xml
'''

from rm_xml import *
import normalize
import index
import re
import sys		# sys.stderr

stack = []
'''стек вложеных тегов по мере разбора строка bb-кода'''

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

class IDError( ValueError ):
	def __init__(self, arg):
		super(IDError, self).__init__()
		self.arg = arg

	def __str__( self ):
		return self.arg
		

def make_id():
	ids = set()
	'идентификатор не должен регистрироваться дважды'

	def make_id( s, only_get=False ):
		'''
		создать идентификатор и проследить, чтобы он не повторялся
		'''
		id = '_%s_%d' % ( normalize.id( s ), len( ids ))

		if not check_id( id ):
			raise IDError( 'make_id: невозможно создать валидный id (%s)' % id )

		if not only_get:
			h = hash( id )
			if h in ids:
				raise IDError( 'make_id: уже было: "%s"' % id )
			ids.add( h )
		return id
	return make_id
make_id = make_id()

def entry( title, reading=None ):
	id = make_id( title )
	full = normalize.brackets( title )
	full = normalize.full( full )

	en = xml_node( 'd', 'entry', attr=(
		xml_attr( '', 'id', id ),
		xml_attr( 'd', 'title', full )
	))

	en.add_child( *gen_indexes( title, reading ))

	h = xml_node( name='span', attr=( xml_attr( name='class', value='ch' ), ))
	h.add_child( *content( full ) )

	en.add_child( h )

	return en

def _index( value, title=None ):
	'''
	создать индекс для конкретных title, value
	'''
	if title is None:
		title = value
	return xml_node( u'd', u'index', True, attr=(
		xml_attr( u'd', u'value', value ),
		xml_attr( u'd', u'title', title )
		)
	)

def gen_indexes( s, reading=None ):
	'''
	gen_indexes( title ) -> list

	создать индексы для всех возможных вариантов
	возвращает список из xml_node
	'''
	idx, full = index.indexes( s, reading )		# комбинации
	return [ _index( i, full ) for i in idx ]	# оформение в xml


def generate_el( name ):
	name = utf( name )
	if name[0] == 'm':
		if len( name ) == 2:
			depth = int( name[ 1 ])
			if not 0 <= depth <= 9:
				raise Exception( 'paragraph: слишком большой уровень (%d)' % level )
		else:
			depth = 0
		v = 'm%d' % depth
		return xml_node( name='span', attr=( xml_attr( name='class', value=v ), ))
	elif name == 'p':
		return xml_node( name='span', attr=( xml_attr( name='class', value='p' ), ))
	elif name == 'c':
		return xml_node( name='span', attr=( xml_attr( name='class', value='c' ), ))
	elif name == 'div':
		return xml_node( name='div' )
	elif name == 'i':
		return xml_node( name='i' )
	elif name == 'b':
		return xml_node( name='b' )
	elif name == '*':
		return xml_node( name='span' )
	elif name == 'ex':
		return xml_node(
			name = 'span',
			attr = (
				xml_attr( name='class', value='e' ),
				xml_attr( prefix='d', name='priority', value='2' )
			)
		)
	elif name == 'ref':
		return xml_node( name='span', attr=( xml_attr( name='class', value='ln' ), ))
	elif name == 'br':
		return xml_node( name='br', single=True )
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
	value <unicode> -- значение токена. для тегов скобки и обратные слеши убираются. 'm1', 'ref'
	length -- исходная длинна токена в символах. особенно актуально для тегов
	'''
	type = 0
	value = None
	length = 0

	s = u( s )

	if s[0] == '[':
		tag_end_ptr = s.find( u']' )		# конец имени тега, не скобки
		if tag_end_ptr == -1:
			raise Exception( 'gettoken: тег не закрыт (%s)' % s )

		length = tag_end_ptr + 1 		# преобразование указателя в длинну

		space_ptr = s.find( ' ', 2, tag_end_ptr )
		if space_ptr != -1:				# на случай всяких там [c black]
			tag_end_ptr = space_ptr

		if s[ 1 ] == u'/':
			type 	= token_type_tag_close
			value 	= s[ 2 : tag_end_ptr ]
		else:
			type 	= token_type_tag_open
			value 	= s[ 1 : tag_end_ptr ]
	else:
		type 	= token_type_string
		tag_begin_ptr = s.find( u'[' )
		if tag_begin_ptr == -1:
			value = s
		else:
			value = s[ : tag_begin_ptr ]
		length = len( value )

	return type, value, length


def parse( s ):
	'''
	parse( s ) -> list of xml_node

	парсер bb-кода. для разбора bb-кода передать только строку с кодом.
	возвращает list из xml_node
	'''
	s = u( s )

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
			if tval.startswith( u'm' ):
				tval = u'm'			# тег абзаца m1..m9 закрывается тегом [/m]
			el = generate_el( tval )
			curnode.append( el )
			
			if tval == u'ref':
				curnode.append( xml_node( name='br', single=True ))

			if not el.single:
				stack_bb.append( tval )
				stack_xml.append( el )
				curnode = el

		elif ttype == token_type_tag_close:
			while len( stack_bb ) > 0:
				last = stack_bb.pop()
				stack_xml.pop()
				if last is tval:
					break

			if len( stack_xml ) > 0:
				curnode = stack_xml[ -1 ]
			else:
				curnode = result
		ptr += tlen

	return result



def content():
	# приватная переменная
	digits_and_bracket_re = re.compile( ur'(\D)(([2-9]|\d{2})\))' )

	def content( s ):
		'''
		content ( s ) -> list of xml_node

		отформатировать bb-код в xhtml
		возвращает список из xml_node
		'''
		s = u( s )
		# &#91;     Left square bracket
		# &#93;     Right square bracket

		s = s.replace( r'\[', r'&#91;' ).replace( r'\]', r'&#93;' )		# обезопасить нарочно \[эскейпнутые\] квадратные скобки
		s = s.replace( r'<',  r'&#60;' ).replace( r'>',  r'&#62;' )		# убрать <треугольные скобки>
		s = re.sub( digits_and_bracket_re, r'\1[br]\2', s )			# переносы строк перед пунктами списка

		return parse( s )
	return content
content = content()


def pin_yin( s ):
	'''
	pin_yin( s ) -> xml_node 'span'

	обёртка для пиньиня
	'''
	s = content( u( s ))

	root = xml_node( name='span' )
	root.add_attr( xml_attr( name='class', value='py' ))
	root.add_child( *s )
	return root


def header( s=None ):
	'''
	создать заголовок статьи
	'''
	x = xml_node( name='h1' )
	if s:
		x.add_child( *content( s ))
	return x


def main():
	s4 = ur'''[b]I[/b][m1][c][i]союз[/i][/c][/m][m1]1) ([i]при сопоставлении[/i]) 可\[是\] kě\[shì\]; 却\[是\] què\[shì\] [i]([c]тк.[/i][/c] перед [c][i]сказ.[/c])[/i]; 而 ér, 但是 dànshì[/m][m2][*][ex]я просил его прийти, а он не согласился - 我请他来, 他可不要了[/ex][/*][/m][m2][*][ex]преподаватель объяснил ему несколько раз, а он так и не понял - 教员给他说了几次, 他却不明白[/ex][/*][/m][m1]2) [i]([c]в знач.[/c] но, однако[/i]) 可\[是\] kě\[shì\], 但\[是\] dàn\[shì\][/m][m2][*][ex]хотя здесь и очень хорошо, а придётся уходить - 虽然这里很好, 但是非去不可[/ex][/*][/m][m1]3) ([i]при противопоставлении[/i]) 而\[是\] ěr\[shì\][/m][m2][*][ex]он не специалист, а просто дилетант - 他不是专家, 而是一个外行[/ex][/*][/m][m1]4) ([i]служит для усиления[/i]) 可 kě, 倒 dào[/m][m2][*][ex]а я и не знал! - 我可不知道啊![/ex][/*][/m][m2][*][ex]а он так и не согласился - 他倒是不同意了[/ex][/*][/m][b]II[/b][m1][c][i]частица[/i][/c][/m][m1]1) ([i]при обращении[/i]) 啊 ā, 呀 yā[/m][m2][*][ex]мам, а мам! - 妈妈, 妈妈呀![/ex][/*][/m][m1]2) [c][i]вопр.[/i][/c] 呢 ne[/m][m2][*][ex]что ты сегодня делаешь? а завтра? - 你今天作什么? 明天呢?[/ex][/*][/m][b]III[/b][m1][c][i]межд.[/i][/c] 啊 ā, 哎呀 āi-yā[/m]'''

	print u'__main__: s4 = %s' % s4
	print u'длинна s4 = %d' % len( s4 )

	set_indent( False )
	for x in content( s4 ):
		print u'%s' % u ( x ),
	print

	print u'pin_yin: %s' % u( str( pin_yin( 'shāndōng' )))
	
if __name__ == u'__main__':
	main()