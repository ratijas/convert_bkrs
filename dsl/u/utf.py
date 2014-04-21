#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def utf( s ):
	'''
	utf( s ) -> str

	преобразование данных ``s'' в utf-8
	'''
	if type( s ) is str:
		return s
	elif type( s ) is unicode:
		return s.encode( 'utf-8' )
	else:
		return str( s )
