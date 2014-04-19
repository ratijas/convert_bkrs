#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from dsl_dictionary_plugin import *

class dicPlugin( dslDictionaryPlugin ):
	def __init__(self):
		super( dicPlugin, self ).__init__()
		super( dicPlugin, self ).set_headers({'NAME': 'BKRS'})

	def dictionary_begin( self ):
		print r'<d:dictionary>'
		for k in self.headers:
			print k + ': ' + self.headers[k]

	def dictionary_end( self ):
		print r'</d:dictionary>'
