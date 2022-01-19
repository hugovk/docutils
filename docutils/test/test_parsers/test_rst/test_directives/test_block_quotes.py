#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Tests for the block quote directives "epigraph", "highlights", and
"pull-quote".
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
                    DocutilsTestSupport._compare_output(self, output, case_expected)


generic_tests = [
["""\
.. %(type)s::

   This is a block quote.

   -- Attribution

   This is another block quote.

   -- Another Attribution,
      Second Line
""",
"""\
<document source="test data">
    <block_quote classes="%(type)s">
        <paragraph>
            This is a block quote.
        <attribution>
            Attribution
    <block_quote classes="%(type)s">
        <paragraph>
            This is another block quote.
        <attribution>
            Another Attribution,
            Second Line
"""],
# TODO: Add class option.
["""\
.. %(type)s::
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Content block expected for the "%(type)s" directive; none found.
        <literal_block xml:space="preserve">
            .. %(type)s::
"""],
]

totest = {}
for block_quote_type in ('epigraph', 'highlights', 'pull-quote'):
    totest[block_quote_type] = [
        [text % {'type': block_quote_type} for text in pair]
        for pair in generic_tests]


if __name__ == '__main__':
    unittest.main()
