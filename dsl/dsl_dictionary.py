#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from dsl_dictionary_plugin import *

class dslDictionary( object ):
	"""
	dslDictionary( plugin, infile, outfile ) -> object

	класс-обёртка для словаря. разбирает заголовки dsl файла, кстати.
	plugin -- экземпляр подкласса dslDictionaryPlugin
	infile -- файл или имя входного файла dsl
	outfile -- файл или имя выходного файла (формат зависит от плагина)
	"""
	def __init__( self, plugin=None, infile=None, outfile=None ):
		super( dslDictionary, self ).__init__()

		# плагин либо dslDictionaryPlugin, либо ничего
		if plugin and not isinstance( plugin, dslDictionaryPlugin ):
			raise TypeError( 'dslDictionary: `plugin` должен быть подкласом dslDictionaryPlugin' )
		else:
			self.plugin = plugin

		# заголовки будут позже
		# self.headers = {}
		# !закомментировано: заголовки переехали в плагин

		# файл для чтения. можно дать имя файла
		#   ваш к.о.
		if not isinstance( infile, file ):
			if isinstance( infile, basestring ):
				try:
					self.infile = open( infile, 'r' )
				except Exception, e:
					raise Exception( 'dslDictionary: не удалось открыть файл %s' % infile )
		else:
			self.infile = infile


		if not isinstance( outfile, file ):
			if isinstance( outfile, basestring ):
				try:
					self.outfile = open( outfile, 'w' )
				except Exception, e:
					raise Exception( 'dslDictionary: не удалось открыть файл %s' % outfile )
		else:
			self.outfile = outfile


	def read_headers( self, f ):
		headers = {}
		return headers

	def convert( self ):
		# метаданные словаря. строки, которые начинаются с решетки
		self.headers = self.read_headers( self.infile )

		# плагин пишет какие-то данные в начале словаря. <d:dictionary ...>, например
		self.plugin.dictionary_begin()

		# напечатать все статьи
		self._print_entries()

		# припечатать outro в конце. </d:dictionary>, например
		self.plugin.dictionary_end()

	def _print_entries( self ):
		print 'printing entries...'
		print 'done'