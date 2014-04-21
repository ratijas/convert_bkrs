#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from u import u

def uread():
	files = dict()

	def uread( f ):
		'''
		uread( f ) -> unicode

		прочесть строку из файла, вернуть в виде unicode
		``f'' может быть именем файла. в таком случае
		файл открывается на чтение ('r') и возвращается назад
		'''
		if not isinstance( f, file ):
			pass
			# try:
				# f = files[ f ]
			# except:
				# f = open( f, 'r' )
				# files[ f.name ] = f
		else:
			pass
		return u( f.readline())
	return uread
uread = uread()
