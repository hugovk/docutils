#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for states.py.
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
                    DocutilsTestSupport._compare_output(self, case_input, output, case_expected)


totest = {}

totest['comments'] = [
["""\
.. A comment

Paragraph.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment
    <paragraph>
        Paragraph.
"""],
["""\
.. A comment
   block.

Paragraph.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment
        block.
    <paragraph>
        Paragraph.
"""],
["""\
..
   A comment consisting of multiple lines
   starting on the line after the
   explicit markup start.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment consisting of multiple lines
        starting on the line after the
        explicit markup start.
"""],
["""\
.. A comment.
.. Another.

Paragraph.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment.
    <comment xml:space="preserve">
        Another.
    <paragraph>
        Paragraph.
"""],
["""\
.. A comment
no blank line

Paragraph.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment
    <system_message level="2" line="2" source="test data" type="WARNING">
        <paragraph>
            Explicit markup ends without a blank line; unexpected unindent.
    <paragraph>
        no blank line
    <paragraph>
        Paragraph.
"""],
["""\
.. A comment.
.. Another.
no blank line

Paragraph.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment.
    <comment xml:space="preserve">
        Another.
    <system_message level="2" line="3" source="test data" type="WARNING">
        <paragraph>
            Explicit markup ends without a blank line; unexpected unindent.
    <paragraph>
        no blank line
    <paragraph>
        Paragraph.
"""],
["""\
.. A comment::

Paragraph.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment::
    <paragraph>
        Paragraph.
"""],
["""\
..
   comment::

The extra newline before the comment text prevents
the parser from recognizing a directive.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        comment::
    <paragraph>
        The extra newline before the comment text prevents
        the parser from recognizing a directive.
"""],
["""\
..
   _comment: http://example.org

The extra newline before the comment text prevents
the parser from recognizing a hyperlink target.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        _comment: http://example.org
    <paragraph>
        The extra newline before the comment text prevents
        the parser from recognizing a hyperlink target.
"""],
["""\
..
   [comment] Not a citation.

The extra newline before the comment text prevents
the parser from recognizing a citation.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        [comment] Not a citation.
    <paragraph>
        The extra newline before the comment text prevents
        the parser from recognizing a citation.
"""],
["""\
..
   |comment| image:: bogus.png

The extra newline before the comment text prevents
the parser from recognizing a substitution definition.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        |comment| image:: bogus.png
    <paragraph>
        The extra newline before the comment text prevents
        the parser from recognizing a substitution definition.
"""],
["""\
.. Next is an empty comment, which serves to end this comment and
   prevents the following block quote being swallowed up.

..

    A block quote.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        Next is an empty comment, which serves to end this comment and
        prevents the following block quote being swallowed up.
    <comment xml:space="preserve">
    <block_quote>
        <paragraph>
            A block quote.
"""],
["""\
term 1
  definition 1

  .. a comment

term 2
  definition 2
""",
"""\
<document source="test data">
    <definition_list>
        <definition_list_item>
            <term>
                term 1
            <definition>
                <paragraph>
                    definition 1
                <comment xml:space="preserve">
                    a comment
        <definition_list_item>
            <term>
                term 2
            <definition>
                <paragraph>
                    definition 2
"""],
["""\
term 1
  definition 1

.. a comment

term 2
  definition 2
""",
"""\
<document source="test data">
    <definition_list>
        <definition_list_item>
            <term>
                term 1
            <definition>
                <paragraph>
                    definition 1
    <comment xml:space="preserve">
        a comment
    <definition_list>
        <definition_list_item>
            <term>
                term 2
            <definition>
                <paragraph>
                    definition 2
"""],
["""\
+ bullet paragraph 1

  bullet paragraph 2

  .. comment between bullet paragraphs 2 and 3

  bullet paragraph 3
""",
"""\
<document source="test data">
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                bullet paragraph 1
            <paragraph>
                bullet paragraph 2
            <comment xml:space="preserve">
                comment between bullet paragraphs 2 and 3
            <paragraph>
                bullet paragraph 3
"""],
["""\
+ bullet paragraph 1

  .. comment between bullet paragraphs 1 (leader) and 2

  bullet paragraph 2
""",
"""\
<document source="test data">
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                bullet paragraph 1
            <comment xml:space="preserve">
                comment between bullet paragraphs 1 (leader) and 2
            <paragraph>
                bullet paragraph 2
"""],
["""\
+ bullet

  .. trailing comment
""",
"""\
<document source="test data">
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                bullet
            <comment xml:space="preserve">
                trailing comment
"""],
]

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
