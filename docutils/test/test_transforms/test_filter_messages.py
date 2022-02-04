#!/usr/bin/env python3

# $Id$
# :Copyright: © 2021 Günter Milde.
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
Tests for docutils.transforms.universal.FilterMessages.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst
from docutils.transforms import universal
from docutils.transforms.references import Substitutions


class TestTransformFilterMessages(unittest.TestCase):
    def test_unknown_directive(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5  # filter all system messages
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        document = utils.new_document('test data', settings.copy())
        rst.Parser().parse('.. unknown-directive:: block markup is filtered without trace.', document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transform(universal.Messages)
        document.transformer.add_transform(universal.FilterMessages)
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()

        output = document.pformat()
        self.assertEqual(output, '<document source="test data">\n')

    def test_unknown_substitution(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5  # filter all system messages
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        document = utils.new_document('test data', settings.copy())
        rst.Parser().parse(unknown_substitution_input, document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transform(Substitutions)
        document.transformer.add_transform(universal.Messages)
        document.transformer.add_transform(universal.FilterMessages)
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()

        output = document.pformat()
        self.assertEqual(output, unknown_substitution_output)

    def test_invalid_inline_markup(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5  # filter all system messages
        settings.halt_level = 5
        settings.debug = False
        settings.warning_stream = False

        document = utils.new_document('test data', settings.copy())
        rst.Parser().parse('Invalid *inline markup is restored to text.', document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transform(universal.Messages)
        document.transformer.add_transform(universal.FilterMessages)
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.apply_transforms()

        output = document.pformat()
        self.assertEqual(output, invalid_inline_output)


invalid_inline_output = """\
<document source="test data">
    <paragraph>
        Invalid \n\
        *
        inline markup is restored to text.
"""

unknown_substitution_input = """\
This |unknown substitution| will generate a system message, thanks to
the "Substitutions" transform. The "Messages" transform will
generate a "System Messages" section and the "FilterMessages" transform
will remove it.
"""

unknown_substitution_output = """\
<document source="test data">
    <paragraph>
        This \n\
        |unknown substitution|
         will generate a system message, thanks to
        the "Substitutions" transform. The "Messages" transform will
        generate a "System Messages" section and the "FilterMessages" transform
        will remove it.
"""


if __name__ == '__main__':
    unittest.main()
