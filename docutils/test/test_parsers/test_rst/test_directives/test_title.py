#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Tests for the 'title' directive.
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

totest['title'] = [
["""\
.. title:: This is the document title.
""",
"""\
<document source="test data" title="This is the document title.">
"""],
]


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
