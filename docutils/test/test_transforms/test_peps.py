#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for docutils.transforms.peps.
"""

import unittest
from test import DocutilsTestSupport
from docutils.transforms.peps import TargetNotes
from docutils.parsers.rst import Parser
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
                    document = utils.new_document('test data', self.settings.copy())
                    self.parser.parse(case_input, document)
                    # Don't do a ``populate_from_components()`` because that would
                    # enable the Transformer's default transforms.
                    document.transformer.add_transforms(transforms)
                    document.transformer.add_transform(universal.TestMessages)
                    document.transformer.components['writer'] = self
                    document.transformer.apply_transforms()
                    output = document.pformat()
                    DocutilsTestSupport._compare_output(self, output, case_expected)


totest = {}

totest['target_notes'] = ((TargetNotes,), [
["""\
No references or targets exist, therefore
no "References" section should be generated.
""",
"""\
<document source="test data">
    <paragraph>
        No references or targets exist, therefore
        no "References" section should be generated.
"""],
["""\
A target exists, here's the reference_.
A "References" section should be generated.

.. _reference: http://www.example.org
""",
"""\
<document source="test data">
    <paragraph>
        A target exists, here's the \n\
        <reference name="reference" refname="reference">
            reference
         \n\
        <footnote_reference auto="1" ids="footnote-reference-1" refname="TARGET_NOTE: footnote-1">
        .
        A "References" section should be generated.
    <target ids="reference" names="reference" refuri="http://www.example.org">
    <section ids="section-1">
        <title>
            References
        <footnote auto="1" ids="footnote-1" names="TARGET_NOTE:\\ footnote-1">
            <paragraph>
                <reference refuri="http://www.example.org">
                    http://www.example.org
"""],
])



if __name__ == '__main__':
    unittest.main()
