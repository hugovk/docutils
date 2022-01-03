#!/usr/bin/env python3
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
    for name, cases in totest.items():
        for casenum, (case_input, case_expected) in enumerate(cases):
            s.addTest(
                DocutilsTestSupport.ParserTestCase("test_parser",
                                                   input=case_input, expected=case_expected,
                                                   id='%s: totest[%r][%s]' % (suite_id, name, casenum),
                                                   suite_settings={'line_length_limit': 80})
            )
    return s

totest = {}

totest['default'] = [
["""\
within the limit
%s
""" % ("x"*80),
"""\
<document source="test data">
    <paragraph>
        within the limit
        %s
""" % ("x"*80)],
["""\
above the limit
%s
""" % ("x"*81),
"""\
<document source="test data">
    <system_message level="3" source="test data" type="ERROR">
        <paragraph>
            Line 2 exceeds the line-length-limit.
"""],
["""\
Include Test
============

.. include:: docutils.conf
   :literal:

A paragraph.
""",
"""\
<document source="test data">
    <section ids="include-test" names="include\\ test">
        <title>
            Include Test
        <system_message level="2" line="4" source="test data" type="WARNING">
            <paragraph>
                "docutils.conf": line 5 exceeds the line-length-limit.
            <literal_block xml:space="preserve">
                .. include:: docutils.conf
                   :literal:
        <paragraph>
            A paragraph.
"""],
]


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
