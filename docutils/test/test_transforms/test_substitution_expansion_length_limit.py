#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for docutils.transforms.references.Substitutions.
"""

import unittest
from test import DocutilsTestSupport
from docutils.transforms.references import Substitutions
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
                    settings = self.settings.copy()
                    settings.line_length_limit = 80
                    document = utils.new_document('test data', settings)
                    self.parser.parse(case_input, document)
                    # Don't do a ``populate_from_components()`` because that would
                    # enable the Transformer's default transforms.
                    document.transformer.add_transforms(transforms)
                    document.transformer.add_transform(universal.TestMessages)
                    document.transformer.components['writer'] = self
                    document.transformer.apply_transforms()
                    output = document.pformat()
                    DocutilsTestSupport._compare_output(self, output, case_expected)


# pseudoxml representation of the substitution definition content:
a = '        lol'
b = '        10^1 \n' + '\n         \n'.join(10 * [a])
c = '        10^2 \n' + '\n         \n'.join(10 * [b])

totest = {}

totest['substitutions'] = ((Substitutions,), [
["""\
The billion laughs attack for ReStructuredText:

.. |a| replace:: lol
.. |b| replace:: 10^1 |a| |a| |a| |a| |a| |a| |a| |a| |a| |a|
.. |c| replace:: 10^2 |b| |b| |b| |b| |b| |b| |b| |b| |b| |b|
.. ...

|a| |c| continuation text
""",
"""\
<document source="test data">
    <paragraph>
        The billion laughs attack for ReStructuredText:
    <substitution_definition names="a">
        lol
    <substitution_definition names="b">
{}
    <substitution_definition names="c">
{}
    <comment xml:space="preserve">
        ...
    <paragraph>
        lol
         \n\
        <problematic ids="problematic-1" refid="system-message-1">
            |c|
         continuation text
    <system_message backrefs="problematic-1" ids="system-message-1" level="3" line="9" source="test data" type="ERROR">
        <paragraph>
            Substitution definition "c" exceeds the line-length-limit.
""".format(b, c)],
])


if __name__ == '__main__':
    unittest.main()
