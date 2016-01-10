#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import getopt, sys


def usage():
    print u'''
использование:
    {name} -a
    {name} -ctmi
'''.format(name=sys.argv[0])


def read_startup_args():
    result = {
        'help': False,
        'convert': False,
        'test': False,
        'make': False,
        'install': False
    }

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hctmia")
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == '-a':
            result['help'] = False
            result['convert'] = True
            result['test'] = True
            result['make'] = True
            result['install'] = True
        elif o == '-h':
            usage()
            sys.exit()
        elif o == '-c':
            result['convert'] = True
        elif o == '-t':
            result['test'] = True
        elif o == '-m':
            result['make'] = True
        elif o == '-i':
            result['install'] = True
        else:
            assert False, "unhandled option"

    return result
