#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for docutils.transforms.universal.Messages.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.transforms.references import Substitutions
from docutils.transforms.universal import Messages


class TestTransformMessages(unittest.TestCase):
    def test_messages(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(system_message_sections_input, document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transforms((Substitutions, Messages))
        document.transformer.apply_transforms()

        output = document.pformat()
        self.assertEqual(output, system_message_sections_expected)


system_message_sections_input = """\
This |unknown substitution| will generate a system message, thanks to
the ``Substitutions`` transform. The ``Messages`` transform will
generate a "System Messages" section.

(A second copy of the system message is tacked on to the end of the
document by the test framework.)
"""

system_message_sections_expected = """\
<document source="test data">
    <paragraph>
        This 
        <problematic ids="problematic-1" refid="system-message-1">
            |unknown substitution|
         will generate a system message, thanks to
        the 
        <literal>
            Substitutions
         transform. The 
        <literal>
            Messages
         transform will
        generate a "System Messages" section.
    <paragraph>
        (A second copy of the system message is tacked on to the end of the
        document by the test framework.)
    <section classes="system-messages">
        <title>
            Docutils System Messages
        <system_message backrefs="problematic-1" ids="system-message-1" level="3" line="1" source="test data" type="ERROR">
            <paragraph>
                Undefined substitution referenced: "unknown substitution".
"""


if __name__ == '__main__':
    unittest.main()
