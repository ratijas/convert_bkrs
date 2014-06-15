#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from u import *

class dslEntryPlugin( object ):
	"""
	абстрактный класс, определяет методы, которые нужно переопределить:

	preparse( t, s ) -> ( t, s )
	postparse( t, s ) -> str
	"""
	def __init__( self ):
		super( dslEntryPlugin, self ).__init__()
 		
	def preparse( self, t, s ):
		return t, s

	def postparse( self, t, s ):
		return u'%s%s' % ( u( t ), u( s ) )
