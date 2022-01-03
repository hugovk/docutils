#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for states.py.
"""

if __name__ == '__main__':
    import __init__
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
                                     suite_settings={})
            )
    return s

totest = {}

totest['bullet_lists'] = [
["""\
- item
""",
"""\
<document source="test data">
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item
"""],
["""\
* item 1

* item 2
""",
"""\
<document source="test data">
    <bullet_list bullet="*">
        <list_item>
            <paragraph>
                item 1
        <list_item>
            <paragraph>
                item 2
"""],
["""\
No blank line between:

+ item 1
+ item 2
""",
"""\
<document source="test data">
    <paragraph>
        No blank line between:
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                item 1
        <list_item>
            <paragraph>
                item 2
"""],
["""\
- item 1, para 1.

  item 1, para 2.

- item 2
""",
"""\
<document source="test data">
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item 1, para 1.
            <paragraph>
                item 1, para 2.
        <list_item>
            <paragraph>
                item 2
"""],
["""\
- item 1, line 1
  item 1, line 2
- item 2
""",
"""\
<document source="test data">
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item 1, line 1
                item 1, line 2
        <list_item>
            <paragraph>
                item 2
"""],
["""\
Different bullets:

- item 1

+ item 1

* item 1
- item 1
""",
"""\
<document source="test data">
    <paragraph>
        Different bullets:
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item 1
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                item 1
    <bullet_list bullet="*">
        <list_item>
            <paragraph>
                item 1
    <system_message level="2" line="8" source="test data" type="WARNING">
        <paragraph>
            Bullet list ends without a blank line; unexpected unindent.
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item 1
"""],
["""\
- item
no blank line
""",
"""\
<document source="test data">
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item
    <system_message level="2" line="2" source="test data" type="WARNING">
        <paragraph>
            Bullet list ends without a blank line; unexpected unindent.
    <paragraph>
        no blank line
"""],
["""\
-

empty item above
""",
"""\
<document source="test data">
    <bullet_list bullet="-">
        <list_item>
    <paragraph>
        empty item above
"""],
["""\
-
empty item above, no blank line
""",
"""\
<document source="test data">
    <bullet_list bullet="-">
        <list_item>
    <system_message level="2" line="2" source="test data" type="WARNING">
        <paragraph>
            Bullet list ends without a blank line; unexpected unindent.
    <paragraph>
        empty item above, no blank line
"""],
["""\
Unicode bullets:

\u2022 BULLET

\u2023 TRIANGULAR BULLET

\u2043 HYPHEN BULLET
""",
"""\
<document source="test data">
    <paragraph>
        Unicode bullets:
    <bullet_list bullet="\u2022">
        <list_item>
            <paragraph>
                BULLET
    <bullet_list bullet="\u2023">
        <list_item>
            <paragraph>
                TRIANGULAR BULLET
    <bullet_list bullet="\u2043">
        <list_item>
            <paragraph>
                HYPHEN BULLET
"""],
]

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
