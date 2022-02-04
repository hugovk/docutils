#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for docutils.transforms.universal.StripComments.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.transforms import universal
from docutils.transforms.universal import StripComments


class TestTransformStripComments(unittest.TestCase):
    def test_strip_comments(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        settings.strip_comments = True
        document = utils.new_document('test data', settings)
        rst.Parser().parse(strip_comments_input, document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transform(StripComments)
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()

        output = document.pformat()
        self.assertEqual(output, strip_comments_expected)


strip_comments_input = """\
.. this is a comment

Title
=====

Paragraph.

.. second comment
"""

strip_comments_expected = """\
<document source="test data">
    <section ids="title" names="title">
        <title>
            Title
        <paragraph>
            Paragraph.
"""

if __name__ == '__main__':
    unittest.main()
