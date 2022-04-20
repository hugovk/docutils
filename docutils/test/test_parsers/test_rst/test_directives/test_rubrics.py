#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the "rubric" directive.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestRubrics(unittest.TestCase):
    def test_rubrics(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        parser = rst.Parser()

        for casenum, (case_input, case_expected) in enumerate(rubrics):
            with self.subTest(id=f'rubrics[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)


rubrics = [
["""\
.. rubric:: This is a rubric
""",
"""\
<document source="test data">
    <rubric>
        This is a rubric
"""],
["""\
.. rubric::
.. rubric:: A rubric has no content

   Invalid content
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Error in "rubric" directive:
            1 argument(s) required, 0 supplied.
        <literal_block xml:space="preserve">
            .. rubric::
    <system_message level="3" line="2" source="test data" type="ERROR">
        <paragraph>
            Error in "rubric" directive:
            no content permitted.
        <literal_block xml:space="preserve">
            .. rubric:: A rubric has no content
            \n\
               Invalid content
"""],
["""\
.. rubric:: A rubric followed by a block quote
..

   Block quote
""",
"""\
<document source="test data">
    <rubric>
        A rubric followed by a block quote
    <comment xml:space="preserve">
    <block_quote>
        <paragraph>
            Block quote
"""],
["""\
.. rubric:: A Rubric
   :class: foo bar
   :name: Foo Rubric
""",
"""\
<document source="test data">
    <rubric classes="foo bar" ids="foo-rubric" names="foo\\ rubric">
        A Rubric
"""],
]


if __name__ == '__main__':
    unittest.main()
