# -*- coding: UTF-8 -*-

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from u import u, utf
del sys.path[0], os, sys


class dslDictionaryPlugin( object ):
	"""
	абстрактный класс. определяет методы, которые нужно переопределить

	примечание: метод set_headers переопределять не стоит
	"""
	def __init__( self ):
		super( dslDictionaryPlugin, self ).__init__()
		self.headers = {}

	def set_headers( self, headers ):
		'''
		set_headers([ {title: str, value: str}, ...])
		'''
		# альтернативный вариант default value для изменяемых типов
		headers = headers if headers else []
		
		# переписать себе
		for h in headers:
			self.headers[ h[ 'title' ]] = u( h[ 'value' ])

	def dictionary_begin( self ):
		return ''

	def dictionary_end( self ):
		return ''
