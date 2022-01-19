#!/usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test for Null writer.
"""

import unittest
from test import DocutilsTestSupport

import docutils
import docutils.core


class WriterPublishTestCase(DocutilsTestSupport.CustomTestCase, docutils.SettingsSpec):

    """
    Test case for publish.
    """

    settings_default_overrides = {"_disable_config": True,
                                  "strict_visitor": True}
    writer_name = "null"

    def test_publish(self):
        for name, cases in totest.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    output = docutils.core.publish_string(
                        source=case_input,
                        reader_name="standalone",
                        parser_name="restructuredtext",
                        writer_name=self.writer_name,
                        settings_spec=self,
                        settings_overrides=self.overrides)
                    DocutilsTestSupport._compare_output(self, output, case_expected)


totest = {}

totest['basic'] = [
["""\
This is a paragraph.
""",
None]
]

if __name__ == '__main__':
    unittest.main()
