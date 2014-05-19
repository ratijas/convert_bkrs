#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dsl
from dsl import jing_test
from ratijas_dictionary_plugin import RatijasDictionaryPlugin
from bruks_entry_plugin import BruksEntryPlugin
from dict_template import template


INFILE = 'bruks/bruks.dsl'
OUTFILE = 'bruks/bruks.xml' 

dsl.set_app_data({
	dsl.INFILE: INFILE,
	dsl.OUTFILE: OUTFILE,
	dsl.DICTIONARY_PLUGIN_CLASS: RatijasDictionaryPlugin,
	dsl.ENTRY_PLUGIN_CLASS: BruksEntryPlugin
})

dsl.convert()

jing_test.run( OUTFILE )

template.run(
	xml_filename	= OUTFILE,
	plist_filename	= 'bruks/bruksInfo.plist',
	prefs_filename	= 'both/prefs.html',
	xsl_filename	= 'both/dict.xsl',
	css_filename	= 'bruks/bruks.css',
	images_dir		= 'both/OtherResources/Images',
	display_name	= 'БРуКС',
	identifier		= 'com.ratijas.dictionary.bruks',
	bundle_name		= 'БРуКС',
	version_string	= 'v61 (2014.03.03)'
	)
