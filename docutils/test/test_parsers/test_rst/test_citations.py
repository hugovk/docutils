#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for states.py.
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
                    document = utils.new_document('test data', self.settings.copy())
                    self.parser.parse(case_input, document)
                    output = document.pformat()
                    DocutilsTestSupport._compare_output(self, output, case_expected)


totest = {}

totest['citations'] = [
["""\
.. [citation] This is a citation.
""",
"""\
<document source="test data">
    <citation ids="citation" names="citation">
        <label>
            citation
        <paragraph>
            This is a citation.
"""],
["""\
.. [citation1234] This is a citation with year.
""",
"""\
<document source="test data">
    <citation ids="citation1234" names="citation1234">
        <label>
            citation1234
        <paragraph>
            This is a citation with year.
"""],
["""\
.. [citation] This is a citation
   on multiple lines.
""",
"""\
<document source="test data">
    <citation ids="citation" names="citation">
        <label>
            citation
        <paragraph>
            This is a citation
            on multiple lines.
"""],
["""\
.. [citation1] This is a citation
     on multiple lines with more space.

.. [citation2] This is a citation
  on multiple lines with less space.
""",
"""\
<document source="test data">
    <citation ids="citation1" names="citation1">
        <label>
            citation1
        <paragraph>
            This is a citation
            on multiple lines with more space.
    <citation ids="citation2" names="citation2">
        <label>
            citation2
        <paragraph>
            This is a citation
            on multiple lines with less space.
"""],
["""\
.. [citation]
   This is a citation on multiple lines
   whose block starts on line 2.
""",
"""\
<document source="test data">
    <citation ids="citation" names="citation">
        <label>
            citation
        <paragraph>
            This is a citation on multiple lines
            whose block starts on line 2.
"""],
["""\
.. [citation]

That was an empty citation.
""",
"""\
<document source="test data">
    <citation ids="citation" names="citation">
        <label>
            citation
    <paragraph>
        That was an empty citation.
"""],
["""\
.. [citation]
No blank line.
""",
"""\
<document source="test data">
    <citation ids="citation" names="citation">
        <label>
            citation
    <system_message level="2" line="2" source="test data" type="WARNING">
        <paragraph>
            Explicit markup ends without a blank line; unexpected unindent.
    <paragraph>
        No blank line.
"""],
["""\
.. [citation label with spaces] this isn't a citation

.. [*citationlabelwithmarkup*] this isn't a citation
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        [citation label with spaces] this isn't a citation
    <comment xml:space="preserve">
        [*citationlabelwithmarkup*] this isn't a citation
"""],
["""
isolated internals : ``.-_``.

.. [citation.withdot] one dot

.. [citation-withdot] one hyphen

.. [citation_withunderscore] one underscore

.. [citation:with:colons] two colons

.. [citation+withplus] one plus
""",
"""<document source="test data">
    <paragraph>
        isolated internals : \n\
        <literal>
            .-_
        .
    <citation ids="citation-withdot" names="citation.withdot">
        <label>
            citation.withdot
        <paragraph>
            one dot
    <citation ids="citation-withdot-1" names="citation-withdot">
        <label>
            citation-withdot
        <paragraph>
            one hyphen
    <citation ids="citation-withunderscore" names="citation_withunderscore">
        <label>
            citation_withunderscore
        <paragraph>
            one underscore
    <citation ids="citation-with-colons" names="citation:with:colons">
        <label>
            citation:with:colons
        <paragraph>
            two colons
    <citation ids="citation-withplus" names="citation+withplus">
        <label>
            citation+withplus
        <paragraph>
            one plus
"""],
]


if __name__ == '__main__':
    unittest.main()
