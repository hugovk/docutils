#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Tests for the 'class' directive.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestClass(unittest.TestCase):
    def test_class_only(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(class_only_input, document)
        output = document.pformat()
        self.assertEqual(output, class_only_output)

    def test_class_with_body(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(class_body_input, document)
        output = document.pformat()
        self.assertEqual(output, class_body_output)


class_only_input = """\
.. class:: class1  class2
"""

class_only_output = """\
<document source="test data">
    <pending>
        .. internal attributes:
             .transform: docutils.transforms.misc.ClassAttribute
             .details:
               class: ['class1', 'class2']
               directive: 'class'
"""

class_body_input = """\
.. class:: class1  class2

   The classes are applied to this paragraph.

   And this one.
"""

class_body_output = """\
<document source="test data">
    <paragraph classes="class1 class2">
        The classes are applied to this paragraph.
    <paragraph classes="class1 class2">
        And this one.
"""

if __name__ == '__main__':
    unittest.main()
