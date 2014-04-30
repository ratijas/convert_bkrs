#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
шаблонизатор файла параметров (plist), страницы настроек (html) и Makefile'а
'''

import os
import shutil

OtherResources = 'OtherResources'

def clean_folder( folder_path ):
	try:
		shutil.rmtree( folder_path )
	except OSError, e:
		pass
	os.makedirs(
		folder_path + '/' + OtherResources
	)


def read_from( filename ):
	_ = open( filename, 'r' )
	s = _.read()
	_.close()
	return s


def write_to( filename, data ):
	f = open( filename, 'w' )
	f.write( data )
	f.close()


def templatize( template, params ):
	'''
	templatize( template, params ) -> str

	params -- словарь из пар "шаблон": "подстановка"
	двойные скобки в шаблоне указывать не нужно
	'''
	for k, v in params.iteritems():
		template = template.replace( '{{' + k + '}}', v )
	return template


def run(
	display_name,
	identifier,
	bundle_name,
	version_string,
	xml_filename	= None,
	plist_filename	= None,
	prefs_filename	= None,
	xsl_filename	= None,
	css_filename	= None,
	images_dir		= None
	):
	
	# папка, куда запишем файлы словаря
	clean_folder( bundle_name )

	# файлы из шаблона
	plist_filename	= plist_filename or 'dict.plist'
	prefs_filename	= prefs_filename or 'dict.html'
	xsl_filename	= xsl_filename or	'dict.xsl'
	css_filename	= css_filename or	'dict.css'

	# параметры замены
	replaces = {
		'BundleDisplayName':	display_name,
		'BundleIdentifier':	identifier,
		'DevelopmentRegion':	'Ukraine',
		'BundleName':			bundle_name,
		'BundleShortVersionString':	version_string,
		'prefs_filename':		prefs_filename,
		'xsl_filenamexsl_filename':			xsl_filename,
		'Dictionary Development Kit':	'../Dictionary Development Kit'
	}

	# xml
	if xml_filename and os.path.isfile( xml_filename ):
		shutil.move( xml_filename, '%s/%s' % ( bundle_name, 'dict.xml' ))

	# установки
	plist = read_from( plist_filename )
	write_to(
		'%s/%s' % ( bundle_name, 'dict.plist' ),
		templatize( plist, replaces )
		)

	# страница настроек
	prefs = read_from( '%s/%s' % ( OtherResources, prefs_filename ))
	write_to(
		'%s/%s/%s' % ( bundle_name, OtherResources, 'dict.html' ),
		templatize( prefs, replaces )
	)

	# xsl
	xsl = read_from( '%s/%s' % ( OtherResources, xsl_filename ))
	write_to(
		'%s/%s/%s' % ( bundle_name, OtherResources, 'dict.xsl' ),
		templatize( xsl, replaces )
		)

	# css
	shutil.copy(
		css_filename,
		'%s/%s' % ( bundle_name, 'dict.css' )
	)

	if images_dir and os.path.isdir( images_dir ):
		images_outdir = '%s/%s/Images' % ( bundle_name, OtherResources )
		try:
			shutil.rmtree( images_outdir )
		except OSError:
			pass
		shutil.copytree( images_dir, images_outdir )

	# makefile
	Makefile = 'Makefile'
	make = read_from( Makefile )
	write_to(
		'%s/%s' % ( bundle_name, Makefile ),
		templatize( make, replaces )
	)


def main():
	run(
		# plist_filename	= 'test.plist',
		xml_filename	= '../bkrs1.xml',
		plist_filename	= None,
		prefs_filename	= None,
		xsl_filename	= None,
		css_filename	= None,
		images_dir		= '/Volumes/DataHD/users/ivan/Documents/convert_bkrs/both/OtherResources/Images',
		display_name	= 'testing dict',
		identifier		= 'com.ratijas.dict.test',
		bundle_name		= 'test bundle name',
		version_string	= '1.0.4'
		)


if __name__ == '__main__':
	main()
