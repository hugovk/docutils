#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for inline markup in PEPs (readers/pep.py).
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.readers import pep


class TestPEPReaderInlineMarkup(unittest.TestCase):
    def test_standalone_references(self):
        parser = rst.Parser(rfc2822=True, inliner=rst.states.Inliner())

        settings = frontend.get_default_settings(rst.Parser, pep.Reader)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        for casenum, (case_input, case_expected) in enumerate(standalone_references):
            with self.subTest(id=f'standalone_references[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                self.assertEqual(document.pformat(), case_expected)

    def test_miscellaneous(self):
        parser = rst.Parser(rfc2822=True, inliner=rst.states.Inliner())

        settings = frontend.get_default_settings(rst.Parser, pep.Reader)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        for casenum, (case_input, case_expected) in enumerate(miscellaneous):
            with self.subTest(id=f'miscellaneous[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                self.assertEqual(document.pformat(), case_expected)


standalone_references = [
["""\
See PEP 287 (pep-0287.txt),
and RFC 2822 (which obsoletes RFC822 and RFC-733).
""",
"""\
<document source="test data">
    <paragraph>
        See \n\
        <reference refuri="https://peps.python.org/pep-0287">
            PEP 287
         (
        <reference refuri="https://peps.python.org/pep-0287">
            pep-0287.txt
        ),
        and \n\
        <reference refuri="https://tools.ietf.org/html/rfc2822.html">
            RFC 2822
         (which obsoletes \n\
        <reference refuri="https://tools.ietf.org/html/rfc822.html">
            RFC822
         and \n\
        <reference refuri="https://tools.ietf.org/html/rfc733.html">
            RFC-733
        ).
"""],
["""\
References split across lines:

PEP
287

RFC
2822
""",
"""\
<document source="test data">
    <paragraph>
        References split across lines:
    <paragraph>
        <reference refuri="https://peps.python.org/pep-0287">
            PEP
            287
    <paragraph>
        <reference refuri="https://tools.ietf.org/html/rfc2822.html">
            RFC
            2822
"""],
["""\
Test PEP-specific implicit references before a URL:

PEP 287 (https://peps.python.org/pep-0287), RFC 2822.
""",
"""\
<document source="test data">
    <paragraph>
        Test PEP-specific implicit references before a URL:
    <paragraph>
        <reference refuri="https://peps.python.org/pep-0287">
            PEP 287
         (
        <reference refuri="https://peps.python.org/pep-0287">
            https://peps.python.org/pep-0287
        ), \n\
        <reference refuri="https://tools.ietf.org/html/rfc2822.html">
            RFC 2822
        .
"""],
]

miscellaneous = [
["""\
For *completeness*, _`let's` ``test`` **other** forms_
|of| `inline markup` [*]_.

.. [*] See https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html.
""",
"""\
<document source="test data">
    <paragraph>
        For \n\
        <emphasis>
            completeness
        , \n\
        <target ids="let-s" names="let's">
            let's
         \n\
        <literal>
            test
         \n\
        <strong>
            other
         \n\
        <reference name="forms" refname="forms">
            forms
        \n\
        <substitution_reference refname="of">
            of
         \n\
        <title_reference>
            inline markup
         \n\
        <footnote_reference auto="*" ids="footnote-reference-1">
        .
    <footnote auto="*" ids="footnote-1">
        <paragraph>
            See \n\
            <reference refuri="https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html">
                https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html
            .
"""],
]


if __name__ == '__main__':
    unittest.main()
