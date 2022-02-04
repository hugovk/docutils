#! /usr/bin/env python3

# $Id$
# Author: Guenter Milde <milde@users.sf.net>
# Copyright: This module has been placed in the public domain.

"""
Tests for docutils.transforms.universal.StripClassesAndElements.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.transforms import universal
from docutils.transforms.universal import StripClassesAndElements


class TestTransformStripClassesAndElements(unittest.TestCase):
    def test_transforms(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        settings.strip_elements_with_classes = ['spam', 'no-ham']
        settings.strip_classes = ['spam', 'noise']
        document = utils.new_document('test data', settings)
        rst.Parser().parse(strip_spam_input, document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transform(StripClassesAndElements)
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()

        output = document.pformat()
        self.assertEqual(output, strip_spam_expected)


strip_spam_input = """\
not classy

.. class:: spam

this is spam

.. class:: ham noise

this is ham

.. code::
   :class: spam
   \n\
   print("spam")
   \n\
.. image:: spam.jpg
   :class: spam

this is not ham
"""

strip_spam_expected = """\
<document source="test data">
    <paragraph>
        not classy
    <paragraph classes="ham">
        this is ham
    <paragraph>
        this is not ham
"""


if __name__ == '__main__':
    unittest.main()
