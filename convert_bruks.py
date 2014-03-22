#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, os
from convert import *

out_file_name = u'bruks.xml'
in_file_name  = u'БРуКС.dsl'

in_file		= None
out_file	= None

set_lang( lang_ru_ch )

def open_resorces():
	global in_file
	global out_file
	in_file	= open( in_file_name, 'r' )
	set_in_file( in_file )
	out_file = open( out_file_name, 'w' )
	set_out_file( out_file )

def close_resorces():
	in_file.close()
	out_file.close()

# программа
def main():
	open_resorces()
	dict2xml.set_indent( False )
	print_begin()
	print_entries()
	print_end()
	close_resorces()

def make():
	if 0 != os.system( 'make bruks' ):
		raise Exception( '`make` failed' )

def install():
	if 0 != os.system( 'make install-bruks' ):
		raise Exception( '`make install` failed' )
	

if __name__ == u'__main__':
	'''
	python __name__ [ -t | -i ] [ dict_file ]
	'''
	install_flag = False
	
	if len( sys.argv ) > 1 and ( sys.argv[ 1 ] == '-t' ):
		test()
		exit()

	# не всем это нужно сразу устанавливать
	if len( sys.argv ) > 1:
		if sys.argv[ 1 ] == u'-i':
			install_flag = True
		else:
			in_file_name = sys.argv[ 1 ]

	main()
	test()
	make()

	if install_flag:
		install()
