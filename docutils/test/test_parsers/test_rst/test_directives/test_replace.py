#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for misc.py "replace" directive.
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

totest['replace'] = [
["""\
Test the |name| directive.

.. |name| replace:: "**replace**"
""",
"""\
<document source="test data">
    <paragraph>
        Test the \n\
        <substitution_reference refname="name">
            name
         directive.
    <substitution_definition names="name">
        "
        <strong>
            replace
        "
"""],
["""\
.. |name| replace:: paragraph 1

                    paragraph 2
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Error in "replace" directive: may contain a single paragraph only.
    <system_message level="2" line="1" source="test data" type="WARNING">
        <paragraph>
            Substitution definition "name" empty or invalid.
        <literal_block xml:space="preserve">
            .. |name| replace:: paragraph 1
            \n\
                                paragraph 2
"""],
["""\
.. |name| replace::
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Content block expected for the "replace" directive; none found.
        <literal_block xml:space="preserve">
            replace::
    <system_message level="2" line="1" source="test data" type="WARNING">
        <paragraph>
            Substitution definition "name" empty or invalid.
        <literal_block xml:space="preserve">
            .. |name| replace::
"""],
["""\
.. |Python| replace:: Python, *the* best language around

.. _Python: http://www.python.org/

I recommend you try |Python|_.
""",
"""\
<document source="test data">
    <substitution_definition names="Python">
        Python, \n\
        <emphasis>
            the
         best language around
    <target ids="python" names="python" refuri="http://www.python.org/">
    <paragraph>
        I recommend you try \n\
        <reference refname="python">
            <substitution_reference refname="Python">
                Python
        .
"""],
["""\
.. |name| replace::  *error in **inline ``markup
""",
"""\
<document source="test data">
    <system_message ids="system-message-1" level="2" line="1" source="test data" type="WARNING">
        <paragraph>
            Inline emphasis start-string without end-string.
    <system_message ids="system-message-2" level="2" line="1" source="test data" type="WARNING">
        <paragraph>
            Inline strong start-string without end-string.
    <system_message ids="system-message-3" level="2" line="1" source="test data" type="WARNING">
        <paragraph>
            Inline literal start-string without end-string.
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Substitution definition contains illegal element <problematic>:
        <literal_block xml:space="preserve">
            <problematic ids="problematic-1" refid="system-message-1">
                *
        <literal_block xml:space="preserve">
            .. |name| replace::  *error in **inline ``markup
"""],
["""\
.. replace:: not valid outside of a substitution definition
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Invalid context: the "replace" directive can only be used within a substitution definition.
        <literal_block xml:space="preserve">
            .. replace:: not valid outside of a substitution definition
"""],
]


if __name__ == '__main__':
    unittest.main()
