#! /usr/bin/env python3

# $Id$
# Author: grubert
# Maintainer: docutils-develop@lists.sourceforge.net
# Copyright: This module has been placed in the public domain.

"""
test get_writer_class
"""

import unittest

from docutils.writers import get_writer_class


class TestGetWriterClass(unittest.TestCase):

    def test_registered_writer(self):
        try:
            get_writer_class('manpage')
        except ImportError:
            self.fail("get_writer_class('manpage') raised an unexpected ImportError!")

    def test_bogus_writer(self):
        with self.assertRaises(ImportError):
            get_writer_class('nope')

    def test_local_writer(self):
        # requires local-writer.py in test directory (testroot)
        try:
            get_writer_class('local-writer')
        except ImportError:
            self.fail("get_writer_class('local-writer') raised an unexpected ImportError!")


if __name__ == '__main__':
    unittest.main()
