#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from dsl_entry_plugin import *
from u import *

class dslEntry( object ):
	"""
	dslEntry( plugin )

	класс для считывания ( read() ), преобразования ( parse() )
	и записи ( str() ) словарной статьи.
	пригоден для многоразового использования
	"""
	def __init__( self, plugin=None ):
		super( dslEntry, self ).__init__()

		self.entry = ''

	def __setattr__( self, name, value ):
		if name is 'plugin':
			plugin = value
			if plugin and not isinstance( plugin, dslEntryPlugin ):
				raise TypeError( 'dslEntry: `plugin` должен быть подкласом dslEntryPlugin' )
			else:
				self.plugin = plugin
		# конец __setattr__


	def read( self, f ):
		self.entry = u''
		result = []
		# пропустить пустые строки
		while True:
			_ = u( f.readline())
			if _ is not u'\n':
				self.entry = _
				break

		# читать до пустой строки
		while True:
			line = u( f.readline())
			if line in (u'\n', u''):
				break
			else:
				result.append( line )

		self.entry = '\n'.join( result )

		return self
		# конец read

	def parse( self ):
		self.entry = self.plugin.preparse( self.entry )
		self.entry = self._parse( self.entry )
		self.entry = self.plugin.postparse( self.entry )
		return self

	def _parse( self, entry ):
		return ''

	def __str__( self ):
		return self.entry
