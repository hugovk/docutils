#!/usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test for Null writer.
"""

if __name__ == '__main__':
    import __init__
from test_writers import DocutilsTestSupport


def suite():
    s = DocutilsTestSupport.CustomTestSuite(suite_id=__file__)
    for name, cases in totest.items():
        for casenum, (case_input, case_expected) in enumerate(cases):
            s.addTest(
                DocutilsTestSupport.WriterPublishTestCase("test_publish",
                                                          input=case_input, expected=case_expected,
                                                          id='%s: totest[%r][%s]' % (s.id, name, casenum),
                                                          suite_settings={},
                                                          writer_name="null")
            )
    return s

totest = {}

totest['basic'] = [
["""\
This is a paragraph.
""",
None]
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
