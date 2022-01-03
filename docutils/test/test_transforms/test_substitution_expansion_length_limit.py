#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for docutils.transforms.references.Substitutions.
"""

if __name__ == '__main__':
    import __init__
import unittest
from test_transforms import DocutilsTestSupport
from docutils.transforms.references import Substitutions
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
                                                      suite_settings={'line_length_limit': 80},
                                                      transforms=transforms, parser=parser)
            )
    return s

# pseudoxml representation of the substitution definition content:
a = '        lol'
b = '        10^1 \n' + '\n         \n'.join(10 * [a])
c = '        10^2 \n' + '\n         \n'.join(10 * [b])

totest = {}

totest['substitutions'] = ((Substitutions,), [
["""\
The billion laughs attack for ReStructuredText:

.. |a| replace:: lol
.. |b| replace:: 10^1 |a| |a| |a| |a| |a| |a| |a| |a| |a| |a|
.. |c| replace:: 10^2 |b| |b| |b| |b| |b| |b| |b| |b| |b| |b|
.. ...

|a| |c| continuation text
""",
"""\
<document source="test data">
    <paragraph>
        The billion laughs attack for ReStructuredText:
    <substitution_definition names="a">
        lol
    <substitution_definition names="b">
{}
    <substitution_definition names="c">
{}
    <comment xml:space="preserve">
        ...
    <paragraph>
        lol
         \n\
        <problematic ids="problematic-1" refid="system-message-1">
            |c|
         continuation text
    <system_message backrefs="problematic-1" ids="system-message-1" level="3" line="9" source="test data" type="ERROR">
        <paragraph>
            Substitution definition "c" exceeds the line-length-limit.
""".format(b, c)],
])


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
