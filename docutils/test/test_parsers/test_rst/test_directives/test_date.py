#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the misc.py "date" directive.
"""

import time
import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestDate(unittest.TestCase):
    def test_date(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        parser = rst.Parser()

        for casenum, (case_input, case_expected) in enumerate(date):
            with self.subTest(id=f'date[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)


date = [
["""\
.. |date| date::

Today's date is |date|.
""",
f"""\
<document source="test data">
    <substitution_definition names="date">
        {time.strftime('%Y-%m-%d')}
    <paragraph>
        Today's date is \n\
        <substitution_reference refname="date">
            date
        .
"""],
["""\
.. |date| date:: %a, %d %b %Y
""",
f"""\
<document source="test data">
    <substitution_definition names="date">
        {time.strftime('%a, %d %b %Y')}
"""],
["""\
.. date::
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Invalid context: the "date" directive can only be used within a substitution definition.
        <literal_block xml:space="preserve">
            .. date::
"""],
]

if __name__ == '__main__':
    unittest.main()
