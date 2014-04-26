#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
from dsl import dslEntryPlugin
from dsl.u import *
from dsl import normalize

def get_id_for_header():
	cnt = [0]
	def get_id_for_header( header ):
		s = u'_%d' % cnt[0]
		cnt[0] += 1
		return s
	return get_id_for_header
get_id_for_header = get_id_for_header()

class AppleEntryPlugin( dslEntryPlugin ):

	def __init__( self ):
		super( AppleEntryPlugin, self ).__init__()
		self.title = u''


	def preparse():
		# замыкание, приватные статические переменные
		plain_replace_table = [
			( ur'[m2][*][ex]', ur'<div class="m2 e" d:priority="2">' ),
			( ur'[/ex][/*][/m]', ur'</div>' ),
			( ur'[*]', ur'<div d:priority="2">' ),
			( ur'[/*]', ur'</div>' )
		]

		reg_sub_table = [
			( ur'(\D)(([2-9]|\d{2})\))', ur'\1\n\2' )	# новая строка перед пунктами 1) 2) 3)
		]

		# скомпилировать регулярки перед запуском
		reg_sub_table = map( lambda (r, s): ( re.compile( r, re.UNICODE ), s ), reg_sub_table )

		def preparse( self, t, s ):
			# запомнить для postparse
			self.title = normalize.full( t )
			self.title_short = normalize.short( t )

			for ( old, new ) in plain_replace_table:
				s = s.replace( old, new )
			for ( reg, sub ) in reg_sub_table:
				s = reg.sub( sub, s )
			return t, s
		return preparse
	preparse = preparse()


	def postparse():
		# замыкание, приватные статические переменные
		href_re = re.compile( ur'href="(.+?)"', re.UNICODE )

		def postparse( self, t, s ):
			s = href_re.sub( ur'href="x-dictionary:d:\1"', s )
			return u'<d:entry id="{id}" d:title="{title}">{indx}{header}{content}</d:entry>'.format(
				id = get_id_for_header( t ),
				title = self.title,
				indx = u''.join(
					[
						self.index( value, title )
						for ( value, title ) in self.indexes()
					]
				),
				header = t,
				content = s
			)

		return postparse
	postparse = postparse()

	def indexes( self ):
		a = [( self.title, self.title )]
		if self.title is not self.title_short:
			a.append(( self.title_short, self.title ))
		return a

	def index( self, value, title ):
		return ur'<d:index d:value="%s" d:title="%s"/>' % ( value, title )
