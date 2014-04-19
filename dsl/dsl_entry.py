#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class dslEntryPlugin( object ):
	"""абстрактный класс, определяет методы, которые нужно переопределить"""
	def __init__( self ):
		super( dslEntryPlugin, self ).__init__()
 		
	def preparse( self, s ):
		return s

	def postparse( self, s ):
		return s

	def tag_map( self, tag ):
		return tag


class dslEntry( object ):
	"""
	класс для считывания, преобразования и записи словарной статьи
	"""
	def __init__( self, plugin=None ):
		super( dslEntry, self ).__init__()

		if plugin and not isinstance( plugin, dslEntryPlugin ):
			raise TypeError( 'dslEntry: `plugin` должен быть подкласом dslEntryPlugin' )
		else:
			self.plugin = plugin
		self.entry = ''

	def read( self, f ):
		self.entry = f.readline()
		return self

	def parse( self ):
		self.entry = self.plugin.preparse( self.entry )
		self.entry = self._parse( self.entry )
		self.entry = self.plugin.postparse( self.entry )
		return self

	def _parse( self, entry ):
		return ''

	def __str__( self ):
		return self.entry
