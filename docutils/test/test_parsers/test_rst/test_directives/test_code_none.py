#! /usr/bin/env python3

# $Id$
# Author: Guenter Milde
# Copyright: This module has been placed in the public domain.

"""
Test the 'code' directive in body.py with syntax_highlight = 'none'.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestCodeParsingNone(unittest.TestCase):
    def test_code_parsing_none(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        settings.syntax_highlight = 'none'
        parser = rst.Parser()

        for casenum, (case_input, case_expected) in enumerate(code_parsing_none):
            with self.subTest(id=f'code_parsing_none[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)


code_parsing_none = [
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
