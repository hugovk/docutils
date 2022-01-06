#!/usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test for Null writer.
"""

import unittest
from test import DocutilsTestSupport


class WriterPublishTestCase(DocutilsTestSupport.WriterPublishTestCase):
    writer_name = "null"

    def test_publish(self):
        for name, cases in totest.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    super()._support_publish(input=case_input, expected=case_expected)


totest = {}

totest['basic'] = [
["""\
This is a paragraph.
""",
None]
]

if __name__ == '__main__':
    unittest.main()
