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

md_parser_class = DocutilsTestSupport.md_parser_class


@unittest.skipUnless(md_parser_class, DocutilsTestSupport.md_skip_msg)
class RecommonmarkParserTestCase(DocutilsTestSupport.CustomTestCase):

    """Test case for 3rd-party CommonMark parsers."""

    if md_parser_class:
        parser = md_parser_class()
        option_parser = frontend.OptionParser(components=(md_parser_class,))
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
]


if __name__ == '__main__':
    unittest.main()
