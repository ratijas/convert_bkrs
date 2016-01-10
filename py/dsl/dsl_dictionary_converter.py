# -*- coding: utf-8 -*-


class dslDictionaryConverter(object):
    """abstract dsl dictionary converter.

    dictionary converter's concrete subclass should know how to:
        - get source data;
        - generate template dictionary / write headers;
        - get entrieses content one by one;
        - finish (write footers / clean temporary resources).

    API for subclassing:
    parameters:
        source -- for example an input file name;
        target -- as well, may be output file name;
        entry_instance -- it is desirable to set it up with plugin; 
    """
    def __init__(self,
                 source=None,
                 target=None,
                 entry_plugin=None):
        super(dslDictionaryConverter, self).__init__()
        self.source = source
        self.target = target
        self.entry_plugin = entry_plugin

    def convert():
        import time
        time_begin = time.time()
        time_init = None
        time_end = None

        e = dslEntry(
            plugin=app_data[ENTRY_PLUGIN_CLASS]()
        )

        d = dslDictionary(
            plugin=app_data[DICTIONARY_PLUGIN_CLASS](),
            infile=app_data[INFILE],
            outfile=app_data[OUTFILE],
            entry_instance=e
        )

        time_init = time.time()

        cnt = d.convert()

        time_end = time.time()
        format_time_report( time_begin, time_init, time_end, cnt )
