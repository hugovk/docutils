#!/usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test for Null writer.
"""

import unittest

import docutils
import docutils.core


class TestNull(unittest.TestCase, docutils.SettingsSpec):

    """
    Test case for publish.
    """

    settings_default_overrides = {"_disable_config": True,
                                  "strict_visitor": True}

    def test_null(self):
        output = docutils.core.publish_string(
            source="This is a paragraph.",
            reader_name="standalone",
            parser_name="restructuredtext",
            writer_name="null",
            settings_spec=self)
        self.assertIsNone(output)


if __name__ == '__main__':
    unittest.main()
