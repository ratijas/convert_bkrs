# -*- coding: UTF-8 -*-
"""
various tools for standardize headers, strings and indentifiers.

- stripping spaces from front and back, and removing multiple
  contiguous spaces;
- generating *stable* id from string;
- working with ambiguous headers like "make up[ one's] mind".
"""

from __future__ import unicode_literals
import re
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from u import u, utf

del sys.path[0], os, sys

try:
    from unidecode import unidecode
except ImportError, e:
    import sys

    print >> sys.stderr, """
module ``unidecode`` is not installed.
you can download it manually from the link bellow:
https://pypi.python.org/packages/source/U/Unidecode/Unidecode-0.04.14.tar.gz
or from install by apt-get if you have one:
sudo apt-get install python-unidecode
"""
    # raise

__all__ = [
    'spaces',
]

# ---- static vars
spaces_re = re.compile(ur'( |\t){2,}', re.UNICODE)


def spaces(s):
    """strip off leading and trailing whitespaces,
    and replace contiguous whitespaces with just one.
    """
    return re.sub(spaces_re, u' ', u(s).strip())


def brackets():
    re_sub = (
        (
            re.compile(ur'( *)\{( *)\\\[( *)', re.UNICODE),  # { \[
            ur'\1\2\3['
        ),
        (
            re.compile(ur'( *)\\\]( *)\}( *)', re.UNICODE),  # \] }
            ur']\1\2\3'
        ),
        (
            re.compile(ur'( *)\{( *)\(( *)\}( *)', re.UNICODE),  # { ( }
            ur'\1\2\3\4['
        ),
        (
            re.compile(ur'( *)\{( *)\)( *)\}( *)', re.UNICODE),  # { ) }
            ur']\1\2\3\4'
        ),
        (
            re.compile(ur'( *)\{( *)\(( *)', re.UNICODE),  # { (
            ur'\1\2\3['
        ),
        (
            re.compile(ur'( *)\)( *)\}( *)', re.UNICODE),  # ) }
            ur']\1\2\3'
        ),
        (
            re.compile(ur'( *)\{( *)', re.UNICODE),  # {
            ur'\1\2['
        ),
        (
            re.compile(ur'( *)\}( *)', re.UNICODE),  # }
            ur']\1\2'
        ),
        (
            re.compile(ur'{.*?}', re.UNICODE),
            ur''
        )
    )

    def brackets(s):
        r"""
        замена всех вариантов скобок на квадратные []

        заменяются такие комбинации:
            { \[ ... \] }
            { ( } ... { ) }
            { ( ... ) }
            { ... }
        """
        s = u(s)
        if s.find(u'{') is not -1:  # -1 значит не найденно
            for exp, sub in re_sub:
                s = re.sub(exp, sub, s)
        return spaces(s)

    return brackets

brackets = brackets()


def full(s):
    """
    full( 'seq[uence]' ) -> 'sequence'

    длинный вариант строки с квадратными скобками
    """
    return u(s).replace(u'[', u'').replace(u']', u'')


def short():
    del_brackets_re = re.compile(ur'\[.*?\]', re.UNICODE)

    def short(s):
        """
        short( 'seq[uence]' ) -> 'seq'

        короткий вариант строки с квадратными скобками
        """
        return spaces(re.sub(del_brackets_re, u'', u(s)))

    return short

short = short()


def id():
    non_id_re = re.compile(ur'[^a-zA-Z0-9_]', re.UNICODE)

    def id(s):
        s = u(s)
        s = unidecode(s)  # возвращает ascii
        s = u(s)
        s = s.strip()
        s = brackets(s)
        s = full(s)
        s = s.lower()
        s = spaces(s)
        s = s.replace(u' ', u'_')
        s = re.sub(non_id_re, u'_', s)
        s = u(s)
        return s

    return id

id = id()

if __name__ == '__main__':
    s = u' попытка 	{(}to{)}   test  这个 '
    print s, '\t\t id() \t\t', id(s)

    r = ur'{(}высоко{)} поднять знамя чего-либо'
    print r, '\t\t brackets() \t\t', brackets(r)

    t = ur'в {(}самый {)}разгар'
    print t, '\t\t full() \t\t', full(brackets(t))

    h = ur'по{ чьему-либо} адресу'
    print h, '\t\t short() \t\t', short(brackets(h))

    d = ur'быть {\[находиться, содержаться\] }под стражей'
    print d, '\t\t brackets() \t\t', brackets(d)
