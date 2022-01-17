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

totest['indented_literal_blocks'] = [
["""\
A paragraph::

    A literal block.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
        A literal block.
"""],
["""\
A paragraph with a space after the colons:: \n\

    A literal block.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph with a space after the colons:
    <literal_block xml:space="preserve">
        A literal block.
"""],
["""\
A paragraph::

    A literal block.

Another paragraph::

    Another literal block.
    With two blank lines following.


A final paragraph.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
        A literal block.
    <paragraph>
        Another paragraph:
    <literal_block xml:space="preserve">
        Another literal block.
        With two blank lines following.
    <paragraph>
        A final paragraph.
"""],
["""\
A paragraph
on more than
one line::

    A literal block.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph
        on more than
        one line:
    <literal_block xml:space="preserve">
        A literal block.
"""],
["""\
A paragraph
on more than
one line::
    A literal block
    with no blank line above.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph
        on more than
        one line:
    <system_message level="3" line="4" source="test data" type="ERROR">
        <paragraph>
            Unexpected indentation.
    <literal_block xml:space="preserve">
        A literal block
        with no blank line above.
"""],
["""\
A paragraph::

    A literal block.
no blank line
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
        A literal block.
    <system_message level="2" line="4" source="test data" type="WARNING">
        <paragraph>
            Literal block ends without a blank line; unexpected unindent.
    <paragraph>
        no blank line
"""],
[r"""
A paragraph\\::

    A literal block.

A paragraph\::

    Not a literal block.
""",
r"""<document source="test data">
    <paragraph>
        A paragraph\:
    <literal_block xml:space="preserve">
        A literal block.
    <paragraph>
        A paragraph::
    <block_quote>
        <paragraph>
            Not a literal block.
"""],
[r"""
\\::

    A literal block.

\::

    Not a literal block.
""",
r"""<document source="test data">
    <paragraph>
        \:
    <literal_block xml:space="preserve">
        A literal block.
    <paragraph>
        ::
    <block_quote>
        <paragraph>
            Not a literal block.
"""],
["""\
A paragraph: ::

    A literal block.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
        A literal block.
"""],
["""\
A paragraph:

::

    A literal block.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
        A literal block.
"""],
["""\
A paragraph:
::

    A literal block.
""",
"""\
<document source="test data">
    <system_message level="1" line="2" source="test data" type="INFO">
        <paragraph>
            Possible title underline, too short for the title.
            Treating it as ordinary text because it's so short.
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
        A literal block.
"""],
["""\
A paragraph:

::

    A literal block.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
        A literal block.
"""],
["""\
A paragraph::

Not a literal block.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <system_message level="2" line="3" source="test data" type="WARNING">
        <paragraph>
            Literal block expected; none found.
    <paragraph>
        Not a literal block.
"""],
["""\
A paragraph::

    A wonky literal block.
  Literal line 2.

    Literal line 3.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
          A wonky literal block.
        Literal line 2.
        \n\
          Literal line 3.
"""],
["""\
EOF, even though a literal block is indicated::
""",
"""\
<document source="test data">
    <paragraph>
        EOF, even though a literal block is indicated:
    <system_message level="2" line="2" source="test data" type="WARNING">
        <paragraph>
            Literal block expected; none found.
"""],
]

totest['quoted_literal_blocks'] = [
["""\
A paragraph::

> A literal block.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
        > A literal block.
"""],
["""\
A paragraph::


> A literal block.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
        > A literal block.
"""],
["""\
A paragraph::

> A literal block.
> Line 2.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
        > A literal block.
        > Line 2.
"""],
["""\
A paragraph::

> A literal block.
  Indented line.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
        > A literal block.
    <system_message level="3" line="4" source="test data" type="ERROR">
        <paragraph>
            Unexpected indentation.
    <block_quote>
        <paragraph>
            Indented line.
"""],
["""\
A paragraph::

> A literal block.
Text.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
        > A literal block.
    <system_message level="3" line="4" source="test data" type="ERROR">
        <paragraph>
            Inconsistent literal block quoting.
    <paragraph>
        Text.
"""],
["""\
A paragraph::

> A literal block.
$ Inconsistent line.
""",
"""\
<document source="test data">
    <paragraph>
        A paragraph:
    <literal_block xml:space="preserve">
        > A literal block.
    <system_message level="3" line="4" source="test data" type="ERROR">
        <paragraph>
            Inconsistent literal block quoting.
    <paragraph>
        $ Inconsistent line.
"""],
]


if __name__ == '__main__':
    unittest.main()
