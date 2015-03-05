#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from dsl_dictionary        import dslDictionary
from dsl_dictionary_plugin import dslDictionaryPlugin
from dsl_entry        import dslEntry
from dsl_entry_plugin import dslEntryPlugin

import time
from format_time_report import format_time_report


#########################
DEBUG_MODE = False		#
#########################

INFILE = 'infile'
OUTFILE = 'outfile'
DICTIONARY_PLUGIN_CLASS = 'dictionary_plugin_class'
ENTRY_PLUGIN_CLASS = 'entry_plugin_class'

# глобальные переменные -- зло
# нужно вынести в замыкние
app_data = {}

def set_app_data( data ):
	'''
	set_app_data({ data1: val1, ...})

	требуемые параметры:
		INFILE
		OUTFILE
		DICTIONARY_PLUGIN_CLASS
		ENTRY_PLUGIN_CLASS
	'''
	global app_data
	app_data[ INFILE ] = data[ INFILE ]
	app_data[ OUTFILE ] = data[ OUTFILE ]
	app_data[ DICTIONARY_PLUGIN_CLASS ] = data[ DICTIONARY_PLUGIN_CLASS ]
	app_data[ ENTRY_PLUGIN_CLASS ] = data[ ENTRY_PLUGIN_CLASS ]


def convert():
	time_begin = time.time()
	time_init  = None
	time_end   = None

	e = dslEntry(
		plugin = app_data[ ENTRY_PLUGIN_CLASS ]()
	)

	d = dslDictionary(
		plugin = app_data[ DICTIONARY_PLUGIN_CLASS ](),
		infile = app_data[ INFILE ],
		outfile = app_data[ OUTFILE ],
		entry_instance = e
	)

	time_init = time.time()

	cnt = d.convert()

	time_end = time.time()
	format_time_report( time_begin, time_init, time_end, cnt )
