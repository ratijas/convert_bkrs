#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dsl
from ratijas_dictionary_plugin import RatijasDictionaryPlugin
from apple_entry_plugin import AppleEntryPlugin
from dsl import jing_test

INFILE = 'bruks_test.dsl'
OUTFILE = 'bruks_test.xml' 

dsl.set_app_data({
	dsl.INFILE: INFILE,
	dsl.OUTFILE: OUTFILE,
	dsl.DICTIONARY_PLUGIN_CLASS: RatijasDictionaryPlugin,
	dsl.ENTRY_PLUGIN_CLASS: AppleEntryPlugin
})

dsl.convert()

jing_test.run( OUTFILE )