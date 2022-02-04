#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for `docutils.transforms.references.TargetNotes`.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.transforms import universal
from docutils.transforms.references import AnonymousHyperlinks
from docutils.transforms.references import DanglingReferences
from docutils.transforms.references import ExternalTargets
from docutils.transforms.references import IndirectHyperlinks
from docutils.transforms.references import InternalTargets
from docutils.transforms.references import PropagateTargets


class TestTransformTargetNotes(unittest.TestCase):
    def test_target_notes(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(tables_of_contents_input, document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transforms(
            (PropagateTargets, AnonymousHyperlinks,  IndirectHyperlinks,
             ExternalTargets, InternalTargets, DanglingReferences))
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()

        output = document.pformat()
        self.assertEqual(output, tables_of_contents_output)

    def test_target_notes_custom_class(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(tables_of_contents_custom_class_input, document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transforms(
            (PropagateTargets, AnonymousHyperlinks,  IndirectHyperlinks,
             ExternalTargets, InternalTargets, DanglingReferences))
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()

        output = document.pformat()
        self.assertEqual(output, tables_of_contents_custom_class_output)


tables_of_contents_input = """\
.. _target: http://example.org

A reference to a target_.

.. target-notes::
"""

tables_of_contents_output = """\
<document source="test data">
    <target ids="target" names="target" refuri="http://example.org">
    <paragraph>
        A reference to a \n\
        <reference name="target" refuri="http://example.org">
            target
         \n\
        <footnote_reference auto="1" ids="footnote-reference-1" refid="footnote-1">
        .
    <footnote auto="1" ids="footnote-1" names="TARGET_NOTE:\\ footnote-1">
        <paragraph>
            <reference refuri="http://example.org">
                http://example.org
"""

tables_of_contents_custom_class_input = """\
.. _target: http://example.org

A reference to a target_.

.. target-notes:: :class: custom
"""

tables_of_contents_custom_class_output = """\
<document source="test data">
    <target ids="target" names="target" refuri="http://example.org">
    <paragraph>
        A reference to a \n\
        <reference name="target" refuri="http://example.org">
            target
        <inline classes="custom">
             \n\
        <footnote_reference auto="1" classes="custom" ids="footnote-reference-1" refid="footnote-1">
        .
    <footnote auto="1" ids="footnote-1" names="TARGET_NOTE:\\ footnote-1">
        <paragraph>
            <reference refuri="http://example.org">
                http://example.org
"""

if __name__ == '__main__':
    unittest.main()
