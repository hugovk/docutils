#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test module for writer_aux transforms.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.transforms import universal
from docutils.transforms import writer_aux


class TestTransformWriterAux(unittest.TestCase):
    def test_admonition_note(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(note_input, document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transform(writer_aux.Admonitions)
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()
        output = document.pformat()
        self.assertEqual(output, note_output)

    def test_admonition_generic(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(generic_admonition_input, document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transform(writer_aux.Admonitions)
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()
        output = document.pformat()
        self.assertEqual(output, generic_admonition_output)


note_input = """\
.. note::

   These are the note contents.

   Another paragraph.
"""

note_output = """\
<document source="test data">
    <admonition classes="note">
        <title>
            Note
        <paragraph>
            These are the note contents.
        <paragraph>
            Another paragraph.
"""

generic_admonition_input = """\
.. admonition:: Generic

   Admonitions contents...
"""

generic_admonition_output = """\
<document source="test data">
    <admonition classes="admonition-generic admonition">
        <title>
            Generic
        <paragraph>
            Admonitions contents...
"""

if __name__ == '__main__':
    unittest.main()
