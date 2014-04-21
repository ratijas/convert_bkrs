#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from apple_dictionary_plugin import AppleDictionaryPlugin


class RatijasDictionaryPlugin( AppleDictionaryPlugin ):
	"""
	этот класс используется одновременно в русско-китайском и китайско-русском направлениях.
	надо было как-то его назвать, и я выбрал нейтральное RatijasDictionaryPlugin
	"""

	def __init__( self ):
		super( RatijasDictionaryPlugin, self ).__init__()

		f = open( 'front_back_matter.html', 'r' )
		self.matter = f.read()
		f.close()

		# конец __init__()

	def front_back_matter( self ):
		return self.matter