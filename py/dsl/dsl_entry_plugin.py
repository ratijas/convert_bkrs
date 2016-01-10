#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from u import *


class dslEntryPlugin(object):
    """
    абстрактный класс, определяет методы, которые нужно переопределить:

    preparse( t, s ) -> ( t, s )
    postparse( t, s ) -> str

    @optional
    read( file ) -> tuple( title, entry )
                 -> None # в случае неудачи

    *примечание: все строки-аргументы и строки-возвращаемые значения являются юникодными
    """

    def __init__(self):
        super(dslEntryPlugin, self).__init__()
        self.escapeXML = True

    def preparse(self, t, s):
        return t, s

    def postparse(self, t, s):
        return u'%s%s' % (u(t), u(s))

    # def read( self, file ):
    # 	if file:
    # 		return ( u'title', u'body' )
    # 	else:
    # 		return None
