#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
разбиение строки с пиньинем на блоки с помощью html-тегов

пиньинь обрамляется тегами span с классом t0 .. t4,
в зависимости от тона
'''

import re
from rm_unicode import *

def colorize( textContent ):
	'''
	colorize( str ) -> str

	берёт строку с пиньиньем (или без),
	возвращает ту же строку, но пиньинь обрамлён
	тегами span
	'''
	# задача делится на 
	# 0) поиск
	# 1) оформление
	# 1.1) определение тона

	# поиск
	found = search_for_pin_yin_in_string( textContent )

	# если ни одного нету, пропустить
	if len( found ) is 0:
		return textContent

	# генерация span-тегов с классами t0 .. t4
	return colorize_pin_yin( textContent, found );
	

all_pin_yin_list = u'zhuang,shuang,chuang,zhuan,zhuai,zhong,zheng,zhang,xiong,xiang,shuan,shuai,sheng,shang,qiong,qiang,niang,liang,kuang,jiong,jiang,huang,guang,chuan,chuai,chong,cheng,chang,zuan,zong,zhuo,zhun,zhui,zhua,zhou,zhen,zhei,zhao,zhan,zhai,zeng,zang,yuan,yong,ying,yang,xuan,xing,xiao,xian,weng,wang,tuan,tong,ting,tiao,tian,teng,tang,suan,song,shuo,shun,shui,shua,shou,shen,shei,shao,shan,shai,seng,sang,ruan,rong,reng,rang,quan,qing,qiao,qian,ping,piao,pian,peng,pang,nüe,nuan,nong,ning,niao,nian,neng,nang,ming,miao,mian,meng,mang,lüe,luan,long,ling,liao,lian,leng,lang,kuan,kuai,kong,keng,kang,juan,jing,jiao,jian,huan,huai,hong,heng,hang,guan,guai,gong,geng,gang,feng,fang,duan,dong,ding,diao,dian,deng,dang,cuan,cong,chuo,chun,chui,chua,chou,chen,chao,chan,chai,ceng,cang,bing,biao,bian,beng,bang,zuo,zun,zui,zou,zhu,zhi,zhe,zha,zen,zei,zao,zan,zai,yun,yue,you,yin,yao,yan,xun,xue,xiu,xin,xie,xia,wen,wei,wan,wai,tuo,tun,tui,tou,tie,tao,tan,tai,suo,sun,sui,sou,shu,shi,she,sha,sen,sei,sao,san,sai,ruo,run,rui,rua,rou,ren,rao,ran,qun,que,qiu,qin,qie,qia,pou,pin,pie,pen,pei,pao,pan,pai,nü,nuo,nou,niu,nin,nie,nen,nei,nao,nan,nai,mou,miu,min,mie,men,mei,mao,man,mai,lü,luo,lun,lou,liu,lin,lie,lia,lei,lao,lan,lai,kuo,kun,kui,kua,kou,ken,kei,kao,kan,kai,jun,jue,jiu,jin,jie,jia,huo,hun,hui,hua,hou,hng,hen,hei,hao,han,hai,guo,gun,gui,gua,gou,gen,gei,gao,gan,gai,fou,fen,fei,fan,duo,dun,dui,dou,diu,die,den,dei,dao,dan,dai,cuo,cun,cui,cou,chu,chi,che,cha,cen,cei,cao,can,cai,bin,bie,ben,bei,bao,ban,bai,ang,ê,zu,zi,ze,za,yu,yi,ye,ya,xu,xi,wu,wo,wa,tu,ti,te,ta,su,si,se,sa,ru,ri,re,qu,qi,pu,po,pi,pa,ou,nu,ni,ng,ne,na,mu,mo,mi,ma,lu,li,le,la,ku,ke,ka,ju,ji,hu,hm,he,ha,gu,ge,ga,fu,fo,fa,er,en,ei,du,di,de,da,cu,ci,ce,ca,bu,bo,bi,ba,ao,an,ai,o,n,m,e,a,r'.split( ',' )


def skip():
	# статические переменные
	space_re     = re.compile( r'\W*', re.L )
	not_space_re = re.compile( r'\w*', re.L )

	def skip( char_p, py_plain ):
		# резануть
		py_plain = py_plain[ char_p : ]
		
		# пропустить все не-пробелы
		end = re.match( not_space_re, py_plain ).end()
		char_p += end
		# пропустить все пробелы
		end = re.match( space_re, py_plain[ end : ]).end()

		return char_p + end
	# замыкание
	return skip

skip = skip()

def plain_pin_yin():
	diactris_table = (
		( u'[āáǎăà]',		u'a' ),
		( u'[ēéěè]',		u'e' ),
		( u'[ōóǒò]',		u'o' ),
		( u'[ūúǔùǖǘǚǜ]',	u'u' ),
		( u'[īíǐì]',		u'i' )
	)
	def plain_pin_yin( s ):
		'упрощение поиска: замена букв с тонами на те же, но без тонов'
		py_plain = u( s ).lower()               #  нижний регистр

		for regex, sub in diactris_table:
			py_plain = re.sub( regex, sub, py_plain )

		return py_plain
	return plain_pin_yin
plain_pin_yin = plain_pin_yin()

def search_for_pin_yin_in_string( s ):
	'''
	search_for_pin_yin_in_string( s ) -> list

	возвращаемый список состоит из словарей,
	каждый из которых содержит два элемента:
	точку начала (start: uint)
	и кусок пиньиня (value: str)
	'''
	result = []

	s = u( s )

	py_plain = plain_pin_yin( s )

	#  пройтись по всей строке 
	char_p = 0
	while char_p < len( py_plain ):
		#  получить код символа 
		ch = ord( py_plain[ char_p ])
		#  97  -- это код символа 'a' 
		#  122 -- это код символа 'z' 
		if not ( 97 <= ch <= 122 ):
			#  не буква латиницы 
			#  сдвиг счётчика 
			char_p += 1
			#  пропускаем 
			continue

		#  если мы дошли сюда, значит символ -- буква латиницы 

		#  в случае нахождения ``word'' содержит строку 
		word = None
		#  переменная ``found'' -- нашли или нет?
		found = False

		# циклический поиск строк из списка ``all_pin_yin_list''
		# в упрощёной входной строке c текущего индекса

		for word in all_pin_yin_list:

			#  так быстрее, чем indexOf() потому, что не ищет по всей строке 
			#  от текущего индекса до (текущего индекса + длинна того чтения, который сверяем)

			if py_plain[ char_p : char_p + len( word )] == word:

				# правило апострофа:
				# апостроф ставится перед словом на a/o/e.
				# если следующая буква -- a/o/e, делаем откат на
				#   одну букву назад и проверяем результат.
				# слово не может начинаться с букв i/u
				#     а буквы ``v'' вообще нет.

				try:
					next_letter = py_plain[ char_p + len( word )]
					if next_letter in 'aoeiu':
				 	# убрать последний символ; откат на одну букву
						word = word[ : -1 ]

						# проверка
						if word not in all_pin_yin_list:
							# такого не существует ???
							char_p = skip( char_p, py_plain )
						# всё ок. откат удался
				except IndexError:
					# в питоне обращение к элементу за пределами диапазона вызывает ошибку
					pass
				# нашли, записываем
				found = True
				# прекращаем цикл
				break
			# конец if
		# конец for

		#  нашли 
		if found:
			#  пригодится пару раз 
			py_length = len( word )

			# записать соответствующую часть пиньиня из входной строки
			# в словарь под ключом, равным текущему индексу
			result.append({
				'start': char_p,
				'value': utf( s[ char_p : char_p + py_length])
				})
			#  сдвинуть указатель за пределы текущего слова 
			char_p += py_length
		else:
			#  это латинская буква, но пиньинь не нашли 
			char_p = skip( char_p, py_plain )
		# конец if found
	# конец while char_p < len( pin_yin )

	#  вернуть массив
	return result


def colorize_pin_yin( text, pin_yin_pairs ):
	'''
	colorize_pin_yin( text, pin_yin_pairs ) -> str

	text -- текст с пиньинем
	pin_yin_pairs -- список в виде {start: int, value: str }
	'''

	# сразу определить тона. если все тона нулевые, не раскрашивать
	all_tones_are_zero = True

	for el in pin_yin_pairs:
		start, value = el['start'], el['value']
		# определить
		t = determineTone( value );
		# сохранить на потом
		el['tone'] = t
		# проверить
		if t is not 0:
			all_tones_are_zero = False

	# наверное, это не пиньинь, а английское слово
	if all_tones_are_zero: return

	# котейнер для всего содержимого этой ветки
	# <span class='pinYinWrapper'>
	wrapper = ''

	# предыдущая пара, нужна для вставки содержимого между пиньинем
	prev_pair_end = None

	for el in pin_yin_pairs:
		# явно преобразовать. а то мало ли что
		start, value, tone = int( el['start'] ), el['value'], el['tone']

		# записать предшествующий не-пиньинь в родительский span
			# резать от предыдущего конца
			# ну, или от начала строки
			# до текущего начала, не включительно
		wrapper += text[
			prev_pair_end and prev_pair_end or 0
			:
			start
		]

		# цветастый span для отдельного слога
		span = u'<span class="t%d">%s</span>' % ( tone, value )

		# припаять к контейнеру
		wrapper += span
		# записать текущую пару
		prev_pair_end = start + len( value )

	# от последнего пиньиня и до конца
	wrapper += text[ prev_pair_end : ]
	return wrapper


def determineTone():

	# статические переменные
	re1 = re.compile( u"[āēūǖīō]",  re.UNICODE )
	re2 = re.compile( u"[áéúǘíó]",  re.UNICODE )
	re3 = re.compile( u"[ǎăěǔǚǐǒ]", re.UNICODE )
	re4 = re.compile( u"[àèùǜìò]",  re.UNICODE )

	def determineTone( pin_yin_word ):
		'''
		determineTone( pin_yin ) -> int in range(0, 4)

		возвращает тон для переданого слога
		'''
		pin_yin_word = u( pin_yin_word )
		# быстрее и компактнее так, чем делать цикл и массив
		# тон слога определяется наличием одного из этих символов

		if re1.search( pin_yin_word ) is not None:
			return 1
		if re2.search( pin_yin_word ) is not None:
			return 2
		if re3.search( pin_yin_word ) is not None:
			return 3
		if re4.search( pin_yin_word ) is not None:
			return 4
		# не нашли, значит нулевой тон
		return 0
	return determineTone

determineTone = determineTone()


def main():
	s = u'bǎiwén bùrú yījiàn // fāng’àn // fǎngán // xúniang'
	print u'изначально: "%s"' % s
	r = search_for_pin_yin_in_string( s )
	print u'search_for_pin_yin_in_string() ->'
	for e in r:
		print u'\t' u'start: %d,' u'\t' u'value: %s' % \
			( e['start'], e['value'] )

	print u'colorize\n----'

	s2 = colorize( s )
	print u'type is', type( s2 )
	print s2


if __name__ == '__main__':
	main()
