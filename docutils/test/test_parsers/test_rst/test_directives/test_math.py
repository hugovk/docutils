#! /usr/bin/env python3

# $Id$
# Author: Guenter Milde <milde@users.sf.net>
# Copyright: This module has been placed in the public domain.

"""
Tests for the 'math' directive.
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

totest['argument'] = [
["""\
.. math:: y = f(x)
""",
"""\
<document source="test data">
    <math_block xml:space="preserve">
        y = f(x)
"""],
]

totest['content'] = [
["""\
.. math::

  1+1=2
""",
"""\
<document source="test data">
    <math_block xml:space="preserve">
        1+1=2
"""],
]

totest['options'] = [
["""\
.. math::
  :class: new
  :name: eq:Eulers law

  e^i*2*\\pi = 1
""",
"""\
<document source="test data">
    <math_block classes="new" ids="eq-eulers-law" names="eq:eulers\\ law" xml:space="preserve">
        e^i*2*\\pi = 1
"""],
]

totest['argument_and_content'] = [
["""\
.. math:: y = f(x)

  1+1=2

""",
"""\
<document source="test data">
    <math_block xml:space="preserve">
        y = f(x)
    <math_block xml:space="preserve">
        1+1=2
"""],
]

totest['content with blank line'] = [
["""\
.. math::

  1+1=2

  E = mc^2
""",
"""\
<document source="test data">
    <math_block xml:space="preserve">
        1+1=2
    <math_block xml:space="preserve">
        E = mc^2
"""],
]


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
