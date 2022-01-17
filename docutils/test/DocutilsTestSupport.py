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
    - `TransformTestCase`
    - `ParserTestCase`
    - `ParserTransformTestCase`
    - `LatexWriterPublishTestCase`
    - `PseudoXMLWriterPublishTestCase`
    - `DevNull` (output sink)
"""
__docformat__ = 'reStructuredText'

import sys
import os
import difflib
import unittest
from pprint import pformat

testroot = os.path.abspath(os.path.dirname(__file__) or os.curdir)
os.chdir(testroot)
sys.path.insert(0, os.path.dirname(testroot))
sys.path.insert(0, testroot)

import docutils
import docutils.core
import docutils.io
from docutils import frontend, utils
from docutils.transforms import universal
from docutils.parsers import rst
from docutils.parsers.rst import tableparser, roles
from docutils.readers import pep
from docutils.statemachine import StringList, string2lines

# Hack to make repr(StringList) look like repr(list):
StringList.__repr__ = StringList.__str__


class DevNull:

    """Output sink."""

    def write(self, string):
        pass

    def close(self):
        pass


class CustomTestCase(unittest.TestCase):

    """
    Helper class, providing extended functionality over unittest.TestCase.

    See the _compare_output method and the parameter list of __init__.

    Note: the modified signature is incompatible with
    the "pytest" and "nose" frameworks.
    """ # cf. feature-request #81

    def __init__(self, method_name, input=None, expected=None, id="",
                 suite_settings=None):
        """
        Initialise the CustomTestCase.

        Arguments:

        method_name -- name of test method to run.
        input -- input to the parser.
        expected -- expected output from the parser.
        id -- unique test identifier, used by the test framework.
        suite_settings -- settings overrides for this test suite.
        """
        self._id = id
        self.input = input
        self.expected = expected
        if suite_settings:
            self.suite_settings = self.overrides = suite_settings.copy()
        else:
            self.suite_settings = self.overrides = {}

            # Ring your mother.
        super().__init__(method_name)

    def __str__(self):
        """
        Return string conversion. Overridden to give test id, in addition to
        method name.
        """
        return f'{self._id}; {super().__str__()}'

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

class TransformTestCase(CustomTestCase):

    """
    Output checker for the transform.

    Should probably be called TransformOutputChecker, but I can deal with
    that later when/if someone comes up with a category of transform test
    cases that have nothing to do with the input and output of the transform.
    """

    option_parser = frontend.OptionParser(components=(rst.Parser,))
    settings = option_parser.get_default_values()
    settings.report_level = 1
    settings.halt_level = 5
    settings.debug = False
    settings.warning_stream = DevNull()
    unknown_reference_resolvers = ()

    def __init__(self, *args, parser=None, transforms=None, **kwargs):
        assert transforms is not None, 'required argument'
        self.transforms = transforms
        """List of transforms to perform for this test case."""

        assert parser is not None, 'required argument'
        self.parser = parser
        """Input parser for this test case."""

        super().__init__(*args, **kwargs)

    def test_transforms(self):
        settings = self.settings.copy()
        settings.__dict__.update(self.suite_settings)
        document = utils.new_document('test data', settings)
        self.parser.parse(self.input, document)
        # Don't do a ``populate_from_components()`` because that would
        # enable the Transformer's default transforms.
        document.transformer.add_transforms(self.transforms)
        document.transformer.add_transform(universal.TestMessages)
        document.transformer.components['writer'] = self
        document.transformer.apply_transforms()
        output = document.pformat()
        _compare_output(self, self.input, output, self.expected)

    def test_transforms_verbosely(self):
        print('\n', self.id)
        print('-' * 70)
        print(self.input)
        settings = self.settings.copy()
        settings.__dict__.update(self.suite_settings)
        document = utils.new_document('test data', settings)
        self.parser.parse(self.input, document)
        print('-' * 70)
        print(document.pformat())
        for transformClass in self.transforms:
            transformClass(document).apply()
        output = document.pformat()
        print('-' * 70)
        print(output)
        _compare_output(self, self.input, output, self.expected)


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
