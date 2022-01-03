#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Tests for the block quote directives "epigraph", "highlights", and
"pull-quote".
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
                                     suite_settings={})
            )
    return s

generic_tests = [
["""\
.. %(type)s::

   This is a block quote.

   -- Attribution

   This is another block quote.

   -- Another Attribution,
      Second Line
""",
"""\
<document source="test data">
    <block_quote classes="%(type)s">
        <paragraph>
            This is a block quote.
        <attribution>
            Attribution
    <block_quote classes="%(type)s">
        <paragraph>
            This is another block quote.
        <attribution>
            Another Attribution,
            Second Line
"""],
# TODO: Add class option.
["""\
.. %(type)s::
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Content block expected for the "%(type)s" directive; none found.
        <literal_block xml:space="preserve">
            .. %(type)s::
"""],
]

totest = {}
for block_quote_type in ('epigraph', 'highlights', 'pull-quote'):
    totest[block_quote_type] = [
        [text % {'type': block_quote_type} for text in pair]
        for pair in generic_tests]


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
