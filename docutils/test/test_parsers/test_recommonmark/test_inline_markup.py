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
Tests for inline markup in CommonMark parsers
Cf. the `CommonMark Specification <https://spec.commonmark.org/>`__
"""

import unittest

from docutils import frontend
from docutils import utils
import docutils.parsers

md_parser_class = docutils.parsers.get_parser_class('recommonmark')


class TestRecommonmarkInlineMarkup(unittest.TestCase):
    def test_emphasis(self):
        parser = md_parser_class()
        settings = frontend.get_default_settings(md_parser_class)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        for casenum, (case_input, case_expected) in enumerate(emphasis):
            with self.subTest(id=f'emphasis[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)

    def test_strong(self):
        parser = md_parser_class()
        settings = frontend.get_default_settings(md_parser_class)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        for casenum, (case_input, case_expected) in enumerate(strong):
            with self.subTest(id=f'strong[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)

    def test_literal(self):
        parser = md_parser_class()
        settings = frontend.get_default_settings(md_parser_class)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        for casenum, (case_input, case_expected) in enumerate(literal):
            with self.subTest(id=f'literal[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)

    def test_references(self):
        parser = md_parser_class()
        settings = frontend.get_default_settings(md_parser_class)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        for casenum, (case_input, case_expected) in enumerate(references):
            with self.subTest(id=f'references[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)

    def test_appended_uris(self):
        parser = md_parser_class()
        settings = frontend.get_default_settings(md_parser_class)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        for casenum, (case_input, case_expected) in enumerate(appended_uris):
            with self.subTest(id=f'appended_uris[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)

    def test_standalone_hyperlink(self):
        parser = md_parser_class()
        settings = frontend.get_default_settings(md_parser_class)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        for casenum, (case_input, case_expected) in enumerate(standalone_hyperlink):
            with self.subTest(id=f'standalone_hyperlink[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)

    def test_raw_html(self):
        parser = md_parser_class()
        settings = frontend.get_default_settings(md_parser_class)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        for casenum, (case_input, case_expected) in enumerate(raw_html):
            with self.subTest(id=f'raw_html[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)

    def test_markup_recognition_rules(self):
        parser = md_parser_class()
        settings = frontend.get_default_settings(md_parser_class)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        for casenum, (case_input, case_expected) in enumerate(markup_recognition_rules):
            with self.subTest(id=f'markup_recognition_rules[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)


emphasis = [
["""\
*emphasis*
_also emphasis_
""",
"""\
<document source="test data">
    <paragraph>
        <emphasis>
            emphasis
        \n\
        <emphasis>
            also emphasis
"""],
["""\
Partially*emphasised*word.
""",
"""\
<document source="test data">
    <paragraph>
        Partially
        <emphasis>
            emphasised
        word.
"""],
["""\
*emphasized sentence
across lines*
""",
"""\
<document source="test data">
    <paragraph>
        <emphasis>
            emphasized sentence
            across lines
"""],
["""\
*no emphasis without closing asterisk
""",
"""\
<document source="test data">
    <paragraph>
        *no emphasis without closing asterisk
"""],
[r"""
No markup when \*escaped or unbalanced *.

What about *this**?
Unbalanced _markup__ is kept as-is without warning.
""",
"""\
<document source="test data">
    <paragraph>
        No markup when *escaped or unbalanced *.
    <paragraph>
        What about \n\
        <emphasis>
            this
        *?
        Unbalanced \n\
        <emphasis>
            markup
        _ is kept as-is without warning.
"""],
[r"""
Emphasized asterisk: *\**

Emphasized double asterisk: *\*\**
""",
"""\
<document source="test data">
    <paragraph>
        Emphasized asterisk: \n\
        <emphasis>
            *
    <paragraph>
        Emphasized double asterisk: \n\
        <emphasis>
            **
"""],
]

strong = [
["""\
**strong**
__also strong__
""",
"""\
<document source="test data">
    <paragraph>
        <strong>
            strong
        \n\
        <strong>
            also strong
"""],
["""\
Strong asterisk must be escaped **\\***

Strong double asterisk: **\\*\\***
""",
"""\
<document source="test data">
    <paragraph>
        Strong asterisk must be escaped \n\
        <strong>
            *
    <paragraph>
        Strong double asterisk: \n\
        <strong>
            **
"""],
["""\
**not strong without closing asterisks
""",
"""\
<document source="test data">
    <paragraph>
        **not strong without closing asterisks
"""],
]

literal = [
["""\
Inline `literals` are called `code spans` in CommonMark.
""",
"""\
<document source="test data">
    <paragraph>
        Inline \n\
        <literal classes="code">
            literals
         are called \n\
        <literal classes="code">
            code spans
         in CommonMark.
"""],
[r"""
`\*literal`
""",
"""\
<document source="test data">
    <paragraph>
        <literal classes="code">
            \\*literal
"""],
[r"""
``lite\ral``
""",
"""\
<document source="test data">
    <paragraph>
        <literal classes="code">
            lite\\ral
"""],
[r"""
``literal\``
""",
"""\
<document source="test data">
    <paragraph>
        <literal classes="code">
            literal\\
"""],
["""\
l'``literal`` and l\u2019``literal`` with apostrophe
""",
"""\
<document source="test data">
    <paragraph>
        l'
        <literal classes="code">
            literal
         and l\u2019
        <literal classes="code">
            literal
         with apostrophe
"""],
["""\
quoted '``literal``', quoted "``literal``",
quoted \u2018``literal``\u2019, quoted \u201c``literal``\u201d,
quoted \xab``literal``\xbb
""",
"""\
<document source="test data">
    <paragraph>
        quoted '
        <literal classes="code">
            literal
        ', quoted "
        <literal classes="code">
            literal
        ",
        quoted \u2018
        <literal classes="code">
            literal
        \u2019, quoted \u201c
        <literal classes="code">
            literal
        \u201d,
        quoted \xab
        <literal classes="code">
            literal
        \xbb
"""],
["""\
``'literal'`` with quotes, ``"literal"`` with quotes,
``\u2018literal\u2019`` with quotes, ``\u201cliteral\u201d`` with quotes,
``\xabliteral\xbb`` with quotes
""",
"""\
<document source="test data">
    <paragraph>
        <literal classes="code">
            'literal'
         with quotes, \n\
        <literal classes="code">
            "literal"
         with quotes,
        <literal classes="code">
            \u2018literal\u2019
         with quotes, \n\
        <literal classes="code">
            \u201cliteral\u201d
         with quotes,
        <literal classes="code">
            \xabliteral\xbb
         with quotes
"""],
[r"""
``literal ``no literal

No warning for `standalone TeX quotes' or other *unbalanced markup**.
""",
"""\
<document source="test data">
    <paragraph>
        <literal classes="code">
            literal \n\
        no literal
    <paragraph>
        No warning for `standalone TeX quotes\' or other \n\
        <emphasis>
            unbalanced markup
        *.
"""],
["""\
``not literal without closing backquotes
""",
"""\
<document source="test data">
    <paragraph>
        ``not literal without closing backquotes
"""],
[r"""
Python ``list``s use square bracket syntax.
""",
"""\
<document source="test data">
    <paragraph>
        Python \n\
        <literal classes="code">
            list
        s use square bracket syntax.
"""],
[r"""
Blank after opening `` not allowed.
""",
"""\
<document source="test data">
    <paragraph>
        Blank after opening `` not allowed.
"""],
[r"""
no blank ``after closing``still ends a literal.
""",
"""\
<document source="test data">
    <paragraph>
        no blank \n\
        <literal classes="code">
            after closing
        still ends a literal.
"""],
]

references = [
["""\
[ref]

[ref]: /uri
""",
"""\
<document source="test data">
    <paragraph>
        <reference name="ref" refuri="/uri">
            ref
"""],
# Fails with recommonmark 0.6.0:
# ["""\
# Inline image ![foo *bar*]
# in a paragraph.
#
# [foo *bar*]: train.jpg "train & tracks"
# """,
# """\
# <document source="test data">
#     <paragraph>
#         Inline image \n\
#         <image alt="foo " title="train & tracks" uri="train.jpg">
#         \n\
#         in a paragraph.
# """],
["""\
[phrase reference]

[phrase reference]: /uri
""",
"""\
<document source="test data">
    <paragraph>
        <reference name="phrase reference" refuri="/uri">
            phrase reference
"""],
["""\
No whitespace required around a[phrase reference].

[phrase reference]: /uri
""",
"""\
<document source="test data">
    <paragraph>
        No whitespace required around a
        <reference name="phrase reference" refuri="/uri">
            phrase reference
        .
"""],
["""\
[phrase reference
across lines]

[phrase reference across lines]: /uri
""",
"""\
<document source="test data">
    <paragraph>
        <reference name="phrase reference across lines" refuri="/uri">
            phrase reference
            across lines
"""],
]

appended_uris = [
["""\
[anonymous reference](http://example.com)
""",
"""\
<document source="test data">
    <paragraph>
        <reference refuri="http://example.com">
            anonymous reference
"""],
["""\
Inline image ![a train](train.jpg) more text.
""",
"""\
<document source="test data">
    <paragraph>
        Inline image \n\
        <image alt="a train" uri="train.jpg">
         more text.
"""],
# recommonmark 0.6.0 drops the "title"
# ["""\
# Inline image ![foo](/url "title") more text.
# """,
# """\
# <document source="test data">
#     <paragraph>
#         Inline image \n\
#         <image alt="foo" title="title" uri="/url">
#          more text.
# """],
["""\
[URI must follow immediately]
(http://example.com)
""",
"""\
<document source="test data">
    <paragraph>
        [URI must follow immediately]
        (http://example.com)
"""],
["""\
Relative URIs' reference text can't be omitted:

[reference](reference)
""",
"""\
<document source="test data">
    <paragraph>
        Relative URIs' reference text can't be omitted:
    <paragraph>
        <reference name="reference" refuri="reference">
            reference
"""],
]

standalone_hyperlink = [
["""\
CommonMark calls standalone hyperlinks
like <http://example.com> "autolinks".
""",
"""\
<document source="test data">
    <paragraph>
        CommonMark calls standalone hyperlinks
        like \n\
        <reference refuri="http://example.com">
            http://example.com
         "autolinks".
"""],
]

raw_html = [
["""\
foo <a href="uri"> bar
""",
"""\
<document source="test data">
    <paragraph>
        foo \n\
        <raw format="html" xml:space="preserve">
            <a href="uri">
         bar
"""],
["""\
foo <br /> bar
and <!-- this is an inline
comment - with hyphen -->
""",
"""\
<document source="test data">
    <paragraph>
        foo \n\
        <raw format="html" xml:space="preserve">
            <br />
         bar
        and \n\
        <raw format="html" xml:space="preserve">
            <!-- this is an inline
            comment - with hyphen -->
"""],
["""\
Hard line breaks are not supported by Docutils.
"recommonmark 0.6.0" converts both, invisible  \n\
(two or more trailing spaces) nor visible\\
(trailing backslash) to raw HTML.
""",
"""\
<document source="test data">
    <paragraph>
        Hard line breaks are not supported by Docutils.
        "recommonmark 0.6.0" converts both, invisible
        <raw format="html" xml:space="preserve">
            <br />
        (two or more trailing spaces) nor visible
        <raw format="html" xml:space="preserve">
            <br />
        (trailing backslash) to raw HTML.
"""],
]

markup_recognition_rules = [
[r"""
Character-level m*a***r**`k`_u_p
works except for underline.
""",
"""\
<document source="test data">
    <paragraph>
        Character-level m
        <emphasis>
            a
        <strong>
            r
        <literal classes="code">
            k
        _u_p
        works except for underline.
"""],
]


if __name__ == '__main__':
    unittest.main()
