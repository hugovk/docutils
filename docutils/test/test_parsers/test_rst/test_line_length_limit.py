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

import os
import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst

os.chdir(os.path.normpath(os.path.join(__file__, '..', '..', '..')))


class TestLineLengthLimit(unittest.TestCase):
    def test_within(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        settings.line_length_limit = 80

        document = utils.new_document('test data', settings)
        rst.Parser().parse(within_input, document)
        output = document.pformat()
        self.assertEqual(output, within_output)

    def test_outwith(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        settings.line_length_limit = 80

        document = utils.new_document('test data', settings)
        rst.Parser().parse(outwith_input, document)
        output = document.pformat()
        self.assertEqual(output, outwith_output)

    def test_include(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        settings.line_length_limit = 80

        document = utils.new_document('test data', settings)
        rst.Parser().parse(include_input, document)
        output = document.pformat()
        self.assertEqual(output, include_output)


within_input = f"""\
within the limit
{"x" * 80}
"""

within_output = f"""\
<document source="test data">
    <paragraph>
        within the limit
        {"x" * 80}
"""

outwith_input = f"""\
above the limit
{"x" * 81}
"""

outwith_output = """\
<document source="test data">
    <system_message level="3" source="test data" type="ERROR">
        <paragraph>
            Line 2 exceeds the line-length-limit.
"""

include_input = """\
Include Test
============

.. include:: docutils.conf
   :literal:

A paragraph.
"""

include_output = """\
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
"""

if __name__ == '__main__':
    unittest.main()
