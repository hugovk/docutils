#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for docutils.transforms.references.Footnotes.
"""

if __name__ == '__main__':
    import __init__
import unittest
from test import DocutilsTestSupport
from docutils.transforms.references import Footnotes
from docutils.parsers.rst import Parser


def suite():
    parser = Parser()
    suite_id = DocutilsTestSupport.make_id(__file__)
    s = unittest.TestSuite()
    for name, (transforms, cases) in totest.items():
        for casenum, (case_input, case_expected) in enumerate(cases):
            s.addTest(
                DocutilsTestSupport.TransformTestCase("test_transforms",
                                                      input=case_input, expected=case_expected,
                                                      id='%s: totest[%r][%s]' % (suite_id, name, casenum),
                                                      suite_settings={},
                                                      transforms=transforms, parser=parser)
            )
    return s

totest = {}

totest['footnotes'] = ((Footnotes,), [
["""\
[#autolabel]_

.. [#autolabel] text
""",
"""\
<document source="test data">
    <paragraph>
        <footnote_reference auto="1" ids="footnote-reference-1" refid="autolabel">
            1
    <footnote auto="1" backrefs="footnote-reference-1" ids="autolabel" names="autolabel">
        <label>
            1
        <paragraph>
            text
"""],
["""\
autonumber: [#]_

.. [#] text
""",
"""\
<document source="test data">
    <paragraph>
        autonumber: \n\
        <footnote_reference auto="1" ids="footnote-reference-1" refid="footnote-1">
            1
    <footnote auto="1" backrefs="footnote-reference-1" ids="footnote-1" names="1">
        <label>
            1
        <paragraph>
            text
"""],
["""\
[#]_ is the first auto-numbered footnote reference.
[#]_ is the second auto-numbered footnote reference.

.. [#] Auto-numbered footnote 1.
.. [#] Auto-numbered footnote 2.
.. [#] Auto-numbered footnote 3.

[#]_ is the third auto-numbered footnote reference.
""",
"""\
<document source="test data">
    <paragraph>
        <footnote_reference auto="1" ids="footnote-reference-1" refid="footnote-1">
            1
         is the first auto-numbered footnote reference.
        <footnote_reference auto="1" ids="footnote-reference-2" refid="footnote-2">
            2
         is the second auto-numbered footnote reference.
    <footnote auto="1" backrefs="footnote-reference-1" ids="footnote-1" names="1">
        <label>
            1
        <paragraph>
            Auto-numbered footnote 1.
    <footnote auto="1" backrefs="footnote-reference-2" ids="footnote-2" names="2">
        <label>
            2
        <paragraph>
            Auto-numbered footnote 2.
    <footnote auto="1" backrefs="footnote-reference-3" ids="footnote-3" names="3">
        <label>
            3
        <paragraph>
            Auto-numbered footnote 3.
    <paragraph>
        <footnote_reference auto="1" ids="footnote-reference-3" refid="footnote-3">
            3
         is the third auto-numbered footnote reference.
"""],
["""\
[#third]_ is a reference to the third auto-numbered footnote.

.. [#first] First auto-numbered footnote.
.. [#second] Second auto-numbered footnote.
.. [#third] Third auto-numbered footnote.

[#second]_ is a reference to the second auto-numbered footnote.
[#first]_ is a reference to the first auto-numbered footnote.
[#third]_ is another reference to the third auto-numbered footnote.

Here are some internal cross-references to the implicit targets
generated by the footnotes: first_, second_, third_.
""",
"""\
<document source="test data">
    <paragraph>
        <footnote_reference auto="1" ids="footnote-reference-1" refid="third">
            3
         is a reference to the third auto-numbered footnote.
    <footnote auto="1" backrefs="footnote-reference-3" ids="first" names="first">
        <label>
            1
        <paragraph>
            First auto-numbered footnote.
    <footnote auto="1" backrefs="footnote-reference-2" ids="second" names="second">
        <label>
            2
        <paragraph>
            Second auto-numbered footnote.
    <footnote auto="1" backrefs="footnote-reference-1 footnote-reference-4" ids="third" names="third">
        <label>
            3
        <paragraph>
            Third auto-numbered footnote.
    <paragraph>
        <footnote_reference auto="1" ids="footnote-reference-2" refid="second">
            2
         is a reference to the second auto-numbered footnote.
        <footnote_reference auto="1" ids="footnote-reference-3" refid="first">
            1
         is a reference to the first auto-numbered footnote.
        <footnote_reference auto="1" ids="footnote-reference-4" refid="third">
            3
         is another reference to the third auto-numbered footnote.
    <paragraph>
        Here are some internal cross-references to the implicit targets
        generated by the footnotes: \n\
        <reference name="first" refname="first">
            first
        , \n\
        <reference name="second" refname="second">
            second
        , \n\
        <reference name="third" refname="third">
            third
        .
"""],
["""\
Mixed anonymous and labelled auto-numbered footnotes:

[#four]_ should be 4, [#]_ should be 1,
[#]_ should be 3, [#]_ is one too many,
[#two]_ should be 2, and [#six]_ doesn't exist.

.. [#] Auto-numbered footnote 1.
.. [#two] Auto-numbered footnote 2.
.. [#] Auto-numbered footnote 3.
.. [#four] Auto-numbered footnote 4.
.. [#five] Auto-numbered footnote 5.
.. [#five] Auto-numbered footnote 5 again (duplicate).
""",
"""\
<document source="test data">
    <paragraph>
        Mixed anonymous and labelled auto-numbered footnotes:
    <paragraph>
        <footnote_reference auto="1" ids="footnote-reference-1" refid="four">
            4
         should be 4, \n\
        <footnote_reference auto="1" ids="footnote-reference-2" refid="footnote-1">
            1
         should be 1,
        <footnote_reference auto="1" ids="footnote-reference-3" refid="footnote-2">
            3
         should be 3, \n\
        <problematic ids="problematic-1 footnote-reference-4" refid="system-message-1">
            [#]_
         is one too many,
        <footnote_reference auto="1" ids="footnote-reference-5" refid="two">
            2
         should be 2, and \n\
        <footnote_reference auto="1" ids="footnote-reference-6" refname="six">
         doesn't exist.
    <footnote auto="1" backrefs="footnote-reference-2" ids="footnote-1" names="1">
        <label>
            1
        <paragraph>
            Auto-numbered footnote 1.
    <footnote auto="1" backrefs="footnote-reference-5" ids="two" names="two">
        <label>
            2
        <paragraph>
            Auto-numbered footnote 2.
    <footnote auto="1" backrefs="footnote-reference-3" ids="footnote-2" names="3">
        <label>
            3
        <paragraph>
            Auto-numbered footnote 3.
    <footnote auto="1" backrefs="footnote-reference-1" ids="four" names="four">
        <label>
            4
        <paragraph>
            Auto-numbered footnote 4.
    <footnote auto="1" dupnames="five" ids="five">
        <label>
            5
        <paragraph>
            Auto-numbered footnote 5.
    <footnote auto="1" dupnames="five" ids="five-1">
        <label>
            6
        <system_message backrefs="five-1" level="2" line="12" source="test data" type="WARNING">
            <paragraph>
                Duplicate explicit target name: "five".
        <paragraph>
            Auto-numbered footnote 5 again (duplicate).
    <system_message backrefs="problematic-1" ids="system-message-1" level="3" line="3" source="test data" type="ERROR">
        <paragraph>
            Too many autonumbered footnote references: only 2 corresponding footnotes available.
"""],
["""\
Mixed auto-numbered and manual footnotes:

.. [1] manually numbered
.. [#] auto-numbered
.. [#label] autonumber-labeled
""",
"""\
<document source="test data">
    <paragraph>
        Mixed auto-numbered and manual footnotes:
    <footnote ids="footnote-1" names="1">
        <label>
            1
        <paragraph>
            manually numbered
    <footnote auto="1" ids="footnote-2" names="2">
        <label>
            2
        <paragraph>
            auto-numbered
    <footnote auto="1" ids="label" names="label">
        <label>
            3
        <paragraph>
            autonumber-labeled
"""],
["""\
A labeled autonumbered footnote referece: [#footnote]_.

An unlabeled autonumbered footnote referece: [#]_.

.. [#] Unlabeled autonumbered footnote.
.. [#footnote] Labeled autonumbered footnote.
   Note that the footnotes are not in the same
   order as the references.
""",
"""\
<document source="test data">
    <paragraph>
        A labeled autonumbered footnote referece: \n\
        <footnote_reference auto="1" ids="footnote-reference-1" refid="footnote">
            2
        .
    <paragraph>
        An unlabeled autonumbered footnote referece: \n\
        <footnote_reference auto="1" ids="footnote-reference-2" refid="footnote-1">
            1
        .
    <footnote auto="1" backrefs="footnote-reference-2" ids="footnote-1" names="1">
        <label>
            1
        <paragraph>
            Unlabeled autonumbered footnote.
    <footnote auto="1" backrefs="footnote-reference-1" ids="footnote" names="footnote">
        <label>
            2
        <paragraph>
            Labeled autonumbered footnote.
            Note that the footnotes are not in the same
            order as the references.
"""],
["""\
Mixed manually-numbered, anonymous auto-numbered,
and labelled auto-numbered footnotes:

[#four]_ should be 4, [#]_ should be 2,
[1]_ is 1, [3]_ is 3,
[#]_ should be 6, [#]_ is one too many,
[#five]_ should be 5, and [#eight]_ doesn't exist.

.. [1] Manually-numbered footnote 1.
.. [#] Auto-numbered footnote 2.
.. [#four] Auto-numbered footnote 4.
.. [3] Manually-numbered footnote 3
.. [#five] Auto-numbered footnote 5.
.. [#] Auto-numbered footnote 6.
.. [#five] Auto-numbered footnote 5 again (duplicate).
""",
"""\
<document source="test data">
    <paragraph>
        Mixed manually-numbered, anonymous auto-numbered,
        and labelled auto-numbered footnotes:
    <paragraph>
        <footnote_reference auto="1" ids="footnote-reference-1" refid="four">
            4
         should be 4, \n\
        <footnote_reference auto="1" ids="footnote-reference-2" refid="footnote-2">
            2
         should be 2,
        <footnote_reference ids="footnote-reference-3" refid="footnote-1">
            1
         is 1, \n\
        <footnote_reference ids="footnote-reference-4" refid="footnote-3">
            3
         is 3,
        <footnote_reference auto="1" ids="footnote-reference-5" refid="footnote-4">
            6
         should be 6, \n\
        <problematic ids="problematic-1 footnote-reference-6" refid="system-message-1">
            [#]_
         is one too many,
        <footnote_reference auto="1" ids="footnote-reference-7" refname="five">
         should be 5, and \n\
        <footnote_reference auto="1" ids="footnote-reference-8" refname="eight">
         doesn't exist.
    <footnote backrefs="footnote-reference-3" ids="footnote-1" names="1">
        <label>
            1
        <paragraph>
            Manually-numbered footnote 1.
    <footnote auto="1" backrefs="footnote-reference-2" ids="footnote-2" names="2">
        <label>
            2
        <paragraph>
            Auto-numbered footnote 2.
    <footnote auto="1" backrefs="footnote-reference-1" ids="four" names="four">
        <label>
            4
        <paragraph>
            Auto-numbered footnote 4.
    <footnote backrefs="footnote-reference-4" ids="footnote-3" names="3">
        <label>
            3
        <paragraph>
            Manually-numbered footnote 3
    <footnote auto="1" dupnames="five" ids="five">
        <label>
            5
        <paragraph>
            Auto-numbered footnote 5.
    <footnote auto="1" backrefs="footnote-reference-5" ids="footnote-4" names="6">
        <label>
            6
        <paragraph>
            Auto-numbered footnote 6.
    <footnote auto="1" dupnames="five" ids="five-1">
        <label>
            7
        <system_message backrefs="five-1" level="2" line="15" source="test data" type="WARNING">
            <paragraph>
                Duplicate explicit target name: "five".
        <paragraph>
            Auto-numbered footnote 5 again (duplicate).
    <system_message backrefs="problematic-1" ids="system-message-1" level="3" line="4" source="test data" type="ERROR">
        <paragraph>
            Too many autonumbered footnote references: only 2 corresponding footnotes available.
"""],
["""\
Referencing a footnote by symbol [*]_.

.. [*] This is an auto-symbol footnote.
""",
"""\
<document source="test data">
    <paragraph>
        Referencing a footnote by symbol \n\
        <footnote_reference auto="*" ids="footnote-reference-1" refid="footnote-1">
            *
        .
    <footnote auto="*" backrefs="footnote-reference-1" ids="footnote-1">
        <label>
            *
        <paragraph>
            This is an auto-symbol footnote.
"""],
["""\
A sequence of symbol footnote references:
[*]_ [*]_ [*]_ [*]_ [*]_ [*]_ [*]_ [*]_ [*]_ [*]_ [*]_ [*]_.

.. [*] Auto-symbol footnote 1.
.. [*] Auto-symbol footnote 2.
.. [*] Auto-symbol footnote 3.
.. [*] Auto-symbol footnote 4.
.. [*] Auto-symbol footnote 5.
.. [*] Auto-symbol footnote 6.
.. [*] Auto-symbol footnote 7.
.. [*] Auto-symbol footnote 8.
.. [*] Auto-symbol footnote 9.
.. [*] Auto-symbol footnote 10.
.. [*] Auto-symbol footnote 11.
.. [*] Auto-symbol footnote 12.
""",
"""\
<document source="test data">
    <paragraph>
        A sequence of symbol footnote references:
        <footnote_reference auto="*" ids="footnote-reference-1" refid="footnote-1">
            *
         \n\
        <footnote_reference auto="*" ids="footnote-reference-2" refid="footnote-2">
            \u2020
         \n\
        <footnote_reference auto="*" ids="footnote-reference-3" refid="footnote-3">
            \u2021
         \n\
        <footnote_reference auto="*" ids="footnote-reference-4" refid="footnote-4">
            \u00A7
         \n\
        <footnote_reference auto="*" ids="footnote-reference-5" refid="footnote-5">
            \u00B6
         \n\
        <footnote_reference auto="*" ids="footnote-reference-6" refid="footnote-6">
            #
         \n\
        <footnote_reference auto="*" ids="footnote-reference-7" refid="footnote-7">
            \u2660
         \n\
        <footnote_reference auto="*" ids="footnote-reference-8" refid="footnote-8">
            \u2665
         \n\
        <footnote_reference auto="*" ids="footnote-reference-9" refid="footnote-9">
            \u2666
         \n\
        <footnote_reference auto="*" ids="footnote-reference-10" refid="footnote-10">
            \u2663
         \n\
        <footnote_reference auto="*" ids="footnote-reference-11" refid="footnote-11">
            **
         \n\
        <footnote_reference auto="*" ids="footnote-reference-12" refid="footnote-12">
            \u2020\u2020
        .
    <footnote auto="*" backrefs="footnote-reference-1" ids="footnote-1">
        <label>
            *
        <paragraph>
            Auto-symbol footnote 1.
    <footnote auto="*" backrefs="footnote-reference-2" ids="footnote-2">
        <label>
            \u2020
        <paragraph>
            Auto-symbol footnote 2.
    <footnote auto="*" backrefs="footnote-reference-3" ids="footnote-3">
        <label>
            \u2021
        <paragraph>
            Auto-symbol footnote 3.
    <footnote auto="*" backrefs="footnote-reference-4" ids="footnote-4">
        <label>
            \u00A7
        <paragraph>
            Auto-symbol footnote 4.
    <footnote auto="*" backrefs="footnote-reference-5" ids="footnote-5">
        <label>
            \u00B6
        <paragraph>
            Auto-symbol footnote 5.
    <footnote auto="*" backrefs="footnote-reference-6" ids="footnote-6">
        <label>
            #
        <paragraph>
            Auto-symbol footnote 6.
    <footnote auto="*" backrefs="footnote-reference-7" ids="footnote-7">
        <label>
            \u2660
        <paragraph>
            Auto-symbol footnote 7.
    <footnote auto="*" backrefs="footnote-reference-8" ids="footnote-8">
        <label>
            \u2665
        <paragraph>
            Auto-symbol footnote 8.
    <footnote auto="*" backrefs="footnote-reference-9" ids="footnote-9">
        <label>
            \u2666
        <paragraph>
            Auto-symbol footnote 9.
    <footnote auto="*" backrefs="footnote-reference-10" ids="footnote-10">
        <label>
            \u2663
        <paragraph>
            Auto-symbol footnote 10.
    <footnote auto="*" backrefs="footnote-reference-11" ids="footnote-11">
        <label>
            **
        <paragraph>
            Auto-symbol footnote 11.
    <footnote auto="*" backrefs="footnote-reference-12" ids="footnote-12">
        <label>
            \u2020\u2020
        <paragraph>
            Auto-symbol footnote 12.
"""],
["""\
Duplicate manual footnote labels:

.. [1] Footnote.

.. [1] Footnote.
""",
"""\
<document source="test data">
    <paragraph>
        Duplicate manual footnote labels:
    <footnote dupnames="1" ids="footnote-1">
        <label>
            1
        <paragraph>
            Footnote.
    <footnote dupnames="1" ids="footnote-2">
        <label>
            1
        <system_message backrefs="footnote-2" level="2" line="5" source="test data" type="WARNING">
            <paragraph>
                Duplicate explicit target name: "1".
        <paragraph>
            Footnote.
"""],
])


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
