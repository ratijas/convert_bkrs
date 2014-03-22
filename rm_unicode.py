#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
простая работа с unicode
'''

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
		s = s.__str__()
		return u( s )

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
		return utf( s.__str__() )

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
			try:
				f = files[ f ]
			except:
				f = open( f, 'r' )
				files[ f.name ] = f
		else:
			pass
		return u( f.readline())
	return uread
uread = uread()

def uwrite( f, s ):
	raise Exception( 'попытка вызвать uwrite' )
	'''
	uwrite( f, s ) -> file

	вывод данных в файл в кодировке utf-8
	f может быть объектом типа file, или именем файла.
	в последнем случае файл открывается на запись ('w')
	данные в строке ``s'', если необходимо, преобразовываются
	в utf-8 строку
	'''
	if type( f ) in ( str, unicode ):
		f = open( f, 'w' )

	print >>f, utf( s )
	return f
