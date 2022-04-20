#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for admonition directives with local language module.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestAdmonitionsDummy(unittest.TestCase):
    def test_admonitions_dummy(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        settings.language_code = 'local-dummy-lang'
        settings.report_level = 2  # warning (has no effect on test output is run as __main__).

        document = utils.new_document('test data', settings)
        rst.Parser().parse(admonitions_dummy_input, document)
        output = document.pformat()
        self.assertEqual(output, admonitions_dummy_output)


admonitions_dummy_input = """\
.. Dummy-Attention:: directive with silly localised name.

.. Attention:: English fallback (an INFO is written).
"""

admonitions_dummy_output = """\
<document source="test data">
    <attention>
        <paragraph>
            directive with silly localised name.
    <attention>
        <paragraph>
            English fallback (an INFO is written).
"""


if __name__ == '__main__':
    unittest.main()
