"""testing jing runner"""

from __future__ import with_statement

import os
import sys
import unittest
import subprocess

# dirty hack to import from up-folder.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import jing_test
del sys.path[0]

here = os.path.dirname(os.path.abspath(__file__))


class ValidXMLTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = os.path.join(here, "valid_dictionary.xml")

    def test_module_run(self):
        jing_test.run(self.filename)

    def test_command_line_run(self):
        oldpwd = os.getcwd()
        try:
            os.chdir(os.path.join(here, ".."))
            subprocess.check_call(["python",
                                   "-m",
                                   "jing_test",
                                   self.filename])
        except:
            raise
        finally:
            os.chdir(oldpwd)


class InvalidXMLTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = os.path.join(here, "invalid_dictionary.xml")

    def test_run(self):
        with self.assertRaises(jing_test.JingTestError):
            try:
                jing_test.run(self.filename)
            except jing_test.JingTestError, e:
                print str(e)
                raise


if __name__ == '__main__':
    unittest.main()
