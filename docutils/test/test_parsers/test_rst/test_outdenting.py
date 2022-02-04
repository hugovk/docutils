#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for states.py.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestOutdenting(unittest.TestCase):
    def test_outdenting(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        parser = rst.Parser()

        for casenum, (case_input, case_expected) in enumerate(outdenting):
            with self.subTest(id=f'outdenting[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)


outdenting = [
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
    unittest.main()
