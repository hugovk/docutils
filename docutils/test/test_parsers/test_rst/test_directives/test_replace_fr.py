#! /usr/bin/env python3

# $Id: test_replace.py 4667 2006-07-12 21:40:56Z wiemann $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for misc.py "replace" directive.
Test in french (not default/fallback language).
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
                    settings.language_code = "fr"
                    document = utils.new_document('test data', settings)
                    self.parser.parse(case_input, document)
                    output = document.pformat()
                    DocutilsTestSupport._compare_output(self, case_input, output, case_expected)


totest = {}

totest['replace'] = [
["""\
Test directive containing french role exposant (superscript).

.. |Na+| remplace:: Na\\ :exp:`+`

Le |Na+| est l'ion sodium.
""",
"""\
<document source="test data">
    <paragraph>
        Test directive containing french role exposant (superscript).
    <substitution_definition names="Na+">
        Na
        <superscript>
            +
    <paragraph>
        Le \n\
        <substitution_reference refname="Na+">
            Na+
         est l\'ion sodium.
"""],
["""\
Test directive containing english role superscript.

.. |Na+| remplace:: Na\\ :sup:`+`

Le |Na+| est l'ion sodium.
""",
"""\
<document source="test data">
    <paragraph>
        Test directive containing english role superscript.
    <system_message level="1" line="3" source="test data" type="INFO">
        <paragraph>
            No role entry for "sup" in module "docutils.parsers.rst.languages.fr".
            Using English fallback for role "sup".
    <substitution_definition names="Na+">
        Na
        <superscript>
            +
    <paragraph>
        Le \n\
        <substitution_reference refname="Na+">
            Na+
         est l\'ion sodium."""],
]


if __name__ == '__main__':
    unittest.main()
