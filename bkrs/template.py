#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
шаблонизатор файла параметров (plist), страницы настроек (html) и Makefile'а
'''

def run(
	plist_filename,
	makefile_filename,
	prefs_filename,
	xsl_filename,
	display_name,
	identifier,
	bundle_name,
	version
	):

	plist_template_file_name = 'bkrsInfo.plist'

	plist_template = open( plist_template_file_name, 'r' )
	plist_final = open( plist_filename, 'w' )

	_ = plist_template											\
		.read() 												\
		.replace( u'{{CFBundleDisplayName}}',	data.display_name )	\
		.replace( u'{{CFBundleIdentifier}}',	data.identifier )	\
		.replace( u'{{CFBundleShortVersionString}}',	data.version_string )

	plist_final.write( _ )
