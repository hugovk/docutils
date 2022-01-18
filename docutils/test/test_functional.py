#!/usr/bin/env python3
# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Perform tests with the data in the functional/ directory.

Please see the documentation on `functional testing`__ for details.

__ ../../docs/dev/testing.html#functional
"""

import sys
import os
import os.path
import shutil
import unittest
import difflib
from pathlib import Path

from test import DocutilsTestSupport              # must be imported before docutils
import docutils
import docutils.core


datadir = 'functional'
"""The directory to store the data needed for the functional tests."""


def join_path(*args):
    return '/'.join(args) or '.'


def clear_output_directory():
    for entry in os.scandir(Path("functional", "output")):
        if os.path.isdir(entry):
            shutil.rmtree(entry)
        elif entry.name != "README.txt":
            os.unlink(entry)


no_expected_template = """\
Cannot find expected output at %(exp)s
If the output in %(out)s
is correct, move it to the expected/ dir and check it in:

  mv %(out)s %(exp)s
  svn add %(exp)s
  svn commit -m "<comment>" %(exp)s"""

expected_output_differs_template = """\
The expected and actual output differs.
Please compare the expected and actual output files:

  diff %(exp)s %(out)s\n'

If the actual output is correct, please replace the
expected output and check it in:

  mv %(out)s %(exp)s
  svn add %(exp)s
  svn commit -m "<comment>" %(exp)s"""


class FunctionalTestCase(DocutilsTestSupport.CustomTestCase):

    """Test case for one config file."""

    def setUp(self):
        clear_output_directory()

    def test(self):
        """Process configfile."""
        for path in Path(datadir, 'tests').rglob("[!_]*.py"):  # TODO document recursion not allowed and switch to .glob
            configfile = path.as_posix()
            print(configfile)
            with self.subTest("message", configfile=configfile):
                # Keyword parameters for publish_file:
                namespace = {}
                # Initialize 'settings_overrides' for test settings scripts:
                namespace['settings_overrides'] = {
                    # disable configuration files
                    '_disable_config': True,
                    # Default settings for all tests.
                    'report_level': 2,
                    'halt_level': 5,
                    'warning_stream': '',
                    'input_encoding': 'utf-8',
                    'embed_stylesheet': False,
                    'auto_id_prefix': '%',
                    # avoid "Pygments not found"
                    'syntax_highlight': 'none'
                }
                # Read the variables set in the default config file and in
                # the current config file into namespace:
                with open(configfile) as f:
                    exec(f.read(), namespace)
                # Check for required settings:
                assert 'test_source' in namespace,\
                       "No 'test_source' supplied in " + configfile
                assert 'test_destination' in namespace,\
                       "No 'test_destination' supplied in " + configfile
                # Set source_path and destination_path if not given:
                namespace.setdefault('source_path',
                                     join_path(datadir, 'input',
                                               namespace['test_source']))
                # Path for actual output:
                namespace.setdefault('destination_path',
                                     join_path(datadir, 'output',
                                               namespace['test_destination']))
                # Path for expected output:
                expected_path = join_path(datadir, 'expected',
                                          namespace['test_destination'])
                # shallow copy of namespace to minimize:
                params = namespace.copy()
                # remove unneeded parameters:
                del params['test_source']
                del params['test_destination']
                # Delete private stuff like params['__builtins__']:
                for key in list(params.keys()):
                    if key.startswith('_'):
                        del params[key]
                # Get output (automatically written to the output/ directory
                # by publish_file):
                output = docutils.core.publish_file(**params)
                # ensure output is unicode
                output_encoding = params.get('output_encoding', 'utf-8')
                # Normalize line endings:
                output = '\n'.join(output.splitlines())
                # Get the expected output *after* writing the actual output.
                no_expected = no_expected_template % {
                    'exp': expected_path, 'out': params['destination_path']}
                self.assertTrue(os.access(expected_path, os.R_OK), no_expected)
                # samples are UTF8 encoded. 'rb' leads to errors with Python 3!
                f = open(expected_path, 'r', encoding='utf-8')
                # Normalize line endings:
                expected = '\n'.join(f.read().splitlines())
                f.close()
        
                diff = expected_output_differs_template % {
                    'exp': expected_path, 'out': params['destination_path']}
                try:
                    self.assertEqual(output, expected, diff)
                except AssertionError:
                    diff = ''.join(difflib.unified_diff(
                        expected.splitlines(True), output.splitlines(True),
                        expected_path, params['destination_path']))
                    print('\n%s:' % (self,), file=sys.stderr)
                    print(diff, file=sys.stderr)
                    raise
                # Execute optional function containing extra tests:
                if '_test_more' in namespace:
                    namespace['_test_more'](join_path(datadir, 'expected'),
                                            join_path(datadir, 'output'),
                                            self, namespace)


if __name__ == '__main__':
    unittest.main()
