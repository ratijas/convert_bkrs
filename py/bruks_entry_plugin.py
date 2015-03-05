#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from chinese_entry_plugin import ChineseEntryPlugin
from dsl import normalize
from dsl.u import u, utf
import color
import re

try:
	import pymorphy2
	morphy = pymorphy2.MorphAnalyzer()
except:
	import sys
	print '''
модуль 'pymorphy2' не установлен на этой машине.
ты можешь скачать его вот отсюда
http://pymorphy2.readthedocs.org/en/latest/
'''
	exit(1)


class BruksEntryPlugin( ChineseEntryPlugin ):
	"""и здесь тоже надо запилить доку"""
	def __init__( self ):
		super( BruksEntryPlugin, self ).__init__()
	

	def indexes( self ):
		'''
		список всех переборов с подстановками, комбинациями, склонениями,
		падежами и прочей красотой.
		при этом знаки препинания исключаются из всех вариантов, кроме
		одного -- полного исходного
		'''
		# type( a ) is set == True
		a = super( BruksEntryPlugin, self ).indexes()

		# фича: ставишь точку в конце -> словарь ищет точное совпадение
		a = set([ ( i[0]+u'.', i[1] ) for i in a ] + list( a ))
				
		# склоняем только карточки из одного слова
		if len( self.title.split()) == 1:

			normal_forms = morphy.parse( self.title )

			if len( normal_forms ) > 0:

				# формы одного слова
				normal_form = normal_forms[0]
				
				for x in normal_form.lexeme:
					a.add(( x.word, self.title ))

		return a
		# конец indexes
