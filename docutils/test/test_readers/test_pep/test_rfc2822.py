#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for RFC-2822 headers in PEPs (readers/pep.py).
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.readers import pep


class TestPEPReaderRFC2822(unittest.TestCase):
    def test_rfc2822(self):
        parser = rst.Parser(rfc2822=True, inliner=rst.states.Inliner())

        settings = frontend.get_default_settings(rst.Parser, pep.Reader)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        for casenum, (case_input, case_expected) in enumerate(rfc2822):
            with self.subTest(id=f'rfc2822[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                self.assertEqual(document.pformat(), case_expected)


rfc2822 = [
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
    unittest.main()
