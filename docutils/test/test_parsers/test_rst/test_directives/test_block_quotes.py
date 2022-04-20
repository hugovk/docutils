#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Tests for the block quote directives "epigraph", "highlights", and
"pull-quote".
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestBlockQuotes(unittest.TestCase):
    def test_block_quote(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        parser = rst.Parser()

        for block_quote_type in 'epigraph', 'highlights', 'pull-quote':
            with self.subTest(type=block_quote_type):
                case_input = block_quote_input.format(type=block_quote_type)
                case_expected = block_quote_output.format(type=block_quote_type)
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)

    def test_block_quote_error(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        parser = rst.Parser()

        for block_quote_type in 'epigraph', 'highlights', 'pull-quote':
            with self.subTest(type=block_quote_type):
                case_input = block_quote_error_input.format(type=block_quote_type)
                case_expected = block_quote_error_output.format(type=block_quote_type)
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)


block_quote_input = """\
.. {type}::

   This is a block quote.

   -- Attribution

   This is another block quote.

   -- Another Attribution,
      Second Line
"""

block_quote_output = """\
<document source="test data">
    <block_quote classes="{type}">
        <paragraph>
            This is a block quote.
        <attribution>
            Attribution
    <block_quote classes="{type}">
        <paragraph>
            This is another block quote.
        <attribution>
            Another Attribution,
            Second Line
"""

# TODO: Add class option.
block_quote_error_input = """\
.. {type}::
"""

block_quote_error_output = """\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Content block expected for the "{type}" directive; none found.
        <literal_block xml:space="preserve">
            .. {type}::
"""

if __name__ == '__main__':
    unittest.main()
