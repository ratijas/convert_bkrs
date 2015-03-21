#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math

__all__ = ['ProgressBar']


class ProgressBar(object):
    """графическое представление продвижения прогресса"""
    __slots__ = ('_min', '_max', '_value', '_width')

    def __init__(self, min, max, width, value=None):
        self.set_min(min)
        self.set_max(max)
        self.set_value(self.min() if value is None else value)
        self.set_width(width)

    def set_min(self, min):
        self._min = float(min)

    def min(self):
        return self._min

    def set_max(self, max):
        self._max = float(max)

    def max(self):
        return self._max

    def set_value(self, value):
        self._value = float(value)

    def value(self):
        return self._value

    def set_width(self, width):
        self._width = int(width)

    def width(self):
        return self._width

    def label_width_max(self):
        'максимальная длина крайних значений в виде строк'
        return max(map(lambda x: len(str(int(x()))),
                   (self.min, self.max, self.value)))

    def __str__(self):
        label_width_max = self.label_width_max()

        max_ = max(self.min(), self.max())
        min_ = min(self.min(), self.max())

        # current точно в диапазоне [ min_ ; max_ ]
        current = min(self.value(), max_)
        current = max(min_, current)

        # ширина ползунка = ширина  -     ширина меток   - “ [>] ”
        active_width = self.width() - (label_width_max * 2) - 5

        try:
            # заполненная часть (слева)
            filled_width = int(math.floor(
                (current - min_) /
                (max_ - min_) * active_width))
        except ZeroDivisionError:
            filled_width = 0

        # пустая часть (справа)
        nofill_width = active_width - filled_width

        return '%*d [%s>%s] %*d' % (
            label_width_max,
            self.value(),
            #
            '=' * filled_width,
            ' ' * nofill_width,
            #
            label_width_max,
            self.max()
        )

    def __repr__(self):
        return 'ProgressBar(min=%d, max=%d, width=%d, value=%d)' %\
            (self.min(), self.max(), self.width(), self.value())
