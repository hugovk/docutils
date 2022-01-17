#! /usr/bin/env python3

# $Id$
# Author: Guenter Milde <milde@users.sf.net>
# Copyright: This module has been placed in the public domain.

"""
Tests for docutils.transforms.universal.StripClassesAndElements.
"""

import unittest
from test import DocutilsTestSupport
from docutils.parsers.rst import Parser
from docutils.transforms.universal import StripClassesAndElements
from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.transforms import universal


class TransformTestCase(DocutilsTestSupport.CustomTestCase):

    """
    Output checker for the transform.

    Should probably be called TransformOutputChecker, but I can deal with
    that later when/if someone comes up with a category of transform test
    cases that have nothing to do with the input and output of the transform.
    """

    option_parser = frontend.OptionParser(components=(rst.Parser,))
    settings = option_parser.get_default_values()
    settings.report_level = 1
    settings.halt_level = 5
    settings.debug = False
    settings.warning_stream = DocutilsTestSupport.DevNull()
    unknown_reference_resolvers = ()
    parser = Parser()

    def test_transforms(self):
        for name, (transforms, cases) in totest.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    settings = self.settings.copy()
                    settings.strip_elements_with_classes = ['spam', 'no-ham']
                    settings.strip_classes = ['spam', 'noise']
                    document = utils.new_document('test data', settings)
                    self.parser.parse(case_input, document)
                    # Don't do a ``populate_from_components()`` because that would
                    # enable the Transformer's default transforms.
                    document.transformer.add_transforms(transforms)
                    document.transformer.add_transform(universal.TestMessages)
                    document.transformer.components['writer'] = self
                    document.transformer.apply_transforms()
                    output = document.pformat()
                    DocutilsTestSupport._compare_output(self, case_input, output, case_expected)


totest = {}

totest['strip_spam'] = ((StripClassesAndElements,), [
["""\
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
""",
"""\
<document source="test data">
    <paragraph>
        not classy
    <paragraph classes="ham">
        this is ham
    <paragraph>
        this is not ham
"""],
])


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
