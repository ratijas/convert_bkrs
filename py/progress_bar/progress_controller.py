#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import signal
from progress_bar import ProgressBar

__all__ = ['ProgressBarController', 'get_term_width']


def get_term_width():
    import os
    f = os.popen("stty size")
    rd = f.read().split()
    f.close()
    return int(rd[1])

ESC = chr(0x1b) + "["


class ProgressBarController(object):
    """управление полоской прогресса"""
    __slots__ = ('_width', '_term_width', '_progress_bar', '_oldsignal')

    def __init__(self, min, max, width=0, value=None):
        self._width = None
        self._term_width = None
        self._oldsignal = None
        self._progress_bar = ProgressBar(min, max, min)
        if value is not None:
            self._progress_bar.set_value(value)
        # ширина в ноль означает, что полоска должна растянуться на все окно
        # при изменении размера окна полоска подстаивается под новый размер
        self.set_width(width)

    def update_term_width(self):
        # узнать ширину окна
        self._term_width = get_term_width()
        # self._term_height = int(rd[0])

    def sigwinch_handler(self, sig, frame):
        if self._width == 0:
            self.set_width(0)
        else:
            pass
        if hasattr(self._oldsignal, '__call__'):
            self._oldsignal(sig, frame)

    def redraw(self):
        import sys
        s = str(self._progress_bar)
        l = len(s)
        sys.stdout.write(s + ESC + str(l) + "D")
        sys.stdout.flush()

    def set_value(self, value, animated=False):
        import sys
        if not animated:
            self._set_value(value)
            sys.stdout.write(str(self._progress_bar))
        else:
            from animation_controller import \
                AnimationController, AnimationTimingQuad
            start_value = self.value()
            delta = value - start_value

            def step_hook(progress):
                self._set_value(start_value + (delta * progress))
                self.redraw()

            def complete_hook():
                self._set_value(value)
                self.redraw()
                sys.stdout.write(ESC + str(len(str(self._progress_bar))) + "C")

            anim = AnimationController(step=step_hook,
                                       timing=AnimationTimingQuad,
                                       complete=complete_hook)
            anim.begin()

    def _set_value(self, value):
        self._progress_bar.set_value(value)

    def value(self):
        return self._progress_bar.value()

    def set_width(self, width):
        self.update_term_width()
        if width < 0:
            raise ValueError('set_width: width must be >= 0')
        elif width == 0 or width >= self._term_width - 1:
            self._width = 0
            self._progress_bar.set_width(self._term_width - 1)
            self._oldsignal = \
                signal.signal(signal.SIGWINCH, self.sigwinch_handler)
        else:
            self._width = width
            self._progress_bar.set_width(width)
            sig = self._oldsignal if self._oldsignal else signal.SIG_DFL
            signal.signal(signal.SIGWINCH, sig)
            self._oldsignal = None

    def width(self):
        if self._width == 0:
            return self._term_width - 1
        else:
            return self._width

    def progress_bar(self):
        return self._progress_bar

    def set_progress_bar(self, pb):
        self._progress_bar = pb
        pb.set_width(self._width)

    def __str__(self):
        return str(self._progress_bar)

    def __repr__(self):
        pb = self._progress_bar
        return 'ProgressBarController(min=%f, max=%f, width=%d, value=%f)' %\
            (pb.min(), pb.max(), pb.width(), pb.value())
