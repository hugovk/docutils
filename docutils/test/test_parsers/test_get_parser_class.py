#! /usr/bin/env python3

# $Id$
# Author: grubert abadger1999
# Maintainer: docutils-develop@lists.sourceforge.net
# Copyright: This module has been placed in the public domain.

"""
test get_parser_class
"""

import unittest

from docutils.parsers import get_parser_class


class TestGetParserClass(unittest.TestCase):
    def test_registered_parser(self):
        try:
            get_parser_class('rst')
        except ImportError:
            self.fail("get_parser_class('rst') raised an unexpected ImportError!")

    def test_bogus_parser(self):
        with self.assertRaises(ImportError):
            get_parser_class('nope')

    def test_local_parser(self):
        # requires local-parser.py in test directory (testroot)
        try:
            get_parser_class('local-parser')
        except ImportError:
            self.fail("get_parser_class('local-parser') raised an unexpected ImportError!")

    def test_missing_parser_message(self):
        try:
            get_parser_class('recommonmark')
        except ImportError as err:
            self.assertIn(
                'requires the package https://pypi.org/project/recommonmark',
                str(err))
        else:
            raise unittest.SkipTest('Optional "recommonmark" module found.')

if __name__ == '__main__':
    unittest.main()
