#!/usr/bin/env python3

# $Id: test_pseudoxml.py 8481 2020-01-31 08:17:24Z milde $
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test for pseudo-XML writer.
"""

import unittest

import docutils
import docutils.core


class TestPseudoXML(unittest.TestCase, docutils.SettingsSpec):
    """
    Test case for publish.
    """

    settings_default_overrides = {'_disable_config': True,
                                  'strict_visitor': True}

    def test_publish(self):
        output = docutils.core.publish_string(
            source=basic_input, reader_name="standalone",
            parser_name="restructuredtext", writer_name='pseudoxml',
            settings_spec=self, settings_overrides={})
        self.assertEqual(output, basic_output)

    def test_publish_detailed(self):
        output = docutils.core.publish_string(
            source=basic_input, reader_name="standalone",
            parser_name="restructuredtext", writer_name='pseudoxml',
            settings_spec=self, settings_overrides={'detailed': True})
        self.assertEqual(output, basic_output_detailed)


basic_input = r"""
This is a paragraph.

----------

This is a paragraph
with \escaped \characters.

A Section
---------

Foo.
"""

basic_output = """\
<document source="<string>">
    <paragraph>
        This is a paragraph.
    <transition>
    <paragraph>
        This is a paragraph
        with escaped characters.
    <section ids="a-section" names="a\\ section">
        <title>
            A Section
        <paragraph>
            Foo.
"""

basic_output_detailed = """\
<document source="<string>">
    <paragraph>
        <#text>
            'This is a paragraph.'
    <transition>
    <paragraph>
        <#text>
            'This is a paragraph\\n'
            'with \\x00escaped \\x00characters.'
    <section ids="a-section" names="a\\ section">
        <title>
            <#text>
                'A Section'
        <paragraph>
            <#text>
                'Foo.'
"""

if __name__ == '__main__':
    unittest.main()
