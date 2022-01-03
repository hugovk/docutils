#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test module for writer_aux transforms.
"""

if __name__ == '__main__':
    import __init__
import unittest
from test import DocutilsTestSupport # before importing docutils!
from docutils.transforms import writer_aux
from docutils.parsers.rst import Parser

def suite():
    parser = Parser()
    suite_id = DocutilsTestSupport.make_id(__file__)
    s = unittest.TestSuite()
    for name, (transforms, cases) in totest.items():
        for casenum, (case_input, case_expected) in enumerate(cases):
            s.addTest(
                DocutilsTestSupport.TransformTestCase("test_transforms",
                                                      input=case_input, expected=case_expected,
                                                      id='%s: totest[%r][%s]' % (suite_id, name, casenum),
                                                      suite_settings={},
                                                      transforms=transforms, parser=parser)
            )
    return s


totest = {}

totest['admonitions'] = ((writer_aux.Admonitions,), [
["""\
.. note::

   These are the note contents.

   Another paragraph.
""",
"""\
<document source="test data">
    <admonition classes="note">
        <title>
            Note
        <paragraph>
            These are the note contents.
        <paragraph>
            Another paragraph.
"""],
["""\
.. admonition:: Generic

   Admonitions contents...
""",
"""\
<document source="test data">
    <admonition classes="admonition-generic admonition">
        <title>
            Generic
        <paragraph>
            Admonitions contents...
"""],
])


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
