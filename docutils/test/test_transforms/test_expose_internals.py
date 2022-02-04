#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test module for universal.ExposeInternals transform.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.transforms import universal
from docutils.transforms.universal import ExposeInternals


class TestTransformExposeInternals(unittest.TestCase):
    def test_expose_internals(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        settings.expose_internals = ['rawsource', 'source']
        document = utils.new_document('test data', settings)
        rst.Parser().parse("This is a test.", document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transform(ExposeInternals)
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()
        output = document.pformat()
        self.assertEqual(output, transitions_expected)


transitions_expected = """\
<document internal:rawsource="" source="test data">
    <paragraph internal:rawsource="This is a test." internal:source="test data">
        This is a test.
"""


if __name__ == '__main__':
    unittest.main()
