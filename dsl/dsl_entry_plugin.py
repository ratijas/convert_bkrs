#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from u import *
import re
from urllib import quote

class dslEntryPlugin( object ):
	"""
	абстрактный класс, определяет методы, которые нужно переопределить
	"""
	def __init__( self ):
		super( dslEntryPlugin, self ).__init__()
 		
	def preparse( self, t, s ):
		return t, s

	def postparse( self, t, s ):
		return u'%s%s' % ( t, s )


if __name__ == '__main__':
	pl = dslEntryPlugin()
