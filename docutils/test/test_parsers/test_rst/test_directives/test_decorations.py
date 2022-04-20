#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the "header" & "footer" directives.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TesDecorations(unittest.TestCase):
    def test_headers(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        parser = rst.Parser()

        for casenum, (case_input, case_expected) in enumerate(headers):
            with self.subTest(id=f'headers[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)

    def test_footers(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        parser = rst.Parser()

        for casenum, (case_input, case_expected) in enumerate(footers):
            with self.subTest(id=f'footers[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)


headers = [
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

footers = [
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
    unittest.main()
