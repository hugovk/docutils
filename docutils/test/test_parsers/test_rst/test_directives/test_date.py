#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the misc.py "date" directive.
"""

import unittest
from test import DocutilsTestSupport
import time

from docutils.io import locale_encoding

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

totest['date'] = [
["""\
.. |date| date::

Today's date is |date|.
""",
"""\
<document source="test data">
    <substitution_definition names="date">
        %s
    <paragraph>
        Today's date is \n\
        <substitution_reference refname="date">
            date
        .
""" % time.strftime('%Y-%m-%d')],
["""\
.. |date| date:: %a, %d %b %Y
""",
"""\
<document source="test data">
    <substitution_definition names="date">
        %s
""" % time.strftime('%a, %d %b %Y')],
["""\
.. date::
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Invalid context: the "date" directive can only be used within a substitution definition.
        <literal_block xml:space="preserve">
            .. date::
"""],
]

# some locales return non-ASCII characters for names of days or months
if locale_encoding in ['utf8', 'utf-8', 'latin-1']:
    totest['decode date'] = [
    ["""\
.. |date| date:: t\xc3glich
""",
    """\
<document source="test data">
    <substitution_definition names="date">
        t\xc3glich
"""],
    ]

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
