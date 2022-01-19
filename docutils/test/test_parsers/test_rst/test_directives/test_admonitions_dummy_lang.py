#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for admonition directives with local language module.
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
                    settings.language_code = "local-dummy-lang"
                    settings.report_level = 2  # warning (has no effect on test output is run as __main__).
                    document = utils.new_document('test data', settings)
                    self.parser.parse(case_input, document)
                    output = document.pformat()
                    DocutilsTestSupport._compare_output(self, output, case_expected)


totest = {}

totest['admonitions'] = [
["""\
.. Dummy-Attention:: directive with silly localised name.

.. Attention:: English fallback (an INFO is written).
""",
"""\
<document source="test data">
    <attention>
        <paragraph>
            directive with silly localised name.
    <attention>
        <paragraph>
            English fallback (an INFO is written).
"""],
]


if __name__ == '__main__':
    unittest.main()
