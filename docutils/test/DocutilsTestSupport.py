# $Id$
# Authors: David Goodger <goodger@python.org>;
#          Garth Kidd <garth@deadlybloodyserious.com>
# Copyright: This module has been placed in the public domain.

"""
Exports the following:

:Modules:
    - `statemachine` is 'docutils.statemachine'
    - `nodes` is 'docutils.nodes'
    - `urischemes` is 'docutils.utils.urischemes'
    - `utils` is 'docutils.utils'
    - `transforms` is 'docutils.transforms'
    - `states` is 'docutils.parsers.rst.states'
    - `tableparser` is 'docutils.parsers.rst.tableparser'

:Classes:
    - `CustomTestCase`
    - `ParserTestCase`
    - `ParserTransformTestCase`
    - `LatexWriterPublishTestCase`
    - `PseudoXMLWriterPublishTestCase`
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

import docutils.parsers
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
    def __init__(self, method_name):
        self.overrides = {}

        # Ring your mother.
        super().__init__(method_name)

    def setUp(self):
        super().setUp()
        # Language-specific roles and roles added by the
        # "default-role" and "role" directives are currently stored
        # globally in the roles._roles dictionary.  This workaround
        # empties that dictionary.
        roles._roles = {}


def _compare_output(testcase, input, output, expected):
    """`input` should by bytes, `output` and `expected` strings."""
    if isinstance(expected, bytes):
        expected = expected.decode("utf-8")
    if isinstance(output, bytes):
        output = output.decode("utf-8")
    # Normalize line endings:
    if expected:
        expected = "\n".join(expected.splitlines())
    if output:
        output = "\n".join(output.splitlines())
    testcase.assertEqual(output, expected)


# Optional tests with 3rd party CommonMark parser
# ===============================================

# TODO: test with alternative CommonMark parsers?
md_parser_name = 'recommonmark'
# md_parser_name = 'pycmark'
# md_parser_name = 'myst'
md_skip_msg = f'Cannot test "{md_parser_name}". Parser not found.'
try:
    md_parser_class = docutils.parsers.get_parser_class(
                                                md_parser_name)
except ImportError:
    md_parser_class = None
if md_parser_class and md_parser_name == 'recommonmark':
    import recommonmark
    if recommonmark.__version__ < '0.6.0':
        md_parser_class = None
        md_skip_msg = f'"{md_parser_name}" parser too old, skip tests'


def _format_parts_output(
    parts,
    standard_html_meta_value,
    standard_html_prolog
):
    """Minimize & standardize the output."""
    # remove redundant parts & uninteresting parts:
    del parts['whole']
    assert parts['body'] == parts['fragment']
    del parts['body']
    del parts['body_pre_docinfo']
    del parts['body_prefix']
    del parts['body_suffix']
    del parts['head']
    del parts['head_prefix']
    del parts['encoding']
    del parts['version']
    # remove standard portions:
    parts['meta'] = parts['meta'].replace(standard_html_meta_value % 'utf-8', '')
    parts['html_head'] = parts['html_head'].replace(
        standard_html_meta_value, '...')
    parts['html_prolog'] = parts['html_prolog'].replace(
        standard_html_prolog, '')
    output = []
    for key in sorted(parts.keys()):
        if not parts[key]:
            continue
        output.append("%r: '''%s'''"
                      % (key, parts[key]))
        if output[-1].endswith("\n'''"):
            output[-1] = output[-1][:-4] + "\\n'''"
    return '{' + ',\n '.join(output) + '}\n'


def make_id(path):
    return os.path.relpath(path, testroot)


def exception_data(func, *args, **kwds):
    """
    Execute `func(*args, **kwds)` and return the resulting exception, the
    exception arguments, and the formatted exception string.
    """
    try:
        func(*args, **kwds)
    except Exception as detail:
        return (detail, detail.args,
                '%s: %s' % (detail.__class__.__name__, detail))
    return None, [], "No exception"
