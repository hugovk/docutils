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


class TestParagraphs(unittest.TestCase):
    def test_paragraphs(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        parser = rst.Parser()

        for casenum, (case_input, case_expected) in enumerate(paragraphs):
            with self.subTest(id=f'paragraphs[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)


paragraphs = [
["""\
A paragraph.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph.
"""],
["""\
Paragraph 1.

Paragraph 2.
""",
"""\
<document source="test data">
    <paragraph>
        Paragraph 1.
    <paragraph>
        Paragraph 2.
"""],
["""\
Line 1.
Line 2.
Line 3.
""",
"""\
<document source="test data">
    <paragraph>
        Line 1.
        Line 2.
        Line 3.
"""],
["""\
Paragraph 1, Line 1.
Line 2.
Line 3.

Paragraph 2, Line 1.
Line 2.
Line 3.
""",
"""\
<document source="test data">
    <paragraph>
        Paragraph 1, Line 1.
        Line 2.
        Line 3.
    <paragraph>
        Paragraph 2, Line 1.
        Line 2.
        Line 3.
"""],
["""\
A. Einstein was a really
smart dude.
""",
"""\
<document source="test data">
    <paragraph>
        A. Einstein was a really
        smart dude.
"""],
]

if __name__ == '__main__':
    unittest.main()
