#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for states.py.
"""

if __name__ == '__main__':
    import __init__
import unittest
from test_parsers import DocutilsTestSupport


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
