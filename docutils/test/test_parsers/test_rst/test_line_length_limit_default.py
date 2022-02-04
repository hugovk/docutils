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

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestDefaultLineLengthLimit(unittest.TestCase):
    def test_within_default_line_length(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(within_default_input, document)
        output = document.pformat()
        self.assertEqual(output, within_default_output)

    def test_outwith_default_line_length(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse(outwith_default_input, document)
        output = document.pformat()
        self.assertEqual(output, outwith_default_output)


within_default_input = f"""\
within the limit
{"x" * 10_000}
"""

within_default_output= f"""\
<document source="test data">
    <paragraph>
        within the limit
        {"x" * 10_000}
"""

outwith_default_input = f"""\
above the limit
{"x" * 10_001}
"""

outwith_default_output = """\
<document source="test data">
    <system_message level="3" source="test data" type="ERROR">
        <paragraph>
            Line 2 exceeds the line-length-limit.
"""

if __name__ == '__main__':
    unittest.main()
