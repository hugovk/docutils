#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for html meta directives.
"""

import unittest
from test import DocutilsTestSupport


def suite():
    suite_id = DocutilsTestSupport.make_id(__file__)
    s = unittest.TestSuite()
    for name, cases in totest.items():
        for casenum, (case_input, case_expected) in enumerate(cases):
            s.addTest(
                DocutilsTestSupport.ParserTestCase("test_parser",
                                     input=case_input, expected=case_expected,
                                     id='%s: totest[%r][%s]' % (suite_id, name, casenum),
                                     suite_settings={})
            )
    return s

totest = {}

totest['meta'] = [
["""\
.. meta::
   :description: The reStructuredText plaintext markup language
   :keywords: plaintext,markup language
""",
"""\
<document source="test data">
    <meta content="The reStructuredText plaintext markup language" name="description">
    <meta content="plaintext,markup language" name="keywords">
"""],
["""\
.. meta::
   :description lang=en: An amusing story
   :description lang=fr: Un histoire amusant
""",
"""\
<document source="test data">
    <meta content="An amusing story" lang="en" name="description">
    <meta content="Un histoire amusant" lang="fr" name="description">
"""],
["""\
.. meta::
   :http-equiv=Content-Type: text/html; charset=ISO-8859-1
""",
"""\
<document source="test data">
    <meta content="text/html; charset=ISO-8859-1" http-equiv="Content-Type">
"""],
["""\
.. meta::
   :name: content
     over multiple lines
""",
"""\
<document source="test data">
    <meta content="content over multiple lines" name="name">
"""],
["""\
Paragraph

.. meta::
   :name: content
""",
"""\
<document source="test data">
    <meta content="content" name="name">
    <paragraph>
        Paragraph
"""],
["""\
.. meta::
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Content block expected for the "meta" directive; none found.
        <literal_block xml:space="preserve">
            .. meta::
"""],
["""\
.. meta::
   :empty:
""",
"""\
<document source="test data">
    <system_message level="1" line="2" source="test data" type="INFO">
        <paragraph>
            No content for meta tag "empty".
        <literal_block xml:space="preserve">
            :empty:
"""],
["""\
.. meta::
   not a field list
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Invalid meta directive.
        <literal_block xml:space="preserve">
            .. meta::
               not a field list
"""],
["""\
.. meta::
   :name: content
   not a field
   :name: content
""",
"""\
<document source="test data">
    <meta content="content" name="name">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Invalid meta directive.
        <literal_block xml:space="preserve">
            .. meta::
               :name: content
               not a field
               :name: content
"""],
["""\
.. meta::
   :name: content
   :name: content
   not a field
""",
"""\
<document source="test data">
    <meta content="content" name="name">
    <meta content="content" name="name">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Invalid meta directive.
        <literal_block xml:space="preserve">
            .. meta::
               :name: content
               :name: content
               not a field
"""],
["""\
.. meta::
   :name notattval: content
""",
"""\
<document source="test data">
    <system_message level="3" line="2" source="test data" type="ERROR">
        <paragraph>
            Error parsing meta tag attribute "notattval": missing "=".
        <literal_block xml:space="preserve">
            :name notattval: content
"""],
[r"""
.. meta::
   :name\:with\:colons: escaped line\
                        break
   :unescaped:embedded:colons: content
""",
"""\
<document source="test data">
    <meta content="escaped linebreak" name="name:with:colons">
    <meta content="content" name="unescaped:embedded:colons">
"""],
]


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
