#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for docutils.transforms.references.Hyperlinks with non-English language.

TODO: This test fails currently when run as part of "alltests" because

      - the "info" system-messages for directive fallbacks are only generated
        once (the name -> directive mapping is cached in
        ``docutils.parsers.rst.directives._directives``).

      - the cache is not reset between after processing a document
        (i.e. it contains name -> directive mappings from other tests).

      See also https://sourceforge.net/p/docutils/feature-requests/71/
"""

from test import DocutilsTestSupport
from docutils.transforms.references import PropagateTargets, \
     AnonymousHyperlinks, IndirectHyperlinks, ExternalTargets, \
     InternalTargets, DanglingReferences
from docutils.parsers.rst import Parser, directives
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
                    settings = self.settings.copy()
                    settings.language_code = "de"
                    document = utils.new_document('test data', settings)
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

totest['hyperlinks'] = ((PropagateTargets, AnonymousHyperlinks,
                         IndirectHyperlinks, ExternalTargets,
                         InternalTargets, DanglingReferences), [

["""\
Target_ should propagate past the system_message to set "id" on note.

.. _target:
.. note:: Kurznotiz
   :name: mynote
""",
"""\
<document source="test data">
    <paragraph>
        <reference name="Target" refid="target">
            Target
         should propagate past the system_message to set "id" on note.
    <target refid="target">
    <system_message level="1" line="4" source="test data" type="INFO">
        <paragraph>
            No directive entry for "note" in module "docutils.parsers.rst.languages.de".
            Using English fallback for directive "note".
    <note ids="mynote target" names="mynote target">
        <paragraph>
            Kurznotiz
    <system_message level="1" source="test data" type="INFO">
        <paragraph>
            Using <module 'docutils.languages.de' from '/usr/local/src/docutils-git-svn/docutils/docutils/languages/de.py'> for language "de".
"""],
])

if __name__ == '__main__':
    unittest.main()
