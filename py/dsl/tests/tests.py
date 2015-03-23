# -*- coding: utf-8 -*-

import os
import sys
import unittest

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", ".."))
import dsl
from dsl import dslEntry

class separate_entry_TestCase(unittest.TestCase):
    pass


class one_entry_dictionary_TestCase(unittest.TestCase):
    pass


class namy_entries_dictionary_TestCase(unittest.TestCase):
    pass


class tools_testing_TestCase(unittest.TestCase):
    pass
