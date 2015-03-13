#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''searching for pinyin and wrap it with HTML.

module provides some useful functions for working with Chinese pinyin,
"phonetic system for transcribing the Mandarin pronunciations of
Chinese characters into the Latin alphabet" (c) wikipedia.

detect and wrap pinyin with HTML in plain text string:
``colorize``

searching for pinyin in string of text:
``ranges_of_pinyin_in_string``

finding out what tone has some pinyin word:
``determine_tone``

remove tones (diacritics) from pinyin string (*utility function*):
``lowercase_string_by_removing_pinyin_tones``

constants:
PINYIN_LIST -- specially sorted list of all possible pinyin words.
'''

import re
from u import u, utf

__all__ = [
    #'colorize',
    'ranges_of_pinyin_in_string',
    'determine_tone',
    'lowercase_string_by_removing_pinyin_tones',
    'PINYIN_LIST',
    ]

PINYIN_LIST = u'zhuang,shuang,chuang,zhuan,zhuai,zhong,zheng,zhang,xiong,xiang,shuan,shuai,sheng,shang,qiong,qiang,niang,liang,kuang,jiong,jiang,huang,guang,chuan,chuai,chong,cheng,chang,zuan,zong,zhuo,zhun,zhui,zhua,zhou,zhen,zhei,zhao,zhan,zhai,zeng,zang,yuan,yong,ying,yang,xuan,xing,xiao,xian,weng,wang,tuan,tong,ting,tiao,tian,teng,tang,suan,song,shuo,shun,shui,shua,shou,shen,shei,shao,shan,shai,seng,sang,ruan,rong,reng,rang,quan,qing,qiao,qian,ping,piao,pian,peng,pang,nüe,nuan,nong,ning,niao,nian,neng,nang,ming,miao,mian,meng,mang,lüe,luan,long,ling,liao,lian,leng,lang,kuan,kuai,kong,keng,kang,juan,jing,jiao,jian,huan,huai,hong,heng,hang,guan,guai,gong,geng,gang,feng,fang,duan,dong,ding,diao,dian,deng,dang,cuan,cong,chuo,chun,chui,chua,chou,chen,chao,chan,chai,ceng,cang,bing,biao,bian,beng,bang,zuo,zun,zui,zou,zhu,zhi,zhe,zha,zen,zei,zao,zan,zai,yun,yue,you,yin,yao,yan,xun,xue,xiu,xin,xie,xia,wen,wei,wan,wai,tuo,tun,tui,tou,tie,tao,tan,tai,suo,sun,sui,sou,shu,shi,she,sha,sen,sei,sao,san,sai,ruo,run,rui,rua,rou,ren,rao,ran,qun,que,qiu,qin,qie,qia,pou,pin,pie,pen,pei,pao,pan,pai,nü,nuo,nou,niu,nin,nie,nen,nei,nao,nan,nai,mou,miu,min,mie,men,mei,mao,man,mai,lü,luo,lun,lou,liu,lin,lie,lia,lei,lao,lan,lai,kuo,kun,kui,kua,kou,ken,kei,kao,kan,kai,jun,jue,jiu,jin,jie,jia,huo,hun,hui,hua,hou,hen,hei,hao,han,hai,guo,gun,gui,gua,gou,gen,gei,gao,gan,gai,fou,fen,fei,fan,duo,dun,dui,dou,diu,die,den,dei,dao,dan,dai,cuo,cun,cui,cou,chu,chi,che,cha,cen,cao,can,cai,bin,bie,ben,bei,bao,ban,bai,ang,zu,zi,ze,za,yu,yi,ye,ya,xu,xi,wu,wo,wa,tu,ti,te,ta,su,si,se,sa,ru,ri,re,qu,qi,pu,po,pi,pa,ou,nu,ni,ng,ne,na,mu,mo,mi,ma,lu,li,le,la,ku,ke,ka,ju,ji,hu,he,ha,gu,ge,ga,fu,fo,fa,er,en,ei,du,di,de,da,cu,ci,ce,ca,bu,bo,bi,ba,ao,an,ai,o,n,m,e,a,r'.split(',')
# sorted by length, so first look up the longest variant.

# static var of function ``lowercase_string_by_removing_pinyin_tones``
_diacritics = (
    (u'āáǎăà',    u'a'),
    (u'ēéěè',     u'e'),
    (u'ōóǒò',     u'o'),
    (u'ūúǔùǖǘǚǜ', u'u'),
    (u'īíǐì',     u'i')
)

def lowercase_string_by_removing_pinyin_tones(s):
    '''lowercase_string_by_removing_pinyin_tones(string) --> unicode

    simplify / plainize chinese pinyin by converting it to lower case and
    removing diacritics from letters 'a', 'e', 'o', 'u', i'.
    '''
    s = u(s).lower()
    for diacrs, normal in _diacritics:
        for diacr in diacrs:
            s = s.replace(diacr, normal)
    return s




def colorize(s):
    '''colorize(s) --> unicode
    
    центральный элемент модуля. парсинг, оформление пиньиня.
    входные параметры:
    - s
        str или unicode, потенциально содержащая пиньинь
    возвращаемое значение:
        unicode; входная строка, найденные вхождения пиньиня завёрнуты
        в теги <span class="t{0..4}">...</span>.  т.е. класс элемента
        состоит из латинской буквы 't' и цифры от нуля до четырёх.
    '''
    found =     search_for_pin_yin_in_string(s)
    # if none found, just skip
    if len(found) == 0:
        return s
    return colorize_pin_yin(s, found)




# ---- static vars
_t1 = u"āēūǖīō"
_t2 = u"áéúǘíó"
_t3 = u"ǎăěǔǚǐǒ"
_t4 = u"àèùǜìò"

def determine_tone(pinyin):
    '''determine_tone(string) --> {0..4}

    detect tone of given pinyin word.
    return value:
        int from 0 up to 4, where 0 means that tone undetermined.
    '''
    pinyin = u(pinyin)
    for letter in pinyin:
        if letter in _t1:
            return 1
        if letter in _t2:
            return 2
        if letter in _t3:
            return 3
        if letter in _t4:
            return 4
    # not found, fall-back to  zero
    return 0


# ---- static vars

def ranges_of_pinyin_in_string(s):
    '''ranges_of_pinyin_in_string(string) -> list<range>

    !! replacing obsolete ``search_for_pin_yin_in_string``

    searches for pinyin in given string *s*.  *s* must be either
    unicode string or utf-8 encoded ``str``, or anything else that
    can be converted by ``u`` function.

    return value:
        list of ranges of pinyin,
        where range is 2-tuple of (index, length).
        list can be empty.
    '''
    raise NotImplementedError
    result = []
    def range(index, length):
        return (index, length)

    # the trick of replacing 'v' is that 'v' does not exists in pinyin,
    # but still returns *True* on str.islower()
    plain_s = lowercase_string_by_removing_pinyin_tones(s).replace(u'v', u' ')
    plain_s_len = len(plain_s)

    char_p = 0  # scan through whole string, skipping len(found) chars.
    while char_p < plain_s_len:
        # scan for next nearest beginning of pinyin word,
        # e.g for small(1) latin char [a-z].
        # (1) small because after ``lowercase_...`` no caps left.
        if not plain_s[char_p].islower():
            char_p += 1
            continue
        # now char_p pointing at lowercase letter

        # try to match string to pinyin from the list.  remember that list is
        # sorted by length.
        for word in PINYIN_LIST:
            word_len = len(word)
            if plain_s.find(word, char_p, char_p + word_len) != -1:
                # rule of apostrophe: "'" must be before 'a', 'e' and 'o'.
                # if next letter exactly 'a', 'e' or 'o',
                # do a rollback by one letter and check.
                # remember that a pinyin never begins with 'i' or 'u',
                # and 'v' already replaced with space before the loop.
                if plain_s[char_p + word_len] in 'aoeiu':
                    # rollback
                    pass
        else:
            # loop exited normally, means word not matches pinyin
            skip()

    return result



def search_for_pin_yin_in_string(s):
    '''search_for_pin_yin_in_string(s) -> list

    возвращаемый список состоит из словарей,
    каждый из которых содержит два элемента:
    точку начала (start: uint)
    и кусок пиньиня (value: str)
    '''
    result = []

    s = u(s)

    py_plain = lowercase_string_by_removing_pinyin_tones( s )

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

        # циклический поиск строк из списка ``PINYIN_LIST''
        # в упрощёной входной строке c текущего индекса

        for word in PINYIN_LIST:

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
                        if word not in PINYIN_LIST:
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


def _closure():
    # ---- статические переменные
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
    return skip
skip = _closure()


def colorize_pin_yin( text, pin_yin_pairs ):
    '''colorize_pin_yin( text, pin_yin_pairs ) -> str

    text -- текст с пиньинем
    pin_yin_pairs -- список в виде {start: int, value: str }
    '''

    # сразу определить тона. если все тона нулевые, не раскрашивать
    all_tones_are_zero = True

    for el in pin_yin_pairs:
        start, value = el['start'], u( el[ 'value' ])
        # определить
        t = determine_tone( value );
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
        start, value, tone = int( el['start'] ), u( el[ 'value' ]), el['tone']

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
