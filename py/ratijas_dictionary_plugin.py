#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from apple_dictionary_plugin import AppleDictionaryPlugin
from dsl.u import *

matter_filename = 'front_back_matter.html'


class RatijasDictionaryPlugin(AppleDictionaryPlugin):
    """
    этот класс используется одновременно в русско-китайском и китайско-русском направлениях.
    надо было как-то его назвать, и я выбрал нейтральное RatijasDictionaryPlugin
    """

    def __init__(self):
        super(RatijasDictionaryPlugin, self).__init__()

        self.matter = u''
        try:
            f = open(matter_filename, 'r')
            self.matter = u(f.read())
            f.close()
        except Exception as e:
            print 'RatijasDictionaryPlugin: не найдено файла обложки словаря (%s)' % matter_filename

        # конец __init__()

    def front_back_matter(self):
        return self.matter
