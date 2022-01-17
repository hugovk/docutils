#! /usr/bin/env python3

# $Id$
# Authors: David Goodger <goodger@python.org>; Dmitry Jemerov
# Copyright: This module has been placed in the public domain.

"""
Tests for `docutils.transforms.parts.SectNum` (via
`docutils.transforms.universal.LastReaderPending`).
"""

import unittest
from test import DocutilsTestSupport
from docutils.transforms.references import Substitutions
from docutils.parsers.rst import Parser
from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.transforms import universal


class TransformTestCase(DocutilsTestSupport.CustomTestCase):

    """
    Output checker for the transform.

    Should probably be called TransformOutputChecker, but I can deal with
    that later when/if someone comes up with a category of transform test
    cases that have nothing to do with the input and output of the transform.
    """

    option_parser = frontend.OptionParser(components=(rst.Parser,))
    settings = option_parser.get_default_values()
    settings.report_level = 1
    settings.halt_level = 5
    settings.debug = False
    settings.warning_stream = DocutilsTestSupport.DevNull()
    unknown_reference_resolvers = ()
    parser = Parser()

    def test_transforms(self):
        for name, (transforms, cases) in totest.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    document = utils.new_document('test data', self.settings.copy())
                    self.parser.parse(case_input, document)
                    # Don't do a ``populate_from_components()`` because that would
                    # enable the Transformer's default transforms.
                    document.transformer.add_transforms(transforms)
                    document.transformer.add_transform(universal.TestMessages)
                    document.transformer.components['writer'] = self
                    document.transformer.apply_transforms()
                    output = document.pformat()
                    DocutilsTestSupport._compare_output(self, case_input, output, case_expected)


totest = {}

totest['section_numbers'] = ((Substitutions,), [
["""\
.. sectnum::

Title 1
=======
Paragraph 1.

Title 2
-------
Paragraph 2.

Title 3
```````
Paragraph 3.

Title 4
-------
Paragraph 4.
""",
"""\
<document source="test data">
    <section ids="title-1" names="title\\ 1">
        <title auto="1">
            <generated classes="sectnum">
                1\u00a0\u00a0\u00a0
            Title 1
        <paragraph>
            Paragraph 1.
        <section ids="title-2" names="title\\ 2">
            <title auto="1">
                <generated classes="sectnum">
                    1.1\u00a0\u00a0\u00a0
                Title 2
            <paragraph>
                Paragraph 2.
            <section ids="title-3" names="title\\ 3">
                <title auto="1">
                    <generated classes="sectnum">
                        1.1.1\u00a0\u00a0\u00a0
                    Title 3
                <paragraph>
                    Paragraph 3.
        <section ids="title-4" names="title\\ 4">
            <title auto="1">
                <generated classes="sectnum">
                    1.2\u00a0\u00a0\u00a0
                Title 4
            <paragraph>
                Paragraph 4.
"""],
["""\
.. sectnum::

**Bold Title**
==============
Paragraph 1.
""",
"""\
<document source="test data">
    <section ids="bold-title" names="bold\\ title">
        <title auto="1">
            <generated classes="sectnum">
                1\u00a0\u00a0\u00a0
            <strong>
                Bold Title
        <paragraph>
            Paragraph 1.
"""],
["""\
.. sectnum:: :depth: 2

Title 1
=======
Paragraph 1.

Title 2
-------
Paragraph 2.

Title 3
```````
Paragraph 3.

Title 4
-------
Paragraph 4.
""",
"""\
<document source="test data">
    <section ids="title-1" names="title\\ 1">
        <title auto="1">
            <generated classes="sectnum">
                1\u00a0\u00a0\u00a0
            Title 1
        <paragraph>
            Paragraph 1.
        <section ids="title-2" names="title\\ 2">
            <title auto="1">
                <generated classes="sectnum">
                    1.1\u00a0\u00a0\u00a0
                Title 2
            <paragraph>
                Paragraph 2.
            <section ids="title-3" names="title\\ 3">
                <title>
                    Title 3
                <paragraph>
                    Paragraph 3.
        <section ids="title-4" names="title\\ 4">
            <title auto="1">
                <generated classes="sectnum">
                    1.2\u00a0\u00a0\u00a0
                Title 4
            <paragraph>
                Paragraph 4.
"""],
["""\
.. contents::
.. sectnum:: :depth: 2

Title 1
=======
Paragraph 1.

Title 2
-------
Paragraph 2.

Title 3
```````
Paragraph 3.

Title 4
-------
Paragraph 4.
""",
"""\
<document source="test data">
    <topic classes="contents" ids="contents" names="contents">
        <title>
            Contents
        <bullet_list classes="auto-toc">
            <list_item>
                <paragraph>
                    <reference ids="toc-entry-1" refid="title-1">
                        <generated classes="sectnum">
                            1\u00a0\u00a0\u00a0
                        Title 1
                <bullet_list classes="auto-toc">
                    <list_item>
                        <paragraph>
                            <reference ids="toc-entry-2" refid="title-2">
                                <generated classes="sectnum">
                                    1.1\u00a0\u00a0\u00a0
                                Title 2
                        <bullet_list>
                            <list_item>
                                <paragraph>
                                    <reference ids="toc-entry-3" refid="title-3">
                                        Title 3
                    <list_item>
                        <paragraph>
                            <reference ids="toc-entry-4" refid="title-4">
                                <generated classes="sectnum">
                                    1.2\u00a0\u00a0\u00a0
                                Title 4
    <section ids="title-1" names="title\\ 1">
        <title auto="1" refid="toc-entry-1">
            <generated classes="sectnum">
                1\u00a0\u00a0\u00a0
            Title 1
        <paragraph>
            Paragraph 1.
        <section ids="title-2" names="title\\ 2">
            <title auto="1" refid="toc-entry-2">
                <generated classes="sectnum">
                    1.1\u00a0\u00a0\u00a0
                Title 2
            <paragraph>
                Paragraph 2.
            <section ids="title-3" names="title\\ 3">
                <title refid="toc-entry-3">
                    Title 3
                <paragraph>
                    Paragraph 3.
        <section ids="title-4" names="title\\ 4">
            <title auto="1" refid="toc-entry-4">
                <generated classes="sectnum">
                    1.2\u00a0\u00a0\u00a0
                Title 4
            <paragraph>
                Paragraph 4.
"""],
["""\
.. sectnum::
   :prefix: Arbitrary-

Title 1
=======
Paragraph 1.

Title 2
-------
Paragraph 2.

Title 3
```````
Paragraph 3.

Title 4
-------
Paragraph 4.
""",
"""\
<document source="test data">
    <section ids="title-1" names="title\\ 1">
        <title auto="1">
            <generated classes="sectnum">
                Arbitrary-1\u00a0\u00a0\u00a0
            Title 1
        <paragraph>
            Paragraph 1.
        <section ids="title-2" names="title\\ 2">
            <title auto="1">
                <generated classes="sectnum">
                    Arbitrary-1.1\u00a0\u00a0\u00a0
                Title 2
            <paragraph>
                Paragraph 2.
            <section ids="title-3" names="title\\ 3">
                <title auto="1">
                    <generated classes="sectnum">
                        Arbitrary-1.1.1\u00a0\u00a0\u00a0
                    Title 3
                <paragraph>
                    Paragraph 3.
        <section ids="title-4" names="title\\ 4">
            <title auto="1">
                <generated classes="sectnum">
                    Arbitrary-1.2\u00a0\u00a0\u00a0
                Title 4
            <paragraph>
                Paragraph 4.
"""],
["""\
.. sectnum::
   :start: 3
   \n\
Title 1
=======
Paragraph 1.

Title 2
-------
Paragraph 2.

Title 3
```````
Paragraph 3.

Title 4
-------
Paragraph 4.
""",
"""\
<document source="test data">
    <section ids="title-1" names="title\\ 1">
        <title auto="1">
            <generated classes="sectnum">
                3\u00a0\u00a0\u00a0
            Title 1
        <paragraph>
            Paragraph 1.
        <section ids="title-2" names="title\\ 2">
            <title auto="1">
                <generated classes="sectnum">
                    3.1\u00a0\u00a0\u00a0
                Title 2
            <paragraph>
                Paragraph 2.
            <section ids="title-3" names="title\\ 3">
                <title auto="1">
                    <generated classes="sectnum">
                        3.1.1\u00a0\u00a0\u00a0
                    Title 3
                <paragraph>
                    Paragraph 3.
        <section ids="title-4" names="title\\ 4">
            <title auto="1">
                <generated classes="sectnum">
                    3.2\u00a0\u00a0\u00a0
                Title 4
            <paragraph>
                Paragraph 4.
"""],
["""\
.. sectnum::
   :prefix: (5.9.
   :suffix: )
   :start: 3
   \n\
Title 1
=======
Paragraph 1.

Title 2
-------
Paragraph 2.

Title 3
```````
Paragraph 3.

Title 4
-------
Paragraph 4.
""",
"""\
<document source="test data">
    <section ids="title-1" names="title\\ 1">
        <title auto="1">
            <generated classes="sectnum">
                (5.9.3)\u00a0\u00a0\u00a0
            Title 1
        <paragraph>
            Paragraph 1.
        <section ids="title-2" names="title\\ 2">
            <title auto="1">
                <generated classes="sectnum">
                    (5.9.3.1)\u00a0\u00a0\u00a0
                Title 2
            <paragraph>
                Paragraph 2.
            <section ids="title-3" names="title\\ 3">
                <title auto="1">
                    <generated classes="sectnum">
                        (5.9.3.1.1)\u00a0\u00a0\u00a0
                    Title 3
                <paragraph>
                    Paragraph 3.
        <section ids="title-4" names="title\\ 4">
            <title auto="1">
                <generated classes="sectnum">
                    (5.9.3.2)\u00a0\u00a0\u00a0
                Title 4
            <paragraph>
                Paragraph 4.
"""],
])


if __name__ == '__main__':
    unittest.main()
