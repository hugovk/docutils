#!/usr/bin/env python3
"""Runs all test modules, searching recursively from "docutils/test"."""

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

from pathlib import Path
import platform
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))
from test import DocutilsTestSupport  # must be imported before docutils

import docutils

STARTUP_MESSAGE = f"""\
Testing Docutils {docutils.__version__} with Python {sys.version.split()[0]}
OS: {platform.system()} {platform.release()} {platform.version()} ({sys.platform}, {platform.platform()})
Working directory: {Path.cwd()}
Docutils package: {Path(docutils.__file__).parent}"""

if __name__ == '__main__':
    print(STARTUP_MESSAGE)
    sys.stdout.flush()
    suite = unittest.defaultTestLoader.discover(DocutilsTestSupport.testroot)
    result = unittest.TextTestRunner().run(suite)
    raise SystemExit(not result.wasSuccessful())
