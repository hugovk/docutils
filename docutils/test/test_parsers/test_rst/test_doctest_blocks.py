#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for states.py.
"""

import unittest
from test import DocutilsTestSupport

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class ParserTestCase(DocutilsTestSupport.CustomTestCase):

    """
    Output checker for the parser.

    Should probably be called ParserOutputChecker, but I can deal with
    that later when/if someone comes up with a category of parser test
    cases that have nothing to do with the input and output of the parser.
    """

    parser = rst.Parser()
    """Parser shared by all ParserTestCases."""

    option_parser = frontend.OptionParser(components=(rst.Parser,))
    settings = option_parser.get_default_values()
    settings.report_level = 5
    settings.halt_level = 5
    settings.debug = False

    def test_parser(self):
        for name, cases in totest.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    document = utils.new_document('test data', self.settings.copy())
                    self.parser.parse(case_input, document)
                    output = document.pformat()
                    DocutilsTestSupport._compare_output(self, case_input, output, case_expected)


totest = {}

totest['doctest_blocks'] = [
["""\
Paragraph.

>>> print("Doctest block.")
Doctest block.

Paragraph.
""",
"""\
<document source="test data">
    <paragraph>
        Paragraph.
    <doctest_block xml:space="preserve">
        >>> print("Doctest block.")
        Doctest block.
    <paragraph>
        Paragraph.
"""],
["""\
Paragraph.

>>> print("    Indented output.")
    Indented output.
""",
"""\
<document source="test data">
    <paragraph>
        Paragraph.
    <doctest_block xml:space="preserve">
        >>> print("    Indented output.")
            Indented output.
"""],
["""\
Paragraph.

    >>> print("    Indented block & output.")
        Indented block & output.
""",
"""\
<document source="test data">
    <paragraph>
        Paragraph.
    <block_quote>
        <doctest_block xml:space="preserve">
            >>> print("    Indented block & output.")
                Indented block & output.
"""],
]

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
