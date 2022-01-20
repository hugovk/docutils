import unittest

from test import DocutilsTestSupport  # before importing docutils!

import docutils.parsers

# TODO: test with alternative CommonMark parsers?
try:
    import recommonmark
    docutils.parsers.get_parser_class('recommonmark')
except ImportError:
    raise unittest.SkipTest('Cannot test "recommonmark". Parser not found.')
else:
    if recommonmark.__version__ < '0.6.0':
        raise unittest.SkipTest('"recommonmark" parser too old, skip tests')
