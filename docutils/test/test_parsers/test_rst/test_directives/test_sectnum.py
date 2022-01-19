#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Tests for the 'sectnum' directive.
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

totest['sectnum'] = [
["""\
.. sectnum::
""",
"""\
<document source="test data">
    <pending>
        .. internal attributes:
             .transform: docutils.transforms.parts.SectNum
             .details:
"""],
["""\
.. sectnum::
   :depth: 23
   :start: 42
   :prefix: A Prefix
   :suffix: A Suffix
""",
"""\
<document source="test data">
    <pending>
        .. internal attributes:
             .transform: docutils.transforms.parts.SectNum
             .details:
               depth: 23
               prefix: 'A Prefix'
               start: 42
               suffix: 'A Suffix'
"""],
]


if __name__ == '__main__':
    unittest.main()
