#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for RFC-2822 headers in PEPs (readers/pep.py).
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
                DocutilsTestSupport.PEPParserTestCase("test_parser",
                                                      input=case_input, expected=case_expected,
                                                      id='%s: totest[%r][%s]' % (suite_id, name, casenum),
                                                      suite_settings={})
            )
    return s

totest = {}

totest['rfc2822'] = [
["""\
Author: Me
Version: 1
Date: 2002-04-23
""",
"""\
<document source="test data">
    <field_list classes="rfc2822">
        <field>
            <field_name>
                Author
            <field_body>
                <paragraph>
                    Me
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2002-04-23
"""],
["""\


Author: Me
Version: 1
Date: 2002-04-23

.. Leading blank lines don't affect RFC-2822 header parsing.
""",
"""\
<document source="test data">
    <field_list classes="rfc2822">
        <field>
            <field_name>
                Author
            <field_body>
                <paragraph>
                    Me
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2002-04-23
    <comment xml:space="preserve">
        Leading blank lines don't affect RFC-2822 header parsing.
"""],
["""\
.. A comment should prevent RFC-2822 header parsing.

Author: Me
Version: 1
Date: 2002-04-23
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment should prevent RFC-2822 header parsing.
    <paragraph>
        Author: Me
        Version: 1
        Date: 2002-04-23
"""],
["""\
Author: Me

Version: 1
Date: 2002-04-23
""",
"""\
<document source="test data">
    <field_list classes="rfc2822">
        <field>
            <field_name>
                Author
            <field_body>
                <paragraph>
                    Me
    <paragraph>
        Version: 1
        Date: 2002-04-23
"""],
["""\
field:
empty item above, no blank line
""",
"""\
<document source="test data">
    <field_list classes="rfc2822">
        <field>
            <field_name>
                field
            <field_body>
    <system_message level="2" line="2" source="test data" type="WARNING">
        <paragraph>
            RFC2822-style field list ends without a blank line; unexpected unindent.
    <paragraph>
        empty item above, no blank line
"""],
["""\
Author:
  Me
Version:
  1
Date:
  2002-04-23
""",
"""\
<document source="test data">
    <field_list classes="rfc2822">
        <field>
            <field_name>
                Author
            <field_body>
                <paragraph>
                    Me
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2002-04-23
"""],
["""\
Authors: Me,
         Myself,
         and I
Version: 1
         or so
Date: 2002-04-23
      (Tuesday)
""",
"""\
<document source="test data">
    <field_list classes="rfc2822">
        <field>
            <field_name>
                Authors
            <field_body>
                <paragraph>
                    Me,
                    Myself,
                    and I
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
                    or so
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2002-04-23
                    (Tuesday)
"""],
["""\
Authors: Me,
  Myself,
  and I
Version: 1
  or so
Date: 2002-04-23
  (Tuesday)
""",
"""\
<document source="test data">
    <field_list classes="rfc2822">
        <field>
            <field_name>
                Authors
            <field_body>
                <paragraph>
                    Me,
                    Myself,
                    and I
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
                    or so
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2002-04-23
                    (Tuesday)
"""],
["""\
Authors: - Me
         - Myself
         - I
Version:
""",
"""\
<document source="test data">
    <field_list classes="rfc2822">
        <field>
            <field_name>
                Authors
            <field_body>
                <bullet_list bullet="-">
                    <list_item>
                        <paragraph>
                            Me
                    <list_item>
                        <paragraph>
                            Myself
                    <list_item>
                        <paragraph>
                            I
        <field>
            <field_name>
                Version
            <field_body>
"""],
["""\
Authors: Me

         Myself and I
Version:
""",
"""\
<document source="test data">
    <field_list classes="rfc2822">
        <field>
            <field_name>
                Authors
            <field_body>
                <paragraph>
                    Me
    <block_quote>
        <paragraph>
            Myself and I
    <system_message level="2" line="4" source="test data" type="WARNING">
        <paragraph>
            Block quote ends without a blank line; unexpected unindent.
    <paragraph>
        Version:
"""],
]

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
