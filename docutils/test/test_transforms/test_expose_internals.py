#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test module for universal.ExposeInternals transform.
"""

if __name__ == '__main__':
    import __init__
from test_transforms import DocutilsTestSupport # before importing docutils!
from docutils.transforms.universal import ExposeInternals
from docutils.parsers.rst import Parser


def suite():
    parser = Parser()
    s = DocutilsTestSupport.CustomTestSuite(suite_id=__file__)
    for name, (transforms, cases) in totest.items():
        for casenum, (case_input, case_expected) in enumerate(cases):
            s.addTest(
                DocutilsTestSupport.TransformTestCase("test_transforms",
                                                      input=case_input, expected=case_expected,
                                                      id='%s: totest[%r][%s]' % (s.id, name, casenum),
                                                      suite_settings={'expose_internals': ['rawsource', 'source']},
                                                      transforms=transforms, parser=parser)
            )
    return s


totest = {}

totest['transitions'] = ((ExposeInternals,), [
["""\
This is a test.
""",
"""\
<document internal:rawsource="" source="test data">
    <paragraph internal:rawsource="This is a test." internal:source="test data">
        This is a test.
"""],
])


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
