#! /usr/bin/env python3

# $Id: test_interpreted.py 6424 2010-09-18 10:43:52Z smerten $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for interpreted text in docutils/parsers/rst/states.py.
Test not default/fallback language french.
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
                                                   suite_settings={'language_code':'fr'})
            )
    return s

totest = {}

totest['basics'] = [
["""\
Simple explicit roles and english fallbacks:
:acronym:`acronym`,
:exp:`superscript`,
:ind:`subscript`,
:titre:`title reference`.
""",
"""\
<document source="test data">
    <paragraph>
        Simple explicit roles and english fallbacks:
        <acronym>
            acronym
        ,
        <superscript>
            superscript
        ,
        <subscript>
            subscript
        ,
        <title_reference>
            title reference
        .
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            No role entry for "acronym" in module "docutils.parsers.rst.languages.fr".
            Using English fallback for role "acronym".
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
