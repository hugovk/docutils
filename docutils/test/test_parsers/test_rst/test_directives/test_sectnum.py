#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Tests for the 'sectnum' directive.
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

totest['sectnum'] = [
["""\
.. sectnum::
""",
"""\
<document source="test data">
    <pending>
        .. internal attributes:
             .transform: docutils.transforms.parts.SectNum
             .details:
"""],
["""\
.. sectnum::
   :depth: 23
   :start: 42
   :prefix: A Prefix
   :suffix: A Suffix
""",
"""\
<document source="test data">
    <pending>
        .. internal attributes:
             .transform: docutils.transforms.parts.SectNum
             .details:
               depth: 23
               prefix: 'A Prefix'
               start: 42
               suffix: 'A Suffix'
"""],
]


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
