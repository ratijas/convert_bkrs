# -*- coding: UTF-8 -*-
"""
abstract dictionary converter based on dsl.

converter takes advantage of dsl concepts:
    - line-based input;
    - headers, usually to be found at the top of file;
    - importing, for dictionaries that are splitted into many files;
    - processing entries one by one.

working well with unicode (module ``u`` is recommended).
extensible by plug-ins API.

``dslDictionaryConverter`` is the first thing you should look at.
it has abstract parameters like *source* and *target*.  although it
don't know nothing about what to do with them and what kind of they
are, it let concrete subclasses to decide how to generate new
dictionary template.

take a look at class's documentation for more information on
subclassing and extending with plug-ins.

in simplest case you need to write only two classes: custom plug-ins
derived from ``dslDictionaryPlugin`` and ``dslEntryPlugin``


``dslEntryConverter`` is the next big thing.  this is where most of
job is performing.  unless you need to parse some dialect of dsl or
in other way customize entry's fields, usually you don't need to modify
these class.  just initialize it with suitable plug-in.

"""

__all__ = [
    'dslDictionaryConverter',
    'dslEntryConverter',
    ]

from .dsl_dictionary_converter import dslDictionaryConverter
