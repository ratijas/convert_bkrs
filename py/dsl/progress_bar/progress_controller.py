#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, os, subprocess
import progress

class ProgressBarController( object ):
	"""управление полоской прогресса"""
	def __init__( self, min, max, width=0 ):
		if min >= max:
			raise ValueError( 'ProgressBarController: min должен быть меньше max' )

		# узнать ширину окна
		f = os.popen( "stty size" )
		rd = f.read().split()
		f.close()
		self.term_width = int( rd[ 1 ])
		self.term_height = int( rd[ 0 ])

		if width == 0 or width >= self.term_width:
			self.width = self.term_width - 1
		else:
			self.width = width
		self.progressBar = progress.ProgressBar( min, max, self.width )

	def redraw( self ):
		# поместить курсор вниз влево
		print chr( 0x1b ) + "[%dD" % self.term_width,
		# нарисовать
		print self.progressBar.__str__()
		# вернуть курсор
		print chr( 0x1b ) + "[1A",

	def set_value( self, value ):
		self.progressBar.set_value( value )
		self.redraw()
