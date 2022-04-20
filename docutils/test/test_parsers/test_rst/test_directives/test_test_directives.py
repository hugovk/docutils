#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for misc.py test directives.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestTestDirectives(unittest.TestCase):
    def test_test_directives(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        parser = rst.Parser()

        for casenum, (case_input, case_expected) in enumerate(test_directives):
            with self.subTest(id=f'test_directives[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)


test_directives = [
["""\
.. reStructuredText-test-directive::

Paragraph.
""",
"""\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            Directive processed. Type="reStructuredText-test-directive", arguments=[], options={}, content: None
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive ::

An optional space before the "::".
""",
"""\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            Directive processed. Type="reStructuredText-test-directive", arguments=[], options={}, content: None
    <paragraph>
        An optional space before the "::".
"""],
["""\
.. reStructuredText-test-directive:: argument

Paragraph.
""",
"""\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            Directive processed. Type="reStructuredText-test-directive", arguments=['argument'], options={}, content: None
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive:: argument
   :option: value

Paragraph.
""",
"""\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            Directive processed. Type="reStructuredText-test-directive", arguments=['argument'], options={'option': 'value'}, content: None
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive:: :option: value

Paragraph.
""",
"""\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            Directive processed. Type="reStructuredText-test-directive", arguments=[], options={'option': 'value'}, content: None
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive:: :option:

Paragraph.
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Error in "reStructuredText-test-directive" directive:
            invalid option value: (option: "option"; value: None)
            argument required but none supplied.
        <literal_block xml:space="preserve">
            .. reStructuredText-test-directive:: :option:
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive::

   Directive block contains one paragraph, with a blank line before.

Paragraph.
""",
"""\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            Directive processed. Type="reStructuredText-test-directive", arguments=[], options={}, content:
        <literal_block xml:space="preserve">
            Directive block contains one paragraph, with a blank line before.
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive::


   Directive block contains one paragraph, with two blank lines before.

Paragraph.
""",
"""\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            Directive processed. Type="reStructuredText-test-directive", arguments=[], options={}, content:
        <literal_block xml:space="preserve">
            Directive block contains one paragraph, with two blank lines before.
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive::
   Directive block contains one paragraph, no blank line before.

Paragraph.
""",
"""\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            Directive processed. Type="reStructuredText-test-directive", arguments=['Directive block contains one paragraph, no blank line before.'], options={}, content: None
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive::
   block
no blank line.

Paragraph.
""",
"""\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            Directive processed. Type="reStructuredText-test-directive", arguments=['block'], options={}, content: None
    <system_message level="2" line="3" source="test data" type="WARNING">
        <paragraph>
            Explicit markup ends without a blank line; unexpected unindent.
    <paragraph>
        no blank line.
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive:: argument
   :option: * value1
            * value2

Paragraph.
""",
"""\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            Directive processed. Type="reStructuredText-test-directive", arguments=['argument'], options={'option': '* value1\\n* value2'}, content: None
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive::

   Directive \\block \\*contains* \\\\backslashes.
""",
"""\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            Directive processed. Type="reStructuredText-test-directive", arguments=[], options={}, content:
        <literal_block xml:space="preserve">
            Directive \\block \\*contains* \\\\backslashes.
"""],
]


if __name__ == '__main__':
    unittest.main()
