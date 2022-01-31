#! /usr/bin/env python3

# $Id$
# Author: grubert abadger1999
# Maintainer: docutils-develop@lists.sourceforge.net
# Copyright: This module has been placed in the public domain.

"""
test get_reader_class
"""

import unittest

from docutils.readers import get_reader_class


class TestGetReaderClass(unittest.TestCase):
    def test_registered_reader(self):
        try:
            get_reader_class('pep')
        except ImportError:
            self.fail("get_reader_class('pep') raised an unexpected ImportError!")

    def test_bogus_reader(self):
        with self.assertRaises(ImportError):
            get_reader_class('nope')

    def test_local_reader(self):
        # requires local-reader.py in test directory (testroot)
        try:
            get_reader_class('local-reader')
        except ImportError:
            self.fail("get_reader_class('local-reader') raised an unexpected ImportError!")


if __name__ == '__main__':
    unittest.main()
