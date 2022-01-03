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

totest['outdenting'] = [
["""\
Anywhere a paragraph would have an effect on the current
indentation level, a comment or list item should also.

+ bullet

This paragraph ends the bullet list item before a block quote.

  Block quote.
""",
"""\
<document source="test data">
    <paragraph>
        Anywhere a paragraph would have an effect on the current
        indentation level, a comment or list item should also.
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                bullet
    <paragraph>
        This paragraph ends the bullet list item before a block quote.
    <block_quote>
        <paragraph>
            Block quote.
"""],
["""\
+ bullet

.. Comments swallow up all indented text following.

  (Therefore this is not a) block quote.

- bullet

  If we want a block quote after this bullet list item,
  we need to use an empty comment:

..

  Block quote.
""",
"""\
<document source="test data">
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                bullet
    <comment xml:space="preserve">
        Comments swallow up all indented text following.
        \n\
        (Therefore this is not a) block quote.
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                bullet
            <paragraph>
                If we want a block quote after this bullet list item,
                we need to use an empty comment:
    <comment xml:space="preserve">
    <block_quote>
        <paragraph>
            Block quote.
"""],
]

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
