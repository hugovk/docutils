#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Tests for the body.py 'parsed-literal' directive.
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

totest['parsed_literals'] = [
["""\
.. parsed-literal::

   This is a parsed literal block.
   It may contain *inline markup
   spanning lines.*
""",
"""\
<document source="test data">
    <literal_block xml:space="preserve">
        This is a parsed literal block.
        It may contain \n\
        <emphasis>
            inline markup
            spanning lines.
"""],
["""\
.. parsed-literal::
  :class: myliteral
  :name: example: parsed

   This is a parsed literal block with options.
""",
"""\
<document source="test data">
    <literal_block classes="myliteral" ids="example-parsed" names="example:\\ parsed" xml:space="preserve">
         This is a parsed literal block with options.
"""],
["""\
.. parsed-literal:: content may start on same line
""",
"""\
<document source="test data">
    <literal_block xml:space="preserve">
        content may start on same line
"""],
["""\
.. parsed-literal::
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Content block expected for the "parsed-literal" directive; none found.
        <literal_block xml:space="preserve">
            .. parsed-literal::
"""],
]


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
