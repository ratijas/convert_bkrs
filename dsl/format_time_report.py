#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pymorphy2

m = pymorphy2.MorphAnalyzer()

def format_time_report( begin, loaded, end, cnt ):
	word = u'статья'
	agree = ( m.parse( m.parse( word )[ 0 ].normal_form )[ 0 ] ).make_agree_with_number( cnt ).word

	print u'''выполнение программы заняло в целом {total} с.
из них на инициализацию ушло {init} с.
{cnt} {entry_agree_form} были обработаны за {convert} с.
в среднем на каждую статью было потрачено: {avg} с.
'''.format(
		total = ( end - begin ),
		init = ( loaded - begin ),
		cnt = cnt,
		entry_agree_form = agree,
		convert = ( end - loaded ),
		avg = (( end - loaded ) / cnt )
	)
