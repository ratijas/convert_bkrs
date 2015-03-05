#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import dsl
from dsl import jing_test
from ratijas_dictionary_plugin import RatijasDictionaryPlugin
from bkrs_entry_plugin import BkrsEntryPlugin
import dict_template


INFILE = 'bkrs/bkrs.dsl'
OUTFILE = 'bkrs/bkrs.xml'
VERSION = open('downloads/version.txt').read().strip()

## только выбранные части, или все
#parts = []
#if len( sys.argv ) > 1:
#	if sys.argv[ 1 ] == '-0':
#		parts = ['']
#	else:
#		for x in sys.argv[ 1: ]:
#			if i in ['1', '2', '3']:
#				parts.append( i )
#else:
#	parts = ['1', '2', '3']
'''
части были раньше.  теперь мы умеем делать одним куском
'''

#for part in parts:

if not ( len( sys.argv ) > 1 and sys.argv[ 1 ] == '-t' ):

	dsl.set_app_data({
		dsl.INFILE: INFILE,
		dsl.OUTFILE: OUTFILE,
		dsl.DICTIONARY_PLUGIN_CLASS: RatijasDictionaryPlugin,
		dsl.ENTRY_PLUGIN_CLASS: BkrsEntryPlugin
	})

	dsl.convert()

	jing_test.run( OUTFILE )

	pass

dict_template.run(
	xml_filename	= OUTFILE,
	plist_filename	= 'bkrs/bkrsInfo.plist',
	prefs_filename	= 'both/prefs.html',
	xsl_filename	= 'both/dict.xsl',
	css_filename	= 'bkrs/bkrs.css',
	images_dir		= 'both/OtherResources/Images',
	display_name	= '大БКРС', # % ( ' ч.%s/3' % part if part else '' ),
	identifier		= 'com.ratijas.dictionary.bkrs', # % part,
	bundle_name		= '大БКРС', # % ( ' %s' % part if part else '' ),
	version_string	= VERSION # 'v63 (2014.09.30)' # % ( '-%s/3' % part if part else '' )
	)

