#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from dsl_entry_plugin import dslEntryPlugin
from u import *
import normalize
from dsl_to_html import dsl_to_html

class dslEntry( object ):
	"""
	dslEntry( plugin )

	класс для считывания ( read() ), преобразования ( parse() )
	и записи ( str() ) словарной статьи.
	пригоден для многоразового использования

	ВНИМАНИЕ: метод __str__ возвращает unicode!
	"""
	def __init__( self, plugin=None ):
		super( dslEntry, self ).__init__()

		self.entry = u''
		self.title = u''
		self.content = u''

		self.plugin = None
		if plugin and not isinstance( plugin, dslEntryPlugin ):
			raise TypeError( 'dslEntry: `plugin` должен быть подкласом dslEntryPlugin' )
		else:
			self.plugin = plugin

		# конец __init__()


	def read( self, f ):
		'''
		считывает статью из файла.

		предполагается, что статьи разделны хотя бы одной пустой строкой
		в случае неудачи (например, EOF) возвращает None
		'''
		self.title = u''
		# пропустить пустые строки
		while True:
			_ = u( f.readline())
			if _ is not u'\n':
				self.title = _.strip()
				break

		# print u'dslEntry.read: прочитал "%s"' % self.title

		self.entry = u''
		# читать до пустой строки или EOF
		while True:
			line = u( f.readline())
			if line not in (u'\n', u''):
				self.entry += line
			else:
				break

		self.entry = self.entry.strip()
		if len( self.entry ) == 0:
			return None
		return self
		# конец read


	def parse( self ):
		# print u'пáршу статью с заголовком "%s"' % self.title
		t, e = self.title, self.entry

		# экранизировать угловые скобки
		e = e.replace( ur'<', ur'&lt;' ).replace( ur'>', ur'&gt;' )
		# полный вариант заголовка со скобками
		t = normalize.brackets( t )

		if self.plugin:
			t, e = self.plugin.preparse( t, e )

		t, e = self._parse( t, e )

		if self.plugin:
			content = self.plugin.postparse( t, e )
		else:
			content = ur'%s\n%s' % ( t, e )

		# убрать оставшуюся экранизацию с квадратных скобок
		content = content.replace( ur'\[', u'[' ).replace( ur'\]', u']' )

		self.content = content
		return self
		# конец parse


	def _parse( self, title, entry ):
		'''
		# Internal. делает основное превращение dsl в html 
		'''

		title = normalize.full( title )
		title = ur'<h1>%s</h1>' % title
		# print u'_parse: title = "%s"' % title

		entry = dsl_to_html( entry ).strip()

		return title, entry
		# конец _parse


	def __str__( self ):
		return self.content


if __name__ == '__main__':
	from io import StringIO
	e = dslEntry()
	s = u'''бывать{(ся)}
 [m1]бывает ([c][i]прим.[/c] часто встречаются[/i])[/m]'''
	e.read( StringIO( s ) )
	e.parse()

	print u'исходный:\n'+s+u'\nрезультат:\n'+e.__str__()