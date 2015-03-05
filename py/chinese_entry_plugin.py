#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from apple_entry_plugin import AppleEntryPlugin
import color

class ChineseEntryPlugin( AppleEntryPlugin ):
	"""
	возможно, когда-нибудь этот класс переопределит метод postparse для статической раскраски пиньиня. на данный момент это делается динамически
	"""
	def __init__( self ):
		super( ChineseEntryPlugin, self ).__init__()
 