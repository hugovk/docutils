#!/usr/bin/env python3

# $Id: test_pseudoxml.py 8481 2020-01-31 08:17:24Z milde $
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test for pseudo-XML writer.
"""

import unittest
from test import DocutilsTestSupport


def suite():
    # Settings dictionary must not be empty for later changes to work.
    settings = {'expose_internals': []} # default
    suite_id = DocutilsTestSupport.make_id(__file__)
    s = unittest.TestSuite()
    for name, cases in totest.items():
        for casenum, (case_input, case_expected) in enumerate(cases):
            s.addTest(
                DocutilsTestSupport.WriterPublishTestCase("test_publish",
                                                          input=case_input, expected=case_expected,
                                                          id='%s: totest[%r][%s]' % (suite_id, name, casenum),
                                                          suite_settings=settings,
                                                          writer_name="pseudoxml")
            )
    settings['detailed'] = True
    for name, cases in totest_detailed.items():
        for casenum, (case_input, case_expected) in enumerate(cases):
            s.addTest(
                DocutilsTestSupport.WriterPublishTestCase("test_publish",
                                                          input=case_input, expected=case_expected,
                                                          id='%s: totest[%r][%s]' % (suite_id, name, casenum),
                                                          suite_settings=settings,
                                                          writer_name="pseudoxml")
            )
    return s

totest = {}
totest_detailed = {}

totest['basic'] = [
# input
[r"""
This is a paragraph.

----------

This is a paragraph
with \escaped \characters.

A Section
---------

Foo.
""",
# output
"""\
<document source="<string>">
    <paragraph>
        This is a paragraph.
    <transition>
    <paragraph>
        This is a paragraph
        with escaped characters.
    <section ids="a-section" names="a\\ section">
        <title>
            A Section
        <paragraph>
            Foo.
"""]
]

totest_detailed['basic'] = [
# input
[totest['basic'][0][0],
# output
"""\
<document source="<string>">
    <paragraph>
        <#text>
            'This is a paragraph.'
    <transition>
    <paragraph>
        <#text>
            'This is a paragraph\\n'
            'with \\x00escaped \\x00characters.'
    <section ids="a-section" names="a\\ section">
        <title>
            <#text>
                'A Section'
        <paragraph>
            <#text>
                'Foo.'
"""]
]

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
