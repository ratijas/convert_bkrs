#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, os, subprocess
import dict2xml
import re

out_file_name = 'bruks.xml'
in_file_name  = 'БРуКС.dsl'

lang_ru_ch	= 'ru_ch'
lang_ch_ru	= 'ch_ru'
lang		= lang_ru_ch
in_file		= None
out_file	= None

def open_resorces():
	global in_file
	global out_file
	in_file	= open( in_file_name, 'r' )
	out_file	= open( out_file_name, 'w' )

def close_resorces():
	in_file.close()
	out_file.close()

def print_begin():
	print >>out_file, dict2xml.xml_declaration(
		dict2xml.xml_attr( '', 'version', '1.0' ),
		dict2xml.xml_attr( '', 'encoding', 'UTF-8' )
		)
	print >>out_file, dict2xml.dictionary_open()

def print_end():
	print >>out_file, '\n', dict2xml.dictionary_close()


_blank_re = re.compile( r'^\s*$' )

def print_entries():

	front = dict2xml.xml_node( 'd', 'entry', attr=(
		dict2xml.xml_attr( '', 'id', 'front_back_matter' ),
		dict2xml.xml_attr( 'd', 'title', 'обложка словаря' )
	))

	front.add_xml( r'''
	<d:index d:value="ratijas &amp; mac-j studio" d:title="ratijas &amp; mac-j studio"/>
	
	<h1 style="text-align: center;"><b>обложка 大БКРС / БРуКС</b></h1>

	<div style="float: right"><img src="Images/icon.png" alt="иконка словаря"/></div>
	<h2>大БКРС - открытый редактируемый большой китайско-русско-китайский словарь</h2>

	<h3>сайт словаря: <a href="http://bkrs.info">bkrs.info</a></h3>
	<p>на сайте есть много разных "плюшек", которые трудно и/или невозможно воспроизвести в приложении dictionary. например: пословный перевод предложений, теги, цветной пиньинь, саттелиты и т.д.</p>

	<h3>цель 大БКРС:</h3>
	<p>создание идеального словаря для практической работы с современным китайским языком</p>

	<h3>основные принциы словаря:</h3>
	<ul>
		<li>полнота - словарь включает в себя не только слова, но и устойчивые сочетания</li>
		<li>современность - словарь не включает в себя древнекитайский язык</li>
	</ul>

	<h3>о версии словаря для mac os x</h3>
	<img width="100%" src="Images/letters.jpg" alt="ratijas &amp; mac-j studio"/>
	<span class="img_note">логотип ratijas &amp; mac-j studio</span>

	<p>данный релиз брукс для dictionary.app — стандартного приложения mac os — скорее всего был подготовлен энтузиастом-одиночкой, известным в интернетах под ником <a href="http://bkrs.info/user.php?name=ratijas">ratijas</a>. хотя тоже ещё не факт, так как пакет мог быть собран кем угодно, используя открытые исходники на <a href="http://bkrs.info/taolun/thread-153-post-26605.html#pid26605">странице форума</a>. так как словарь каждый день чуть-чуть меняется, добавляются новые слова, редактируются уже имеющиеся, то примерно раз в месяц в <a href="http://bkrs.info/taolun/thread-153-post-26605.html#pid26605">ветку</a> форума будет выкладыватся обновление</p>
	<p>словарь на mac os x выходит под <a href="http://ru.wikipedia.org/wiki/Копилефт">копилефтом <span class="copyleft">©</span> </a>, а это означает, что разработчик забыл-запил-забил на авторские права. :)<br />
	учите китайский и не тратьте время на чепуху!</p>
''' )

	out_file.write( str( front ))


	count = 0

	for line in in_file:
		if re.match( _blank_re, line ) or line[0] is '#':
			continue
		try:
			header = line					# первая строчка -- заголовок
			if lang is lang_ch_ru:
				pinyin = in_file.next()		# чтение в китайско-русском

			content = in_file.next()		# вторая, или третья, в зависимости от направления

			count += 1
			if count % 1000 == 0:
				print '#% 6d: %s' % ( count, header )

			if lang is lang_ru_ch:
				print_entry( header, content )
			else:
				print_entry( header, content, pinyin )
		except StopIteration, e:
			break


def print_entry( title, content, reading='' ):
	title = title.strip()

	try:
		entry = dict2xml.entry( title )
	except Exception, e:		# идентификатор уже зарегистрирован
		print e
		return

	reading = reading.strip()
	content = content.strip()

	entry.add_child( *dict2xml.content( content ))

	try:
		out_file.write( str( entry ))
	except:
		close_resorces()
		raise Exception( 'print_entry: ошибка при записи в файл' )


# программа
def main():
	open_resorces()
	print_begin()
	print_entries()
	print_end()
	close_resorces()

def test():
	jing_jar_path	= 'jing/bin/jing.jar'
	# rng_path		= 'Dictionary Development Kit/documents/DictionarySchema/AppleDictionarySchema.rng'
	rng_path		= 'DictionarySchema/AppleDictionarySchema.rng'

	try:
		pipe = subprocess.Popen(
			[ 'java', '-jar', jing_jar_path, rng_path, out_file_name ],
			stdout=subprocess.PIPE )
		retcode = pipe.wait()

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

def make():
	if 0 != os.system( 'make' ):
		raise Exception( '`make` failed' )

def install():
	if 0 != os.system( 'make install' ):
		raise Exception( '`make install` failed' )
	

if __name__ == '__main__':
	if len( sys.argv ) > 1 and ( sys.argv[ 1 ] == 'test' ):
		test()
		exit()
	main()
	test()
	make()

	# не всем это нужно сразу устанавливать
	if len( sys.argv ) > 1 and ( sys.argv[ 1 ] == 'install' ):
		install()