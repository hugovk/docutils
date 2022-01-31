import unittest

import docutils.parsers

# TODO: test with alternative CommonMark parsers?
try:
    import recommonmark
    docutils.parsers.get_parser_class('recommonmark')
except ImportError:
    raise unittest.SkipTest('Cannot test "recommonmark". Parser not found.')
