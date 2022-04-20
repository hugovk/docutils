#! /usr/bin/env python3

# $Id$
# Author: Guenter Milde
# Copyright: This module has been placed in the public domain.

"""
Test the 'code' directive in body.py with syntax_highlight = 'long'.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestCodeLong(unittest.TestCase):
    def test_code_parsing_long_number_lines(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        settings.syntax_highlight = "long"

        document = utils.new_document('test data', settings)
        rst.Parser().parse(number_lines_input, document)
        output = document.pformat()
        self.assertEqual(output, number_lines_output)

    def test_code_parsing_long(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        settings.syntax_highlight = "long"

        document = utils.new_document('test data', settings)
        rst.Parser().parse(latex_input, document)
        output = document.pformat()
        self.assertEqual(output, latex_output)


number_lines_input = """\
.. code:: python3
  :number-lines: 7

  def my_function():
      '''Test the lexer.
      '''

      # and now for something completely different
      print(8/2)
"""

number_lines_output = """\
<document source="test data">
    <literal_block classes="code python3" xml:space="preserve">
        <inline classes="ln">
             7 \n\
        <inline classes="keyword">
            def
         \n\
        <inline classes="name function">
            my_function
        <inline classes="punctuation">
            ():
        \n\
        <inline classes="ln">
             8 \n\
            \n\
        <inline classes="literal string doc">
            \'\'\'Test the lexer.
        <inline classes="ln">
             9 \n\
        <inline classes="literal string doc">
                \'\'\'
        \n\
        <inline classes="ln">
            10 \n\
        \n\
        <inline classes="ln">
            11 \n\
            \n\
        <inline classes="comment single">
            # and now for something completely different
        \n\
        <inline classes="ln">
            12 \n\
            \n\
        <inline classes="name builtin">
            print
        <inline classes="punctuation">
            (
        <inline classes="literal number integer">
            8
        <inline classes="operator">
            /
        <inline classes="literal number integer">
            2
        <inline classes="punctuation">
            )
"""


latex_input = """\
.. code:: latex

  hello \\emph{world} % emphasize
"""

latex_output = """\
<document source="test data">
    <literal_block classes="code latex" xml:space="preserve">
        hello \n\
        <inline classes="keyword">
            \\emph
        <inline classes="name builtin">
            {
        world
        <inline classes="name builtin">
            }
         \n\
        <inline classes="comment">
            % emphasize
"""

if __name__ == '__main__':
    unittest.main()
