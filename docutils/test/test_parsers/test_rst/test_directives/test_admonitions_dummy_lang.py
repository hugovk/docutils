#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for admonition directives with local language module.
"""

if __name__ == '__main__':
    import __init__
import unittest
from test_parsers import DocutilsTestSupport

def suite():
    suite_id = DocutilsTestSupport.make_id(__file__)
    s = unittest.TestSuite()
    for name, cases in totest.items():
        for casenum, (case_input, case_expected) in enumerate(cases):
            s.addTest(
                DocutilsTestSupport.ParserTestCase("test_parser",
                                                   input=case_input, expected=case_expected,
                                                   id='%s: totest[%r][%s]' % (suite_id, name, casenum),
                                                   suite_settings={'language_code': 'local-dummy-lang',
                                                                   'report_level': 2}, # warning (has no effect on test output is run as __main__).
                                                   )
            )
    return s

totest = {}

totest['admonitions'] = [
["""\
.. Dummy-Attention:: directive with silly localised name.

.. Attention:: English fallback (an INFO is written).
""",
"""\
<document source="test data">
    <attention>
        <paragraph>
            directive with silly localised name.
    <attention>
        <paragraph>
            English fallback (an INFO is written).
"""],
]


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
