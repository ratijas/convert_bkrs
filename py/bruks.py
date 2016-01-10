#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import dsl
from dsl import jing_test
from ratijas_dictionary_plugin import RatijasDictionaryPlugin
from bruks_entry_plugin import BruksEntryPlugin
import dict_template

INFILE = 'bruks/bruks.dsl'
OUTFILE = 'bruks/bruks.xml'
VERSION = open('downloads/version.txt').read().strip()

if not (len(sys.argv) > 1 and sys.argv[1] == '-t'):
    dsl.set_app_data({
        dsl.INFILE: INFILE,
        dsl.OUTFILE: OUTFILE,
        dsl.DICTIONARY_PLUGIN_CLASS: RatijasDictionaryPlugin,
        dsl.ENTRY_PLUGIN_CLASS: BruksEntryPlugin
    })

    dsl.convert()

    jing_test.run(OUTFILE)


dict_template.run(
    xml_filename=OUTFILE,
    plist_filename='bruks/bruksInfo.plist',
    prefs_filename='both/prefs.html',
    xsl_filename='both/dict.xsl',
    css_filename='bruks/bruks.css',
    images_dir='both/OtherResources/Images',
    display_name='БРуКС',
    identifier='com.ratijas.dictionary.bruks',
    bundle_name='БРуКС',
    version_string=VERSION  # 'v63 (2014.09.30)'
)
