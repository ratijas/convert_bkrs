"""testing XML files with apple dictionary schema.

this module can be run from command line with only argument -- file to
be checked.  if not, you need to import this module and call
``run`` function passing it the file's name.
"""

__all__ = ['JingTestError', 'run', 'main']

from .main import run, main, JingTestError
