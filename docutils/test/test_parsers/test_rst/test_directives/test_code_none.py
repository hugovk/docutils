#! /usr/bin/env python3

# $Id$
# Author: Guenter Milde
# Copyright: This module has been placed in the public domain.

"""
Test the 'code' directive in body.py with syntax_highlight = 'none'.
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
                    settings.syntax_highlight = "none"
                    document = utils.new_document('test data', settings)
                    self.parser.parse(case_input, document)
                    output = document.pformat()
                    DocutilsTestSupport._compare_output(self, case_input, output, case_expected)


totest = {}

totest['code-parsing-none'] = [
["""\
.. code::

   This is a code block.
""",
"""\
<document source="test data">
    <literal_block classes="code" xml:space="preserve">
        This is a code block.
"""],
["""\
.. code:: python
  :number-lines: 7

  def my_function():
      '''Test the lexer.
      '''

      # and now for something completely different
      print(8/2)
""",
"""\
<document source="test data">
    <literal_block classes="code python" xml:space="preserve">
        <inline classes="ln">
             7 \n\
        def my_function():
        <inline classes="ln">
             8 \n\
            \'\'\'Test the lexer.
        <inline classes="ln">
             9 \n\
            \'\'\'
        <inline classes="ln">
            10 \n\
        \n\
        <inline classes="ln">
            11 \n\
            # and now for something completely different
        <inline classes="ln">
            12 \n\
            print(8/2)
"""],
["""\
.. code:: latex

  hello \\emph{world} % emphasize
""",
"""\
<document source="test data">
    <literal_block classes="code latex" xml:space="preserve">
        hello \\emph{world} % emphasize
"""],
]


if __name__ == '__main__':
    unittest.main()
