#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from dsl_dictionary import *
from dsl_entry import *

from test_plugin import *

def main():
	converter_data = {
		'infile': 'bkrs.dsl',
		'outfile': 'bruks_text.xml'
	}
	d = dslDictionary(
		plugin=dicPlugin(),
		infile=converter_data['infile'],
		outfile=converter_data['outfile']
		)
	d.convert()

if __name__ == '__main__':
	main()
