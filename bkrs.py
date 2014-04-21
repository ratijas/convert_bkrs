#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dsl
from ratijas_dictionary_plugin import RatijasDictionaryPlugin
from apple_entry_plugin import AppleEntryPlugin

dsl.set_app_data({
	dsl.INFILE: 'bkrs.dsl',
	dsl.OUTFILE: 'bruks_text.xml',
	dsl.DICTIONARY_PLUGIN_CLASS: RatijasDictionaryPlugin,
	dsl.ENTRY_PLUGIN_CLASS: AppleEntryPlugin
})

dsl.convert()
