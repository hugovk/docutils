#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for parts.py contents directive.
"""

import unittest
from test import DocutilsTestSupport

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class ParserTestCase(DocutilsTestSupport.CustomTestCase):

    """
    Output checker for the parser.

    Should probably be called ParserOutputChecker, but I can deal with
    that later when/if someone comes up with a category of parser test
    cases that have nothing to do with the input and output of the parser.
    """

    parser = rst.Parser()
    """Parser shared by all ParserTestCases."""

    option_parser = frontend.OptionParser(components=(rst.Parser,))
    settings = option_parser.get_default_values()
    settings.report_level = 5
    settings.halt_level = 5
    settings.debug = False

    def test_parser(self):
        for name, cases in totest.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    document = utils.new_document('test data', self.settings.copy())
                    self.parser.parse(case_input, document)
                    output = document.pformat()
                    DocutilsTestSupport._compare_output(self, output, case_expected)


totest = {}

totest['contents'] = [
["""\
.. contents::
""",
"""\
<document source="test data">
    <topic classes="contents" ids="contents" names="contents">
        <title>
            Contents
        <pending>
            .. internal attributes:
                 .transform: docutils.transforms.parts.Contents
                 .details:
"""],
["""\
.. contents:: Table of Contents
""",
"""\
<document source="test data">
    <topic classes="contents" ids="table-of-contents" names="table\\ of\\ contents">
        <title>
            Table of Contents
        <pending>
            .. internal attributes:
                 .transform: docutils.transforms.parts.Contents
                 .details:
"""],
["""\
.. contents::
   Table of Contents
""",
"""\
<document source="test data">
    <topic classes="contents" ids="table-of-contents" names="table\\ of\\ contents">
        <title>
            Table of Contents
        <pending>
            .. internal attributes:
                 .transform: docutils.transforms.parts.Contents
                 .details:
"""],
["""\
.. contents:: Table
   of
   Contents
""",
"""\
<document source="test data">
    <topic classes="contents" ids="table-of-contents" names="table\\ of\\ contents">
        <title>
            Table
            of
            Contents
        <pending>
            .. internal attributes:
                 .transform: docutils.transforms.parts.Contents
                 .details:
"""],
["""\
.. contents:: *Table* of ``Contents``
""",
"""\
<document source="test data">
    <topic classes="contents" ids="table-of-contents" names="table\\ of\\ contents">
        <title>
            <emphasis>
                Table
             of \n\
            <literal>
                Contents
        <pending>
            .. internal attributes:
                 .transform: docutils.transforms.parts.Contents
                 .details:
"""],
["""\
.. contents::
   :depth: 2
   :local:
""",
"""\
<document source="test data">
    <topic classes="contents local" ids="contents" names="contents">
        <pending>
            .. internal attributes:
                 .transform: docutils.transforms.parts.Contents
                 .details:
                   depth: 2
                   local: None
"""],
["""\
.. contents::
   :local: arg
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Error in "contents" directive:
            invalid option value: (option: "local"; value: 'arg')
            no argument is allowed; "arg" supplied.
        <literal_block xml:space="preserve">
            .. contents::
               :local: arg
"""],
["""\
.. contents:: Table of Contents
   :local:
   :depth: 2
   :backlinks: none
""",
"""\
<document source="test data">
    <topic classes="contents local" ids="table-of-contents" names="table\\ of\\ contents">
        <title>
            Table of Contents
        <pending>
            .. internal attributes:
                 .transform: docutils.transforms.parts.Contents
                 .details:
                   backlinks: None
                   depth: 2
                   local: None
"""],
["""\
.. contents::
   :depth: two
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Error in "contents" directive:
            invalid option value: (option: "depth"; value: 'two')
            %s.
        <literal_block xml:space="preserve">
            .. contents::
               :depth: two
""" % DocutilsTestSupport.exception_data(int, "two")[1][0]],
["""\
.. contents::
   :width: 2
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Error in "contents" directive:
            unknown option: "width".
        <literal_block xml:space="preserve">
            .. contents::
               :width: 2
"""],
["""\
.. contents::
   :backlinks: no way!
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Error in "contents" directive:
            invalid option value: (option: "backlinks"; value: 'no way!')
            "no way!" unknown; choose from "top", "entry", or "none".
        <literal_block xml:space="preserve">
            .. contents::
               :backlinks: no way!
"""],
["""\
.. contents::
   :backlinks:
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Error in "contents" directive:
            invalid option value: (option: "backlinks"; value: None)
            must supply an argument; choose from "top", "entry", or "none".
        <literal_block xml:space="preserve">
            .. contents::
               :backlinks:
"""],
["""\
* .. contents::
""",
"""\
<document source="test data">
    <bullet_list bullet="*">
        <list_item>
            <system_message level="3" line="1" source="test data" type="ERROR">
                <paragraph>
                    The "contents" directive may not be used within topics or body elements.
                <literal_block xml:space="preserve">
                    .. contents::
"""],
["""\
.. sidebar:: containing contents

   .. contents::
""",
"""\
<document source="test data">
    <sidebar>
        <title>
            containing contents
        <topic classes="contents" ids="contents" names="contents">
            <title>
                Contents
            <pending>
                .. internal attributes:
                     .transform: docutils.transforms.parts.Contents
                     .details:
"""],
]


if __name__ == '__main__':
    unittest.main()
