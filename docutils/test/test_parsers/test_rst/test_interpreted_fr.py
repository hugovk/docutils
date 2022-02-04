#! /usr/bin/env python3

# $Id: test_interpreted.py 6424 2010-09-18 10:43:52Z smerten $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for interpreted text in docutils/parsers/rst/states.py.
Test not default/fallback language french.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestInterpretedFrench(unittest.TestCase):
    def test_basics(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        settings.language_code = 'fr'
        parser = rst.Parser()

        document = utils.new_document('test data', settings.copy())
        parser.parse(basics_input, document)
        output = document.pformat()
        self.assertEqual(output, basics_output)


basics_input = """\
Simple explicit roles and english fallbacks:
:acronym:`acronym`,
:exp:`superscript`,
:ind:`subscript`,
:titre:`title reference`.
"""

basics_output = """\
<document source="test data">
    <paragraph>
        Simple explicit roles and english fallbacks:
        <acronym>
            acronym
        ,
        <superscript>
            superscript
        ,
        <subscript>
            subscript
        ,
        <title_reference>
            title reference
        .
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            No role entry for "acronym" in module "docutils.parsers.rst.languages.fr".
            Using English fallback for role "acronym".
"""

if __name__ == '__main__':
    unittest.main()
