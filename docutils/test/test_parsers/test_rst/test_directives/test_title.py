#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Tests for the 'title' directive.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestTitle(unittest.TestCase):
    def test_title(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        document = utils.new_document('test data', settings)
        rst.Parser().parse('.. title:: This is the document title.', document)
        output = document.pformat()
        self.assertEqual(output, '<document source="test data" title="This is the document title.">\n')


if __name__ == '__main__':
    unittest.main()
