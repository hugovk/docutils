#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for unknown directives.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestParser(unittest.TestCase):
    def test_unknown(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(unknown_input, document)
        output = document.pformat()
        self.assertEqual(output, unknown_output)


unknown_input = """\
.. reStructuredText-unknown-directive::

.. reStructuredText-unknown-directive:: argument

.. reStructuredText-unknown-directive::
   block
"""

unknown_output = """\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            No directive entry for "reStructuredText-unknown-directive" in module "docutils.parsers.rst.languages.en".
            Trying "reStructuredText-unknown-directive" as canonical directive name.
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Unknown directive type "reStructuredText-unknown-directive".
        <literal_block xml:space="preserve">
            .. reStructuredText-unknown-directive::
    <system_message level="1" line="3" source="test data" type="INFO">
        <paragraph>
            No directive entry for "reStructuredText-unknown-directive" in module "docutils.parsers.rst.languages.en".
            Trying "reStructuredText-unknown-directive" as canonical directive name.
    <system_message level="3" line="3" source="test data" type="ERROR">
        <paragraph>
            Unknown directive type "reStructuredText-unknown-directive".
        <literal_block xml:space="preserve">
            .. reStructuredText-unknown-directive:: argument
    <system_message level="1" line="5" source="test data" type="INFO">
        <paragraph>
            No directive entry for "reStructuredText-unknown-directive" in module "docutils.parsers.rst.languages.en".
            Trying "reStructuredText-unknown-directive" as canonical directive name.
    <system_message level="3" line="5" source="test data" type="ERROR">
        <paragraph>
            Unknown directive type "reStructuredText-unknown-directive".
        <literal_block xml:space="preserve">
            .. reStructuredText-unknown-directive::
               block
"""

if __name__ == '__main__':
    unittest.main()
