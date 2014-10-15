#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math

class ProgressBar( object ):
	"""графическое представление продвижения прогресса"""
	def __init__( self, minval, maxval, width ):

		self.minval = minval
		self.maxval = maxval
		self.current = self.minval
		self.width = width


	def set_value( self, value ):
		self.current = int( value )


	def __str__( self ):
		maxval_as_str = str( self.maxval )
		minval_as_str = str( self.minval )

		# максимальная длина крайних значений в виде строк
		label_width_max = max( len( maxval_as_str ), len( minval_as_str ) )

		# ширина ползунка = ширина     -     ширина меток        - “ [”…“] ” - “>”
		active_width      = self.width - ( label_width_max * 2 ) -     4     -  1

		# label_current точно в диапазоне [ self.minval ; self.maxval ]
		label_current = float( self.current )
		label_current = min( label_current, self.maxval )
		label_current = max( self.minval, label_current )

		yes_width = int( math.floor(
			( label_current - self.minval ) / float( self.maxval - self.minval ) * active_width
			))
		no_width  = active_width - yes_width

		return u'%*d [%s>%s] %*d' % (
			label_width_max,
			label_current,
			#
			u'=' * yes_width,
			u' ' * no_width,
			#
			label_width_max,
			self.maxval
		)
