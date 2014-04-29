#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dsl
from dsl import jing_test
from ratijas_dictionary_plugin import RatijasDictionaryPlugin
from bruks_entry_plugin import BruksEntryPlugin

INFILE = 'bruks_test.dsl'
OUTFILE = 'bruks_test2.xml' 

dsl.set_app_data({
	dsl.INFILE: INFILE,
	dsl.OUTFILE: OUTFILE,
	dsl.DICTIONARY_PLUGIN_CLASS: RatijasDictionaryPlugin,
	dsl.ENTRY_PLUGIN_CLASS: BruksEntryPlugin
})

dsl.convert()

jing_test.run( OUTFILE )
