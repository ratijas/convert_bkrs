#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from dsl_entry_plugin import dslEntryPlugin
from u import u, utf
import normalize
from dsl_to_html import dsl_to_html


class dslEntry(object):
    """
    dslEntry( plugin )

    класс для считывания ( read() ), преобразования ( parse() )
    и записи ( str() ) словарной статьи.
    пригоден для многоразового использования

    # ВНИМАНИЕ: метод __str__ возвращает unicode!
    поправка: _раньше_ возвращал, что приводило к ошибкам вызова str( entry ). теперь возвращает <type 'str'>
    """

    def __init__(self, plugin=None):
        super(dslEntry, self).__init__()

        self.entry = u''
        self.title = u''
        self.content = u''

        if plugin and not isinstance(plugin, dslEntryPlugin):
            raise TypeError('dslEntry: `plugin` должен быть подкласом dslEntryPlugin')
        self.plugin = plugin

    # конец __init__()


    def read(self, f):
        """
        считывает статью из файла.

        предполагается, что статьи разделны хотя бы одной пустой строкой
        в случае неудачи (например, EOF) возвращает None

        может делегировать вызов плагину
        self.plugin.read( f )
            -> tuple( title, entry )
            -> None // в случае неудачи
        """
        if hasattr(self.plugin, 'read'):
            _ = self.plugin.read(f)
            if _:
                self.title, self.entry = _[0], _[1].strip()
                return self
            return None

        self.title = u''
        # пропустить пустые строки
        while True:
            _ = u(f.readline())
            if _ is not u'\n':
                self.title = _.strip()
                break

        self.entry = u''
        # читать до пустой строки или EOF
        # именно пустой, а не содержащей пробелы
        while True:
            line = u(f.readline())
            if line != u'\n' and line != u'':
                self.entry += line
            else:
                break

        self.entry = self.entry.strip()
        if len(self.entry) == 0:
            return None
        return self

    # конец read

    def escapeXML(self, s):
        return s \
            .replace(ur'&', ur'&amp;') \
            .replace(ur'<', ur'&lt;') \
            .replace(ur'>', ur'&gt;') \
            .replace(ur'"', ur'&quot;')

    def parse(self):
        t, e = self.title, self.entry

        # полный вариант заголовка со скобками
        t = normalize.brackets(t)

        if self.plugin == None or self.plugin.escapeXML:
            t = self.escapeXML(t)
            e = self.escapeXML(e)

        if self.plugin:
            t, e = self.plugin.preparse(t, e)

        t, e = self._parse(t, e)

        if self.plugin:
            self.content = self.plugin.postparse(t, e)
        else:
            self.content = ur'%s%s' % (t, e)

        return self

    # конец parse


    def _parse(self, title, entry):
        """
        # Internal. делает основное превращение dsl в html
        """

        title = normalize.full(title)
        title = ur'<h1>%s</h1>' % title if title != u'' else u''

        entry = dsl_to_html(entry)

        return title, entry

    # конец _parse


    def __str__(self):
        return utf(self.content)


if __name__ == '__main__':
    from io import StringIO

    # from apple_entry_plugin import AppleEntryPlugin
    # e = dslEntry( plugin = AppleEntryPlugin() )
    e = dslEntry()

    testing_entries = [
        u'''бывать{(ся)}
 [m1]бывает ([c][i]прим.[/c] часто встречаются[/i])[/m]
''',
        u'''статья & ко
тест <на> эскейпы & скобки''',
        u'''escapeXML
здесь мы собираемся заменять символы '<', '>', '&' и '[b]"[/b]'.
они будут заменены на '&lt;', '&gt;', '&amp;' и '&quot;' соответственно.
''',
        u'''
проверка
[m1][p]сущ.[/p] от [c][i]гл.[/c][/i] [b]проверять[/b][/m]
[m1]1) тестирование[/m]
[m2][ex][*]проверка на вшивость[/*][/ex][/m]
''',
        u'''加一点儿[汉语]
[m1]为的是[ref]看一看[/ref]。[b]一见[/b]复杂的句子，就[ref]吓死[/ref]了。[/m]
''',
        u'''ссылки
[m1]поведение [ref]"ссылок"[/ref] со специальными [url]& знаками[/url][/m]
''',
        u'''одинаковые ссылки
[ref] "tt" [/ref]
[ref] "dd" [/ref]
[ref] "tt & dd" [/ref]
[ref] "dd" & tt [/ref]
''',
        u'''R&D计划
 r&d jìhuà
 [m1]программа, план исследований и разработок[/m]
'''
    ]

    for s in testing_entries:
        e.read(StringIO(s))
        e.parse()
        print u'исходный:\n' + s + u'\nрезультат:\n' + u(e) + '\n\n'
