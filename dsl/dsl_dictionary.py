#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from dsl_dictionary_plugin import *
import re
from u import *
from dsl_entry import dslEntry

class dslDictionary( object ):
	"""
	dslDictionary( plugin, infile, outfile, entry_instance ) -> object

	класс-обёртка для словаря. разбирает заголовки dsl файла, кстати.
	plugin -- экземпляр подкласса dslDictionaryPlugin
	infile -- файл или имя входного файла dsl
	outfile -- файл или имя выходного файла (формат зависит от плагина)
	entry_instance -- экземпляр класса dslEntry, желательно, заправленый плагином
	"""
	def __init__( self, plugin=None, infile=None, outfile=None, entry_instance=None ):
		super( dslDictionary, self ).__init__()

		# плагин либо dslDictionaryPlugin, либо ничего
		if plugin and not isinstance( plugin, dslDictionaryPlugin ):
			raise TypeError( 'dslDictionary: `plugin` должен быть подкласом dslDictionaryPlugin' )
		else:
			self.plugin = plugin

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

		# аналогично, можно передать имя файла
		if not isinstance( outfile, file ):
			if isinstance( outfile, basestring ):
				try:
					self.outfile = open( outfile, 'w' )
				except Exception, e:
					raise Exception( 'dslDictionary: не удалось открыть файл %s' % outfile )
		else:
			self.outfile = outfile

		if not isinstance( entry_instance, dslEntry ):
			raise Exception( 'dslDictionary: `entry_instance` должен быть экземпляром dslEntry' )
		else:
			self.entry = entry_instance

		# конец __init__()

	def read_headers( self ):
		headers = []
		print 'read_headers: begin'
		while True:
			self.last_read = u( self.infile.readline().strip())
			# print 'read_headers: прочел "%s"' % utf( self.last_read )

			if self.last_read.startswith( u'#' ):
				_ = re.match(
					# #INDEX_LANGUAGE "Russian"
					# #      \w+    \s " .+  "
					ur'#(\w+)\s+("?)(.+)\2',
					self.last_read,
					re.UNICODE
				)
				if _ is not None:
					# \1 -- имя, \3 -- значение
					_ = _.groups()
					headers.append({ 'title': _[0], 'value': _[2] })
				else:
					break
			else:
				break

		return headers
		# конец read_headers()


	def convert( self ):
		# метаданные словаря. строки, которые начинаются с решетки
		self.plugin.set_headers( self.read_headers())

		# плагин пишет какие-то данные в начале словаря. <d:dictionary ...>, например, обложку, ...
		_ = self.plugin.dictionary_begin()
		self.outfile.write( utf( _ ))

		# напечатать все статьи
		self._print_entries()

		# припечатать outro в конце. </d:dictionary>, например
		_ = self.plugin.dictionary_end()
		self.outfile.write( utf( _ ))

		# последняя новая строчка
		self.outfile.write( '\n' )

		# конец convert


	def _print_entries( self ):
		print 'printing entries...'
		# ...

		writen = 0
		while True:
			# следующий
			_ = self.entry.read( self.infile )

			# признак окончания файла?
			if _ is None:
				break

			# идём дальше
			self.entry.parse()

			# print u'-' * 20
			# print self.entry.__str__()

			# вывод в файл
			self.outfile.write( utf( self.entry.__str__()))

			writen += 1

		# ...
		print 'done'