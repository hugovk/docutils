#! /usr/bin/env python3

# $Id$
# Author: Garth Kidd <garth@deadlybloodyserious.com>
# Copyright: This module has been placed in the public domain.

"""
This module extends unittest.py with `loadTestModules()`, by loading multiple
test modules from a directory.  Optionally, test packages are also loaded,
recursively.
"""

import sys
import os
import glob
import importlib
import unittest


def loadTestModules(path, name=''):
    """
    Return a test suite composed of all the tests from modules in a directory.

    Search for modules in directory `path`, beginning with `name`.
    Then search subdirectories (also beginning with `name`)
    recursively.  Subdirectories must be Python packages; they must contain an
    '__init__.py' module.
    """
    testSuite = unittest.TestSuite()
    testModules = []
    path = os.path.abspath(path)        # current working dir if `path` empty
    paths = [path]
    while paths:
        p = paths.pop() + "/" + name
        for file_path in glob.glob(p + "*.py"):
            testModules.append(path2mod(os.path.relpath(file_path, path)))
        for file_path in glob.glob(p + "*/__init__.py"):
            paths.append(os.path.dirname(file_path))
    # Import modules and add their tests to the suite.
    sys.path.insert(0, path)
    for mod in testModules:
        try:
            module = importlib.import_module(mod)
        except ImportError:
            print("ERROR: Can't import %s, skipping its tests:" % mod, file=sys.stderr)
            sys.excepthook(*sys.exc_info())
        else:
            # if there's a suite defined, incorporate its contents
            try:
                suite = module.suite
            except AttributeError:
                # Look for individual tests
                moduleTests = unittest.defaultTestLoader.loadTestsFromModule(module)
                # unittest.TestSuite.addTests() doesn't work as advertised,
                # as it can't load tests from another TestSuite, so we have
                # to cheat:
                testSuite.addTest(moduleTests)
            else:
                if callable(suite):
                    testSuite.addTest(suite())
                else:
                    raise AssertionError("don't understand suite (%s)" % mod)
    sys.path.pop(0)
    return testSuite

def path2mod(path):
    """Convert a file path to a dotted module name."""
    return path[:-3].replace(os.sep, '.')
