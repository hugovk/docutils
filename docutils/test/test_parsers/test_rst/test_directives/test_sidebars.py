#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the "sidebar" directive.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestSidebars(unittest.TestCase):
    def test_sidebars(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        parser = rst.Parser()

        for casenum, (case_input, case_expected) in enumerate(sidebars):
            with self.subTest(id=f'sidebars[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)



sidebars = [
["""\
.. sidebar:: Outer

   .. sidebar:: Nested

      Body.
""",
"""\
<document source="test data">
    <sidebar>
        <title>
            Outer
        <system_message level="3" line="3" source="test data" type="ERROR">
            <paragraph>
                The "sidebar" directive may not be used within a sidebar element.
            <literal_block xml:space="preserve">
                .. sidebar:: Nested
                \n\
                   Body.
"""],
["""\
.. sidebar:: Margin Notes
   :subtitle: with options
   :class: margin
   :name: note:Options

   Body.
""",
"""\
<document source="test data">
    <sidebar classes="margin" ids="note-options" names="note:options">
        <title>
            Margin Notes
        <subtitle>
            with options
        <paragraph>
            Body.
"""],
["""\
.. sidebar::

   The title is optional.
""",
"""\
<document source="test data">
    <sidebar>
        <paragraph>
            The title is optional.
"""],
["""\
.. sidebar:: Outer

   .. topic:: Topic

      .. sidebar:: Inner

         text
""",
"""\
<document source="test data">
    <sidebar>
        <title>
            Outer
        <topic>
            <title>
                Topic
            <system_message level="3" line="5" source="test data" type="ERROR">
                <paragraph>
                    The "sidebar" directive may not be used within topics or body elements.
                <literal_block xml:space="preserve">
                    .. sidebar:: Inner
                    \n\
                       text
"""],
]


if __name__ == '__main__':
    unittest.main()
