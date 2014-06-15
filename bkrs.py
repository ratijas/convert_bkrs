#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dsl
from dsl import jing_test
from ratijas_dictionary_plugin import RatijasDictionaryPlugin
from bkrs_entry_plugin import BkrsEntryPlugin
import dict_template

import sys, getopt

parts = []
if len( sys.argv ) > 1:
	for x in sys.argv[ 1: ]:
		i = int( x )
		if 1 <= i <= 3:
			parts.append( i )
else:
	parts = [1, 2, 3]

for part in parts:

	INFILE = 'bkrs/bkrs%d.dsl' % part
	OUTFILE = 'bkrs/bkrs%d.xml' % part

	dsl.set_app_data({
		dsl.INFILE: INFILE,
		dsl.OUTFILE: OUTFILE,
		dsl.DICTIONARY_PLUGIN_CLASS: RatijasDictionaryPlugin,
		dsl.ENTRY_PLUGIN_CLASS: BkrsEntryPlugin
	})

	dsl.convert()

	jing_test.run( OUTFILE )

	dict_template.run(
		xml_filename	= OUTFILE,
		plist_filename	= 'bkrs/bkrsInfo.plist',
		prefs_filename	= 'both/prefs.html',
		xsl_filename	= 'both/dict.xsl',
		css_filename	= 'bkrs/bkrs.css',
		images_dir		= 'both/OtherResources/Images',
		display_name	= '大БКРС ч.%d/3' % part,
		identifier		= 'com.ratijas.dictionary.bkrs%d' % part,
		bundle_name		= '大БКРС %d' % part,
		version_string	= 'v61-%d/3 (2014.03.03)' % part
		)
	pass
