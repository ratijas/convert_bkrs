#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, os, subprocess
import dict2xml
import re
import codecs
from rm_unicode import *

out_file = None
in_file  = None

lang_ru_ch	= 'ru_ch'
lang_ch_ru	= 'ch_ru'

def set_out_file( f ):
	global out_file
	out_file = f
def set_in_file( f ):
	global in_file
	in_file = f

def set_lang():
	_lang = [None]
	def set_lang( l ):
		if _lang[0] is not None:
			raise Exception( 'set_lang: язык уже установлен: %s' % lang )
		_lang[0] = l
	def lang():
		return _lang[0]
	return set_lang, lang
set_lang, lang = set_lang()

def print_begin():
	decl =	dict2xml.xml_declaration(
				dict2xml.xml_attr( '', 'version',  '1.0' ),
				dict2xml.xml_attr( '', 'encoding', 'UTF-8' )
			)
	print >>out_file, decl
	
	print >>out_file, dict2xml.dictionary_open()

def print_end():
	print >>out_file, '\n%s' % dict2xml.dictionary_close()


def print_entries():
	blank_line_re = re.compile( ur'^\s*$', re.UNICODE )

	def print_entries():

		front = dict2xml.xml_node( 'd', 'entry', attr=(
			dict2xml.xml_attr( '', 'id', 'front_back_matter' ),
			dict2xml.xml_attr( 'd', 'title', 'обложка словаря' )
		))

		front_back_matter_file = open( 'front_back_matter.html', 'r' )
		front.add_xml( front_back_matter_file.read() )
		front_back_matter_file.close()

		print >>out_file, front

		writen = 0

		for line in in_file:

			if re.match( blank_line_re, line ) or '#' in line:
				continue						# пустая строка или комментарий

			header = line					# первая строчка -- заголовок
			contents = []					# остальные строки статьи, которые начинаются с пробела

			for line in in_file:
				if not re.match( blank_line_re, line ):
					contents.append( line )
					# print >>sys.stderr, 'append %d lens: %s' % ( len( line ), line ),
				else:
					break

			if writen % 10 == 0:
				print >>sys.stderr, '#% 6d: %s' % ( writen, header ), # заголовок содержит перенос строки
			print_entry( header, contents )
			writen += 1

			# print >>sys.stderr, 'contents: %s' % contents
		print >>sys.stderr, 'обработано %d статей' % writen

	return print_entries
print_entries = print_entries()


def print_entry( title, contents ):
	title = title.strip()
	if len( contents ) is 0:
		contents[ 0 ] = ''

	try:
		entry = dict2xml.entry( title, contents[ 0 ])	
	except dict2xml.IDError, e:		# идентификатор уже зарегистрирован
		print '%s, title: %s' % ( e, title )
		return

	contents = map( str.strip, map( utf, contents ))
	
	if lang() is lang_ch_ru:
		neirong = [[ dict2xml.pin_yin( contents[ 0 ])]]
		if len( contents ) > 1:
			neirong.extend( map( dict2xml.content, contents[ 1: ]))
		contents = neirong
	else:
		contents = map( dict2xml.content, contents )

	for x in contents:
		entry.add_child( *x )

	try:
		print >>out_file, entry
	except:
		close_resorces()
		raise Exception( 'print_entry: ошибка при записи в файл' )


def test():
	jing_jar_path	= 'jing/bin/jing.jar'
	rng_path		= 'DictionarySchema/AppleDictionarySchema.rng'
	pipe = None

	print >>sys.stderr, 'running `jing` test...'
	pipe = subprocess.Popen(
		[ 'java', '-jar', jing_jar_path, rng_path, out_file.name ],
		stdout=subprocess.PIPE )
	retcode = pipe.wait()
	try:
		if retcode is not 0:
			if retcode < 0:
				print >>sys.stderr, '`jing` was terminated by signal', -retcode
			elif  retcode > 0:
				print >>sys.stderr, '`jing` test returned', retcode
			raise Exception( '`jing` execution failed' )

	except:
		print >>sys.stderr, '%s' % pipe.communicate()[ 0 ]
		raise
	else:
		print >>sys.stderr, '`jing` test passed'
