#! /usr/bin/env python3

# $Id$
# Author: Guenter Milde <milde@users.sf.net>
# Copyright: This module has been placed in the public domain.

"""
Tests for the 'math' directive.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestMaths(unittest.TestCase):
    def test_argument(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(argument_input, document)
        output = document.pformat()
        self.assertEqual(output, argument_output)

    def test_content(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(content_input, document)
        output = document.pformat()
        self.assertEqual(output, content_output)

    def test_options(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(options_input, document)
        output = document.pformat()
        self.assertEqual(output, options_output)

    def test_argument_and_content(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(argument_and_content_input, document)
        output = document.pformat()
        self.assertEqual(output, argument_and_content_output)

    def test_content_with_blank_line(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(content_with_blank_line_input, document)
        output = document.pformat()
        self.assertEqual(output, content_with_blank_line_output)


argument_input = """\
.. math:: y = f(x)
"""

argument_output = """\
<document source="test data">
    <math_block xml:space="preserve">
        y = f(x)
"""


content_input = """\
.. math::

  1+1=2
"""

content_output = """\
<document source="test data">
    <math_block xml:space="preserve">
        1+1=2
"""


options_input = """\
.. math::
  :class: new
  :name: eq:Eulers law

  e^i*2*\\pi = 1
"""

options_output = """\
<document source="test data">
    <math_block classes="new" ids="eq-eulers-law" names="eq:eulers\\ law" xml:space="preserve">
        e^i*2*\\pi = 1
"""


argument_and_content_input = """\
.. math:: y = f(x)

  1+1=2

"""

argument_and_content_output = """\
<document source="test data">
    <math_block xml:space="preserve">
        y = f(x)
    <math_block xml:space="preserve">
        1+1=2
"""


content_with_blank_line_input = """\
.. math::

  1+1=2

  E = mc^2
"""

content_with_blank_line_output = """\
<document source="test data">
    <math_block xml:space="preserve">
        1+1=2
    <math_block xml:space="preserve">
        E = mc^2
"""

if __name__ == '__main__':
    unittest.main()
