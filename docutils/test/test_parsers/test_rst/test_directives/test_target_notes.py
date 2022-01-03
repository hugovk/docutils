#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the target-notes directives.
"""

import unittest
from test import DocutilsTestSupport


def suite():
    suite_id = DocutilsTestSupport.make_id(__file__)
    s = unittest.TestSuite()
    for name, cases in totest.items():
        for casenum, (case_input, case_expected) in enumerate(cases):
            s.addTest(
                DocutilsTestSupport.ParserTestCase("test_parser",
                                     input=case_input, expected=case_expected,
                                     id='%s: totest[%r][%s]' % (suite_id, name, casenum),
                                     suite_settings={})
            )
    return s

totest = {}

totest['target-notes'] = [
["""\
.. target-notes::
""",
"""\
<document source="test data">
    <pending>
        .. internal attributes:
             .transform: docutils.transforms.references.TargetNotes
             .details:
"""],
["""\
.. target-notes:: :class: custom
""",
"""\
<document source="test data">
    <pending>
        .. internal attributes:
             .transform: docutils.transforms.references.TargetNotes
             .details:
               class: ['custom']
"""],
["""\
.. target-notes::
   :class: custom
   :name: targets
""",
"""\
<document source="test data">
    <pending ids="targets" names="targets">
        .. internal attributes:
             .transform: docutils.transforms.references.TargetNotes
             .details:
               class: ['custom']
"""],
["""\
.. target-notes::
   :class:
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Error in "target-notes" directive:
            invalid option value: (option: "class"; value: None)
            argument required but none supplied.
        <literal_block xml:space="preserve">
            .. target-notes::
               :class:
"""],
]


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
