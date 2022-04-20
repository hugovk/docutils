#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Tests for the body.py 'parsed-literal' directive.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestParsedLiterals(unittest.TestCase):
    def test_parsed_literals(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        parser = rst.Parser()

        for casenum, (case_input, case_expected) in enumerate(parsed_literals):
            with self.subTest(id=f'parsed_literals[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)


parsed_literals = [
["""\
.. parsed-literal::

   This is a parsed literal block.
   It may contain *inline markup
   spanning lines.*
""",
"""\
<document source="test data">
    <literal_block xml:space="preserve">
        This is a parsed literal block.
        It may contain \n\
        <emphasis>
            inline markup
            spanning lines.
"""],
["""\
.. parsed-literal::
  :class: myliteral
  :name: example: parsed

   This is a parsed literal block with options.
""",
"""\
<document source="test data">
    <literal_block classes="myliteral" ids="example-parsed" names="example:\\ parsed" xml:space="preserve">
         This is a parsed literal block with options.
"""],
["""\
.. parsed-literal:: content may start on same line
""",
"""\
<document source="test data">
    <literal_block xml:space="preserve">
        content may start on same line
"""],
["""\
.. parsed-literal::
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Content block expected for the "parsed-literal" directive; none found.
        <literal_block xml:space="preserve">
            .. parsed-literal::
"""],
]


if __name__ == '__main__':
    unittest.main()
