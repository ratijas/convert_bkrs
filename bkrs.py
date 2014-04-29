#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dsl
from dsl import jing_test
from ratijas_dictionary_plugin import RatijasDictionaryPlugin
from bkrs_entry_plugin import BkrsEntryPlugin

INFILE = 'bkrs1.dsl'
OUTFILE = 'bkrs1.xml' 

dsl.set_app_data({
	dsl.INFILE: INFILE,
	dsl.OUTFILE: OUTFILE,
	dsl.DICTIONARY_PLUGIN_CLASS: RatijasDictionaryPlugin,
	dsl.ENTRY_PLUGIN_CLASS: BkrsEntryPlugin
})

dsl.convert()

jing_test.run( OUTFILE )
