#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for states.py.
"""

import unittest
from test import DocutilsTestSupport

import docutils.parsers
from docutils import frontend
from docutils import utils

md_parser_class = docutils.parsers.get_parser_class('recommonmark')


class RecommonmarkParserTestCase(DocutilsTestSupport.CustomTestCase):

    """Test case for 3rd-party CommonMark parsers."""

    parser = md_parser_class()
    option_parser = frontend.OptionParser(components=(md_parser_class,))
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
                    DocutilsTestSupport._compare_output(self, output, case_expected)

totest = {}

totest['paragraphs'] = [
["""\
A paragraph.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph.
"""],
["""\
Paragraph 1.

Paragraph 2.
""",
"""\
<document source="test data">
    <paragraph>
        Paragraph 1.
    <paragraph>
        Paragraph 2.
"""],
["""\
Line 1.
Line 2.
Line 3.
""",
"""\
<document source="test data">
    <paragraph>
        Line 1.
        Line 2.
        Line 3.
"""],
["""\
Paragraph 1, Line 1.
Line 2.
Line 3.

Paragraph 2, Line 1.
Line 2.
Line 3.
""",
"""\
<document source="test data">
    <paragraph>
        Paragraph 1, Line 1.
        Line 2.
        Line 3.
    <paragraph>
        Paragraph 2, Line 1.
        Line 2.
        Line 3.
"""],
]

if __name__ == '__main__':
    unittest.main()
