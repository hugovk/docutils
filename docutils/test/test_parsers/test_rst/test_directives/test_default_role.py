#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for misc.py "default-role" directive.
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


totest = {}

totest['default-role'] = [
["""\
.. default-role:: subscript

This is a `subscript`.
""",
"""\
<document source="test data">
    <paragraph>
        This is a \n\
        <subscript>
            subscript
        .
"""],
["""\
Must define a custom role before using it.

.. default-role:: custom
""",
"""\
<document source="test data">
    <paragraph>
        Must define a custom role before using it.
    <system_message level="1" line="3" source="test data" type="INFO">
        <paragraph>
            No role entry for "custom" in module "docutils.parsers.rst.languages.en".
            Trying "custom" as canonical role name.
    <system_message level="3" line="3" source="test data" type="ERROR">
        <paragraph>
            Unknown interpreted text role "custom".
        <literal_block xml:space="preserve">
            .. default-role:: custom
"""],
["""\
.. role:: custom
.. default-role:: custom

This text uses the `default role`.

.. default-role::

Returned the `default role` to its standard default.
""",
"""\
<document source="test data">
    <paragraph>
        This text uses the \n\
        <inline classes="custom">
            default role
        .
    <paragraph>
        Returned the \n\
        <title_reference>
            default role
         to its standard default.
"""],
]


if __name__ == '__main__':
    unittest.main()
