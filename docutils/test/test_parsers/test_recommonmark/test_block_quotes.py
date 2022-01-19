#!/usr/bin/env python3
# -*- coding: utf8 -*-
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
Test for block quotes in CommonMark parsers
Cf. the `CommonMark Specification <https://spec.commonmark.org/>`__
"""

import unittest
from test import DocutilsTestSupport

from docutils import frontend
from docutils import utils

md_parser_class = DocutilsTestSupport.md_parser_class


@unittest.skipUnless(md_parser_class, DocutilsTestSupport.md_skip_msg)
class RecommonmarkParserTestCase(DocutilsTestSupport.CustomTestCase):

    """Test case for 3rd-party CommonMark parsers."""

    if md_parser_class:
        parser = md_parser_class()
        option_parser = frontend.OptionParser(components=(md_parser_class,))
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

totest['block_quotes'] = [
["""\
> block quote
> line 2
""",
"""\
<document source="test data">
    <block_quote>
        <paragraph>
            block quote
            line 2
"""],
["""\
Line 1.

  > Indented block quote.
""",
"""\
<document source="test data">
    <paragraph>
        Line 1.
    <block_quote>
        <paragraph>
            Indented block quote.
"""],
["""\
Line 1.
Line 2.
> Block quote, without blank line before.
""",
"""\
<document source="test data">
    <paragraph>
        Line 1.
        Line 2.
    <block_quote>
        <paragraph>
            Block quote, without blank line before.
"""],
["""\
Line 1.
Line 2.

>Block quote,
continuation line
""",
"""\
<document source="test data">
    <paragraph>
        Line 1.
        Line 2.
    <block_quote>
        <paragraph>
            Block quote,
            continuation line
"""],
["""\
Here is a paragraph.

>   >  Nested
>
>   block quotes.
""",
"""\
<document source="test data">
    <paragraph>
        Here is a paragraph.
    <block_quote>
        <block_quote>
            <paragraph>
                Nested
        <paragraph>
            block quotes.
"""],
]


if __name__ == '__main__':
    unittest.main()
