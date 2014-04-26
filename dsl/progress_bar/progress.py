#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math

class ProgressBar( object ):
	"""графическое представление продвижения прогресса"""
	def __init__(self, minval, maxval, width ):
		
		self.minval = minval
		self.maxval = maxval
		self.current = self.minval
		self.width = width
		

	def set_value( self, value ):
		self.current = int( value )


	def __str__( self ):
		maxval_as_str = str( self.maxval )
		minval_as_str = str( self.minval )

		maxvallen = len( maxval_as_str )
		minvallen = len( minval_as_str )

		maxwidth = max( maxvallen , minvallen )

		# ширина ползунка = ширина - ширина меток  - “ [” ... “] ” - “>” - 1 ( на всякий случай )
		active_width = self.width - maxwidth * 2 - 4 - 1 - 1

		current = self.current
		if current > self.maxval:
			current = self.maxval
		elif current < self.minval:
			current = self.minval

		yes_width = int( math.floor( float( current ) / float( self.maxval - self.minval ) * active_width ))
		no_width  = active_width - yes_width
		# print 'all = %d\nactive = %d\nyes = %d\nno = %d' % ( self.width, active_width, yes_width, no_width )
		return u'%*d [%s>%s] %*d' % (
			maxwidth,
			current,
			u'=' * yes_width,
			u' ' * no_width,
			maxwidth,
			self.maxval
		)
