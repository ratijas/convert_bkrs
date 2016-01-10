# -*- coding: UTF-8 -*-

from dsl_dictionary_plugin import *
import re
from u import *
from dsl_entry import dslEntry
import progress_bar
import os


class dslDictionary(object):
    """
    dslDictionary( plugin, infile, outfile, entry_instance ) -> object

    класс-обёртка для словаря. разбирает заголовки dsl файла, кстати.
    plugin -- экземпляр подкласса dslDictionaryPlugin
    infile -- файл или имя входного файла dsl
    outfile -- файл или имя выходного файла (формат зависит от плагина)
    entry_instance -- экземпляр класса dslEntry, желательно, заправленый плагином
    """

    def __init__(self, plugin=None, infile=None, outfile=None, entry_instance=None):
        super(dslDictionary, self).__init__()

        # плагин либо dslDictionaryPlugin, либо ничего
        if plugin and not isinstance(plugin, dslDictionaryPlugin):
            raise TypeError('dslDictionary: `plugin` должен быть подкласом dslDictionaryPlugin')
        else:
            self.plugin = plugin

        # файл для чтения. можно дать имя файла
        #   ваш к.о.
        if not isinstance(infile, file):
            if isinstance(infile, basestring):
                try:
                    self.infile = open(infile, 'r')
                except Exception, e:
                    raise Exception('dslDictionary: не удалось открыть файл %s' % infile)
        else:
            self.infile = infile

        # аналогично, можно передать имя файла
        if not isinstance(outfile, file):
            if isinstance(outfile, basestring):
                try:
                    self.outfile = open(outfile, 'w')
                except Exception, e:
                    raise Exception('dslDictionary: не удалось открыть файл %s' % outfile)
        else:
            self.outfile = outfile

        if not isinstance(entry_instance, dslEntry):
            raise Exception('dslDictionary: `entry_instance` должен быть экземпляром dslEntry')
        else:
            self.entry = entry_instance

        print u'подсчитываю кол-во статей...'

        self.entries_count = 0
        f = os.popen("grep -c -e '^\s*$' '%s'" % self.infile.name)
        self.entries_count = int(f.read())
        if self.entries_count > 0:
            print u'\t->%d' % self.entries_count
        else:
            print u'не удалось подсчитать кол-во статей =('
            self.entries_count = 1
        f.close()
        self.progress_drawer = progress_bar.ProgressBarController(0, self.entries_count)

    # конец __init__

    def __del__(self):
        self.infile.close()
        self.outfile.close()

    def read_headers(self):
        headers = []
        print 'читаю заголовки...'
        while True:
            self.last_read = u(self.infile.readline().strip())
            # print 'read_headers: прочел "%s"' % utf( self.last_read )

            if self.last_read.startswith(u'#'):
                _ = re.match(
                    # #INDEX_LANGUAGE "Russian"
                    # #      \w+    \s " .+  "
                    ur'#(\w+)\s+([\'"]?)([^\n]+?)\2',
                    self.last_read,
                    re.UNICODE
                )
                if _:
                    # \1 -- имя, \3 -- значение
                    _ = _.groups()
                    headers.append({'title': _[0], 'value': _[2]})
                    print u'dslDictionary.read_headers: title: "%s", value: "%s"' % (_[0], _[2])
                else:
                    break
            else:
                # положить обратно где взял
                self.infile.seek(- len(self.last_read), 1)
                break

        return headers

    # конец read_headers


    def convert(self):
        # метаданные словаря. строки, которые начинаются с решетки
        headers = self.read_headers()
        if self.plugin:
            self.plugin.set_headers(headers)

        # плагин пишет какие-то данные в начале словаря. <d:dictionary ...>, например, обложку, ...
        if self.plugin:
            _ = self.plugin.dictionary_begin()
            self.outfile.write(utf(_))

        # напечатать все статьи
        cnt = self._print_entries()

        # припечатать outro в конце. </d:dictionary>, например
        if self.plugin:
            _ = self.plugin.dictionary_end()
            self.outfile.write(utf(_))

        return cnt

    # конец convert


    def _print_entries(self):
        """
        # Internal
        """
        print 'печатаю статьи...'
        # ...

        writen = 0

        # выход из цикла по окончании файла
        while True:
            # следующий
            _ = self.entry.read(self.infile)

            # признак окончания файла или другой проблемы?
            if not _:
                break

            # идём дальше
            self.entry.parse()

            # вывод в файл
            out = utf(self.entry)

            self.outfile.write(out + '\n')

            writen += 1
            if writen % 10 == 0:
                self.progress_drawer.set_value(writen)

        self.progress_drawer.set_value(writen)
        # новая строка после ползунка
        print

        return writen

    # конец _print_entries
