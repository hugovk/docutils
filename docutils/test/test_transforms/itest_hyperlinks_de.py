#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for docutils.transforms.references.Hyperlinks with non-English language.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.languages import de
from docutils.parsers import rst
from docutils.transforms import universal
from docutils.transforms.references import AnonymousHyperlinks
from docutils.transforms.references import DanglingReferences
from docutils.transforms.references import ExternalTargets
from docutils.transforms.references import IndirectHyperlinks
from docutils.transforms.references import InternalTargets
from docutils.transforms.references import PropagateTargets


class TestTransformHyperlinksNonEnglish(unittest.TestCase):
    def test_hyperlinks_transform_non_english(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        settings.language_code = 'de'
        document = utils.new_document('test data', settings)
        rst.Parser().parse("""\
Target_ should propagate past the system_message to set "id" on note.

.. _target:
.. note:: Kurznotiz
   :name: mynote
""", document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transforms(
            (PropagateTargets, AnonymousHyperlinks, IndirectHyperlinks,
             ExternalTargets, InternalTargets, DanglingReferences))
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()

        output = document.pformat()
        self.assertEqual(output, f"""\
<document source="test data">
    <paragraph>
        <reference name="Target" refid="target">
            Target
         should propagate past the system_message to set "id" on note.
    <target refid="target">
    <system_message level="1" line="4" source="test data" type="INFO">
        <paragraph>
            No directive entry for "note" in module "docutils.parsers.rst.languages.de".
            Using English fallback for directive "note".
    <note ids="mynote target" names="mynote target">
        <paragraph>
            Kurznotiz
    <system_message level="1" source="test data" type="INFO">
        <paragraph>
            Using <module 'docutils.languages.de' from {de.__file__!r}> for language "de".
""")


if __name__ == '__main__':
    unittest.main()
