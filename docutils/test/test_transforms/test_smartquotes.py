#!/usr/bin/env python3
# $Id$
# :Copyright: © 2011 Günter Milde.
# :Maintainer: docutils-develop@lists.sourceforge.net
# :License: Released under the terms of the `2-Clause BSD license`_, in short:
#
#    Copying and distribution of this file, with or without modification,
#    are permitted in any medium without royalty provided the copyright
#    notice and this notice are preserved.
#    This file is offered as-is, without any warranty.
#
# .. _2-Clause BSD license: https://opensource.org/licenses/BSD-2-Clause

"""
Test module for universal.SmartQuotes transform.
"""

from contextlib import contextmanager
import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.transforms import universal
from docutils.utils import smartquotes


@contextmanager
def local_quotes():
    orig = smartquotes.smartchars.quotes.copy()
    yield
    smartquotes.smartchars.quotes = orig


class TestTransformSmartQuotes(unittest.TestCase):
    def test_default(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        settings.smart_quotes = True

        for casenum, (case_input, case_expected) in enumerate(smartquotes_cases):
            with local_quotes(), self.subTest(id=f'smartquotes_cases[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                rst.Parser().parse(case_input, document)
                # Don't do a ``populate_from_components()`` because that would
                # enable the Transformer's default transforms.
                document.transformer.add_transform(universal.SmartQuotes)
                document.transformer.add_transform(universal.TestMessages)
                document.transformer.apply_transforms()
                output = document.pformat()

                # Normalise line endings:
                if output:
                    output = "\n".join(output.splitlines())
                if case_expected:
                    case_expected = "\n".join(case_expected.splitlines())
                self.assertEqual(output, case_expected)

    def test_de(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        settings.smart_quotes = True
        settings.language_code = 'de'

        with local_quotes():
            document = utils.new_document('test data', settings.copy())
            rst.Parser().parse(smartquotes_de_input, document)
            # Don't do a ``populate_from_components()`` because that would
            # enable the Transformer's default transforms.
            document.transformer.add_transform(universal.SmartQuotes)
            document.transformer.apply_transforms()
            output = document.pformat()
            self.assertEqual(output, smartquotes_de_expected)

    def test_de_alternative(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        settings.smart_quotes = 'alternative'
        settings.language_code = 'de'

        with local_quotes():
            document = utils.new_document('test data', settings.copy())
            rst.Parser().parse(smartquotes_de_alt_input, document)
            # Don't do a ``populate_from_components()`` because that would
            # enable the Transformer's default transforms.
            document.transformer.add_transform(universal.SmartQuotes)
            document.transformer.add_transform(universal.TestMessages)
            document.transformer.apply_transforms()
            output = document.pformat()
            self.assertEqual(output, smartquotes_de_alt_expected)

    def test_de_locales(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 1
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        settings.smart_quotes = True
        settings.language_code = 'de'
        settings.smartquotes_locales = [('de', '«»()'), ('nl', '„”’’')]

        with local_quotes():
            document = utils.new_document('test data', settings)
            rst.Parser().parse(smartquotes_locales_input, document)
            # Don't do a ``populate_from_components()`` because that would
            # enable the Transformer's default transforms.
            document.transformer.add_transform(universal.SmartQuotes)
            document.transformer.add_transform(universal.TestMessages)
            document.transformer.apply_transforms()
            output = document.pformat()
            self.assertEqual(output, smartquotes_locales_expected)


smartquotes_cases = [
["""\
Test "smart quotes", 'secondary smart quotes',
"'nested' smart" quotes
-- and ---also long--- dashes.
""",
"""\
<document source="test data">
    <paragraph>
        Test “smart quotes”, ‘secondary smart quotes’,
        “‘nested’ smart” quotes
        – and —also long— dashes.
"""],
[r"""Escaped \"ASCII quotes\" and \'secondary ASCII quotes\'.
""",
"""\
<document source="test data">
    <paragraph>
        Escaped "ASCII quotes" and 'secondary ASCII quotes'.
"""],
["""\
Do not "educate" quotes ``inside "literal" text`` and ::

  "literal" blocks.

.. role:: python(code)
   :class: python

Keep quotes straight in code and math:
:code:`print "hello"` :python:`print("hello")` :math:`1' 12"`.

.. code::

   print("hello")

.. math::

   f'(x) = df(x)/dx

""",
"""\
<document source="test data">
    <paragraph>
        Do not “educate” quotes \n\
        <literal>
            inside "literal" text
         and
    <literal_block xml:space="preserve">
        "literal" blocks.
    <paragraph>
        Keep quotes straight in code and math:
        <literal classes="code">
            print "hello"
         \n\
        <literal classes="code python">
            print("hello")
         \n\
        <math>
            1' 12"
        .
    <literal_block classes="code" xml:space="preserve">
        print("hello")
    <math_block xml:space="preserve">
        f'(x) = df(x)/dx
"""],
["""\
Closing quotes, if preceded by
wor"d char's
or punctuation:"a",'a';'a' (TODO: opening quotes if followed by word-char?).

Opening quotes after
normal space "a" 'a',
thin space "a" 'a',
em space "a" 'a',
NBSP "a" 'a',
ZWSP\u200B"a" and\u200B'a',
ZWNJ\u200C"a" and\u200C'a',
escaped space\\ "a" and\\ 'a',

hyphen -"a", -'a'
&mdash;"a",&mdash;'a'
en dash –"a"–'a',
em dash —"a"—'a'.

opening brackets ("a") ('a') ["a"] ['a'] {"a"} {'a'}

But not if followed by (optional punctuation and) whitespace:
"-", "–", "—", "(", "a[", "{"
'-', '–', '—', '((', '[', '{'
""",
"""\
<document source="test data">
    <paragraph>
        Closing quotes, if preceded by
        wor”d char’s
        or punctuation:”a”,’a’;’a’ (TODO: opening quotes if followed by word-char?).
    <paragraph>
        Opening quotes after
        normal space “a” ‘a’,
        thin space “a” ‘a’,
        em space “a” ‘a’,
        NBSP “a” ‘a’,
        ZWSP\u200B“a” and\u200B‘a’,
        ZWNJ\u200C“a” and\u200C‘a’,
        escaped space“a” and‘a’,
    <paragraph>
        hyphen -“a”, -‘a’
        &mdash;“a”,&mdash;‘a’
        en dash –“a”–‘a’,
        em dash —“a”—‘a’.
    <paragraph>
        opening brackets (“a”) (‘a’) [“a”] [‘a’] {“a”} {‘a’}
    <paragraph>
        But not if followed by (optional punctuation and) whitespace:
        “-”, “–”, “—”, “(”, “a[”, “{”
        ‘-’, ‘–’, ‘—’, ‘((’, ‘[’, ‘{’
"""],
["""\
Quotes and inline-elements:

* Around "_`targets`", "*emphasized*" or "``literal``" text
  and links to "targets_".

* Inside *"emphasized"* or other `inline "roles"`

Do not drop characters from intra-word inline markup like
*re*\\ ``Structured``\\ *Text*.
""",
"""\
<document source="test data">
    <paragraph>
        Quotes and inline-elements:
    <bullet_list bullet="*">
        <list_item>
            <paragraph>
                Around “
                <target ids="targets" names="targets">
                    targets
                ”, “
                <emphasis>
                    emphasized
                ” or “
                <literal>
                    literal
                ” text
                and links to “
                <reference name="targets" refname="targets">
                    targets
                ”.
        <list_item>
            <paragraph>
                Inside \n\
                <emphasis>
                    “emphasized”
                 or other \n\
                <title_reference>
                    inline “roles”
    <paragraph>
        Do not drop characters from intra-word inline markup like
        <emphasis>
            re
        <literal>
            Structured
        <emphasis>
            Text
        .\
"""],
["""\
Do not convert context-character at inline-tag boundaries
(in French, smart quotes expand to two characters).

.. class:: language-fr-ch-x-altquot

  Around "_`targets`", "*emphasized*" or "``literal``" text
  and links to "targets_".

  Inside *"emphasized"* or other `inline "roles"`:
  (``"string"``), (``'string'``), *\"betont\"*, \"*betont*".

  Do not drop characters from intra-word inline markup like
  *re*\\ ``Structured``\\ *Text*.
""",
"""\
<document source="test data">
    <paragraph>
        Do not convert context-character at inline-tag boundaries
        (in French, smart quotes expand to two characters).
    <paragraph classes="language-fr-ch-x-altquot">
        Around «\u202f
        <target ids="targets" names="targets">
            targets
        \u202f», «\u202f
        <emphasis>
            emphasized
        \u202f» or «\u202f
        <literal>
            literal
        \u202f» text
        and links to «\u202f
        <reference name="targets" refname="targets">
            targets
        \u202f».
    <paragraph classes="language-fr-ch-x-altquot">
        Inside \n\
        <emphasis>
            «\u202femphasized\u202f»
         or other \n\
        <title_reference>
            inline «\u202froles\u202f»
        :
        (
        <literal>
            "string"
        ), (
        <literal>
            'string'
        ), \n\
        <emphasis>
            «\u202fbetont\u202f»
        , «\u202f
        <emphasis>
            betont
        \u202f».
    <paragraph classes="language-fr-ch-x-altquot">
        Do not drop characters from intra-word inline markup like
        <emphasis>
            re
        <literal>
            Structured
        <emphasis>
            Text
        .
"""],
[r"""
Docutils escape mechanism uses the backslash:

\Remove \non-escaped \backslashes\:
\item \newline \tab \" \' \*.

\ Remove-\ escaped-\ white\ space-\
including-\ newlines.

\\Keep\\escaped\\backslashes\\
(but\\only\\one).

\\ Keep \\ space\\ around  \\ backslashes.

Keep backslashes ``\in\ literal``, :math:`in \mathrm{math}`,
and :code:`in\ code`.

Test around inline elements:\ [*]_

*emphasized*, H\ :sub:`2`\ O and :math:`x^2`

*emphasized*, H\ :sub:`2`\ O and :math:`x^2`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. [*] and footnotes
""",
"""\
<document source="test data">
    <paragraph>
        Docutils escape mechanism uses the backslash:
    <paragraph>
        Remove non-escaped backslashes:
        item newline tab " \' *.
    <paragraph>
        Remove-escaped-whitespace-including-newlines.
    <paragraph>
        \\Keep\\escaped\\backslashes\\
        (but\\only\\one).
    <paragraph>
        \\ Keep \\ space\\ around  \\ backslashes.
    <paragraph>
        Keep backslashes \n\
        <literal>
            \\in\\ literal
        , \n\
        <math>
            in \\mathrm{math}
        ,
        and \n\
        <literal classes="code">
            in\\ code
        .
    <paragraph>
        Test around inline elements:
        <footnote_reference auto="*" ids="footnote-reference-1">
    <paragraph>
        <emphasis>
            emphasized
        , H
        <subscript>
            2
        O and \n\
        <math>
            x^2
    <section ids="emphasized-h2o-and-x-2" names="emphasized,\\ h2o\\ and\\ x^2">
        <title>
            <emphasis>
                emphasized
            , H
            <subscript>
                2
            O and \n\
            <math>
                x^2
        <footnote auto="*" ids="footnote-1">
            <paragraph>
                and footnotes
"""],
[r"""
Character-level m\ *a*\ **r**\ ``k``\ `u`:title:\p
with backslash-escaped whitespace, including new\
lines.
""",
"""\
<document source="test data">
    <paragraph>
        Character-level m
        <emphasis>
            a
        <strong>
            r
        <literal>
            k
        <title_reference>
            u
        p
        with backslash-escaped whitespace, including newlines.
"""],
["""\
.. class:: language-de

German "smart quotes" and 'secondary smart quotes'.

.. class:: language-en-UK-x-altquot

British "primary quotes" use single and
'secondary quotes' double quote signs.

.. class:: language-foo

"Quoting style" for unknown languages is 'ASCII'.

.. class:: language-de-x-altquot

Alternative German "smart quotes" and 'secondary smart quotes'.
""",
"""\
<document source="test data">
    <paragraph classes="language-de">
        German „smart quotes“ and ‚secondary smart quotes‘.
    <paragraph classes="language-en-uk-x-altquot">
        British ‘primary quotes’ use single and
        “secondary quotes” double quote signs.
    <paragraph classes="language-foo">
        "Quoting style" for unknown languages is 'ASCII'.
    <paragraph classes="language-de-x-altquot">
        Alternative German »smart quotes« and ›secondary smart quotes‹.
    <system_message level="2" line="12" source="test data" type="WARNING">
        <paragraph>
            No smart quotes defined for language "foo".
"""],
]

smartquotes_de_input = """\
German "smart quotes" and 'secondary smart quotes'.

.. klasse:: language-en

English "smart quotes" and 'secondary smart quotes'.
"""

smartquotes_de_expected = """\
<document source="test data">
    <paragraph>
        German „smart quotes“ and ‚secondary smart quotes‘.
    <paragraph classes="language-en">
        English “smart quotes” and ‘secondary smart quotes’.
"""

smartquotes_de_alt_input = """\
Alternative German "smart quotes" and 'secondary smart quotes'.

In this case, the apostrophe isn't a closing secondary quote!

.. klasse:: language-en-UK

British "quotes" use single and 'secondary quotes' double quote signs
(there are no alternative quotes defined).

.. klasse:: language-ro

Romanian "smart quotes" and 'secondary' smart quotes.
"""

smartquotes_de_alt_expected = """\
<document source="test data">
    <paragraph>
        Alternative German »smart quotes« and ›secondary smart quotes‹.
    <paragraph>
        In this case, the apostrophe isn’t a closing secondary quote!
    <paragraph classes="language-en-uk">
        British ‘quotes’ use single and “secondary quotes” double quote signs
        (there are no alternative quotes defined).
    <paragraph classes="language-ro">
        Romanian „smart quotes” and «secondary» smart quotes.
"""

smartquotes_locales_input = """\
German "smart quotes" and 'secondary smart quotes'.

.. klasse:: language-nl

Dutch "smart quotes" and 's Gravenhage (leading apostrophe).
"""

smartquotes_locales_expected = """\
<document source="test data">
    <paragraph>
        German «smart quotes» and (secondary smart quotes).
    <paragraph classes="language-nl">
        Dutch „smart quotes” and ’s Gravenhage (leading apostrophe).
"""


if __name__ == '__main__':
    unittest.main()
