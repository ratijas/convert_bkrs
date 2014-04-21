#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from dsl_entry_plugin import dslEntryPlugin
from u import *

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

		self.plugin = None
		if plugin and not isinstance( plugin, dslEntryPlugin ):
			raise TypeError( 'dslEntry: `plugin` должен быть подкласом dslEntryPlugin' )
		else:
			self.plugin = plugin

		# конец __init__()


	def read( self, f ):
		'''
		считывает статью из файла.

		предпологается, что статьи разделны хотя бы одной пустой строкой
		в случае неудачи (например, EOF) возвращает None
		'''
		self.title = u''
		# пропустить пустые строки
		while True:
			_ = u( f.readline())
			if _ is not u'\n':
				self.title = _
				break

		self.entry = u''
		# читать до пустой строки или EOF
		while True:
			line = u( f.readline())
			if line not in (u'\n', u''):
				self.entry += line
			else:
				break

		if len( self.entry.strip()) == 0:
			return None
		return self
		# конец read

	def parse( self ):
		t, e = self.title, self.entry

		t, e = self.plugin.preparse( t, e )
		t, e = self._parse( t, e )
		t, e = self.plugin.postparse( t, e )

		self.title, self.entry = t, e
		return self

	def _parse( self, title, entry ):
		title = title.strip()

		# entry = to_xhtml( title, entry )

			# full = normalize.brackets( title )
			# full = normalize.full( full )

			# h = xml_node( name='span', attr=( xml_attr( name='class', value='ch' ), ))
			# h.add_child( *content( full ) )

			# en.add_child( h )

			# return en

		return title, entry

	def __str__( self ):
		return self.title + u'\n' + self.entry
