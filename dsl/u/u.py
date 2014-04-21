#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def u( s ):
	'''
	u( s ) -> unicode

	преобразование данных ``s'' в unicode
	'''
	if type( s ) is unicode:
		return s
	elif type( s ) is str:
		return s.decode( 'utf-8' )
	else:
		return u( str( s ))
