#! /usr/bin/env python3
# $Id$
# :Copyright: © 2020 Günter Milde.
# :License: Released under the terms of the `2-Clause BSD license`_, in short:
#
#    Copying and distribution of this file, with or without modification,
#    are permitted in any medium without royalty provided the copyright
#    notice and this notice are preserved.
#    This file is offered as-is, without any warranty.
#
# .. _2-Clause BSD license: https://opensource.org/licenses/BSD-2-Clause

"""
Tests for inline markup in docutils/parsers/rst/states.py.
Interpreted text tests are in a separate module, test_interpreted.py.
"""

import unittest
from test import DocutilsTestSupport


def suite():
    suite_id = DocutilsTestSupport.make_id(__file__)
    s = unittest.TestSuite()
    if DocutilsTestSupport.recommonmark_ready_for_tests():
        for name, cases in totest.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                s.addTest(
                    DocutilsTestSupport.RecommonmarkParserTestCase("test_parser",
                                                                   input=case_input, expected=case_expected,
                                                                   id='%s: totest[%r][%s]' % (suite_id, name, casenum),
                                                                   suite_settings={})
                )
    return s

totest = {}

totest['default'] = [
["""\
within the limit
%s
""" % ("x"*10000),
"""\
<document source="test data">
    <paragraph>
        within the limit
        %s
""" % ("x"*10000)],
["""\
above the limit
%s
""" % ("x"*10001),
"""\
<document source="test data">
    <system_message level="3" source="test data" type="ERROR">
        <paragraph>
            Line 2 exceeds the line-length-limit.
"""],
]


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
