#! /usr/bin/env python3
# $Id$
# Author: Günter Milde <milde@users.sf.net>,
# :License: Released under the terms of the `2-Clause BSD license`_, in short:
#
#    Copying and distribution of this file, with or without modification,
#    are permitted in any medium without royalty provided the copyright
#    notice and this notice are preserved.
#    This file is offered as-is, without any warranty.
#
# .. _2-Clause BSD license: https://opensource.org/licenses/BSD-2-Clause
"""
Test module for `docutils.parsers.rst.directives`.
"""

import unittest

import docutils
import docutils.parsers.null
from docutils.parsers.rst import directives


class TestDirectiveOptionConversion(unittest.TestCase):
    def test_flag(self):
        # Raise error when there is an argument:
        self.assertIs(None, directives.flag(''))
        with self.assertRaises(ValueError):
            directives.flag('alles')

    def test_unchanged_required(self):
        # Raise error when there is no argument:
        with self.assertRaises(ValueError):
            directives.unchanged_required(None)
        self.assertEqual(3, directives.unchanged_required(3))

    def test_unchanged(self):
        self.assertEqual('', directives.unchanged(''))
        self.assertTrue('something' == directives.unchanged('something'))
        self.assertEqual(3, directives.unchanged(3))
        self.assertEqual([3], directives.unchanged([3]))

    # TODO: 13 more directive option conversion functions.

    def test_parser_name(self):
        self.assertEqual(directives.parser_name(None), None)
        self.assertEqual(directives.parser_name('null'),
                         docutils.parsers.null.Parser)
        self.assertEqual(directives.parser_name('rst'),
                         docutils.parsers.rst.Parser)
        with self.assertRaises(ValueError):
            directives.parser_name('fantasy')


if __name__ == '__main__':
    unittest.main()
