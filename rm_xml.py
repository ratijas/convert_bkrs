#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
модуль предоставляет функции и классы для создания простенького xml-документа, а также функции для проверки правильности идентификатора и замены таких символов, как <>"' на &-эквиваленты
'''

import re # для check_id()
from rm_unicode import *

def indent():
	ind = [True]

	def set_indent( b ):
		ind[0] = bool( b )

	def is_indent():
		return ind[0]

	return set_indent, is_indent
set_indent, is_indent = indent()
del indent


def escape_xml_specials():
	_amp_re = re.compile( ur'\&([^\#])', re.UNICODE )

	def escape_xml_specials( value ):
		'''
		escape_xml_specials( s ) -> str

		замена "опасных" символов строки на их xml-эквиваленты
		заменяются <, ?, >, кавычки (одинарные и двойные), переносы строк
		'''
		value = u( value )
		value = re.sub(	_amp_re, ur'&amp;\1', value ) \
			.replace( ur'<', ur'&#60;' )	\
			.replace( ur'>', ur'&#62;' )	\
			.replace( u"'",  ur'&#39;' )	\
			.replace( u'"',  ur'&#34;' )	\
			.replace( u'\n', ur'\n' )
		return utf( value )
	return escape_xml_specials
escape_xml_specials = escape_xml_specials()

def check_id():
	id_re = re.compile( u'[_A-Za-z][-_a-zA-Z0-9]*$', re.UNICODE )
	def check_id( s ):
		'''
		check_id( s ) -> bool

		проверка идентификатора
		только строки, состоящие только из латинских букв, цифр или подчёркиваний и дефисов
		'''
		return ( isinstance( s, str ) or isinstance( s, unicode )) and bool( re.match( id_re, s ))
	return check_id
check_id = check_id()


class xml_stuff( object ):
	'''
	абстрактный класс для xml.

	определяет методы для работы с префиксами и названиями тегов/ аттрибутов
	'''
	def __init__( self, prefix='', name='' ):
		prefix = u( prefix )
		name = u( name )

		super( xml_stuff, self ).__init__()

		if not check_id( name ):
			raise Exception( 'xml_stuff: плохое имя (%s)' % name )
		self.name = name

		if prefix is not u'':
			if not check_id( prefix ):
				raise Exception( 'xml_stuff: плохой префикс (%s)' % prefix )
			self.prefix = prefix
		else:
			self.prefix = None

	def __hash__( self ):
		'''
		hash( x ) -> int  <==>  hash( x.head())

		хэш только префикса и заголовока
		'''
		return hash( self.head())

	def head( self ):
		'''
		head() -> str

		префикс и имя xml- тега, аттрибута, разделённые двоеточием
		prefix:name
		'''
		s = None
		if self.prefix:
			s = u'%s:%s' % ( self.prefix, self.name )
		else:
			s = u'%s' % self.name 
		return s


class xml_attr( xml_stuff ):
	'''
	аттрибут xml-узла

	содержит обязательное имя, необязательные префикс и значение
	prefix:name='value'
	'''
	def __init__( self, prefix='', name='', value='' ):
		'''
		строка, передаваемая в параметре value проходит "очистку" функцией escape_xml_specials()
		'''
		prefix = u( prefix )
		name = u( name )
		value = u( value )

		super( xml_attr, self ).__init__( prefix, name )

		if value is not '':
			self.value = u( escape_xml_specials( value ))
		else:
			self.value = None

	def __str__( self ):
		'''
		формирует аттрибут в xml-виде

		полный вариант:
			prefix:name="value"
		простой вариант -- только имя
			name
		если значения нету, символ равно (=) не входит в результат
			prefix:name
		если нет префикса, имени не предшествует двоеточие
			name="value"
		'''
		s = u' '
		if self.prefix is not None:
			s += u'%s:' % self.prefix

		s += u'%s' % self.name

		if self.value is not None:
			s += u'="%s"' % self.value

		return utf( s )


class xml_node( xml_stuff ):
	'''
	xml-узел собственной персоной
	'''

	indent = 0
	'''
	содержит кол-во вложеных тегов; используется для форматирования тега как строки

	чтобы отключить отступы, установите
	``__module__.no_indent = True''
	'''

	def __init__( self, prefix='', name='', single=False, attr=()):
		'''
		* name -- обязательный параметр! остальные -- по усмотрению

		single -- явно укажи 'труъ', если тег не должен ничего содержать, т.е. самозакрывается <tag />
		attr   -- аттрибуты тега, созданные при помощи класса xml_attr. любое перечисляемое множество
		'''
		prefix = u( prefix )
		name = u( name )

		super( xml_node, self ).__init__( prefix, name )

		if not isinstance( single, bool ):
			raise Exception( 'xml_node: аргумент \'single\' должен быть типа \'bool\'' )
		self.single = single

		if self.single:
			self._child_list = None
		else:
			self._child_list = []

		self._attr_list = []
		for a in attr:
			self._add_attr( a )

	def __str__( self ):
		'''
		str( x ) <==> x.__str__()

		формирует строковое представление тега с красивенькими такими отступами
		'''
		s = u''						# результат
		h = self.head()				# имя тега, включая префикс
		i = u'\n%s' % ( u'\t' * self.__class__.indent )		# indent, величина отступа

		if is_indent():
			s = i

		self.__class__.indent += 1

		s += ur'<%s' % h			# открыть тег

		s += u''.join( map( u, self._attr_list ))		  # добавить аттрибуты

		if self.single:
			s += ur'/>'				# закрыть тег-одиночку
		else:
			s += ur'>'									  # закрыть открывающий тег
			if len( self._child_list ) is not 0:
				s += u''.join( map( u, self._child_list ))	  # добавить контент
				if is_indent():
					s += i 				# новая строка после потомков
			s += ur'</%s>' % h

		self.__class__.indent -= 1

		return utf( s )

	def __contains__( self, other ):
		if isinstance( other, xml_attr ):
			return other in self._attr_list
		elif isinstance( other, xml_node ):
			return other in self._child_list
		else:
			raise Exception( 'xml_node.__contains__: неподдерживаемый тип аргумента (%s)' % type( other ))

	def _add_child( self, node ):
		'''
		приватный метод для добавления одного потомка
		'''
		if self.single:
			raise Exception( 'add_child: попытка добавить потомка для единичного тега' )
		if isinstance( node, self.__class__ ):
			self._child_list.append( node )
		else:
			raise Exception( 'попытка добавить в дерево элемент, который не является подклассом \'xml_node\': %s', node.__repr__())

	def add_child( self, *node ):
		'''
		add_child( [node[, ... ]]) -> self

		публичный метод для добавления потомка(-ов)
		'''
		for x in node:
			self._add_child( x )
		return self

	def append( self, *node ):
		'''
		append( ... ) <==> add_child( ... )

		для совместимости с типом 'list'
		'''
		self.add_child( *node )

	def add_xml( self, s ):
		'''
		add_xml( s ) -> self

		добавить в тег непосредственно xml-код
		предпочтительнее использовать метод add_child()
		'''
		self._child_list.append( u( s ))

	def _add_attr( self, attr ):
		'''
		приватный метод для добавления аттрибутов тега
		'''
		if isinstance( attr, xml_attr ):
			for a in self._attr_list:			# возможно этого аттрибут уже существует
				if hash( a ) == hash( attr ):
					self._attr_list.remove( a )	# заменить новым значением
					break
			self._attr_list.append( attr )
		else:
			raise Exception( '_add_attr: попытка добавить в тег аттрибут, который не является подклассом \'xml_attr\': %s', attr.__repr__())

	def add_attr( self, *attr ):
		'''
		add_attr( [attr1[, ... ]]) -> self

		добавить аттрибут(-ы) к тегу
		каждый аттрибут должен быть экземпляром класса xml_attr
		если аттрибут с таким же префиксом и именем уже существует, он значение заменяется на новое
		'''
		for a in attr:
			self._add_attr( a )
		return self


class xml_declaration( xml_node ):
	'''
	создание декларации xml-документа в виде <?xml ... ?>
	'''
	def __init__(self, *attr ):
		'''
		передаваемые значения -- аттрибуты в обёртке 'xml_attr'
		'''
		super( xml_declaration, self )	\
			.__init__( prefix='', name=u'xml', single=True, attr=attr )

	def __str__( self ):
		return utf( u'<?xml%s?>' % u''.join( map( u, self._attr_list )))		  # добавить аттрибуты
		

class xml_text( xml_node ):
	'''
	контейнер для текста в xml-теге

	специальные символы автоматически заменяются
	'''
	def __init__( self, text ):
		self.text = u( escape_xml_specials( utf( text )))

	def __str__( self ):
		'''
		учитывается текущий уровень отступов для форматирования
		'''
		if is_indent():
			return utf( u'\n%s%s' % (( u'\t' * self.__class__.indent ), self.text )) 	# indent унаследован от родительского класса
		else:
			return utf( u'%s' % self.text )

	def __eq__( self, other ):
		if isinstance( other, self.__class__ ):
			return self.text == other.text
		else:
			return self.text == u( other )
		

def main():
	# set_indent( True )
	# обширный тест xml_node
	print
	print 'тестирование xml_node'

	print '\nсоздание узла d:entry'
	de = xml_node( prefix='d', name='entry' )
	print 'результат:', de

	print '\nсоздание аттрибута id="make_1"'
	m1 = xml_attr( name='id', value='make_1' )
	print 'результат:', m1

	print '\nдобавление аттрибута тегу'
	de.add_attr( m1 )
	print 'результат:', de


	print '\nсоздание индекса сразу с аттрибутами'
	xa1 = xml_attr( prefix='d', name='value', value='делаю' )
	xa2 = xml_attr( 'd', 'title', 'делать' )
	
	x1 = xml_node( 'd', 'index', single=True, attr=( xa1, xa2 ))
	print 'результат:', x1

	print '\nдобавление индекса в entry'
	de.add_child( x1 )
	print 'результат:', de

	print '\nдобавление текста'
	h1 = xml_node( name='h1' )
	h1.add_child( xml_text( 'ничегонеделание' ))
	de.add_child( h1 )
	print 'результат:', de

	print '\nxml-декларация'
	dec = xml_declaration( xml_attr( name='version', value='1.0' ), xml_attr( name='encoding', value='UTF-8' ))
	print 'результат:', dec

	print '\n__contains__'
	print 'xa1 in x1 (должно быть True):', xa1 in x1
	print 'm1 in x1 (должно быть False):', m1 in x1
	try:
		print '<string> in x1 (должно вызвать ошибку):', u'string' in x1
	except Exception, e:
		print 'произошла обишка: %s' % e

	print 'h1 in entry (должно быть True):', h1 in de
	print 'x1 in h1 (должно быть False):', x1 in h1

if __name__ == '__main__':
	main()
