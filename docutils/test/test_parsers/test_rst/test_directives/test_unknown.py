#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for unknown directives.
"""

if __name__ == '__main__':
    import __init__
from test_parsers import DocutilsTestSupport


def suite():
    s = DocutilsTestSupport.CustomTestSuite(suite_id=__file__)
    for name, cases in totest.items():
        for casenum, (case_input, case_expected) in enumerate(cases):
            s.addTest(
                DocutilsTestSupport.ParserTestCase("test_parser",
                                     input=case_input, expected=case_expected,
                                     id='%s: totest[%r][%s]' % (s.id, name, casenum),
                                     suite_settings={})
            )
    return s

totest = {}

totest['unknown'] = [
["""\
.. reStructuredText-unknown-directive::

.. reStructuredText-unknown-directive:: argument

.. reStructuredText-unknown-directive::
   block
""",
"""\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            No directive entry for "reStructuredText-unknown-directive" in module "docutils.parsers.rst.languages.en".
            Trying "reStructuredText-unknown-directive" as canonical directive name.
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Unknown directive type "reStructuredText-unknown-directive".
        <literal_block xml:space="preserve">
            .. reStructuredText-unknown-directive::
    <system_message level="1" line="3" source="test data" type="INFO">
        <paragraph>
            No directive entry for "reStructuredText-unknown-directive" in module "docutils.parsers.rst.languages.en".
            Trying "reStructuredText-unknown-directive" as canonical directive name.
    <system_message level="3" line="3" source="test data" type="ERROR">
        <paragraph>
            Unknown directive type "reStructuredText-unknown-directive".
        <literal_block xml:space="preserve">
            .. reStructuredText-unknown-directive:: argument
    <system_message level="1" line="5" source="test data" type="INFO">
        <paragraph>
            No directive entry for "reStructuredText-unknown-directive" in module "docutils.parsers.rst.languages.en".
            Trying "reStructuredText-unknown-directive" as canonical directive name.
    <system_message level="3" line="5" source="test data" type="ERROR">
        <paragraph>
            Unknown directive type "reStructuredText-unknown-directive".
        <literal_block xml:space="preserve">
            .. reStructuredText-unknown-directive::
               block
"""],
]


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
