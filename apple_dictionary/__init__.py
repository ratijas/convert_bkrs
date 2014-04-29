#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

dirpath = os.path.dirname(__file__) + '/'

class AppleDictionary( object ):
	"""
	AppleDictionary -- создание шаблона словаря для dictionary.app, стандартного приложения mac os x

	класс должен быть унаследован, переменные переустановлены
	"""
	def __init__(
		self,
		xml			=	dirpath + 'template/dict.xml',
		makefile	=	dirpath + 'template/Makefile',
		plist		=	dirpath + 'template/dict.plist',
		css			=	dirpath + 'template/dict.css',
		xsl			=	dirpath + 'OtherResources/dict.xsl',
		prefs		=	dirpath + 'OtherResources/dict.html',
		other		=	dirpath + 'OtherResources/'
		out 		=	'./objects/'
		):
		super( AppleDictionary, self ).__init__()
		self.xml 				= open( xml )
		self.makefile 			= open( makefile )
		self.plist 				= open( plist )
		self.css 				= open( css )
		self.xsl 				= open( xsl )
		self.prefs 				= open( prefs )
		self.other 				= other
		self.out				= os.mkdir( out )

		

if __name__ == '__main__':
	a = AppleDictionary()