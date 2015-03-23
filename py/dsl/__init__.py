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

``dslDictionaryConverter`` has abstract parameters like *source* and
*target*.  although it don't know nothing about what to do with them
and what kind of they are, it let concrete subclasses to decide how to
generate new dictionary template.
"""

__all__ = [
    'dslDictionaryConverter'
    ]

from .dsl_dictionary_converter import dslDictionaryConverter

# from dsl_dictionary        import dslDictionary
# from dsl_dictionary_plugin import dslDictionaryPlugin
# from dsl_entry        import dslEntry
# from dsl_entry_plugin import dslEntryPlugin

# import time
# from format_time_report import format_time_report
