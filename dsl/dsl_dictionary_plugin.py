#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class dslDictionaryPlugin( object ):
	"""
	абстрактный класс. определяет методы, которые нужно переопределить

	примечание: метод set_headers переопределять не нужно
	"""
	def __init__( self ):
		super( dslDictionaryPlugin, self ).__init__()
		self.headers = {}

	def set_headers( self, headers ):
		# альтернативный вариант default value для изменяемых типов
		headers = headers if headers else {}
		
		# переписать
		for key in headers:
			self.headers[key] = headers[ key ]

	def dictionary_begin( self ):
		return ''

	def dictionary_end( self ):
		return ''
