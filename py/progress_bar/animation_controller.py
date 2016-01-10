#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""simple in-thread animations.

simple but "real-sized" animations based on timing functions.
really, there's no matter what you want to animate, just create one
controller, feed it with progress callback function and run!

for example:
    >>> import sys
    >>> def step(progress):
    ...     print '=' * int(80 * progress) + '\r',
    ...     # return carriage to the BOL
    ...     sys.stdout.flush()
    ...
    >>> # put carriage on the new line after animation
    ... ac = AnimationController(step, 1.5,
                                 complete=lambda: sys.stdout.write('\n'))
    >>> ac.begin()
"""

from __future__ import division

__all__ = [
    "AnimationController",
    "make_ease_out",
    "make_ease_in_out",
    "AnimationTimingLinear",
    "AnimationTimingEase",
    "AnimationTimingEaseIn",
    "AnimationTimingEaseOut",
    "AnimationTimingEaseInOut",
    "AnimationTimingQuad",
    "AnimationTimingBounce",
    "AnimationTimingBow",
    "AnimationTimingElastic",
    ]


def make_ease_out(timing):
    """make_ease_out(timing_function) --> timing_function_ease_out

    reverse timing function.
    """
    def ease_out(progress):
        return 1 - timing(1 - progress)
    ease_out.__name__ = timing.__name__ + '_ease_out'
    if timing.__doc__:
        ease_out.__doc__ = "reversed timing function:\n\n" + timing.__doc__
    return ease_out


def make_ease_in_out(timing):
    """make_ease_in_out(timing_function) --> timing_function_ease_in_out

    half forward, half backward.
    """
    def ease_in_out(progress):
        if progress < 0.5:
            return timing(2 * progress) / 2.
        else:
            return (2 - timing(2 * (1 - progress))) / 2.
    ease_in_out.__name__ = timing.__name__ + '_ease_in_out'
    if timing.__doc__:
        ease_in_out.__doc__ = "ease_in_out timing function:\n\n%s" %\
            timing.__doc__
    return ease_in_out


def AnimationTimingLinear(progress):
    """linear timing for animations.

    the simplest case.  just returns the given progress.
    """
    return progress


def AnimationTimingEase(progress):
    """quite like cubic_bezier(0.25, 0.1, 0.25, 1)"""
    if progress == 1:
        return 1
    q = 0.07813 - progress / 2
    alpha = -0.25
    Q = (0.0066 + q * q) ** 0.5
    x = Q - q
    X = (abs(x) ** (1/3)) * (-1 if x < 0 else 1)
    y = -Q - q
    Y = (abs(y) ** (1/3)) * (-1 if y < 0 else 1)
    t = X + Y + 0.25
    return ((1 - t) ** 2) * 0.3*t + 3*(1 - t)*t**2 + t**3


def AnimationTimingEaseIn(progress):
    """quite like cubic_bezier(0.42, 0, 1, 1)"""
    return progress ** 1.7


def AnimationTimingEaseOut(progress):
    """quite like cubic_bezier(0, 0.58, 1, 1)"""
    return progress ** 0.48


def AnimationTimingEaseInOut(progress):
    if progress == 1:
        return 1
    q = 0.48 - progress / 1.04
    Q = (0.1734 + q * q) ** 0.5
    x = Q - q
    X = (abs(x) ** (1/3)) * (-1 if x < 0 else 1)
    y = -Q - q
    Y = (abs(y) ** (1/3)) * (-1 if y < 0 else 1)
    t = X + Y + 0.5
    return (1 - t) * 3 * t**2 + t**3


def AnimationTimingQuad(progress):
    """square the progress value"""
    return progress ** 2


def AnimationTimingBounce(progress):
    """bounces four times, reaches end on the last."""
    a = 0
    b = 1
    while True:
        if progress >= (7 - 4 * a) / 11.:
            return -(((11 - 6 * a - 11 * progress) / 4.) ** 2) + (b ** 2)
        a += b
        b /= 2.


def AnimationTimingBow(factor):
    """AnimationTimingBow(x) --> <timing function>

    bow effect.  strengths depends on factor `x`
    """
    def bow(progress):
        return progress ** 2 * ((factor + 1) * progress - factor)
    return bow


def AnimationTimingElastic(factor=1.5):
    """AnimationTimingElastic(x) --> <timing function>

    left-right-left-riight-left-riiight.  factor 1.5 is recommended.
    """
    import math

    def elastic(progress):
        return 2 ** (10 * (progress-1)) *\
            math.cos(20 * math.pi * factor/3. * progress)
    return elastic


class AnimationController(object):
    """setting up animation details and target

    animation controller takes arguments on set up (or post-set up)
    and launches animation on .begin().  user can set animation
    duration and timing function to calculate progress on each frame,
    which will be passed as argument to `step` function.  on finish
    `complete` callable hook executed if provided.

    arguments:
        step - the only required argument.
            must be callable.  to be call every frame of animation.

            called with parameters:
                progress - result of timing function.
                    should but not restricted to be in range [0, 1],
                    also not guaranteed to hit the bounds.
                    again: it depends on provided timing function.

        duration - duration of animation is seconds.  defaults to 0.3.

        timing - *important*  timing function which takes current
            animation progress as percentage of time passed by since
            it begins, and should return real progress of animation as
            a value between 0 and 1.  function must be clean as there
            is NO guarantee about how much times it will be called.

            called with parameters:
                delta - time passed since animation starts to duration.
                    *always* in range [0, 1], starting with 0.

            defaults to AnimationTimingLinear.

        framerate - number of frames (`step` calls) per second.
            defaults to 60.

        complete - hook that would be called only once on animation
            finish.  could be None.
    """
    def __init__(self, step, duration=0.3, timing=AnimationTimingLinear,
                 framerate=None, complete=None):
        super(AnimationController, self).__init__()
        self.step = step
        self.duration = duration
        self.framerate = framerate if framerate else 60  # try hard
        self.timing = timing
        self.complete = complete
        self._begint = None  # starting moment.  to be set up in .begin()

    def begin(self):
        import time
        if self._begint:
            return  # already started and not finished yet
        self._begint = time.time()  # seconds.miliseconds
        delay = 1. / self.framerate
        delta = 0
        while delta != 1:
            now = time.time()
            delta = min(1, (now - self._begint) / self.duration)
            self.step(self.timing(delta))
            # never know how long .step() takes
            until_next_frame = now + delay - time.time()
            if until_next_frame < 0:
                continue
            time.sleep(until_next_frame)
        self._end()

    def _end(self):
        if hasattr(self.complete, "__call__"):
            self.complete()
        self._begint = None
