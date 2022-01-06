#!/usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the S5/HTML writer.
"""

import os
import platform

import unittest
from test import DocutilsTestSupport

class WriterPublishTestCase(DocutilsTestSupport.WriterPublishTestCase):
    writer_name = "s5"
    overrides = {'stylesheet_path': '/test.css',
                 'embed_stylesheet': 0,}

    def test_publish(self):
        for name, cases in totest_1.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    super()._support_publish(input=case_input, expected=case_expected)

        self.overrides['hidden_controls'] = 0
        self.overrides['view_mode'] = 'outline'
        for name, cases in totest_2.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    super()._support_publish(input=case_input, expected=case_expected)


interpolations = {
        'version': DocutilsTestSupport.docutils.__version__,
        'drive': '', }

if platform.system() == 'Windows':
    interpolations['drive'] = os.path.splitdrive(os.getcwd())[0]

totest_1 = {}
totest_2 = {}

totest_1['basics'] = [
["""\
============
 Show Title
============

Title slide

First Slide
===========

Slide text.
""",
"""\
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="generator" content="Docutils %(version)s: https://docutils.sourceforge.io/" />
<meta name="version" content="S5 1.1" />
<title>Show Title</title>
<link rel="stylesheet" href="%(drive)s/test.css" type="text/css" />
<!-- configuration parameters -->
<meta name="defaultView" content="slideshow" />
<meta name="controlVis" content="hidden" />
<!-- style sheet links -->
<script src="ui/default/slides.js" type="text/javascript"></script>
<link rel="stylesheet" href="ui/default/slides.css"
      type="text/css" media="projection" id="slideProj" />
<link rel="stylesheet" href="ui/default/outline.css"
      type="text/css" media="screen" id="outlineStyle" />
<link rel="stylesheet" href="ui/default/print.css"
      type="text/css" media="print" id="slidePrint" />
<link rel="stylesheet" href="ui/default/opera.css"
      type="text/css" media="projection" id="operaFix" />

<style type="text/css">
#currentSlide {display: none;}
</style>
</head>
<body>
<div class="layout">
<div id="controls"></div>
<div id="currentSlide"></div>
<div id="header">

</div>
<div id="footer">
<h1>Show Title</h1>

</div>
</div>
<div class="presentation">
<div class="slide" id="slide0">
<h1 class="title">Show Title</h1>

<p>Title slide</p>

</div>
<div class="slide" id="first-slide">
<h1>First Slide</h1>
<p>Slide text.</p>
</div>
</div>
</body>
</html>
""" % interpolations]
]

totest_2['settings'] = [
["""\
==================
 Bogus Slide Show
==================

We're just checking the settings
""",
"""\
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="generator" content="Docutils %(version)s: https://docutils.sourceforge.io/" />
<meta name="version" content="S5 1.1" />
<title>Bogus Slide Show</title>
<link rel="stylesheet" href="%(drive)s/test.css" type="text/css" />
<!-- configuration parameters -->
<meta name="defaultView" content="outline" />
<meta name="controlVis" content="visible" />
<!-- style sheet links -->
<script src="ui/default/slides.js" type="text/javascript"></script>
<link rel="stylesheet" href="ui/default/slides.css"
      type="text/css" media="projection" id="slideProj" />
<link rel="stylesheet" href="ui/default/outline.css"
      type="text/css" media="screen" id="outlineStyle" />
<link rel="stylesheet" href="ui/default/print.css"
      type="text/css" media="print" id="slidePrint" />
<link rel="stylesheet" href="ui/default/opera.css"
      type="text/css" media="projection" id="operaFix" />

<style type="text/css">
#currentSlide {display: none;}
</style>
</head>
<body>
<div class="layout">
<div id="controls"></div>
<div id="currentSlide"></div>
<div id="header">

</div>
<div id="footer">
<h1>Bogus Slide Show</h1>

</div>
</div>
<div class="presentation">
<div class="slide" id="slide0">
<h1 class="title">Bogus Slide Show</h1>

<p>We're just checking the settings</p>
</div>
</div>
</body>
</html>
""" % interpolations]
]

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
