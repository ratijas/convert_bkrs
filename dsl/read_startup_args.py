#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import getopt, sys

def usage():
	print u'''
использование:
	{name} -a
	{name} -ctmi
'''.format( name = sys.argv[ 0 ] )

def read_startup_args():
	jieguo = {
		'help':		False,
		'convert':	False,
		'test':		False,
		'make':		False,
		'install':	False
		}


	try:
		opts, args = getopt.getopt( sys.argv[ 1: ], "hctmia" )
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	for o, a in opts:
		if o == '-a':
			jieguo[ 'help' ]	= False
			jieguo[ 'convert' ]	= True
			jieguo[ 'test' ]	= True
			jieguo[ 'make' ]	= True
			jieguo[ 'install' ]	= True
		elif o == '-h':
			usage()
			sys.exit()
		elif o == '-c':
			jieguo[ 'convert' ]	= True
		elif o == '-t':
			jieguo[ 'test' ] 	= True
		elif o == '-m':
			jieguo[ 'make' ]	= True
		elif o == '-i':
			jieguo[ 'install' ]	= True
		else:
			assert False, "unhandled option"
			
	return jieguo