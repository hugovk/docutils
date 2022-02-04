#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for docutils.transforms.peps.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.transforms import universal
from docutils.transforms.peps import TargetNotes


class TestTransformPEPs(unittest.TestCase):
    def test_peps(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(target_notes_input, document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transform(TargetNotes)
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()
        output = document.pformat()
        self.assertEqual(output, target_notes_output)

    def test_peps_no_section(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(no_target_notes_input, document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transform(TargetNotes)
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()
        output = document.pformat()
        self.assertEqual(output, no_target_notes_output)


no_target_notes_input = """\
No references or targets exist, therefore
no "References" section should be generated.
"""

no_target_notes_output = """\
<document source="test data">
    <paragraph>
        No references or targets exist, therefore
        no "References" section should be generated.
"""


target_notes_input = """\
A target exists, here's the reference_.
A "References" section should be generated.

.. _reference: https://www.example.org
"""

target_notes_output = """\
<document source="test data">
    <paragraph>
        A target exists, here's the 
        <reference name="reference" refname="reference">
            reference
         
        <footnote_reference auto="1" ids="footnote-reference-1" refname="TARGET_NOTE: footnote-1">
        .
        A "References" section should be generated.
    <target ids="reference" names="reference" refuri="https://www.example.org">
    <section ids="section-1">
        <title>
            References
        <footnote auto="1" ids="footnote-1" names="TARGET_NOTE:\\ footnote-1">
            <paragraph>
                <reference refuri="https://www.example.org">
                    https://www.example.org
"""

if __name__ == '__main__':
    unittest.main()
