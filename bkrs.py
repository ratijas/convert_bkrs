#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dsl
from ratijas_dictionary_plugin import RatijasDictionaryPlugin
from apple_entry_plugin import AppleEntryPlugin

########################
# for test
########################
from dsl import dslEntryPlugin

dsl.set_app_data({
	dsl.INFILE: 'bkrs_test.dsl',
	dsl.OUTFILE: 'bruks_test.xml',
	dsl.DICTIONARY_PLUGIN_CLASS: RatijasDictionaryPlugin,
	# dsl.ENTRY_PLUGIN_CLASS: AppleEntryPlugin
	dsl.ENTRY_PLUGIN_CLASS: dslEntryPlugin
})

dsl.convert()
