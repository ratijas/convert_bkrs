#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dsl
from dsl.u import *

class AppleDictionaryPlugin( dsl.dslDictionaryPlugin ):

	def dictionary_begin( self ):
		return ur'''<?xml version="1.0" encoding="UTF-8"?>

<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">
''' + u( self.front_back_matter())

	def dictionary_end( self ):
		return ur'''
</d:dictionary>
'''

	def front_back_matter( self ):
		return u''