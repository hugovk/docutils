#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for `docutils.transforms.parts.Contents` (via
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

totest['tables_of_contents'] = ((Substitutions,), [
["""\
.. contents::

Title 1
=======
Paragraph 1.

Title_ 2
--------
Paragraph 2.

_`Title` 3
``````````
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
        <bullet_list>
            <list_item>
                <paragraph>
                    <reference ids="toc-entry-1" refid="title-1">
                        Title 1
                <bullet_list>
                    <list_item>
                        <paragraph>
                            <reference ids="toc-entry-2" refid="title-2">
                                Title
                                 2
                        <bullet_list>
                            <list_item>
                                <paragraph>
                                    <reference ids="toc-entry-3" refid="title-3">
                                        Title
                                         3
                    <list_item>
                        <paragraph>
                            <reference ids="toc-entry-4" refid="title-4">
                                Title 4
    <section ids="title-1" names="title\\ 1">
        <title refid="toc-entry-1">
            Title 1
        <paragraph>
            Paragraph 1.
        <section ids="title-2" names="title\\ 2">
            <title>
                <reference name="Title" refname="title">
                    Title
                 2
            <paragraph>
                Paragraph 2.
            <section ids="title-3" names="title\\ 3">
                <title refid="toc-entry-3">
                    <target ids="title" names="title">
                        Title
                     3
                <paragraph>
                    Paragraph 3.
        <section ids="title-4" names="title\\ 4">
            <title refid="toc-entry-4">
                Title 4
            <paragraph>
                Paragraph 4.
"""],
["""\
.. contents:: Table of Contents

Title 1
=======
Paragraph 1.

Title 2
-------
Paragraph 2.
""",
"""\
<document source="test data">
    <topic classes="contents" ids="table-of-contents" names="table\\ of\\ contents">
        <title>
            Table of Contents
        <bullet_list>
            <list_item>
                <paragraph>
                    <reference ids="toc-entry-1" refid="title-1">
                        Title 1
                <bullet_list>
                    <list_item>
                        <paragraph>
                            <reference ids="toc-entry-2" refid="title-2">
                                Title 2
    <section ids="title-1" names="title\\ 1">
        <title refid="toc-entry-1">
            Title 1
        <paragraph>
            Paragraph 1.
        <section ids="title-2" names="title\\ 2">
            <title refid="toc-entry-2">
                Title 2
            <paragraph>
                Paragraph 2.
"""],
["""\
.. contents:: There's an image in Title 2

Title 1
=======
Paragraph 1.

|Title 2|
=========
Paragraph 2.

.. |Title 2| image:: title2.png
""",
"""\
<document source="test data">
    <topic classes="contents" ids="there-s-an-image-in-title-2" names="there's\\ an\\ image\\ in\\ title\\ 2">
        <title>
            There's an image in Title 2
        <bullet_list>
            <list_item>
                <paragraph>
                    <reference ids="toc-entry-1" refid="title-1">
                        Title 1
            <list_item>
                <paragraph>
                    <reference ids="toc-entry-2" refid="title-2">
                        Title 2
    <section ids="title-1" names="title\\ 1">
        <title refid="toc-entry-1">
            Title 1
        <paragraph>
            Paragraph 1.
    <section ids="title-2" names="title\\ 2">
        <title refid="toc-entry-2">
            <image alt="Title 2" uri="title2.png">
        <paragraph>
            Paragraph 2.
        <substitution_definition names="Title\\ 2">
            <image alt="Title 2" uri="title2.png">
"""],                                   # emacs cruft: "
["""\
.. contents::
   :depth: 2

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
        <bullet_list>
            <list_item>
                <paragraph>
                    <reference ids="toc-entry-1" refid="title-1">
                        Title 1
                <bullet_list>
                    <list_item>
                        <paragraph>
                            <reference ids="toc-entry-2" refid="title-2">
                                Title 2
                    <list_item>
                        <paragraph>
                            <reference ids="toc-entry-3" refid="title-4">
                                Title 4
    <section ids="title-1" names="title\\ 1">
        <title refid="toc-entry-1">
            Title 1
        <paragraph>
            Paragraph 1.
        <section ids="title-2" names="title\\ 2">
            <title refid="toc-entry-2">
                Title 2
            <paragraph>
                Paragraph 2.
            <section ids="title-3" names="title\\ 3">
                <title>
                    Title 3
                <paragraph>
                    Paragraph 3.
        <section ids="title-4" names="title\\ 4">
            <title refid="toc-entry-3">
                Title 4
            <paragraph>
                Paragraph 4.
"""],
["""\
Title 1
=======

.. contents::
   :local:

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
        <title>
            Title 1
        <topic classes="contents local" ids="contents" names="contents">
            <bullet_list>
                <list_item>
                    <paragraph>
                        <reference ids="toc-entry-1" refid="title-2">
                            Title 2
                    <bullet_list>
                        <list_item>
                            <paragraph>
                                <reference ids="toc-entry-2" refid="title-3">
                                    Title 3
                <list_item>
                    <paragraph>
                        <reference ids="toc-entry-3" refid="title-4">
                            Title 4
        <paragraph>
            Paragraph 1.
        <section ids="title-2" names="title\\ 2">
            <title refid="toc-entry-1">
                Title 2
            <paragraph>
                Paragraph 2.
            <section ids="title-3" names="title\\ 3">
                <title refid="toc-entry-2">
                    Title 3
                <paragraph>
                    Paragraph 3.
        <section ids="title-4" names="title\\ 4">
            <title refid="toc-entry-3">
                Title 4
            <paragraph>
                Paragraph 4.
"""],
["""\
.. contents::
   :local:

Test duplicate name "Contents".

Section
--------
Paragraph.
""",
"""\
<document source="test data">
    <topic classes="contents local" ids="contents" names="contents">
        <bullet_list>
            <list_item>
                <paragraph>
                    <reference ids="toc-entry-1" refid="section">
                        Section
    <paragraph>
        Test duplicate name "Contents".
    <section ids="section" names="section">
        <title refid="toc-entry-1">
            Section
        <paragraph>
            Paragraph.
"""],
["""\
.. contents::
   :backlinks: top

Section
--------
Paragraph.
""",
"""\
<document source="test data">
    <topic classes="contents" ids="contents" names="contents">
        <title>
            Contents
        <bullet_list>
            <list_item>
                <paragraph>
                    <reference ids="toc-entry-1" refid="section">
                        Section
    <section ids="section" names="section">
        <title refid="contents">
            Section
        <paragraph>
            Paragraph.
"""],
["""\
.. contents::
   :backlinks: none

Section
--------
Paragraph.
""",
"""\
<document source="test data">
    <topic classes="contents" ids="contents" names="contents">
        <title>
            Contents
        <bullet_list>
            <list_item>
                <paragraph>
                    <reference ids="toc-entry-1" refid="section">
                        Section
    <section ids="section" names="section">
        <title>
            Section
        <paragraph>
            Paragraph.
"""],
["""\
.. contents::

Degenerate case, no table of contents generated.
""",
"""\
<document source="test data">
    <paragraph>
        Degenerate case, no table of contents generated.
"""],
["""\
Title 1
=======

Paragraph 1.

.. sidebar:: Contents

   .. contents::
      :local:

Title 2
-------
Paragraph 2.

Title 3
```````
Paragraph 3.
""",
"""\
<document source="test data">
    <section ids="title-1" names="title\\ 1">
        <title>
            Title 1
        <paragraph>
            Paragraph 1.
        <sidebar>
            <title>
                Contents
            <topic classes="contents local" ids="contents" names="contents">
                <bullet_list>
                    <list_item>
                        <paragraph>
                            <reference ids="toc-entry-1" refid="title-2">
                                Title 2
                        <bullet_list>
                            <list_item>
                                <paragraph>
                                    <reference ids="toc-entry-2" refid="title-3">
                                        Title 3
        <section ids="title-2" names="title\\ 2">
            <title refid="toc-entry-1">
                Title 2
            <paragraph>
                Paragraph 2.
            <section ids="title-3" names="title\\ 3">
                <title refid="toc-entry-2">
                    Title 3
                <paragraph>
                    Paragraph 3.
"""],
])


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
