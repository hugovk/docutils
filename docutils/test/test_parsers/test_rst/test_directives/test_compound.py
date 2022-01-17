#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the 'compound' directive from body.py.
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

totest['compound'] = [
["""\
.. compound::

   Compound paragraphs are single logical paragraphs
   which contain embedded

   * lists
   * tables
   * literal blocks
   * and other body elements

   and are split into multiple physical paragraphs.
""",
"""\
<document source="test data">
    <compound>
        <paragraph>
            Compound paragraphs are single logical paragraphs
            which contain embedded
        <bullet_list bullet="*">
            <list_item>
                <paragraph>
                    lists
            <list_item>
                <paragraph>
                    tables
            <list_item>
                <paragraph>
                    literal blocks
            <list_item>
                <paragraph>
                    and other body elements
        <paragraph>
            and are split into multiple physical paragraphs.
"""],
["""\
.. compound::
   :name: interesting
   :class: log

   This is an extremely interesting compound paragraph containing a
   simple paragraph, a literal block with some useless log messages::

       Connecting... OK
       Transmitting data... OK
       Disconnecting... OK

   and another simple paragraph which is actually just a continuation
   of the first simple paragraph, with the literal block in between.
""",
"""\
<document source="test data">
    <compound classes="log" ids="interesting" names="interesting">
        <paragraph>
            This is an extremely interesting compound paragraph containing a
            simple paragraph, a literal block with some useless log messages:
        <literal_block xml:space="preserve">
            Connecting... OK
            Transmitting data... OK
            Disconnecting... OK
        <paragraph>
            and another simple paragraph which is actually just a continuation
            of the first simple paragraph, with the literal block in between.
"""],
["""\
.. compound:: content may start on same line

   second paragraph
""",
"""\
<document source="test data">
    <compound>
        <paragraph>
            content may start on same line
        <paragraph>
            second paragraph
"""],
]


if __name__ == '__main__':
    unittest.main()
