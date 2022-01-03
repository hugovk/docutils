#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the "header" & "footer" directives.
"""

if __name__ == '__main__':
    import __init__
import unittest
from test import DocutilsTestSupport


def suite():
    suite_id = DocutilsTestSupport.make_id(__file__)
    s = unittest.TestSuite()
    for name, cases in totest.items():
        for casenum, (case_input, case_expected) in enumerate(cases):
            s.addTest(
                DocutilsTestSupport.ParserTestCase("test_parser",
                                     input=case_input, expected=case_expected,
                                     id='%s: totest[%r][%s]' % (suite_id, name, casenum),
                                     suite_settings={})
            )
    return s

totest = {}

totest['headers'] = [
["""\
.. header:: a paragraph for the header
""",
"""\
<document source="test data">
    <decoration>
        <header>
            <paragraph>
                a paragraph for the header
"""],
["""\
.. header::
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Content block expected for the "header" directive; none found.
        <literal_block xml:space="preserve">
            .. header::
"""],
["""\
.. header:: first part of the header
.. header:: second part of the header
""",
"""\
<document source="test data">
    <decoration>
        <header>
            <paragraph>
                first part of the header
            <paragraph>
                second part of the header
"""],
]

totest['footers'] = [
["""\
.. footer:: a paragraph for the footer
""",
"""\
<document source="test data">
    <decoration>
        <footer>
            <paragraph>
                a paragraph for the footer
"""],
["""\
.. footer:: even if a footer is declared first
.. header:: the header appears first
""",
"""\
<document source="test data">
    <decoration>
        <header>
            <paragraph>
                the header appears first
        <footer>
            <paragraph>
                even if a footer is declared first
"""],
]


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
