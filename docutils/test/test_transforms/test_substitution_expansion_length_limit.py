#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for docutils.transforms.references.Substitutions.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.transforms import universal
from docutils.transforms.references import Substitutions


class TestTransformSubstitutionLimit(unittest.TestCase):
    def test_laughs(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        settings.line_length_limit = 80
        document = utils.new_document('test data', settings)
        rst.Parser().parse(substitutions_input, document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transform(Substitutions)
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()

        output = document.pformat()
        self.assertEqual(output, substitutions_expected)


# pseudoxml representation of the substitution definition content:
a = '        lol'
b = '        10^1 \n' + '\n         \n'.join(10 * [a])
c = '        10^2 \n' + '\n         \n'.join(10 * [b])

substitutions_input = """\
The billion laughs attack for ReStructuredText:

.. |a| replace:: lol
.. |b| replace:: 10^1 |a| |a| |a| |a| |a| |a| |a| |a| |a| |a|
.. |c| replace:: 10^2 |b| |b| |b| |b| |b| |b| |b| |b| |b| |b|
.. ...

|a| |c| continuation text
"""

substitutions_expected = f"""\
<document source="test data">
    <paragraph>
        The billion laughs attack for ReStructuredText:
    <substitution_definition names="a">
        lol
    <substitution_definition names="b">
{b}
    <substitution_definition names="c">
{c}
    <comment xml:space="preserve">
        ...
    <paragraph>
        lol
         
        <problematic ids="problematic-1" refid="system-message-1">
            |c|
         continuation text
    <system_message backrefs="problematic-1" ids="system-message-1" level="3" line="9" source="test data" type="ERROR">
        <paragraph>
            Substitution definition "c" exceeds the line-length-limit.
"""

if __name__ == '__main__':
    unittest.main()
