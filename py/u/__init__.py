# -*- coding: utf-8 -*-
"""converting utf strings to unicode and vice-versa"""

__all__ = ('u', 'utf')


def u(s):
    "convert anything to unicode"
    if isinstance(s, unicode):
        return s
    try:
        s = unicode(s)
    except UnicodeDecodeError:
        s = str(s)
        s = s.decode("utf-8")
    return s


def utf(s):
    "convert anything to utf-8"
    if isinstance(s, str):
        return s
    if hasattr(s, '__unicode__'):
        s = unicode(s).encode('utf-8')
    else:
        try:
            s = str(s)
        except UnicodeEncodeError:
            s = s.encode('utf-8')
    return s

# completed and tested with unittest test_unicode.py
