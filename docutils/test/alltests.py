#!/bin/sh
''''exec python3 -u "$0" "$@" #'''

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

__doc__ = """\
All modules named 'test_*.py' in the current directory, and recursively in
subdirectories (packages) called 'test_*', are loaded and test suites within
are run.
"""

import time
# Start point for actual elapsed time, including imports
# and setup outside of unittest.
start = time.time()  # noqa

import importlib
from pathlib import Path
import platform
import sys
import traceback
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))
from test import DocutilsTestSupport              # must be imported before docutils

import docutils


def load_test_modules(root):
    """
    Return a test suite composed of all the tests from modules in a directory.

    Search for modules in directory `path`, beginning with `name`.
    Then search subdirectories (also beginning with `name`)
    recursively.  Subdirectories must be Python packages; they must contain an
    '__init__.py' module.
    """
    test_suite = unittest.TestSuite()
    test_modules = []
    root = Path(root).absolute()        # current working dir if `path` empty
    paths = [root]
    while paths:
        p = paths.pop()
        for path in p.glob("test_*.py"):
            mod = ".".join(path.relative_to(root).parts).removesuffix(".py")
            test_modules.append(mod)
        for path in p.glob("test_*/__init__.py"):
            paths.append(path.parent)
    # Import modules and add their tests to the suite.
    sys.path.insert(0, str(root))
    for mod in test_modules:
        try:
            module = importlib.import_module(mod)
        except ImportError:
            print(f"ERROR: Can't import {mod}, skipping its tests:", file=sys.stderr)
            traceback.print_exc()
        else:
            # if there's a suite defined, incorporate its contents
            try:
                module_tests = module.suite
            except AttributeError:
                # Look for individual tests
                module_tests = unittest.defaultTestLoader.loadTestsFromModule(module)
                # unittest.TestSuite.addTests() doesn't work as advertised,
                # as it can't load tests from another TestSuite, so we have
                # to cheat:
                test_suite.addTest(module_tests)
            else:
                if callable(module_tests):
                    test_suite.addTest(module_tests())
                else:
                    raise AssertionError("don't understand suite (%s)" % mod)
    sys.path.pop(0)
    return test_suite


if __name__ == '__main__':
    suite = load_test_modules(DocutilsTestSupport.testroot)
    print(f'Testing Docutils {docutils.__version__} with '
          f'Python {sys.version.split()[0]} on {time.strftime("%Y-%m-%d")} '
          f'at {time.strftime("%H:%M:%S")}')
    print(f'OS: {platform.system()} {platform.release()} {platform.version()} '
          f'({sys.platform}, {platform.platform()})')
    print(f'Working directory: {Path().cwd()}')
    print(f'Docutils package: {Path(docutils.__file__).parent}')
    sys.stdout.flush()
    result = unittest.TextTestRunner().run(suite)
    finish = time.time()
    print(f'Elapsed time: {finish - start:.3f} seconds')
    sys.exit(not result.wasSuccessful())
