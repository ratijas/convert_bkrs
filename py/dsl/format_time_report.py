#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pymorphy2

m = pymorphy2.MorphAnalyzer()

def format_time_report( begin, loaded, end, cnt ):
	'''
	напечатать отчёт о занятом времени, количестве статей и средней скорости

	begin - дата начала
	loaded - дата окончания загрузки и инициализации
	end - дата окончания конвертации
	cnt - общее кол-во сконвертированных статей
	'''

	print u'выполнение программы заняло в целом {total} с.\n'	\
		  u'из них на инициализацию ушло {init} с.'.format(
		  	total = ( end - begin ),
		  	init = ( loaded - begin )
		  	)

	if cnt > 0:
		word = u'статья'
		agree = ( m.parse( m.parse( word )[ 0 ].normal_form )[ 0 ] ).make_agree_with_number( cnt ).word
		
		print u'{cnt} {entry_agree_form} были обработаны за {convert} с.\n'		\
			  u'в среднем на каждую статью было потрачено: {avg} с.'.format(
				cnt = cnt,
				entry_agree_form = agree,
				convert = ( end - loaded ),
				avg = (( end - loaded ) / cnt )
			)
	else:
		print u'не удалось подсчитать кол-во статей, но есть информация, что\n'	\
			  u'их обработка заняла {convert} с.'.format( convert = ( end  - loaded ))
