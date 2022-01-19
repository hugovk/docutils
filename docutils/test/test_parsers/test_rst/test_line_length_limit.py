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
                    settings = self.settings.copy()
                    settings.line_length_limit = 80
                    document = utils.new_document('test data', settings)
                    self.parser.parse(case_input, document)
                    output = document.pformat()
                    DocutilsTestSupport._compare_output(self, output, case_expected)


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
    unittest.main()
