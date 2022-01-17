#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the "sidebar" directive.
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

totest['sidebars'] = [
["""\
.. sidebar:: Outer

   .. sidebar:: Nested

      Body.
""",
"""\
<document source="test data">
    <sidebar>
        <title>
            Outer
        <system_message level="3" line="3" source="test data" type="ERROR">
            <paragraph>
                The "sidebar" directive may not be used within a sidebar element.
            <literal_block xml:space="preserve">
                .. sidebar:: Nested
                \n\
                   Body.
"""],
["""\
.. sidebar:: Margin Notes
   :subtitle: with options
   :class: margin
   :name: note:Options

   Body.
""",
"""\
<document source="test data">
    <sidebar classes="margin" ids="note-options" names="note:options">
        <title>
            Margin Notes
        <subtitle>
            with options
        <paragraph>
            Body.
"""],
["""\
.. sidebar::

   The title is optional.
""",
"""\
<document source="test data">
    <sidebar>
        <paragraph>
            The title is optional.
"""],
["""\
.. sidebar:: Outer

   .. topic:: Topic

      .. sidebar:: Inner

         text
""",
"""\
<document source="test data">
    <sidebar>
        <title>
            Outer
        <topic>
            <title>
                Topic
            <system_message level="3" line="5" source="test data" type="ERROR">
                <paragraph>
                    The "sidebar" directive may not be used within topics or body elements.
                <literal_block xml:space="preserve">
                    .. sidebar:: Inner
                    \n\
                       text
"""],
]


if __name__ == '__main__':
    unittest.main()
