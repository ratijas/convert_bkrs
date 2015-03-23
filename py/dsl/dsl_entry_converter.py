# -*- coding: utf-8 -*-

class dslEntryConverter(object):
    """a class that knows good how to organize entry processing.

    require a plugin, as it don't know anything about entry formatting.
    what it does:
        - read entry;
        - store entry's title and content in ivars;
        - 
    """
    def __init__(self, plugin):
        super(dslEntryConverter, self).__init__()
        self.plugin = plugin
