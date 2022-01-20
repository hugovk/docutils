# $Id$
# Authors: David Goodger <goodger@python.org>;
#          Garth Kidd <garth@deadlybloodyserious.com>
# Copyright: This module has been placed in the public domain.

"""
Exports the following:

:Classes:
    - `CustomTestCase`
    - `DevNull` (output sink)
"""
__docformat__ = 'reStructuredText'

import sys
import os
import unittest

testroot = os.path.abspath(os.path.dirname(__file__) or os.curdir)
os.chdir(testroot)
sys.path.insert(0, os.path.dirname(testroot))
sys.path.insert(0, testroot)

from docutils.parsers.rst import roles
from docutils.statemachine import StringList

# Hack to make repr(StringList) look like repr(list):
StringList.__repr__ = StringList.__str__


class DevNull:

    """Output sink."""

    def write(self, string):
        pass

    def close(self):
        pass


class CustomTestCase(unittest.TestCase):
    def setUp(self):
        # Language-specific roles and roles added by the
        # "default-role" and "role" directives are currently stored
        # globally in the roles._roles dictionary.  This workaround
        # empties that dictionary.
        roles._roles = {}


def _compare_output(testcase, output, expected):
    """`input` should by bytes, `output` and `expected` strings."""
    # Normalise line endings:
    if expected:
        expected = "\n".join(expected.splitlines())
    if output:
        output = "\n".join(output.splitlines())
    testcase.assertEqual(output, expected)


def exception_data(func, *args, **kwds):
    """
    Execute `func(*args, **kwds)` and return the resulting exception, the
    exception arguments, and the formatted exception string.
    """
    try:
        func(*args, **kwds)
    except Exception as detail:
        return (detail, detail.args,
                f'{detail.__class__.__name__}: {detail}')
    return None, [], "No exception"
